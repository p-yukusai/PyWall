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
This app esentially writes a rule to the [Windows Firewall](## "Needless to say, it is required that you have your Firewall active") to deny access to just about anything, by default only executable files will be taken into consideration. 
As a consequence of interacting directly with the Firewall, this app requires elevation to properly work.<br /> This app does not have the ability to allow internet access for apps that have already been blocked by means other than PyWall itself, for instance custom firewalls, previous firewall rules, etc.<br/><br />
PyWall also has the ability to block or allow entire folders (which was the main reason behind its development, since OneClickFirewall lacks the ability to do so 👀), the way it does this is by sorting through the entire folder to look for all files with a matching type, then it will either block or allow all matches, this is done recursively, meaning that *every* folder inside the initial selection will be scanned, so please be careful with what you select!<br /><br />
The code was written (to the best of my ability) with the intent of being read by just about anyone, so go right ahead and look through my spaguetti code by yourself if you want to know how the app works in more detail!

## False positives ☣️
As previously mentioned, this app interacts directly with the firewall, this is done via [console command](https://github.com/p-yukusai/PyWall/blob/7381bf84a4a30da80d945c9994e4429de47764ab/src/cmdWorker.py#L95) through the use of the OS library from Python, this, in 
conjuction with the fact that it requires elevation to work, having to check for said elevation, has made it such that [five security vendors](# "Antiy-AVL, VBA32, Zillya, Yandex and Microsoft") have flagged this app as "malicious", this is what's commonly described as a ["false positive"](https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/images/false-positives-overview.png?view=o365-worldwide).<br/>
As seen in the attatched [VirusTotal report](https://www.virustotal.com/gui/file/4f6b1ef718632803404e00f0611350698c9aa35c560e63a658f52df7eb727e20), better (and quite frankly more reputable) antiviruses than those five do *not* detect PyWall as malware, because it isn't, even the aforementioned OneClickFirewall has a [similar problem](https://www.virustotal.com/gui/file/c5b2fd236c9430b2d8ed48d6b08526753ecc47f2246af668e3b757cc54cd26e5), though greatly reduced, this is *probably* due a combination of the relatively reduced capabilities and better coding of the software.<br/><br/>
You are free to read the code and compile it yourself, use the artifacts available by clicking on the latest run [here](https://github.com/p-yukusai/PyWall/actions) (as the [process](https://github.com/p-yukusai/PyWall/actions/workflows/main.yml) and [code](https://github.com/p-yukusai/PyWall/blob/master/.github/workflows/main.yml) by which the program is compiled are freely available for anyone to see and scrutinize) and review/use the [.iss script](https://github.com/p-yukusai/PyWall/blob/master/PyWall%20Installer.iss) used to create the installer available in the "releases" section.

## PSA 🌠
I believe it to be important to remind people of the potential dangers of programs that interact with the security features of your system, this is why it is so valuable to be able to review what a certain piece software does and doesn't do, as such, please excercise caution with what you install on your system!<br/> If you do not trust a particular piece of software, you can just not install it, use a sandbox or block its internet access to make having it on your system a bit more secure, and, since you're already here, why not use PyWall for the later? 😉.
 
## Anything else? 🚀
Nope, that's it. I hope you have some use for this little app!
## 
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
