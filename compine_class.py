import os
import shutil
import xml.etree.ElementTree as ET

# Nhập tên class cần hợp nhất
target_class = input("Nhập class bạn muốn hợp nhất: ")

# Đường dẫn tới hai thư mục đã tách trước đó
only_class_folder = f"only_{target_class}_label"
remove_class_folder = f"remove_{target_class}_label"

# Thư mục mới để lưu trữ các file đã hợp nhất
verified_folder = "verified_label"
os.makedirs(verified_folder, exist_ok=True)

# Duyệt qua từng file trong thư mục chỉ chứa class
for filename in os.listdir(only_class_folder):
    only_class_file_path = os.path.join(only_class_folder, filename)
    remove_class_file_path = os.path.join(remove_class_folder, filename)
    verified_file_path = os.path.join(verified_folder, filename)

    # Kiểm tra nếu file là XML (Pascal VOC format)
    if filename.endswith('.xml'):
        # Tạo cây XML từ file "chỉ chứa class" và "loại bỏ class"
        only_class_tree = ET.parse(only_class_file_path)
        only_root = only_class_tree.getroot()

        if os.path.exists(remove_class_file_path):
            remove_class_tree = ET.parse(remove_class_file_path)
            remove_root = remove_class_tree.getroot()

            # Hợp nhất các đối tượng từ file "loại bỏ class" vào file "chỉ chứa class"
            for obj in remove_root.findall('object'):
                only_root.append(obj)

        # Lưu file hợp nhất vào thư mục verified_label
        only_class_tree.write(verified_file_path)

    # Kiểm tra nếu file là TXT (YOLO format)
    elif filename.endswith('.txt'):
        # Đọc các dòng từ cả hai file
        with open(only_class_file_path, 'r') as only_file:
            only_class_lines = only_file.readlines()
        
        if os.path.exists(remove_class_file_path):
            with open(remove_class_file_path, 'r') as remove_file:
                remove_class_lines = remove_file.readlines()
        else:
            remove_class_lines = []

        # Hợp nhất các dòng và loại bỏ các dòng trùng lặp
        combined_lines = only_class_lines + remove_class_lines
        combined_lines = list(dict.fromkeys(combined_lines))  # Loại bỏ trùng lặp

        # Ghi file hợp nhất vào thư mục verified_label
        with open(verified_file_path, 'w') as verified_file:
            verified_file.writelines(combined_lines)

print(f"Tất cả các file đã được hợp nhất và lưu vào thư mục '{verified_folder}'.")
