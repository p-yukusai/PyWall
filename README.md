<h1 align="center">
<img  src="https://raw.githubusercontent.com/p-yukusai/PyWall/master/img/PyWall.png" height="100" width="100">
</p>
PyWall
</h1>

<p align="center">
    A small app to make it easy to administrate simple firewall configurations.
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
  
## What is it? 🔐

This is a small application, written in Python and Qt, that makes it easy to block or allow applications from access to the internet, it contains a graphical user interface and a shell extension, so you may choose between the benefits of an easy-to-use GUI app with the efficiency of just right clicking any folder or file for maximum convinience! <br />
PyWall was heavily inspired by [OneClickFirewall](https://winaero.com/oneclickfirewall/) by Winaero, and you should totally check that app out!

## What does it do? 🔓
This app esentially writes a rule to the [Windows Firewall](#technical-explination-) to deny access to just about anything, by default only executable files will be taken into consideration; as a consequence of interacting directly with the Firewall, this app requires elevation to properly work.<br /> Pywall does not and cannot allow internet access for apps that have already been blocked by means other than itself, for instance, any custom firewalls, existing rules, WFP, etc.<br/><br />

This program has the ability to block or allow almost any file, it can even do so with entire folders of them (which was the main reason behind its development, since OneClickFirewall lacks the ability to do so 👀), the way it does this is by sorting through the entire folder to look for all files with a [matching type](#parsing), then it will either block or allow all matches, this also scans all sub-folders by default, meaning that *every* folder inside the initial selection will be scanned, so please be careful with what you select!<br /><br />
The code was written (to the best of my ability) with the intent of being read by just about anyone, so go right ahead and look through my spaguetti code by yourself if you want to know how the app works in more detail!

## Is PyWall malware?! ☣️
#### No.
As previously mentioned, this app interacts directly with the firewall, this is done via [console command](#the-command) through the use of the OS library from Python and as such it requires elevation to work, this in and of itself should *not* trigger any alert, but the app gets flagged as a Trojan regardless by some security software, why is this?<br/>
The most likely immediate cause of this issue is the use of PyInstaller to compile the program into an executable, which has quite the [history](https://github.com/pyinstaller/pyinstaller/issues?q=is%3Aissue+virus+is%3Aclosed+) with AV's falsely detecting executables created with it as Trojans, as a consequence of this [five antivirus vendors](## "Antiy-AVL, VBA32, Zillya, Yandex and Microsoft") have wrongly flagged this app as "malicious", this is what's commonly described as a [false positive](https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/images/false-positives-overview.png?view=o365-worldwide).<br/>

As seen in the attatched [VirusTotal report](https://www.virustotal.com/gui/file/4f6b1ef718632803404e00f0611350698c9aa35c560e63a658f52df7eb727e20), better (and quite frankly more reputable) antiviruses than those five do *not* detect PyWall as malware, that's because it isn't, a lot of apps compiled with PyInstaller and, in general, software that interacts with the security of the system have this same issue, even OneClickFirewall has a [similar issue](https://www.virustotal.com/gui/file/c5b2fd236c9430b2d8ed48d6b08526753ecc47f2246af668e3b757cc54cd26e5), though greatly reduced, this is *probably* due to the compiler itself, and not any significant deviation of what the code actually does, since as far as I'm able to tell the aforementioned software uses the same method to deny or allow internet access, that being, to write a rule directly to the firewall.<br/><br/>
You are free to read the code and compile it yourself, use the artifacts available by clicking on the latest run [here](https://github.com/p-yukusai/PyWall/actions) (as the [process](https://github.com/p-yukusai/PyWall/actions/workflows/main.yml) and [code](https://github.com/p-yukusai/PyWall/blob/master/.github/workflows/main.yml) by which the program is compiled are freely available for anyone to see and scrutinize) and review/use the [.iss script](https://github.com/p-yukusai/PyWall/blob/master/PyWall%20Installer.iss) used to create the installer available in the "releases" section.

## Technical explination 👩‍🔬

#### Tl;dr:
PyWall essentially runs a command from an elevated prompt to either add or remove (if it exists) a rule from the Windows Firewall, needless to say, you *need* to have your firewall active to make any practical use of this program, additionally, it uses PyQt5 alongside with qt-material to draw the GUI, winotify to create toast notifications and context_menu, combined with some custom regkey manipulation, to create the context menu.

#### The command:
The command runs from the src/cmdWorker.py script, and it is as follows:
```cmd
@echo off && netsh advfirewall firewall {add/delete} rule name="PyWall blocked {filename}" dir=out program="{file path}" action=block
```
- echo is turned off to avoid having a bunch of consoles popping up.
- "netsh advfirewall firewall" allows interaction with the rules of the firewall, in the program "Allow Internet Access" will *delete* the rule if it exists and "Deny Internet Access" will *add* it.

#### Parsing:
What the program does when the user attempts to allow or deny the internet access varies depending if the path detected results in a file or a directory.

The program has two variables that define what will and won't be considered in the parse, these are "blacklisted_names" and "accepted_types", the former is a list of all filenames (e.g. Discord, Chrome, etc.) that *won't* be considered by the parser and the later is a list of all accepted suffixes (e.g. .exe, .msi, etc.) that *will* be considered by the parser.

For files it's fairly simple, the variable that will be used to run the command is just the path from the file selected, for folders it will check if "recursive" in the config file is set to true or false, if true it will check the folder and all subfolders for matches, otherwise only the initial folder will be scanned, either way, the variable will be a list containing one or more paths to all accepted matches, which will later be allowed or blocked by the command. 
The command is run for each item detected.

## PSA 🌠
I believe it to be important to remind people of the potential dangers of programs that interact with the security features of your system, this is why it is so valuable to be able to review what a certain piece software does and doesn't do, as such, please excercise caution with what you install on your system!<br/> If you do not trust a particular piece of software, you can just not install it, use a sandbox or block its internet access to make having it on your system a bit more secure, and, since you're already here, why not use PyWall for the later? 😉.
 
## Anything else? 🚀
Nope! That's all there really is to it. I hope you have some use for this little app!
## 

<h1 align="center">
<a href=https://forthebadge.com>
  <img alt="With Love" src="https://forthebadge.com/images/badges/built-with-love.svg">
</a>
<a href=https://forthebadge.com>
  <img alt="With Spaguett" src="https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg">
</a>
<a href=https://forthebadge.com>
    <img alt="With Python" src="https://forthebadge.com/images/badges/made-with-python.svg">
</a>
</h1>
