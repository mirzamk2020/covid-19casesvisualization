######################################################
# Name: Mirza MK Baig
# Project: Global COVID-19 cases visualization
# URL: https://trinket.io/library/trinkets/b05765a5fc
# 
# Description: In this project, I used urllib.request, json, and pygal modules to create charting
# that demonstrates the COVID-19 confirmed cases and recovered by date with a line chart and COVID-19
# confirmed cases and recovered by country with a pie chart of top 'x' countries in the world.
# I utilized the data from github that transformed into json file. The data originally came from
# the data repository for the 2019 Novel Coronavirus Visual Dashboard operated 
# by the Johns Hopkins University Center for Systems Science and Engineering.
#

######################################################
#!/bin/python3

import urllib.request
import json
import pygal

url = "https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json"

#accesses the file
covid_response = urllib.request.urlopen(url)

#opens the file to read
covid_data = covid_response.read()

#creates dictionary from the covid data
data = json.loads(covid_data)

#obtain country names from the main keys of the data
country_names = map(lambda e:e, data)


#a nested list of confirmed cases for a total of 190 countries
confirmed_cases = []
recovered_cases = []

#uses nested for loop to append the confirmed cases for each country to daily_cases 
#then that daily_cases list for that country is appended to all cases list
for i in range(len(country_names)):
  daily_cases =[]
  recovered = []
  #list with all the dates
  date_list = []
  for day in data[country_names[i]]:
    daily_cases.append(day["confirmed"])
    date_list.append(day["date"])
    recovered.append(day["recovered"])
  confirmed_cases.append(daily_cases)
  recovered_cases.append(recovered)

#creates a dictionary for each country with name and confirmed cases list
#uses zip function to pair the two objects together(country_names and all_cases)
country_confirmed_cases = dict(zip(country_names, confirmed_cases))
country_recovered_cases = dict(zip(country_names, recovered_cases))


confirmed_cases_list_of_tuples = []
recovered_cases_list_of_tuples = []
for i in range(len(country_names)):
  cases_list = country_confirmed_cases[country_names[i]] #gets the list of cases from dict
  recovered_cases_list = country_recovered_cases[country_names[i]]
  confirmed_value = cases_list[-1] #gets the recent confirmed case value
  recovered_value = recovered_cases_list[-1] #gets recent recovered case value
  country_confirmed_cases_pair = (country_names[i] , confirmed_value)
  country_recovered_cases_pair = (country_names[i], recovered_value)
  confirmed_cases_list_of_tuples.append(country_confirmed_cases_pair) #adds to the list of tuples
  recovered_cases_list_of_tuples.append(country_recovered_cases_pair)

confirmed_sorted_tuples = sorted(confirmed_cases_list_of_tuples, key = lambda v:v[1], reverse = True)
recovered_sorted_tuples = sorted(recovered_cases_list_of_tuples, key = lambda v:v[1], reverse = True)

x = int(input("Enter an integer to see Top 'x' countries corona confirmed cases and recovered"))

#Line chart for confirmed cases
line_chart = pygal.Line()
line_chart.title = 'Corona Cases by Date'
#data list contains all the dates that are same for all countries
line_chart.x_labels = map(str, date_list)
#loops for x many times user entered to get top x countries corona cases
for i in range(x):
  line_chart.add(confirmed_sorted_tuples[i][0], country_confirmed_cases[confirmed_sorted_tuples[i][0]])
line_chart.render()

#Line chart for recovered
line_chart = pygal.Line()
line_chart.title = 'Recovered Corona Cases by Date'
#data list contains all the dates that are same for all countries
line_chart.x_labels = map(str, date_list)
#loops for x many times user entered to get top x countries corona cases
for i in range(x):
  line_chart.add(recovered_sorted_tuples[i][0], country_recovered_cases[recovered_sorted_tuples[i][0]])
line_chart.render()

#Pie chart for confirmed cases
confirmed_pie_chart = pygal.Pie()
confirmed_pie_chart.title = 'Corona Cases by Country'
#loops through the list of sorted tuples
for i in range(len(confirmed_sorted_tuples)):
  confirmed_pie_chart.add(confirmed_sorted_tuples[i][0], confirmed_sorted_tuples[i][1] )
confirmed_pie_chart.render()

#Pie chart for recovered
recovered_pie_chart = pygal.Pie()
recovered_pie_chart.title = 'Recovered Corona Cases by Country'
#loops through the list of sorted tuples
for i in range(len(recovered_sorted_tuples)):
  recovered_pie_chart.add(recovered_sorted_tuples[i][0], recovered_sorted_tuples[i][1] )
recovered_pie_chart.render()


