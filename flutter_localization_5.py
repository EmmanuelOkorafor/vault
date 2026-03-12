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
    # "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_android_app\\android_app\\lib",
    # "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_ios_app\\ios_app\\lib",
    "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_web_app\\web_desktop_app\\lib",
    # "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_web_app\\web_mobile_app\\lib"
]

# Supported languages
languages = {
    'ar': 'Arabic', 'bg': 'Bulgarian', 'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)', 'hr': 'Croatian', 'cs': 'Czech',
    'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'et': 'Estonian',
    'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'ka': 'Georgian',
    'de': 'German', 'el': 'Greek', 'hi': 'Hindi', 'hu': 'Hungarian',
    'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'no': 'Norwegian',
    'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian',
    'es': 'Spanish', 'tr': 'Turkish', 'uk': 'Ukrainian'
}

# Updated regex: handles normal, triple quotes, single quotes, and ternary operators
pattern = r'AppLocalizations\.of\(.*?\)\.translate\(\s*(?:(?:(?P<q1>"""|\'\'\'|["\'])(?P<str1>.*?)(?P=q1))|(?:[^\)]*?\?(?:\s*)(?P<q2>["\'])(?P<true_val>.*?)(?P=q2)\s*:\s*(?P<q3>["\'])(?P<false_val>.*?)(?P=q3)))\s*\)'

# Extra static strings to include in translations
extra_strings = [
    'Analytics', 'Filter', 'Convert', 'QR Scanner', 'Upgrade', 'Theme',
    'Languages', 'Settings', 'Community', 'Feedback', 'Resources', 'Support',
    'Legal', 'Logout', "Slow or no internet connection",
    "There's been a problem connecting to goyerv. Please try again later", 'Radar', 'Messages'
]

# Batch size for translations
BATCH_SIZE = 10

# Function to keep PC awake
def keep_awake():
    """Simulate mouse movement to prevent sleep/hibernation every 60 seconds."""
    pyautogui.FAILSAFE = False
    while True:
        pyautogui.moveRel(0, 1)
        pyautogui.moveRel(0, -1)
        print("Keeping PC awake with mouse wiggle...")
        time.sleep(60)

# Translate a batch of strings
def translate_batch(strings, lang_code):
    try:
        concatenated = " || ".join(strings)
        translator = GoogleTranslator(source='en', target=lang_code)
        translated = translator.translate(concatenated)
        translated_strings = [t.strip() for t in translated.split("||")]
        if len(translated_strings) != len(strings):
            print(f"Warning: Translation mismatch for {lang_code}, falling back to English for batch")
            return strings
        return translated_strings
    except Exception as e:
        print(f"Error translating batch to {lang_code}: {e}")
        return strings

# Translate a language file
def translate_language(lang_code, lang_name, output_file):
    print(f"Starting translation for {lang_name} ({lang_code})...")
    try:
        with open(output_file, "r", encoding="utf-8") as json_file:
            translations = json.load(json_file)

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
                    translated_dict[key] = translations[key]

        translations.update(translated_dict)

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

# Process each project
for project_idx, project_root in enumerate(project_roots, 1):
    print(f"\nProcessing project {project_idx}: {project_root}")

    english_translations = {}

    print(f"Scanning project {project_idx} for localization strings...")
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith(".dart"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        matches = re.finditer(pattern, content, re.DOTALL)
                        for match in matches:
                            if match.group('str1'):  # Normal call
                                text = match.group('str1')
                                english_translations[text] = text
                            elif match.group('true_val') and match.group('false_val'):  # Ternary call
                                english_translations[match.group('true_val')] = match.group('true_val')
                                english_translations[match.group('false_val')] = match.group('false_val')
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Add extra static strings
    for s in extra_strings:
        english_translations[s] = s

    print(f"Found {len(english_translations)} unique strings for translation in project {project_idx}")

    output_base = os.path.join(os.path.dirname(__file__), "web_desktop_languages")
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

    print(f"Starting concurrent translation for all languages in project {project_idx}...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(translate_language, lang_code, lang_name, os.path.join(output_base, f"{lang_code}.json"))
            for lang_code, lang_name in languages.items() if lang_code != 'en'
        ]
        for future in futures:
            future.result()

    print(f"Completed processing project {project_idx}! All languages processed.")

print("\nLocalization extraction and translation completed for all projects!")
