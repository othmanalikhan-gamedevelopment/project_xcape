import os
import sys

from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.join("C:\\Users", "OzAli", "Anaconda3")
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict(packages=["pygame",
                              "xcape",
                              "xcape.common",
                              "xcape.components",
                              "xcape.engines",
                              "xcape.entities"],
                    excludes=["tkinter",
                              "email",
                              "html",
                              "http",
                              "xml",
                              "xmlrpc",
                              "lib2to3",
                              "json",
                              "ctypes",
                              "multiprocessing",
                              "pydoc_data",
                              "urllib",
                              "distutils",
                              "logging",
                              "unittest",
                              "test",
			      "nose",
			      "numpy",
			      "scipy",
			      "curses",
                              ],
                    include_files=["README.md",
                                   "LICENSE.txt",
                                   "sfx/",
                                   "images/",
                                   "extra/"],
                    build_exe="build")

executables = [
    Executable('main.py',
               targetName="xcape.exe",
               base=base,
               icon=os.path.join("images", "icons", "assets", "ico", "1.ico"))
]

setup(name='xcape',
      version='2.1',
      description='A game (platformer) made using a simple engine built on pygame',
      options=dict(build_exe=buildOptions),
      executables=executables
)

