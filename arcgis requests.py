import requests
import json
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

# Fetch GeoJSON data from the URL
url = "https://ipi.eprostor.gov.si/wfs-si-gurs-kn/ogc/features/collections/SI.GURS.KN:HISNE_STEVILKE/items?bbox=15.8821,46.5862,16.0373,46.6881&filter-lang=cql-text&additionalProp1"
response = requests.get(url)
geojson_data = response.json()

# Connect to your ArcGIS Online or Enterprise
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# Create a new feature service
service_name = "GeoJSON_Feature_Service"
feature_service = gis.content.create_service(name=service_name, service_type='featureService')

# Create a FeatureLayerCollection from the new service
feature_layer_collection = FeatureLayerCollection.fromitem(feature_service)

# Overwrite the feature layer with the GeoJSON data
feature_layer_collection.manager.overwrite(geojson_data)

print("GeoJSON data has been successfully stored in the ArcGIS feature class.")


import requests
import json
import arcpy

# Fetch GeoJSON data from the URL
url = "https://ipi.eprostor.gov.si/wfs-si-gurs-kn/ogc/features/collections/SI.GURS.KN:HISNE_STEVILKE/items?bbox=15.8821,46.5862,16.0373,46.6881&filter-lang=cql-text&additionalProp1"
response = requests.get(url)
geojson_data = response.json()

# Save GeoJSON data to a temporary file
geojson_file = "temp_data.geojson"
with open(geojson_file, 'w') as f:
    json.dump(geojson_data, f)

# Define the output file geodatabase and feature class
gdb_path = r"C:\path\to\your\geodatabase.gdb"
feature_class_name = "GeoJSON_Feature_Class"

# Convert GeoJSON to feature class
arcpy.conversion.JSONToFeatures(geojson_file, f"{gdb_path}\\{feature_class_name}")

print("GeoJSON data has been successfully stored in the ArcGIS feature class.")
