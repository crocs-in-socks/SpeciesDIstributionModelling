import os
import rasterio
from tqdm import tqdm
import geopandas as gpd
from rasterio.mask import mask

def generate_sweden_shapefile(admin_countries_path, output_path):
    admin_countries_shapefile = admin_countries_path
    countries = gpd.read_file(admin_countries_shapefile)
    sweden = countries[countries['NAME'] == 'Sweden']  # Or use 'ISO_A3' == 'SWE'
    sweden.to_file(output_path)
    print(f"\nSweden's shapefile has been saved at: {output_path}\n")

def regenerate_tiff_basename(basename):
    basename = basename.split('.tif')[0]

    parts = basename.split('_')    
    variable = parts[1]
    month = parts[2]
    year = parts[3]
    version = parts[4].replace('.', '_')

    return f"CHELSA_{version}_{variable}_{year}-{month}.tif"

def mask_GeoTIFF_with_sweden(tiff_path, shape, output_path):

    with rasterio.open(tiff_path) as src:

        # Reproject the shapefile to match the CRS of the GeoTIFF
        sweden_shape_proj = shape.to_crs(src.crs)

        # Convert the shapefile geometry to a format readable by rasterio
        shapes = [sweden_shape_proj.geometry.values[0]]

        # Apply the mask
        out_image, out_transform = mask(src, shapes, crop=True)

        # Update metadata for the masked image
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        basename = regenerate_tiff_basename(os.path.basename(tiff_path))
        output_path = os.path.join(output_path, basename)

        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(out_image)
        # print(f"Masked file saved at: {output_path}")

folder_path = r'D:\Projects\Project-1\CHELSA-clt'
sweden_shapefile = r'D:\Projects\Project-1\naturalearth-countries-shapefile\sweden_boundary.shp'
output_path = r'D:\Projects\Project-1\CHELSA-clt-clipped'

os.makedirs(output_path, exist_ok=True)

sweden_mask = gpd.read_file(sweden_shapefile)

# Process each GeoTIFF in the folder
for tiff_file in tqdm(os.listdir(folder_path)):
    if tiff_file.endswith('.tif'):  # Process only GeoTIFF files
        tiff_path = os.path.join(folder_path, tiff_file)
        mask_GeoTIFF_with_sweden(tiff_path, sweden_mask, output_path)

print("Masking complete!")