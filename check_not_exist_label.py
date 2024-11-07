''''
Dưới đây là script giúp bạn tìm ra các file label không chứa một class mà bạn nhập vào. 
Script sẽ duyệt qua tất cả các file trong folder và kiểm tra xem class có xuất hiện trong mỗi file hay không. Nếu không, tên file đó sẽ được liệt kê.
'''
import os
import xml.etree.ElementTree as ET

# Enter the class name you want to check for
target_class = input("Enter the class you want to check for: ")

# Path to the folder containing labeled files
label_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Train\\Label_unverify'

# List to store files that do not contain the desired class
files_without_class = []

# Check each file in the folder
for filename in os.listdir(label_folder):
    file_has_class = False  # Flag to indicate if the file contains the desired class

    # For XML files (Pascal VOC format)
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

    # For TXT files (YOLO format)
    elif filename.endswith('.txt'):
        filepath = os.path.join(label_folder, filename)
        with open(filepath, 'r') as file:
            for line in file:
                class_id = line.split()[0]  # Extract the class ID from the line
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
