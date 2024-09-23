import os
import shutil

# Define the base folder containing the numbered folders
base_folder = "/home/son/S_GLMS_L9_197"

# List of cams to process (cam1 and cam2)
cams = ['cam1', 'cam2']

# List of image types to process (rgb and depth)
image_types = ['rgb', 'depth']

# Iterate over the numbered folders (0 to 5)
for i in range(6):
    # Path to the current numbered folder (e.g., /home/son/S_GLMS_L9_19/0)
    numbered_folder = os.path.join(base_folder, str(i))
    
    # Iterate over cam1 and cam2 folders
    for cam in cams:
        # Iterate over rgb and depth image types
        for image_type in image_types:
            # Define source and destination folders
            source_folder = os.path.join(numbered_folder, cam, image_type)
            destination_folder1 = os.path.join(numbered_folder, cam, f"sub_sort_{image_type}")
            destination_folder2 = os.path.join(numbered_folder, cam, f"sort_{image_type}")
            
            # Ensure destination folders exist
            os.makedirs(destination_folder1, exist_ok=True)
            os.makedirs(destination_folder2, exist_ok=True)
            
            # Step 1: Copy and rename files from source_folder to destination_folder1
            files = sorted([f for f in os.listdir(source_folder) if f.startswith(f"{image_type}_") and f.endswith(".png")])
            
            # Rename and copy files to destination_folder1
            for file in files:
                # Extract the number from the file name
                number = int(file.split('_')[1].split('.')[0])  # 'rgb_300.png' -> 300
                
                # Calculate the new number (e.g., 300 -> 0, 301 -> 1)
                new_number = number - 300
                
                # Define new file name
                new_file_name = f"{image_type}_{new_number}.png"
                
                # Construct full file paths
                old_file_path = os.path.join(source_folder, file)
                new_file_path = os.path.join(destination_folder1, new_file_name)
                
                # Copy the file to the destination folder with the new name
                shutil.copy(old_file_path, new_file_path)

            print(f"Step 1: Renamed and copied {len(files)} files to {destination_folder1}.")
            
            # Step 2: Filter files divisible by 6 and copy them to destination_folder2
            files = sorted([f for f in os.listdir(destination_folder1) if f.startswith(f"{image_type}_") and f.endswith(".png")])
            
            # Filter files that are divisible by 6
            filtered_files = [f for f in files if int(f.split('_')[1].split('.')[0]) % 6 == 0]
            
            # Copy files to the new destination folder without renaming
            for old_file in filtered_files:
                old_file_path = os.path.join(destination_folder1, old_file)
                new_file_path = os.path.join(destination_folder2, old_file)  # Keep the same file name
                
                # Copy the file to the destination folder with the same name
                shutil.copy(old_file_path, new_file_path)

            print(f"Step 2: Copied {len(filtered_files)} files to {destination_folder2}.")
            
            # Step 3: Rename files sequentially in destination_folder2
            files = sorted([f for f in os.listdir(destination_folder2) if f.startswith(f"{image_type}_") and f.endswith(".png")])
            
            # Sort files based on the number after 'image_type_'
            files_sorted = sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0]))
            
            # Rename files sequentially, starting from image_type_0.png
            for new_idx, old_file in enumerate(files_sorted):
                # Define new file name
                new_file_name = f"{image_type}_{new_idx}.png"
                
                # Construct full file paths
                old_file_path = os.path.join(destination_folder2, old_file)
                new_file_path = os.path.join(destination_folder2, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)

            print(f"Step 3: Renamed {len(files_sorted)} files starting from {image_type}_0.png in {destination_folder2}.")

print("All folders processed successfully.")
