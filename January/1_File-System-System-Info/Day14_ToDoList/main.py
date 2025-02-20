import os

STD_FOLDER: str = "January/1_File-System-System-Info/Day14_ToDoList/lists"
STD_NAME: str = "std"
STD_PATH: str = os.path.join(STD_FOLDER, STD_NAME)

def create_todo_list(name: str = STD_NAME, folder: str = STD_FOLDER) -> None:
   
   if not os.path.exists(folder):
      os.makedirs(folder)
   
   file_path = os.path.join(folder, name)
   if os.path.exists(file_path):
      print(f"{name} already exists")
      return
   
   with open(file_path, "w") as f:
      f.write("")
   print(f"To-do list '{name}' created at '{file_path}'")

def read_todo_list(file_path: str = STD_PATH) -> None:
   with open(file_path, "r") as f:
      return f.readlines()

def add_todo(task: str, progress: str = "not-started", file_path: str = STD_PATH) -> None:
   
   if f"\"{task}\"{progress}\n" in read_todo_list(file_path):
      print("Task already exists")
      return
      
   with open(file_path, "a") as f:
      f.write(f"\"{task}\"{progress}\n")

def update_progress(task: str, progress: str, file_path: str = STD_PATH):
   lines = read_todo_list(file_path)
   updated_lines = []
   task_found = False

   for line in lines:
      if f"\"{task}\"" in line:
            updated_lines.append(f"\"{task}\" {progress}\n")
            task_found = True
      else:
            updated_lines.append(line)

   if not task_found:
      print(f"Task '{task}' not found in the to-do list.")
      return

   with open(file_path, "w") as f:
      f.writelines(updated_lines)
   print(f"Progress updated for task '{task}' to '{progress}'.")

create_todo_list()
add_todo("get Hello World tattooed")
print(read_todo_list())
update_progress("get Hello World tattooed", "done")
print(read_todo_list())