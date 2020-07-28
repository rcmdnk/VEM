# VEM


![VEM](https://github.com/rcmdnk/VEM/raw/master/pics/VEM.png "VEM")

Vim Emulation Menubar icon.

This application work with [Vim Emulation](https://github.com/rcmdnk/KE-complex_modifications/)
using [Karabiner-Elements](https://karabiner-elements.pqrs.org/).

If you run Karabiner-Elements and Vim Emulation is enabled,
VEM' icon indicates the current mode of Vim Emulation.

* Insert Mode:

![insert](https://github.com/rcmdnk/VEM/raw/master/pics/menubar_insert.jpg "insert")

* Normal Mode:

![normal](https://github.com/rcmdnk/VEM/raw/master/pics/menubar_normal.jpg "normal")

* If you check `Gray icon` option, all icons will be gray icons.

![insert gray](https://github.com/rcmdnk/VEM/raw/master/pics/menubar_insert_gray.jpg "insert gray")

# Installation
With [Homebrew Cask](http://caskroom.io/), do:

    $ brew cask install rcmdnk/rcmdnkcask/vem

Or download the app from 
[releases](https://github.com/rcmdnk/VEM/releases) and install it in **/Applications** or **~/Applications**.

# Uninstall

Launch VEM, and click **Uninstall** menu from menu bar icon.

This function will remove

* $HOME/Library/LaunchAgents/menubargmail.plist
* VEM.app

If you want to remain settings (or don't care about it), just remove VEM.app.

# Getting started

Install [Karabiner-Elements](https://karabiner-elements.pqrs.org/).

Add [Vim emulation](https://rcmdnk.com/KE-complex_modifications/) in Complex modifications Rules of Karabiner-Elements
and enable settings.

Launch VEM.app.

# Menus

* About: Show information of VEM.
* Gray icon: Check if you want to use gray icons.
* Set check interval: Set interval to check state (Default: 1 (sec)).
* Start at login: Toggle if starting at login or not.
* Uninstall: Uninstall VEM.
* Quit: Quit VEM.

# How to build

* Required pip packages:
    * [rumps](https://github.com/jaredks/rumps)
    * [py2app](https://pypi.python.org/pypi/py2app/)

            $ pip install rumps py2app

* Test
    * Run

            $ python VEM.py
* Build
    * Run

            $ rm -rf build dist && python setup.py py2app

    * Then, **VEM.app** will appear in **./dist** directory.


# Icons

* Menu bar icons were created with; [CMAN](https://sozai.cman.jp/icon/string/alphabet1/)
* Application icon was created with; [hatchful](https://hatchful.shopify.com/ja/)
