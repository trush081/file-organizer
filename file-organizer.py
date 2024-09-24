import os
import shutil
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Define folder names and their corresponding file extensions
folder_mappings = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".md"],
    "Apps": [".exe", ".msi", ".apk", ".dmg", ".pkg", ".run", ".appimage"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Development/Python": [".py"],
    "Development/Java": [".java", ".jar"],
    "Development/JavaScript": [".js", ".jsx"],
    "Development/TypeScript": [".ts", ".tsx"],
    "Development/HTML": [".html", ".htm"],
    "Development/CSS": [".css"],
    "Development/Go": [".go"],
    "Development/C#": [".cs"],
    "Development/C++": [".cpp", ".h"],
    "Development/PHP": [".php"],
    "Development/Ruby": [".rb"],
    "Development/Shell": [".sh"],
    "Development/Config": [".json", ".xml", ".yaml", ".yml", ".ini", ".env"],
    "Development/Database": [".sql", ".db", ".sqlite", ".mdb", ".dbf"],
    "Development/Docker": [".dockerfile", "Dockerfile"],
    "Development/Git": [".gitignore", ".gitattributes"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Others": []  # Catch-all for unmatched files
}

# List of files to ignore
ignore_files = [
    '.DS_Store',  # macOS system file
    # Add any other files you want to ignore here
]

# Create folders if they do not exist
def create_folders(base_path):
    for folder in folder_mappings.keys():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

def organize_file(file_path, filename, base_path):
    # Skip ignored files
    if filename in ignore_files or any(filename.startswith(f) for f in ignore_files):
        logging.info(f'Ignored: {filename}')
        return

    moved = False
    for folder, extensions in folder_mappings.items():
        if any(filename.endswith(ext) for ext in extensions):
            target_path = os.path.join(base_path, folder, filename)

            # Handle duplicate filenames
            if os.path.exists(target_path):
                base, extension = os.path.splitext(filename)
                count = 1
                while os.path.exists(target_path):
                    target_path = os.path.join(base_path, folder, f"{base}_{count}{extension}")
                    count += 1

            try:
                shutil.move(file_path, target_path)
                logging.info(f'Moved: {filename} -> {folder}')
                moved = True
            except Exception as e:
                logging.error(f'Error moving {filename}: {e}')
            break

    # If no matching folder was found, move to 'Others'
    if not moved:
        others_folder = os.path.join(base_path, "Others")
        os.makedirs(others_folder, exist_ok=True)
        target_path = os.path.join(others_folder, filename)

        # Handle duplicate filenames in Others folder
        if os.path.exists(target_path):
            base, extension = os.path.splitext(filename)
            count = 1
            while os.path.exists(target_path):
                target_path = os.path.join(others_folder, f"{base}_{count}{extension}")
                count += 1

        try:
            shutil.move(file_path, target_path)
            logging.info(f'Moved: {filename} -> Others')
        except Exception as e:
            logging.error(f'Error moving {filename} to Others: {e}')

class FileHandler(FileSystemEventHandler):
    def __init__(self, base_path):
        self.base_path = base_path

    def on_created(self, event):
        if not event.is_directory:
            organize_file(event.src_path, os.path.basename(event.src_path), self.base_path)

def run_watchdog(base_path):
    event_handler = FileHandler(base_path)
    observer = Observer()
    observer.schedule(event_handler, base_path, recursive=False)
    observer.start()
    logging.info("Watching for new files...")
    try:
        while True:
            pass  # Keep running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Organize Files in Specified Directory.')
    parser.add_argument('directory', type=str, help='The directory to organize.')
    parser.add_argument('--watch', action='store_true', help='Run in watchdog mode.')
    args = parser.parse_args()

    # Set the base path from the argument
    base_path = os.path.abspath(args.directory)

    # Create folders if they do not exist
    create_folders(base_path)

    if args.watch:
        run_watchdog(base_path)
    else:
        # One-time organization
        for filename in os.listdir(base_path):
            file_path = os.path.join(base_path, filename)
            if os.path.isfile(file_path):
                organize_file(file_path, filename, base_path)

        logging.info("One-time organization completed.")