def list_files(path: str) -> list[str]:
   from os import listdir
   return listdir(path)

print(list_files("January/1_File-System-System-Info/Day12_DirectoryLister"))