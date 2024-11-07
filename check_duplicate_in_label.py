'''
Dưới đây là một script giúp bạn tìm các file label có chứa hơn 2 đối tượng của một class mà bạn nhập vào. 
Script này sẽ kiểm tra từng file trong folder và đếm số lần xuất hiện của class đó. Nếu số lượng vượt quá 2, tên file sẽ được liệt kê.
'''

import os
import xml.etree.ElementTree as ET

# Enter the class name you want to check for
target_class = input("Enter the class you want to check for: ")

# Path to the folder containing labeled files
label_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Train\\Label_unverify'

# List to store files with more than 2 instances of the desired class
files_with_multiple_class = []

# Check each file in the folder
for filename in os.listdir(label_folder):
    class_count = 0  # Count the number of the specified class in each file

    # For XML files (Pascal VOC format)
    if filename.endswith('.xml'):
        filepath = os.path.join(label_folder, filename)
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Count occurrences of the class in the XML file
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name == target_class:
                class_count += 1

    # For TXT files (YOLO format)
    elif filename.endswith('.txt'):
        filepath = os.path.join(label_folder, filename)
        with open(filepath, 'r') as file:
            for line in file:
                class_id = line.split()[0]  # Extract the class ID from the line
                if class_id == target_class:
                    class_count += 1

    # If the file has more than 2 instances of the desired class, add it to the list
    if class_count > 2:
        files_with_multiple_class.append(filename)

# Display files with more than 2 instances of the desired class
if files_with_multiple_class:
    print(f"Files with more than 2 instances of the class '{target_class}':")
    for file in files_with_multiple_class:
        print(file)
else:
    print(f"No files contain more than 2 instances of the class '{target_class}'.")
