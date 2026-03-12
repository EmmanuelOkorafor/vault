#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Goyerv SEO Landing Generator
----------------------------
Traverses web/<lang>/ subfolders, enhances each HTML file with:
- Localized SEO body content (H1, paragraphs, bullets, routes, images, FAQ)
- 3s delay for any explicit JS redirects (window.location.href assignments)
- Minimal CSS, preserves original head/scripts/meta
- RTL handling for Arabic, etc.

Usage:
  python goyerv_seo_generator.py --root ./web

Back up your web directory before running in production.
"""

import os
import re
import sys
import json
import html
import argparse
from pathlib import Path

REDIR_PATTERN = re.compile(r"window\.location\.href\s*=\s*(['\"]).*?\1\s*;", re.IGNORECASE)
META_DESC_PATTERN = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)
OG_TITLE_PATTERN = re.compile(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)
HTML_LANG_PATTERN = re.compile(r'<html\b[^>]*\blang=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)
BODY_OPEN_PATTERN = re.compile(r'(<body\b[^>]*>)', re.IGNORECASE)

RTL_LANGS = {"ar", "fa", "he", "ur"}

PHRASES = {
    "en": {
        "cta": "Get started",
        "headline_fallback": "Faster global delivery with Goyerv",
        "intro": "Crowdsourced logistics, instant delivery, and on-demand personal shoppers. Global reach, fast speed.",
        "benefits": [
            "Ship worldwide with verified travelers.",
            "Save time and money on urgent deliveries.",
            "On-demand personal shopping across borders.",
            "Real-time tracking and secure payments."
        ],
        "how": ["Post a request", "Match with a verified traveler", "Track and receive"],
        "routes_label": "Popular routes",
        "faq_label": "FAQ",
        "faq": [
            ("Is Goyerv safe?", "Yes. We verify identities and use secure, escrow-like payments."),
            ("How fast can it be?", "Often same-day within a city and 1-3 days internationally, depending on routes."),
            ("What can I ship?", "Documents, gifts, small electronics, and more, subject to local laws.")
        ],
        "img_alt": "Goyerv delivery illustration",
        "cta2": "Open the app"
    },
    "es": {
        "cta": "Comenzar",
        "headline_fallback": "Entrega global mas rapida con Goyerv",
        "intro": "Logistica colaborativa, entrega instantanea y personal shoppers bajo demanda. Alcance global, velocidad impresionante.",
        "benefits": [
            "Envia a todo el mundo con viajeros verificados.",
            "Ahorra tiempo y dinero en envios urgentes.",
            "Personal shoppers bajo demanda entre paises.",
            "Seguimiento en tiempo real y pagos seguros."
        ],
        "how": ["Publica tu pedido", "Conectate con un viajero verificado", "Sigue y recibe"],
        "routes_label": "Rutas populares",
        "faq_label": "Preguntas frecuentes",
        "faq": [
            ("Es seguro Goyerv?", "Si. Verificamos identidades y usamos pagos seguros tipo deposito en garantia."),
            ("Que tan rapido puede ser?", "A veces el mismo dia en la ciudad y 1-3 dias internacionalmente, segun la ruta."),
            ("Que puedo enviar?", "Documentos, regalos, pequenos electronicos y mas, sujeto a las leyes locales.")
        ],
        "img_alt": "Ilustracion de entrega de Goyerv",
        "cta2": "Abrir la app"
    },
    "fr": {
        "cta": "Commencer",
        "headline_fallback": "Livraison mondiale plus rapide avec Goyerv",
        "intro": "Logistique participative, livraison instantanee et personal shoppers a la demande. Portee mondiale, vitesse elevee.",
        "benefits": [
            "Expediez partout avec des voyageurs verifies.",
            "Gagnez du temps et de l'argent pour les envois urgents.",
            "Personal shoppers a la demande entre pays.",
            "Suivi en temps reel et paiements securises."
        ],
        "how": ["Publiez une demande", "Trouvez un voyageur verifie", "Suivez et recevez"],
        "routes_label": "Itineraires populaires",
        "faq_label": "FAQ",
        "faq": [
            ("Goyerv est-il sur?", "Oui. Nous verifions les identites et utilisons des paiements securises de type escrow."),
            ("Quelle rapidite?", "Souvent le jour meme en ville et 1-3 jours a l'international selon les trajets."),
            ("Que puis-je envoyer?", "Documents, cadeaux, petits appareils, etc., sous reserve des lois locales.")
        ],
        "img_alt": "Illustration de livraison Goyerv",
        "cta2": "Ouvrir l'app"
    },
    "ar": {
        "cta": "ابدأ الآن",
        "headline_fallback": "توصيل عالمي أسرع مع Goyerv",
        "intro": "لوجستيات جماعية، توصيل فوري، ومتسوقون شخصيون عند الطلب. انتشار عالمي، وسرعة فائقة.",
        "benefits": [
            "اشحن إلى أي مكان عبر مسافرين موثقين.",
            "وفّر الوقت والمال في الطلبات العاجلة.",
            "متسوقون شخصيون عبر الحدود عند الطلب.",
            "تتبع لحظي ومدفوعات آمنة."
        ],
        "how": ["انشر طلبك", "تطابق مع مسافر موثق", "تتبع واستلم"],
        "routes_label": "مسارات شائعة",
        "faq_label": "الأسئلة الشائعة",
        "faq": [
            ("هل Goyerv آمن؟", "نعم، نتحقق من الهوية ونستخدم مدفوعات آمنة شبيهة بالإسكرو."),
            ("ما مدى السرعة؟", "أحيانًا في نفس اليوم داخل المدينة و1-3 أيام دوليًا حسب المسار."),
            ("ماذا يمكنني شحنه؟", "مستندات وهدايا وأجهزة صغيرة وغير ذلك وفق القوانين المحلية.")
        ],
        "img_alt": "رسم توضيحي لتسليم Goyerv",
        "cta2": "افتح التطبيق"
    },
    "pt": {
        "cta": "Comecar",
        "headline_fallback": "Entrega global mais rapida com a Goyerv",
        "intro": "Logistica colaborativa, entrega instantanea e personal shoppers sob demanda. Alcance global, velocidade impressionante.",
        "benefits": [
            "Envie para o mundo com viajantes verificados.",
            "Economize tempo e dinheiro em envios urgentes.",
            "Personal shoppers sob demanda entre paises.",
            "Rastreamento em tempo real e pagamentos seguros."
        ],
        "how": ["Publique o pedido", "Combine com um viajante verificado", "Acompanhe e receba"],
        "routes_label": "Rotas populares",
        "faq_label": "Perguntas frequentes",
        "faq": [
            ("A Goyerv e segura?", "Sim. Verificamos identidades e usamos pagamentos seguros tipo escrow."),
            ("Qual a velocidade?", "As vezes no mesmo dia na cidade e 1-3 dias internacionalmente, dependendo da rota."),
            ("O que posso enviar?", "Documentos, presentes, pequenos eletronicos e mais, sujeito as leis locais.")
        ],
        "img_alt": "Ilustracao de entrega Goyerv",
        "cta2": "Abrir o aplicativo"
    },
    "de": {
        "cta": "Jetzt starten",
        "headline_fallback": "Schnellere weltweite Zustellung mit Goyerv",
        "intro": "Crowdsourced Logistik, sofortige Lieferung und Personal Shopper auf Abruf. Globale Reichweite, hohe Geschwindigkeit.",
        "benefits": [
            "Versenden Sie weltweit mit verifizierten Reisenden.",
            "Sparen Sie Zeit und Geld bei eiligen Sendungen.",
            "Personal Shopper auf Abruf uber Grenzen hinweg.",
            "Echtzeit-Tracking und sichere Zahlungen."
        ],
        "how": ["Anfrage posten", "Mit verifiziertem Reisenden matchen", "Verfolgen und erhalten"],
        "routes_label": "Beliebte Routen",
        "faq_label": "Haufige Fragen",
        "faq": [
            ("Ist Goyerv sicher?", "Ja. Wir verifizieren Identitaten und nutzen sichere Escrow-ahnliche Zahlungen."),
            ("Wie schnell geht es?", "Oft am selben Tag in der Stadt und 1-3 Tage international, je nach Route."),
            ("Was kann ich versenden?", "Dokumente, Geschenke, kleine Elektronik usw., gemass den lokalen Gesetzen.")
        ],
        "img_alt": "Goyerv Lieferillustration",
        "cta2": "App offnen"
    },
    "it": {
        "cta": "Inizia ora",
        "headline_fallback": "Consegna globale piu veloce con Goyerv",
        "intro": "Logistica collaborativa, consegna istantanea e personal shoppers on-demand. Copertura globale, velocita elevata.",
        "benefits": [
            "Spedisci ovunque con viaggiatori verificati.",
            "Risparmia tempo e denaro nelle urgenze.",
            "Personal shopper tra paesi su richiesta.",
            "Tracciamento in tempo reale e pagamenti sicuri."
        ],
        "how": ["Pubblica la richiesta", "Abbina un viaggiatore verificato", "Traccia e ricevi"],
        "routes_label": "Rotte popolari",
        "faq_label": "Domande frequenti",
        "faq": [
            ("Goyerv e sicuro?", "Si. Verifichiamo le identita e usiamo pagamenti sicuri tipo escrow."),
            ("Quanto e veloce?", "Spesso in giornata in citta e 1-3 giorni a livello internazionale, secondo la rotta."),
            ("Cosa posso spedire?", "Documenti, regali, piccoli dispositivi, ecc., nel rispetto delle leggi locali.")
        ],
        "img_alt": "Illustrazione consegna Goyerv",
        "cta2": "Apri l'app"
    },
    "ru": {
        "cta": "Nachat'",
        "headline_fallback": "Bystraya mezhdunarodnaya dostavka s Goyerv",
        "intro": "Kraudsorsingovaya logistika, mgnovennaya dostavka i personal'nye shoppery po trebovaniyu. Global'nyy ohvat, vysokaya skorost'.",
        "benefits": [
            "Dostavlyayte po vsemu miru s proverennymi puteshestvennikami.",
            "Ekonom'te vremya i den'gi na srochnyh otpravleniyah.",
            "Personal'nye pokupki za rubezhom po zaprosu.",
            "Otslezhivanie v real'nom vremeni i bezopasnye platezhi."
        ],
        "how": ["Sozdayte zayavku", "Sopostav'tes' s proverennym puteshestvennikom", "Otslezhivayte i poluchayte"],
        "routes_label": "Populyarnye marshruty",
        "faq_label": "FAQ",
        "faq": [
            ("Eto bezopasno?", "Da. My proveryaem lichnosti i ispol'zuem bezopasnye platezhi napodobie escrow."),
            ("Kak bystro?", "Inogda v tot zhe den' po gorodu i 1-3 dnya mezhdunarodno, v zavisimosti ot marshruta."),
            ("Chto mozhno otpravlyat'?", "Dokumenty, podarki, melkuyu elektroniku i t.d., s uchetom mestnyh zakonov.")
        ],
        "img_alt": "Illyustratsiya dostavki Goyerv",
        "cta2": "Otkryt' prilozhenie"
    },
    "ja": {
        "cta": "Hajimeru",
        "headline_fallback": "Goyerv de hayai global haiso",
        "intro": "Kuraudososingu butsuryu, sokujitsu haiso, on-demando no pasonaru shoppa. Sekai teki reach, kosoku.",
        "benefits": [
            "Ninsho-zumi ryokosha de sekai-chu ni hasso.",
            "Kinkyuu haiso no jikan to kosuto o sakugen.",
            "Kokkyo o koeru on-demando kojin-kai.",
            "Riarutaimu tsuuchaku to anzen shiharai."
        ],
        "how": ["Rikuesuto o toukou", "Ninsho-zumi ryokosha to macchi", "Tsuiseki shite jushin"],
        "routes_label": "Ninki ruto",
        "faq_label": "FAQ",
        "faq": [
            ("Goyerv wa anzen?", "Hai. Shomei kakunin to escrow-gata no anzen-na shiharai o saiyou."),
            ("Dorekurai hayai?", "Toshinai dewa toujitsu, kokusai dewa 1-3 nichi (ruto ni yoru)."),
            ("Nani o okureru?", "Shorui, gifuto, kogata denshi seihin nado. Kokkun no houritsu ni shitagatte kudasai.")
        ],
        "img_alt": "Goyerv haiso no irasuto",
        "cta2": "Apuri o hiraku"
    }
}

ROUTES = {
    "en": [("Lagos", "New York"), ("London", "Berlin"), ("Los Angeles", "Tokyo")],
    "es": [("Madrid", "Buenos Aires"), ("Ciudad de Mexico", "Barcelona"), ("Lima", "Santiago")],
    "fr": [("Paris", "Montreal"), ("Casablanca", "Paris"), ("Abidjan", "Dakar")],
    "ar": [("دبي", "القاهرة"), ("الرياض", "إسطنبول"), ("الدار البيضاء", "باريس")],
    "pt": [("Sao Paulo", "Lisboa"), ("Rio de Janeiro", "Porto"), ("Luanda", "Maputo")],
    "de": [("Berlin", "Munchen"), ("Frankfurt", "Zurich"), ("Hamburg", "Wien")],
    "it": [("Roma", "Milano"), ("Torino", "Napoli"), ("Bologna", "Firenze")],
    "ru": [("Moskva", "Sankt-Peterburg"), ("Moskva", "Minsk"), ("Kazan", "Ekaterinburg")],
    "ja": [("Tokyo", "Osaka"), ("Nagoya", "Fukuoka"), ("Tokyo", "Taipei")],
    "ko": [("Seoul", "Busan"), ("Seoul", "Tokyo"), ("Incheon", "Shanghai")],
    "hi": [("Mumbai", "Dilli"), ("Bengaluru", "Kolkata"), ("Hyderabad", "Chennai")],
    "zh-CN": [("Shanghai", "Guangzhou"), ("Beijing", "Shenzhen"), ("Chengdu", "Hong Kong")]
}

def is_rtl(lang_code: str) -> bool:
    base = lang_code.split("-")[0].lower()
    return base in RTL_LANGS

def pick_phrases(lang_code: str):
    base = lang_code.split("-")[0]
    return PHRASES.get(base, PHRASES["en"]), base

def pick_routes(lang_code: str):
    base = lang_code.split("-")[0]
    return ROUTES.get(base, ROUTES["en"])

def build_seo_section(lang: str, description: str, og_title: str=None) -> str:
    phrases, base = pick_phrases(lang)
    rtl = is_rtl(lang)
    dir_attr = ' dir="rtl"' if rtl else ""
    headline_seed = (og_title or "").strip() or description.strip() or phrases["headline_fallback"]
    headline = html.escape(headline_seed)
    intro = html.escape(description.strip() or phrases["intro"])
    benefits = "".join(f"<li>{html.escape(b)}</li>" for b in phrases["benefits"][:4])
    how_steps = "".join(f"<li>{html.escape(s)}</li>" for s in phrases["how"][:3])
    routes = pick_routes(lang)
    routes_html = "".join(f"<li>{html.escape(a)} -> {html.escape(b)}</li>" for a,b in routes)

    section = f'''
<!-- GOYERV-SEO: autogenerated section -->
<section class="goyerv-seo" lang="{html.escape(lang)}"{dir_attr}>
  <header class="hero">
    <h1>{headline}</h1>
    <p class="subtitle">{intro}</p>
    <a class="cta" href="/" rel="nofollow">{html.escape(phrases["cta"])}</a>
  </header>

  <figure class="hero-media">
    <img src="/seo/image/hero.jpg" alt="{html.escape(phrases["img_alt"])}" loading="lazy" width="1200" height="630">
    <figcaption>{html.escape(phrases["img_alt"])}</figcaption>
  </figure>

  <section class="benefits">
    <h2>Benefits</h2>
    <ul>{benefits}</ul>
  </section>

  <section class="how-it-works">
    <h2>How it works</h2>
    <ol>{how_steps}</ol>
  </section>

  <section class="routes">
    <h2>{html.escape(phrases["routes_label"])}</h2>
    <ul>{routes_html}</ul>
  </section>

  <section class="faq">
    <h2>{html.escape(phrases["faq_label"])}</h2>
    {''.join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in phrases["faq"])}
  </section>

  <p class="redirect-note">{html.escape(phrases.get("cta2", "Open the app"))} in 3s...</p>
</section>
<!-- /GOYERV-SEO -->
'''.strip()
    return section

def inject_styles(head_html: str) -> str:
    if "/* GOYERV-SEO styles */" in head_html:
        return head_html
    css = '''
<style>
/* GOYERV-SEO styles */
.goyerv-seo { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.65; }
.goyerv-seo .hero h1 { font-size: 2rem; margin: 0 0 .5rem; }
.goyerv-seo .subtitle { color: #444; margin: 0 0 1rem; }
.goyerv-seo .cta { display: inline-block; padding: .6rem 1rem; border-radius: 12px; box-shadow: 0 1px 6px rgba(0,0,0,.08); text-decoration: none; border: 1px solid #ddd; }
.goyerv-seo .hero-media { margin: 1rem 0; }
.goyerv-seo .hero-media img { width: 100%; height: auto; border-radius: 12px; }
.goyerv-seo .benefits ul, .goyerv-seo .routes ul { padding-inline-start: 1.2rem; }
.goyerv-seo .how-it-works ol { padding-inline-start: 1.2rem; }
.goyerv-seo details { margin: .5rem 0; }
.goyerv-seo .redirect-note { color: #666; margin-top: 1rem; font-size: .95rem; }
</style>
'''.strip()
    return head_html.replace("</head>", css + "\n</head>")

def delay_redirects(body_html: str) -> str:
    return REDIR_PATTERN.sub(lambda m: f"setTimeout(function(){{ {m.group(0)} }}, 3000);", body_html)

def process_file(path: Path) -> tuple[bool, str]:
    orig = path.read_text(encoding="utf-8", errors="ignore")
    if "<!-- GOYERV-SEO: autogenerated section -->" in orig:
        return False, f"[SKIP] Already enhanced: {path}"

    lang_match = HTML_LANG_PATTERN.search(orig)
    lang = (lang_match.group(1) if lang_match else path.parent.name)

    desc_match = META_DESC_PATTERN.search(orig)
    og_title_match = OG_TITLE_PATTERN.search(orig)
    description = (desc_match.group(1).strip() if desc_match else "").replace("\n", " ").strip()
    og_title = (og_title_match.group(1).strip() if og_title_match else "").replace("\n", " ").strip()

    seo_section = build_seo_section(lang, description, og_title)

    if "</head>" in orig:
        head_injected = inject_styles(orig)
    else:
        head_injected = orig

    if BODY_OPEN_PATTERN.search(head_injected):
        enhanced = BODY_OPEN_PATTERN.sub(r"\1\n" + seo_section + "\n", head_injected, count=1)
    else:
        enhanced = head_injected + "\n" + seo_section

    enhanced = delay_redirects(enhanced)

    path.write_text(enhanced, encoding="utf-8")
    return True, f"[UPDATED] {path}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Path to the web/ root folder that contains language subfolders")
    parser.add_argument("--ext", default=".html", help="File extension to process (default: .html)")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"[ERROR] Root not found: {root}")
        sys.exit(1)

    updated = 0
    skipped = 0
    for lang_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        for html_file in lang_dir.rglob(f"*{args.ext}"):
            ok, msg = process_file(html_file)
            print(msg)
            if ok: updated += 1
            else: skipped += 1

    print(f"\nDone. Updated: {updated}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
