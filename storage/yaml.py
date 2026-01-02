import os
import yaml as yamllib
import io
import config
from datetime import date, timedelta, time
import data

def load(file):
    # return empty array if file is empty
    if os.stat(file).st_size == 0:
        os.remove(file)
        return []
    with io.open(file, 'r') as data:
        yamlData = yamllib.safe_load(data)
    return yamlData

def save(days):
    yamlData = {}
    # serialize with date keys
    for day in days.days:
        yamlData[day.date.strftime("%Y-%m-%d")] = day
    
    # Define how different objects should be represented in YAML
    yamllib.add_representer(date, lambda self, value: self.represent_str(value.strftime("%Y-%m-%d")))
    yamllib.add_representer(time, lambda self, value: self.represent_str('{d.hour}:{d.minute:02}'.format(d=value)))
    yamllib.add_representer(timedelta, lambda self, value: self.represent_str(data.format_delta(value)))
    yamllib.add_multi_representer(data.block.Block, lambda self, value: self.represent_dict(_filter_empty(value.__dict__)))
    yamllib.add_multi_representer(data.day.Day, lambda self, value: self.represent_dict(_filter_empty(value.__dict__)))
    
    
    yamlData = yamllib.dump(
        yamlData,
        sort_keys=True
    )
    if yamlData:
        file = io.open(config.log_path(), 'w', encoding='utf8')
        file.write(yamlData)
        file.close()

# see https://betterprogramming.pub/how-to-remove-null-none-values-from-a-dictionary-in-python-1bedf1aab5e4
def _filter_empty(dict: dict):
    return {
      k:v
      for k, v in dict.items()
      if v is not None and v is not ""
   }