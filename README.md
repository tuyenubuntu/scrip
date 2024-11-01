# scrip
#scrip for AOI - copy images

Step-by-Step Logic
Initialize the Program:

Import necessary libraries for file operations and data handling.
Load configuration data from an external Excel file to a dictionary.
Define Functions:

Load Config Data: Load categories (ElementType) from the Excel file into a dictionary for easy look-up.
Load Copied Log: Check if the log file exists for a given line name and load the previously copied items to avoid duplication.
Copy Files: For each image folder that meets the criteria, copy files to the destination folder if they haven’t already been copied and haven’t reached the copy limit.
Update Log: After copying, update the log file with newly copied images.
Run the Program:

Use a main loop to apply the function to each line name in the list, copying images according to the defined criteria.