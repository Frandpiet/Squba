import sys
from argparse import ArgumentParser
from json import dump, load
from os import getcwd
from os.path import dirname, exists, join, realpath

from colorama import init

from dive.classes import Config
from dive.utils import defaultConfiguration, get_path_data, split_arg

__updated__ = '2023-02-02 15:43:05'

init()

if getattr(sys, 'frozen', False):
    # frozen
    dir_ = dirname(sys.executable)
    config_file = dir_ + '\config.json'
    last_diving_file = dir_ + '\last_diving.json'
else:
    # unfrozen
    dir_ = dirname(realpath(__file__))
    config_file = dir_ + '\config.json'
    last_diving_file = dir_ + '\last_diving.json'

if not exists(config_file):
  with open(config_file, 'w', encoding='utf-8') as f:
    dump(defaultConfiguration, f, indent=2, ensure_ascii=False)
    
config = Config(config_file)

def extend_exclude(x):
  exclude_list = split_arg(x)
  exclude_list.extend(config.defaultExclude)
  return exclude_list

parser = ArgumentParser()

parser.add_argument('path', type=join, nargs='?',default=getcwd(),
                    help='path to dive into; e.g. "C:\\Users\\<User>\\Desktop"')

parser.add_argument('-L', '--max-lvl',default=config.defaultMaxLvl,type=int,
                    help='dive down to a certain level (default = %s); e.g. 3' % config.defaultMaxLvl)

parser.add_argument('-S', '--search',default=[],type=split_arg,
                    help='list of stuff (terms) to look for while diving, separated by commas; e.g ".txt,microsoft"')

parser.add_argument('-E', '--exclude',default=config.defaultExclude,type=extend_exclude,
                    help='list of stuff (terms) to ignore while diving, separated by commas (default => %s); e.g ".txt,microsoft"' % config.defaultExclude)

parser.add_argument('-I', '--indent',default=config.defaultIndent, type=int,
                    help='indentation spaces (default => %s); e.g 3' % config.defaultIndent)

parser.add_argument('-M', '--mode',default=config.defaultMode, choices=['all', 'folders', 'files'])

parser.add_argument('--detail',action='store_true',help='make a deep diving')

parser.add_argument('--log',action='store_true', help='whether to log every found file or not')

parser.add_argument('--config',action='store_true',help='get configuration file location')

parser.add_argument('--last',action='store_true',help='get last diving info')

parser.add_argument('--dir',action='store_true',help='get directory location')

if __name__ == '__main__':

  args = parser.parse_args()
  
  
  if args.max_lvl != config.defaultMaxLvl and not args.detail:
    parser.error('--max_lvl must be used with --detail')

  if args.last:
    if exists(last_diving_file):
      with open(last_diving_file, 'r', encoding='utf-8') as f:
        print(load(f, indent=2))
    else:
      print("You haven't submerged into the depths of your file system yet.")
    sys.exit()

  if args.config:
    print(config_file)
    sys.exit()
    
  if args.dir:
    print(dir_)
    sys.exit()
  
  data = get_path_data(args, config, last_diving_file)
  data.display()