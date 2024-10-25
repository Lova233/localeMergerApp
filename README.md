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
LANGUAGE
├── BaseDictionary
│   ├── de-CH.xml
│   ├── es.xml
├── PolicyDictionary
│   ├── fr.xml
│   ├── it.xml
```
### Why Folder Structure Matters

The folder structure ensures that translations for each dictionary file are clearly separated by locale, minimizing errors in the merging process. By matching each subfolder in the LANGUAGE directory to its corresponding XML file in the OG directory, the tool can:
1. Locate and update the appropriate language entries accurately.
2. Prevent any untranslated text in the OG files from being altered.
3. Keep new translations confined to their exact sections, preserving a clean and organized XML structure.

### Usage

1. Start the program and open the upload interface.
2. Upload the **OG** folder (containing your main dictionary XML files).
3. Upload the **LANGUAGE** folder (with locale-specific subfolders containing translations).
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

