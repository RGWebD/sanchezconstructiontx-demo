# Vector redraw of the existing Sanchez roofline mark + favicons/OG image
from pathlib import Path
import subprocess,asyncio
B=Path(__file__).parent/'brand'
RED='#D3262E'
def mark(c1=RED,c2='#16171A',c3='#7A7D83',win=RED):
    # three offset rooflines; later roofs stop where they meet the previous one
    return f'''<g fill="none" stroke-width="26" stroke-linejoin="miter" stroke-miterlimit="10">
<path d="M322 48 L375 0 L540 150" stroke="{c3}"/>
<path d="M217 48 L270 0 L435 150" stroke="{c2}"/>
<path d="M0 150 L165 0 L330 150" stroke="{c1}"/></g>
<g fill="{win}"><rect x="128" y="70" width="34" height="30"/><rect x="168" y="70" width="34" height="30"/><rect x="128" y="106" width="34" height="30"/><rect x="168" y="106" width="34" height="30"/></g>'''
def svg(body,vb): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>'
VB='-20 -22 580 190'
(B/'mark-light.svg').write_text(svg(mark(),VB))
(B/'mark-dark.svg').write_text(svg(mark(c2='#F4F1EA',c3='#9EA2A8'),VB))
(B/'mark-mono.svg').write_text(svg(mark('#fff','#fff','#fff','#fff'),VB))
# favicon: red roof + window only on asphalt tile
fav=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#141518"/>
<g transform="translate(6 14) scale(0.158)"><path d="M0 150 L165 0 L330 150" fill="none" stroke="{RED}" stroke-width="30"/>
<g fill="#FFC21A"><rect x="128" y="70" width="34" height="30"/><rect x="168" y="70" width="34" height="30"/><rect x="128" y="106" width="34" height="30"/><rect x="168" y="106" width="34" height="30"/></g></g></svg>'''
(B/'favicon.svg').write_text(fav)
from playwright.async_api import async_playwright
from PIL import Image
async def render():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':512,'height':512})
        await pg.set_content(f'<style>html,body{{margin:0;background:transparent}}svg{{width:512px;height:512px;display:block}}</style>{fav}')
        await pg.screenshot(path=str(B/'fav-512.png'),omit_background=True)
        # brand sheet
        await pg.set_viewport_size({'width':1200,'height':760})
        await pg.set_content(f'''<style>body{{margin:0;font-family:sans-serif}}.r{{display:flex;height:380px}}.c{{flex:1;display:grid;place-items:center}}svg{{width:420px}}.s{{display:flex;gap:0;height:0}}</style>
<div class="r"><div class="c" style="background:#F4F1EA">{svg(mark(),VB)}</div><div class="c" style="background:#141518">{svg(mark(c2="#F4F1EA",c3="#9EA2A8"),VB)}</div></div>
<div class="r" style="height:380px">{''.join(f'<div class="c" style="background:{c};color:{"#000" if c in ("#FFC21A","#F4F1EA") else "#fff"};font:600 20px monospace">{c}</div>' for c in ["#141518","#FFC21A",RED,"#F4F1EA","#7A7D83"])}</div>''')
        await pg.screenshot(path=str(B/'brand-sheet.png'))
        await b.close()
asyncio.run(render())
im=Image.open(B/'fav-512.png')
for s in (16,32,180,512): im.resize((s,s),Image.LANCZOS).save(B/f'fav-{s}.png')
im.save(B/'favicon.ico',sizes=[(16,16),(32,32),(48,48)])
print('ok')
