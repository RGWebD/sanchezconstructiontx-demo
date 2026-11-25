import asyncio,http.server,threading,functools,socketserver
from playwright.async_api import async_playwright
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.ThreadingTCPServer(('127.0.0.1',8966),functools.partial(Q,directory='/workspace/sanchez/site'));threading.Thread(target=srv.serve_forever,daemon=True).start()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.goto('http://127.0.0.1:8966/projects.html',wait_until='load'); await pg.wait_for_timeout(1500)
    el=await pg.query_selector('.ba-wrap'); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.querySelector('.ba input').value=35;document.querySelector('.ba input').dispatchEvent(new Event('input'))")
    await pg.evaluate("scrollBy(0,-60)"); await pg.wait_for_timeout(400)
    await pg.screenshot(path='/workspace/sanchez/shots/final-projects-before-after-desktop.png')
    await pg.goto('http://127.0.0.1:8966/index.html',wait_until='load'); await pg.wait_for_timeout(1800)
    el=await pg.query_selector('.hsframe'); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(1200)
    await pg.evaluate("scrollBy(0,120)"); await pg.wait_for_timeout(300)
    await pg.hover('.hs-pin >> nth=1'); await pg.wait_for_timeout(600)
    await pg.screenshot(path='/workspace/sanchez/shots/final-home-hotspots-desktop.png')
    el=await pg.query_selector('.stats'); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(2400)
    await pg.evaluate("scrollBy(0,-200)"); await pg.wait_for_timeout(300)
    await pg.screenshot(path='/workspace/sanchez/shots/final-home-tapes-stats-desktop.png')
    m=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); mp=await m.new_page()
    for n in ['services','contact']:
      await mp.goto(f'http://127.0.0.1:8966/{n}.html',wait_until='load'); await mp.wait_for_timeout(1500)
      await mp.evaluate("scrollTo(0,900)"); await mp.wait_for_timeout(1500)
      await mp.screenshot(path=f'/workspace/sanchez/shots/v6-{n}-m-scrolled.png')
    await b.close()
asyncio.run(m())
