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
        return text  # fallback

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

def translate_index_html(index_path):
    if not os.path.exists(index_path):
        print(f"📄 File not found: {index_path}")
        return

    for lang in LANGUAGES:
        print(f"\n🌐 Translating to: {lang}")
        translator = GoogleTranslator(source='en', target=lang)
        output_file = os.path.join(lang, "index.html")
        process_html_file(index_path, output_file, translator)

def main():
    # CHANGE THIS PATH TO WHERE YOUR index.html IS LOCATED
    index_html_path = "C:\\Users\\EMMANUEL\\Documents\\Projects\\Goyerv\\front_end\\goyerv_community_app\\community_app\\web\\index.html"
    translate_index_html(index_html_path)
    print("\n🎉 All translations done!")

if __name__ == "__main__":
    main()
