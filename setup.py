"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['VEM.py']
DATA_FILES = ['images']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'VEM.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
