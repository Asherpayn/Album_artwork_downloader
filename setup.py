from setuptools import setup

APP = ['main.py']  # Replace with the name of your Python script
DATA_FILES = []
OPTIONS = {
	'argv_emulation': True,
	'packages': ['requests', 'spotipy', 'PIL'],  # Include necessary packages
	'iconfile': 'icon.icon',  # Optional: path to your app icon
}

setup(
	app=APP,
	data_files=DATA_FILES,
	options={'py2app': OPTIONS},
	setup_requires=['py2app'],
)
