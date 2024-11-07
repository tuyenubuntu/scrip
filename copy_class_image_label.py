'''
copy label file and image with specified class
'''


import os
import shutil
import xml.etree.ElementTree as ET

# Enter the target class name
target_class = input("Enter the class you want to search for: ")

# Path to the folder containing label and image files
label_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Train\\Label_unverify'
image_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Train\\Image_raw'  # Path to the image folder (Update if needed)

# Create a new folder to save copied files, named as class + '_label'
output_folder_label = f"{target_class}_label"
output_folder_image = f"{target_class}_image"

os.makedirs(output_folder_label, exist_ok=True)
os.makedirs(output_folder_image, exist_ok=True)

# Counter for the number of files copied
copied_files_count = 0

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

    # If the file contains the desired class, copy it to the new folder
    if file_has_class:
        # Copy the label file
        shutil.copy(filepath, output_folder_label)
        
        # Check and copy the corresponding image file with the same name
        image_filename = filename.replace('.xml', '.jpg')  # Change extension if needed (e.g., .png, .jpeg)
        image_filepath = os.path.join(image_folder, image_filename)
        
        # If the image exists, copy it
        if os.path.exists(image_filepath):
            shutil.copy(image_filepath, output_folder_image)
        
        copied_files_count += 1

# Print the number of copied files
print(f"Copied {copied_files_count} files containing the class '{target_class}' to the folder '{output_folder_label}'.")
print(f"Copied {copied_files_count} files containing the class '{target_class}' to the folder '{output_folder_image}'.")
