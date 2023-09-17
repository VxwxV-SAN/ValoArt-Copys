import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"  

executables = [Executable("x.py", base=base, icon="logo.ico", target_name="Copy_Pastes_Gekko_Rida.exe")]

packages = ["tkinter","time","pygetwindow","pyautogui"]
includes = ["tkinter.ttk", "json"]
excludes = []
include_files = ["data.json","logo.ico"] 

options = {
    'build_exe': {
        'packages': packages,
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files,
    },
}

setup(
    name="Copy_Pastes_Gekko_Rida",
    options=options,
    version="2.0",
    description="Copy_Pastes_Gekko_Rida",
    executables=executables,
)
