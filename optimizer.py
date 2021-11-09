# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:00:31 2021

@author: Jake.Pridotkas
"""

import pandas as pd
from pulp import *
import geopy.distance
from geopy.geocoders import Nominatim

# return distance in miles between two cities from our initial dataframe
# kind of messy way to do this


class Optimizer:
    def __init__(self, suppliers, distributions, consumers, all_cities):
        self.suppliers = suppliers
        self.distributions = distributions
        self.consumers = consumers
        self.all_cities = all_cities
        self.model = None
        self.total_cost = None
        self.formatted_total_cost = None
        self.model_status = None

    def get_distance(self, city1, city2):
        coords_1 = (self.all_cities[self.all_cities['city'] == city1].lat.iloc[0], self.all_cities[self.all_cities['city'] == city1].long.iloc[0])
        coords_2 = (self.all_cities[self.all_cities['city'] == city2].lat.iloc[0], self.all_cities[self.all_cities['city'] == city2].long.iloc[0])
        return geopy.distance.distance(coords_1, coords_2).miles
    
    def build_model(self):
        # Initialize model
        model = LpProblem("Supply_Chain_Optimization", LpMinimize)
        
        # Create Decision Variables
        x = LpVariable.dicts("supplier_", [(i,j) for i in self.suppliers['city'] for j in self.distributions['city']],
                             lowBound=0, upBound=None)
        
        y = LpVariable.dicts("distribution_", 
                             [(i,j) for i in self.distributions['city'] for j in self.consumers['city']], 
                            lowBound=0, upBound=None)
        
        # Define Objective Function
        COST_PER_MILE = 1 #Arbitrary mileage cost
        model += (lpSum([self.get_distance(i,j) * x[(i,j)] * COST_PER_MILE for i in self.suppliers['city'] for j in self.distributions['city']]) + \
                  lpSum([self.get_distance(i,j) * y[(i,j)] * COST_PER_MILE for i in self.distributions['city'] for j in self.consumers['city']]))
            
        # Add Constraints
        
        # Must meet demand at every consumer location
        for consumer_city in self.consumers['city']:
            model += lpSum([y[(i, consumer_city)] for i in self.distributions['city']]) >= \
                     self.consumers[self.consumers['city']==consumer_city].demand.iloc[0]
        
        # Must recieve enough supply to distribute
        for distribution_center in self.distributions['city']:
            model += lpSum([x[(i, distribution_center)] for i in self.suppliers['city']]) >= \
                     lpSum([y[(distribution_center, j)] for j in self.consumers['city']])
            
        # Do suppliers or distributers have limits?
        self.model = model
    
    def solve_model(self):
        # Solve Model
        self.model.solve()
        self.formatted_total_cost = "Total Cost = ${:,}".format(int(value(self.model.objective)))
        self.total_cost = int(value(self.model.objective))
        self.model_status = "Status: {}".format(LpStatus[self.model.status])


#return data frame with coords given a list of cities
def get_coords(city_list):
    df = pd.DataFrame({'city': [],'lat': [],'long': []})
    geolocator = Nominatim(user_agent="supply_app")
    for city in city_list:
        location = geolocator.geocode(city)
        df2 = {'city': city, 'lat': location.latitude, 'long': location.longitude}
        df = df.append(df2, ignore_index = True)
    return df

#INITIAL_TOTAL_COST = int(value(model.objective))


