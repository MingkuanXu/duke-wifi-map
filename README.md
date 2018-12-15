
# Duke FiMap

An application to visualize the Wi-Fi signal strength within Duke campus.

## Overview

As a student at Duke, the use of Wi-Fi is an important part of our daily student life. Sometimes we may want to print course materials, send messages, or watch videos online, but find the DukeBlue is however not in range, or the signal is really weak. This can be an extremely frustrating experience. The motivation of our project is therefore to design an web page to visualize the Wi-Fi signal strength within Duke campus. 

Creating such a map can benefit the Duke community in many different ways. With the knowledge of which places have the strongest Wi-Fi signal, students can make wiser choices on where to go for activities that require Internet connection, such as studying or watching movies. Furthermore, if a mobile application is published, it can have even more functionalities such as automatically switching between Wi-Fi and mobile data while walking, based on the strength of different Wi-Fi networks as predicted from the map. The app can also suggest the most optimal directions when travelling between different places to make sure the network connection is strong enough along the way, switching between networks if necessary. In addition, gathering and computing such data may help the OIT make better decisions on optimizing and installing new Wi-Fi facilities for improvements in areas where Wi-Fi connections are poor. 

## Timeline

Start Date: 9/11/2018

Finish Date: 12/13/2018

## Contributors & Roles

* Charles Lyu : Data Collection & Machine Learning Algorithm Development
* Mingkuan Xu : Front-End Desgin & Data Visualization
* Yunhao Qing: CSV Parser & Database Design.
* Yikai Wu : Data Interpretation & Front-End/Back-End Interaction.

## Data Collection

We use an existing Android application, Wi-Fi Collector, that can measure the signal strengths of all the Wi-Fi in range in a given location. We carried a phone with this app and walked around almost every corner of this campus, including Duke Gardens, East Campus, Central Campus, West Campus, Wilson Gym, and Duke Hospital, for two weeks, resulting in 13,513 data points. Having developed the machine learning algorithm later, we further collected a lot of data in places where the predictions seem strange, to improve the accuracy and coverage of empirical data. Additionally, we revisited some places after our first trial of data analysis and visualization, since the app and our initial data collection methods had some flaws that we did not realize until then.

## Data Parsing

The data collected using Wi-Fi Collector are stored in several .csv files, with a lot of useless attributes. In order to conveniently deliver the data to the front-end, we decided to use XML format for our two databases (reason explained in the data visualization section). Therefore, a data parser is needed to extract useful information from the .csv files and put them into an .xml file, which we implemented in Python by writing two methods called parse_csv and write_into_xml, respectively. 

## Data Manipulation

The data in the input database cannot be directly transformed to the final map, because there will be multiple measurements at the same place and also some places may not have any data recorded. Therefore, we need an additional data manipulation process to analyze these raw data and transform them to a new database system, in which the data stored should be a list of tuples in the form of (location, strength), so that they can be directly used to display the map. We called this new database the output database.

Essentially, there are three issues we should focus on. Firstly, the application measured the Wi-Fi strength in dBm, which usually ranges from -120 to -30. We need to come up with a reasonable formula that can adjust this negative value to a simple positive number, in order to more easily implement the data visualization process. Secondly, we often have multiple measurements at the same location across different times and Wi-Fi networks, so we need to filter the data to deal with duplicate measurements. Thirdly, notice that the measured locations will not cover the whole map, so a Machine Learning algorithm needs to be designed to predict the Wi-Fi strength in some regions to ensure the final map is continuous.

### dBm Strength Adjustment

Our signal strength is calculated based on the formula shown below. The empirical data for Wi-Fi signals is collected as dBm values, which is a universal and accurate way to measure the signal strength at the given locations. However, those values are logarithm-based and do not reflect well on a map. Thus, we came up with a formula to transform the dBm values into a float value from 0 (weakest) to 7 (strongest), which is more intuitive for readers (similar to how Wi-Fi signals are presented on phones) and easier to work with for visualization. 

### Data Filtering

To ensure the best accuracy of data, we often measure the Wi-Fi signal strengths at the exact same locations over time. Even at the same time and location, the data usually have several different Wi-Fi networks, including Duke and non-Duke networks. Therefore, we wrote a function that filters the data and ensures we are left with one single signal strength data for each location as much as possible, by:
* Keeping one data tuple for each distinct location, identified by their latitudes and longitudes. Locations with slightly different coordinates are treated as different ones to maximize accuracy of data.
* For data at the same location measured within 5 minutes of each other, pick the one with the strongest signal strength. This is because the raw data might contain the same network (e.g. Dukeblue) from different routers with varying signal strengths available at the same location, when in reality the device will automatically pick the best one. Also, in case of several different Duke Wi-Fi networks all available at the same location, a rational user will connect to the best network as well.
* For data at the same location not within 5 minutes of each other (i.e. all data left after the previous step), the average signal will be taken across all times. This is to minimize random errors and achieve the best accuracy.

After data filtering, the number of available data points was brought down to 1,885.

### K-Nearest-Neighbor Strength Prediction

After collecting empirical Wi-Fi signals at visited locations, we use the k-Nearest Neighbor algorithm, a commonly used Machine Learning algorithm, to predict the Wi-Fi signal strength at any location, including those we have not visited. 
In summary, the k-Nearest Neighbor algorithm predicts the signal strength at each point by examining its k nearest neighbors. While k-NN is not the best algorithm available (since Wi-Fi signals typically decay over distance), we see it as most suitable for the scope of our course project and most feasible to implement.

The number of neighbors to be examined, k, is determined with cross validation. All integers from 1 to 100 were tested, and 44 is eventually chosen as it results in the lowest validation risk. While such a high number used might be surprising, we suspect it works best for areas with a higher density of measured points.

## Data Visualization

We have applied a Google Map API key, which not only can be used to display Google Map on our webpage, but also allow us to use Google Weighted Heatmap function. Google Weighted Heatmap API can directly transform a set of weighted locations to a colorful map. Using this function requires an input list of tuples in a form of (latitude, longitude, weight), which is exactly how our output data look like. Therefore, this API helps us to easily visualize the Wi-Fi strengths in Duke campus.

To extract information from the back-end database and deliver them to the Google Heatmap function, we have written two Javascript functions named readDatabase and getPoints, respectively. The function readDaabase is used to handle the HTTP Request of XML files for different browsers and extract all the “location” nodes from the xml document by the Javascript function “getElementsByTagName”, which works similar to XQuery to identify nodes with a particular tag name in an XML file. Thanks to this function, our data can be conveniently delivered from back-end to front-end. This is also an important reason why we choose XML as the type of our databases.

## Result

### NYC Hotspots Map
![](https://github.com/MingkuanXu/duke-wifi-map/blob/master/resources/nyc-hotspots-map.jpeg)

### Duke Wi-Fi Map
![](https://github.com/MingkuanXu/duke-wifi-map/blob/master/resources/duke-wifi-map.jpeg)

## Future Prospect

In the future, we plan to extend the web application into mobile applications so students and staff can use the app to get information on the WiFi and in the meanwhile collecting new data for our database. The database will be updated so only the data within 7 days will be used for calculation and estimation for better accuracy. We also want to try on more ways of visualising the data. So, in the future, the users can define how they want to view the data. They can see results in a specific area, or within a specific time. We believe, with better data collection and visualization, this application will be useful to many stakeholders.

## Resources Used

* Wi-Fi Collector. Android APP. 

* Kaggle NYC Hotspots Dataset (https://www.kaggle.com/new-york-city/nyc-public-wifi)

* Google Heatmap API (https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap)

* Background Picture (https://image-store.slidesharecdn.com/14276b0c-436a-4fa3-adbf-42fbd5c7c6a6-original.jpeg)

