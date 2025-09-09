# Install All Google Fonts

Automatically install all Google Fonts downloaded from:  
👉 [Google Fonts Repo ZIP](https://github.com/google/fonts/archive/main.zip)

## Installation – Easiest (Recommended, Windows/Linux/Mac)

Prebuilt binaries are available for **Windows**, **Linux**, and **macOS**.  

1. Download Google Fonts using the link above and extract it.  
2. Download the latest binary for your OS from [Releases](https://github.com/zmn-hamid/install-google-fonts/releases/latest).  
   - Windows → `install-all-google-fonts-windows.exe`  
   - Linux → `install-all-google-fonts-linux`  
   - macOS → `install-all-google-fonts-macos`  
3. Copy the downloaded binary into the extracted fonts directory.  
4. Run it:  
   - On **Windows**: double-click the `.exe`.  
   - On **Linux/macOS**: make it executable first:  
     ```bash
     chmod +x ./install-all-google-fonts-linux
     ./install-all-google-fonts-linux
     ```
5. The installer will go through all fonts automatically. Just wait!  

⚠️ If you hit a permission error, run with admin/root privileges:  
- Windows → *Right-click → Run as Administrator*  
- Linux/macOS → run with `sudo ./install-all-google-fonts-linux`

---

## Installation – Alternative (Cross-platform, Python)

If you don’t want to use binaries, you can run the Python script instead.

1. Download and extract Google Fonts as above.  
2. Install Python 3.12 (make sure you add it to PATH).  
3. Download [install_all_google_fonts.py](install_all_google_fonts.py) and place it inside the extracted fonts folder.  
4. Run the installer script:  
   - **Windows**: double-click [install.bat](cross_platform_installation/install.bat).  
   - **Linux/macOS**: double-click [install.sh](cross_platform_installation/install.sh) or run it from terminal.  
5. Wait until all fonts are installed.  

⚠️ Again, run with admin/root privileges if you get errors.  

---

## Notes

- Binaries are built automatically and uploaded via GitHub Actions for every release.  

---

### ✨ Cheers & Happy Designing!

