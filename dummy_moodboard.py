import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Valid aesthetic Pinterest style URLs
img_urls = [
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=600&h=800&fit=crop", # girl portrait
    "https://images.unsplash.com/photo-1495120464115-28d5f0ce852d?w=600&h=500&fit=crop", # coffee
    "https://images.unsplash.com/photo-1445205170230-053b83016050?w=600&h=900&fit=crop", # fashion aesthetic
    "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=600&h=400&fit=crop", # interior
    "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=600&h=700&fit=crop", # minimalist room
    "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=600&h=600&fit=crop", # portrait
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=600&h=850&fit=crop", # girl fashion
    "https://images.unsplash.com/photo-1507133750070-4ed3a105f963?w=600&h=500&fit=crop", # aesthetic flowers
    "https://images.unsplash.com/photo-1519638399535-1b036603ac77?w=600&h=750&fit=crop", # polaroid
    "https://images.unsplash.com/photo-1506744626753-1fa28f6e52c8?w=600&h=450&fit=crop", # nature
    "https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?w=600&h=800&fit=crop", # fashion model
    "https://images.unsplash.com/photo-1500336624523-d727130c3328?w=600&h=600&fit=crop", # aesthetic pink
    "https://images.unsplash.com/photo-1515347619152-475306121f15?w=600&h=900&fit=crop", # matcha/coffee
    "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=600&h=550&fit=crop"  # girl sunset
]

img_tags = []
for url in img_urls:
    # Notice I removed pop-in. If pop-in class was buggy (hiding without revealing) it's safer to remove it for now.
    img_tags.append(f'            <img src=\"{url}\" class=\"masonry-item\" loading=\"lazy\" alt=\"Moodboard image\">')

masonry_content = chr(10).join(img_tags)

pattern = r'(<div class=\"masonry-grid.*?>)(.*?)(</section>)'

def replacer(match):
    return match.group(1) + '\n' + masonry_content + '\n        </div>\n    ' + match.group(3)

new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
