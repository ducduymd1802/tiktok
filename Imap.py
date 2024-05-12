import imaplib
import re

# Thay thế thông tin này bằng thông tin của bạn
YOUR_IMAP_SERVER = 'outlook.office365.com'
codes = {'Inbox': None, 'Junk': None}

def get_latest_email_id(imap, folder):
    status, emails = imap.search(None, '(ALL)')

    if status == 'OK':
        if emails[0]:  # Kiểm tra xem danh sách emails không rỗng
            return emails[0].split()[-1]
        else:
            print('Không tìm thấy email nào trong thư mục', folder)
            return None
    else:
        print('Lỗi lấy email mới nhất trong thư mục', folder)
        return None


def find_code_6_digits(text):
    # Sử dụng regex để tìm đoạn code 6 số đầu tiên trong text
    match = re.search(r"(\b\d{6}\b)", text)
    if match:
        return match.group()
    else:
        return None


def get_email_text(imap, email_id):
    status, email_data = imap.fetch(email_id, '(BODY[TEXT])')  # Chỉ lấy phần text

    if status == 'OK':
        return email_data[0][1].decode('utf-8')
    else:
        print(f'Lỗi lấy dữ liệu email ID {email_id}')
        return None


def get_code_mail(YOUR_EMAIL, YOUR_PASSWORD):
    try:
        imap = imaplib.IMAP4_SSL(YOUR_IMAP_SERVER)
        imap.login(YOUR_EMAIL, YOUR_PASSWORD)

        # Lấy email mới nhất từ hộp thư đến
        imap.select('Inbox')
        inbox_id = get_latest_email_id(imap, 'Inbox')
        if inbox_id:
            message = get_email_text(imap, inbox_id)
            if message:
                matches = find_code_6_digits(message)

                if matches:
                    print('Email ID (Inbox):', inbox_id)
                    print('Đoạn code 6 số:', matches)
                    codes['Inbox'] = matches

        # Lấy email mới nhất từ thư rác
        imap.select('Junk')
        junk_id = get_latest_email_id(imap, 'Junk')
        if junk_id:
            message = get_email_text(imap, junk_id)
            if message:
                matches = find_code_6_digits(message)

                if matches:
                    print('Email ID (Junk):', junk_id)
                    print('Đoạn code 6 số:', matches)
                    codes['Junk'] = matches

        if codes['Inbox'] is None and codes['Junk'] is None:
            print('Không tìm thấy đoạn code 6 số trong Inbox hoặc Junk')
            return None

        return codes
    except Exception as e:
        # print(f"Lỗi: {e}")
        print("Mail die hoặc đã không chính xác.")
    finally:
        # Đóng kết nối POP3 trong mọi trường hợp
        try:
            imap.close()
        except Exception as e:
            # print(f"Lỗi: {e}")
            pass

if __name__ == '__main__':
    YOUR_EMAIL = 'klneilllkksanchez7529@hotmail.com'
    YOUR_PASSWORD = 'TpLs2sRJ4'
    codes_result = get_code_mail(YOUR_EMAIL, YOUR_PASSWORD)

    # Sử dụng codes ở đây hoặc truyền cho hàm khác
    if codes_result is not None:
        print('Codes:', codes_result)
        print('Inbox code:', codes_result['Inbox'])
        print('Junk code:', codes_result['Junk'])
    else:
        print('Không thể lấy được mã.')
