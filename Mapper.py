import os
import sys
import requests
from tqdm import tqdm

class Mapper:
    def __init__(self):
        
        self.base_URL = "https://os.zhdk.cloud.switch.ch/chelsav2/GLOBAL/monthly"
        self.variable_map = {
            "clt": "clt",
            "cmi": "cmi",
            "hurs": "hurs",
            "pet": "pet_penman",
            "pr": "pr",
            "rsds": "rsds",
            "sfcWind": "sfcWind",
            "tas": "tas",
            "tasmin": "tasmin",
            "vpd": "vpd",
            "tasmax": "tasmax"
        }

    def generate_URL(self, variable, month, year):
        
        if variable in self.variable_map:
            # Only rsds shows this URL pattern so far.
            if variable == "rsds":
                return f"{self.base_URL}/{variable}/CHELSA_{self.variable_map[variable]}_{year}_{str(month).zfill(2)}_V.2.1.tif"
            return f"{self.base_URL}/{variable}/CHELSA_{self.variable_map[variable]}_{str(month).zfill(2)}_{year}_V.2.1.tif"
        else:
            raise ValueError(f"Unknown variable: {variable}")
    
    def download_file(self, URL, output_path):

        os.makedirs(output_path, exist_ok=True)
        local_file_path = os.path.join(output_path, os.path.basename(URL))

        try:
            with requests.get(URL, stream=True) as response:
                total_file_size = int(response.headers.get('content-length', 0))
                block_size = 1024 # 1KB

                with tqdm(total=total_file_size, unit='iB', unit_scale=True) as progress_bar:
                    with open(local_file_path, 'wb') as file:
                        for data in response.iter_content(block_size):
                            progress_bar.update(len(data))
                            file.write(data)

        except Exception as e:
            print(f"Error downloading {URL}: {e}")

    def download_monthly_variables(self, month, year, output_path):

        output_path = os.path.join(output_path, f"{year}-{month}")

        for variable in self.variable_map:
            url = self.generate_URL(variable, month, year)
            self.download_file(url, output_path)