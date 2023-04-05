# -*- coding: utf-8 -*-
"""


@author: BINEETH MATHEW
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sts
from scipy.stats import skew, kurtosis

"""Reading manipulating file with country name
and returning a dataframe and transpose of the dataframe as return"""


def dataFrame(file_name, years, countries, col, value1):
    # Reading Data for dataframe
    data = pd.read_csv(file_name, skiprows=4)
    # Grouping data with col value
    data1 = data.groupby(col, group_keys=True)
    # retriving the data with the all the group element
    data1 = data1.get_group(value1)
    # Reseting the index of the dataframe
    data1 = data1.reset_index()
    # Storing the column data in a variable
    a = data1['Country Name']
    # cropping the data from dataframe
    data1 = data1.iloc[countries, years]
    data1.insert(loc=0, column='Country Name', value=a)
    # Dropping the NAN values from dataframe Column wise
    data1 = data1.dropna(axis=1)
    # transposing the index of the dataframe
    data2 = data1.set_index('Country Name').T
    # returning the normal dataframe and transposed dataframe
    return data1, data2

'''Reading a dataframe with multiple indicator name and returning a dataframe
where dataframe will be used for the Heat Map '''


def stats_f(file_name, years, col, value1):
    # Reading Data for dataframe
    df = pd.read_csv(file_name, skiprows=4)
    # Grouping data with col value
    df1 = df.groupby(col, group_keys=True)
    # retriving the data with the all the group_by element
    df1 = df1.get_group(value1)
    # Resetting the index of the dataframe
    df1 = df1.reset_index()
    # cropping the data from dataframe
    df1 = df1.iloc[:, years]
    # Dropping the NAN values from dataframe Columnwise
    df1 = df1.dropna(axis=0)
    # Dropping the NAN values from dataframe Rowwise
    df1 = df1.dropna(axis=1)
    # transposing the index of the dataframe
    df2 = df1.set_index("Indicator Name").T
    df2 = df2.rename_axis(None, axis=1)
    # returning dataframe required for Heatmap
    return df2

'''with this function Plotting a bar graph using pandas plotting method'''
def plot_p(DataFrame, col, types, name):
    #plotting graph with the parameter which given in the function
    ax = DataFrame.plot(x=col, rot=45, figsize=(50,25),
                      kind= types, title= name, fontsize=30)
    #setting legend font size
    ax.legend(fontsize=36)
    #setting Title and font size for a plot
    ax.set_title(name, pad=20, fontdict={'fontsize':40})
    return

def stats_af(af):
    """a fuction called stats_af is used to do some basic statistic on
    the data frame. Takes the dataframe with countries as
    columns as the argument.
    parameter:
        af = file name
        """
    # To explore dataset by describe()
    print(af.describe())
    # to find skewness
    print("\nSkewness:\n", skew(af))
    # to find kurtosis
    print("\nKurtosis:\n", kurtosis(af))

    return

"""Function to create a heatmap using matplotlib"""


def heatMap(value2, colours, title_name, x):
    fig, ax = plt.subplots(figsize=(20, 20))
    # creating a Heatplot
    im = ax.imshow(value2, cmap=colours)
    # creating a Heatplot bar for more data accuracy
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.85)
    # add tick labels
    ax.set_xticks(np.arange(len(x)), labels= x, size = 20)
    ax.set_yticks(np.arange(len(x)),labels=x, size = 12)
    # Rotate the tick labels to be more legible
    plt.setp(ax.get_xticklabels(),rotation = 90,ha = "right",rotation_mode = "anchor")
    ax.set_title(title_name, size = 12)
    fig.tight_layout()
    # saving Heatmap
    plt.savefig(title_name + ".png", format ='png', dpi = 150)
    return

# years using for the data analysis
years = [35, 40, 45, 50, 55, 60, 65]
# countries which are using for data analysis
countries = [35, 40, 55, 81, 109, 119, 202, 205, 233, 251]
'''calling dataFrame functions for all the dataframe which will be
used for visualization'''
population_c, population_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                                     countries, "Indicator Name", "Population, total")
Green_gas_c, Green_gas_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                                    countries, "Indicator Name",
                                    "Total greenhouse gas emissions (kt of CO2 equivalent)")
co2_c, co2_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                        countries,"Indicator Name","CO2 emissions (kt)")
Up_c, Up_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                      countries, "Indicator Name", "Urban population")
india = stats_f("API_19_DS2_en_csv_v2_4700503.csv", [3,35,40,45,50,55,60,64],
                "Country Name", "India")

# plotting the bar graph1
plot_p(population_c, "Country Name", "bar", "Total population")
# Saving plot
plt.savefig('Total population.jpg')
plot_p(Green_gas_c, "Country Name", "bar", "Total greenhouse gas emissions (kt of CO2 equivalent)")
plt.savefig('Total greenhouse gas emissions.jpg')

legend_properties = {'weight':'bold', 'size':36}
# plotting the bar graph-2
ax1 = Up_y.plot(figsize=(60,30), kind="line", fontsize=36, linewidth=4.0)
#setting a title for the graph
ax1.set_title("Total Urban population", pad=20, fontdict={'fontsize':40})
ax1.legend(loc=2, prop=legend_properties)
# Saving plot
plt.savefig('Total Urban population line.jpg')

#creating a line graph using pandas
ax2 = co2_y.plot(figsize=(60,30), kind="line", fontsize=36, linewidth=4.0)
#setting a Title for a graph
ax2.set_title("Total Co2 Emission", pad=30, fontdict={'fontsize':40})
#setting legends for a graph
ax2.legend(prop=legend_properties)
# Saving plot
plt.savefig('Total Co2 Emission line.jpg')
# creating a variable x for HeatMap
x=["Population, total","Urban population","Foreign direct investment, net inflows (% of GDP)","CO2 emissions (kt)"]
# filtering the columns and rows as per the heatmap requirement
india = india.loc[:,x ]
# correlation usied in heatmap the heatmap
correlation= india.corr()
print(correlation)

# some basic statistic function using stats_af function
stats_af(population_y)
stats_af(Green_gas_y)
stats_af(co2_y)
stats_af(Up_y)

#Calling a function to create a heatmap
heatMap(correlation, "YlOrBr", "Indian's Heatmap",x)
