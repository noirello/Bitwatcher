from distutils.core import setup
import py2exe

setup(
      options = {"py2exe": {"compressed": 1, 
                            "optimize": 2, 
                            "bundle_files": 2
                            }
      },
      windows = ['bitwatcher.py'],
      zipfile = None
)