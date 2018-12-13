from xml.dom.minidom import Document
import random
import os
import math

def dbm_to_measure(dbm):
    return max(0, 7 - 0.4383 * math.exp(-0.0278 * dbm))

names_list = ['DukeOpen', 'Dukeblue', 'DukeVisitor', 'eduroam']

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
            signalStrength = float(myList[3])
            wifiSignal = dbm_to_measure(signalStrength)
            wifiTime = myList[-3]
            wifiLongitude = myList[-2]
            wifiLatitude = myList[-1][:-2]
            if (wifiLongitude != '' and wifiLatitude != ''):
                if (wifiName in names_list):
                    data = [wifiName, wifiSignal, wifiTime, wifiLongitude, wifiLatitude]
                else:
                    data = [wifiName, 0, wifiTime, wifiLongitude, wifiLatitude]
                datas.append(data)
        line = f.readline()
    f.close()
    return datas

def write_into_xml(path, fileName):

    doc = Document()
    hotspots = doc.createElement("hotspots")
    doc.appendChild(hotspots)

    for file in os.listdir(path):
        datas = parse_csv(path + "/" + file)
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
            latitude.appendChild(doc.createTextNode(data[4]))

            longitude = doc.createElement("longitude")
            location.appendChild(longitude)
            longitude.appendChild(doc.createTextNode(data[3]))

    f = open(fileName, "w")
    f.write(doc.toprettyxml(indent="  "))
    f.close()

if __name__ == '__main__':
    write_into_xml("data/csv","webpage/src/data.xml")
