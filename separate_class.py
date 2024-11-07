'''
Dưới đây là script Python thực hiện các bước sau:

Copy các file label chứa class mà bạn đã nhập từ thư mục gốc sang hai thư mục mới: only_<class>_label và remove_<class>_label.
Chỉnh sửa nội dung file:
Trong thư mục only_<class>_label: Chỉ giữ lại các đối tượng có class đã nhập, loại bỏ các class khác.
Trong thư mục remove_<class>_label: Loại bỏ các đối tượng có class đã nhập, chỉ giữ lại các class khác.
'''

import os
import shutil
import xml.etree.ElementTree as ET

# Nhập tên class cần kiểm tra
target_class = input("Nhập class bạn muốn kiểm tra: ")

# Đường dẫn tới folder chứa các file label gốc
# label_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Train\\Label_unverify'
label_folder = 'Label_unverify'

# Tạo hai thư mục đích để lưu các file đã được xử lý
only_class_folder = f"only_{target_class}_label"
remove_class_folder = f"remove_{target_class}_label"
os.makedirs(only_class_folder, exist_ok=True)
os.makedirs(remove_class_folder, exist_ok=True)

# Duyệt qua từng file trong folder label
for filename in os.listdir(label_folder):
    file_path = os.path.join(label_folder, filename)

    # Kiểm tra nếu file là XML (Pascal VOC format)
    if filename.endswith('.xml'):
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Sao chép file sang hai thư mục đích
        only_class_file_path = os.path.join(only_class_folder, filename)
        remove_class_file_path = os.path.join(remove_class_folder, filename)
        shutil.copy(file_path, only_class_file_path)
        shutil.copy(file_path, remove_class_file_path)

        # Chỉnh sửa file trong "only_<class>_label" để chỉ giữ lại class cần tìm
        only_class_tree = ET.parse(only_class_file_path)
        only_root = only_class_tree.getroot()
        for obj in only_root.findall('object'):
            class_name = obj.find('name').text
            if class_name != target_class:
                only_root.remove(obj)
        only_class_tree.write(only_class_file_path)

        # Chỉnh sửa file trong "remove_<class>_label" để loại bỏ class cần tìm
        remove_class_tree = ET.parse(remove_class_file_path)
        remove_root = remove_class_tree.getroot()
        for obj in remove_root.findall('object'):
            class_name = obj.find('name').text
            if class_name == target_class:
                remove_root.remove(obj)
        remove_class_tree.write(remove_class_file_path)

    # Kiểm tra nếu file là TXT (YOLO format)
    elif filename.endswith('.txt'):
        # Sao chép file sang hai thư mục đích
        only_class_file_path = os.path.join(only_class_folder, filename)
        remove_class_file_path = os.path.join(remove_class_folder, filename)
        shutil.copy(file_path, only_class_file_path)
        shutil.copy(file_path, remove_class_file_path)

        # Đọc các dòng trong file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Ghi các dòng chỉ chứa class cần tìm vào file "only_<class>_label"
        only_class_lines = [line for line in lines if line.split()[0] == target_class]
        with open(only_class_file_path, 'w') as only_file:
            only_file.writelines(only_class_lines)

        # Ghi các dòng không chứa class cần tìm vào file "remove_<class>_label"
        remove_class_lines = [line for line in lines if line.split()[0] != target_class]
        with open(remove_class_file_path, 'w') as remove_file:
            remove_file.writelines(remove_class_lines)

print(f"Đã xử lý các file chứa class '{target_class}' và sao chép vào thư mục '{only_class_folder}' và '{remove_class_folder}'.")
