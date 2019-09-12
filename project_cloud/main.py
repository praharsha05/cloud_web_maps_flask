from flask import Flask, render_template
import folium
import pandas as pd

app = Flask(__name__)


def color_producer(rating):
    r=rating
    if r > 9.2:
        return "orange"
    elif r > 8.8:
        return "cyan"
    elif r > 8.5:
        return "green"
    elif r > 8:
        return "brown"
    else:
        return "red"


dataW = pd.read_csv("Waterfalls.txt")
lat = list(dataW["Lat"])
lon = list(dataW["Lon"])
name = list(dataW["Name"])
rat = list(dataW["Rating"])

dataT = pd.read_csv("temples.txt")
tname = list(dataT["Name"])
tlon = list(dataT["Lon"])
tlat = list(dataT["Lat"])

# search query to redirect it to search in web
htmlW = """
Waterfall Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
"""

htmlT = """
Temple Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
"""

#to add map objects like points in a webmap
map = folium.Map(location = [22.378939, 82.612773],zoom_start=5,tiles = "Mapbox Bright")

fgW = folium.FeatureGroup(name="Waterfalls")

for lt,ln,nm,rt in zip(lat, lon, name, rat):
    iframe = folium.IFrame(html=htmlW % (nm, nm), width=150, height=80)
    fgW.add_child(folium.CircleMarker(location=[lt,ln] ,popup=folium.Popup(iframe),tooltip = nm ,radius = 6,
    fill_color = color_producer(rt), color = "grey" ,fill = True ,fill_opacity=0.7,))

fgP = folium.FeatureGroup(name="Population_Density")

world_pop = open("world.json",'r',encoding='utf-8-sig')
world = world_pop.read()
fgP.add_child(folium.GeoJson(world,
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

fgT = folium.FeatureGroup(name="Temples")

for lt,ln,nm in zip(tlat, tlon, tname):
    iframe = folium.IFrame(html=htmlT % (nm, nm), width=150, height=80)
    fgT.add_child(folium.Marker(location=[lt,ln] ,popup=folium.Popup(iframe),icon=folium.Icon(color="green")))

map.add_child(fgP)
map.add_child(fgW)
map.add_child(fgT)

map.add_child(folium.LayerControl())

map.save("templates/Map.html")

@app.route('/')
def home():
    return render_template("Map.html")

if __name__=="__main__":
    app.run(debug=True)
