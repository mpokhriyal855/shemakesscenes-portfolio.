import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

videos = [
    'IMG_5171.MOV',
    'IMG_5172.MOV',
    'IMG_5173.MOV',
    'WhatsApp Video 2026-05-24 at 12.46.07 AM.mp4',
    'WhatsApp Video 2026-05-24 at 12.46.10 AM.mp4',
    'WhatsApp Video 2026-05-24 at 12.46.13 AM.mp4',
    'WhatsApp Video 2026-05-24 at 12.46.15 AM.mp4',
    'WhatsApp Video 2026-05-24 at 2.59.08 PM.mp4'
]
images = [
    'WhatsApp Image 2026-05-24 at 2.59.06 PM.jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.07 PM (1).jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.07 PM.jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.09 PM (1).jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.09 PM.jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.10 PM (1).jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.10 PM (2).jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.10 PM (3).jpeg',
    'WhatsApp Image 2026-05-24 at 2.59.10 PM.jpeg'
]

# We need to find all <div class=\"sd-phone...\">...</div> and replace the <div class=\"sd-pscreen\">...</div> content
phones = re.split(r'(<div class=\"sd-phone[^>]*>)', html)

# The user wants videos in highlighted phones first.
# Wait, the prompt says: "first put videos in outlines phone sthen in other phones".
# I'll create a two-pass logic or just pre-allocate.
# Let's count highlighted phones:
highlighted_count = sum(1 for p in phones if 'highlighted' in p)
print(f'Found {highlighted_count} highlighted phones')

# We have 8 videos. Highlighted phones get videos first.
v_idx = 0
i_idx = 0

out = [phones[0]]

# First pass: assign videos to highlighted phones
for i in range(1, len(phones), 2):
    tag = phones[i]
    content = phones[i+1]
    
    is_highlighted = 'highlighted' in tag
    
    if is_highlighted and v_idx < len(videos):
        vid = videos[v_idx]
        v_idx += 1
        replacement = f'<video src=\"assets/story/{vid}\" loop muted playsinline style=\"width:100%;height:100%;object-fit:cover;\"></video>'
        
        # Replace everything inside <div class=\"sd-pscreen\">...</div>
        new_content = re.sub(r'(<div class=\"sd-pscreen\">)(.*?)(</div>)', r'\1' + replacement + r'\3', content, flags=re.DOTALL)
        out.append(tag)
        out.append(new_content)
    else:
        # We will assign the rest in a second pass or we can do it all in one if we know the counts.
        # Actually, if we just assign highlighted FIRST, but we are traversing sequentially!
        # If we traverse sequentially, we just assign videos to highlighted.
        # But wait, what if we hit a normal phone and assign a video, and run out before we hit the highlighted one?
        # Better: Pre-assign what goes to which index.
        pass

# Let's rewrite the logic correctly.
v_idx = 0
i_idx = 0
assignments = {}

# Pass 1: Highlighted phones get videos
for i in range(1, len(phones), 2):
    if 'highlighted' in phones[i] and v_idx < len(videos):
        assignments[i] = f'<video src=\"assets/story/{videos[v_idx]}\" loop muted playsinline style=\"width:100%;height:100%;object-fit:cover;\"></video>'
        v_idx += 1

# Pass 2: Normal phones get remaining videos, then images
for i in range(1, len(phones), 2):
    if i not in assignments:
        if v_idx < len(videos):
            assignments[i] = f'<video src=\"assets/story/{videos[v_idx]}\" loop muted playsinline style=\"width:100%;height:100%;object-fit:cover;\"></video>'
            v_idx += 1
        elif i_idx < len(images):
            assignments[i] = f'<img src=\"assets/story/{images[i_idx]}\" loading=\"lazy\" style=\"width:100%;height:100%;object-fit:cover;\">'
            i_idx += 1
        else:
            assignments[i] = f'<img src=\"assets/story/{images[-1]}\" loading=\"lazy\" style=\"width:100%;height:100%;object-fit:cover;\">'

# Now build the output
out = [phones[0]]
for i in range(1, len(phones), 2):
    tag = phones[i]
    content = phones[i+1]
    replacement = assignments[i]
    new_content = re.sub(r'(<div class=\"sd-pscreen\">)(.*?)(</div>)', r'\1\n' + replacement + r'\n\3', content, flags=re.DOTALL)
    out.append(tag)
    out.append(new_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(''.join(out))
print("Done writing index.html")
