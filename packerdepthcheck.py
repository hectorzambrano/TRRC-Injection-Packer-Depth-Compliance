############### Packer Depth Delinquency Checks ###############

############### Checks Texas RRC injection/disposal permits for injection zone depths
#               and compares it to the most recent H-10 reported packer depths. ###############

############### Hector Zambrano, July 2020 ###############

from selenium import webdriver
import pandas as pd
import re

############### Create blank dataframe ###############

#column_names = ["Lease Name", "Well Number", "UIC Number", "Top Injection Zone", "Bottom Injection Zone",
                #"Approved Packer Depth", "Reported Packer Depth", "H-10 Date", "Delinquent Packer Depth?"]

column_names = ["Lease Name", "Well Number", "UIC Number","API Number","Approved Packer Depth","Top Injection Zone", "Bottom Injection Zone"]


df = pd.DataFrame(columns=column_names)

############### Create Chrome webdriver instance ###############

# need to have Chromedriver installed in same folder as python script before running.

driver = webdriver.Chrome()
driver.get("http://webapps2.rrc.texas.gov/EWA/uicQueryAction.do")

############### prompt user for lease ID ###############

#lease_id = input("Please enter Lease ID:")

############### Inputs into search query ###############

# need "" in argument for send.keys to make it work for lease numbers beginning with 0 - test converting input to string?

lease = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input").send_keys("24526")
status = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]/select/option[2]").click()
submit = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[4]/td/input[1]").click()

############### Change Page Size to View All ###############
# Will not work for very large search results but probably fine for only active wells - test for more leases

page_size = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/label/select/option[1]").click()

############### Get total number of results ###############

results_string = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]").text
results_number = re.findall('^[0-9]*',results_string)   # regular expressions to extract number - test if it works for triple digits
#print(results_number[0])
results_number = int(results_number[0])

############### Scrape information from permits ###############

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

    data_results1.extend(data_results2)

    df.loc[i] = data_results1    # append to dataframe

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/input").click()  # return to search results


print("Done")
driver.quit()

df.to_csv(r'C:\Users\Hector A\Desktop\python\Packer Depth\injpermit.csv')
