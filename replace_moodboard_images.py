import os
import re

html_path = 'index.html'
assets_dir = 'assets/moodboard'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Get the list of images
files = os.listdir(assets_dir)
images = sorted([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))])

img_tags = []
for img in images:
    img_tags.append(f'            <img src="assets/moodboard/{img}" class="masonry-item" loading="lazy" alt="Moodboard image">')

masonry_content = '\n'.join(img_tags)

pattern = r'(<div class=\"masonry-grid.*?>)(.*?)(</section>)'

def replacer(match):
    return match.group(1) + '\n' + masonry_content + '\n        </div>\n    ' + match.group(3)

new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Successfully replaced moodboard images with {len(images)} images from assets/moodboard/")
