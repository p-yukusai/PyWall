<h1 align="center">
<img  src="https://raw.githubusercontent.com/p-yukusai/PyWall/master/img/PyWall.png" height="100" width="100">
<p>
🔥PyWall🔥
</p>
</h1>

<p align="center">
    A simple app that makes firewall rules easy.
</p>

<h1 align="center">
<a href=https://github.com/p-yukusai/PyWall/blob/master/LICENSE>
  <img alt="Licence" src="https://img.shields.io/github/license/p-yukusai/PyWall?style=for-the-badge">
</a>
<a href=https://ko-fi.com/V7V04YLC3>
  <img alt="ko-fi" src="https://img.shields.io/badge/Donate-Support%20me%20on%20Ko--Fi-red?style=for-the-badge&logo=ko-fi">
</a>
<a href=https://github.com/p-yukusai/PyWall/actions>
    <img alt="Build" src="https://img.shields.io/github/workflow/status/p-yukusai/PyWall/PyWall%20CI?style=for-the-badge">
</a>
</h1>

# PyWall

PyWall is a Python-based firewall application. This tool helps manage network traffic by filtering incoming and outgoing connections based on configurable rules.

## Features

- Configure firewall rules
- Monitor network traffic
- Block or allow connections based on IP, port, or application
- User-friendly interface

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/PyWall.git
cd PyWall

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## What is it? 🔐

This is a small application, written in Python and Qt, that makes it easy to block or allow internet access to certain files or folders, it contains a graphical user interface and a shell extension, so you may choose between the benefits of an easy-to-use GUI app with the efficiency of just right-clicking any folder or file for maximum convenience! <br />
PyWall was heavily inspired by [OneClickFirewall](https://winaero.com/oneclickfirewall/) by Winaero, and you should totally check that app out!

## What does it do? 🔓

This app essentially writes a rule to the [Windows Firewall](#technical-explanation-) to deny access to just about anything, by default only executable files will be taken into consideration; as a consequence of interacting directly with the Firewall, this app requires elevation to properly work.<br /> Pywall does not and cannot allow internet access for apps that have already been blocked by means other than itself, for instance, any custom firewalls, existing rules, WFP, etc.<br/><br />

This program has the ability to block or allow almost any file, it can even do so with entire folders of them (which was the main reason behind its development, since OneClickFirewall lacks the ability to do so 👀), the way it does this is by sorting through the entire folder to look for all files with a [matching type](#parsing), then it will either block or allow all matches, this also scans all sub-folders by default, meaning that *every* folder inside the initial selection will be scanned, so please be careful with what you select!<br /><br />
PyWall can write and delete both [Inbound and Outbound rules](https://superuser.com/questions/48343/what-are-inbound-and-outbound-rules-for-windows-firewall).
The code was written (to the best of my ability) with the intent of being read by just about anyone, so go right ahead and look through my spaghetti code by yourself if you want to know how the app works in more detail!

## Technical explanation 👩‍🔬

#### Tl;dr

PyWall essentially runs a command from an elevated prompt to either add or remove (if it exists) a rule from the Windows Firewall, needless to say, you *need* to have your firewall active to make any practical use of this program, additionally, it uses PyQt5 with qt-material to draw the GUI, winotify to create toast notifications and context_menu, combined with some custom regkey manipulation, to create the context menu.

#### The command

The command runs from the [src/cmdWorker.py](https://github.com/p-yukusai/PyWall/blob/master/src/cmdWorker.py) script, and it goes along these lines:

```cmd
@echo off && netsh advfirewall firewall add rule name="PyWall blocked {Program Name}" dir={rule type} program="{p}"
```

- "@echo off" means that the command line won't show up while running the script.
- "netsh advfirewall firewall" allows interaction with the rules of the firewall, in the program "Allow Internet Access" will *delete* the rule if it exists and "Deny Internet Access" will *add* it.
- "dir" means the direction of the connection, whether Inbound or Outbound.

#### Parsing

What the program does when the user attempts to allow or deny the internet access varies depending on the path detected being either a file or a directory.

The program has two variables that define what will and won't be considered in the parse, these are "blacklisted_names" and "accepted_types", the former is a list of all filenames (e.g. Discord, Chrome, etc.) that *won't* be considered by the parser and the latter is a list of all accepted suffixes (e.g.: .exe, .msi, etc.) that *will* be considered by the parser.

For files, it's fairly simple, the variable that will be used to run the command is just the path from the file selected, for folders it will check if "recursive" in the config file is set to true or false, if true it will check the folder and all sub-folders for matches, otherwise only the initial folder will be scanned, either way, the variable will be a list containing one or more paths to all accepted matches, which will later be allowed or blocked by the command.
The command is run for each item detected.

## Is PyWall malware?! ☣️

#### No

As previously mentioned, this app interacts directly with the firewall, this is done via [console command](#the-command) through the use of the OS library from Python and as such it requires elevation to work, this in and of itself should *not* trigger any alert, but the app gets flagged as a Trojan regardless by some security software, why is this?<br/>

The most likely immediate cause of this issue is the use of PyInstaller to compile the program into an executable, which has quite the [history](https://github.com/pyinstaller/pyinstaller/issues?q=is%3Aissue+virus+is%3Aclosed+) with AV's falsely detecting executables created with it as Trojans, as a consequence of this Microsoft's AV has wrongly flagged this app as "malicious", this is what's commonly described as a [false positive](https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/images/false-positives-overview.png?view=o365-worldwide).<br/>

As seen in the attached [VirusTotal report](https://www.virustotal.com/gui/file/912c520ef7beda3e561d09c48140905181b6c2d823bab45fff21144297158abc?nocache=1), better antiviruses than Microsoft's offer do *not* detect PyWall as malware, that's because it isn't, a lot of apps compiled with PyInstaller and, in general, software that interacts with the security of the system have this same issue, even OneClickFirewall has a [similar issue](https://www.virustotal.com/gui/file/c5b2fd236c9430b2d8ed48d6b08526753ecc47f2246af668e3b757cc54cd26e5), though greatly reduced, this is *probably* due to the compiler itself, and not any significant deviation of what the code actually does, since as far as I'm able to tell the aforementioned software uses the same method to deny or allow internet access, that being, to write a rule directly to the firewall.<br/><br/>

You are free to read the code and compile it yourself, and, while the releases are taken directly from the artifacts to create the installer, you may download them from the GitHub CI anyway by clicking on the latest run [here](https://github.com/p-yukusai/PyWall/actions) (as the [process](https://github.com/p-yukusai/PyWall/actions/workflows/main.yml) and [code](https://github.com/p-yukusai/PyWall/blob/master/.github/workflows/main.yml) by which the program is compiled are freely available for anyone to see and scrutinize) and review/use the [.iss script](https://github.com/p-yukusai/PyWall/blob/master/PyWall%20Installer.iss) used to create the installer available in the "releases" section.

## PSA 🌠

I believe it to be important to remind people of the potential dangers of programs that interact with the security features of your system, this is why it is so valuable to be able to review what a certain piece software does and doesn't do, as such, please exercise caution with what you install on your system!<br/> If you do not trust a particular piece of software, you can just not install it, use a sandbox or block its internet access to make having it on your system a bit more secure, and, since you're already here, why not use PyWall for the latter? 😉.
