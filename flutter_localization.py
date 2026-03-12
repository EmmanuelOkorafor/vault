import os
import re
import json

# Path to your Flutter project root
project_root = "/path/to/your/flutter/project"

# Regex pattern to match AppLocalizations.of(context).translate("...")
pattern = r'AppLocalizations\.of\(.*?\)\.translate\(["\'](.*?)["\']\)'

# Dictionary to hold the translations
translations = {}

# Walk through the Flutter project files
for root, dirs, files in os.walk(project_root):
    for file in files:
        if file.endswith(".dart"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.findall(pattern, content)
                for match in matches:
                    translations[match] = match  # Key = Value for now

# Output path for the generated JSON
output_file = os.path.join(project_root, "lib", "l10n", "en.json")

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save to JSON
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(translations, json_file, indent=2, ensure_ascii=False)

print(f"Localization keys extracted to {output_file}")
C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_android_app\\android_app\\lib