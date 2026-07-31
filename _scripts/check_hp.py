html = open('ESTRATEGA/plan_julio2026.html', encoding='utf-8').read()
hp_count = html.count('data-brand="hp"')
print(f'HP pieces found: {hp_count}')

# Check if HP pieces have piece-with-copy class
import re
hp_pieces = re.findall(r'class="piece piece-with-copy".*?data-brand="hp"', html)
print(f'HP with piece-with-copy: {len(hp_pieces)}')

# Find HP piece markers
hp_markers = re.findall(r'class="piece[^"]*"[^>]*data-brand="hp"', html)
print(f'HP piece markers: {len(hp_markers)}')

# Check for HP badge
hp_badges = re.findall(r'class="num">HP</div>', html)
print(f'HP badges (HP text): {len(hp_badges)}')
