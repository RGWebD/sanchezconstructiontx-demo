import asyncio,sys,http.server,threading,functools,socketserver
from playwright.async_api import async_playwright
tag=sys.argv[1]; pages=sys.argv[2].split(',') if len(sys.argv)>2 else ['index','services','projects','reviews','contact']
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.ThreadingTCPServer(('127.0.0.1',8944),functools.partial(Q,directory='/workspace/sanchez/site'));threading.Thread(target=srv.serve_forever,daemon=True).start()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w,h,n in [(1440,900,'d'),(390,844,'m')]:
      ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
      pg=await ctx.new_page()
      for pn in pages:
        await pg.goto(f'http://127.0.0.1:8944/{pn}.html',wait_until='load'); await pg.wait_for_timeout(2900)
        await pg.screenshot(path=f'/workspace/sanchez/shots/{tag}-{pn}-{n}.png')
        H=await pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,400): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(70)
        await pg.wait_for_timeout(1800); await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'/workspace/sanchez/shots/{tag}-{pn}-{n}-full.png',full_page=True)
      await ctx.close()
    await b.close()
asyncio.run(m())
