import os
import shutil
import xml.etree.ElementTree as ET

# Thư mục chứa ảnh và file label
image_folder = "main_label/patch1/images"  # Thay bằng đường dẫn thư mục ảnh
label_folder = "main_label/patch1/labels"  # Thay bằng đường dẫn thư mục label
output_folder = "main_label/patch1/images_no_label"  # Thư mục để lưu ảnh không hợp lệ

# Định dạng ảnh và nhãn
image_extensions = [".jpg", ".png", ".jpeg", ".bmp"]
label_extension = ".xml"

# Tạo thư mục output nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Hàm kiểm tra file label có chứa class không
def has_class_in_xml(label_path):
    try:
        tree = ET.parse(label_path)
        root = tree.getroot()
        # Kiểm tra nếu có ít nhất một thẻ <object>
        return root.find("object") is not None
    except ET.ParseError:
        print(f"Lỗi khi đọc file XML: {label_path}")
        return False

# Lọc và xử lý các ảnh không hợp lệ
def process_images(image_folder, label_folder, output_folder):
    for image_file in os.listdir(image_folder):
        if any(image_file.endswith(ext) for ext in image_extensions):
            image_path = os.path.join(image_folder, image_file)
            label_name = os.path.splitext(image_file)[0] + label_extension
            label_path = os.path.join(label_folder, label_name)

            # Kiểm tra nếu không có label hoặc label không có class
            if not os.path.exists(label_path):
                # Copy ảnh không có label vào thư mục output
                output_image_path = os.path.join(output_folder, image_file)
                shutil.copy(image_path, output_image_path)
                print(f"Đã copy file ảnh không có label: {output_image_path}")
            elif not has_class_in_xml(label_path):
                # Xóa file label không có class
                os.remove(label_path)
                print(f"Đã xóa file label không có class: {label_path}")
                
                # Copy ảnh tương ứng vào thư mục output
                output_image_path = os.path.join(output_folder, image_file)
                shutil.copy(image_path, output_image_path)
                print(f"Đã copy file ảnh có label không có class: {output_image_path}")

# Chạy hàm xử lý
process_images(image_folder, label_folder, output_folder)
print("\nHoàn thành việc xử lý các file không hợp lệ.")
