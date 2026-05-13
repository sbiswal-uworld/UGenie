import re
import html
import sys

def extract_seo(filepath, label):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else 'NOT FOUND'

    # Meta description - try multiple attribute orderings
    meta_match = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        content, re.IGNORECASE | re.DOTALL
    )
    if not meta_match:
        meta_match = re.search(
            r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']',
            content, re.IGNORECASE | re.DOTALL
        )
    meta_desc = html.unescape(meta_match.group(1).strip()) if meta_match else 'NOT FOUND'

    # OG description fallback
    og_desc = 'NOT FOUND'
    og_match = re.search(
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
        content, re.IGNORECASE | re.DOTALL
    )
    if og_match:
        og_desc = html.unescape(og_match.group(1).strip())

    # H1
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    h1_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_matches]
    h1_clean = [h for h in h1_clean if h]

    # H2
    h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)
    h2_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in h2_matches]
    h2_clean = [h for h in h2_clean if h]

    # H3
    h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.IGNORECASE | re.DOTALL)
    h3_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in h3_matches]
    h3_clean = [h for h in h3_clean if h]

    # Word count - strip scripts/styles first, then tags
    no_scripts = re.sub(r'<(script|style)[^>]*>.*?</(script|style)>', ' ', content, flags=re.IGNORECASE | re.DOTALL)
    text_only = re.sub(r'<[^>]+>', ' ', no_scripts)
    text_only = re.sub(r'&[a-zA-Z#0-9]+;', ' ', text_only)
    text_only = re.sub(r'\s+', ' ', text_only)
    words = [w for w in text_only.split() if len(w) > 1 and not w.startswith('{') and not w.startswith('/')]
    word_count = len(words)

    # Internal links - count unique hrefs pointing to mygunturmp.in or relative paths
    internal_links = re.findall(
        r'href=["\']((?:https?://(?:www\.)?mygunturmp\.in|/)[^"\'#\s]*)["\']',
        content, re.IGNORECASE
    )
    unique_internal = list(set(internal_links))

    # Canonical
    canonical_match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',
        content, re.IGNORECASE
    )
    canonical = canonical_match.group(1) if canonical_match else 'NOT FOUND'

    # Robots meta
    robots_match = re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'](.*?)["\']',
        content, re.IGNORECASE
    )
    robots = robots_match.group(1) if robots_match else 'NOT FOUND'

    # Schema / structured data
    schema_types = re.findall(r'"@type"\s*:\s*"([^"]+)"', content)

    # Open Graph
    og_title_match = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', content, re.IGNORECASE)
    og_title = html.unescape(og_title_match.group(1)) if og_title_match else 'NOT FOUND'

    # Print report
    print(f"\n{'='*60}")
    print(f"PAGE: {label}")
    print(f"{'='*60}")
    print(f"TITLE          : {title}")
    print(f"TITLE LENGTH   : {len(title)} chars")
    print(f"META DESC      : {meta_desc}")
    print(f"META DESC LEN  : {len(meta_desc)} chars")
    print(f"OG TITLE       : {og_title}")
    print(f"OG DESC        : {og_desc[:120]}..." if len(og_desc) > 120 else f"OG DESC        : {og_desc}")
    print(f"CANONICAL      : {canonical}")
    print(f"ROBOTS META    : {robots}")
    print(f"H1 COUNT       : {len(h1_clean)}")
    for i, h in enumerate(h1_clean, 1):
        print(f"  H1[{i}]        : {h[:120]}")
    print(f"H2 COUNT       : {len(h2_clean)}")
    for i, h in enumerate(h2_clean[:12], 1):
        print(f"  H2[{i:02d}]      : {h[:100]}")
    print(f"H3 COUNT       : {len(h3_clean)}")
    for i, h in enumerate(h3_clean[:12], 1):
        print(f"  H3[{i:02d}]      : {h[:100]}")
    print(f"WORD COUNT     : ~{word_count}")
    print(f"INTERNAL LINKS : {len(internal_links)} total, {len(unique_internal)} unique")
    print(f"SCHEMA TYPES   : {list(set(schema_types)) if schema_types else 'NONE'}")


extract_seo('C:/Users/sbiswal/Downloads/UGenie/page_home.html', 'HOMEPAGE /')
extract_seo('C:/Users/sbiswal/Downloads/UGenie/page_impact.html', 'MY IMPACT /my-impact/')
extract_seo('C:/Users/sbiswal/Downloads/UGenie/page_foundation.html', 'OUR FOUNDATION /our-foundation/')
extract_seo('C:/Users/sbiswal/Downloads/UGenie/page_contact.html', 'CONTACT US /contact-us/')
