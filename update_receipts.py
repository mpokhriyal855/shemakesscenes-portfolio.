import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_texts = [
    "Trend-Based Fast Paced Editing",
    "Cinematic Burger King Trend",
    "Lip Sync Comedy Timing",
    "Cafe Reel With Shutter Effects",
    "Dark Cinematic Color Grading",
    "Banaras Travel Storytelling Edit",
    "Spiritual Visual Aesthetic",
    "Song Sync Self Edit",
    "Aesthetic Beat Transition Edit",
    "Birthday Day-Out Storytelling",
    "Creating Scroll Stopping Visuals \u2728"
]

pattern = r'(<section class=\"video-gallery\".*?<div class=\"video-grid[^\"]*\">(?:\s*<!--.*?-->\s*)?)(.*?)(</div>\s*</section>)'
match = re.search(pattern, html, flags=re.DOTALL)
if not match:
    print("Could not find video-grid")
    exit(1)

prefix = match.group(1)
grid_content = match.group(2)
suffix = match.group(3)

items = grid_content.split('<div class="video-item')

valid_items = []
for item in items[1:]:
    full_item = '<div class="video-item' + item
    valid_items.append(full_item)

print(f"Found {len(valid_items)} video items.")

if len(valid_items) < 11:
    print("Not enough video items!")
else:
    final_items = []
    for i in range(11):
        item_html = valid_items[i]
        new_text = new_texts[i]
        item_html = re.sub(r'(<p class=\"v-text\">)(.*?)(</p>)', r'\g<1>' + new_text + r'\g<3>', item_html)
        final_items.append(item_html)
    
    new_grid_content = '\n'.join(final_items)
    new_html = html[:match.start(2)] + new_grid_content + html[match.end(2):]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Updated index.html successfully. Kept exactly 11 items.")
