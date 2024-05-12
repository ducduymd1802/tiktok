import multiprocessing
import time
import random

def process_data(process_id, mail_pass_list, current_position, lock):
    while True:
        with lock:
            if current_position.value >= len(mail_pass_list):
                break

            mail_pass = mail_pass_list[current_position.value]
            current_position.value += 1

        try:
            # Tách mail và pass từ dòng
            mail, password = mail_pass.split('|')

            # Xử lý mail và pass ở đây
            print(f"Process {process_id} processing: Mail: {mail}, Password: {password}")

            # Thêm thời gian ngẫu nhiên từ 1 đến 5 giây
            sleep_time = random.uniform(1, 5)
            time.sleep(sleep_time)

            # Xóa dòng vừa đọc
            with lock:
                if current_position.value <= len(mail_pass_list):
                    # Ghi dữ liệu còn lại trở đi vào file
                    with open('maximum.txt', 'w') as file:
                        file.write('\n'.join(mail_pass_list[current_position.value:]))
                    print(f"Process {process_id} deleted line: {mail_pass}")
        except ValueError as e:
            # Xử lý lỗi khi không thể tách mail và pass
            print(f"Process {process_id} encountered an error: {e}")

def main():
    try:
        with open('maximum.txt', 'r') as file:
            mail_pass_list = [line.strip() for line in file]
            print(mail_pass_list)
            input("")
    except FileNotFoundError:
        print("File 'maximum.txt' not found. Exiting.")
        return

    if not mail_pass_list:
        print("File 'maximum.txt' is empty. Exiting.")
        return

    current_position = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()

    num_processes = 10
    processes = []

    for i in range(num_processes):
        process = multiprocessing.Process(target=process_data, args=(i, mail_pass_list, current_position, lock))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()
