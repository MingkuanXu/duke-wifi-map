from xml.dom.minidom import Document
import random

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
            #wifiSignal = random.random() * 5
            #wifiSignal = myList[3]
            signalStrength = float(myList[3])
            wifiSignal = max(0, 7 - 0.4383 * math.exp(-0.0278 * signalStrength))
            wifiTime = myList[-3]
            wifiLongitude = myList[-2]
            wifiLatitude = myList[-1][:-2]
            if (wifiLongitude != '' and wifiLatitude != '' and wifiName in names_list):
                data = [wifiName, wifiSignal, wifiTime, wifiLongitude, wifiLatitude]
                datas.append(data)
        line = f.readline()
    f.close()
    return datas

def write_into_xml(datas, fileName):

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
        latitude.appendChild(doc.createTextNode(data[4]))

        longtitude = doc.createElement("longtitude")
        location.appendChild(longtitude)
        longtitude.appendChild(doc.createTextNode(data[3]))

    f = open(fileName, "w")
    f.write(doc.toprettyxml(indent="  "))
    f.close()

if __name__ == '__main__':
    dataTime = "20181118_135522"
    datas = parse_csv("data/csv/"+ dataTime +".csv")
    write_into_xml(datas,"webpage/src/" + dataTime+".xml")
