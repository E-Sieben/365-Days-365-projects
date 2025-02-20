from csv import reader
STD_PATH = "January/2_Data-Input-Output/Day22_CSVReader/test.csv"

def read_csv(file_path: str = STD_PATH) -> list[dict[str, str]]:
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

print(readCSV())