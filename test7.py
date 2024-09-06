import arcpy
import os

#
# TODO DELA!!!

# ArcGIS Online portal credentials
portal_url = "https://www.arcgis.com"  # or your enterprise portal URL
username = "komunala_radgona"
password = "kora1234"


# Set the path to the ArcGIS Pro project (.aprx) and the map name
aprx_path = r"d:\Kataster\GR_D96\Projects\dev_project.aprx"
map_name = "map1"
layer_name = "jasek_razno5"
temp_path = r"d:\temp"

# Sign in to your ArcGIS Online account
# Replace with your credentials or make sure you're signed into the portal via ArcGIS Pro
arcpy.SignInToPortal("https://www.arcgis.com", username, password)


# Log function
def log(message):
    print(message)


try:
    log(f"Opening ArcGIS Pro project: {aprx_path}")

    # Open the ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject(aprx_path)

    log(f"Accessing map: {map_name}")

    # Access the specified map
    map_obj = aprx.listMaps(map_name)[0]

    log(f"Looking for the layer: {layer_name}")

    # Check if the layer exists
    layer = None
    for lyr in map_obj.listLayers():
        if lyr.name == layer_name:
            layer = lyr
            break

    if layer is None:
        raise Exception(f"Layer '{layer_name}' not found in map '{map_name}'.")

    log(f"Layer '{layer_name}' found. Preparing to share as web layer.")

    # Define the service definition draft output location
    sddraft = os.path.join(os.getcwd(), f"{layer_name}.sddraft")

    # Create a service definition draft only for the selected layer
    log("Creating service definition draft...")
    arcpy.mp.CreateWebLayerSDDraft(
        layer, sddraft, layer_name, "MY_HOSTED_SERVICES", "FEATURE_ACCESS"
    )

    log(f"Service definition draft created at: {sddraft}")

    # Analyze the service definition draft (optional, to ensure it's valid)
    # log("Analyzing the service definition draft...")
    # analysis = arcpy.mapping.AnalyzeForSD(sddraft)
    # log(f"Analysis result: {analysis}")

    # Stage the service definition
    sd = os.path.join(os.getcwd(), f"{layer_name}.sd")
    log("Staging the service definition...")
    arcpy.StageService_server(sddraft, sd)

    log(f"Service definition staged at: {sd}")

    # Upload the service definition to ArcGIS Online
    log("Uploading the service definition to ArcGIS Online...")
    arcpy.UploadServiceDefinition_server(sd, "My Hosted Services")

    log(f"Layer '{layer_name}' successfully shared as a web layer.")

except Exception as e:
    log(f"An error occurred: {e}")
