#!/usr/bin/env python
# coding: utf-8

# In[314]:


import threading #Imports the threading package from the python library
from urllib.request import urlopen#Imports the urllib package from the python library to open and read the urls
import sqlite3 #Imports the sqlite3 package from the python library to allow for performing SQL operations
import matplotlib.pyplot as plt #Imports the matplotlib package for graphing functionality
import numpy as np #Imports the numpy package for linear regression
from bs4 import BeautifulSoup #Imports the BeautifulSoup package from the bs4 library to parse the html for specific HTML elements
import re as deep_scraper #Imports the regex with the name "deep_scraper" to do a more specific search
import time

class Thread: #Class by the name "thread" is declared
    def __init__(self, file): #The constructor is initialized with the self variable to access the attributes of the object
        self.CO2 = [] #The file attribute is defined
        self.CH4 = [] #The encryption attribute is defined
        self.N2O = []
        self.CFC12 = []
        self.CFC11 = []
        self.minor15 = [] #Had to be named this way to avoid interpreter confusion
    def db_pre_config():
        conn = sqlite3.connect('global_radiative_forcing_annual_data.db') #Creates and connects to the db file
        db_cursor = conn.cursor() #The conn variable calls upon the cursor which is assigned to the db_cursor variable
        create_table = "CREATE TABLE radiative_forcing (Year VARCHARS(20), CO2 VARCHARS(20), CH4 VARCHARS(20), N2O VARCHARS(20), CFC12 VARCHARS(20), CFC11 VARCHARS(20), MINOR15 VARCHARS(20))"
        db_cursor.execute(create_table)
    def database_input(): #The years for all the six threads are to be extracted through this function
        html_file = urlopen('https://www.esrl.noaa.gov/gmd/aggi/aggi.html') #Opens the url through the html_file variable
        soup = BeautifulSoup(html_file, 'html.parser') #The soup variable has the variable and the parsing utility parameters parsed in
        td_elems = soup.select('td') #The Beautiful Soup utility finds all the td elements
        years = deep_scraper.findall("[1-2]+[0-9]{3}", str(td_elems)) #The deep_scraper finds all the years
        data = deep_scraper.findall("[0-3]+.[0-9]{3}", str(td_elems)) #Scrapes all the data
        years_list = []
        CO2_data = []
        CH4_data = []
        N2O_data = []
        CFC12_data = []
        CFC11_data = []
        minor15 = []
        for i in range(3, len(years)):
            years_list.append(years[i])
        for i in range(1, len(data), 8):
            CO2_data.append(data[i])
        for i in range (2, len(data), 8):
            CH4_data.append(data[i])
        for i in range (3, len(data), 8):
            N2O_data.append(data[i])
        for i in range (4, len(data), 8):
            CFC12_data.append(data[i])
        for i in range (5, len(data), 8):
            CFC11_data.append(data[i])
        for i in range (6, len(data), 8):
            minor15.append(data[i])
        #----------------------------------------------------------------------------------------
        conn = sqlite3.connect('global_radiative_forcing_annual_data.db') #Connects to the db file
        db_cursor = conn.cursor()
        for i in range(len(years_list)):
            insert_into_table = "INSERT INTO radiative_forcing (Year, CO2, CH4, N2O, CFC12, CFC11, MINOR15) VALUES (?, ?, ?, ?, ?, ?, ?)"
            values_to_insert = (years_list[i], CO2_data[i], CH4_data[i], N2O_data[i], CFC12_data[i], CFC11_data[i], minor15[i])
            db_cursor.execute(insert_into_table, values_to_insert) #The second parameter needs to be in the square brackets so it won't be misinterpreted as a group expression
            conn.commit()
        #db_cursor.execute("SELECT * from radiative_forcing")
        #records = db_cursor.fetchall() #Was used to test if the data was inserted
        #for row in records: #Prints by row
            #print(row[3])
    def thread_and_plot_setup(agent_row):
        conn = sqlite3.connect('global_radiative_forcing_annual_data.db') #Connects to the db file
        db_cursor = conn.cursor() #Cursor object
        db_cursor.execute("SELECT * from radiative_forcing")
        result = db_cursor.fetchall()
        year_list_for_graph = [] #List for years
        CO2_list_for_graph = [] #List for CO2
        CH4_list_for_graph = [] #List for CH4
        N2O_list_for_graph = [] #List for N2O
        CFC12_list_for_graph = [] #List for CFC12
        CFC11_list_for_graph = [] #List for CFC11
        minor15_list_for_graph = [] #List for 15-minor
        for row in result: #This one is to append the years for the x-axis
            year_list_for_graph.append(row[0])
        # ----- The if and else if conditions to be used for the thread at the end
        if agent_row == 1:
            for row in result:
                CO2_list_for_graph.append(row[agent_row])
            plt.figure(figsize=(30,30))
            plt.xlabel("Year", fontsize=20)
            plt.ylabel("CO2 data", fontsize=20)
            x = np.array(year_list_for_graph, dtype = np.float32)
            y = np.array(CO2_list_for_graph, dtype = np.float32)
            plt.scatter(x, y)
            (m,b) = np.polyfit(x, y, 1)
            new_y = m*x + b
            plt.plot(x, new_y)
            plt.show()
        elif agent_row == 2:
            for row in result:
                CH4_list_for_graph.append(row[agent_row])
            plt.figure(figsize=(30,30))
            plt.xlabel("Year", fontsize=20)
            plt.ylabel("CH4 data", fontsize=20)
            x = np.array(year_list_for_graph, dtype = np.float32)
            y = np.array(CH4_list_for_graph, dtype = np.float32)
            plt.scatter(x, y)
            (m,b) = np.polyfit(x, y, 1)
            new_y = m*x + b
            plt.plot(x, new_y)
            plt.show()
        elif agent_row == 3:
            for row in result:
                N2O_list_for_graph.append(row[agent_row])
            plt.figure(figsize=(30,30))
            plt.xlabel("Year", fontsize=20)
            plt.ylabel("N2O data", fontsize=20)
            x = np.array(year_list_for_graph, dtype = np.float32)
            y = np.array(N2O_list_for_graph, dtype = np.float32)
            plt.scatter(x, y)
            (m,b) = np.polyfit(x, y, 1)
            new_y = m*x + b
            plt.plot(x, new_y)
            plt.show()
        elif agent_row == 4:
            for row in result:
                CFC12_list_for_graph.append(row[agent_row])
            plt.figure(figsize=(30,30))
            plt.xlabel("Year", fontsize=20)
            plt.ylabel("CFC12 data", fontsize=20)
            x = np.array(year_list_for_graph, dtype = np.float32)
            y = np.array(CFC12_list_for_graph, dtype = np.float32)
            plt.scatter(x, y)
            (m,b) = np.polyfit(x, y, 1)
            new_y = m*x + b
            plt.plot(x, new_y)
            plt.show()
        elif agent_row == 5:
            for row in result:
                CFC11_list_for_graph.append(row[agent_row])
            plt.figure(figsize=(30,30))
            plt.xlabel("Year", fontsize=20)
            plt.ylabel("CFC11 data", fontsize=20)
            x = np.array(year_list_for_graph, dtype=np.float32)
            y = np.array(CFC11_list_for_graph, dtype=np.float32)
            plt.scatter(x, y)
            (m,b) = np.polyfit(x, y, 1)
            new_y = m*x + b
            plt.plot(x, new_y)
            plt.show()
        elif agent_row == 6:
            for row in result:
                minor15_list_for_graph.append(row[agent_row])
            plt.figure(figsize=(30,30))
            plt.xlabel("Year", fontsize=20)
            plt.ylabel("15minor data", fontsize=20)
            x = np.array(year_list_for_graph, dtype=np.float32)
            y = np.array(minor15_list_for_graph, dtype=np.float32)
            plt.scatter(x, y)
            (m,b) = np.polyfit(x, y, 1)
            new_y = m*x + b
            plt.plot(x, new_y)
            plt.show()


Thread.db_pre_config() #Calls the db_pre_config function 
Thread.database_input() #Calls the database_input function
for i in range(7):
        thread_function = threading.Thread(target = Thread.thread_and_plot_setup, args=[i])
        thread_function.start() #Starts the thread
        thread_function.join() #Joins the thread
        time.sleep(2) #Specifies the standby time
        


# In[ ]:




