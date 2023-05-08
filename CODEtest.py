# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 03:14:35 2023

@author: filiz
"""
#Filippo Zallocco
#April 16, 2023
#MTA, Data Analytics Department
#Test file

#In this test file, I show how to import the functions from the CODE python file and how to call them on a Pandas data frame object
import CODE

pd = CODE.load_file(r"C:\Users\filiz\OneDrive\Desktop\Intern_Summer2023\MTA\Filippo_Zallocco_MTA_DATA\DATA\DATA.csv")

CODE.visualize_head(pd)

CODE.visualize_tail(pd)

CODE.get_info(pd)

CODE.total_successful_trips_by_weekday_and_weekend(pd)

CODE.average_by_mode(pd)

CODE.percentage_by_mode(pd)

CODE.histograms(pd)

CODE.sorted_zipcode(pd)