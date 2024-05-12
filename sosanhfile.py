import random
import re

def replace_user_agents_in_place(file_path, user_agents_file_path):
    # Đọc danh sách các user agent từ tệp user_agents_file
    with open(user_agents_file_path, 'r') as f:
        user_agents = f.read().splitlines()

    # Đọc nội dung từ tệp
    with open(file_path, 'r') as f:
        content = f.read()

    # Tìm và thay thế các vị trí User Agent trong nội dung
    pattern = re.compile(r'(User-Agent: )(.+)')
    replaced_content = pattern.sub(lambda x: x.group(1) + random.choice(user_agents), content)

    # Ghi nội dung đã thay đổi trở lại vào tệp
    with open(file_path, 'w') as f:
        f.write(replaced_content)

# Sử dụng hàm replace_user_agents_in_place với các tham số tương ứng
file_path = 'user agent/window1.txt'
user_agents_file_path = 'user agent/window.txt'

replace_user_agents_in_place(file_path, user_agents_file_path)
