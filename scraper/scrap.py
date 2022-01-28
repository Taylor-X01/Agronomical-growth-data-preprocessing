import os
import sys
import pandas as pd
import time
from selenium import webdriver

Url = "https://databank.banquemondiale.org/reports.aspx?source=2&Topic=1"
opts = webdriver.ChromeOptions()
opts.headless = False
driver = webdriver.Chrome(
    executable_path="C:\\chromedriver\\chromedriver97.exe")
driver.get(Url)

class scrap_WorldBank:

    def __init__(self,driver=driver,url=Url):
        self.url = Url
        self.driver = driver
        self.header = None
        self.data = None

    def _setup_layout(self,driver):
        """
        Setup the layout of the data table with countries in the rows,
        series in columns, and years in pages 
        """
        layout = []
        layout.append(driver.find_element_by_xpath('.//*[@id="liLayout"]/a[1]'))
        layout.append(driver.find_element_by_xpath('//*[@id="liOrienationPopular"]'))
        layout.append(driver.find_element_by_xpath('.//*[@id="divTablePopularOrientation"]/label[4]'))
        layout.append(driver.find_element_by_xpath('.//*[@id="divReportContent"]/div[5]/a[2]'))
        for i in range(len(layout)):
            layout[i].click()


    def get_table_header(self,driver):
        """
        Get series name from the website table
        """
        self.header = ['Countries']
        head = driver.find_element_by_id(
            'grdTableView_DXHeadersRow0').find_elements_by_xpath('.//td[contains(@id, "grdTableView_col")]')
        print(len(head))
        for i,col in enumerate(head[1:]):
            h_text = col.find_element_by_xpath('.//table/tbody/tr/td/span[@class="grid-column-text"]')
            self.header.append(h_text.get_attribute('innerHTML'))
        
        print(f"Out from the header : {self.header}")



    def get_table_content(self,driver):
        """
        Get the every row of the data table
        """
        self.get_table_header(driver)
        self.data = []
        R = driver.find_elements_by_xpath('.//*[contains(@id,"grdTableView_DXDataRow")]')

        for row in R:
            var = row.find_elements_by_tag_name('td')
            data_list = [r.get_attribute('innerHTML') for r in var[:len(self.header)]]
            self.data.append(data_list)


    def convert2csv(self):
        data = self.data
        header = self.header

        print(f"Header size : {len(header)}\nColumns : {len(data[0])}")
        df = pd.DataFrame(data, columns=header)
        df.to_csv(index=False,path_or_buf='data.csv')



scraper = scrap_WorldBank(driver=driver,url=Url)
scraper._setup_layout(driver)
time.sleep(10)
scraper.get_table_content(driver)
scraper.convert2csv()