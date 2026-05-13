import re
import html

def get_visible_text(filepath):
    """Extract visible body text, stripping scripts, styles, nav, footer boilerplate."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Remove script and style blocks
    cleaned = re.sub(r'<(script|style|noscript)[^>]*>.*?</(script|style|noscript)>', ' ', content, flags=re.IGNORECASE | re.DOTALL)
    # Remove HTML comments
    cleaned = re.sub(r'<!--.*?-->', ' ', cleaned, flags=re.DOTALL)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', ' ', cleaned)
    # Decode entities
    text = html.unescape(text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text, content

def check_template_strings(content):
    """Flag unrendered JS template literals."""
    templates = re.findall(r'\$\{[^}]+\}', content)
    return list(set(templates))

def check_duplicate_titles(pages):
    titles = {}
    for label, title in pages:
        if title not in titles:
            titles[title] = []
        titles[title].append(label)
    return {t: pages for t, pages in titles.items() if len(pages) > 1}

def check_meta_length_issues(pages):
    issues = []
    for label, title, meta in pages:
        if len(title) < 30:
            issues.append(f"[TOO SHORT] {label}: title {len(title)} chars")
        if len(title) > 60:
            issues.append(f"[TOO LONG]  {label}: title {len(title)} chars")
        if len(meta) < 120:
            issues.append(f"[TOO SHORT] {label}: meta desc {len(meta)} chars")
        if len(meta) > 160:
            issues.append(f"[TOO LONG]  {label}: meta desc {len(meta)} chars (Google truncates at ~155-160)")
    return issues

def count_visible_words(text):
    words = [w for w in text.split() if len(w) > 1]
    return len(words)

def check_keyword_presence(text, keywords, page_label):
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

    # Experience signals
    if any(w in text_lower for w in ['inaugurated', 'visited', 'attended', 'met with', 'personally', 'i have', 'our team']):
        signals.append("EXPERIENCE: First-hand action language detected")
    if re.search(r'\d{4}', text):
        signals.append("EXPERIENCE: Year references found (temporal anchoring)")

    # Expertise signals
    if any(w in text_lower for w in ['dr.', 'phd', 'mbbs', 'minister', 'member of parliament', 'mp', 'iit', 'aiims']):
        signals.append("EXPERTISE: Professional credentials/title referenced")
    if any(w in text_lower for w in ['policy', 'parliament', 'lok sabha', 'budget', 'ministry', 'committee']):
        signals.append("EXPERTISE: Parliamentary/policy domain signals")

    # Authoritativeness signals
    if any(w in content_lower for w in ['press', 'media', 'news', 'article', 'report', 'published']):
        signals.append("AUTHORITY: Press/media coverage referenced")
    if re.search(r'schema.*person|person.*schema', content_lower):
        signals.append("AUTHORITY: Person schema markup (not detected here — see schema types)")
    if any(w in text_lower for w in ['award', 'recognized', 'honour', 'felicitated']):
        signals.append("AUTHORITY: Awards/recognition mentioned")

    # Trustworthiness signals
    if any(w in text_lower for w in ['contact', 'address', 'phone', 'email', '@', 'reach us']):
        signals.append("TRUST: Contact information present")
    if 'https' in content_lower[:500]:
        signals.append("TRUST: HTTPS (secure connection)")
    if any(w in text_lower for w in ['privacy', 'terms', 'disclaimer']):
        signals.append("TRUST: Legal/policy pages referenced")
    if 'donation' in text_lower or 'transparent' in text_lower:
        signals.append("TRUST: Financial transparency signals (donation/transparency)")

    return signals


pages = [
    ('page_home.html', 'HOMEPAGE /'),
    ('page_impact.html', 'MY IMPACT /my-impact/'),
    ('page_foundation.html', 'OUR FOUNDATION /our-foundation/'),
    ('page_contact.html', 'CONTACT US /contact-us/'),
]

base = 'C:/Users/sbiswal/Downloads/UGenie/'

title_list = []
meta_length_check = []

for filename, label in pages:
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

    # Primary keyword checks per page
    if 'home' in filename:
        kw_targets = ['guntur mp', 'chandra sekhar pemmasani', 'public grievance', 'guntur']
    elif 'impact' in filename:
        kw_targets = ['pemmasani', 'guntur mp', 'public service', 'community', 'parliament']
    elif 'foundation' in filename:
        kw_targets = ['pemmasani foundation', 'flood relief', 'education', 'healthcare', 'social welfare']
    else:
        kw_targets = ['contact', 'pemmasani', 'guntur', 'reach out']

    kw_counts = check_keyword_presence(visible_text, kw_targets, label)

    print(f"\n{'='*60}")
    print(f"DEEP ANALYSIS: {label}")
    print(f"{'='*60}")
    print(f"VISIBLE WORD COUNT (body text only): ~{word_count}")
    print(f"\n--- KEYWORD DENSITY CHECK ---")
    for kw, count in kw_counts.items():
        density = (count / word_count * 100) if word_count > 0 else 0
        print(f"  '{kw}': {count} occurrences ({density:.2f}%)")
    print(f"\n--- TEMPLATE STRING ISSUES ---")
    if template_issues:
        for t in template_issues[:10]:
            print(f"  UNRENDERED: {t}")
    else:
        print("  None detected")
    print(f"\n--- E-E-A-T SIGNALS ---")
    for s in eeat:
        print(f"  + {s}")
    if not eeat:
        print("  No strong E-E-A-T signals found")

    # Sample 400 chars of visible text for manual review
    print(f"\n--- VISIBLE TEXT SAMPLE (first 500 chars) ---")
    print(f"  {visible_text[:500]}")

    title_list.append((label, title))
    meta_length_check.append((label, title, meta))

print("\n\n" + "="*60)
print("CROSS-PAGE CHECKS")
print("="*60)

print("\n--- DUPLICATE TITLE CHECK ---")
dupes = check_duplicate_titles(title_list)
if dupes:
    for t, pages in dupes.items():
        print(f"  DUPLICATE: '{t}' on: {pages}")
else:
    print("  No duplicate titles detected")

print("\n--- META TAG LENGTH ISSUES ---")
issues = check_meta_length_issues(meta_length_check)
if issues:
    for i in issues:
        print(f"  {i}")
else:
    print("  All titles and meta descriptions within optimal ranges")

print("\n--- TITLE KEYWORD ALIGNMENT CHECK ---")
for label, title in title_list:
    has_name = 'pemmasani' in title.lower() or 'guntur' in title.lower() or 'chandra' in title.lower()
    print(f"  {label}: Contains MP name or Guntur? {'YES' if has_name else 'NO - MISSING BRAND/GEO'} | '{title}'")
