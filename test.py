import arcpy
import os, sys
from arcgis.gis import GIS
import vars


print("Posodobi kanalizacijo na AGO...")


def overwrite_layer():
    # Local paths
    map_name = vars.map_name
    group_layer_name = "Dev"
    prj_path = os.path.join(vars.aprx_path, vars.aktualna_karta)
    source_layer_1 = "Kanalizacijska linija"
    source_layer_2 = "Kanalizacijski jašek"
    print("Project", prj_path)

    # Set portal login
    portal = vars.ago_url
    ago_user = vars.ago_username
    ago_pass = vars.ago_password
    web_folder = "_Dev"

    # Connect to AGO
    print("Connecting to {}".format(portal))
    gis = arcpy.SignInToPortal(portal, ago_user, ago_pass)

    outdir = vars.aprx_path
    service_name = "Kanalizacijska linija"
    sddraft_filename = service_name + ".sddraft"
    sdddraft_output_filename = os.path.join(outdir, sddraft_filename)
    sd_filename = service_name + ".sd"
    sd_output_filename = os.path.join(outdir, sd_filename)

    aprx = arcpy.mp.ArcGISProject(prj_path)
    m = aprx.listMaps(map_name)[0]

    server_type = "HOSTING_SERVER"
    sddraft = m.getWebLayerSharingDraft(server_type, "FEATURE", service_name)
    sddraft.overwriteExistingService = True

    sddraft.exportToSDDraft(sdddraft_output_filename)

    print("Start Staging.")
    arcpy.server.StageService(sdddraft_output_filename, sd_output_filename)

    print("Start uploading.")
    arcpy.server.UploadServiceDefinition(sd_output_filename, server_type)


def upload_pro():
    # Sign in to portal
    arcpy.SignInToPortal("https://www.arcgis.com", vars.ago_username, vars.ago_password)

    # Set output file names
    outdir = vars.aprx_path
    service_name = "Jasek_razno"
    sddraft_filename = service_name + ".sddraft"
    sddraft_output_filename = os.path.join(outdir, sddraft_filename)
    sd_filename = service_name + ".sd"
    sd_output_filename = os.path.join(outdir, sd_filename)

    # Reference map to publish
    aprx = arcpy.mp.ArcGISProject(os.path.join(vars.aprx_path, vars.aktualna_karta))
    m = aprx.listMaps("Kataster D96")[0]
    print("map", m)

    # Create FeatureSharingDraft and set metadata, portal folder, export data properties, and CIM symbols
    server_type = "HOSTING_SERVER"
    sddraft = m.getWebLayerSharingDraft(server_type, "FEATURE", service_name)
    sddraft.credits = "These are credits"
    sddraft.description = "This is description"
    sddraft.summary = "This is summary"
    sddraft.tags = "tag1, tag2"
    sddraft.useLimitations = "These are use limitations"
    sddraft.portalFolder = "_Dev"
    sddraft.allowExporting = True
    sddraft.useCIMSymbols = True

    # Create Service Definition Draft file
    sddraft.exportToSDDraft(sddraft_output_filename)

    # # Read the .sddraft file
    # docs = DOM.parse(sddraft_output_filename)
    # key_list = docs.getElementsByTagName("Key")
    # value_list = docs.getElementsByTagName("Value")
    #
    # # Change following to "true" to share
    # SharetoOrganization = "false"
    # SharetoEveryone = "true"
    # SharetoGroup = "false"
    # # If SharetoGroup is set to "true", uncomment line below and provide group IDs
    # GroupID = ""  # GroupID = "f07fab920d71339cb7b1291e3059b7a8, e0fb8fff410b1d7bae1992700567f54a"
    #
    # # Each key has a corresponding value. In all the cases, value of key_list[i] is value_list[i].
    # for i in range(key_list.length):
    #     if key_list[i].firstChild.nodeValue == "PackageUnderMyOrg":
    #         value_list[i].firstChild.nodeValue = SharetoOrganization
    #     if key_list[i].firstChild.nodeValue == "PackageIsPublic":
    #         value_list[i].firstChild.nodeValue = SharetoEveryone
    #     if key_list[i].firstChild.nodeValue == "PackageShareGroups":
    #         value_list[i].firstChild.nodeValue = SharetoGroup
    #     if (
    #         SharetoGroup == "true"
    #         and key_list[i].firstChild.nodeValue == "PackageGroupIDs"
    #     ):
    #         value_list[i].firstChild.nodeValue = GroupID
    #
    # # Write to the .sddraft file
    # f = open(sddraft_output_filename, "w")
    # docs.writexml(f)
    # f.close()
    #
    # # Stage Service
    # print("Start Staging")
    # arcpy.server.StageService(sddraft_output_filename, sd_output_filename)
    #
    # # Share to portal
    # print("Start Uploading")
    # arcpy.server.UploadServiceDefinition(sd_output_filename, server_type)
    #
    print("Finish Publishing")


# https://pro.arcgis.com/en/pro-app/latest/arcpy/sharing/featuresharingdraft-class.htm


def upload_layer():
    # Local vars
    map_name = vars.map_name
    # group_layer_name = "Dev"
    prj_path = os.path.join(vars.aprx_path, vars.aktualna_karta)
    # source_layer_1 = "Kanalizacijska linija"
    # source_layer_2 = "Kanalizacijski jašek"
    print("Project", prj_path)

    # Set portal login
    portal = vars.ago_url
    ago_user = vars.ago_username
    ago_pass = vars.ago_password
    # web_folder = "_Dev"

    # Sign in to AGOL
    print("Connecting to {}".format(portal))
    gis = arcpy.SignInToPortal(portal, ago_user, ago_pass)
    print("Connected.")

    # Prepare paths
    outdir = vars.aprx_path
    print("outdir", outdir)

    service_name = "Jasek_razno"  # Layer 1

    sddraft_filename = service_name + ".sddraft"
    print("sddraft_filename", sddraft_filename)

    sdddraft_output_filename = os.path.join(outdir, sddraft_filename)

    sd_filename = service_name + ".sd"
    sd_output_filename = os.path.join(outdir, sd_filename)

    aprx = arcpy.mp.ArcGISProject(prj_path)
    m = aprx.listMaps(map_name)[0]

    server_type = "HOSTING_SERVER"
    sddraft = m.getWebLayerSharingDraft(server_type, "FEATURE", service_name)
    sddraft.overwriteExistingService = True

    sddraft.exportToSDDraft(sdddraft_output_filename)

    print("Start Staging.")
    arcpy.server.StageService(sdddraft_output_filename, sd_output_filename)

    print("Start uploading.")
    arcpy.server.UploadServiceDefinition(sd_output_filename, server_type)


upload_pro()


# map_obj = aprx.listMaps(map_name)[0]
# group_layer = [
#     layer
#     for layer in map_obj.listLayers()
#     if layer.isGroupLayer and layer.name == group_layer_name
# ][0]
#
# source_layer_1_obj = [
#     layer for layer in group_layer.listLayers() if layer.name == source_layer_1
# ][0]
# source_layer_2_obj = [
#     layer for layer in group_layer.listLayers() if layer.name == source_layer_2
# ][0]
#
#
# def overwrite_web_layer(source_layer):
#     # create sharing draft
#     sharing_draft = map_obj.getWebLayerSharingDraft(
#         "HOSTING_SERVER", "FEATURE", source_layer.name
#     )
#     sharing_draft.overwriteExistingService = True
#     sharing_draft.portalFolder = web_folder
#
#     # stage and upload service definitions
#     print("Staging")
#     sd_filename = f"{source_layer.name}.sd"
#     sd_output = arcpy.server.StageService(sharing_draft, sd_filename)
#     arcpy.server.UploadServiceDefinition(sd_output, portal)
#
#     print(f"Sucsessfully overwritten {source_layer.name}")
#
#
# print("Overwrite 1")
# overwrite_web_layer(source_layer_1_obj)
# print("Overwrite 2")
# overwrite_web_layer(source_layer_2_obj)

print("Končano...")
