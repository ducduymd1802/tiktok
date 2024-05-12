import poplib
import re
from email import parser
import time

# Thông tin tài khoản email
pop3_server = "outlook.office365.com"

# Số lần thử lại


def get_verification_code(email_address,password,max_retries):
    # Vòng lặp để thử lại
    for attempt in range(max_retries):
        try:
            # Kết nối đến email server qua POP3
            mail = poplib.POP3_SSL(pop3_server)
            mail.user(email_address)
            mail.pass_(password)

            # Lấy số lượng email trong hộp thư
            email_count = len(mail.list()[1])

            # Lấy nội dung của email mới nhất
            if email_count > 0:
                email_index = email_count  # Lấy email mới nhất
                raw_email = mail.retr(email_index)[1]

                # Chuyển dữ liệu email thành một chuỗi văn bản
                email_data = b"\n".join(raw_email)

                # Parse email
                msg = parser.BytesParser().parsebytes(email_data)

                # Trích xuất nội dung email
                email_body = msg.get_payload()

                # Sử dụng regex để tìm mã gồm 6 chữ số
                code_pattern = r"\d{6}"  # Biểu thức chính quy để tìm 6 chữ số liên tiếp
                match = re.search(code_pattern, email_body)

                if match:
                    verification_code = match.group()
                    print(f"Mã xác minh: {verification_code}")
                    return verification_code  # Trả về mã xác minh nếu tìm thấy
                else:
                    print("Không tìm thấy mã xác minh trong email.")
            else:
                print("Không có email trong hộp thư.")
                break  # Nếu không có email, thoát khỏi vòng lặp

        except Exception as e:
            #print(f"Lỗi: {e}")
            if attempt < max_retries - 1:
                #print(f"Thử lại sau 2 giây (Lần thử lại thứ {attempt + 1}/{max_retries})")
                time.sleep(500/1000)
            else:
                print("Đã hết số lần thử lại. Không thể kết nối hoặc có lỗi khác.")

        finally:
            # Đóng kết nối POP3 trong mọi trường hợp
            try:
                mail.quit()
            except:
                pass

# Gọi hàm để lấy mã xác minh
email_address = "vanzjinxia@hotmail.com"
password = "dtXB3HzKz"
max_retries = 1
result = get_verification_code(email_address,password,max_retries)

# Thực hiện các hành động khác với giá trị `result` nếu cần
