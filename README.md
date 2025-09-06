# Install All Google Fonts

Automatically install all google fonts downloaded using:
https://github.com/google/fonts/archive/main.zip

## Installation - Easy but only for Windows x64

1. Install google fonts using the link above then extract it.
2. Download the latest release from [here](https://github.com/zmn-hamid/install-google-fonts/releases/latest).
3. Copy the exe file to the extracted directory and run it. It should start installing them one by one. Wait for it, it won't tell you which files is it installing.

In case you got an error, run the file with admin privileges (Run As Administrator on Windows)

## Installation - Cross-platform but harder

This method will work for windows, mac and linux, but is a bit harder for non-programmers.

All you have to do is to run the python file in the root directory of the downloaded fonts folder:

1. Install google fonts using the link above then extract it.
2. Download and install python 3.12 from its website. Make sure "add to path" option (or something like that) is enabled. If you forgot, search for "adding python to environment path" and follow the instructions.
3. Download [install_all_google_fonts.py](install_all_google_fonts.py) and copy it to the
    extracted folder from step 1.
4. If you're on Windows, do the same (as step 3) with [install.bat](cross_platform_installation/install.bat), otherwise do it on [install.sh](cross_platform_installation/install.sh).
5. Now simply double click the `install.bat/sh` file and wait for it to install the fonts.

In case you got an error, run the file with admin privileges (Run As Administrator on Windows)

### cheers
