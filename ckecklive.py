from playwright.sync_api import sync_playwright
import time
import random
import os
from pop3_imap import get_verification_code
from vn_fullname_generator.generator import generate
import faker
from playwright.async_api import async_playwright
import requests
import re
from creatChromeProfile import main
from deletAndCreatNewFolder import delete_profiles
from playwright.sync_api import sync_playwright, Playwright
from fake_useragent import UserAgent
import multiprocessing
import pygetwindow as gw
from datetime import datetime, timedelta
import shutil

# Hàm mở profile và add ext bypasss captcha
def find_paragraph_with_text(page, text):
    selector = f'p:has-text("{text}")'
    element = page.locator(selector)
    return element
def open_browser_with_profile(page,context,mail_pass,lock):

        # Xóa page[0]
        pages = context.pages
        if len(pages) > 1:
            pages[0].close()
        split = mail_pass.split('|')
        username = split[2]
        print(username)
        # Chuyển tới trang đăng ký
        time.sleep(3)
        try:
            page.goto(f'https://www.tiktok.com/@{username}')
            page.wait_for_load_state("load")
        except requests.ConnectionError:
            time.sleep(10)
            page.goto(f'https://www.tiktok.com/@{username}')
            page.wait_for_load_state("load")
        time.sleep(5)
        captcha_element = page.locator('.captcha-solver-info')
        check_captcha = False
        while not check_captcha:
            captcha_element = page.locator('.captcha-solver-info')
            if captcha_element.is_visible():
                print("Tiếp tục giải captcha")
                time.sleep(10)
            else :
                check_captcha = True   
        # button_selector = 'button[data-e2e="next-button"]'
        # button_element = page.locator(button_selector)
        # button_element.click()
        text_content = "Couldn't find this account"
        element = find_paragraph_with_text(page, text_content)
        if element.is_visible():
            with lock:
                with open('die.txt', 'a', encoding='utf-8') as error_file:
                    error_file.write(f"{mail_pass}|tài khoản die\n")
                return True
        else:
            with lock:
                with open('live.txt', 'a', encoding='utf-8') as error_file:
                    error_file.write(f"{mail_pass}\n")
            return False

# Xóa profile
def delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass):
 try :
    with lock:
      if current_position.value <= len(mail_pass_list):
          # Ghi dữ liệu còn lại trở đi vào file
          with open('Account.txt', 'w') as file:
              file.write('\n'.join(mail_pass_list[current_position.value:]))
          print(f"Process {process_id} deleted line: {mail_pass}")
 except ValueError as e:
      # Xử lý lỗi khi không thể tách mail và pass
      print(f"Process {process_id} encountered an error: {e}")



def while_loop(user_data_dir, extension_path,process_id, mail_pass_list, current_position, lock):
    try:
        while True :
                ua = UserAgent()
                user_agent = ua.random
                with lock:
                  if current_position.value >= len(mail_pass_list):
                      break
                  mail_pass = mail_pass_list[current_position.value]
                  current_position.value += 1
                print(user_agent)
                print(process_id)
                #user_data_dir = user_data_dir+str(process_id)
                print(user_data_dir)
                #input("check")
                with sync_playwright() as p:
                    # Mở trình duyệt với profile đã cung cấp
                    context = p.chromium.launch_persistent_context(
                        user_data_dir,
                        headless=False,   
                        args=[
                            f"--disable-extensions-except={extension_path}",
                            f"--load-extension={user_data_dir}",
                        ],
                        user_agent=user_agent,
                        viewport={'width': 600, 'height': 600},
                        screen={'width': 600, 'height': 600},
                    )
                    page = context.new_page()
                    #page.set_viewport_size({"width": 400, "height": 400})
                    # window = gw.getWindowsWithTitle('TikTok')[0]
                    # window.moveTo(200*process_id, 400)
                    #page.goto('https://www.tiktok.com/@khongyeukemay')
                    page.goto('chrome-extension://ifnpembpekmnpihkkmjallnjelnfodep/popup/popup.html')
                    time.sleep(3)
                    #page.evaluate(f"window.scrollTo({x}, {y})")
                    page.fill('[placeholder="Enter subscription key"]', 'c03ca43736416de2612946d22ede7026')
                    page.click('.plan_button.save_key.clickable')
                    time.sleep(2)
                    # Các thao tác khác trên trang web
                    #input("Press Enter to continue...")
                    if open_browser_with_profile(page,context,mail_pass,lock):
                        #delete_Fistline()
                        page.close()
                        context.close()
                        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                        continue
                    else :
                        page.close()
                        context.close()
                        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                        continue
    except Exception as e:
        print(f"An error occurred: {e}")
        with lock:
            with open('maximum.txt', 'a', encoding='utf-8') as maximum_file:
                maximum_file.write(mail_pass+'\n')
        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
        while_loop(user_data_dir, extension_path,process_id, mail_pass_list, current_position, lock)
def main(user_data_dir, extension_path):
 #delete_profiles()
 num_processes = int(input("Nhập số luồng cần chạy : "))
 while True:
    try:
        with open('Account.txt', 'r') as file:
            mail_pass_list = [line.strip() for line in file]
            print(mail_pass_list)
    except FileNotFoundError:
        print("File 'Account.txt' không tồn tại.")
        return

    if not mail_pass_list:
        print("File 'Account.txt' không có dữ liệu.")
        with open('maximum.txt', 'r') as source:
            data = source.read()
        if not data :
            print("ssss")
            return 
        else:
            print("cherp file")
            with open('Account.txt','w') as write_to_Mail :
                write_to_Mail.write(data)
            with open('maximum.txt', 'w') as source:
                source.write('')
            try:
                with open('Account.txt', 'r') as file:
                    mail_pass_list = [line.strip() for line in file]
                    print(mail_pass_list)
            except FileNotFoundError:
                print("File 'Account.txt' không tồn tại.")
                return

    current_position = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()

    
    processes = []

    for i in range(num_processes):
        process = multiprocessing.Process(target=while_loop, args=(user_data_dir+str(i), extension_path,i+1, mail_pass_list, current_position, lock))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

if __name__ == "__main__":
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    #user_data_dir = r"F:\Tool PY\AuToRegTT\user_profile\profile"
    user_data_dir = os.path.join(current_folder_path, "user_profile/profile")
    #extension_path = r"F:\Tool PY\AuToRegTT\extension\Achi"
    extension_path = os.path.join(current_folder_path, "extension/Achi")
    #while_loop(user_data_dir, extension_path)
    main(user_data_dir, extension_path)