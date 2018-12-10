from sklearn.neighbors import KNeighborsRegressor
from xml.etree import ElementTree
from sklearn.model_selection import GridSearchCV
import dateutil.parser
import datetime
from xml.dom.minidom import Document
import numpy

data_path = "webpage/src/data.xml"
neighbors_trial = list(range(1, 101))
lat_start = 35.995410
lat_end = 36.007632
lon_start = -78.948664
lon_end = -78.929848
lat_step = 0.00005
lon_step = 0.00005
max_delta = 0.0025  # only consider neighbors
output_path = "webpage/src/predictions.xml"

raw_data = []
locations = []
signals = []
knn = KNeighborsRegressor(weights='distance')


def parse():
    '''
    Generates list of locations, signal strengths and times from data file,
    and store them in raw_data
    '''
    root = ElementTree.parse(data_path).getroot()
    for location in root:
        lat = float(location.find('latitude').text)
        lon = float(location.find('longitude').text)
        signal = float(location.find('signal').text)
        time = dateutil.parser.parse(location.find('time').text)
        raw_data.append((lat, lon, signal, time))

def filter():
    '''
    Filter the raw data according to the following rules:
    - For each location (same lat/lon), for data within 5 minutes of each
      other, take the highest signal;
    - For data not within 5 minutes of each other, take the average signal.
    Store the results in locations and signals.
    '''
    data_for_location = {}
    for lat, lon, signal, time in raw_data:
        if (lat, lon) not in data_for_location:
            data_for_location[(lat, lon)] = []
        data_for_location[(lat, lon)].append((time, signal))

    for location, signal_list in data_for_location.items():
        if not signal_list:
            continue

        signal_list.sort(key=lambda tup: tup[0])
        distinct_signals = []
        prev_time = None
        prev_best_signal = float("-inf")
        for time, signal in signal_list:
            if (prev_time == None) or (
                    time - prev_time <= datetime.timedelta(0, 5, 0)):
                if prev_time == None:
                    prev_time = time
                prev_best_signal = max(prev_best_signal, signal)
            else:
                distinct_signals.append(prev_best_signal)
                prev_time = time
                prev_best_signal = signal
        distinct_signals.append(prev_best_signal)

        locations.append(list(location))
        signals.append(sum(distinct_signals) / len(distinct_signals))


def train():
    '''
    Train the K-NN regressor.
    '''
    global knn
    knn = KNeighborsRegressor(weights='distance')  # TODO: Use Great Circle Distance
    parameters = {'n_neighbors': neighbors_trial}
    cv = GridSearchCV(knn, parameters, cv=10).fit(locations, signals)
    best_params = cv.best_params_
    knn = KNeighborsRegressor(n_neighbors=best_params.get('n_neighbors', 1),
                              weights='distance').fit(locations, signals)


def predict(coords):
    '''
    Predict the signal strength for some input points.

    Neighbors with a distance greater than max_delta are discarded.
    If no valid neighbors exist, return -1.
    :param coords: list of [lat, lon] arrays
    :return: list of corresponding signal strengths (-1 for ignored points)
    '''
    distances, neighbors = knn.kneighbors(coords, return_distance=True)
    predictions = []
    # Note: query point is not its own neighbor

    for i in range(len(coords)):
        sum_signals = 0
        sum_weights = 0
        for j in range(len(distances[i])):
            if distances[i][j] > max_delta:
                continue
            if distances[i][j] == 0:  # should not happen, but just in case, i is a data point itself
                sum_signals = signals[neighbors[i][j]]
                sum_weights = 1
                break
            weight = 1 / distances[i][j]
            sum_signals += signals[neighbors[i][j]] * weight
            sum_weights += weight
        if sum_weights == 0:
            predictions.append(-1)
        else:
            predictions.append(sum_signals / sum_weights)

    return predictions


def output():
    '''
    Write output for (lat,lon) grids with boundaries given in parameters.
    '''
    lats = numpy.arange(lat_start, lat_end, lat_step)
    lons = numpy.arange(lon_start, lon_end, lon_step)
    coords = [[lat, lon] for lat in lats for lon in lons]
    preds = predict(coords)

    doc = Document()
    grid = doc.createElement("grid")
    doc.appendChild(grid)

    for i in range(len(coords)):
        if (preds[i] == -1):
            continue
        location = doc.createElement("location")
        grid.appendChild(location)

        latitude = doc.createElement("latitude")
        location.appendChild(latitude)
        latitude.appendChild(doc.createTextNode(str(coords[i][0])))

        longitude = doc.createElement("longitude")
        location.appendChild(longitude)
        longitude.appendChild(doc.createTextNode(str(coords[i][1])))

        signal = doc.createElement("signal")
        location.appendChild(signal)
        signal.appendChild(doc.createTextNode(str(preds[i])))

    f = open(output_path, 'w+')
    f.write(doc.toprettyxml(indent="  "))
    f.close()


if __name__ == '__main__':
    parse()
    filter()
    train()
    output()
