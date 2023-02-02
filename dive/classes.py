import sys
from json import dump, dumps, load
from os import getcwd
from os.path import isfile

from colorama import Fore


class File:
  def __init__(self, path, config, query):
    self.lvl = len(path.replace(getcwd(),'').split('\\'))-1
    self.route = path
    self.file_name = self.route.split('\\')[-1]
    self.is_file = isfile(self.route)
    self.query = query
    self.config = config
    
    if self.is_file:
      extension = self.file_name.split('.')[-1]
      self.extension = extension if extension in self.config.get_extensions() else 'unknownFile'
      
    if not self.is_file and self.lvl != 0:
      self.file_name = self.file_name + ' (LvL %s)' % self.lvl
      
    self.symbol = self.get_symbol()

  def display(self):
    display = ((' ' * self.query.indent) * self.lvl)+self.__repr__()
    return display

  def check_match(self):
    check = any([term in self.file_name for term in self.query.search])
    if check:
      self.file_name = Fore.LIGHTGREEN_EX + self.file_name# + self.config.matchedFileSymbol
    else:
      self.file_name = Fore.WHITE + self.file_name
    return check
      
  def check_exclude(self):
    return (
        any([term in self.file_name for term in self.query.exclude])
      )
  
  def check_lvl(self):
    return self.lvl > self.query.max_lvl
              
  def __repr__(self):
    return '%s %s' % (self.symbol, self.file_name)

  def get_symbol(self):
    if self.is_file:
      if self.extension == 'unknownFile':
        return self.config.unknownFileSymbol
      
      for symbol, ext_list in self.config.symbols.items():
        if self.extension in ext_list:
          return symbol
    else:
      return self.config.folderSymbol
    
  
class Config:
  def __init__(self, file_location: str):
    
    self.fileLocation = file_location
    
    with open(self.fileLocation, 'r', encoding='utf-8') as f:
      
      self.defaultConfig = load(f)
      
    for key, value in self.items():
      
      self.__setattr__(key,value)
  
  def __repr__(self) -> str:
    return dumps((self.defaultConfig), indent=2)
  
  def items(self):
    return self.__dict__().items()
  
  def __dict__(self):
    return self.defaultConfig
  
  def get_extensions(self):
    ext = []
    for value in self.symbols.values():
      ext.extend(value)
    return ext
  
class Query:
  def __init__(self, args, last_diving_file):
    self.path = args.path.replace('\\','/')
    self.detail = args.detail
    self.max_lvl = args.max_lvl
    self.search = args.search
    self.exclude = args.exclude
    self.indent = args.indent
    self.log = args.log
    self.mode = args.mode
    
    with open(last_diving_file, 'w') as f:
      dump(self.__dict__, f, indent=2)
  
class Data:
  def __init__(self, query) -> None:
    self.file_count = 0
    self.dir_count = 0
    self.excluded_files = 0
    self.excluded_dirs = 0
    self.matches = 0
    self.results = []
    self.query = query
    
  def display_output(self):
    output = '%s directories; %s files' % (
    
    '{:,}'.format(self.dir_count-1),
    '{:,}'.format(self.file_count)
    
    )
    
    if self.query.search != [] and self.matches > 0:
      output = output+'; '+Fore.LIGHTGREEN_EX+'%s matches'+Fore.WHITE
      output = output % self.matches

    if self.query.exclude != [] and self.excluded_dirs + self.excluded_files > 0:
      output = output+'; '+Fore.RED+'%s excluded (%s directories, %s files)'+Fore.WHITE
      output = output % (
        self.excluded_dirs + self.excluded_files, self.excluded_dirs, self.excluded_files
        )
    
    print(output)
  
  def map_iter(self, func, iter):
    for item in iter:
      func(item)
  
  def display(self):
    
    print('-------------------------------')
    self.map_iter(lambda item: print(item.display()), self.results)
    print(Fore.WHITE+'-------------------------------')
    self.display_output()