"""
This script extracts mission files from a ZIP archive for the game "Men of War Assault Squad 2".

Usage:
1. Set the `base_path` variable to the directory containing the 'resource/map.pak' file.
2. Run the script. It will:
   - Extract the contents of 'map.pak' to the 'resource' directory.
   - Retrieve mission folders and their paths.
   - Process each mission's '0.mi' file to remove lines containing '{"autosave"}'.
   - Delete the original 'map.pak' file after extraction.

Requirements:
- Python 3.x
- The 'zipfile' and 'os' modules (included in the Python standard library).

Original author: Kanroot
"""

import zipfile as zipfile   # For working with ZIP files
import os                   # For interacting with the operating system

# Edit line number eight
# EXAMPLE OF PATH
# /media/2A/SteamLibrary/steamapps/common/Men of War Assault Squad 2/
base_path = "./"  # Base path for files


def extract_pak():
    """
    Extracts the contents of the 'map.pak' ZIP file located in the resource directory.

    This function performs the following steps:
    1. Constructs the path to the 'map.pak' file using the global `base_path`.
    2. Checks if the ZIP file exists at the specified path.
    3. If the file exists:
       - Opens the ZIP file and extracts all its contents into the 'resource' directory.
       - Retrieves a list of mission folders from the extracted files.
       - Obtains the paths of missions contained within those folders.
       - Processes each mission's '0.mi' file to remove any lines containing '{"autosave"}'.
       - Deletes the original 'map.pak' file to clean up.
       - Prints a completion message to indicate that the process is finished.
    4. If the file does not exist, prints an error message indicating that the path is incorrect.
    """
    global base_path
    pak_file_path = base_path + "resource/map.pak"  # Path to the ZIP file

    # Check if the ZIP file exists
    if os.path.exists(pak_file_path):
        with zipfile.ZipFile(pak_file_path, "r") as zip_ref:
            zip_ref.extractall(base_path + "resource")      # Extract files
        mission_folders = get_mission_folders()             # Get mission folders
        mission_paths = get_mission_paths(mission_folders)  # Get missions
        process_mission_files(mission_paths)                # Process '0.mi' files
        delete_pak_file(pak_file_path)                      # Delete the ZIP file
        print_completion_message()                          # Print completion message

    else:
        print("PATH DOES NOT EXIST")  # Error if the path is wrong


def delete_pak_file(pak_file_path: str):
    """
    Deletes the specified ZIP file if it exists.

    Args:
        pak_file_path (str): The path to the ZIP file to be deleted.

    This function checks if the provided path exists and, if so, removes the file.
    """
    if os.path.exists(pak_file_path):
        # Remove the ZIP file
        os.remove(pak_file_path)


def get_mission_folders():
    """
    Retrieves a list of valid mission folder paths from the faction directory.

    This function constructs the path to the faction folder, lists all subdirectories,
    and filters out only those that are valid directories. It returns a sorted list of
    paths to these mission folders.

    Returns:
        list: A list of paths to valid mission folders.
    """
    faction_folder_path = base_path + "resource/map/single/"
    folder_list = os.listdir(faction_folder_path)  # List all folders

    valid_folders = [
        folder_name
        for folder_name in folder_list
        if os.path.isdir(faction_folder_path + folder_name)
    ]

    # Sort folder names
    valid_folders.sort()

    # Return mission paths
    return [faction_folder_path + folder + "/" for folder in valid_folders]


def get_mission_paths(faction_folders: list):
    """
    Retrieves a list of mission paths from the provided faction folders.

    This function iterates through each faction folder, lists all subdirectories,
    and checks if they are valid directories. It constructs the full paths for
    each mission folder and adds them to the list of mission paths.

    Args:
        faction_folders (list): A list of paths to faction folders.

    Returns:
        list: A list of paths to the mission folders found within the faction folders.
    """
    mission_paths = []

    for faction_folder in faction_folders:
        subfolder_list = os.listdir(faction_folder)  # List all folders in the faction

        mission_paths.extend(
            faction_folder + mission_folder + "/"
            for mission_folder in subfolder_list
            if os.path.isdir(faction_folder + mission_folder + "/")
        )

    return mission_paths  # Return mission paths


def process_mission_files(mission_paths: list):
    """
    Processes the '0.mi' files for each mission path.

    This function opens each '0.mi' file located in the specified mission paths,
    reads its contents, and removes any lines that contain the string '{"autosave"}'.
    The cleaned content is then written back to the same file.

    Args:
        mission_paths (list): A list of paths to the mission folders containing '0.mi' files.

    This function modifies the files in place, ensuring that only relevant data remains.
    """
    for mission_path in mission_paths:
        mission_file_path = mission_path + "0.mi"  # Path to '0.mi' file

        with open(mission_file_path, "r") as file:
            lines = file.readlines()  # Read all lines

        with open(mission_file_path, "w") as file:
            for line in lines:
                if '{"autosave"}' not in line:
                    file.write(line)  # Write the line back


def print_completion_message():
    """
    Prints a completion message to indicate that the process is finished.

    This function outputs a simple message to the console, confirming that
    the extraction and processing of mission files have been completed.
    """
    print("it's done! \nby: Kanroot and TheIIIrd")


if __name__ == "__main__":
    extract_pak()  # Start the extraction process
