import pytz
from datetime import datetime
import csv
import os

path_58 = '/home/admin/dropbox-alfasoft/Informe_Panapass'
path_10 = '/home/admin/dropbox-alfasoft/Informe_Panapass (1)'

def get_txt_file(company: str):
  """
  Function to retrieve a text file for a given company
  """

  # Datos de la fecha y hora actual
  # Define la zona horaria de Ciudad de Panamá
  panama_timezone = pytz.timezone('America/Panama')
  # Obtén la hora actual en la zona horaria de Ciudad de Panamá
  now_in_panama = datetime.now(panama_timezone)
  # Formatea la fecha según lo requerido
  fecha = now_in_panama.strftime("%Y_%m_%d")
  
  if company == '58':
    base_path = path_58
  elif company == '10':
    base_path = path_10
  else:
    return ''

  for file in ['pm', 'am']:
    path = os.path.join(base_path, f'Informe_PanaPass_{fecha}_{file}.txt')
    if os.path.isfile(path):
      return path

  return ''

#-----------------------------------------------------------------------------------------------

def search_value_in_txt(search_column, search_value, return_column, path):
  """
  Searches for a specific value in a text file and returns the corresponding value from another column.
  """
  with open(path, newline='', encoding='latin-1') as f:
    reader = csv.DictReader(f)
    for row in reader:
      if row[search_column] == search_value:
        return row[return_column]
  return None

#-----------------------------------------------------------------------------------------------