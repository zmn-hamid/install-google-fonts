import os
import shutil
import ctypes
from ctypes import wintypes
import subprocess
import platform
import sys
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class FontInstaller:
    def __find_all_fonts(self, root_dir: str) -> list[str]:
        """
        Traverse the Google Fonts directory and find all .ttf and .otf files.
        Assumes structure: root_dir / {license_dirs} / {family_dirs} / *.ttf
        """
        
        files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith((".ttf", ".otf")):
                    files.append(os.path.join(dirpath, filename))
        
        return files
    
    def __win_install(self, font_files: list[str]):
        """
        Install fonts on Windows by copying to Fonts directory and notifying the system.
        Requires running the script as Administrator.
        """
        fonts_folder = os.path.join(os.environ["WINDIR"], "Fonts")
        added = False
        
        for font_path in font_files:
            dest = os.path.join(fonts_folder, os.path.basename(font_path))
            if not os.path.exists(dest):
                shutil.copy(font_path, dest)
                ctypes.windll.gdi32.AddFontResourceW(dest)
                added = True
                logger.info(f"Font '{os.path.basename(font_path)}' installed.")
            else:
                logger.info(f"Font already exists: {dest}")
        
        if added:
            # Notify running programs of font change
            HWND_BROADCAST = 0xFFFF
            WM_FONTCHANGE = 0x001D
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_ulong()
            user32 = ctypes.WinDLL("user32")
            user32.SendMessageTimeoutW(
                HWND_BROADCAST,
                WM_FONTCHANGE,
                0,
                0,
                SMTO_ABORTIFHUNG,
                1000,
                ctypes.byref(result),
            )
            
            logger.info("Fonts installed and system notified on Windows.")
    
    def __mac_install(self, font_files: list[str]):
        """
        Install fonts on macOS by copying to user's Library/Fonts.
        For all users, use /Library/Fonts (requires sudo).
        """
        
        fonts_folder = os.path.expanduser("~/Library/Fonts")
        
        os.makedirs(fonts_folder, exist_ok=True)
        
        for font_path in font_files:
            dest = os.path.join(fonts_folder, os.path.basename(font_path))

            if not os.path.exists(dest):
                shutil.copy(font_path, dest)
                logger.info(f"Font '{os.path.basename(font_path)}' installed.")
            else:
                logger.info(f"Font already exists: {dest}")

        logger.info(
            "Fonts installed on macOS. You may need to restart applications to see changes."
        )
    
    def __linux_install(self, font_files: list[str]):
        """
        Install fonts on Linux by copying to ~/.fonts and running fc-cache.
        For all users, use /usr/share/fonts (requires sudo).
        """
        
        fonts_folder = os.path.expanduser("~/.fonts")
        
        os.makedirs(fonts_folder, exist_ok=True)
        
        for font_path in font_files:
            dest = os.path.join(fonts_folder, os.path.basename(font_path))
            
            if not os.path.exists(dest):
                shutil.copy(font_path, dest)
                logger.info(f"Font '{os.path.basename(font_path)}' installed.")
            else:
                logger.info(f"Font already exists: {dest}")
        
        # Refresh font cache
        subprocess.call(["fc-cache", "-f", "-v"])
        logger.info("Fonts installed and cache refreshed on Linux.")
    
    def install(self):
        if not self.__is_sudo():
            logger.error("Program must run with admin/sudo privileges!")
            sys.exit(1)
        
        # Use the current directory as the Google Fonts directory
        root_dir = os.getcwd()

        if not os.path.exists(root_dir):
            logger.error(f"Current directory not found: {root_dir}")
            sys.exit(1)

        font_files = self.__find_all_fonts(root_dir)
        if not font_files:
            logger.error("No font files found in the current directory.")
            input("Press any key to exit...")
            exit(0)

        logger.info(f"Found {len(font_files)} font files to install in {root_dir}.")

        system = platform.system()
        if system == "Windows":
            self.__win_install(font_files)
        elif system == "Darwin":  # macOS
            self.__mac_install(font_files)
        elif system == "Linux":
            self.__linux_install(font_files)
        else:
            logger.error(f"Unsupported operating system: {system}")
            input("Press any key to exit...")
            exit(1)

        logger.info("Installation complete. Note: Some fonts may have duplicate names; check for conflicts.\n\n")
        input("Press any key to exit...")
    
    def __is_sudo(self) -> bool:
        """
        Checks if the current script is running with administrative (root) privileges.

        This function is cross-platform and works on both Windows and Unix-like
        systems (Linux, macOS).

        - **On Windows**, it uses the `IsUserAnAdmin` function from the Shell32 library.
        - **On Unix-like systems**, it checks if the effective user ID (EUID) is 0.

        Returns:
            bool: True if the script has admin privileges, False otherwise.
        """
        try:
            system = platform.system()
            
            if system == "Windows":
                # IsUserAdmin function in windows return non zero value if we have admin privileges
                return ctypes.windll.shell32.IsUserAnAdmin() == 1
            elif system == "Darwin" or system == "Linux":
                # For Unix-like systems (Linux, macOS) uid of root user is 0
                return os.getuid() == 0
            else:
                logger.error(f"Unsupported operating system: {system}")
                return False
        except (AttributeError, ImportError):
            # If any required module or function is not available, assume no admin rights
            return False
    
    def __win_notify_font_change():
        """
        Broadcasts a WM_FONTCHANGE message to all top-level windows to notify
        them of a change in the available fonts.
        
        This is the modern, 64-bit compatible way to perform this action.
        """
        # Define Windows constants
        HWND_BROADCAST = 0xFFFF
        WM_FONTCHANGE = 0x001D
        SMTO_ABORTIFHUNG = 0x0002
        
        # Load the user32 library
        user32 = ctypes.WinDLL("user32")
        
        # Define the function signature for SendMessageTimeoutW for type safety.
        # This prevents potential crashes and ensures correct data types are used,
        # especially between 32-bit and 64-bit systems.
        send_message_timeout = user32.SendMessageTimeoutW
        send_message_timeout.argtypes = [
            wintypes.HWND,       # hWnd
            wintypes.UINT,       # uMsg
            wintypes.WPARAM,     # wParam
            wintypes.LPARAM,     # lParam
            wintypes.UINT,       # fuFlags
            wintypes.UINT,       # uTimeout
            ctypes.POINTER(wintypes.DWORD_PTR) # lpdwResult
        ]
        send_message_timeout.restype = wintypes.LRESULT

        # This variable will receive the result of the broadcast.
        # Using c_size_t makes it compatible with both 32-bit (DWORD) and 
        # 64-bit (DWORD_PTR) systems. The original code's use of c_ulong
        # was only correct for 32-bit systems.
        result = wintypes.DWORD_PTR()
        
        print("Broadcasting font change notification...")
        
        # Call the function
        send_message_timeout(
            HWND_BROADCAST,
            WM_FONTCHANGE,
            0,                 
            0,                  
            SMTO_ABORTIFHUNG,
            1000,               
            ctypes.byref(result)
        )
