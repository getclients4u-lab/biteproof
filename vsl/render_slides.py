#!/usr/bin/env python3
"""
render_slides.py — BiteProof "Mosquito-Proof Home System" VSL silent slideshow.
UPPERCASE slides (deep-green bg, mint/amber/white text) -> 1920x1080 PNGs -> ~5:00 MP4.
Requires: ImageMagick (convert), FFmpeg.
"""
import os, re, subprocess, textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
SLIDES_DIR = os.path.join(BASE, "slides")
OUT_MP4 = os.path.join(BASE, "vsl-slideshow.mp4")
FONT = "DejaVu-Sans-Bold"
BG = "#071410"
MINT = "#5eead4"    # system / mechanism / CTA
AMBER = "#fbbf24"   # news / urgency
WHITE = "#ffffff"   # body

def pick_color(text):
    urgent = ('2.5 MILLION', 'OUTBREAK', 'RECORD', '22 YEARS', 'WEST NILE',
              'CONFIRMED', 'ALERTING', 'INFECTED', 'KEEPING KIDS INSIDE',
              'CANCELING EVENINGS', 'WORST START', 'NO VACCINE')
    brand = ('BITEPROOF', 'RING ', 'SYSTEM', 'DRAIN IT. DEFEND IT. DONE.',
             '4-RING', '8 DONE-FOR-YOU', 'PEACE-OF-MIND', 'PROTECT YOUR FAMILY')
    if any(k in text for k in urgent):
        return AMBER
    if any(k in text for k in brand):
        return MINT
    return WHITE

# Parse slides from vsl-script.md storyboard: "**Slide N**\nTEXT"
script = open(os.path.join(BASE, "vsl-script.md")).read()
block = script.split('## STORYBOARD')[1].split('## Production notes')[0]
slides = []
for m in re.finditer(r'\*\*Slide (\d+)\*\*\n(.+)', block):
    text = m.group(2).strip()
    slides.append((text, pick_color(text)))
assert len(slides) >= 85, f"expected 90ish slides, got {len(slides)}"

os.makedirs(SLIDES_DIR, exist_ok=True)
for png in os.listdir(SLIDES_DIR):
    if png.endswith('.png'):
        os.remove(os.path.join(SLIDES_DIR, png))

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

for i, (text, color) in enumerate(slides, 1):
    out = os.path.join(SLIDES_DIR, f"slide_{i:03d}.png")
    # shrink font for long lines; wrap at ~22 chars for 2-line max aesthetic
    words = text.split()
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 <= 24:
            cur = (cur + ' ' + w).strip()
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    if len(lines) > 2 and max(len(l) for l in lines) > 26:
        lines = textwrap.wrap(text, width=34)[:3]
    fs = 96 if max(len(l) for l in lines) <= 16 else (72 if max(len(l) for l in lines) <= 24 else 56)
    if len(lines) > 2: fs = 52
    body = "\n".join(lines)
    label = f'caption "   {esc(body)}   "'
    cmd = ['convert', '-size', '1920x1080', f'xc:{BG}',
           '-font', FONT, '-pointsize', str(fs), '-fill', color,
           '-gravity', 'center', '-annotate', '+0+0', body,
           '-bordercolor', BG, '-border', '40',
           out]
    subprocess.run(cmd, check=True)

# build concat list: ~3.3s per slide over 90 slides ≈ 5:00
with open(os.path.join(BASE, 'slides.txt'), 'w') as f:
    for i in range(1, len(slides) + 1):
        f.write(f"file 'slides/slide_{i:03d}.png'\n")
        f.write("duration 3.30\n")
    # repeat last frame so total >= 295s
    f.write(f"file 'slides/slide_{len(slides):03d}.png'\n")

subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', os.path.join(BASE, 'slides.txt'),
                '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264',
                '-preset', 'medium', '-crf', '20', OUT_MP4],
               check=True, capture_output=True)
print(f"rendered {len(slides)} slides -> {OUT_MP4}")
