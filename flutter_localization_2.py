import os
import re
import json
from deep_translator import GoogleTranslator
import time
import pyautogui
import threading
from concurrent.futures import ThreadPoolExecutor

# List of Flutter project root directories
project_roots = [
    "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_android_app\\android_app\\lib",
    "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_ios_app\\ios_app\\lib",
    "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_web_app\\web_desktop_app\\lib",
    "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_web_app\\web_mobile_app\\lib"
    # "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_community_app\\community_app\\lib"
    # "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_support_app\\support_app\\lib"
    # Add more project paths here
]

# Supported languages
language = {
    'ar': 'Arabic', 'bg': 'Bulgarian', 'zh-CN': 'Chinese (Simplified)', 
    'zh-TW': 'Chinese (Traditional)', 'hr': 'Croatian', 'cs': 'Czech', 
    'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'et': 'Estonian',
    'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'ka': 'Georgian', 
    'de': 'German', 'el': 'Greek', 'hi': 'Hindi', 'hu': 'Hungarian',
    'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'no': 'Norwegian', 
    'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 
    'es': 'Spanish', 'tr': 'Turkish', 'uk': 'Ukrainian'
}


# Regex pattern to match AppLocalizations.of(context).translate with single, double, or triple quotes
pattern = r'AppLocalizations\.of\(.*?\)\.translate\(\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\'|"(.*?)"|\'(.*?)\')\s*\)'

# Batch size for translations
BATCH_SIZE = 10

# Function to keep PC awake
def keep_awake():
    """Simulate mouse movement to prevent sleep/hibernation every 60 seconds."""
    pyautogui.FAILSAFE = False  # Disable fail-safe to avoid interruption
    while True:
        pyautogui.moveRel(0, 1)  # Move mouse 1 pixel down
        pyautogui.moveRel(0, -1)  # Move mouse 1 pixel back up
        print("Keeping PC awake with mouse wiggle...")
        time.sleep(60)  # Wait 60 seconds before next wiggle

# Function to translate a batch of strings
def translate_batch(strings, lang_code):
    """Translate a batch of strings concatenated with || and split back."""
    try:
        concatenated = " || ".join(strings)
        translator = GoogleTranslator(source='en', target=lang_code)
        translated = translator.translate(concatenated)
        # Split translated text, handling cases where delimiter might get translated
        translated_strings = [t.strip() for t in translated.split("||")]
        # Ensure the number of translated strings matches input
        if len(translated_strings) != len(strings):
            print(f"Warning: Translation mismatch for {lang_code}, falling back to English for batch")
            return strings
        return translated_strings
    except Exception as e:
        print(f"Error translating batch to {lang_code}: {e}")
        return strings  # Fallback to English

# Function to translate a single language's JSON file
def translate_language(lang_code, lang_name, output_file):
    """Translate all strings in a JSON file for a given language."""
    print(f"Starting translation for {lang_name} ({lang_code})...")
    try:
        # Read the JSON file
        with open(output_file, "r", encoding="utf-8") as json_file:
            translations = json.load(json_file)
        
        # Get all keys and process in batches
        keys = list(translations.keys())
        translated_dict = {}
        
        for i in range(0, len(keys), BATCH_SIZE):
            batch_keys = keys[i:i + BATCH_SIZE]
            batch_strings = [translations[key] for key in batch_keys]
            try:
                translated_batch = translate_batch(batch_strings, lang_code)
                for key, translated_text in zip(batch_keys, translated_batch):
                    translated_dict[key] = translated_text
            except Exception as e:
                print(f"Error in batch {i//BATCH_SIZE + 1} for {lang_code}: {e}")
                for key in batch_keys:
                    translated_dict[key] = translations[key]  # Fallback to English
        
        # Update translations with batch results
        translations.update(translated_dict)
        
        # Rewrite the JSON file
        try:
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(translations, json_file, indent=2, ensure_ascii=False)
            print(f"Finished translating {lang_name} ({lang_code}), updated {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")
            
    except Exception as e:
        print(f"Error processing {output_file}: {e}")

# Start keep-awake thread
awake_thread = threading.Thread(target=keep_awake, daemon=True)
awake_thread.start()
print("Started keep-awake thread to prevent PC from sleeping...")

# Process each project directory sequentially
for project_idx, project_root in enumerate(project_roots, 1):
    print(f"\nProcessing project {project_idx}: {project_root}")
    
    # Step 1: Scan directory and extract English translations
    print(f"Scanning project {project_idx} for localization strings...")
    english_translations = {}
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith(".dart"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        matches = re.findall(pattern, content, re.DOTALL)
                        for match in matches:
                            # Extract the non-empty match from the tuple (handles different quote types)
                            text = next((item for item in match if item), None)
                            if text:
                                english_translations[text] = text  # English is the source
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    print(f"Found {len(english_translations)} unique strings for translation in project {project_idx}")

    # Step 2: Create JSON files for all languages with English translations
    # output_base = os.path.join(os.path.dirname(__file__), f"project_{project_idx}_languages")
    output_base = os.path.join(os.path.dirname(__file__), f"support_languages")
    os.makedirs(output_base, exist_ok=True)

    print(f"Creating JSON files with English translations for project {project_idx}...")
    for lang_code in languages:
        output_file = os.path.join(output_base, f"{lang_code}.json")
        try:
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(english_translations, json_file, indent=2, ensure_ascii=False)
            print(f"Created {output_file} with English translations")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")

    # Step 3: Translate non-English JSON files concurrently
    print(f"Starting concurrent translation for all languages in project {project_idx}...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(translate_language, lang_code, lang_name, os.path.join(output_base, f"{lang_code}.json"))
            for lang_code, lang_name in languages.items() if lang_code != 'en'
        ]
        # Wait for all translations to complete
        for future in futures:
            future.result()

    print(f"Completed processing project {project_idx}! All languages processed.")

print("\nLocalization extraction and translation completed for all projects!")