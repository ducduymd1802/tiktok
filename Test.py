from playwright.sync_api import sync_playwright
import time
import random
import os
from pop3_imap import get_verification_code
from vn_fullname_generator.generator import generate
import faker
from playwright.async_api import async_playwright
import asyncio

# Hàm mở profile và add ext bypasss captcha
def open_browser_with_profile(page,context):
    # with sync_playwright() as p:
    #     # Mở trình duyệt với profile đã cung cấp
    #     context = p.chromium.launch_persistent_context(
    #         user_data_dir,
    #         headless=False,
    #         args=[
    #             f"--disable-extensions-except={extension_path}",
    #             f"--load-extension={extension_path}",
    #         ],
    #     )
        
    #     # Thực hiện các thao tác trên trang web (nếu cần)
    #     page = context.new_page()
    #     page.goto('chrome-extension://ifnpembpekmnpihkkmjallnjelnfodep/popup/popup.html')
    #     # Thực hiện điền api
    #     # page.fill('[type="text"]','3f1e391ca82b66be57762c71be648a47')
    #     page.fill('[placeholder="Enter subscription key"]', 'c03ca43736416de2612946d22ede7026')
    #     time.sleep(1)
    #     page.click('.plan_button.save_key.clickable')

        # Xóa page[0]
        pages = context.pages
        if len(pages) > 3:
            pages[0].close()

        # Chuyển tới trang đăng ký
        page.goto('https://www.tiktok.com/signup/phone-or-email/email')
        page.wait_for_load_state("load")
        time.sleep(2)
        input("")
        return page
    
def check_file_acc() :
    if not os.path.isfile("mail.txt"):
            print("Tệp 'mail.txt' không tồn tại.")
            input("Nhấn Enter để kết thúc ......")
            exit(1)
    elif os.path.getsize("mail.txt") == 0:
            print("Tệp 'mail.txt' không có dữ liệu.")
            input("Nhấn Enter để kết thúc ......")
            exit(1)
# Setup random date
def setup_date(page):
    #Random ngày sinh
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
def setup_account(page) :
    # Setup mail and password
    global mail, passMail
    with open('mail.txt','r') as file:
        first_line= file.readline()
    mail, passMail = first_line.strip().split('|')
    print(f"{mail}|{passMail} | 1")
    passAccount = passMail+"A@"
    page.fill('input[placeholder="Email address"]',mail)
    page.fill('input[placeholder="Password"]',passAccount)
    time.sleep(1)
    page.click('button[type="button"]:has-text("Send code")')
    time.sleep(1)
    page.click('button[type="button"]:has-text("Send code")')
    p_element = page.locator('//p[contains(text(), "You’ve already signed up")]')    
    time.sleep(5)
    if p_element.is_visible():
        print("Mail này đã được sử dụng")
        delete_Fistline()
        with open('Error.txt', 'a', encoding='utf-8') as error_file:
            error_file.write(f"{mail}|{passMail}|mail đã đăng ký tài khoản tiktok\n")
        return True
    else:
        return False
 #Kiểm tra có bị maximium khi getcode hay mail đã được đăng ký tiktok chưa   
def check_send_code(page):  
    check_send_code_flag = False
    span_element = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
    if span_element.is_visible():
        for i in range(10):
            try:
                print("go here")
                time.sleep(500 / 1000)
                page.click('button[type="button"]:has-text("Send code")',timeout=5000) 
                #Check mail reg chưa
                check_signed = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
                if check_signed.is_visible():
                        check_send_code_flag = True
                        break
                else:
                        check_send_code_flag = False
            except Exception as e:
                print(f"An error occurred in the loop: {e}")
                break
            check_send_code_flag = page.locator('//p[contains(text(), "You’ve already signed up")]')  
            if check_send_code_flag.is_visible() :
                print("Mail này đã được sử dụng")
                delete_Fistline()
                with open('Error.txt', 'a', encoding='utf-8') as error_file:
                    error_file.write(f"{mail}|{passMail}|mail đã đăng ký tài khoản tiktok\n")

    time.sleep(5)
    return_Last_Check = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
    print(return_Last_Check.is_visible())
    #input("check ne")
    if return_Last_Check.is_visible():
        with open('maximum.txt', 'a', encoding='utf-8') as maximum_file:
            maximum_file.write(f"{mail}|{passMail}\n")
        return True
    else:
        return False

#Lấy thông tin code và nếu không có code thì ghi vào file error
def get_code(context,page) :
    print(f'day la mai :{mail}|{passMail}ne')
    code = get_verification_code(mail.strip(),passMail.strip(),30)
    print(f'code : {code}')
    if code is None or len(code) > 6:
        context.close()
        with open('Error.txt', 'a', encoding='utf-8') as error_file:
            error_file.write(f"{mail}|{passMail}|mail sai hoặc die\n")
        delete_Fistline()
    else :
        page.fill('input[placeholder="Enter 6-digit code"]',code)
        time.sleep(1)
        page.click('button[type="submit"]:has-text("Next")')
        time.sleep(3)
        page.wait_for_load_state("load")
        span_element = page.locator('//span[contains(text(), "Maximum number of attempts reached. Try again later.")]')
        print(span_element.is_visible())
        if span_element.is_visible():
            for i in range(30):
                try:
                    time.sleep(700 / 1000)
                    page.click('button[type="submit"]:has-text("Next")',timeout=3000) 
                except Exception as e:
                    break
#Setup profile với các thông tin name và bio với lib random
def setup_profile(page):
    gender = 1
    full_name = generate(gender)
    print(f'{full_name}')
    fake = faker.Faker()
    sentence = fake.sentence()
    sentence = sentence[:80]
    print(sentence)
    #input("bypass captcha")
    page.click('span:has-text("Edit profile")')
    avt = random.randint(1, 50)
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
    page.click('button:has-text("Confirm")')
    with open('Account.txt', 'a', encoding='utf-8') as done_file:
        done_file.write(f"{mail}|{passMail}|{username_input_value}|{passMail}A@\n")
    delete_Fistline()
    page.goto('https://www.tiktok.com/logout')
    time.sleep(3)
    page.wait_for_load_state("load")
#Hàm xóa mail đang đọc trong file mail nếu xuất hiện lỗi
def delete_Fistline():
    with open('mail.txt', 'r') as file:
            lines = file.readlines()
    with open('mail.txt', 'w') as file:
            file.writelines(lines[1:])


def while_loop(user_data_dir, extension_path):
    run = True
    while run :
        try :
            with sync_playwright() as p:
            # Mở trình duyệt với profile đã cung cấp
                context = p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=False,
                    args=[
                        f"--disable-extensions-except={extension_path}",
                        f"--load-extension={extension_path}",
                    ],
                )
            page = context.new_page()
            page.goto('chrome-extension://ifnpembpekmnpihkkmjallnjelnfodep/popup/popup.html')
            # Thực hiện điền api
            # page.fill('[type="text"]','3f1e391ca82b66be57762c71be648a47')
            page.fill('[placeholder="Enter subscription key"]', 'c03ca43736416de2612946d22ede7026')
            time.sleep(1)
            page.click('.plan_button.save_key.clickable')    
            #open_browser_with_profile(page,context)
        except Exception as e:
            print(f"An error occurred: {e}")
        # Thực hiện các thao tác trên trang web (nếu cần)
        
        input("")
        
        check_file_acc()
        page = open_browser_with_profile(user_data_dir, extension_path) 
        print(page)
        input("")
        setup_date(page)
        setup_account(page)
        if setup_account(page) :
             exit(0)
        else:
             input("ket thuc chuong trinh")
             exit(0)

if __name__ == "__main__":
    user_data_dir = r"F:\Tool PY\AuToRegTT\user_profile\profile"
    extension_path = r"F:\Tool PY\AuToRegTT\extension\Achi"
    while_loop(user_data_dir, extension_path)
    #open_browser_with_profile(user_data_dir, extension_path)