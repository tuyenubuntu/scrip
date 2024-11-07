import os
import shutil
import xml.etree.ElementTree as ET

# Enter the target class name to remove
target_class = input("Enter the class you want to remove: ")

# Paths to the folder containing the label files
label_folder = 'Label_unverify'

# Create a new folder to save the modified label files, named as class + '_label'
output_folder = f"{target_class}_label"
os.makedirs(output_folder, exist_ok=True)

# Process each file in the label folder
for filename in os.listdir(label_folder):
    # Skip non-label files
    if not (filename.endswith('.xml') or filename.endswith('.txt')):
        continue

    filepath = os.path.join(label_folder, filename)
    modified = False  # Track if file was modified

    # Case 1: XML file (Pascal VOC format)
    if filename.endswith('.xml'):
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Find and remove target class objects
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name == target_class:
                root.remove(obj)
                modified = True

        # If modified, save to new folder
        if modified:
            output_path = os.path.join(output_folder, filename)
            tree.write(output_path)

    # Case 2: TXT file (YOLO format)
    elif filename.endswith('.txt'):
        lines_to_keep = []
        
        # Read lines and filter out target class
        with open(filepath, 'r') as file:
            for line in file:
                class_id = line.split()[0]
                if class_id != target_class:
                    lines_to_keep.append(line)
                else:
                    modified = True

        # If modified, write remaining lines to new file
        if modified:
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w') as output_file:
                output_file.writelines(lines_to_keep)

print(f"All modified label files saved to '{output_folder}' without the class '{target_class}'.")
