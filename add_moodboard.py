import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Get all images
files = os.listdir('assets/story')
images = sorted([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])

img_tags = []
for img in images:
    img_tags.append(f'            <img src="assets/story/{img}" class="masonry-item pop-in" loading="lazy" alt="Moodboard image">')

masonry_html = f'''
    <!-- PINTEREST MOOD BOARD -->
    <section class="moodboard-section" id="moodboard">
        <div class="test-header reveal-up">
            <h2 class="section-title">My <span class="highlight">Aesthetic.</span></h2>
            <p class="section-subtitle">A glimpse into my visual world.</p>
        </div>
        <div class="masonry-grid reveal-up delay-2">
{chr(10).join(img_tags)}
        </div>
    </section>
'''

# Comment out testimonials-strip
# We need to find <section class="testimonials-strip"> up to its closing tag.
# Using regex:
pattern = r'(<section class="testimonials-strip">.*?</section>)'
html = re.sub(pattern, r'<!-- \1 -->\n' + masonry_html, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
