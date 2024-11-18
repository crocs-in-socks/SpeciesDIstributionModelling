from Mapper import *

month = "01"
year = "1980"
output_path = "../CHELSA-direct-download"

mapper = Mapper()
mapper.download_monthly_variables(month, year, output_path)