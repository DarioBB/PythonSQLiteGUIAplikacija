import sys
from cx_Freeze import setup, Executable

import hashlib
import time

def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

str_md5 = computeMD5hash(time.strftime("%c")+"my_salt")

company_name = "Test tvrtka d.o.o."
product_name = "GUI aplikacija by Dario Benšić"

bdist_msi_options = {
    'upgrade_code': '{'+str_md5+'}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
    }
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}
#build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

"""setup(  name = "Adresar kontakata",
        version = "0.1",
        description = "Adresar kontakata GUI aplikacija",
        options = {"bdist_msi": bdist_msi_options,"build_exe": build_exe_options},
        executables = [Executable("adresar_kontakata.py", shortcutName="Adresar kontakata GUI aplikacija",
            shortcutDir="DesktopFolder",base=base)])"""
setup(  name = "Adresar kontakata Python SQLite GUI aplikacija",
        version = "1.0",
        description = "Adresar kontakata Python SQLite GUI aplikacija by Dario Benšić",
        options = {"bdist_msi": bdist_msi_options,"build_exe": build_exe_options},
        executables = [Executable("adresar_kontakata.py",base=base)])