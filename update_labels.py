import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

updates = {
    1: "Trend-Based Fast Paced Editing",
    2: "Lip Sync Comedy Timing",
    3: "“tere mai bich mai kya hai” lip sync reel",
    5: "Lip Sync Beat Syncing",
    6: "Birthday Day-Out Storytelling",
    7: "Shutter Effect Cinematic Shoot",
    8: "Dark Cinematic Color Grading",
    9: "Banaras Travel Storytelling Edit",
    10: "Spiritual Visual Aesthetic",
    11: "Creating Scroll Stopping Visuals \u2728"
}

for item_num, new_text in updates.items():
    # Find the comment <!-- Video Item X (Type) -->
    # Then replace the first <p class="v-text">...</p> after it before the next Video Item comment.
    
    # We can split the string by `<!-- Video Item `
    parts = html.split('<!-- Video Item ')
    
    new_parts = [parts[0]]
    for part in parts[1:]:
        # check if this part corresponds to item_num
        # it starts with something like `1 (Vertical) -->`
        match = re.match(r'^(\d+)', part)
        if match and int(match.group(1)) == item_num:
            # Replace the first v-text
            part = re.sub(r'(<p class=\"v-text\">)(.*?)(</p>)', r'\g<1>' + new_text + r'\g<3>', part, count=1)
        new_parts.append(part)
        
    html = '<!-- Video Item '.join(new_parts)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
