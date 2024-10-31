import os
import shutil
import pandas as pd

# Read data from Excel file to create a dictionary of MixName and ElementType
excel_path = 'type_e.xlsx'
data = pd.read_excel(excel_path)

def copy_images(src_root, dest_root, line_name):
    # Create a dictionary to get ElementType based on MixName
    element_dict = dict(zip(data['MixName'], data['ElementType']))
    
    # Path to the log file
    log_path = f'Copied_MixNames_{line_name}.xlsx'
    
    # Check and create the log file if it doesn't exist
    if os.path.exists(log_path):
        copied = pd.read_excel(log_path)
        copied_ls = set(copied["CopiedMixName"])  # Use a set to increase lookup efficiency
    else:
        copied_ls = set()
    
    copied_mix_list = []  # List of newly copied MixNames
    total_files_copied = 0  # Counter for total files copied
    element_type_count = {}  # Track counts per ElementType

    # Filter valid folders to copy (names start with 'C' and are 7 characters long)
    mix_names = [mix_name for mix_name in os.listdir(os.path.join(src_root, line_name)) 
                 if mix_name.startswith('C') and len(mix_name) == 7]

    for mix_name in mix_names:
        if mix_name in copied_ls:
            print(f"{mix_name} has already been copied, skipping.")
            continue  # Skip if MixName has already been copied
        
        element_type = element_dict.get(mix_name)
        if element_type is None:
            continue  # Skip if ElementType is not found

        # Check if the element type has reached its 1500-image limit
        if element_type_count.get(element_type, 0) >= 1500:
            print(f"Reached 1500 limit for ElementType '{element_type}', prioritizing others.")
            continue

        src_folders = [os.path.join(src_root, line_name, mix_name, track, "SaddleSurface") for track in ["A", "B"]]
        dest_folder = os.path.join(dest_root, element_type)
        os.makedirs(dest_folder, exist_ok=True)  # Create destination folder if it doesn't exist

        files_copied = 0
        for src_folder in src_folders:
            if not os.path.exists(src_folder):
                continue  # Skip if source folder does not exist

            for filename in os.listdir(src_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    src_path = os.path.join(src_folder, filename)
                    dest_path = os.path.join(dest_folder, filename)

                    # Copy the image if necessary
                    shutil.copy(src_path, dest_path)
                    print(f"Copied: {filename} to {dest_folder}")

                    files_copied += 1
                    total_files_copied += 1
                    element_type_count[element_type] = element_type_count.get(element_type, 0) + 1

                    if total_files_copied >= 2000:
                        print("Copied 2000 images in total. Stopping.")
                        break  # Stop if the 2000-file limit is reached
                    if element_type_count[element_type] >= 1500:
                        break  # Stop further copying for this element type
                if total_files_copied >= 2000 or element_type_count[element_type] >= 1500:
                    break
            if total_files_copied >= 2000:
                break

        if files_copied > 0:
            copied_mix_list.append(mix_name)  # Add MixName to the copied list
        
        # Re-check to stop the main loop if the required image count is reached
        if total_files_copied >= 2000:
            break
    
    # Update the log file with newly copied MixNames
    if copied_mix_list:
        copied_df = pd.DataFrame(copied_mix_list, columns=["CopiedMixName"])
        if os.path.exists(log_path):
            existing_log = pd.read_excel(log_path)
            combined_log = pd.concat([existing_log, copied_df]).drop_duplicates()
        else:
            combined_log = copied_df

        combined_log.to_excel(log_path, index=False)
        print(f"Updated the log with copied MixNames in '{log_path}'.")

src_root = "Z"
dest_root = "data"
line_Names = ['11', '12'] 
for line_name in line_Names:
    copy_images(src_root, dest_root, line_name)
