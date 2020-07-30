#!usr/bin/#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Packer Depth Delinquency Checks

Checks Texas RRC injection/disposal permits for injection zone depths
and compares it to the most recent H-10 reported packer depths.

Hector A Zambrano
July 2020

"""

__author__ = 'Hector A Zambrano'
__email__ = 'hector.a.zambrano@gmail.com'
__status__ = 'dev'

from selenium import webdriver
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib import style
import numpy as np

######################### Create blank dataframe ##############################

start_time = time.time()

column_names = ["Lease Name", "Well Number", "UIC Number","API Number",
                "Approved Packer Depth","Top Injection Zone",
                "Bottom Injection Zone","H-10 Date",
                "Reported H-10 Packer Depth"]

df = pd.DataFrame(columns=column_names)

######################### Create Chrome webdriver instance ####################

# need to have Chromedriver installed in same folder as python script
# before running.

driver = webdriver.Chrome()
driver.get("http://webapps2.rrc.texas.gov/EWA/uicQueryAction.do")

######################### prompt user for lease ID ############################

#lease_id = input("Please enter Lease ID:")

######################### Inputs into search query ############################

# need "" in argument for send.keys to make it work for lease numbers
# beginning with 0 - test converting input to string?

lease = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input").send_keys("18696")
status = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]/select/option[2]").click()
submit = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[4]/td/input[1]").click()

######################### Change Page Size to View All ########################
# Will not work for very large search results but probably fine for only
# active wells - test for more leases

page_size = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/label/select/option[1]").click()

######################### Get total number of results #########################

results_string = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]").text
results_number = re.findall('^[0-9]*',results_string)   # regular expressions to extract number - test if it works for triple digits
#print(results_number[0])
results_number = int(results_number[0])

######################### Scrape Injection Permits ############################

for i in range(results_number):

    row = 3+i   # first UIC permit starts at 3 in the xpath element

    data_results1 = [driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[%s]/td[5]" %row).text,
                        driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[%s]/td[6]" %row).text]  # get well name and number

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[%s]/td[1]/a" %row).click()  # s% used for string formatting

    data_results2 =  [driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]").text,
                    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]").text,
                    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[24]/td[2]").text,
                    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[25]/td[2]").text,
                    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[26]/td[2]").text]

############################ Scrape H-10 ######################################

    driver2 = webdriver.Chrome()
    driver2.get("http://webapps.rrc.texas.gov/H10/searchH10.do?fromMain=yes&sessionId=15960580028904")
    driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/input").send_keys(data_results2[0]) #use UIC number to search
    driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr[2]/td/input[1]").click()

    status_new = driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td/form/table/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr[3]/td[3]").text

    if status_new == "CURRENT": # current H-10s are still blank, open old H-10
        driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td/form/table/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/a").click()
        data_H10 = [driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td[3]/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/td[5]/p[2]/strong").text,
                    driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td[3]/form/table/tbody/tr/td/table[2]/tbody/tr[6]/td/table/tbody/tr[1]/td[2]/div/strong[1]").text]
    else:
        driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td/form/table/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/a").click()
        data_H10 = [driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td[3]/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/td[5]/p[2]/strong").text,
                    driver2.find_element_by_xpath("/html/body/table[4]/tbody/tr/td[3]/form/table/tbody/tr/td/table[2]/tbody/tr[6]/td/table/tbody/tr[1]/td[2]/div/strong[1]").text]

    driver2.quit()

    data_results1.extend(data_results2)
    data_results1.extend(data_H10)

######################### Append to dataframe #################################

    df.loc[i] = data_results1    # append to dataframe

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/input").click()  # return to search results

driver.quit()

######################### Data Cleanup ########################################

df['API Number'] = '42-' + df['API Number'].astype(str)

df[["Top Injection Zone", "Reported H-10 Packer Depth"]] = df[["Top Injection Zone", "Reported H-10 Packer Depth"]].apply(pd.to_numeric)

df['Depth Difference']= df["Top Injection Zone"]-df["Reported H-10 Packer Depth"]

df['SWR 9 Delinquent? (100 ft)']=df['Depth Difference'].gt(100)
df['Over 1000 ft?']=df['Depth Difference'].gt(1000)

df['SWR 9 Delinquent? (100 ft)']= df['SWR 9 Delinquent? (100 ft)'].replace(False, "No")
df['SWR 9 Delinquent? (100 ft)']= df['SWR 9 Delinquent? (100 ft)'].replace(True, "Yes")
df['Over 1000 ft?']= df['Over 1000 ft?'].replace(False, "No")
df['Over 1000 ft?']= df['Over 1000 ft?'].replace(True, "Yes")

df.to_csv(r'C:\Users\Hector A\Desktop\python\Packer Depth\injpermit.csv', index=False)

######################### Data Visualization ##################################
style.use('ggplot')

#extract counts
list_SWR9 = df[df['SWR 9 Delinquent? (100 ft)']=="Yes"].count().to_list()
list_1000ft = df[df['Over 1000 ft?']=="Yes"].count().to_list()

SWR9_counts = list_SWR9[10]
over1000ft_counts = list_1000ft[11]
total_count = df['SWR 9 Delinquent? (100 ft)'].count()
compliant_packers = total_count - SWR9_counts

noncompliant_ratio = SWR9_counts/total_count
compliant_ratio = compliant_packers/total_count
ratios_pie = [noncompliant_ratio, compliant_ratio]

over1000_ratio = over1000ft_counts/SWR9_counts
less1000_ratio = 1-over1000_ratio
ratios_bar = [over1000_ratio, less1000_ratio]

values_pie = [SWR9_counts,compliant_packers]

#function to show both counts and percentages in pie chart
def make_autopct(values_pie):
    def my_autopct(pct):
        total = sum(values_pie)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

# make figure and assign axis objects
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0)

# pie chart parameters
values_pie = [SWR9_counts,compliant_packers]
labels = ['Non-Compliant\n      Packers', 'Compliant Packers']
explode = [0.2, 0]
# rotate so that first wedge is split by the x-axis
angle = -180 * ratios_pie[0]
ax1.pie(ratios_pie, autopct=make_autopct(values_pie), startangle=angle,
        labels=labels, explode=explode, shadow=True)

# bar chart parameters
xpos = 0
bottom = 0
ratios_bar = [over1000_ratio, less1000_ratio]
width = .2

for j in range(len(ratios_bar)):
    height = ratios_bar[j]
    ax2.bar(xpos, height, width, bottom=bottom)
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100),
             ha='center')

ax2.set_title('Depth Difference from Top of Injection Zone')
ax2.legend(('Over 1000 feet', 'Less than 1000 feet'))
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
# get the wedge data
theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
center, r = ax1.patches[0].center, ax1.patches[0].r
bar_height = sum([item.get_height() for item in ax2.patches])

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show()

print("--- Web Scrape Complete %s seconds ---" % (time.time() - start_time))
