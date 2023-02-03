# coding: utf-8

import sys
from argparse import ArgumentParser
from json import dump, load
from os import getcwd, getenv, mkdir
from os.path import exists, join

from colorama import init

from squba.classes import Config
from squba.dive import dive
from squba.utils import defaultConfiguration, split_arg

__updated__ = '2023-02-02 23:11:11'

init()

# if getattr(sys, 'frozen', False):
#     # frozen
#     DIR: str = dirname(sys.executable)

#     DIR: str = '%APPDATA%\\SqubaConfig\\'
#     CONFIG_FILE = DIR + '\\config.json'
#     LAST_DIVING_FILE = DIR + '\\last_diving.json'
# else:
#     # unfrozen
#     DIR: str = dirname(realpath(__file__))

#     DIR: str = '%APPDATA%\\SqubaConfig\\'
#     CONFIG_FILE = DIR + '\\config.json'
#     LAST_DIVING_FILE = DIR + '\\last_diving.json'

DIR = getenv('appdata')+'\\SqubaData'

CONFIG_FILE = DIR + '\\config.json'
LAST_DIVING_FILE = DIR + '\\last_diving.json'

if not exists(DIR):
  mkdir(DIR)
if not exists(CONFIG_FILE):
  with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
    dump(defaultConfiguration, file, indent=2, ensure_ascii=False)

CONFIG = Config(CONFIG_FILE)


def extend_exclude(x: str):
  exclude_list: str = split_arg(x)
  exclude_list.extend(CONFIG.defaultExclude)
  return exclude_list


PARSER = ArgumentParser()

PARSER.add_argument('path', type=join, nargs='?', default=getcwd(),
                    help='path to dive into; e.g. "C:\\Users\\<User>\\Desktop"')

PARSER.add_argument('-L', '--max-lvl', default=CONFIG.defaultMaxLvl, type=int,
                    help='dive down to a certain level (default = %s); e.g. 3' % CONFIG.defaultMaxLvl)

PARSER.add_argument('-S', '--search', default=[], type=split_arg,
                    help='list of stuff (terms) to look for while diving, separated by commas; e.g ".txt,microsoft"')

PARSER.add_argument('-E', '--exclude', default=CONFIG.defaultExclude, type=extend_exclude,
                    help='list of stuff (terms) to ignore while diving, separated by commas (default => %s); e.g ".txt,microsoft"' % CONFIG.defaultExclude)

PARSER.add_argument('-I', '--indent', default=CONFIG.defaultIndent, type=int,
                    help='indentation spaces (default => %s); e.g 3' % CONFIG.defaultIndent)

PARSER.add_argument('-M', '--mode', default=CONFIG.defaultMode, choices=['all', 'folders', 'files'])

PARSER.add_argument('--detail', action='store_true', help='make a deep diving')

PARSER.add_argument('--log', action='store_true', help='whether to log every found file or not')

PARSER.add_argument('--config', action='store_true', help='get configuration file location')

PARSER.add_argument('--last', action='store_true', help='get last diving info')

PARSER.add_argument('--dir', action='store_true', help='get directory location')

if __name__ == '__main__':

  ARGS = PARSER.parse_args()

  if ARGS.max_lvl != CONFIG.defaultMaxLvl and not ARGS.detail:
    PARSER.error('--max_lvl must be used with --detail')

  if ARGS.last:
    if exists(LAST_DIVING_FILE):
      with open(LAST_DIVING_FILE, 'r', encoding='utf-8') as file:
        print(load(file, indent=2))
    else:
      print("You haven't submerged into the depths of your file system yet.")
    sys.exit()

  if ARGS.config:
    print(CONFIG_FILE)
    sys.exit()

  if ARGS.dir:
    print(DIR)
    sys.exit()

  DATA = dive(ARGS, CONFIG, LAST_DIVING_FILE)
  DATA.display()

  sys.exit()
