import arcpy
import os

# Define the project and map
project_path = r"d:\Kataster\GR_D96\Projects\dev_project.aprx"
print(f"Loading project from {project_path}")
project = arcpy.mp.ArcGISProject(project_path)

map_name = "map1"
print(f"Accessing map: {map_name}")
map_obj = project.listMaps(map_name)[0]

# Define the layer to be shared
layer_name = "jasek_razno4"
print(f"Finding layer: {layer_name}")
layer = map_obj.listLayers(layer_name)[0]
print("layer", layer.name)

# Define output paths
sddraft_output_filename = os.path.join(
    r"d:\Kataster\GR_D96\Projects", "jasek_razno2.sddraft"
)
sd_output_filename = os.path.join(r"d:\Kataster\GR_D96\Projects", "jasek_razno2.sd")

print(f"Creating sharing draft for layer: {layer_name}")
# Create a sharing draft
sharing_draft = map_obj.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", layer)
sharing_draft.exportToSDDraft(sddraft_output_filename)

print(f"Staging service from {sddraft_output_filename} to {sd_output_filename}")
# Stage the service
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

print(f"Uploading service definition to ArcGIS Online")
# Upload the service definition
arcpy.server.UploadServiceDefinition(sd_output_filename, "My Hosted Services")

print("Layer successfully uploaded to ArcGIS Online.")
