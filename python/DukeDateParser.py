from xml.dom.minidom import Document
import random


def parse_csv(fileName):
    datas = []
    f = open(fileName, 'r')
    line = f.readline() # Ignore the first line
    while(line):
        # Read every other line starting from the second line.
        line = f.readline()
        if (line != ''):
            myList = line.split('","')
            wifiName = myList[0][1:]
            wifiSignal = random.random() * 5
            #wifiSignal = myList[3]
            wifiTime = myList[-3]
            wifiLongitude = myList[-2]
            wifiLatitude = myList[-1][:-2]
            if (wifiLongitude != '' and wifiLatitude != '' and
            (wifiName == 'DukeOpen' or wifiName == 'Dukeblue'
            or wifiName == 'DukeVisitor' or wifiName == 'eduroam')):
                data = []
                data.append(wifiName)
                data.append(wifiSignal)
                data.append(wifiTime)
                data.append(wifiLongitude)
                data.append(wifiLatitude)
                datas.append(data)
        line = f.readline()
    f.close()
    return datas

def write_into_xml(datas):

    doc = Document()
    hotspots = doc.createElement("hotspots")
    doc.appendChild(hotspots)

    for data in datas:
        location = doc.createElement("location")
        hotspots.appendChild(location)

        name = doc.createElement("name")
        location.appendChild(name)
        name.appendChild(doc.createTextNode(data[0]))

        signal = doc.createElement("signal")
        location.appendChild(signal)
        signal.appendChild(doc.createTextNode(str(data[1])))

        time = doc.createElement("time")
        location.appendChild(time)
        time.appendChild(doc.createTextNode(data[2]))

        latitude = doc.createElement("latitude")
        location.appendChild(latitude)
        latitude.appendChild(doc.createTextNode(data[3]))

        longtitude = doc.createElement("longtitude")
        location.appendChild(longtitude)
        longtitude.appendChild(doc.createTextNode(data[4]))

    f = open("webpage/src/20181118_135522.xml", "w")
    f.write(doc.toprettyxml(indent="  "))
    f.close()

if __name__ == '__main__':
    datas = parse_csv("data/csv/20181118_135522.csv")
    write_into_xml(datas)
