# VirtualBox Rich Presence

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

## Installation

First, clone the repository.

```cmd
git clone https://www.github.com/yolodude25/virtualbox-rich-presence
```

Then go to the [VirtualBox downloads Page](https://www.virtualbox.org/wiki/Downloads) and download the VirtualBox SDK.

After downloading it, extract the `.zip` file and run the installer.

```cmd
cd installer
```

```cmd
python vboxapisetup.py install
```

Then, install the required modules.

```cmd
cd virtualbox-rich-presence
```

```cmd
pip install -r requirements.txt
```

## Config

The [config](config.ini.example) allows you to change what is displayed on your rich presence.

### Available Values

- `{os_hf}`: Name of OS. (e.g. "Microsoft Windows")
- `{version_hf}`: Name of OS version. (e.g. "Windows 8")
- `{version_image}`: Image key of OS version. (e.g. "windows_8")
- `{architecture}`: OS architecture (e.g. "64")
- `{architecture_image}`: Image key of OS architecture (e.g. "64")
- `{icon}`: Image key of VirtualBox Icon.

## Usage

Make a copy of [`config.ini.example`](config.ini.example) and remove the `.example`, then [edit it](#config) if you want.

Run `presence.py`.
