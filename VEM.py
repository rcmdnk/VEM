#!/usr/bin/env python
"""
Vim Emulation (https://github.com/rcmdnk/KE-complex_modifications/)
Menu bar icon

Requirement: rumps (https://github.com/jaredks/rumps),
Worked with python 2.7.16 or later
"""

import argparse
import json
import os
import re

import rumps

__prog__ = os.path.basename(__file__)
__description__ = __doc__
__author__ = 'rcmdnk'
__copyright__ = 'Copyright (c) 2020 rcmdnk'
__credits__ = ['rcmdnk']
__license__ = 'Apache License 2.0'
__version__ = 'v0.1.0'
__date__ = '28/Jul/2020'
__maintainer__ = 'rcmdnk'
__email__ = 'rcmdnk@gmail.com'
__url__ = 'https://github.com/rcmdnk/VEM'
__status__ = 'Prototype'

DEBUG = True
SETTING_FILE = os.environ['HOME'] + '/.config/vem/config'
PLIST_FILE = os.environ['HOME'] + '/Library/LaunchAgents/vem.plist'
CHECK_INTERVAL = 1
KARABINER_JSON = '/Library/Application Support/org.pqrs/tmp/' \
    'karabiner_grabber_manipulator_environment.json'
ICON_SET = {'normal': 'images/normal.png', 'visual': 'images/visual.png',
            'insert': 'images/insert.png', 'command': 'images/command.png',
            'search': 'images/search.png', 'disabled': 'images/disabled.png'}
ICON_SET_GRAY = {'normal': 'images/normal_gray.png',
                 'visual': 'images/visual_gray.png',
                 'insert': 'images/insert_gray.png',
                 'command': 'images/command_gray.png',
                 'search': 'images/search_gray.png',
                 'disabled': 'images/disabled_gray.png'}
ABOUT_TITLE = __prog__
ABOUT_MESSAGE = 'Vim Emulation Menu bar icon\n\n' \
    + 'This application work with  Vim Emulation using Karabiner-Elements:\n' \
    + 'https://github.com/rcmdnk/KE-complex_modifications/\n\n' \
    + 'Version %s\n' % __version__ \
    + '%s' % __copyright__


class VEM(rumps.App):
    def __init__(self, autostart=True, debug=False):
        # Set default values
        self.debug_mode = debug
        rumps.debug_mode(self.debug_mode)

        self.setting_file = SETTING_FILE
        self.plist_file = PLIST_FILE
        self.karabiner_json = KARABINER_JSON
        self.icon_set = ICON_SET
        self.icon_set_gray = ICON_SET_GRAY
        self.icons = self.icon_set

        # Read settings
        self.settings = {}
        self.read_settings()

        # Application setup
        super(VEM, self).__init__(type(self).__name__, title=None,
                                  icon=self.icons['insert'])
        self.menu = [
            'About',
            None,
            'Gray icon',
            None,
            'Set check interval',
            'Start at login',
            None,
            'Uninstall',
            None,
        ]

        # Other class variables

        if 'gray_icon' in self.settings and self.settings['gray_icon'] == '1':
            self.icons = self.icon_set_gray
            self.menu['Gray icon'].state = True
        else:
            self.icons = self.icon_set
            self.menu['Gray icon'].state = False

        if 'start_at_login' in self.settings\
                and self.settings['start_at_login'] == '1':
            self.menu['Start at login'].state = True
        else:
            self.menu['Start at login'].state = False

        # Set and start get_messages
        self.timer = rumps.Timer(self.check_karabiner,
                                 int(self.settings['interval'])
                                 if 'interval' in self.settings
                                 else CHECK_INTERVAL)
        if autostart:
            self.start()

    @rumps.clicked('About')
    def about(self, sender):
        rumps.alert(title=ABOUT_TITLE, message=ABOUT_MESSAGE)

    @rumps.clicked('Set check interval')
    def set_interval(self, sender):
        # Need to stop timer job, otherwise interval can not be changed.
        self.stop()
        response = rumps.Window('Set check interval (s)',
                                default_text=str(
                                    self.timer.interval),
                                dimensions=(100, 20)).run()
        if response.clicked:
            self.timer.interval = int(response.text)
            self.settings['interval'] = response.text
            self.write_settings()

        self.start()

    @rumps.clicked('Gray icon')
    def gray_icon(self, sender):
        sender.state = not sender.state
        if sender.state == 0:
            self.icons = self.icon_set
        else:
            self.icons = self.icon_set_gray
        self.settings['gray_icon'] = str(sender.state)
        self.write_settings()

    @rumps.clicked('Start at login')
    def set_startup(self, sender):
        sender.state = not sender.state
        if sender.state == 0:
            if os.path.exists(self.plist_file):
                os.system('launchctl unload %s' % self.plist_file)
                os.remove(self.plist_file)
        else:
            plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"'''\
''' "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>Label</key>
        <string>vem</string>
        <key>ProgramArguments</key>
        <array>
            <string>''' + self.get_exe() + '''</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
</dict>
</plist>'''
            with open(self.plist_file, 'w') as f:
                f.write(plist)

        self.settings['start_at_login'] = str(sender.state)
        self.write_settings()

    @rumps.clicked('Uninstall')
    def uninstall(self, sender):
        ret = rumps.alert('Do you want to uninstall VEM?',
                          ok='OK', cancel='Cancel')
        if ret == 1:
            self.remove_me()

    def check_karabiner(self, sender):
        if not os.path.exists(self.karabiner_json):
            self.icon = self.icons['disabled']
            return
        with open(self.karabiner_json) as f:
            kara = json.load(f)
        if 'variables' not in kara \
                or 'vim_emu_normal' not in kara['variables']:
            self.icon = self.icons['disabled']
            return
        if kara['variables']['vim_emu_insert'] == 1:
            self.icon = self.icons['insert']
        elif kara['variables']['vim_emu_visual'] == 1 \
                or kara['variables']['vim_emu_visual_line'] == 1:
            self.icon = self.icons['visual']
        elif kara['variables']['vim_emu_command'] == 1:
            self.icon = self.icons['command']
        else:
            self.icon = self.icons['normal']

    def read_settings(self):
        if not os.path.exists(self.setting_file):
            return
        with open(self.setting_file, 'r') as f:
            for line in f:
                line = re.sub(r' *#.*', '', line).strip()
                if line == '':
                    continue
                line = line.split('=')
                if len(line) < 2:
                    continue
                self.settings[line[0]] = line[1]

    def write_settings(self):
        setting_dir = os.path.dirname(self.setting_file)
        if not os.path.exists(setting_dir):
            os.makedirs(setting_dir)
        with open(self.setting_file, 'w') as f:
            for (k, v) in self.settings.items():
                f.write('%s=%s\n' % (k, v))

    def get_exe(self):
        exe = os.path.abspath(__file__)
        if exe.find('Contents/Resources/') != -1:
            name, ext = os.path.splitext(exe)
            if ext == '.py':
                exe = name
            exe = exe.replace('Resources', 'MacOS')
        return exe

    def get_app(self):
        exe = self.get_exe()
        if exe.find('Contents/MacOS/') == -1:
            # Not in app
            return ''
        else:
            return os.path.dirname(exe).replace('/Contents/MacOS', '')

    def reset(self):
        if os.path.exists(self.plist_file):
            os.system('launchctl unload %s' % self.plist_file)
            os.remove(self.plist_file)
        os.system('rm -f %s %s' % (self.authentication_file,
                                   self.setting_file))
        os.system('rm -rf "%s/%s"' %
                  (os.environ['HOME'],
                   '/Library/Application Support/VEM'))

    def remove_me(self):
        self.reset()
        app = self.get_app()
        if app != "":
            os.system('rm -rf "%s"' % app)
        else:
            print('%s is not in App' % self.get_exe())

    def start(self):
        self.timer.start()

    def stop(self):
        if self.timer.is_alive():
            self.timer.stop()

    def restart(self):
        self.stop()
        self.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=__prog__,
        formatter_class=argparse.RawTextHelpFormatter,
        description=__description__)
    parser.add_argument('-u', '--uninstall', action='store_true',
                        dest='uninstall',
                        default=False, help='Uninstall %s' % __prog__)
    parser.add_argument('-d', '--debug', action='store_true',
                        dest='debug',
                        default=False, help='Show debug output')
    parser.add_argument('-r', '--reset', action='store_true', dest='reset',
                        default=False, help='Reset settings')
    args = parser.parse_args()
    app = VEM(not (args.uninstall or args.reset), debug=args.debug)
    if args.uninstall:
        app.remove_me()
    elif args.reset:
        app.reset()
    else:
        app.run()
