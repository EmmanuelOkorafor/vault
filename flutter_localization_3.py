import os
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# 🌍 Target languages
LANGUAGES = ['fr', 'es', 'hi', 'ja', 'zh-CN', 'zh-TW']


# 🏷 Tags and attributes to translate
TAGS_TO_TRANSLATE = [
    ('meta', 'name', 'description'),
    ('meta', 'property', 'og:title'),
    ('meta', 'property', 'og:description'),
    ('meta', 'property', 'og:site_name'),
    ('meta', 'name', 'twitter:title'),
    ('meta', 'name', 'twitter:description'),
    ('meta', 'name', 'apple-mobile-web-app-title'),
    ('title', None, None),
]

def translate_text(text, translator):
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"❌ Translation failed: '{text[:30]}' -> {e}")
        return text  # Fallback to original

def process_html_file(file_path, output_path, translator):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        for tag_name, attr_key, attr_value in TAGS_TO_TRANSLATE:
            if tag_name == 'title':
                title_tag = soup.title
                if title_tag and title_tag.string:
                    translated = translate_text(title_tag.string, translator)
                    title_tag.string.replace_with(translated)
            else:
                for tag in soup.find_all(tag_name):
                    if tag.get(attr_key) == attr_value and tag.get('content'):
                        tag['content'] = translate_text(tag['content'], translator)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"✅ Translated: {output_path}")

    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")

def translate_language(lang, input_dir='articles'):
    print(f"\n🌐 Starting translations for: {lang}")
    translator = GoogleTranslator(source='en', target=lang)
    output_base = os.path.join(lang, 'articles')

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, input_dir)
                out_path = os.path.join(output_base, rel_path)
                process_html_file(src_path, out_path, translator)

def main():
    input_dir = 'articles'
    if not os.path.exists(input_dir):
        print("📁 'articles' folder not found.")
        return

    for lang in LANGUAGES:
        translate_language(lang, input_dir)

    print("\n🎉 All translations done!")

if __name__ == "__main__":
    main()
