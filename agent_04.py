import os
import base64
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
IMAGE_MODEL = "gpt-image-2.6-sunburst"
OUTPUT_DIR = "outputs"
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

def create_poster(company_name, script):
    print("VIDEO EDITOR AGENT : Creating poster for company:", company_name, flush=True)

    prompt = f"""
Design a profesional poster for {company_name}.
Follow the POSTER SCRIPT below: use its visual, description, and render headline, sub-headline and call to act:
correctly spelled text. Ignore the video script.

{script}
"""

    result = openai.images.generate(model=IMAGE_MODEL, prompt=prompt, size="1024x1536")
    image_bytes = base64.b64decode(result.data[0].b64_json)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = company_name.strip().lower().replace(" ", "_")
    poster_path = os.path.join(OUTPUT_DIR, f"{filename}_poster_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    with open(poster_path, "wb") as f:
        f.write(image_bytes)
    return poster_path

sam_scri = """
    ## POSTER SCRIPT (Vertical Hero “Summer Menu Launch”)

**Headline (max 6 words, bold and punchy):**  
**SUMMER MENU IS HERE**

**Sub-headline (max 12 words):**  
Limited-time favorites—made fresh for warm days

**Call to action (max 5 words):**  
Order yours today

**Visual description (for designer):**  
- **Format:** 1080×1350 (4:5), vertical hero poster, “feed-ready” with safe margins.  
- **Background image:** Full-bleed **sunlit window-light photo** (warm, authentic, not overly staged). Show **one iced signature drink** in the foreground (clear condensation + ice texture) plus **one seasonal bite** beside it on a light café surface. Keep steam/ice highlights crisp.  
- **Color treatment:**  
  - Add a subtle **cream/off-white overlay gradient** (top-left to bottom-right at ~25–35% opacity) to ensure typography legibility.  
  - Typography accents in **sea-glass teal**; one tight **lime highlight** used sparingly for emphasis (e.g., a small badge/asterisk).  
- **Typography system (bold + minimal):**  
  - Headline in a **heavy sans** (condensed or strong weight), all caps, **tight tracking**.  
  - Sub-headline smaller, clean sans, sentence case, medium weight.  
  - 3-item highlight block uses **uppercase micro-labels** + bold item names.  
- **Collage accents:**  
  - Near the headline’s right edge, place a small **hand-cut collage shape** (leaf silhouette or ice-crystal) with a slight paper texture.  
  - Add one **thin “torn paper” strip** or deckle-edged label behind the 3-item block (cream with teal outline).  
- **Layout (top to bottom):**  
  1) **Top:** small logo lockup (Blue Bottle Café) in **sea-glass teal** or cream-white depending on contrast.  
  2) **Center-left:** **Headline** (“SUMMER MENU IS HERE”) large, bold.  
  3) **Under headline:** sub-headline in 1–2 lines, balanced.  
  4) **Mid-lower highlight block:** a rounded rectangle or sticker-style card (cream background, teal border) with **3 rows**:  
     - Row 1: **“Iced ____”** — *$__* (lime asterisk “*limited”)  
     - Row 2: **“Blended ____”** — *$__*  
     - Row 3: **“Seasonal Bite ____”** — *$__*  
     Keep each row: item name bold, price smaller, asterisk note at bottom (“*While supplies last”).  
  5) **Bottom:** CTA text (“Order yours today”) centered, medium-large, sea-glass teal.  
- **Details:**  
  - Add subtle **ice sparkle dots** (3–5 small lime/white highlights) near the drink to feel summery and fresh.  
  - No clutter—high contrast, readable at thumb distance.


---

## VIDEO SCRIPT (30-second vertical Reels/TikTok)

**Goal:** Summer Menu Launch hero reel for Blue Bottle Café with bold, authentic food-drink visuals + quick menu clarity.

### Scroll-stopping hook (first 3 seconds)
**On-screen text (big, bold):** “SUMMER IS LOADING…”  
**VO (voice-over):** “Summer menu just dropped—cool sips, fresh bites.”

---

### Scene-by-scene (0–30s)

**Scene 1 (0:00–0:03)**  
- **Visual:** Fast push-in on an **iced drink**—ice clinks, condensation beads, sunlight flare through the window.  
- **Motion/Effects:** Subtle zoom + crisp text pop.  
- **On-screen text:** “SUMMER IS LOADING…”  
- **VO:** “Summer menu just dropped—cool sips, fresh bites.”

**Scene 2 (0:03–0:07)**  
- **Visual:** Cut to a **second angle**: the seasonal bite next to the drink, warm natural light, textured food surface.  
- **On-screen text:** “Cool sips.”  
- **VO:** “First up—cool sips made for warm days.”

**Scene 3 (0:07–0:12)**  
- **Visual:** Quick montage: pouring/blending moment (e.g., iced or blended item).  
- **On-screen text:** “Iced. Blended. Fresh.”  
- **VO:** “Iced, blended, and crafted fresh—every time.”

**Scene 4 (0:12–0:18)**  
- **Visual:** Overlay card appears while the camera slowly pans across the drink and garnish.  
- **On-screen text (carousel-style list):**  
  - “Iced ____”  
  - “Blended ____”  
  - “Seasonal Bite ____”  
  (Use **teal text**, highlight one word in **lime**.)  
- **VO:** “Three fan-favorites to start your summer run.”

**Scene 5 (0:18–0:23)**  
- **Visual:** Snap to a close-up of the seasonal bite—one satisfying bite moment (no chewing, just the cut/serve moment).  
- **On-screen text:** “Limited-time favorites*”  
- **VO:** “Limited-time favorites—while supplies last.”

**Scene 6 (0:23–0:30) — CTA**  
- **Visual:** Wider shot of the café vibe: window light, branded cup close-ups, quick “walk-in” energy. End on the iced drink hero shot.  
- **On-screen text (large):** “Blue Bottle Cafe” then “Order today”  
- **VO:** “Swing by Blue Bottle Café—order yours today.”

**End call to action (last frame, keep readable):**  
**“Order today”** (lime underline accent)

---  

If you upload Blue Bottle Café’s brand PDF/guide, I’ll swap the typography + exact sea-glass/lime usage to your approved logo colors and fonts.
"""

poster = create_poster("Blue Bottle Cafe", sam_scri)