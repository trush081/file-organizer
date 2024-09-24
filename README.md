# File Organizer

A Python script that organizes files in a specified directory based on their file types. It automatically moves files to appropriate subdirectories such as Images, Documents, Apps, Videos, Music, and Development files. Files that do not match any criteria are moved to an "Others" folder.

## Features

- Monitors a specified directory for new files and organizes them automatically.
- Supports various file types and organizes them into specific folders.
- Handles duplicate filenames by renaming them with a count suffix.
- Ignores certain files (e.g., `.DS_Store` on macOS).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/trush081/file-organizer.git
   cd file-organizer
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the script in one-time organization mode, specify the target directory:
```bash
python file-organizer.py /path/to/your/directory
```

To run the script in watchdog mode (to monitor the specified directory):
```bash
python file-organizer.py --watch /path/to/your/directory
```

## Dependencies

The project requires the following Python libraries:

- `watchdog`: For monitoring filesystem events.
- `argparse`: For parsing command-line arguments.

You can find the complete list of dependencies in the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.