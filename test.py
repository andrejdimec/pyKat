import arcpy

# Define the list of coordinates (latitude, longitude) in decimal degrees
coordinates = [
    (46.6806, 15.9507),
    # Add more coordinates as needed
]


def convert_to_slovenia_grid(lat, lon):
    """
    Convert a single (latitude, longitude) coordinate from decimal degrees to meters
    in the Slovenia National Grid 1996 coordinate system (EPSG:3794).

    Args:
        lat (float): Latitude in decimal degrees.
        lon (float): Longitude in decimal degrees.

    Returns:
        tuple: (X, Y) coordinates in meters.
    """
    input_sr = arcpy.SpatialReference(4326)  # WGS 1984
    output_sr = arcpy.SpatialReference(3794)  # Slovenia National Grid 1996

    point = arcpy.Point(lon, lat)
    point_geom = arcpy.PointGeometry(point, input_sr)
    projected_point_geom = point_geom.projectAs(output_sr)

    x_meters = projected_point_geom.centroid.X
    y_meters = projected_point_geom.centroid.Y

    return x_meters, y_meters


# Example usage
latitude = 46.6806
longitude = 15.9507

x, y = convert_to_slovenia_grid(latitude, longitude)
print(f"Projected coordinates: X = {x}, Y = {y}")
