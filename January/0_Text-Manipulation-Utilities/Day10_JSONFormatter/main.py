
def pretty_print_json(json_string):
   import json

   try:
      parsed_json = json.loads(json_string)
      print(json.dumps(parsed_json, indent=3))
   except:
      print("Not a proper JSON string")

pretty_print_json('[{"name": "Berlin", "population": 3645000, "country": "Germany"}, {"name": "Hamburg", "population": 1841000, "country": "Germany"}]')