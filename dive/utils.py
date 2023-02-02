from argparse import Namespace
from os import chdir, listdir, walk
from os.path import dirname, join
from time import sleep

from dive.classes import Config, Data, File, Query

file_dir = dirname(__file__)


def get_path_data(args: Namespace, config: Config, last_diving_file: str) -> Data:

  QUERY = Query(args, last_diving_file)

  chdir(args.path)

  DATA = Data(QUERY)

  loading_msg = 'Diving...'

  if QUERY.DETAIL:
    loading_msg = loading_msg.replace('...', ' deep...')

  if QUERY.LOG:
    loading_msg = loading_msg.replace('...', ' and logging...')

  if QUERY.SEARCH != []:
    loading_msg = loading_msg.replace('...', ' while looking for %s terms...' % len(QUERY.SEARCH))

  if QUERY.EXCLUDE != []:
    loading_msg = loading_msg.replace('...', ' (ignoring %s terms)...' % len(QUERY.EXCLUDE))

  print('----------------------------')
  print(loading_msg)

  sleep(3)

  if QUERY.DETAIL:
    for root, dirs, files in walk(QUERY.PATH):
      ROOT_OBJ = File(root, config, QUERY)
      if ROOT_OBJ.check_lvl():
        continue

      if QUERY.LOG:
        print(root)

      if ROOT_OBJ.check_match():
        DATA.matches += 1

      DATA.results.append(ROOT_OBJ)
      DATA.dir_count += 1

      if QUERY.MODE in ['all', 'folders']:
        for direc in dirs:
          PATH = join(root, direc)
          DIR_OBJ = File(PATH, config, QUERY)

          if DIR_OBJ.check_lvl():
            continue

          if DIR_OBJ.check_exclude():
            DATA.excluded_dirs += 1
            continue

          if QUERY.LOG:
            print(PATH)

          if DIR_OBJ.check_match():
            DATA.matches += 1

          DATA.dir_count += 1

      if QUERY.MODE in ['all', 'files']:
        for file in files:
          PATH = join(root, file)
          FILE_OBJ = File(PATH, config, QUERY)

          if FILE_OBJ.check_exclude():
            DATA.excluded_files += 1
            continue

          if FILE_OBJ.check_lvl():
            continue

          if QUERY.LOG:
            print(PATH)

          if FILE_OBJ.check_match():
            DATA.matches += 1

          DATA.results.append(FILE_OBJ)
          DATA.file_count += 1

    return DATA
  else:

    FILE_OBJ = File(QUERY.PATH, config, QUERY)
    DATA.results.append(FILE_OBJ)
    DATA.dir_count += 1

    for item in listdir(QUERY.PATH):
      PATH = join(QUERY.PATH, item)
      FILE_OBJ = File(PATH, config, QUERY)

      if not FILE_OBJ.IS_FILE and QUERY.MODE == 'files' or (
        FILE_OBJ.IS_FILE and QUERY.MODE == 'folders'
      ):
        continue

      if FILE_OBJ.check_exclude():
        if FILE_OBJ.IS_FILE:
          DATA.excluded_files += 1
        else:
          DATA.excluded_dirs += 1

      if QUERY.LOG:
        print(PATH)

      if FILE_OBJ.check_match():
        DATA.matches += 1

      DATA.results.append(FILE_OBJ)

      if FILE_OBJ.IS_FILE:
        DATA.file_count += 1
      else:
        DATA.dir_count += 1

    return DATA


def expose(content: any):
  print('----------------------------')
  print(str(content))
  print('----------------------------')


def split_arg(content: str):
  return content.replace(', ', ',').replace(' ,', ',').split(',')


defaultConfiguration = {
  "defaultDetail": False,
  "defaultMaxLvl": 3,
  "defaultExclude": [".sys", ".tmp", "node_modules", ".git", ".env"],
  "defaultIndent": 2,
  "defaultMode": "all",
  "symbols": {
    "🎶": ["mp3", "wav"],
    "🗜️": ["7z", "rar", "zip"],
    "📝": ["txt", "md", "log"],
    "🖼️": ["jpg", "jpeg", "png", "pdf", "svg", "ico", "gif"],
    "🖥️": ["bat", "sh", "msi"],
    "⚙️": ["ini", "dll", "yml"],
    "🔧": ["sys", "json"],
    "🎬": ["mp4", "avi"],
    "✒️": ["lnk"],
    "🐍": ["py", "python"],
    "💾": ["exe"],
    "💿": ["iso"],
    "📤": ["torrent"]
  },
  "unknownFileSymbol": "📄",
  "matchedFileSymbol": "❗",
  "folderSymbol": "📁"
}
