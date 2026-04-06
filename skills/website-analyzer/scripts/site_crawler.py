#!/usr/bin/env python3
"""
Site Crawler — Playwright-based website crawler for website-analyzer skill.
Crawls a website up to depth N, captures screenshots, extracts HTML/meta/links/perf metrics.
Outputs structured JSON + screenshots folder.

Usage:
    python site_crawler.py <URL> [--depth 2] [--max-pages 50] [--delay 1.5] [--output ./output] [--timeout 15]
"""

import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright non installé. Exécuter:")
    print("  pip install playwright && playwright install chromium")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 non installé. Exécuter:")
    print("  pip install beautifulsoup4")
    sys.exit(1)


def normalize_url(url):
    """Normalize URL for deduplication."""
    parsed = urlparse(url)
    # Remove trailing slash, fragment, and common tracking params
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def classify_page(url, title="", html=""):
    """Classify a page by its strategic importance."""
    url_lower = url.lower()
    title_lower = (title or "").lower()
    html_lower = (html[:5000] if html else "").lower()

    # Priority levels: 1 (highest) to 5 (lowest)
    # Conversion pages
    if any(kw in url_lower for kw in [
        "checkout", "panier", "cart", "order", "commande",
        "signup", "register", "inscription", "pricing", "tarif", "prix"
    ]):
        return "conversion", 1

    # Product/Service pages
    if any(kw in url_lower for kw in [
        "product", "produit", "service", "solution", "offre",
        "shop", "boutique", "catalogue"
    ]):
        return "product", 2

    # Landing pages
    if any(kw in url_lower for kw in [
        "landing", "promo", "offer", "demo", "essai", "trial"
    ]):
        return "landing", 2

    # About / Brand pages
    if any(kw in url_lower for kw in [
        "about", "a-propos", "qui-sommes", "equipe", "team",
        "histoire", "valeur", "mission"
    ]):
        return "brand", 3

    # Contact
    if any(kw in url_lower for kw in ["contact", "nous-contacter"]):
        return "contact", 3

    # Blog / Content
    if any(kw in url_lower for kw in [
        "blog", "article", "actualite", "news", "ressource"
    ]):
        return "blog", 4

    # Legal pages
    if any(kw in url_lower for kw in [
        "mention", "legal", "cgv", "cgu", "confidentialite",
        "privacy", "cookie", "terms", "conditions"
    ]):
        return "legal", 4

    # FAQ / Help
    if any(kw in url_lower for kw in ["faq", "aide", "help", "support"]):
        return "help", 4

    # Homepage
    parsed = urlparse(url)
    if parsed.path in ("/", "", "/index.html", "/index.php", "/fr", "/en"):
        return "homepage", 1

    return "other", 5


def detect_technologies(page, html, soup):
    """Detect technologies, frameworks, CMS, analytics from page content."""
    tech = {
        "cms": [],
        "frameworks": [],
        "analytics": [],
        "cdn": [],
        "libraries": [],
        "server": "",
        "hosting_hints": [],
    }

    html_lower = html.lower()

    # CMS Detection
    cms_signatures = {
        "WordPress": ['wp-content/', 'wp-includes/', 'wp-json', 'wordpress'],
        "Shopify": ['cdn.shopify.com', 'shopify.com', 'Shopify.theme'],
        "Wix": ['wix.com', 'parastorage.com', '_wix_browser_sess'],
        "Squarespace": ['squarespace.com', 'sqsp.com', 'squarespace-cdn'],
        "Webflow": ['webflow.com', 'wf-cdn', 'webflow.js'],
        "PrestaShop": ['prestashop', 'presta-shop', '/modules/ps_'],
        "Magento": ['magento', 'mage/', 'varien/js'],
        "Drupal": ['drupal', '/sites/default/files', 'drupal.settings'],
        "Joomla": ['joomla', '/components/com_', '/media/jui/'],
        "Ghost": ['ghost.org', 'ghost-'],
        "WooCommerce": ['woocommerce', 'wc-blocks', 'wc-cart'],
    }
    for name, sigs in cms_signatures.items():
        if any(sig.lower() in html_lower for sig in sigs):
            tech["cms"].append(name)

    # JS Framework Detection
    framework_signatures = {
        "React": ['react', 'reactDOM', '__NEXT_DATA__', '_next/'],
        "Vue.js": ['vue.js', 'vue.min.js', '__vue__', 'vue-router'],
        "Angular": ['ng-version', 'angular', 'ng-app'],
        "Svelte": ['svelte', '__svelte'],
        "Next.js": ['__NEXT_DATA__', '_next/', 'next/image'],
        "Nuxt.js": ['__NUXT__', 'nuxt', '_nuxt/'],
        "Gatsby": ['gatsby', '___gatsby'],
        "jQuery": ['jquery', 'jQuery'],
        "Alpine.js": ['x-data', 'x-show', 'alpine'],
        "HTMX": ['htmx.org', 'hx-get', 'hx-post'],
        "Tailwind CSS": ['tailwindcss', 'tw-'],
        "Bootstrap": ['bootstrap.min', 'bootstrap.css', 'bootstrap.js'],
    }
    for name, sigs in framework_signatures.items():
        if any(sig.lower() in html_lower for sig in sigs):
            tech["frameworks"].append(name)

    # Analytics/Tracking Detection
    analytics_signatures = {
        "Google Analytics (GA4)": ['gtag', 'google-analytics', 'G-', 'googletagmanager'],
        "Google Tag Manager": ['googletagmanager.com', 'gtm.js'],
        "Facebook Pixel": ['fbq(', 'connect.facebook.net', 'facebook.com/tr'],
        "Hotjar": ['hotjar.com', 'hj(', 'hjSiteSettings'],
        "Matomo/Piwik": ['matomo', 'piwik'],
        "Plausible": ['plausible.io'],
        "Fathom": ['usefathom.com'],
        "Segment": ['segment.com', 'analytics.js'],
        "Mixpanel": ['mixpanel.com', 'mixpanel.init'],
        "Amplitude": ['amplitude.com', 'amplitude.getInstance'],
        "Microsoft Clarity": ['clarity.ms'],
        "TikTok Pixel": ['analytics.tiktok.com'],
        "Pinterest Tag": ['pintrk(', 'ct.pinterest.com'],
        "LinkedIn Insight": ['snap.licdn.com', 'linkedin.com/px'],
        "Crisp": ['crisp.chat', 'CRISP_WEBSITE_ID'],
        "Intercom": ['intercom.com', 'intercomSettings'],
        "Zendesk": ['zendesk.com', 'zdassets.com'],
        "HubSpot": ['hubspot.com', 'hs-scripts', 'hbspt'],
        "Drift": ['drift.com', 'driftt'],
    }
    for name, sigs in analytics_signatures.items():
        if any(sig.lower() in html_lower for sig in sigs):
            tech["analytics"].append(name)

    # CDN Detection
    cdn_signatures = {
        "Cloudflare": ['cdnjs.cloudflare.com', 'cdn-cgi/', 'cf-ray'],
        "AWS CloudFront": ['cloudfront.net'],
        "Akamai": ['akamai', 'akamaihd.net', 'akamaized.net'],
        "Fastly": ['fastly.net', 'fastly.com'],
        "Vercel": ['vercel.app', 'vercel.com', 'v0.dev'],
        "Netlify": ['netlify.app', 'netlify.com'],
        "Google CDN": ['googleapis.com', 'gstatic.com'],
        "jsDelivr": ['cdn.jsdelivr.net'],
        "unpkg": ['unpkg.com'],
        "KeyCDN": ['kxcdn.com'],
    }
    for name, sigs in cdn_signatures.items():
        if any(sig.lower() in html_lower for sig in sigs):
            tech["cdn"].append(name)

    # JS-based deeper detection
    try:
        js_tech = page.evaluate("""() => {
            const detected = [];
            if (window.React || document.querySelector('[data-reactroot]')) detected.push('React');
            if (window.Vue || document.querySelector('[data-v-]')) detected.push('Vue.js');
            if (window.angular || document.querySelector('[ng-version]')) detected.push('Angular');
            if (window.__NEXT_DATA__) detected.push('Next.js');
            if (window.__NUXT__) detected.push('Nuxt.js');
            if (window.jQuery || window.$) detected.push('jQuery');
            if (window.Shopify) detected.push('Shopify');
            if (window.wp) detected.push('WordPress');
            if (window.ga || window.gtag) detected.push('Google Analytics');
            if (window.fbq) detected.push('Facebook Pixel');
            if (window.hj) detected.push('Hotjar');
            if (window.dataLayer) detected.push('Google Tag Manager');
            return detected;
        }""")
        for t in js_tech:
            if t not in tech["frameworks"] and t not in tech["analytics"] and t not in tech["cms"]:
                tech["libraries"].append(t)
    except Exception:
        pass

    return tech


def extract_resources_breakdown(page):
    """Extract CSS/JS/image resource details via Performance API."""
    try:
        resources = page.evaluate("""() => {
            const entries = performance.getEntriesByType('resource');
            const breakdown = {
                css: [], js: [], images: [], fonts: [], other: [],
                total_css_bytes: 0, total_js_bytes: 0, total_img_bytes: 0,
                total_font_bytes: 0, total_requests: entries.length,
                third_party_domains: [],
                render_blocking: []
            };
            const currentDomain = window.location.hostname;
            const thirdPartyDomains = new Set();

            entries.forEach(e => {
                const entry = {
                    name: e.name.split('?')[0].split('#')[0],
                    size: e.transferSize || 0,
                    duration: Math.round(e.duration),
                    type: e.initiatorType
                };

                // Detect third-party
                try {
                    const url = new URL(e.name);
                    if (url.hostname !== currentDomain && !url.hostname.endsWith('.' + currentDomain)) {
                        thirdPartyDomains.add(url.hostname);
                    }
                } catch(err) {}

                if (e.name.match(/\\.css(\\?|$)/i) || e.initiatorType === 'css') {
                    breakdown.css.push(entry);
                    breakdown.total_css_bytes += entry.size;
                } else if (e.name.match(/\\.js(\\?|$)/i) || e.initiatorType === 'script') {
                    breakdown.js.push(entry);
                    breakdown.total_js_bytes += entry.size;
                } else if (e.name.match(/\\.(png|jpg|jpeg|gif|svg|webp|avif|ico)(\\?|$)/i) || e.initiatorType === 'img') {
                    breakdown.images.push(entry);
                    breakdown.total_img_bytes += entry.size;
                } else if (e.name.match(/\\.(woff2?|ttf|otf|eot)(\\?|$)/i) || e.initiatorType === 'font') {
                    breakdown.fonts.push(entry);
                    breakdown.total_font_bytes += entry.size;
                } else {
                    breakdown.other.push(entry);
                }
            });

            breakdown.third_party_domains = Array.from(thirdPartyDomains);

            return {
                css_count: breakdown.css.length,
                js_count: breakdown.js.length,
                img_count: breakdown.images.length,
                font_count: breakdown.fonts.length,
                total_requests: breakdown.total_requests,
                total_css_bytes: breakdown.total_css_bytes,
                total_js_bytes: breakdown.total_js_bytes,
                total_img_bytes: breakdown.total_img_bytes,
                total_font_bytes: breakdown.total_font_bytes,
                third_party_domains: breakdown.third_party_domains.slice(0, 50),
                third_party_count: thirdPartyDomains.size,
                top_heavy_js: breakdown.js.sort((a,b) => b.size - a.size).slice(0, 10).map(e => ({name: e.name.split('/').pop(), size: e.size, duration: e.duration})),
                top_heavy_css: breakdown.css.sort((a,b) => b.size - a.size).slice(0, 5).map(e => ({name: e.name.split('/').pop(), size: e.size})),
            };
        }""")
        return resources
    except Exception:
        return {}


def extract_structured_data_details(soup):
    """Extract full structured data (JSON-LD) content, not just presence."""
    structured_data = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json as _json
            content = _json.loads(script.string)
            if isinstance(content, list):
                for item in content:
                    structured_data.append({
                        "type": item.get("@type", "Unknown"),
                        "data_keys": list(item.keys())[:20],
                    })
            elif isinstance(content, dict):
                structured_data.append({
                    "type": content.get("@type", "Unknown"),
                    "data_keys": list(content.keys())[:20],
                })
        except Exception:
            structured_data.append({"type": "parse_error", "raw_length": len(script.string or "")})
    return structured_data


def extract_content_metrics(soup, html):
    """Extract content quality metrics: word count, text-to-HTML ratio, reading time."""
    text = soup.get_text(separator=" ", strip=True)
    words = text.split()
    word_count = len(words)
    html_size = len(html)
    text_size = len(text)
    text_to_html_ratio = round(text_size / html_size * 100, 1) if html_size > 0 else 0
    reading_time_min = round(word_count / 250, 1)  # 250 wpm average

    return {
        "word_count": word_count,
        "text_size_bytes": text_size,
        "html_size_bytes": html_size,
        "text_to_html_ratio_pct": text_to_html_ratio,
        "reading_time_min": reading_time_min,
    }


def extract_security_headers(response):
    """Extract security-related HTTP headers from response."""
    headers = {}
    security_headers_to_check = [
        "strict-transport-security",
        "content-security-policy",
        "x-content-type-options",
        "x-frame-options",
        "x-xss-protection",
        "referrer-policy",
        "permissions-policy",
        "cross-origin-opener-policy",
        "cross-origin-embedder-policy",
        "cross-origin-resource-policy",
    ]
    all_headers = response.all_headers() if response else {}
    for h in security_headers_to_check:
        headers[h] = all_headers.get(h, None)

    headers["server"] = all_headers.get("server", "")
    headers["x-powered-by"] = all_headers.get("x-powered-by", "")
    headers["content-encoding"] = all_headers.get("content-encoding", "")
    headers["cache-control"] = all_headers.get("cache-control", "")
    headers["vary"] = all_headers.get("vary", "")

    return headers


def extract_cookies(page):
    """Extract cookies set by the page (first-party and third-party indicators)."""
    try:
        cookies = page.context.cookies()
        cookie_summary = []
        for c in cookies[:50]:
            cookie_summary.append({
                "name": c.get("name", ""),
                "domain": c.get("domain", ""),
                "secure": c.get("secure", False),
                "httpOnly": c.get("httpOnly", False),
                "sameSite": c.get("sameSite", ""),
                "expires": c.get("expires", -1),
            })
        return cookie_summary
    except Exception:
        return []


def extract_social_links(soup, links_external):
    """Extract social media profile links."""
    social_platforms = {
        "facebook.com": "Facebook",
        "twitter.com": "Twitter/X",
        "x.com": "Twitter/X",
        "instagram.com": "Instagram",
        "linkedin.com": "LinkedIn",
        "youtube.com": "YouTube",
        "tiktok.com": "TikTok",
        "pinterest.com": "Pinterest",
        "github.com": "GitHub",
        "discord.gg": "Discord",
        "discord.com": "Discord",
        "t.me": "Telegram",
        "wa.me": "WhatsApp",
    }
    found = {}
    for link in links_external:
        url_lower = link.get("url", "").lower()
        for domain, name in social_platforms.items():
            if domain in url_lower and name not in found:
                found[name] = link["url"]
    return found


def extract_contact_info(soup):
    """Extract contact information (emails, phones, addresses)."""
    import re as _re
    text = soup.get_text(separator=" ")

    # Emails
    emails = list(set(_re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))
    emails = [e for e in emails if not e.endswith('.png') and not e.endswith('.jpg')][:10]

    # Phone numbers (FR + international)
    phones = list(set(_re.findall(
        r'(?:\+33|0033|0)\s*[1-9](?:[\s.-]*\d{2}){4}|'
        r'\+\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}',
        text
    )))[:10]

    # mailto: links
    mailto_links = [a["href"].replace("mailto:", "").split("?")[0]
                    for a in soup.find_all("a", href=_re.compile(r'^mailto:'))]

    # tel: links
    tel_links = [a["href"].replace("tel:", "").strip()
                 for a in soup.find_all("a", href=_re.compile(r'^tel:'))]

    return {
        "emails": list(set(emails + mailto_links))[:10],
        "phones": list(set(phones + tel_links))[:10],
    }


def extract_page_data(page, url):
    """Extract structured data from a loaded page."""
    data = {
        "url": url,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": None,
        "title": "",
        "meta_description": "",
        "meta_keywords": "",
        "h1": [],
        "h2": [],
        "headings_structure": [],
        "links_internal": [],
        "links_external": [],
        "images": [],
        "ctas": [],
        "forms": [],
        "colors_detected": [],
        "fonts_detected": [],
        "has_favicon": False,
        "has_og_tags": False,
        "has_schema": False,
        "has_canonical": False,
        "has_robots_meta": False,
        "lang": "",
        "load_time_ms": 0,
        "dom_size": 0,
        "page_weight_bytes": 0,
        "classification": "",
        "priority": 5,
    }

    try:
        html = page.content()
        data["dom_size"] = len(html)
        soup = BeautifulSoup(html, "html.parser")

        # Title
        title_tag = soup.find("title")
        data["title"] = title_tag.get_text(strip=True) if title_tag else ""

        # Meta tags
        for meta in soup.find_all("meta"):
            name = (meta.get("name") or meta.get("property") or "").lower()
            content = meta.get("content", "")
            if name == "description":
                data["meta_description"] = content
            elif name == "keywords":
                data["meta_keywords"] = content
            elif name.startswith("og:"):
                data["has_og_tags"] = True
            elif name == "robots":
                data["has_robots_meta"] = True

        # Lang
        html_tag = soup.find("html")
        if html_tag:
            data["lang"] = html_tag.get("lang", "")

        # Headings
        for level in range(1, 7):
            tag = f"h{level}"
            for h in soup.find_all(tag):
                text = h.get_text(strip=True)[:200]
                data["headings_structure"].append({"level": level, "text": text})
                if level == 1:
                    data["h1"].append(text)
                elif level == 2:
                    data["h2"].append(text)

        # Links
        base_domain = urlparse(url).netloc
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)
            if parsed.scheme not in ("http", "https"):
                continue
            link_text = a.get_text(strip=True)[:100]
            if parsed.netloc == base_domain:
                data["links_internal"].append({
                    "url": full_url,
                    "text": link_text
                })
            else:
                data["links_external"].append({
                    "url": full_url,
                    "text": link_text
                })

        # Images
        for img in soup.find_all("img"):
            data["images"].append({
                "src": img.get("src", ""),
                "alt": img.get("alt", ""),
                "has_alt": bool(img.get("alt")),
            })

        # CTAs (buttons and links with action-like text)
        cta_patterns = re.compile(
            r"(acheter|buy|commander|order|essayer|try|démarrer|start|"
            r"s.inscrire|sign.?up|register|contact|devis|quote|"
            r"télécharger|download|en savoir|learn more|découvrir|"
            r"ajouter|add to|réserver|book)",
            re.IGNORECASE
        )
        for el in soup.find_all(["button", "a"]):
            text = el.get_text(strip=True)[:100]
            classes = " ".join(el.get("class", []))
            if cta_patterns.search(text) or "cta" in classes.lower() or "btn" in classes.lower():
                data["ctas"].append({
                    "tag": el.name,
                    "text": text,
                    "href": el.get("href", ""),
                    "classes": classes,
                })

        # Forms
        for form in soup.find_all("form"):
            fields = []
            for inp in form.find_all(["input", "select", "textarea"]):
                if inp.get("type") in ("hidden", "submit"):
                    continue
                fields.append({
                    "type": inp.get("type", inp.name),
                    "name": inp.get("name", ""),
                    "label": inp.get("placeholder", inp.get("aria-label", "")),
                    "required": inp.has_attr("required"),
                })
            data["forms"].append({
                "action": form.get("action", ""),
                "method": form.get("method", "GET"),
                "fields_count": len(fields),
                "fields": fields[:20],  # Limit
            })

        # Prices (extract from rendered DOM to catch JS-rendered prices)
        prices = []
        price_patterns = re.compile(r'(\d+[.,]\d{2})\s*[€$£]|[€$£]\s*(\d+[.,]\d{2})')
        for el in soup.find_all(class_=lambda c: c and any(kw in (c if isinstance(c, str) else " ".join(c)).lower() for kw in ["price", "prix", "money", "amount"])):
            text = el.get_text(strip=True)
            if text:
                prices.append(text[:50])
        # Also search raw text for price patterns
        page_text = soup.get_text()
        price_matches = price_patterns.findall(page_text)
        data["prices_detected"] = prices[:20]
        data["has_prices"] = len(prices) > 0 or len(price_matches) > 0

        # Stock indicators
        stock_keywords = ["stock", "disponible", "available", "rupture", "out of stock", "épuisé", "plus que"]
        stock_elements = []
        for el in soup.find_all(string=re.compile("|".join(stock_keywords), re.IGNORECASE)):
            stock_elements.append(el.strip()[:100])
        data["stock_indicators"] = stock_elements[:10]
        data["has_stock_info"] = len(stock_elements) > 0

        # Canonical
        canonical = soup.find("link", rel="canonical")
        data["has_canonical"] = canonical is not None

        # Schema.org
        for script in soup.find_all("script", type="application/ld+json"):
            data["has_schema"] = True
            break

        # Favicon
        favicon = soup.find("link", rel=lambda x: x and "icon" in x.lower() if isinstance(x, str) else any("icon" in v.lower() for v in (x or [])))
        data["has_favicon"] = favicon is not None

        # Classification
        data["classification"], data["priority"] = classify_page(
            url, data["title"], html
        )

    except Exception as e:
        data["error"] = str(e)

    return data


def extract_colors_and_fonts(page):
    """Extract computed colors and fonts from the page via JS."""
    try:
        result = page.evaluate("""() => {
            const colors = new Set();
            const fonts = new Set();
            const elements = document.querySelectorAll('*');
            const sample = Array.from(elements).slice(0, 500);

            sample.forEach(el => {
                const style = window.getComputedStyle(el);
                const bgColor = style.backgroundColor;
                const color = style.color;
                const font = style.fontFamily;

                if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)' && bgColor !== 'transparent') {
                    colors.add(bgColor);
                }
                if (color) {
                    colors.add(color);
                }
                if (font) {
                    // Extract first font name
                    const firstName = font.split(',')[0].trim().replace(/['"]/g, '');
                    fonts.add(firstName);
                }
            });

            return {
                colors: Array.from(colors).slice(0, 30),
                fonts: Array.from(fonts).slice(0, 10)
            };
        }""")
        return result.get("colors", []), result.get("fonts", [])
    except Exception:
        return [], []


def crawl_site(base_url, depth=2, max_pages=50, delay=1.5, output_dir="./output", timeout_min=15):
    """Main crawl function."""
    os.makedirs(output_dir, exist_ok=True)
    screenshots_dir = os.path.join(output_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    base_domain = urlparse(base_url).netloc
    visited = set()
    to_visit = [(normalize_url(base_url), 0)]  # (url, depth)
    results = []
    start_time = time.time()
    timeout_sec = timeout_min * 60

    print(f"[CRAWLER] Démarrage du crawl de {base_url}")
    print(f"[CRAWLER] Profondeur max: {depth}, Pages max: {max_pages}, Timeout: {timeout_min}min")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="fr-FR",
        )

        while to_visit and len(results) < max_pages:
            # Timeout check
            elapsed = time.time() - start_time
            if elapsed > timeout_sec:
                print(f"[CRAWLER] Timeout atteint ({timeout_min}min). Arrêt du crawl.")
                break

            # Sort by priority (lowest priority number first)
            to_visit.sort(key=lambda x: x[1])
            url, current_depth = to_visit.pop(0)

            normalized = normalize_url(url)
            if normalized in visited:
                continue
            visited.add(normalized)

            print(f"[CRAWLER] [{len(results)+1}/{max_pages}] Profondeur {current_depth}: {url}")

            page = context.new_page()
            try:
                # Measure load time with fallback wait strategies
                # Shopify/heavy sites often never reach "networkidle" due to analytics scripts
                load_start = time.time()
                response = None
                wait_strategies = ["networkidle", "domcontentloaded", "load"]
                timeouts = [30000, 20000, 15000]

                for strategy, strat_timeout in zip(wait_strategies, timeouts):
                    try:
                        response = page.goto(url, wait_until=strategy, timeout=strat_timeout)
                        load_time = int((time.time() - load_start) * 1000)
                        print(f"[CRAWLER]   Chargé avec stratégie '{strategy}' en {load_time}ms")
                        break
                    except Exception as nav_err:
                        if strategy == wait_strategies[-1]:
                            # All strategies failed
                            raise nav_err
                        print(f"[CRAWLER]   Timeout avec '{strategy}', retry avec '{wait_strategies[wait_strategies.index(strategy)+1]}'...")
                        continue

                if response is None:
                    page.close()
                    continue

                # Wait for JS-rendered content (prices, stock, dynamic elements)
                # Critical for Shopify/React/Vue sites where content loads after DOM
                page.wait_for_timeout(2000)

                # Wait for common e-commerce price selectors to appear
                try:
                    page.wait_for_selector(
                        ".price, [class*='price'], [class*='Price'], .product-price, .money, span.amount",
                        timeout=3000
                    )
                except Exception:
                    pass  # Not all pages have prices, that's OK

                # Auto-scroll to trigger lazy loading
                page.evaluate("""async () => {
                    const delay = ms => new Promise(r => setTimeout(r, ms));
                    for (let i = 0; i < document.body.scrollHeight; i += 500) {
                        window.scrollTo(0, i);
                        await delay(100);
                    }
                    window.scrollTo(0, 0);
                }""")
                page.wait_for_timeout(500)

                # Extract page data
                page_data = extract_page_data(page, url)
                page_data["status"] = response.status
                page_data["load_time_ms"] = load_time
                page_data["depth"] = current_depth

                # Extract colors and fonts
                colors, fonts = extract_colors_and_fonts(page)
                page_data["colors_detected"] = colors
                page_data["fonts_detected"] = fonts

                # === NEW: Technical deep scraping ===
                html_content = page.content()
                soup_tech = BeautifulSoup(html_content, "html.parser")

                # Security headers
                page_data["security_headers"] = extract_security_headers(response)

                # Technology detection (only on first page to avoid redundancy)
                if len(results) == 0:
                    page_data["technologies"] = detect_technologies(page, html_content, soup_tech)

                # Resources breakdown
                page_data["resources"] = extract_resources_breakdown(page)

                # Structured data details
                page_data["structured_data_details"] = extract_structured_data_details(soup_tech)

                # Content metrics
                page_data["content_metrics"] = extract_content_metrics(soup_tech, html_content)

                # Cookies (only on first page)
                if len(results) == 0:
                    page_data["cookies"] = extract_cookies(page)

                # Social links (only on first page - usually in footer)
                if len(results) == 0:
                    page_data["social_links"] = extract_social_links(soup_tech, page_data.get("links_external", []))

                # Contact info
                page_data["contact_info"] = extract_contact_info(soup_tech)

                # Extract JS-rendered prices (catches Shopify/React/Vue dynamic prices)
                try:
                    js_prices = page.evaluate("""() => {
                        const priceSelectors = [
                            '.price', '[class*="price"]', '[class*="Price"]',
                            '.product-price', '.money', 'span.amount',
                            '[class*="prix"]', '[data-price]',
                            '.product-card__price', '.card__price'
                        ];
                        const prices = new Set();
                        priceSelectors.forEach(sel => {
                            document.querySelectorAll(sel).forEach(el => {
                                const text = el.textContent.trim();
                                if (text && /\\d/.test(text) && text.length < 50) {
                                    prices.add(text);
                                }
                            });
                        });
                        return Array.from(prices).slice(0, 30);
                    }""")
                    if js_prices:
                        page_data["js_prices_detected"] = js_prices
                        page_data["has_prices"] = True
                except Exception:
                    pass

                # Take screenshot
                safe_name = re.sub(r'[^\w\-.]', '_', urlparse(url).path or "index")[:80]
                screenshot_path = os.path.join(screenshots_dir, f"{len(results):03d}_{safe_name}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                page_data["screenshot"] = screenshot_path

                # Also take a viewport-only screenshot (above the fold)
                fold_path = os.path.join(screenshots_dir, f"{len(results):03d}_{safe_name}_fold.png")
                page.screenshot(path=fold_path, full_page=False)
                page_data["screenshot_fold"] = fold_path

                results.append(page_data)

                # Discover new URLs (if not at max depth)
                if current_depth < depth:
                    for link in page_data["links_internal"]:
                        link_url = normalize_url(link["url"])
                        link_domain = urlparse(link_url).netloc
                        if link_domain == base_domain and link_url not in visited:
                            # Classify to get priority
                            _, priority = classify_page(link_url)
                            to_visit.append((link_url, current_depth + 1))

                # Re-sort to_visit by page classification priority
                to_visit.sort(key=lambda x: classify_page(x[0])[1])

            except Exception as e:
                print(f"[CRAWLER] Erreur sur {url}: {e}")
                page_data = {
                    "url": url,
                    "error": str(e),
                    "depth": current_depth,
                    "classification": classify_page(url)[0],
                }
                results.append(page_data)
            finally:
                page.close()

            # Delay between pages
            if delay > 0:
                time.sleep(delay)

        # === NEW: Site-level technical data (robots.txt, sitemap.xml, SSL) ===
        site_tech = {}

        # Fetch robots.txt
        try:
            robots_url = f"{urlparse(base_url).scheme}://{base_domain}/robots.txt"
            robots_page = context.new_page()
            robots_resp = robots_page.goto(robots_url, timeout=10000)
            if robots_resp and robots_resp.status == 200:
                robots_text = robots_page.content()
                # Extract text content from possible HTML wrapper
                robots_soup = BeautifulSoup(robots_text, "html.parser")
                raw_text = robots_soup.get_text()
                site_tech["robots_txt"] = {
                    "found": True,
                    "content": raw_text[:5000],
                    "has_sitemap_ref": "sitemap" in raw_text.lower(),
                    "disallowed_paths": [
                        line.split(":", 1)[1].strip()
                        for line in raw_text.split("\n")
                        if line.strip().lower().startswith("disallow")
                    ][:30],
                }
            else:
                site_tech["robots_txt"] = {"found": False}
            robots_page.close()
        except Exception:
            site_tech["robots_txt"] = {"found": False, "error": "fetch failed"}

        # Fetch sitemap.xml
        try:
            sitemap_url = f"{urlparse(base_url).scheme}://{base_domain}/sitemap.xml"
            sitemap_page = context.new_page()
            sitemap_resp = sitemap_page.goto(sitemap_url, timeout=10000)
            if sitemap_resp and sitemap_resp.status == 200:
                sitemap_text = sitemap_page.content()
                sitemap_soup = BeautifulSoup(sitemap_text, "html.parser")
                urls_in_sitemap = [loc.get_text(strip=True) for loc in sitemap_soup.find_all("loc")]
                site_tech["sitemap_xml"] = {
                    "found": True,
                    "url_count": len(urls_in_sitemap),
                    "sample_urls": urls_in_sitemap[:20],
                    "has_index": "sitemapindex" in sitemap_text.lower(),
                }
            else:
                site_tech["sitemap_xml"] = {"found": False}
            sitemap_page.close()
        except Exception:
            site_tech["sitemap_xml"] = {"found": False, "error": "fetch failed"}

        browser.close()

    # Generate summary
    elapsed_total = time.time() - start_time
    classifications = {}
    for r in results:
        cls = r.get("classification", "unknown")
        classifications[cls] = classifications.get(cls, 0) + 1

    summary = {
        "base_url": base_url,
        "crawl_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_pages": len(results),
        "max_depth_reached": max(r.get("depth", 0) for r in results) if results else 0,
        "elapsed_seconds": round(elapsed_total, 1),
        "classifications": classifications,
        "errors": sum(1 for r in results if "error" in r and "status" not in r),
        "pages_with_issues": {
            "missing_title": sum(1 for r in results if not r.get("title")),
            "missing_meta_desc": sum(1 for r in results if not r.get("meta_description")),
            "missing_h1": sum(1 for r in results if not r.get("h1")),
            "no_canonical": sum(1 for r in results if not r.get("has_canonical")),
            "no_og_tags": sum(1 for r in results if not r.get("has_og_tags")),
            "no_schema": sum(1 for r in results if not r.get("has_schema")),
            "slow_pages": sum(1 for r in results if r.get("load_time_ms", 0) > 3000),
        },
        "all_fonts": list(set(f for r in results for f in r.get("fonts_detected", []))),
        "site_tree": [{"url": r["url"], "title": r.get("title", ""), "depth": r.get("depth", 0), "classification": r.get("classification", "")} for r in results],
        # Technical infrastructure data
        "technologies": results[0].get("technologies", {}) if results else {},
        "cookies": results[0].get("cookies", []) if results else [],
        "social_links": results[0].get("social_links", {}) if results else {},
        "robots_txt": site_tech.get("robots_txt", {}),
        "sitemap_xml": site_tech.get("sitemap_xml", {}),
        "security_headers_homepage": results[0].get("security_headers", {}) if results else {},
        "resources_homepage": results[0].get("resources", {}) if results else {},
    }

    # Save results
    crawl_path = os.path.join(output_dir, "crawl_results.json")
    with open(crawl_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n[CRAWLER] Crawl terminé !")
    print(f"[CRAWLER] {len(results)} pages crawlées en {elapsed_total:.1f}s")
    print(f"[CRAWLER] Classifications: {classifications}")
    print(f"[CRAWLER] Résultats sauvegardés dans {output_dir}/")

    return crawl_path, summary_path


def main():
    parser = argparse.ArgumentParser(description="Website Crawler for website-analyzer skill")
    parser.add_argument("url", help="URL du site à crawler")
    parser.add_argument("--depth", type=int, default=2, help="Profondeur max de crawl (défaut: 2)")
    parser.add_argument("--max-pages", type=int, default=50, help="Nombre max de pages (défaut: 50)")
    parser.add_argument("--delay", type=float, default=1.5, help="Délai entre pages en secondes (défaut: 1.5)")
    parser.add_argument("--output", default="./website_audit_output", help="Dossier de sortie")
    parser.add_argument("--timeout", type=int, default=15, help="Timeout global en minutes (défaut: 15)")

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url

    crawl_site(
        base_url=args.url,
        depth=args.depth,
        max_pages=args.max_pages,
        delay=args.delay,
        output_dir=args.output,
        timeout_min=args.timeout,
    )


if __name__ == "__main__":
    main()
