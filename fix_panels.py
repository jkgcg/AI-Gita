import re

html_path = r'c:\Users\girijyo\OneDrive - adidas\Desktop\Work\AI Learning\AI_Gita.html'

with open(html_path, encoding='utf-8') as f:
    html = f.read()

panels = list(re.finditer(r'<div id="tab-(\w+)" class="panel[^"]*">', html))
print(f'Total panel divs: {len(panels)}')

# For each panel, count div balance in its content region.
# If unbalanced by +1 (missing closing div), insert </div> just before the next panel starts.
# Work in reverse order so insertions don't shift earlier positions.

fixes = []
for i, m in enumerate(panels):
    pid = m.group(1)
    start = m.start()
    if i + 1 < len(panels):
        next_start = panels[i+1].start()
    else:
        # Last panel: find </body>
        next_start = html.find('</body>', start)
        if next_start < 0:
            next_start = len(html)

    between = html[start:next_start]
    opens = between.count('<div')
    closes = between.count('</div>')
    diff = opens - closes
    if diff == 1:
        fixes.append((pid, next_start))  # insert </div> at next_start

print(f'Panels needing closing </div>: {len(fixes)}')
for pid, pos in fixes:
    print(f'  {pid} -> insert at pos {pos}')

# Apply in reverse order
fixes.sort(key=lambda x: x[1], reverse=True)
for pid, pos in fixes:
    html = html[:pos] + '\n</div>' + html[pos:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nFixed. New file size: {len(html):,} chars ({len(html)//1024} KB)')

# Verify
with open(html_path, encoding='utf-8') as f:
    html2 = f.read()
panels2 = list(re.finditer(r'<div id="tab-(\w+)" class="panel[^"]*">', html2))
still_bad = []
for i, m in enumerate(panels2):
    pid = m.group(1)
    start = m.start()
    if i + 1 < len(panels2):
        next_start = panels2[i+1].start()
    else:
        next_start = html2.find('</body>', start)
        if next_start < 0:
            next_start = len(html2)
    between = html2[start:next_start]
    opens = between.count('<div')
    closes = between.count('</div>')
    diff = opens - closes
    if diff != 0:
        still_bad.append(f'{pid}: diff={diff}')

if still_bad:
    print('Still unbalanced:', still_bad)
else:
    print('All panels div-balanced after fix.')
