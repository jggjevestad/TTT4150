from lib.navlib import dm2deg

# Parse data from NMEA RMC to KML
def parse_nmea2kml(infile, outfile):

    # Open files
    infile = open(infile, 'r')
    outfile = open(outfile, 'w')

    # Write KML header
    outfile.write("""<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document><name>CalTopo Export</name><description>Export from CalTopo</description>
    <Folder><open>1</open><name>Lines and Polygons</name>
    <Placemark><Style><LineStyle><color>FF0000FF</color><width>2.0</width></LineStyle><PolyStyle><fill>1</fill><outline>1</outline><width>2.0</width><color>000000FF</color></PolyStyle></Style><name>3 Fingered Jack</name><description/>
    <LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>
    <coordinates>\n""")

    # Read NMEA file line by line
    for line in infile:
        # Split line into elements
        data = line.split(",")

        # Get position from RMC message
        if data[0] == "$GPRMC":
            # Get position only if GPS status i valid (code: A)
            if data[2] == "A":
                lat = float(data[3])
                if data[4] == "S":
                    lat = -lat
                lon = float(data[5])
                if data[6] == "W":
                    lon = -lon

                # Convert decimal minutes to decimal degrees
                lat = dm2deg([int(lat/100), (lat/100 - int(lat/100))*100])
                lon = dm2deg([int(lon/100), (lon/100 - int(lon/100))*100])

                # Generate KML file
                outfile.write("{:.10f},{:.10f},0\n".format(lon, lat))

    # Write KML footer
    outfile.write("""</coordinates></LineString></Placemark></Folder></Document></kml>\n""")

    # Close files
    infile.close()
    outfile.close()


if __name__ == "__main__":
    parse_nmea2kml('data/gnss.nmea',
                   'data/gnss.kml')

print('Finished...')
