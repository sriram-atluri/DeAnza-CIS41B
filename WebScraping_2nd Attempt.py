#!/usr/bin/env python
# coding: utf-8

# In[58]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# --- All the packages to be imported from the FrontEnd to the BackEnd ---#
from urllib.request import urlopen #Imports the url opener from the url functions library package
from bs4 import BeautifulSoup #Imports the Beautiful Soup utility from bs4 to allow for html parsing
import sqlite3 #Allows for the connection to the SQL database
import re #Imports the regex package to parse using regex
import matplotlib.pyplot as plotter #Imports the matplotlib package 
import numpy as np #Imports the numpy package to do the numerical calculations

#--------------------The class and its respective functions -----------------------------#

class ScrapeToSQL: #Creates the ScrapeToSQL class from the scraping activity to storing into the SQL Database
    
        def __init__(self): #Initializes the constructor 
            self.country = [] #Creates the instance of country and the list
            self.emissions = [] #Creates the instance of emissions and the list
        def create_database():  #The function by the name "initialize_database" runs the methods to initialize the database
            connection = None #The connection is initially set as "None"
            try: #The first set of instructions are executed
                connection = sqlite3.connect('Country_vs_Emission_Data.db') #Establishes the connection to the database by creating the db file with the connection object set from above
            except Error as e: #If error occurs, an error message is printed to the screen, in the 2nd set of instructions
                print(e)
            finally: #The final set of instructions, if the above steps fail, is to close the connection
                if connection:
                    connection.close()
        def create_table():
            connection = sqlite3.connect('Country_vs_Emission_Data.db') #Establishes the connection to the database by creating the db file with the connection object set from above
            cur = connection.cursor() #Instantiates the cursor object
            data_table = "CREATE TABLE country_emissions (country VARCHARS(20), emissions VARCHARS(20))" #The command is specified on what data will be stored
            cur.execute(data_table) #The cur variable executes the SQL command specified in the data_table variable
        def insert_table():
            #-----------------------The parsing of the countries----------------------------------------# 
            country = [] #Creates the stack to store the countries
            html_file = urlopen('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions') #The html_file variable calls upon the urlopen function to open the desired webpage
            soup = BeautifulSoup(html_file, 'html.parser') #The soup instance parses the specified HTML file
            length_of_countries_scrap = len(soup.select('td a'))
            for i in range(1, length_of_countries_scrap - 145):
                tdElements_for_countries = soup.select('td a')[i]
                country.append(str(tdElements_for_countries.get('title')))
            print(len(country))
            print(country)
            #-----------------------The parsing of the emissions data----------------------------------------# 
            emissions = [] #Creates the stack to store the emissions data
            html_file = urlopen('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions') #The html_file variable calls upon the urlopen function to open the desired webpage
            soup = BeautifulSoup(html_file, 'html.parser') #The soup instance parses the specified HTML file
            td_elements_for_percentages = soup.select('td')
            percentages = re.findall(r"([0-9]*.[0-9][0-9]%\B)+", str(td_elements_for_percentages)) #Finds all the 2017 (% of the world data) based on the specified Regex parameters
            for i in range(3, len(percentages)-32): #Converts the percentages from string form to float form by removing the % sign from the end of each data piece
                converted_percentage = percentages[i]
                emissions.append(float(converted_percentage[:-1]))
            #print(emissions) The initial set of values is printed to check the list
            #print(len(emissions)) #The length is printed to check how many values are missing
            #index = emissions.index(float(0.97)) #The index for this value is located, as it applies to three countries
            emissions.insert(97, float(0.97)) #0.97 is manually inserted into indices 97 and 98 to account for the other two countries
            emissions.insert(98, float(0.97))
            #print(len(emissions)) #The updated length is checked
            #print(emissions.index(float(0.76)))  #The index for this value is located, as it applies to three countries
            emissions.insert(179, float(0.76)) #An extra 0.76 is inserted to account for the two countries
            emissions.insert(181, float(0.00)) #An extra 0.00 is inserted to account for two countries
            #print(len(emissions)) #We check the updated length
            emissions.insert(185, float(0.11))  #An extra 0.11 is inserted to account for the two countries
            #print(len(emissions)) #We check the updated length again to see how much closer we are
            #print(emissions.index(float(0.91)))
            emissions.insert(70, float(0.91)) #An extra 0.91 is inserted to account for two countries
            #-------------------------The insertion of the countries and emissions data--------------------------------------#
            connection = sqlite3.connect('Country_vs_Emission_Data.db') #Establishes the connection to the database by creating the db file with the connection object set from above
            cur = connection.cursor() #Same as before
            insert_command = "INSERT INTO country_emissions (country, emissions) VALUES (?, ?)" #Inserts the data into the table in the database
            for i in range(0, len(country)):
                populate_values = (country[i], emissions[i])
                cur.execute(insert_command, populate_values)
                connection.commit() #This is a required command in order for the commands to actually insert the data into the table
            
#-------------------------The calling of the ScrapeToSQL functions----------------------------------------#  

ScrapeToSQL.create_database() # Calls the create_database command from the ScrapeToSQL class 
ScrapeToSQL.create_table() # Calls the create_table command from the ScrapeToSQL class
ScrapeToSQL.insert_table() # Calls the insert_table command from the ScrapeToSQL class


#-----------------------------The pie graph plotting of the top 10 countries and the emission data -----------#

class PieGraph: #The pie graph class
    def __init__(self):
        self.top_10_countries = []
        self.emissions_data = []
    def select_and_graph_elements():
            connection = sqlite3.connect('Country_vs_Emission_Data.db') #Establishes the connection to the database by creating the db file with the connection object set from above
            cur = connection.cursor() #Instantiates the cursor object
            sqlite_select_query = "SELECT country, emissions FROM country_emissions ORDER BY emissions DESC"
            cur.execute(sqlite_select_query) #Executes the sqlite_select_query
            records = cur.fetchall() #Fetches all the data from the execute command in the prior line
            row1 = [] # Creates the list to collect the raw row data from the SQLite database
            row2 = [] # Creates the list to collect the raw data from the SQLite database
            top_10_countries = [] #Creates the list for the top 10 emission producing countries
            top_10_emissions_data = [] #Creates the list for the quantitative data of the top 10 emission producing countries
            for row in records: #Appends the raw data from the rows in the SQLite database
                row1.append(row[0])
                row2.append(row[1])
            for i in range(0, 10): #The top 10 countries as well as their emission levels are added to the respective stacks
                top_10_countries.append(row1[i]) #Appends the top 10 countries to the top 10 countries list
                top_10_emissions_data.append(float(row2[i])) #Appends the emissions data into the top_10_emissions_data list
            fig1, ax1 = plotter.subplots() #Creates the pie-graph figure and the axes
            explode = (0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75)
            ax1.pie(top_10_emissions_data, explode=explode, labels=top_10_countries, autopct='%.2f%%') #Specifies the parameters on the graph layout should be
            ax1.axis('equal') #Sets the axes equal
            plotter.show() #Displays the pie graph
            
PieGraph.select_and_graph_elements() #The function is called in order for select_and_graph_elements() to execute


# In[ ]:



# In[ ]:




