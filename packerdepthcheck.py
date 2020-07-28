# Packer Depth Delinquency Checks

# Checks Texas RRC injection/disposal permits for injection zone depths
# and compares it to the most recent H-10 reported packer depths.

# Hector Zambrano, July 2020

from selenium import webdriver
import pandas as pd

# Create blank dataframe

column_names = ["Lease Name", "Well Number", "UIC Number", "Top Injection Zone", "Bottom Injection Zone",
                "Approved Packer Depth", "Reported Packer Depth", "H-10 Date", "Delinquent Packer Depth?"]

df = pd.DataFrame(columns=column_names)

# Create Chrome webdriver instance, need to have Chromedriver installed in same folder as python script before running.

driver = webdriver.Chrome()
driver.get("http://webapps2.rrc.texas.gov/EWA/uicQueryAction.do")

# prompt user for lease ID

#lease_id = input("Please enter Lease ID:")

lease = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input").send_keys(18696)
status = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]/select/option[2]").click()
submit = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[4]/td/input[1]").click()
