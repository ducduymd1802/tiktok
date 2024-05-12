def remove_duplicate_user_agents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        unique_user_agents = list(set(lines))

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(unique_user_agents)

        print("Đã lọc và xóa các đoạn mã User Agent trùng lặp trong '{}'.".format(file_path))
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn và thử lại.")

# Thay thế 'user_agents.txt' bằng đường dẫn tới file của bạn
file_path = 'Error.txt'

remove_duplicate_user_agents(file_path)
