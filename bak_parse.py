import mmap
import re
import os
import zipfile

truncate_size = 20000 # for big binary files, just use the beginning
tempfilename = "tempfile.xxx"

def main(path):
  bak_path = path
  if os.path.exists(bak_path):
      if zipfile.is_zipfile(bak_path):
          print(f"{bak_path} is a compressed BAK file")
          with open(bak_path, 'rb') as zip_file:
              with zipfile.ZipFile(zip_file, 'r') as zipped:
                  file_list = zipped.namelist()
                  if len(file_list) == 1:
                      file_name = file_list[0]
                      print(f"Unique file {file_name} inside compressed BAK.")
                      # Unable to uncompress directly in memory
                      # So creation of a temp file localy then read in mmap
                      zipped.getinfo(file_name).filename = tempfilename
                      zipped.extract(file_name)
                      bak_path = tempfilename
                  else:
                      print(f"The BAK file {bak_path} doesn't contain a unique file.")
      else:
          print(f"{bak_path} is an uncompressed BAK file.")
          
      with open(bak_path, 'r+b') as f:
          mm = mmap.mmap(f.fileno(), 0)
              
      while mm.tell()<mm.size() :
          read_meta = mm.readline().decode('utf_8','ignore')
          read_path = mm.readline().decode('utf_8','ignore')
          read_attr = mm.readline().decode('utf_8','ignore')
          read_date = mm.readline().decode('utf_8','ignore')
  
          content_start= mm.tell()
          content_size=re.search('\d+', read_attr).group(0)
          content_size=int(content_size)

          read_truncated = false
          if content_size>truncate_size and re.search('binary', read_attr):
              read_cont=mm.read(truncate_size)
              read_truncated = true
              mm.seek(content_size-truncate_size,1)
          else:
              read_cont=mm.read(content_size)
          
          meta.append(read_meta)
          metapath.append(read_path)
          metaattr.append(read_attr)
          metadate.append(read_date)
          contentsize.append(content_size)                
          contentstart.append(content_start)
          content.append(read_cont)
          truncated.append(read_truncated)
          
      mm.close()
  else:
      print(f"{bak_path} file doesn't exist.")
