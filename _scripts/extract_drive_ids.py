import requests, re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

formats = {
    'CARRUSELES': '1CMNv9zsq4XyrevaKnb4Z9VT2kkSuRcYp',
    'POST': '1cfJyIEekzKMYgHMreeb9VQ6q_BCUP2HO',
    'VIDEOS': '1p_ZABqizg3TauFpb19HDrGNWZSj0nwCz'
}

all_results = {}

for fname, fid in formats.items():
    url = f'https://drive.google.com/drive/folders/{fid}'
    resp = requests.get(url, headers=headers, timeout=15)
    # Find all data-id attributes
    ids = re.findall(r'data-id\s*=\s*["\']([a-zA-Z0-9_-]{25,})["\']', resp.text)
    # Deduplicate preserving order
    unique = []
    for i in ids:
        if i not in unique:
            unique.append(i)
    
    print(f'{fname} ({fid}):')
    format_results = {}
    for uid in unique:
        # Search for the folder name by finding the data-id and looking at surrounding HTML
        idx = resp.text.find(uid)
        if idx >= 0:
            snippet = resp.text[idx:idx+500]
            # Try different patterns to find folder name
            patterns = [
                r'aria-label="([^"]+)"',
                r'>([^<]{3,80})</div></div></div></div></div>',
                r'title="([^"]+)"',
            ]
            name = '?'
            for p in patterns:
                m = re.search(p, snippet)
                if m:
                    candidate = m.group(1).strip()
                    if len(candidate) > 2 and len(candidate) < 80 and 'data-' not in candidate:
                        name = candidate
                        break
            print(f'  {uid} -> {name}')
            format_results[name] = uid
    all_results[fname] = format_results
    print()

# Also check the old folders
old_folders = {
    'CARRUSEL BLUETTI': '1kHo0DaYn7qNF9JLL7orDcYZUKJSq5vX6',
    'CARRUSEL RESPALDO ELECTRICO': '1EGJjR6MS-LmYb5VHrocZg-Agf_9aCGZx'
}
for fname, fid in old_folders.items():
    url = f'https://drive.google.com/drive/folders/{fid}'
    resp = requests.get(url, headers=headers, timeout=15)
    ids = re.findall(r'data-id\s*=\s*["\']([a-zA-Z0-9_-]{25,})["\']', resp.text)
    unique = []
    for i in ids:
        if i not in unique:
            unique.append(i)
    print(f'{fname} ({fid}):')
    for uid in unique:
        print(f'  {uid}')
    print()
