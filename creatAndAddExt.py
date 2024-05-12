from playwright.sync_api import sync_playwright
import time
import random
import os
from Imap import get_code_mail
from vn_fullname_generator.generator import generate
import faker
import asyncio
import sys

mail = "wilheminafunplausible5228@hotmail.com"
passMail = "LbHRSyTMb"
codes_result = get_code_mail(mail, passMail)

if codes_result is not None:
    print('Codes:', codes_result)
    if codes_result['Inbox'] is None :
        print('Inbox code:', codes_result['Inbox']) 
    
    print('Junk code:', codes_result['Junk'])
else:
    print('Không thể lấy được mã.')
