import os
import shutil
import platform
import subprocess
import sys
import ctypes
from ctypes import wintypes

def find_all_fonts(root_dir):
    """
    Traverse the Google Fonts directory and find all .ttf and .otf files.
    Assumes structure: root_dir / {license_dirs} / {family_dirs} / *.ttf
    """
    font_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.ttf', '.otf')):
                font_files.append(os.path.join(dirpath, filename))
    return font_files

def install_fonts_on_windows(font_files):
    """
    Install fonts on Windows by copying to Fonts directory and notifying the system.
    Requires running the script as Administrator.
    """
    fonts_folder = os.path.join(os.environ['WINDIR'], 'Fonts')
    added = False
    for font_path in font_files:
        dest = os.path.join(fonts_folder, os.path.basename(font_path))
        if not os.path.exists(dest):
            shutil.copy(font_path, dest)
            ctypes.windll.gdi32.AddFontResourceW(dest)
            added = True
        else:
            print(f"Font already exists: {dest}")

    if added:
        # Notify running programs of font change
        HWND_BROADCAST = 0xFFFF
        WM_FONTCHANGE = 0x001D
        SMTO_ABORTIFHUNG = 0x0002
        result = wintypes.DWORD()
        user32 = ctypes.WinDLL('user32')
        user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, ctypes.byref(result))
        print("Fonts installed and system notified on Windows.")

def install_fonts_on_macos(font_files):
    """
    Install fonts on macOS by copying to user's Library/Fonts.
    For all users, use /Library/Fonts (requires sudo).
    """
    fonts_folder = os.path.expanduser('~/Library/Fonts')
    os.makedirs(fonts_folder, exist_ok=True)
    for font_path in font_files:
        dest = os.path.join(fonts_folder, os.path.basename(font_path))
        if not os.path.exists(dest):
            shutil.copy(font_path, dest)
        else:
            print(f"Font already exists: {dest}")
    print("Fonts installed on macOS. You may need to restart applications to see changes.")

def install_fonts_on_linux(font_files):
    """
    Install fonts on Linux by copying to ~/.fonts and running fc-cache.
    For all users, use /usr/share/fonts (requires sudo).
    """
    fonts_folder = os.path.expanduser('~/.fonts')
    os.makedirs(fonts_folder, exist_ok=True)
    for font_path in font_files:
        dest = os.path.join(fonts_folder, os.path.basename(font_path))
        if not os.path.exists(dest):
            shutil.copy(font_path, dest)
        else:
            print(f"Font already exists: {dest}")
    # Refresh font cache
    subprocess.call(['fc-cache', '-f', '-v'])
    print("Fonts installed and cache refreshed on Linux.")

def main(root_dir):
    system = platform.system()
    font_files = find_all_fonts(root_dir)
    if not font_files:
        print("No font files found in the specified directory.")
        return

    print(f"Found {len(font_files)} font files to install.")

    if system == 'Windows':
        install_fonts_on_windows(font_files)
    elif system == 'Darwin':  # macOS
        install_fonts_on_macos(font_files)
    elif system == 'Linux':
        install_fonts_on_linux(font_files)
    else:
        print(f"Unsupported operating system: {system}")
        return

    print("Installation complete. Note: Some fonts may have duplicate names; check for conflicts.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = 'fonts-main'  # Default to 'fonts-main' in current directory
        print("Using default directory: 'fonts-main'. Provide path as argument if different.")

    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        sys.exit(1)

    main(root_dir)