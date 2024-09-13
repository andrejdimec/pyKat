import arcpy
import os
import xml.dom.minidom as DOM
import vars

# Sign in to portal
arcpy.SignInToPortal("https://www.arcgis.com", "komunala_radgona", "kora1234")

# Set output file names
outdir = r"D:\Temp"

service_name = "jasek_razno10"
sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Reference map to publish
project = os.path.join(vars.aprx_path, vars.aprx_name)
aprx = arcpy.mp.ArcGISProject(project)
m = aprx.listMaps("map1")[0]

# Create FeatureSharingDraft and set metadata, portal folder, export data properties, and CIM symbols
server_type = "HOSTING_SERVER"
sddraft = m.getWebLayerSharingDraft(server_type, "FEATURE", service_name)
sddraft.credits = "These are credits"
sddraft.description = "This is description"
sddraft.summary = "This is summary"
sddraft.tags = "tag1, tag2"
sddraft.useLimitations = "These are use limitations"
sddraft.portalFolder = ""
sddraft.allowExporting = True
sddraft.useCIMSymbols = True

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

# Read the .sddraft file
docs = DOM.parse(sddraft_output_filename)
key_list = docs.getElementsByTagName("Key")
value_list = docs.getElementsByTagName("Value")

# Change following to "true" to share
SharetoOrganization = "false"
SharetoEveryone = "true"
SharetoGroup = "false"
# If SharetoGroup is set to "true", uncomment line below and provide group IDs
GroupID = (
    ""  # GroupID = "f07fab920d71339cb7b1291e3059b7a8, e0fb8fff410b1d7bae1992700567f54a"
)

# Each key has a corresponding value. In all the cases, value of key_list[i] is value_list[i].
for i in range(key_list.length):
    if key_list[i].firstChild.nodeValue == "PackageUnderMyOrg":
        value_list[i].firstChild.nodeValue = SharetoOrganization
    if key_list[i].firstChild.nodeValue == "PackageIsPublic":
        value_list[i].firstChild.nodeValue = SharetoEveryone
    if key_list[i].firstChild.nodeValue == "PackageShareGroups":
        value_list[i].firstChild.nodeValue = SharetoGroup
    if SharetoGroup == "true" and key_list[i].firstChild.nodeValue == "PackageGroupIDs":
        value_list[i].firstChild.nodeValue = GroupID

# Write to the .sddraft file
f = open(sddraft_output_filename, "w")
docs.writexml(f)
f.close()

# Stage Service
print("Start Staging")
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Share to portal
print("Start Uploading")
arcpy.server.UploadServiceDefinition(sd_output_filename, server_type)

print("Finish Publishing")
