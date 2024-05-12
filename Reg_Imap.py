from playwright.sync_api import sync_playwright
import time
import random
import os
from Imap import get_code_mail
from vn_fullname_generator.generator import generate
import faker
from playwright.async_api import async_playwright
import asyncio
import requests
import re
from creatChromeProfile import main
from deletAndCreatNewFolder import delete_profiles
from playwright.sync_api import sync_playwright, Playwright
import fake_useragent
from fake_useragent import UserAgent
import concurrent.futures
import threading
import multiprocessing
import pygetwindow as gw
import sys


# Hàm mở profile và add ext bypasss captcha
def open_browser_with_profile(page,context):

        # Xóa page[0]
        pages = context.pages
        if len(pages) > 1:
            pages[0].close()

        # Chuyển tới trang đăng ký
        time.sleep(3)
        try:
            page.goto('https://www.tiktok.com/signup/phone-or-email/email')
            page.wait_for_load_state("load")
        except requests.ConnectionError:
            time.sleep(10)
            page.goto('https://www.tiktok.com/signup/phone-or-email/email')
            page.wait_for_load_state("load")
        time.sleep(2000)
    
def check_file_acc(context) :
    if not os.path.isfile("mail.txt"):
            print("Tệp 'mail.txt' không tồn tại.")
            context.close()
            input("Nhấn Enter để kết thúc ......")
            
            exit(1)
    elif os.path.getsize("mail.txt") == 0:
            print("Tệp 'mail.txt' không có dữ liệu.")
            context.close()
            input("Nhấn Enter để kết thúc ......")
            
            exit(1)
# Thu room web 
def roomWeb(page):
    page.keyboard.down("Control")
    time.sleep(1)
    for _ in range(3):
        print("room")
        page.mouse.down()
    page.keyboard.up("Control")
    page.wait_for_timeout(2000)
# Setup random date
def setup_date(page):
    #Random ngày sinh
    roomWeb(page)
    time.sleep(5000)
    combobox_xpath = '//div[@aria-label="Day. Double-tap for more options"]'
    random_day= random.randint(0, 27)
    page.click(combobox_xpath)
    time.sleep(500 / 1000)
    combobox_css = f'[id="Day-options-item-{random_day}"]'
    page.click(combobox_css)
    
    # Random month()
    combobox_xpath = '//div[@aria-label="Month. Double-tap for more options"]'
    time.sleep(500 / 1000)
    random_month = random.randint(0, 11)
    page.click(combobox_xpath)
    
    combobox_css = f'[id="Month-options-item-{random_month}"]'
    page.click(combobox_css)       
    #Random year()
    combobox_xpath = '//div[@aria-label="Year. Double-tap for more options"]'
    time.sleep(500 / 1000)
    random_year = random.randint(22, 50)
    page.click(combobox_xpath)
    combobox_css = f'[id="Year-options-item-{random_year}"]'
    page.click(combobox_css)
#Autofill mass and passMail
def setup_account(page,mail_pass,process_id,lock) :
    # Setup mail and password
    global mail, passMail
    # Tách mail và pass từ dòng
    mail, passMail = mail_pass.split('|')
    print(mail_pass)
    # Xử lý mail và pass ở đây
    print(f"Profile{process_id} : Mail: {mail}, Password: {passMail}")
    passAccount = passMail+"1A@"
    page.fill('input[placeholder="Email address"]',mail)
    page.fill('input[placeholder="Password"]',passAccount)
    time.sleep(10)
    page.click('button[type="button"]:has-text("Send code")')
    time.sleep(1)
    page.click('button[type="button"]:has-text("Send code")')
    p_element = page.locator('//p[contains(text(), "You’ve already signed up")]')    
    time.sleep(5)
    if p_element.is_visible():
        print("Mail này đã được sử dụng")
        with lock:
            with open('Error.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"{mail}|{passMail}|mail đã đăng ký tài khoản tiktok\n")
        return True
    else:
        return False
 #Kiểm tra có bị maximium khi getcode hay mail đã được đăng ký tiktok chưa   
def check_send_code(page,lock):  
    span_element = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
    if span_element.is_visible():
        for i in range(10):
            try:
                #print("go here")
                time.sleep(500 / 1000)
                page.click('button[type="button"]:has-text("Send code")',timeout=10000) 
                #Check mail reg chưa
                check_signed = page.locator('//p[contains(text(), "You’ve already signed up")]')
                if check_signed.is_visible():
                        print("Mail này đã đăng ký tiktok")
                        with lock:
                          with open('Error.txt', 'a', encoding='utf-8') as error_file:
                              error_file.write(f"{mail}|{passMail}|mail đã đăng ký tài khoản tiktok\n")
                          return True
                        #break
            except Exception as e:
                print(e)
        return False
# Kiểm tra xem còn maximinum hay không sau khi spam send code
def Re_check(page,lock):
    try :
        time.sleep(2)
        return_Last_Check = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
        print("check lai lan nua : "+str(return_Last_Check.is_visible()))
        #input("check ne")
        if return_Last_Check.is_visible():
            with lock:
                with open('maximum.txt', 'a', encoding='utf-8') as maximum_file:
                    maximum_file.write(f"{mail}|{passMail}"+'\n')
            return True
        else:
            return False
    except Exception as e:
        print(f"Lỗi khi đóng file : {e}")
#check quet QR
def check_app(page,lock): 
    div_locator = page.locator('//div[contains(text(), "Continue on the TikTok app")]')
    if div_locator.is_visible():
        with lock:
            with open('QRapp.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"{mail}|{passMail}\n")
        return True
    else:
        return False
def Check_again(page):
 svg_element = page.locator('svg.tiktok-9ec6sj-StyledLoadingCircle')
 if svg_element.is_visible():
     return True
 button_locator = 'button[data-e2e="send-code-button"]'
 button = page.locator(button_locator)
 button_content = button.inner_text()
 print("Nội dung của thẻ button:", button_content)
 pattern = r"Resend code: \d+s"
 if re.match(pattern, button_content):
    print("Nội dung đúng định dạng.")
    return False
 else :
     return True
 
def Check_send(page,lock):
  for i in range(10):
    button_locator = 'button[data-e2e="send-code-button"]'
    button = page.locator(button_locator)
    button_content = button.inner_text()
    pattern = r"Resend code: \d+s"
    if re.match(pattern, button_content):
        print("đã gửi mã")
        return False
    else:
        with lock:
            with open('maximum.txt', 'a', encoding='utf-8') as maximum_file:
                maximum_file.write(f"{mail}|{passMail}"+'\n')
        return True
#Lấy thông tin code và nếu không có code thì ghi vào file error
def get_code(page,lock) :
    print(f'lấy code mail :{mail}|{passMail}')
    time.sleep(10)
    codes_result = get_code_mail(mail.strip(),passMail.strip())
    print('Codes:', codes_result)
    if codes_result is not None:     
        if codes_result['Inbox'] is not None :
            page.fill('input[placeholder="Enter 6-digit code"]',codes_result['Inbox'])
            time.sleep(1)
            page.click('button[type="submit"]:has-text("Next")')
            time.sleep(3)
            page.wait_for_load_state("load")
            span_element = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
            print(span_element.is_visible())
            if span_element.is_visible():
                for i in range(1):
                    try:
                        span_locator = page.locator('//span[contains(text(), "Verification code is expired or incorrect. Try again.")]')
                        if span_locator.is_visible():
                            get_code(page)
                        time.sleep(700 / 1000)
                        page.click('button[type="submit"]:has-text("Next")',timeout=3000) 
                    except Exception as e:
                        print(e)
                        return False         
            span_element = page.locator('//span[contains(text(), "Verification code is expired or incorrect. Try again.")]')
            print(span_element.is_visible())
            if span_element.is_visible():
                if codes_result['Junk'] is not None :
                    page.fill('input[placeholder="Enter 6-digit code"]',codes_result['Junk'])
                    time.sleep(1)
                    page.click('button[type="submit"]:has-text("Next")')
                    time.sleep(3)
                    page.wait_for_load_state("load")
                    span_element = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
                    print(span_element.is_visible())
                    if span_element.is_visible():
                        for i in range(1):
                            try:
                                span_locator = page.locator('//span[contains(text(), "Verification code is expired or incorrect. Try again.")]')
                                if span_locator.is_visible():
                                    get_code(page)
                                time.sleep(700 / 1000)
                                page.click('button[type="submit"]:has-text("Next")',timeout=3000) 
                            except Exception as e:
                                print(e)
                                return True   
        if codes_result['Junk'] is not None :
            page.fill('input[placeholder="Enter 6-digit code"]',codes_result['Junk'])
            time.sleep(1)
            page.click('button[type="submit"]:has-text("Next")')
            time.sleep(3)
            page.wait_for_load_state("load")
            span_element = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
            print(span_element.is_visible())
            if span_element.is_visible():
                for i in range(1):
                    try:
                        span_locator = page.locator('//span[contains(text(), "Verification code is expired or incorrect. Try again.")]')
                        if span_locator.is_visible():
                            get_code(page)
                        time.sleep(700 / 1000)
                        page.click('button[type="submit"]:has-text("Next")',timeout=3000) 
                    except Exception as e:
                        print(e)
                        return True 
    else:
        print('Không thể lấy được mã.')
        with lock:
            with open('Error.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"{mail}|{passMail}|mail không thể kết nối\n")
        return True   
    return False  

# vào trang chủ
def goto_site(page):
    print("Bắt đầu vào profile")
    time.sleep(10)
    try:
        page.goto('https://www.tiktok.com/')
        page.wait_for_load_state("load")
    except requests.ConnectionError:
         time.sleep(5)
         page.goto('https://www.tiktok.com/')
         page.wait_for_load_state("load")
    time.sleep(2)
    following_span = page.locator('span:has-text("Following")')
    if following_span.is_visible():
        print("loading site done")
    else :
        page.reload() 
        page.wait_for_load_state("load")
    time.sleep(2)
    try:
        page.click('#header-more-menu-icon')
        page.wait_for_selector('span:has-text("View profile")',timeout=3000)
        page.click('span:has-text("View profile")',timeout=3000)
    except Exception as e:
        page.reload() 
        page.wait_for_load_state("load")
        time.sleep(3) 
        page.click('#header-more-menu-icon')
        page.wait_for_selector('span:has-text("View profile")',timeout=3000)
        page.click('span:has-text("View profile")',timeout=3000)
    captcha_element = page.locator('.captcha-solver-info')
    check_captcha = False
    while not check_captcha:
        captcha_element = page.locator('.captcha-solver-info')
        if captcha_element.is_visible():
            print("Tiếp tục giải captcha")
            time.sleep(10)
        else :
            check_captcha = True   
#Setup profile với các thông tin name và bio với lib random
def setup_profile(page,lock):
    gender = 1
    full_name = generate(gender)
    print(f'{full_name}')
    fake = faker.Faker()
    sentence = fake.sentence()
    sentence = sentence[:80]
    print(sentence)
    #input("bypass captcha")
    page.click('span:has-text("Edit profile")')
    avt = random.randint(1, 147)
    file_path = os.path.join('avt', f'{avt}.jpg')
    input_file_element = page.locator('input[type="file"]')
    input_file_element.set_input_files(file_path)
    time.sleep(1)
    page.click('button:has-text("Apply")')
    time.sleep(1)
    username_input_value = page.locator('input[placeholder="Username"]').get_attribute('value')
    print(username_input_value)
    #input("userID")
    page.fill('input[placeholder="Name"]', full_name)
    time.sleep(700/1000)
    page.fill('textarea[placeholder="Bio"]', sentence)
    time.sleep(700/1000)
    page.click('button:has-text("Save")')
    time.sleep(1)
    page.click('button:has-text("Confirm")')
    time.sleep(10)
    page.wait_for_load_state("load")
    with lock:
      with open('Account.txt', 'a', encoding='utf-8') as done_file:
          done_file.write(f"{mail}|{passMail}|{username_input_value}|{passMail}1A@\n")
    try:
        page.goto('https://www.tiktok.com/logout')
    except requests.ConnectionError:
         time.sleep(10)
         page.goto('https://www.tiktok.com/logout')
    time.sleep(3)
    page.wait_for_load_state("load")
#Hàm xóa mail đang đọc trong file mail nếu xuất hiện lỗi
def delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass):
 try :
    with lock:
      if current_position.value <= len(mail_pass_list):
          # Ghi dữ liệu còn lại trở đi vào file
          with open('Mail.txt', 'w') as file:
              file.write('\n'.join(mail_pass_list[current_position.value:]))
          print(f"Process {process_id} deleted line: {mail_pass}")
 except ValueError as e:
      # Xử lý lỗi khi không thể tách mail và pass
      print(f"Process {process_id} encountered an error: {e}")
# Xóa profile
def delete_profile(process_id, mail_pass_list, current_position, lock,mail_pass):
    try :
        with lock:
         if current_position.value <= len(mail_pass_list):
            # Ghi dữ liệu còn lại trở đi vào file
            with open('Mail.txt', 'w') as file:
                file.write('\n'.join(mail_pass_list[current_position.value:]))
            print(f"Process {process_id} deleted line: {mail_pass}")
    except ValueError as e:
        # Xử lý lỗi khi không thể tách mail và pass
        print(f"Process {process_id} encountered an error: {e}")
# def context.clear_cookies():
#     context.clear_cookies()
def get_random_user_agent():
    file_path = 'user agent/window1.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Loại bỏ ký tự trắng và lựa chọn một User Agent ngẫu nhiên
        random_user_agent = random.choice(lines).strip()

        return random_user_agent
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn và thử lại.")


def while_loop(user_data_dir, extension_path,process_id, mail_pass_list, current_position, lock):
    try:
        while True :
                user_agent = get_random_user_agent()
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
                    page.goto('chrome-extension://ifnpembpekmnpihkkmjallnjelnfodep/popup/popup.html')
                    time.sleep(3)
                    page.fill('[placeholder="Enter subscription key"]', 'c03ca43736416de2612946d22ede7026')
                    page.click('.plan_button.save_key.clickable')
                    time.sleep(3)
                    page.goto('https://www.tiktok.com/logout')
                    time.sleep(5)
                    # page.goto('https://www.tiktok.com/@numbersV2qgd')
                    # time.sleep(15)
                    # Các thao tác khác trên trang web
                    #input("Press Enter to continue...")
                    check_file_acc(context)
                    open_browser_with_profile(page,context)  # Thay đổi ở đây
                    setup_date(page)
                    #setup_account(page)
                    if setup_account(page,mail_pass,process_id,lock):
                        #delete_Fistline()
                        context.clear_cookies()
                        page.close()
                        context.close()
                        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                        continue
                    if check_send_code(page,lock):
                        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                        context.clear_cookies()
                        page.close()
                        context.close()
                        #delete_profiles()
                        continue
                    else:
                         if Re_check(page,lock):
                              delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                              context.clear_cookies()
                              page.close()
                              context.close()
                              #delete_profiles()
                              continue 
                    #input("")
                    if Check_send(page,lock) :
                        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                        context.clear_cookies()
                        page.close()
                        context.close()
                        #delete_profiles()
                        continue
                    if get_code(page,lock):
                         delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                         page.close()
                         context.close()
                         #delete_profiles()
                         continue
                    if check_app(page,lock):
                         delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
                         page.close()
                         context.close()
                         delete_profile(process_id, mail_pass_list, current_position, lock,mail_pass)
                         continue
                    goto_site(page)
                    setup_profile(page,lock)
                    page.close()
                    context.close()
                    delete_profile(process_id, mail_pass_list, current_position, lock,mail_pass)
    except TimeoutError: 
        with lock:
            with open('maximum.txt', 'a', encoding='utf-8') as maximum_file:
                maximum_file.write(mail_pass+'\n')
        delete_Fistline(process_id, mail_pass_list, current_position, lock,mail_pass)
        while_loop(user_data_dir, extension_path,process_id, mail_pass_list, current_position, lock)              

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
        with open('Mail.txt', 'r') as file:
            mail_pass_list = [line.strip() for line in file]
            print(mail_pass_list)
    except FileNotFoundError:
        print("File 'Mail.txt' không tồn tại.")
        return

    if not mail_pass_list:
        print("File 'Mail.txt' không có dữ liệu.")
        with open('maximum.txt', 'r') as source:
            data = source.read()
            print(data)
        if not data :
            print("ssss")
            return 
        else:
            print("cherp file")
            with open('Mail.txt','w') as write_to_Mail :
                write_to_Mail.write(data)
            with open('maximum.txt', 'w') as source:
                source.write('')
            try:
                with open('Mail.txt', 'r') as file:
                    mail_pass_list = [line.strip() for line in file]
                    print(mail_pass_list)
            except FileNotFoundError:
                print("File 'Mail.txt' không tồn tại.")
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