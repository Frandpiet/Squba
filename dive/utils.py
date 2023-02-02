from os import chdir, listdir, walk
from os.path import dirname, join
from time import sleep

from colorama import Fore

from dive.classes import Query

file_dir = dirname(__file__)

def get_path_data(args, config, last_diving_file):
  
  from .classes import Data, File
    
  query = Query(args, last_diving_file)
  
  chdir(args.path)
  
  data = Data(query)
  
  loading_msg = 'Diving...'
  
  if query.detail:
    loading_msg = loading_msg.replace('...',' deep...')
    
  if query.log:
    loading_msg = loading_msg.replace('...',' and logging...')
  
  if query.search != []:
    loading_msg = loading_msg.replace('...', ' while looking for %s terms...' % len(query.search))
    
  if query.exclude != []:
    loading_msg = loading_msg.replace('...', ' (ignoring %s terms)...' % len(query.exclude))
  
  print('----------------------------')
  print(loading_msg)
  
  sleep(3)
  
  if query.detail:
    for root,dirs,files in walk(query.path):
      
      r_obj = File(root, config, query)
      
      if r_obj.check_lvl():
        continue
      
      if query.log:
        print(root)
        
      if r_obj.check_match():
        data.matches += 1
        
      data.results.append(r_obj)
    
      data.dir_count += 1
      
      if query.mode in ['all', 'folders']:
        
        for direc in dirs:
          
          path = join(root, direc)
          dir_obj = File(path, config, query)
          
          if dir_obj.check_lvl():
            continue
          
          if dir_obj.check_exclude():
            data.excluded_dirs += 1
            continue
          
          if query.log:
            print(path)
          
          if dir_obj.check_match():
            data.matches += 1
          
          data.dir_count += 1
      
      if query.mode in ['all', 'files']:
        
        for file in files:
          
          path = join(root, file)
          
          file_obj = File(path, config, query)
          
          if file_obj.check_exclude():
            data.excluded_files += 1
            continue
          
          if file_obj.check_lvl():
            continue
          
          if query.log:
            print(path)
          
          if file_obj.check_match():
            data.matches += 1
            
          data.results.append(file_obj)
          
          data.file_count += 1
        
    return data
  else:
    
    file_obj = File(query.path, config, query)
    
    data.results.append(file_obj)
    
    data.dir_count += 1
    
    for item in listdir(query.path):
      
      file_path = join(query.path, item)
      
      file_obj = File(file_path, config, query)
      
      if not file_obj.is_file and query.mode == 'files' or (
        file_obj.is_file and query.mode == 'folders'
      ):
        continue
      
      if file_obj.check_exclude():
        if file_obj.is_file:
          data.excluded_files += 1
        else:
          data.excluded_dirs += 1
      
      if query.log:
        print(file_path)
        
      if file_obj.check_match():
        data.matches += 1
        
      data.results.append(file_obj)
    
      if file_obj.is_file:
        data.file_count += 1
      else:
        data.dir_count += 1
        
    return data

def expose(content):
  print('----------------------------')
  
  print(content)
      
  print('----------------------------')
  
def split_arg(content: str):
  return content.replace(', ',',').replace(' ,',',').split(',')

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
