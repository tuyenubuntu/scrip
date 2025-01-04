'''Đoạn mã Python này được thiết kế để kiểm tra xem một lớp mục tiêu cụ thể có tồn tại trong các tệp nhãn XML hoặc TXT trong một thư mục đã chỉ định hay không. Dưới đây là mô tả chức năng của nó:

Yêu cầu lớp mục tiêu: Đoạn mã trước tiên yêu cầu người dùng nhập tên của lớp mà họ muốn kiểm tra.

Chỉ định đường dẫn thư mục: Thư mục chứa các tệp nhãn được chỉ định trong biến label_folder. Đoạn mã sẽ tìm kiếm trong thư mục này để tìm bất kỳ tệp XML hoặc TXT nào.

Khởi tạo danh sách: Một danh sách, files_without_class, được khởi tạo để lưu tên của các tệp không chứa lớp mục tiêu.

Lặp qua các tệp: Đối với mỗi tệp trong thư mục:

Nếu tệp có phần mở rộng .xml (định dạng Pascal VOC):
Đoạn mã phân tích cú pháp XML và kiểm tra từng phần tử <object> để xem liệu target_class có xuất hiện trong thẻ <name> hay không.
Nếu tệp có phần mở rộng .txt (định dạng YOLO):
Đoạn mã đọc từng dòng, trích xuất ID của lớp (phần tử đầu tiên trong mỗi dòng). Nếu bất kỳ ID lớp nào khớp với target_class, cờ sẽ được bật.
Kiểm tra và lưu kết quả:

Nếu lớp mục tiêu được tìm thấy trong tệp, một cờ (file_has_class) sẽ được đặt thành True.
Nếu cờ vẫn là False sau khi kiểm tra, tên của tệp sẽ được thêm vào danh sách files_without_class.
Hiển thị kết quả:

Nếu bất kỳ tệp nào thiếu lớp mục tiêu, tên của chúng sẽ được hiển thị.
Nếu tất cả các tệp đều chứa lớp mục tiêu, một thông báo sẽ được hiển thị để thông báo.'''

import os
import xml.etree.ElementTree as ET

# Enter the target class name to check
target_class = input("Enter the class you want to check for: ")

# Path to the folder containing labeled files
label_folder = 'main_label\patch1\labels'

# List to store files that do not contain the desired class
files_without_class = []

# Check each file in the folder
for filename in os.listdir(label_folder):
    file_has_class = False  # Flag if the file contains the desired class

    # For XML file (Pascal VOC format)
    if filename.endswith('.xml'):
        filepath = os.path.join(label_folder, filename)
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Check if the class appears in the XML file
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name == target_class:
                file_has_class = True
                break

    # For TXT file (YOLO format)
    elif filename.endswith('.txt'):
        filepath = os.path.join(label_folder, filename)
        with open(filepath, 'r') as file:
            for line in file:
                class_id = line.split()[0]  # Get the class ID from the line
                if class_id == target_class:
                    file_has_class = True
                    break

    # If the file does not contain the desired class, add it to the list
    if not file_has_class:
        files_without_class.append(filename)

# Display files that do not contain the desired class
if files_without_class:
    print(f"Files without the class '{target_class}':")
    for file in files_without_class:
        print(file)
else:
    print(f"All files contain the class '{target_class}'.")
