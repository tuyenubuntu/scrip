import os
import random
import shutil
import xml.etree.ElementTree as ET

# Đường dẫn đến thư mục chứa ảnh và nhãn
image_dir = "data/model-element/image"
label_dir = "data/model-element/label"
annotation_dir = "data/model-element/Annotations"
jpeg_images_dir = "data/model-element/JPEGImages"
imageset_dir = "data/model-element/ImageSets/Main"
os.makedirs(imageset_dir, exist_ok=True)

# Tạo thư mục Annotations nếu chưa tồn tại
os.makedirs(annotation_dir, exist_ok=True)

# Tỷ lệ phân chia cho train, val, test
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Lấy danh sách tất cả các file ảnh
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Trộn ngẫu nhiên danh sách ảnh
random.shuffle(image_files)

# Tính toán số lượng ảnh cho mỗi tập
total_images = len(image_files)
train_count = int(total_images * train_ratio)
val_count = int(total_images * val_ratio)
test_count = total_images - train_count - val_count

# Chia ảnh thành các tập train, val, test
train_files = image_files[:train_count]
val_files = image_files[train_count:train_count + val_count]
test_files = image_files[train_count + val_count:]

# Ghi danh sách vào các file .txt (không có phần mở rộng .xml)
def write_list_to_file(file_list, filename):
    with open(filename, 'w') as f:
        for item in file_list:
            f.write(f"{os.path.splitext(item)[0]}\n")  # Loại bỏ phần mở rộng

write_list_to_file(train_files, "data/model-element/ImageSets/Main/train.txt")
write_list_to_file(val_files, "data/model-element/ImageSets/Main/val.txt")
write_list_to_file(test_files, "data/model-element/ImageSets/Main/test.txt")

# Sao chép các file .xml từ label sang Annotations
xml_files = [f for f in os.listdir(label_dir) if f.endswith('.xml')]
for xml_file in xml_files:
    src_path = os.path.join(label_dir, xml_file)
    dest_path = os.path.join(annotation_dir, xml_file)
    shutil.copy(src_path, dest_path)

# Sao chép các file ảnh từ image sang JPEGImages
for image_file in image_files:
    src_path = os.path.join(image_dir, image_file)
    dest_path = os.path.join(jpeg_images_dir, image_file)
    shutil.copy(src_path, dest_path)

# Trích xuất tên class từ các file .xml và lưu vào labels.txt
class_names = set()

for xml_file in xml_files:
    tree = ET.parse(os.path.join(annotation_dir, xml_file))
    root = tree.getroot()
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        class_names.add(class_name)

# Ghi các class vào labels.txt
with open("data/model-element/labels.txt", 'w') as f:
    for class_name in sorted(class_names):
        f.write(f"{class_name}\n")

# Kết hợp train và val để tạo file trainval.txt
trainval_files = train_files + val_files
trainval_files = [os.path.splitext(f)[0] for f in trainval_files]

# Ghi vào file trainval.txt
with open(os.path.join(imageset_dir, "trainval.txt"), 'w') as f:
    for item in trainval_files:
        f.write(f"{item}\n")

print(f"Đã sao chép {len(image_files)} file ảnh vào thư mục JPEGImages")
print(f"Đã sao chép {len(xml_files)} file .xml vào thư mục Annotations")
print(f"Đã lưu {train_count} ảnh vào train.txt")
print(f"Đã lưu {val_count} ảnh vào val.txt")
print(f"Đã lưu {test_count} ảnh vào test.txt")
print(f"Đã tạo file trainval.txt với {len(trainval_files)} mục.")
print(f"Đã xuất {len(class_names)} lớp vào labels.txt")
