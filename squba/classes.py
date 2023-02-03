# coding: utf-8

from argparse import Namespace
from json import dump, dumps, load
from os import getcwd
from os.path import isfile
from typing import Literal

from colorama import Fore


class Config:
  def __init__(self, file_location: str) -> None:
    self.FILE_LOCATION = file_location
    with open(self.FILE_LOCATION, 'r', encoding='utf-8') as f:
      self.DEFAULT_CONFIG: dict = load(f)
    for key, value in self.items():
      self.__setattr__(key, value)

  def __repr__(self) -> str:
    return dumps((self.DEFAULT_CONFIG), indent=2)

  def items(self) -> dict:
    return self.__dict__().items()

  def __dict__(self) -> dict:
    return self.DEFAULT_CONFIG

  def get_extensions(self) -> list[str]:
    ext: list[str] = []
    for value in self.symbols.values():
      ext.extend(value)
    return ext


class Query:
  def __init__(self, args: Namespace, last_diving_file: str) -> None:
    self.PATH: str = args.path.replace('\\', '/')
    self.DETAIL: bool = args.detail
    self.MAX_LVL: int = args.max_lvl
    self.SEARCH: list[str] = args.search
    self.EXCLUDE: list[str] = args.exclude
    self.INDENT: int = args.indent
    self.LOG: bool = args.log
    self.MODE: str = args.mode

    with open(last_diving_file, 'w', encoding='utf-8') as f:
      dump(self.__dict__, f, indent=2)


class File:
  def __init__(self, path: str, config: Config, query: Query) -> None:
    self.LVL = len(path.replace(getcwd(), '').split('\\'))-1
    self.ROUTE = path
    self.file_name = self.ROUTE.split('\\')[-1]
    self.IS_FILE = isfile(self.ROUTE)
    self.QUERY = query
    self.CONFIG = config

    if self.IS_FILE:
      extension = self.file_name.split('.')[-1]
      self.EXTENSION = extension if extension in self.CONFIG.get_extensions() else 'unknownFile'

    if not self.IS_FILE and self.LVL != 0:
      self.file_name = self.file_name + ' (LvL %s)' % self.LVL

    self.symbol = self.get_symbol()

  def display(self) -> str:
    display = ((' ' * self.QUERY.INDENT) * self.LVL)+self.__repr__()
    return display

  def check_match(self) -> bool:
    check = any([term in self.file_name for term in self.QUERY.SEARCH])
    if check:
      self.file_name = Fore.LIGHTGREEN_EX + self.file_name
    else:
      self.file_name = Fore.RESET + self.file_name
    return check

  def check_exclude(self) -> bool:
    return (
        any([term in self.file_name for term in self.QUERY.EXCLUDE])
      )

  def check_lvl(self) -> bool:
    return self.LVL > self.QUERY.MAX_LVL

  def __repr__(self) -> str:
    return '%s %s' % (self.symbol, self.file_name)

  def get_symbol(self) -> Literal['symbol']:
    if self.IS_FILE:
      if self.EXTENSION == 'unknownFile':
        return self.CONFIG.unknownFileSymbol

      for symbol, ext_list in self.CONFIG.symbols.items():
        if self.EXTENSION in ext_list:
          return symbol
    else:
      return self.CONFIG.folderSymbol


class Data:
  def __init__(self, query: Query) -> None:
    self.file_count = 0
    self.dir_count = 0
    self.excluded_files = 0
    self.excluded_dirs = 0
    self.matches = 0
    self.results = []
    self.QUERY = query

  def display_output(self) -> None:
    output = '%s directories; %s files' % (
      '{:,}'.format(self.dir_count-1),
      '{:,}'.format(self.file_count)
    )

    if self.QUERY.SEARCH != [] and self.matches > 0:
      output = output+'; '+Fore.LIGHTGREEN_EX+'%s matches'+Fore.RESET
      output = output % self.matches

    if self.QUERY.EXCLUDE != [] and self.excluded_dirs + self.excluded_files > 0:
      output = output+'; '+Fore.RED+'%s excluded (%s directories, %s files)'+Fore.RESET
      output = output % (
        self.excluded_dirs + self.excluded_files, self.excluded_dirs, self.excluded_files
        )

    print(output)

  def map_iter(self, func, iter: list | tuple) -> None:
    for item in iter:
      func(item)

  def display(self) -> None:
    print(Fore.RESET+'-------------------------------')
    self.map_iter(lambda item: print(item.display()), self.results)
    print(Fore.RESET+'-------------------------------')
    self.display_output()
