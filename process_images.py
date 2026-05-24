import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Get all files from assets/story
files = os.listdir('assets/story')
videos = sorted([f for f in files if f.lower().endswith(('.mp4', '.mov'))])
images = sorted([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])

# We need to find all <div class=\"sd-phone...\">...</div> and replace the <div class=\"sd-pscreen\">...</div> content
phones = re.split(r'(<div class=\"sd-phone[^>]*>)', html)

# Highlighted phones count
highlighted_count = sum(1 for p in phones if 'highlighted' in p)
print(f'Found {highlighted_count} highlighted phones')

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
    # Use DOTALL to replace everything inside sd-pscreen, handling newlines correctly.
    # The existing content might be empty (like <div class="sd-pscreen"></div>) or have newlines.
    new_content = re.sub(r'(<div class=\"sd-pscreen\">)(.*?)(</div>)', r'\1\n' + replacement + r'\n\3', content, flags=re.DOTALL)
    out.append(tag)
    out.append(new_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(''.join(out))
print(f"Done writing index.html. Used {v_idx} videos and {i_idx} images.")
