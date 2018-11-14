from xml.dom.minidom import Document


def parse_csv():
    """
    Extract locations of hotspots, in terms of latitude and longtitude, from
    the file NYC_Wi-Fi_HotSpot_Locations.csv and store them in a list of tuples
    """

    locations = []

    f = open('data/NYC_Wi-Fi_HotSpot_Locations.csv', 'r')
    line = f.readline() # Ignore the first line
    line = f.readline()
    while(line):
        # Read every other line starting from the thrid line.
        line = f.readline()
        (latitude,longtitude) = line[1:-3].split(", ")
        locations.append((latitude,longtitude))
        line = f.readline()
    f.close()

    return locations

def write_into_xml(locations):
    """
    Write the latitudes and longtitudes to the file NYCDatabase.xml in the form
    of:
    <hotspots>
        <location>
            <latitude> latitude1 </latitude>
            <longtitude> longtitude1 </longtitude>
        </location>
        <location>
            ...
        </location>
        ...
    <hotspots>
    """
    doc = Document()
    hotspots = doc.createElement("hotspots")
    doc.appendChild(hotspots)

    for each in locations:
        location = doc.createElement("location")
        hotspots.appendChild(location)

        latitude = doc.createElement("latitude")
        location.appendChild(latitude)
        latitude.appendChild(doc.createTextNode(each[0]))
        longtitude = doc.createElement("longtitude")
        location.appendChild(longtitude)
        longtitude.appendChild(doc.createTextNode(each[1]))

    f = open("webpage/src/NYCDatabase.xml", "w")
    f.write(doc.toprettyxml(indent="  "))
    f.close()

if __name__ == '__main__':
    locations = parse_csv()
    write_into_xml(locations)
