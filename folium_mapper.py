# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:02:48 2021

@author: Jake.Pridotkas
"""
import folium

class Folium_Mapper:
    def __init__(self, suppliers, distributions, consumers, all_cities, model):
        self.suppliers = suppliers
        self.distributions = distributions
        self.consumers = consumers
        self.all_cities = all_cities
        self.model = model
        self.mapObject = None

# use the Map function from folium to generate a map
# create map object with folium.Map()
    def build_map(self):
        mapObject = folium.Map(location = [29,-95],
                              zoom_start = 3)
        # create markers with .Marker
        for city in self.suppliers.city:
            folium.Marker(location= [self.all_cities[self.all_cities['city'] == city].lat.iloc[0], self.all_cities[self.all_cities['city'] == city].long.iloc[0]],
                                     popup = "This is a marker!",
                                     icon=folium.Icon(color="blue",icon="cloud")
                                     ).add_to(mapObject)
        for city in self.distributions.city:
            folium.Marker(location= [self.all_cities[self.all_cities['city'] == city].lat.iloc[0], self.all_cities[self.all_cities['city'] == city].long.iloc[0]],
                                     popup = "This is a marker!",
                                     icon=folium.Icon(color="red",icon="cloud")
                                     ).add_to(mapObject)
        
        for city in self.consumers.city:
            folium.Marker(location= [self.all_cities[self.all_cities['city'] == city].lat.iloc[0], self.all_cities[self.all_cities['city'] == city].long.iloc[0]],
                                     popup = "This is a marker!",
                                     icon=folium.Icon(color="green",icon="cloud")
                                     ).add_to(mapObject)
        # add marker to map
        def build_line(city1, city2):
            coords_1 = [self.all_cities[self.all_cities['city'] == city1].lat.iloc[0], self.all_cities[self.all_cities['city'] == city1].long.iloc[0]]
            coords_2 = [self.all_cities[self.all_cities['city'] == city2].lat.iloc[0], self.all_cities[self.all_cities['city'] == city2].long.iloc[0]]
            folium.PolyLine(locations=[coords_1, coords_2],weight=3).add_to(mapObject)
            return
        
        # gross way to do this, but works for now
        def get_routes(model):
            routes = []
            for v in model.variables():
                if v.varValue > 0:
                    cities = v.name.replace("_", " ").split("'")[1::2]
                    routes = routes + [cities]
            return routes
        
        # Create the map and add the line
        routes = get_routes(self.model)
        
        for route in routes:
            build_line(route[0], route[1])
            
        self.mapObject = mapObject

    def save_map(self, filename):
        self.mapObject.save(filename)