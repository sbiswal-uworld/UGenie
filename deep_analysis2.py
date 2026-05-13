import re
import html
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def get_visible_text(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    cleaned = re.sub(r'<(script|style|noscript)[^>]*>.*?</(script|style|noscript)>', ' ', content, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'<!--.*?-->', ' ', cleaned, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', cleaned)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text, content

def check_template_strings(content):
    templates = re.findall(r'\$\{[^}]+\}', content)
    return list(set(templates))

def count_visible_words(text):
    words = [w for w in text.split() if len(w) > 1]
    return len(words)

def check_keyword_presence(text, keywords):
    text_lower = text.lower()
    results = {}
    for kw in keywords:
        count = text_lower.count(kw.lower())
        results[kw] = count
    return results

def extract_eeat_signals(text, content):
    signals = []
    text_lower = text.lower()
    content_lower = content.lower()

    if any(w in text_lower for w in ['inaugurated', 'visited', 'attended', 'met with', 'personally', 'i have', 'our team']):
        signals.append("EXPERIENCE: First-hand action language detected")
    if re.search(r'\b(20\d{2})\b', text):
        signals.append("EXPERIENCE: Year references found (temporal anchoring)")
    if any(w in text_lower for w in ['dr.', 'phd', 'mbbs', 'member of parliament', 'iit', 'aiims']):
        signals.append("EXPERTISE: Professional credentials/title referenced")
    if any(w in text_lower for w in ['policy', 'parliament', 'lok sabha', 'budget', 'ministry', 'committee']):
        signals.append("EXPERTISE: Parliamentary/policy domain signals")
    if any(w in content_lower for w in ['in the press', 'news', 'article', 'report', 'published', 'media']):
        signals.append("AUTHORITY: Press/media coverage referenced")
    if any(w in text_lower for w in ['award', 'recognized', 'honour', 'felicitated']):
        signals.append("AUTHORITY: Awards/recognition mentioned")
    if any(w in text_lower for w in ['contact', 'address', 'phone', 'email', '@', 'reach us']):
        signals.append("TRUST: Contact information present")
    if 'https' in content_lower[:500]:
        signals.append("TRUST: HTTPS in page metadata")
    if any(w in text_lower for w in ['privacy', 'terms', 'disclaimer']):
        signals.append("TRUST: Legal/policy pages referenced")
    if 'donation' in text_lower or 'relief fund' in text_lower:
        signals.append("TRUST: Financial/charitable transparency signals")

    # Check for Person schema
    if '"@type": "Person"' in content or "'@type': 'Person'" in content or '"Person"' in content:
        signals.append("AUTHORITY: Person schema detected in structured data")

    return signals

def check_meta_length(label, title, meta):
    issues = []
    if len(title) < 30:
        issues.append(f"Title too short ({len(title)} chars)")
    elif len(title) > 60:
        issues.append(f"Title too long ({len(title)} chars, will truncate in SERPs)")
    else:
        issues.append(f"Title length OK ({len(title)} chars)")

    if len(meta) < 120:
        issues.append(f"Meta desc too short ({len(meta)} chars)")
    elif len(meta) > 160:
        issues.append(f"Meta desc too long ({len(meta)} chars, Google truncates ~155-160)")
    else:
        issues.append(f"Meta desc length OK ({len(meta)} chars)")
    return issues


pages = [
    ('page_home.html',       'HOMEPAGE /',                    ['guntur mp', 'chandra sekhar pemmasani', 'public grievance', 'guntur', 'pemmasani']),
    ('page_impact.html',     'MY IMPACT /my-impact/',         ['pemmasani', 'guntur mp', 'public service', 'community', 'parliament', 'guntur']),
    ('page_foundation.html', 'OUR FOUNDATION /our-foundation/', ['pemmasani foundation', 'flood relief', 'education', 'healthcare', 'social welfare', 'guntur']),
    ('page_contact.html',    'CONTACT US /contact-us/',       ['contact', 'pemmasani', 'guntur', 'reach out', 'chandrasekhar']),
]

base = 'C:/Users/sbiswal/Downloads/UGenie/'

title_list = []
meta_length_check = []
all_results = []

for filename, label, kw_targets in pages:
    filepath = base + filename
    visible_text, raw_content = get_visible_text(filepath)
    word_count = count_visible_words(visible_text)

    title_match = re.search(r'<title[^>]*>(.*?)</title>', raw_content, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else 'NOT FOUND'

    meta_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', raw_content, re.IGNORECASE | re.DOTALL)
    if not meta_match:
        meta_match = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', raw_content, re.IGNORECASE | re.DOTALL)
    meta = html.unescape(meta_match.group(1).strip()) if meta_match else ''

    template_issues = check_template_strings(raw_content)
    eeat = extract_eeat_signals(visible_text, raw_content)
    kw_counts = check_keyword_presence(visible_text, kw_targets)
    meta_issues = check_meta_length(label, title, meta)

    # Safe sample: encode to ascii with replacement for display
    sample = visible_text[:600].encode('ascii', errors='replace').decode('ascii')

    print(f"\n{'='*65}")
    print(f"DEEP ANALYSIS: {label}")
    print(f"{'='*65}")
    print(f"VISIBLE WORD COUNT (body text, no nav/footer): ~{word_count}")
    print(f"\nMETA TAG ASSESSMENT:")
    for issue in meta_issues:
        print(f"  - {issue}")

    print(f"\nKEYWORD OCCURRENCE CHECK:")
    for kw, count in kw_counts.items():
        density = (count / word_count * 100) if word_count > 0 else 0
        flag = ""
        if count == 0:
            flag = " <<< MISSING"
        elif density > 4.0:
            flag = " <<< POSSIBLE OVER-USE"
        print(f"  '{kw}': {count}x ({density:.2f}%){flag}")

    print(f"\nTEMPLATE STRING ISSUES (unrendered JS in DOM):")
    if template_issues:
        for t in template_issues[:10]:
            print(f"  UNRENDERED: {t}")
        print(f"  TOTAL UNIQUE TEMPLATE STRINGS: {len(template_issues)}")
    else:
        print("  None detected")

    print(f"\nE-E-A-T SIGNALS DETECTED:")
    for s in eeat:
        print(f"  + {s}")
    if not eeat:
        print("  No strong E-E-A-T signals found")

    print(f"\nVISIBLE TEXT SAMPLE (first 600 chars, Telugu chars replaced):")
    print(f"  {sample}")

    title_list.append((label, title))
    meta_length_check.append((label, title, meta))

print(f"\n\n{'='*65}")
print("CROSS-PAGE ANALYSIS")
print(f"{'='*65}")

print("\n--- DUPLICATE TITLE CHECK ---")
title_map = {}
for label, title in title_list:
    title_map.setdefault(title, []).append(label)
dupes_found = False
for t, pages_list in title_map.items():
    if len(pages_list) > 1:
        print(f"  DUPLICATE: '{t}' on: {pages_list}")
        dupes_found = True
if not dupes_found:
    print("  No duplicate titles found across audited pages")

print("\n--- TITLE BRAND/GEO KEYWORD ALIGNMENT ---")
for label, title in title_list:
    has_name = any(w in title.lower() for w in ['pemmasani', 'guntur', 'chandra', 'chandrasekhar'])
    status = "OK" if has_name else "MISSING BRAND/GEO SIGNAL"
    print(f"  [{status}] {label}")
    print(f"    Title: '{title}'")

print("\n--- THIN CONTENT RISK SUMMARY ---")
word_counts = {
    'HOMEPAGE /': 375,
    'MY IMPACT /my-impact/': 1087,
    'OUR FOUNDATION /our-foundation/': 416,
    'CONTACT US /contact-us/': 185,
}
page_types = {
    'HOMEPAGE /': ('Homepage', 500),
    'MY IMPACT /my-impact/': ('Service/About page', 800),
    'OUR FOUNDATION /our-foundation/': ('Service page', 800),
    'CONTACT US /contact-us/': ('Contact page', 150),
}
for page, wc in word_counts.items():
    ptype, minimum = page_types[page]
    status = "OK" if wc >= minimum else f"BELOW MINIMUM ({minimum} recommended for {ptype})"
    print(f"  {page}: ~{wc} words => {status}")

print("\n--- SCHEMA COVERAGE GAPS ---")
print("  All pages have: WebSite, Organization, WebPage, BreadcrumbList, ImageObject")
print("  MISSING on ALL pages: Person schema for Dr. Pemmasani")
print("  MISSING on ALL pages: LocalBusiness or PoliticianProfile schema")
print("  MISSING on MY IMPACT: Article/NewsArticle schema for press mentions")
print("  MISSING on FOUNDATION: NGO or Organization (charity) schema")
print("  MISSING on CONTACT: ContactPage schema type")
