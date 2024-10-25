import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, jsonify
import os
import html
import logging
from werkzeug.utils import secure_filename
from xml.dom import minidom

# Setup logging to file
logging.basicConfig(filename="merge_process.log", level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
app.config['MERGED_FOLDER'] = 'static/merged_og'

# Ensure the output folder exists
if not os.path.exists(app.config['MERGED_FOLDER']):
    os.makedirs(app.config['MERGED_FOLDER'])

@app.route('/')
def index():
    return render_template('interface.html')

@app.route('/preview', methods=['POST'])
def preview():
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
    try:
        og_files = request.files.getlist('og_folder')
        language_files = request.files.getlist('locale_folder')

        if not og_files or not language_files:
            error_message = "Both OG and LANGUAGE folders must contain files."
            logging.error(error_message)
            return jsonify({"error": error_message}), 400

        merged_files = process_dictionary_files(og_files, language_files)
        logging.info("Merged files: %s", merged_files)
        return jsonify({"status": "Merge complete", "merged_files": merged_files})
    except Exception as e:
        logging.error("Error in upload_and_merge: %s", e)
        return jsonify({"error": str(e)}), 500

def process_dictionary_files(og_files, language_files):
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
            merge_language_entries(og_root, language_file)

        # Apply pretty-printing for the XML structure
        output_filename = secure_filename(og_file.filename)
        output_path = os.path.join(app.config['MERGED_FOLDER'], output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            pretty_print_xml(og_tree.getroot(), file)
        
        merged_files.append(output_path)
        logging.info("Merged file written to: %s", output_path)

    return merged_files

def merge_language_entries(og_root, language_file):
    lang_tree = ET.parse(language_file.stream)
    lang_root = lang_tree.getroot()

    locale_id = os.path.splitext(os.path.basename(language_file.filename))[0]
    logging.info("Processing locale '%s' from LANGUAGE file '%s'", locale_id, language_file.filename)

    for message in lang_root.findall(".//message"):
        message_name = message.get('name')
        og_message = og_root.find(f".//message[@name='{message_name}']")

        if og_message is None:
            logging.info("Message '%s' not found in OG file.", message_name)
            continue

        lang_entry = message.find(f"language[@id='{locale_id}']")
        if lang_entry is not None:
            original_value = lang_entry.get('value')
            decoded_value = decode_special_characters(original_value)
            logging.debug("LANGUAGE file: Original: '%s', Decoded: '%s'", original_value, decoded_value)

            og_lang_entry = og_message.find(f"language[@id='{locale_id}']")

            if og_lang_entry is not None:
                old_value = og_lang_entry.get('value')
                logging.debug("Existing '%s' entry found in message '%s'. Old value: '%s'", locale_id, message_name, old_value)
                
                og_lang_entry.set('value', decoded_value)
                logging.info("Updated '%s' in message '%s' to new value: '%s'", locale_id, message_name, decoded_value)
            else:
                logging.info("'%s' entry not found in message '%s' in OG file. Adding new entry with value: '%s'", locale_id, message_name, decoded_value)
                new_lang_entry = ET.Element("language", id=locale_id, value=decoded_value)
                og_message.append(new_lang_entry)

def decode_special_characters(text):
    """Decode special HTML or XML character entities (e.g., &#x27; to ') without re-encoding."""
    return html.unescape(text)

def pretty_print_xml(element, file):
    """Pretty-print the XML to file with indented lines and no extra blank lines."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Remove extra blank lines
    no_blank_lines = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])
    file.write(no_blank_lines)

if __name__ == '__main__':
    app.run(debug=True)
