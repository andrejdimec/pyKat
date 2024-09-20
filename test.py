import arcpy

# Sign in to ArcGIS Online
arcpy.SignInToPortal("https://www.arcgis.com", "komunala_radgona", "kora1234")

# List of layers to overwrite
layers_to_overwrite = [
    {"path": "C:/path/to/your/layer1.lyrx", "service_name": "ExistingServiceName1"},
    {"path": "C:/path/to/your/layer2.lyrx", "service_name": "ExistingServiceName2"},
    # Add more layers as needed
]

for layer in layers_to_overwrite:
    # Load the layer
    layer_file = arcpy.mp.LayerFile(layer["path"])
    map_doc = arcpy.mp.ArcGISProject("CURRENT").listMaps()[0]
    map_doc.addLayer(layer_file)

    # Create a sharing draft
    sharing_draft = map_doc.getWebLayerSharingDraft(
        "HOSTING_SERVER", "FEATURE", layer["service_name"]
    )
    sharing_draft.overwriteExistingService = True

    # Stage the service
    sddraft_path = f"C:/path/to/output/{layer['service_name']}.sddraft"
    sharing_draft.exportToSDDraft(sddraft_path)
    sd_path = f"C:/path/to/output/{layer['service_name']}.sd"
    arcpy.StageService_server(sddraft_path, sd_path)

    # Upload and publish the service
    arcpy.UploadServiceDefinition_server(sd_path, "My Hosted Services")

    # Clean up
    map_doc.removeLayer(layer_file)

print("All layers have been successfully overwritten.")
