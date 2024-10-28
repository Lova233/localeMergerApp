# Locale Merger Tool

The **Locale Merger Tool** is a user-friendly program that simplifies merging multiple locale files into a base, or **OG file**, ensuring consistent translations across your XML dictionary files. With a simple upload interface, you can select your OG and LANGUAGE folders, and the tool handles the rest, merging translations for specific locales with ease.

### Features
- Merges translations from multiple locale files into a base XML dictionary file.
- Maintains original content by adding or updating only the specific locale entries.
- Simple two-folder upload interface.
- Currently optimized for merging **Dictionary.xml** files.

### Folder Structure

The folder structure is crucial for proper operation. The tool reads from an **OG folder** (containing base XML files) and a **LANGUAGE folder** (with subfolders containing locale-specific XML files). Here’s the expected setup:

```plaintext
OG
├── Dictionaries
│   ├── BaseDictionary.xml
│   ├── PolicyDictionary.xml
│   ├── MenuDictionary.xml
├── Enums
│   ├── EnumFileOne.xml
│   ├── EnumFileTwo.xml
LANGUAGE
├── BaseDictionary
│   ├── de-CH.xml
│   ├── es.xml
├── PolicyDictionary
│   ├── fr.xml
│   ├── it.xml
├── EnumFileOne
│   ├── de-CH.xml
│   ├── fr.xml
```
### Why Folder Structure Matters
The folder structure ensures that translations for each dictionary and enumeration file are clearly separated by locale, minimizing errors in the merging process. By matching each subfolder in the LANGUAGE directory to its corresponding XML file in the OG directory, the tool can:

- **Locate and update** the appropriate language entries accurately.
- **Prevent untranslated text** in the OG files from being altered.
- **Keep new translations confined** to their exact sections, preserving a clean and organized XML structure.

### Usage
1. Start the program and open the upload interface.
2. For **Dictionary.xml** files, upload the OG and LANGUAGE folders using **AppDictionary**.
3. For **Enum.xml** files, upload the OG and LANGUAGE folders using **AppEnum**.
4. Click "Generate and Download Merged Files" to receive your updated XML files.

The tool will output a **MERGED-OG** folder mirroring the OG structure, with all specified translations merged.

### Technology Stack
- **Flask**: Backend framework for handling file uploads and XML processing.
- **Python**: Core language, with XML libraries for parsing and modifying XML files.
- **HTML/CSS/JavaScript**: User interface, providing a straightforward file upload experience.
- **Logging**: Provides detailed logs to track processing steps for each file.

### Installation

1. Clone the repository.
2. Ensure you have Python installed, along with Flask and any necessary libraries:
```bash
   pip install flask
```
   Run the application:

```bash
python app.py
```
Open the interface in your browser at http://127.0.0.1:5000.

### Potential Extensions
Expand support to additional XML file types.
Enable a preview mode to show merged content before saving.
Enhance error handling for more complex folder structures.
### Example Output
After successful merging, files in MERGED-OG are organized with each <language> entry on its own line, providing a clean, readable structure.

### Contributions
Feel free to contribute, report issues, or suggest enhancements. Any improvements to make this tool more versatile and user-friendly are welcome!

Happy merging! 😊




script utile per noi stronzi 

```bash 

#!/bin/bash

# Define the root directory as the current working directory
ROOT_DIR=$(pwd)

# Directories to process
TARGET_DIRS=("Dictionaries" "Enums_xml")

function restructure_files() {
    # Loop through each target directory (Dictionaries and Enums_xml)
    for TARGET in "${TARGET_DIRS[@]}"; do
        # Check if the target directory exists in each date/language folder
        for DATE_LANG_FOLDER in "$ROOT_DIR"/*/; do
            TARGET_SUBDIR="$DATE_LANG_FOLDER/$TARGET"
            LANG=$(basename "$DATE_LANG_FOLDER" | cut -d'_' -f2)

            # If the target subdirectory exists, process its files
            if [[ -d "$TARGET_SUBDIR" ]]; then
                for FILE in "$TARGET_SUBDIR"/*.xml; do
                    if [[ -f "$FILE" ]]; then
                        # Extract base file name without the extension
                        BASE_NAME=$(basename "$FILE" .xml)

                        # Create a directory for the file in the root Dictionaries or Enums_xml
                        DEST_DIR="$ROOT_DIR/$TARGET/$BASE_NAME"
                        mkdir -p "$DEST_DIR"

                        # Move or copy the file into the new directory, naming it by language code
                        cp "$FILE" "$DEST_DIR/$LANG.xml"
                    fi
                done
            fi
        done
    done
}

# Execute the function to perform restructuring
restructure_files

echo "Folder restructuring complete. Each XML file is now organized by language within $TARGET_DIRS."

```

