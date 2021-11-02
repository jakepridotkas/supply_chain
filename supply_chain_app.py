# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import streamlit.components.v1 as components

from optimizer import *
from folium_mapper import *

import os.path
import sys
import pandas as pd
import folium

st.write("""
# Supply Chain Vizualization
Playing around with linear programming of supply chains.  Add new distribuition center below to see effect on network.
""")

#random suppliers, distribution centers, and customers with demand

suppliers = get_coords(['Des Moines', 'Iowa City', 'Cleveland', 'San Antonio'])
distributions = get_coords(['Houston'])
consumers = get_coords(['Destin', 'LA', 'Boston', 'Minneapolis', 'San Francisco', 'Miami', 'Charlotte', 'Boise'])

# give consumers some number of demand
consumers['demand'] = [10, 15, 5, 8, 10, 50, 20, 10]

all_cities = pd.concat([suppliers, distributions, consumers])

# If map is not already drawn then generate it
#if not os.path.isfile('index.html'):   
optimizer = Optimizer(suppliers, distributions, consumers, all_cities)
optimizer.build_model()
optimizer.solve_model()

#if solved
mapper = Folium_Mapper(suppliers, distributions, consumers, all_cities, optimizer.model)
mapper.build_map()
mapper.save_map('index.html')

st.write(optimizer.model_status)
st.write(optimizer.formatted_total_cost)
st.write('Calculated based on ____')
#else:
#    print('skipping optimization, file still here')

# Load HTML file in HTML component for display on Streamlit page    
HtmlFile = open('index.html', 'r', encoding='utf-8')
components.html(HtmlFile.read(), height=435)
st.markdown(
    """
    <br>
    <h6>Blue = Suppliers | Red = Distributers | Green = Customers</h6>
    <h6></h6>
    """, unsafe_allow_html=True
    )

# Declare a form and call methods directly on the returned object
form = st.form(key='my_form')
new_city = form.text_input("Enter new distribution location: ", "St Louis")
submit = form.form_submit_button(label='Submit')

if submit:  
    #add new city to distribution center
    new_distributions = [new_city]
    try:
        df = get_coords(new_distributions)
    except:
        st.write("Hmmm I don't think that's a real city, try again!")
        sys.exit(1) 
    distributions = distributions.append(df, ignore_index=True)
    all_cities = pd.concat([suppliers, distributions, consumers])
    
    #rebuild and solve model
    new_optimizer = Optimizer(suppliers, distributions, consumers, all_cities)
    new_optimizer.build_model()
    new_optimizer.solve_model()
    
    #if solved
    mapper = Folium_Mapper(suppliers, distributions, consumers, all_cities, new_optimizer.model)
    mapper.build_map()
    mapper.save_map('new_index.html')
    
    st.write(new_optimizer.model_status)
    st.write(new_optimizer.formatted_total_cost)
    st.write('Calculated based on ____')
    st.write('Cost difference of: ${:,}'.format(int(optimizer.total_cost - new_optimizer.total_cost)))
        
    HtmlFile = open('new_index.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=435)
    st.markdown(
    """
    <br>
    <h6>Blue = Suppliers | Red = Distributers | Green = Customers</h6>
    <h6></h6>
    """, unsafe_allow_html=True
    )
