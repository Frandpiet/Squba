# coding: utf-8

from os.path import dirname

FILE_DIR = dirname(__file__)


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
