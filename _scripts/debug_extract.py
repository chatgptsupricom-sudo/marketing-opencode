import re

html = open('ESTRATEGA/plan_julio2026.html', encoding='utf-8').read()

# Find week card markers
weeks = re.findall(r'class="week-card" id="(s\d+)"', html)
print('Week cards found:', weeks)

# Find first piece
piece = re.search(r'class="piece piece-with-copy"', html)
if piece:
    print('First piece at:', piece.start())
    # Show context
    start = max(0, piece.start() - 200)
    print('Context before piece:')
    print(html[start:piece.start() + 50])
