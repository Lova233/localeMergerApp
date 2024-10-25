from flask import Flask, render_template, request, jsonify
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from werkzeug.utils import secure_filename
import logging

# Initialize Flask app and configure paths
app = Flask(__name__)
app.config['MERGED_FOLDER'] = 'static/merged_og'

# Ensure the output folder exists
if not os.path.exists(app.config['MERGED_FOLDER']):
    os.makedirs(app.config['MERGED_FOLDER'])

# Setup logging to file
logging.basicConfig(filename="enum_merge_process.log", level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

@app.route('/')
def index():
    return render_template('interface.html')

@app.route('/preview', methods=['POST'])
def preview():
    """Preview the count of files uploaded for OG and LANGUAGE folders."""
    try:
        og_files = request.files.getlist('og_folder')
        language_files = request.files.getlist('locale_folder')

        preview_data = {
            "og_file_count": len(og_files),
            "locale_file_count": len(language_files)
        }
        logging.info("Preview data: %s", preview_data)
        return jsonify(preview_data)
    except Exception as e:
        logging.error("Error in preview: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_and_merge():
    """Main route to handle file uploads and merging."""
    try:
        og_files = request.files.getlist('og_folder')
        language_files = request.files.getlist('locale_folder')

        if not og_files or not language_files:
            error_message = "Both OG and LANGUAGE folders must contain files."
            logging.error(error_message)
            return jsonify({"error": error_message}), 400

        merged_files = process_enum_files(og_files, language_files)
        logging.info("Merged files: %s", merged_files)
        return jsonify({"status": "Merge complete", "merged_files": merged_files})
    except Exception as e:
        logging.error("Error in upload_and_merge: %s", e)
        return jsonify({"error": str(e)}), 500

def process_enum_files(og_files, language_files):
    """Process enum files from OG and LANGUAGE folders based on exact folder matching."""
    merged_files = []
    language_folders = {}
    
    for lang_file in language_files:
        folder_name = os.path.basename(os.path.dirname(lang_file.filename))
        if folder_name not in language_folders:
            language_folders[folder_name] = []
        language_folders[folder_name].append(lang_file)

    for og_file in og_files:
        og_file_base = os.path.splitext(os.path.basename(og_file.filename))[0]

        if og_file_base not in language_folders:
            logging.info("No matching folder for '%s' in LANGUAGE files.", og_file_base)
            continue

        logging.info("Processing OG file: %s", og_file.filename)
        og_tree = ET.parse(og_file.stream)
        og_root = og_tree.getroot()

        for language_file in language_folders[og_file_base]:
            logging.info("Using LANGUAGE file: %s", language_file.filename)
            merge_enum_entries(og_root, language_file)

        output_filename = secure_filename(og_file.filename)
        output_path = os.path.join(app.config['MERGED_FOLDER'], output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pretty_print_xml(og_root, output_path)
        merged_files.append(output_path)

        logging.info("Merged and formatted file written to: %s", output_path)

    return merged_files

def merge_enum_entries(og_root, language_file):
    """Merge a specific localized language entry from a LANGUAGE file into the OG enum structure."""
    lang_tree = ET.parse(language_file.stream)
    lang_root = lang_tree.getroot()

    locale_id = os.path.splitext(os.path.basename(language_file.filename))[0]
    logging.info("Processing locale '%s' from LANGUAGE file '%s'", locale_id, language_file.filename)

    for lang_enumerated in lang_root.findall(".//enumerated"):
        idEnum = lang_enumerated.get("idEnum")
        og_enumerated = og_root.find(f".//enumerated[@idEnum='{idEnum}']")

        if og_enumerated is None:
            logging.info("No matching 'idEnum' '%s' found in OG file.", idEnum)
            continue

        for lang_enum in lang_enumerated.findall(".//item-enum"):
            enum_value = lang_enum.get("value")
            og_enum = og_enumerated.find(f".//item-enum[@value='{enum_value}']")

            if og_enum is None:
                logging.info("Enum with value '%s' not found in OG file.", enum_value)
                continue

            lang_description = lang_enum.find(f"item-description[@language='{locale_id}']")
            if lang_description is not None:
                new_value = lang_description.get('value')
                og_description = og_enum.find(f"item-description[@language='{locale_id}']")

                if og_description is not None:
                    old_value = og_description.get('value')
                    logging.info("Updating '%s' description in enum '%s'. Old: '%s', New: '%s'", locale_id, enum_value, old_value, new_value)
                    og_description.set('value', new_value)
                else:
                    logging.info("'%s' entry not found in enum '%s' in OG file. Adding new entry with value: '%s'", locale_id, enum_value, new_value)
                    new_description = ET.Element("item-description", language=locale_id, value=new_value)
                    og_enum.append(new_description)

def pretty_print_xml(element, file_path):
    """Pretty-print the XML to a file with indented lines."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join([line for line in pretty_xml.splitlines() if line.strip()]))

if __name__ == '__main__':
    app.run(debug=True)
