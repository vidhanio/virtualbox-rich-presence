# This installs the required Python-Modules dependant on the used platform
import pip, sys



def install(packages):
    for package in packages:
        pip.main(['install', package])

all_platforms = [
    "pyvbox",
    "pypresence",
    "psutil",
    "virtualbox",
    "pypresence"
]

windows = [
    "pywin32"
]

install(all_platforms)

if sys.platform == "win32":
    install(windows)