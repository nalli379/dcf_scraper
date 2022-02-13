from flask import Flask
import folium
import csv
from folium.plugins import MarkerCluster

app = Flask(__name__)


@app.route("/")
def home():
    return "Recycle Rewards System"


@app.route('/map')
def index():
    map = folium.Map(location=[54.560886, -2.2125118], tiles='OpenStreetMap', zoom_start=4)
    markerCluster = MarkerCluster().add_to(map)
    with open('dcf_sites.csv', 'r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            lat = row['latitude']
            long = row['longitude']
            name = row['place_name']
            folium.Marker(location=[lat, long], popup=name).add_to(markerCluster)

    return map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True, port=5001)