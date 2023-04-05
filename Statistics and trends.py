# -*- coding: utf-8 -*-
"""


@author: Bineeth Mathew
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis


def dataFrame(file_name, years, countries, col, value1):
    """Reading manipulating file with country name
      and returning a dataframe and transpose of the dataframe as return"""
    # Read the CSV file into a DataFrame and skip the first 4 rows.
    df = pd.read_csv(file_name, skiprows=4)

    # Group the DataFrame by the specified column.
    df_grouped = df.groupby(col, group_keys=True)

    # Filter the DataFrame to include only the rows with the specified column .
    df_filtered = df_grouped.get_group(value1)

    # Reset the index of the DataFrame.
    df_filtered = df_filtered.reset_index()

    # Store the 'Country Name' column in a variable.
    country_names = df_filtered['Country Name']

    # Crop the DataFrame to include only the specified years and countries.
    df_cropped = df_filtered.iloc[countries, years]

    # Insert the 'Country Name' column back into the DataFrame.
    df_cropped.insert(loc=0, column='Country Name', value=country_names)

    # Drop any columns that contain NaN values.
    df_clean = df_cropped.dropna(axis=1)

    # Transpose the DataFrame.
    df_transposed = df_clean.set_index('Country Name').T

    # Return the filtered DataFrame and its transposed version.
    return df_clean, df_transposed


'''Reading a dataframe with multiple indicator name and returning a dataframe
where dataframe will be used for the Heat Map '''


def stats_f(file_name, years, col, value1):
    # Read data from CSV file, skip first 4 rows
    df = pd.read_csv(file_name, skiprows=4)
    # Group data by col value and get group with value1
    df1 = df.groupby(col).get_group(value1)
    # Reset the index of the dataframe
    df1 = df1.reset_index()
    # Crop the data from dataframe based on specified years
    df1 = df1.iloc[:, years]
    # Drop rows with missing values
    df1 = df1.dropna(axis=0)
    # Drop columns with missing values
    df1 = df1.dropna(axis=1)
    # Transpose the index of the dataframe
    df2 = df1.set_index("Indicator Name").T
    df2 = df2.rename_axis(None, axis=1)
    # Return the cleaned and transposed dataframe
    return df2


def work(file_name):
    """a fuction called stats_af is used to do some basic statistic on
      the data frame. Takes the dataframe with countries as
      columns as the argument.
      parameter:
          af = file name
          """
    # To explore dataset by describe()
    print(file_name.describe())
    return


"""Function to create a heatmap using matplotlib"""


def heatMap(value2, colours, title_name, x):

    fig, ax = plt.subplots(figsize=(20, 20))
    # creating a Heatplot
    im = ax.imshow(value2, cmap=colours)
    # creating a Heatplot bar for more data accuracy
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.85)
    # add tick labels
    ax.set_xticks(np.arange(len(x)), labels=x, size=20)
    ax.set_yticks(np.arange(len(x)), labels=x, size=12)
    # Rotate the tick labels to be more legible
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
             rotation_mode="anchor")
    ax.set_title(title_name, size=12)
    fig.tight_layout()
    # saving Heatmap
    plt.savefig(title_name + ".png", format='png', dpi=150)
    return


'''with this function Plotting a bar graph using pandas plotting method'''


def plot_p(DataFrame, col, types, name):
    # plotting graph with the parameter which given in the function
    ax = DataFrame.plot(x=col, rot=45, figsize=(50, 25),
                        kind=types, title=name, fontsize=30)
    # setting legend font size
    ax.legend(fontsize=36)
    # setting Title and font size for a plot
    ax.set_title(name, pad=20, fontdict={'fontsize': 40})
    return


# years using for the data analysis
years = [35, 40, 45, 50, 55, 60, 64]
# countries which are using for data analysis
countries = [35, 40, 55, 81, 109, 119, 202, 205, 251]
'''calling dataFrame functions for all the dataframe which will be
                      used for visualization'''
population_c, population_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv",
                                       years, countries, "Indicator Name",
                                       "Population,total")
Green_gas_c, Green_gas_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                                     countries, "Indicator Name",
                                     "Total greenhouse gas emissions(ktofCO2)")
co2_c, co2_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                         countries, "Indicator Name", "CO2 emissions (kt)")
Up_c, Up_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv", years,
                       countries, "Indicator Name", "Urban population")
Canada = stats_f("API_19_DS2_en_csv_v2_4700503.csv",
                 [3, 35, 40, 45, 50, 55, 60, 64], "Country Name", "Canada")

# plotting the bar graph1
plot_p(population_c, "Country Name", "bar", "Total population")
# Saving plot
plt.savefig('Total population.jpg')
plot_p(Green_gas_c, "Country Name", "bar", "Total greenhouse gas emissions")
plt.savefig('Total greenhouse gas emissions.jpg')

legend_properties = {'weight': 'bold', 'size': 36}
# plotting the bar graph-2
ax1 = Up_y.plot(figsize=(60, 30), kind="line", fontsize=36, linewidth=4.0)
# setting a title for the graph
ax1.set_title("Total Urban population", pad=20, fontdict={'fontsize': 40})
ax1.legend(loc=2, prop=legend_properties)
# Saving plot
plt.savefig(' Total Urban population line.jpg')

# creating a line graph using pandas
ax2 = co2_y.plot(figsize=(60, 30), kind="line", fontsize=36, linewidth=4.0)
# setting a Title for a graph
ax2.set_title("Total Co2 Emission", pad=30, fontdict={'fontsize': 40})
# setting legends for a graph
ax2.legend(prop=legend_properties)
# Saving plot
plt.savefig('Total Co2 Emission line.jpg')
# creating a variable x for HeatMap
x = ["Population, total", "Urban population", "Foreign direct investment",
     "net inflows(% of GDP)", "CO2 emissions(kt)"]
# filtering the columns and rows as per the heatmap requirement
canada = Canada.loc[:, x]
# correlation usied in heatmap the heatmap
correlation = canada.corr()
print(correlation)

# Calling a function to create a heatmap
heatMap(correlation, "YlOrBr", "Canada's Heatmap", x)


# some basic statistic function using stats_af function

work(Green_gas_c)
work(co2_c)
work(Up_c)
