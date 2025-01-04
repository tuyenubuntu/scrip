import os
import xml.etree.ElementTree as ET

# Enter the class name to be replaced and the new class name
old_class = input("Enter the class you want to rename: ")
new_class = input("Enter the new name for the class: ")

# Path to the folder containing the label files
#label_folder = 'Label_unverify'
label_folder = 'C:\\Users\\rbu1hc\\OneDrive - Bosch Group\\AI Model Development\\Data\\Test\\labels_Tuyen'
# label_folder = input('Input labels folder:')

# Process each file in the label folder
for filename in os.listdir(label_folder):
    # Flag to check if a file was modified
    modified = False

    # Case 1: XML file (Pascal VOC format)
    if filename.endswith('.xml'):
        filepath = os.path.join(label_folder, filename)
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Find and replace the class name
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name == old_class:
                obj.find('name').text = new_class
                modified = True

        # If modified, save changes to the XML file
        if modified:
            tree.write(filepath)
            print(f"Updated class name in '{filename}' from '{old_class}' to '{new_class}'.")

    # Case 2: TXT file (YOLO format)
    elif filename.endswith('.txt'):
        filepath = os.path.join(label_folder, filename)
        lines_to_write = []

        # Read and replace class name in each line
        with open(filepath, 'r') as file:
            for line in file:
                class_id = line.split()[0]
                if class_id == old_class:
                    # Replace the old class name with the new one
                    line = line.replace(old_class, new_class)
                    modified = True
                lines_to_write.append(line)

        # If modified, rewrite the TXT file with updated content
        if modified:
            with open(filepath, 'w') as file:
                file.writelines(lines_to_write)
            print(f"Updated class name in '{filename}' from '{old_class}' to '{new_class}'.")

print("Class name replacement complete.")
