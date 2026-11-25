import asyncio
from playwright.async_api import async_playwright
U='https://rgwebd.github.io/sanchezconstructiontx-demo/'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    d=await b.new_context(viewport={'width':1440,'height':900}); pg=await d.new_page()
    await pg.goto(U,wait_until='load'); await pg.wait_for_timeout(3600)
    await pg.screenshot(path='/workspace/sanchez/shots/final-home-hero-desktop.png')
    await pg.goto(U+'services.html',wait_until='load'); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.querySelector('#exterior').scrollIntoView()"); await pg.wait_for_timeout(1800)
    await pg.screenshot(path='/workspace/sanchez/shots/final-services-grid-desktop.png')
    m=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True); mp=await m.new_page()
    await mp.goto(U,wait_until='load'); await mp.wait_for_timeout(3600)
    await mp.screenshot(path='/workspace/sanchez/shots/final-home-hero-mobile.png')
    await b.close()
asyncio.run(m())
