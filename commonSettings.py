import urllib
from bs4 import BeautifulSoup
import pickle
import simplejson
from pybing import Bing
import re
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
import mimetypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import getpass
import time

moneycontrolURL = 'http://www.moneycontrol.com/'
month = {'Jan':1,'Feb':1,'Mar':1,'Apr':1,'May':1,'Jun':1,'Jul':1,'Aug':1,'Sep':1,'Oct':1,'Nov':1,'Dec':1}
monthList = ['Mar','Jun','Sep','Dec']
def main():
    pass

if __name__ == "__main__":
    main()
