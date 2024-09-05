import arcpy
from arcpy import mp
from arcpy.sharing import CreateSharingDraft
from arcpy.server import UploadServiceDefinition

# Define the project and map
project_path = r"d:\Kataster\GR_D96\Projects\Kataster_2024_09.aprx"
map_name = "Kataster D96"
layer_name = "Jasek_razno"
web_map_name = "Karta za testiranje"

# Log in to ArcGIS Online
print("Logging in to ArcGIS Online...")
arcpy.SignInToPortal("https://www.arcgis.com", "komunala_radgona", "kora1234")
print("Logged in successfully.")

# Open the ArcGIS Pro project
print(f"Opening project: {project_path}")
aprx = mp.ArcGISProject(project_path)
print("Project opened successfully.")

# Get the map and the layer
print(f"Getting map: {map_name}")
map_obj = aprx.listMaps(map_name)[0]
print(f"Getting layer: {layer_name}")
layer = map_obj.listLayers(layer_name)[0]

# Create a sharing draft for the web layer
print("Creating sharing draft...")
sharing_draft = map_obj.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", layer_name)
sharing_draft.summary = "This is a test layer."
sharing_draft.tags = "test, Jasek_razno"
sharing_draft.description = "Layer for testing purposes."
sharing_draft.credits = "Created by [Your Name]"
sharing_draft.useLimitations = "For testing only."
print("Sharing draft created successfully.")

# Save the sharing draft to a service definition draft file
sddraft_path = r"d:\Kataster\GR_D96\Projects\Jasek_razno.sddraft"
print(f"Exporting sharing draft to: {sddraft_path}")
sharing_draft.exportToSDDraft(sddraft_path)
print("Sharing draft exported successfully.")

# Stage the service
sd_path = r"d:\Kataster\GR_D96\Projects\Jasek_razno.sd"
print(f"Staging service to: {sd_path}")
arcpy.StageService_server(sddraft_path, sd_path)
print("Service staged successfully.")

# Upload the service definition and publish the web layer
print("Uploading service definition and publishing web layer...")
arcpy.UploadServiceDefinition_server(sd_path, "My Hosted Services")
print("Layer uploaded and published successfully!")
