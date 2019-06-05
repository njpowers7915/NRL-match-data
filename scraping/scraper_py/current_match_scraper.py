#Scraping Imports
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
#SQL Imports
import mysql.connector
#Pandas imports
import pandas as pd

#xpath for each match on a round page
1 --> //*[@id="draw-content"]/div/div/div/section[1]/ul/li/div[1]/div[1]/a
2 --> //*[@id="draw-content"]/div/div/div/section[2]/ul/li[1]/div[1]/div[1]/a
3 --> //*[@id="draw-content"]/div/div/div/section[2]/ul/li[2]/div[1]/div[1]/a
4 --> //*[@id="draw-content"]/div/div/div/section[3]/ul/li[1]/div[1]/div[1]/a
5 --> //*[@id="draw-content"]/div/div/div/section[3]/ul/li[2]/div[1]/div[1]/a
6 --> //*[@id="draw-content"]/div/div/div/section[3]/ul/li[3]/div[1]/div[1]/a
7 --> //*[@id="draw-content"]/div/div/div/section[4]/ul/li[1]/div[1]/div[1]/a
8 --> //*[@id="draw-content"]/div/div/div/section[4]/ul/li[2]/div[1]/div[1]/a
