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
  
## What is it? 🔐

This is a small application, written in Python and Qt, that makes it easy to block or allow applications from access to the internet, it contains a graphical user interface and a shell extension, so you may choose between the benefits of an easy-to-use GUI app with the efficiency of just right clicking any folder or file for maximum convinience! <br />
PyWall was heavily inspired by [OneClickFirewall](https://winaero.com/oneclickfirewall/) by Winaero, and you should totally check that app out!

## What does it do? 🔓
This app esentially writes a rule to the Windows Firewall to deny access to just about anything, however by default only executable files will be taken into consideration, as a consequence of interacting directly with the Firewall, this app requires elevation to properly work. <br />
PyWall also has the ability to block or allow entire folders (which was the main reason behind its development, since OneClickFirewall lacks the ability to do so 👀), the way it does this is by sorting through the entire folder to look for all files with a matching type, then it will either block or allow all matches. <br />
The code was written (to the best of my ability) with the intent of being read by just about anyone, so go right ahead and look through my spaguetti code by yourself if you want to know how the app works in more detail!

## Anything else? 🚀
Nope, that's it. I hope you have some use for this little app!
## 
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
