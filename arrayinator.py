import os
import rasterio
import numpy as np
from tqdm import tqdm
from glob import glob

tif_folder = r'D:\Projects\Project-1\occurrence-rasters'
output_dir = '../occurrence-arrays' 

os.makedirs(output_dir, exist_ok=True)
tif_files = glob(os.path.join(tif_folder, 'occurrence_*.tif'))

def tif_to_numpy_and_save(tif_path, output_dir):
    with rasterio.open(tif_path) as src:
        numpy_array = src.read()
        event_date = os.path.basename(tif_path).split('_')[1].split('.')[0].replace('-', '')        
        npz_path = os.path.join(output_dir, f"{event_date}.npz")
        np.savez_compressed(npz_path, numpy_array)

for tif_file in tqdm(tif_files):
    tif_to_numpy_and_save(tif_file, output_dir)

print("All .tif files have been converted to NumPy arrays.")
