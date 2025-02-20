from csv import reader
from json import dumps

STD_PATH = "January/2_Data-Input-Output/Day23_CSVToJson"

def read_csv(file_path: str = STD_PATH + "/test.csv") -> list[dict[str, str]]:
   with open(file_path, 'r') as csv_file:
      csv_reader = reader(csv_file)
      header = next(csv_reader)
      if header != None:
         data = []
         for row in csv_reader:
            row_dict = {}
            for i in range(len(header)):
               row_dict[header[i]] = row[i]
            data.append(row_dict)
         return data
      else:
         return []

def csv_to_json(file_path: str = STD_PATH) -> str:
   items = read_csv(STD_PATH + "/test.csv")
   json_str = dumps(items, indent=4)
   with open(f"{file_path}/output.json", "w") as json_file:
      json_file.write(json_str)
   return json_str

print(csv_to_json())