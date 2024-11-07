'''
Script trên sẽ đếm tất cả các đối tượng của mỗi class trong từng file chứ không chỉ lấy một đối tượng duy nhất cho mỗi class. 
Nghĩa là nếu một file label có nhiều đối tượng cùng class (ví dụ: 3 xe ô tô), script sẽ đếm tất cả 3 đối tượng này và tăng số lượng của class tương ứng.

Tóm lại:

Mỗi đối tượng trong mỗi file đều được đếm.
Nếu một file có nhiều đối tượng của cùng một class, tất cả đều sẽ được cộng vào tổng số.
Nếu bạn muốn đếm số lượng file có chứa mỗi class (tức là đếm file, không phải tổng số đối tượng của từng class), hãy cho mình biết.
'''
import os
import xml.etree.ElementTree as ET
from collections import Counter

# Path to the folder containing the labeled files
label_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Train\\Label_unverify'
class_counts = Counter()

# Check each file in the folder
for filename in os.listdir(label_folder):
    # Case for XML file (Pascal VOC format)
    if filename.endswith('.xml'):
        filepath = os.path.join(label_folder, filename)
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Loop through all objects and count the class name
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_counts[class_name] += 1

    # Case for TXT file (YOLO format)
    elif filename.endswith('.txt'):
        filepath = os.path.join(label_folder, filename)
        with open(filepath, 'r') as file:
            for line in file:
                # Each line has the format: class_id x_center y_center width height
                class_id = line.split()[0]  # Get the class ID from the line
                class_counts[class_id] += 1

# Display the distribution of classes
for class_name, count in class_counts.items():
    print(f"Class '{class_name}': {count} instances")
