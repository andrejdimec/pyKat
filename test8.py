import arcpy
import os


# Define log function
def log(message):
    print(message)
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")


# Define the project and map
project_path = r"d:\Kataster\GR_D96\Projects\dev_project.aprx"
log(f"Loading project from {project_path}")
project = arcpy.mp.ArcGISProject(project_path)

map_name = "map1"
log(f"Accessing map: {map_name}")
map_obj = project.listMaps(map_name)[0]

# Define the layer to be shared
layer_name = "jasek_razno6"
log(f"Finding layer: {layer_name}")
layer_list = map_obj.listLayers(layer_name)

if not layer_list:
    log(f"Layer {layer_name} not found in map {map_name}. Exiting script.")
else:
    layer = layer_list[0]
    log(f"Layer found: {layer.name}")

    # Define output paths using the layer_name variable
    sddraft_output_filename = os.path.join(
        r"d:\Kataster\GR_D96\Projects", f"{layer_name}.sddraft"
    )
    sd_output_filename = os.path.join(
        r"d:\Kataster\GR_D96\Projects", f"{layer_name}.sd"
    )

    log(f"Creating sharing draft for layer: {layer_name}")
    # Create a sharing draft
    arcpy.mp.CreateWebLayerSDDraft(
        layer,
        sddraft_output_filename,
        layer_name,
        "MY_HOSTED_SERVICES",
        "FEATURE_ACCESS",
    )

    log(f"Staging service from {sddraft_output_filename} to {sd_output_filename}")
    # Stage the service
    arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

    log(f"Uploading service definition to ArcGIS Online")
    # Upload the service definition
    arcpy.server.UploadServiceDefinition(sd_output_filename, "My Hosted Services")

    log("Layer successfully uploaded to ArcGIS Online.")
