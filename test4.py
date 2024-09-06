import arcpy
import os

# Define the project and map
project_path = r"d:\Kataster\GR_D96\Projects\dev_project.aprx"
project = arcpy.mp.ArcGISProject(project_path)
map_name = "map1"  # Change this to the name of your map if different
map_obj = project.listMaps(map_name)[0]

# Define the layer to be shared
layer_name = "jasek_razno"
layer = map_obj.listLayers(layer_name)[0]

# Define output paths
sddraft_output_filename = os.path.join(
    r"d:\Kataster\GR_D96\Projects", "jasek_razno.sddraft"
)
sd_output_filename = os.path.join(r"d:\Kataster\GR_D96\Projects", "jasek_razno.sd")

# Create a sharing draft
sharing_draft = map_obj.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", layer_name)
sharing_draft.exportToSDDraft(sddraft_output_filename)

# Stage the service
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Analyze the service definition draft
analysis = arcpy.mapping.AnalyzeForSD(sddraft_output_filename)

# Check for errors
if analysis["errors"] == {}:
    # Upload the service definition
    arcpy.server.UploadServiceDefinition(sd_output_filename, "My Hosted Services")
    print("Layer successfully uploaded to ArcGIS Online.")
else:
    # Print errors
    print("Errors were found during analysis:")
    for key, value in analysis["errors"].items():
        print(f"{key}: {value}")
