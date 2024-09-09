import arcpy
import os
import sys


# TODO Zadnja - dela
# Function to print and log progress
def log(message):
    print(message)


def delete_temp():
    # Delete the temporary files after the upload is complete
    try:
        log("Deleting temporary files...")
        if os.path.exists(sddraft):
            os.remove(sddraft)
            log(f"Deleted: {sddraft}")
        if os.path.exists(sd):
            os.remove(sd)
            log(f"Deleted: {sd}")
        if os.path.exists(thumb):
            os.remove(thumb)
            log(f"Deleted: {thumb}")
    except Exception as e:
        log(f"Error while deleting temporary files: {str(e)}")


# Define input variables
project_path = r"d:\Kataster\GR_D96\Projects\dev_project.aprx"
map_name = "map1"
layer_name = "jasek_razno6"

# ArcGIS Online credentials
portal_url = "https://www.arcgis.com"
username = "komunala_radgona"
password = "kora1234"

# Define the output service name using the layer name
output_service_name = layer_name

# Start logging process
log("Starting the layer sharing process...")

# Sign into ArcGIS Online
log("Signing into ArcGIS Online...")
arcpy.SignInToPortal(portal_url, username, password)

# Open the ArcGIS Pro project
log(f"Opening ArcGIS Pro project at: {project_path}")
aprx = arcpy.mp.ArcGISProject(project_path)

# Access the specified map
log(f"Accessing the map: {map_name}")
mymap = aprx.listMaps(map_name)[0]

# Find and confirm the layer exists in the map
log(f"Looking for the layer: {layer_name}")
layer = None
for lyr in mymap.listLayers():
    if lyr.name == layer_name:
        layer = lyr
        log(f"Layer '{layer_name}' found.")
        break

if not layer:
    log(f"Layer '{layer_name}' not found in the map. Exiting...")
    sys.exit(1)

# Set the ArcGIS environment to use the scratch folder for temporary files
scratch_folder = arcpy.env.scratchFolder
if not scratch_folder:
    scratch_folder = os.path.join(os.getcwd(), "scratch")
    os.makedirs(scratch_folder, exist_ok=True)
    arcpy.env.scratchFolder = scratch_folder

log(f"Using scratch folder: {scratch_folder}")

# Define paths for service definition draft and staged service
sddraft = os.path.join(scratch_folder, f"{layer_name}.sddraft")
sd = os.path.join(scratch_folder, f"{layer_name}.sd")
thumb = os.path.join(scratch_folder, "Thumbnail.png")


# Create a service definition draft
log(f"Creating Service Definition Draft for layer '{layer_name}'...")

description = f"This web layer is created from the {layer_name} layer in ArcGIS Pro"

arcpy.mp.CreateWebLayerSDDraft(
    map_or_layers=layer,  # Input layer object
    out_sddraft=sddraft,  # Output path for .sddraft file
    service_name=output_service_name,  # Name of the web service to be published
    service_type="HOSTING_SERVER",  # ArcGIS Online hosting server
    server_type="MY_HOSTED_SERVICES",  # Service connection type for ArcGIS Online
    folder_name="_Dev",  # Folder on ArcGIS Online (empty means root folder)
    overwrite_existing_service=True,  # Overwrite existing service with the same name
    summary="Web layer of the Arcgis Pro layer",  # Summary for the service
    tags="ArcGIS Online, arcpy",  # Tags to describe the web layer
    credits="andrejd",
    description="Opis",  # Detailed description
)

# Skip AnalyzeForSD and move directly to staging the service
log(f"Staging the service definition to create the .sd file at {sd}...")
try:
    arcpy.StageService_server(sddraft, sd)
    warnings = arcpy.GetMessages(1)
    if warnings:
        log(f"Warnings:")
        for warning in warnings:
            log(f"\t{warning}")
except Exception as e:
    log(f"Errors:")
    log("Sddraft not staged. Analyzer errors encountered - {}".format(str(e)))
    delete_temp()
    sys.exit("Napaka pri staging.")

# Upload the staged service definition to ArcGIS Online
log(f"Uploading and publishing the service '{layer_name}' to ArcGIS Online...")
try:
    arcpy.UploadServiceDefinition_server(sd, "MY_HOSTED_SERVICES")
    f"Layer '{layer_name}' has been successfully shared as a web layer on ArcGIS Online."
except Exception as e:
    log("Upload error - {}".format(str(e)))
    delete_temp()
    sys.exit("Napaka pri upload.")

delete_temp()
# Final log confirming completion
log(f"Končano v.")
