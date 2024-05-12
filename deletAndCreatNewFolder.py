import os
import shutil

#def delete_profiles(folder_path,sl):
folder_path = "user_profile"
sl='10'
def delete_profiles():
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            # Xóa toàn bộ nội dung của thư mục "user_profile"
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            print("Đã xóa tất cả profile")
            
            # Tạo thư mục có tên "profile1" đến "profile" + sl

            for i in range(1, int(sl)+1):
                new_profile_folder = os.path.join(folder_path, f"profile{i}")
                os.makedirs(new_profile_folder)
            
            print("Đã tạo "+ sl +" thư mục profile mới.")
        except Exception as e:
            print(f"Lỗi khi xóa nội dung và tạo thư mục: {e}")
    else:
        print("Thư mục không tồn tại hoặc không phải là một thư mục.")

if __name__ == "__main__":
    #folder_path = "user_profile"
    #sl=5
    #delete_profiles(folder_path,sl)
    delete_profiles()

