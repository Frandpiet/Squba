import os

from cx_Freeze import Executable, setup

os.system('py main.py')

base = 'console'

executables = [
    Executable('main.py', base=base, target_name = 'dive', icon='../visuals/Icon.ico')
]

setup(name='dive',
      version = '1.0',
      description = '',
      options = {'build_exe': {
          'include_files':[
              ]
          }
        },
      executables = executables)
