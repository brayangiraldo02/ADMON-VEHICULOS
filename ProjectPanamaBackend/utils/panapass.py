import pytz
from datetime import datetime
import csv

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
  #fecha = '2025_06_11'
  
  if company == '58':
    try:
      path = path_58 + f'/Informe_PanaPass_{fecha}_pm.txt'
      with open(path, 'r') as file:
        return path
    except FileNotFoundError:
      path = path_58 + f'/Informe_PanaPass_{fecha}_am.txt'
      with open(path, 'r') as file:
        return path
  elif company == '10':
    try:
      path = path_10 + f'/Informe_PanaPass_{fecha}_pm.txt'
      with open(path, 'r') as file:
        return path
    except FileNotFoundError:
      path = path_10 + f'/Informe_PanaPass_{fecha}_am.txt'
      with open(path, 'r') as file:
        return path

#-----------------------------------------------------------------------------------------------

def search_value_in_txt(search_column, search_value, return_column, path):
  """
  Searches for a specific value in a text file and returns the corresponding value from another column.
  """
  with open(path, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
      if row[search_column] == search_value:
        return row[return_column]
  return None

#-----------------------------------------------------------------------------------------------