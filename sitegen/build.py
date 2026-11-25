#!/usr/bin/env python3
"""Static site generator: Sanchez Construction Services demo (RGWebD). Facts: see notes.md."""
import json, shutil, sys
from pathlib import Path
from html import escape as e
from PIL import Image
GEN=Path(__file__).parent
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/sanchez/site')
BASE='https://rgwebd.github.io/sanchezconstructiontx-demo/'
NAME='Sanchez Construction Services'
PHONE='(956) 206-3885'; TEL='tel:+19562063885'; EMAIL='jcsanc@sbcglobal.net'
ADDR='2507 Market St, Laredo, TX 78043'
GMAPS='https://maps.google.com/?cid=174853116217362907'
DIR='https://www.google.com/maps/dir/?api=1&destination=Sanchez+Construction+Services%2C+2507+Market+St%2C+Laredo%2C+TX+78043'
MAPEMBED='https://www.google.com/maps?q=Sanchez+Construction+Services,+2507+Market+St,+Laredo,+TX+78043&z=15&output=embed'
QUOTE='contact.html#quote'

# ---------- assets ----------
for d in ['assets','index.html']: pass
A=OUT/'assets'
if A.exists(): shutil.rmtree(A)
(A/'img').mkdir(parents=True)
for f in (GEN/'img').glob('*.webp'): shutil.copy(f,A/'img'/f.name)
shutil.copytree(GEN/'fonts',A/'fonts',ignore=shutil.ignore_patterns('*.css'))
css=(GEN/'fonts'/'faces.css').read_text().replace('jetbrainsmono-700','jetbrainsmono-500')+'\n'+(GEN/'src'/'styles.css').read_text()
(A/'styles.css').write_text(css); shutil.copy(GEN/'src'/'script.js',A/'script.js')
for f in ['mark-light.svg','mark-dark.svg','favicon.svg']: shutil.copy(GEN/'brand'/f,A/f)
shutil.copy(GEN/'brand'/'favicon.ico',OUT/'favicon.ico'); shutil.copy(GEN/'brand'/'fav-180.png',OUT/'apple-touch-icon.png'); shutil.copy(GEN/'brand'/'fav-512.png',A/'icon-512.png')
# OG image: hero photo + mark
og=Image.open(GEN/'img'/'dump-trailer-loader.webp').convert('RGB'); W,H=og.size; t=630/1200
og=og.crop((int(W*.12),0,int(W*.12)+int(H/t),H)).resize((1200,630),Image.LANCZOS)
from PIL import ImageDraw
ov=Image.new('RGBA',(1200,630),(0,0,0,0)); dr=ImageDraw.Draw(ov); dr.rectangle((0,0,560,630),fill=(14,15,17,215))
for x in range(-40,1240,36): dr.polygon([(x,610),(x+18,610),(x-2,630),(x-20,630)],fill=(255,194,26,255))
og=Image.alpha_composite(og.convert('RGBA'),ov)
mk=Image.open(GEN/'brand'/'fav-512.png').resize((150,150)); og.alpha_composite(mk,(50,60))
from PIL import ImageFont
try:
    fbig=ImageFont.truetype(str(GEN/'fonts'/'anybody-100_900.woff2'),64)
except Exception: fbig=ImageFont.load_default()
dr=ImageDraw.Draw(og)
try:
    fbig.set_variation_by_axes([150,900])
except Exception: pass
dr.text((50,250),'SANCHEZ',font=fbig,fill=(255,255,255)); dr.text((50,322),'CONSTRUCTION',font=fbig,fill=(255,194,26))
try: fs=ImageFont.truetype(str(GEN/'fonts'/'inter-400_700.woff2'),26)
except Exception: fs=ImageFont.load_default()
dr.text((52,420),'General contractor · Laredo, TX',font=fs,fill=(230,230,230)); dr.text((52,460),'★ 5.0 · 19 Google reviews',font=fs,fill=(255,194,26))
og.convert('RGB').save(A/'og-image.jpg',quality=86)

DIM={}
def dims(n):
    if n not in DIM: DIM[n]=Image.open(GEN/'img'/f'{n}.webp').size
    return DIM[n]
def pic(n,alt,cls='',eager=False,attrs=''):
    w,h=dims(n)
    return f'<img src="assets/img/{n}.webp" width="{w}" height="{h}" alt="{e(alt)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async" {attrs}>'

I={'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
   'doc':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>'}
def b_call(cls='',lab=None): return f'<a class="btn mag {cls}" href="{TEL}">{I["phone"]}<span>{lab or "Call "+PHONE}</span></a>'
def b_quote(cls='ghost',lab='Get a quote'): return f'<a class="btn mag {cls}" href="{QUOTE}">{I["doc"]}<span>{lab}</span></a>'
STATUS='<span class="status" data-status><i></i><span>Mon–Fri 8 AM–6 PM</span></span>'
STARS='<span class="st" aria-hidden="true">★★★★★</span>'

# ---------- data ----------
# (id, name, group, photo or None, description, alt)  — names from old-site gallery captions
SERV=[
 ('commercial','Commercial Construction','build',None,'New construction and repairs/restorations for businesses. Occupied, fully operational job sites are never a problem, and multi-phase jobs can be planned, managed and built.',''),
 ('residential','Residential Construction','build',None,'Construction and repair work for homes, from a single fix to a larger project.',''),
 ('remodels','Remodels','build','remodel-arch','Interior remodels that rework existing rooms and spaces.','Remodeling crew working inside an arched living room'),
 ('cabin','Cabin Finish Outs','build','cabin-finish-out','Interior finish outs that turn a shell into a finished, livable cabin.','Finished cabin interior with wood-look floors, bed and seating'),
 ('painting','Painting','interior','painting','Interior and exterior painting.','Painter rolling a fresh coat on an interior wall'),
 ('drywall','Drywall Repairs & Installation','interior','drywall','Drywall installation and repairs.','Two crew members installing drywall'),
 ('flooring','Flooring Installation','interior','flooring-tile','Flooring installation, including tile and wood-look plank floors.','Crew member setting large-format floor tile'),
 ('bathroom','Bathroom Remodeling','interior','bath-after','Bathroom remodels, from tub-and-tile to a finished walk-in shower.','Remodeled walk-in shower with marble-look tile and glass door'),
 ('ceiling','Suspended Ceiling Installation','interior','suspended-ceiling','Suspended (drop) ceiling grid and tile installation for commercial spaces.','New suspended ceiling grid with panel lights'),
 ('glazing','Glazing','interior','glazing','Glass and glazing work, such as storefront-style glass doors.','Glass double doors installed at a commercial entrance'),
 ('roofing','Roofing Repairs & Installations','exterior','roofing-shingles','Roof repairs and installations, including new shingle roofs.','Shingle bundles staged on a roof during installation'),
 ('masonry','Masonry','exterior','masonry','Masonry work on block and brick walls.','Crew in safety vests working along a block wall'),
 ('fence','Block Fences','exterior','block-fence-2','Concrete block fence construction.','Masons laying concrete block for a fence'),
 ('slabs','Cement Slabs','exterior','cement-slab','Concrete slab pours and finishing.','Crew placing concrete from a mixer truck'),
 ('asphalt','Asphalt','exterior','asphalt','Asphalt paving.','Freshly laid asphalt lot'),
 ('parking','Parking Lot Asphalt & Restriping','exterior','parking-lot-aerial','Parking lot asphalt and restriping, with stalls, arrows and hatched zones.','Aerial view of a freshly paved and striped parking lot'),
 ('landscaping','Landscaping Services','exterior',None,'Landscaping services for residential and commercial properties.',''),
 ('ranch','Ranch Services','ranch','ranch-services','Ranch work and land clearing with heavy equipment.','Heavy equipment clearing brush on ranch land'),
 ('septic','Septic Tank Services','ranch',None,'Septic tank services.',''),
 ('dump','Dump Trailer Services','ranch','dump-trailer-gravel','Dump trailer services for hauling material such as gravel.','Dump trailer loaded with gravel'),
 ('moving','Moving Services','ranch','moving-truck','Moving services with a stake-bed truck.','Sanchez Construction Services truck loaded with furniture'),
 ('furniture','Furniture Assembly','ranch','furniture-assembly','Furniture assembly, including office workstations.','Crew member assembling office workstation desks'),
 ('gazebo','Gazebo Assembly','ranch','gazebo','Gazebo assembly for backyards and outdoor living areas.','Assembled gazebo with curtains and string lights at dusk'),
]
GROUPS=[('build','Build &amp; Manage','Commercial and residential projects, remodels and finish outs, planned and managed from start to finish.'),
        ('interior','Interiors','Paint, drywall, flooring, bathrooms, ceilings and glass.'),
        ('exterior','Exterior &amp; Site','Roofing, masonry, concrete, asphalt and the ground around the building.'),
        ('ranch','Ranch, Hauling &amp; Assembly','Ranch services, septic, dump trailer, moving and assembly.')]
NS=len(SERV)
WIDE={'commercial','cabin','roofing','parking'}
# Reviews: Google (full text, GBP) + old-site widget (Marisela); verbatim
REV=[
 ('Annie Serna','Google review','I contacted Sanchez Construction Services when I needed the roof replaced. Mr. Sanchez and his staff were prompt and very professional in their initial visit and with the estimate. Upon agreeing to the job, they were on it the very next day and finished within two days. Not only did they replace the roof; they removed any all all debris from the property. We have had strong rain and winds since the roof was replaced and there have not been any problems with it. I have since asked Mr. Sanchez and crew to do other jobs and the results are always the same. Timely, professional and work is of the best quality. The professionalism of Sanchez Construction is like none I have ever seen. I recommend them for any and all jobs without any hesitation whatsoever.',
  'They were on it the very next day and finished within two days. Not only did they replace the roof; they removed any all all debris from the property.'),
 ('Nora Menza','Google review','I highly recommend Sanchez Construction Services. This company takes pride in the quality of work they do. They have installed new roof shingles on our home, renovated our four bathrooms, and painted the siding of our house. Everything is done in a timely and professional manner with close attention to detail. The employees are respectful and trustworthy. Their work is excellent! ~~Jorge and Nora Mendoza',
  'This company takes pride in the quality of work they do. Everything is done in a timely and professional manner with close attention to detail.'),
 ('Eli Lopez','Google review','I’m a manager at a prominent Pediatric Dentistry here in Laredo. We had a major repair to do at the office. Because of the nature of our business we had to schedule the repair to be after hours. We contacted Sanchez Construction Services and they were extremely prompt with their response. They came out to the office gave us an estimate and by the next day we had our issue fixed. The very next day the owner of the company came out to the office to introduce himself and to let us know that any type of construction work we need he would be able to take care of us. Hands down the best in South Texas! Recommend them 100%!',
  'They came out to the office gave us an estimate and by the next day we had our issue fixed. Hands down the best in South Texas!'),
 ('monica robledo','Google review','Excellent Customer Service! The team at Sanchez Construction is very professional, experience and dependable. Highly recommended Sanchez, for any and all of my home repairs and construction needs. You WILL NOT be disappointed!',
  'The team at Sanchez Construction is very professional, experience and dependable. You WILL NOT be disappointed!'),
 ('Marisela Castaneda','Review shown on the company’s previous website','I was very impressed with the time it took to get my iron gate repaired. I called on a Monday morning and by Tuesday Morning my gate was as good as new. Mr. Sanchez is very professional and courteous.',
  'I called on a Monday morning and by Tuesday Morning my gate was as good as new. Mr. Sanchez is very professional and courteous.'),
]
DAYS=[(1,'Monday','8 AM – 6 PM'),(2,'Tuesday','8 AM – 6 PM'),(3,'Wednesday','8 AM – 6 PM'),(4,'Thursday','8 AM – 6 PM'),(5,'Friday','8 AM – 6 PM'),(6,'Saturday','Closed'),(0,'Sunday','Closed')]
FAQ=[
 ('What kind of work does Sanchez Construction Services do?',f'Commercial and residential construction, including new construction and repairs/restorations, plus {NS} listed services such as roofing, painting, drywall, flooring, bathroom remodeling, masonry, cement slabs, asphalt and parking lot restriping, ranch services, dump trailer and moving services.'),
 ('Can you work at a business that stays open during construction?','Yes. Occupied and fully operational job sites are never a problem, and multi-phase jobs can be planned, managed and built.'),
 ('How do I get a quote?',f'Call {PHONE} Monday to Friday, 8 AM to 6 PM, or email {EMAIL} with a few details about your project.'),
 ('Where are you located?',f'2507 Market Street, Laredo, Texas 78043.'),
 ('What happens when the build is finished?','Post-construction covers site cleanup, systems training, final inspections and move-in coordination, followed by a final walkthrough to make sure you are completely satisfied.'),
]

# ---------- layout ----------
NAV=[('index.html','Home'),('services.html','Services'),('projects.html','Projects'),('reviews.html','Reviews'),('contact.html','Contact')]
def header(cur):
    links=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<header class="hdr"><div class="wrap"><a class="brand" href="index.html" aria-label="{NAME} home"><img src="assets/mark-dark.svg" width="64" height="21" alt=""><span><b>SANCHEZ</b><small>CONSTRUCTION SERVICES</small></span></a>
<nav class="nav" aria-label="Main">{links}</nav><div class="hdr-cta">{STATUS}{b_call('sm','Call')}{b_quote('ghost sm','Quote')}</div>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button></div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">{''.join(f'<a href="{h}">{t}</a>' for h,t in NAV)}<div class="ctas">{b_call()}{b_quote()}</div><p style="margin-top:18px">{STATUS}</p></nav>'''
def footer():
    return f'''<section class="cta-band" aria-labelledby="cta-h"><div class="wrap cta-grid"><div data-r>
<p class="kicker">Got a project?</p><h2 id="cta-h">Let’s get the job done.</h2>
<p>Call for a quote or tell us about your project. New construction, repairs, restorations and everything on our list, in Laredo.</p>
<div class="ctas">{b_call('dark')}{b_quote('dark" style="--bg:transparent;--fg:#111;border-color:#111','Request a quote')}</div></div>
<div class="cta-card" data-r="right"><dl><dt>Phone</dt><dd><a href="{TEL}">{PHONE}</a></dd><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd><dt>Office</dt><dd><a href="{DIR}" target="_blank" rel="noopener">{ADDR}</a></dd><dt>Hours</dt><dd>Mon–Fri 8 AM–6 PM<br>Sat &amp; Sun closed</dd><dt>Now</dt><dd>{STATUS}</dd></dl></div></div></section>
<footer class="ftr"><div class="wrap"><div class="fgrid">
<div><img class="logo" src="assets/mark-dark.svg" width="150" height="49" alt="" loading="lazy"><p class="fbrand">SANCHEZ<small>CONSTRUCTION SERVICES</small></p><p>{NAME} is a general contractor in Laredo, Texas. Building trust with quality work. Rated 5.0 from 19 Google reviews.</p></div>
<div><h2>Office</h2><address style="font-style:normal">{NAME}<br>2507 Market Street<br>Laredo, Texas 78043</address><p style="margin-top:10px"><a href="{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h2>Hours</h2><ul><li>Monday–Friday: 8 AM–6 PM</li><li>Saturday: Closed</li><li>Sunday: Closed</li></ul></div>
<div><h2>Explore</h2><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV)}<li><a href="{GMAPS}" target="_blank" rel="noopener">Google reviews</a></li></ul></div>
</div><div class="fine"><span>© 2026 {NAME}. All rights reserved.</span><span>Website design by RGWebD</span></div></div></footer>
<div class="mbar" role="navigation" aria-label="Quick actions">{b_call('','Call now')}{b_quote('ghost','Get a quote')}</div>
<div class="demo" role="note">Design preview by RGWebD <button aria-label="Dismiss design preview note">×</button></div>'''

def biz(extra=None):
    d={"@type":"GeneralContractor","@id":BASE+"#business","name":NAME,"url":BASE,"telephone":"+1-956-206-3885","email":EMAIL,
       "description":"General contractor in Laredo, Texas offering commercial and residential construction, repairs and restorations, roofing, painting, drywall, flooring, remodeling, masonry, concrete, asphalt and parking lot restriping, ranch, hauling and moving services.",
       "image":[BASE+"assets/og-image.jpg",BASE+"assets/img/dump-trailer-loader.webp"],"logo":BASE+"assets/icon-512.png",
       "address":{"@type":"PostalAddress","streetAddress":"2507 Market St","addressLocality":"Laredo","addressRegion":"TX","postalCode":"78043","addressCountry":"US"},
       "geo":{"@type":"GeoCoordinates","latitude":27.5035321,"longitude":-99.4703193},"hasMap":GMAPS,"areaServed":{"@type":"City","name":"Laredo, Texas"},
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"}],
       "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"19","bestRating":"5"},"sameAs":[GMAPS],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":"Construction services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s[1],"url":BASE+"services.html#"+s[0]}} for s in SERV]}}
    if extra: d.update(extra)
    return d
def reviews_ld(): return {"review":[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":t} for n,src,t,_ in REV]}
def crumbs_ld(name,file): return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":name,"item":BASE+file}]}

def page(file,title,desc,body,ld,pre=''):
    url=BASE+('' if file=='index.html' else file)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="theme-color" content="#121316"><meta name="robots" content="index,follow">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="en_US"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{NAME} — general contractor in Laredo, TX">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/anybody-100_900.woff2" as="font" type="font/woff2" crossorigin>{pre}
<link rel="stylesheet" href="assets/styles.css"><script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":ld},ensure_ascii=False)}</script></head>
<body>{header(file)}<main id="main">{body}</main>{footer()}<script src="assets/script.js" defer></script></body></html>'''

def phero(img,kick,h1,lead,crumb,alt):
    return f'''<section class="phero grain"><div class="bg" data-px="0.22">{pic(img,alt,eager=True)}</div><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / {crumb}</p><p class="kicker" data-r>{kick}</p><h1 class="split">{h1}</h1><p class="lead" data-r>{lead}</p><div class="ctas" data-r style="margin-top:26px">{b_call()}{b_quote()}</div></div><div class="frame" aria-hidden="true"></div></section>'''
def sid(i): return f'{i+1:02d}'

# ---------- HOME ----------
names=[s[1] for s in SERV]
tapeA=''.join(f'<li>{e(n)}</li>' for n in names[:12])
tapeB=''.join(f'<li>{e(n)}</li>' for n in names[12:]+names[:2])
MARK=(GEN/'brand'/'mark-dark.svg').read_text()
reel=[('cabin-finish-out','Cabin Finish Outs','Build & Manage','Finished cabin interior'),('roofing-shingles','Roofing','Exterior','Shingles staged during a roof installation'),('gazebo','Gazebo Assembly','Assembly','Assembled gazebo at dusk'),('bath-after','Bathroom Remodeling','Interiors','Remodeled walk-in shower'),('masonry','Masonry','Exterior & Site','Crew working on a block wall'),('ranch-services','Ranch Services','Ranch','Equipment clearing brush on ranch land'),('suspended-ceiling','Suspended Ceilings','Interiors','New suspended ceiling with panel lights'),('cement-slab','Cement Slabs','Exterior & Site','Concrete pour from a mixer truck')]
reelh=''.join(f'<figure><a href="projects.html" aria-label="{e(t)} — see projects">{pic(n,a)}</a><figcaption><small>{c}</small>{t}</figcaption></figure>' for n,t,c,a in reel)
hs=[(30,52,'Fresh asphalt','New asphalt surface across the whole lot.'),(52,22,'Stall striping','Bright yellow stall lines, laid out evenly on both sides.'),(55.5,78,'Directional arrows','Painted arrows to guide traffic in and out.'),(80,90,'Hatched zones','Hatched no-parking areas at the entrance corners.')]
hsh=''.join(f'<button class="hs-pin" style="left:{x}%;top:{y}%" aria-expanded="false" aria-controls="hs{i}" aria-label="{t}">{i+1}</button><div class="hs-tip{' below' if y<40 else ''}" id="hs{i}" role="tooltip" style="left:{x}%;top:{y}%"><b>{t}</b>{d}</div>' for i,(x,y,t,d) in enumerate(hs))
rvh=''.join(f'<figure class="rv-card{" on" if i==0 else ""}">{STARS.replace("st","st")}<blockquote>“{e(s)}”</blockquote><cite>{e(n)} · {src}</cite></figure>' for i,(n,src,t,s) in enumerate(REV))
dots=''.join('<i></i>' for _ in REV)
home=f'''<div class="loader" aria-hidden="true"><div class="gate l"></div><div class="gate r"></div><div class="mk">{MARK.replace('<path','<path pathLength="260"')}</div><p class="cap">SANCHEZ CONSTRUCTION SERVICES</p></div>
<section class="hero grain"><div class="bg" data-px="0.18">{pic('dump-trailer-loader','Wheel loader dumping material into a black dump trailer behind a white pickup',eager=True)}</div>
<div class="wrap"><p class="kicker coords">General contractor · Laredo, Texas<span class="geo"> · 27.5035° N 99.4703° W</span></p>
<h1 class="split"><span class="o">Building trust</span> with <span class="y">quality work.</span></h1>
<p class="lead">Commercial and residential construction, repairs and restorations, planned, managed and built by one team. We’ll get the job done!</p>
<div class="ctas">{b_call()}{b_quote()}</div>
<div class="trust"><a class="chip" href="{GMAPS}" target="_blank" rel="noopener">{STARS}<b>5.0</b> · 19 Google reviews</a>{STATUS}</div></div>
<p class="side" aria-hidden="true">2507 MARKET ST · LAREDO TX</p><div class="edge" aria-hidden="true"></div></section>
<section class="tapes" aria-label="Services"><div class="tape a"><ul>{tapeA}</ul><ul aria-hidden="true">{tapeA}</ul></div><div class="tape b"><ul>{tapeB}</ul><ul aria-hidden="true">{tapeB}</ul></div></section>
<section class="sec light bp-l" aria-labelledby="about-h"><span class="ghost-type" style="right:-4vw;top:40px" aria-hidden="true">Laredo</span><div class="wrap">
<div class="head-row"><div><p class="kicker">About us</p><h2 class="h2 split" id="about-h">One crew. <em>Start to finish.</em></h2></div><p class="lead" data-r>We work with architects and designers to produce beautiful, functional structures, and bring project management skills and extensive construction experience to every job.</p></div>
<div class="pillars">
<article class="pillar" data-r><span class="dim" aria-hidden="true"></span><span class="no">01</span><h3>What we do</h3><p>Our commercial projects include both new construction and repairs/restorations. Occupied and fully operational job sites are never a problem. And we can also plan, manage, and build multi-phase jobs.</p></article>
<article class="pillar" data-r style="transition-delay:.12s"><span class="dim" aria-hidden="true"></span><span class="no">02</span><h3>Working together</h3><p>An end-to-end client experience that includes seamless communication, budgeting, staffing, on-site organization, and solid, quality handiwork every time.</p></article>
<article class="pillar" data-r style="transition-delay:.24s"><span class="dim" aria-hidden="true"></span><span class="no">03</span><h3>Why choose us</h3><p>Built for eye-catching beauty and efficiency. We know how to make the most out of limited space: if you don’t have room to build out, we’ll build up.</p></article>
</div></div></section>
<section class="sec bp" aria-labelledby="num-h" style="padding-block:90px"><div class="wrap"><p class="kicker">By the numbers</p><h2 class="h2 split" id="num-h" style="margin-bottom:46px">Measured <em>twice.</em></h2>
<div class="stats">
<div class="stat"><div class="num" data-count="5.0" data-dec="1"><b>5.0</b><small>★</small></div><div class="lab">Google rating</div><div class="rule" style="--f:1"><i></i></div></div>
<div class="stat"><div class="num" data-count="19"><b>19</b></div><div class="lab">Google reviews</div><div class="rule" style="--f:.76"><i></i></div></div>
<div class="stat"><div class="num" data-count="{NS}"><b>{NS}</b></div><div class="lab">Services on our list</div><div class="rule" style="--f:.92"><i></i></div></div>
<div class="stat"><div class="num" data-count="3"><b>3</b></div><div class="lab">Build phases, start to finish</div><div class="rule" style="--f:.5"><i></i></div></div>
</div></div></section>
<section class="sec ink" aria-labelledby="feat-h"><span class="ghost-type" style="left:-3vw;bottom:-30px" aria-hidden="true">Restripe</span><div class="wrap feat">
<div class="hsframe" data-r="zoom">{pic('parking-lot-aerial','Aerial view of a parking lot with fresh asphalt and new yellow striping')}{hsh}</div>
<div><p class="kicker">Featured work</p><h2 class="h2 split" id="feat-h" style="font-size:clamp(34px,4.2vw,60px)">Parking lot asphalt <em>&amp; restriping.</em></h2>
<ol class="hs-list" data-r>{''.join(f'<li><span><b style="color:#fff">{t}.</b> {d}</span></li>' for x,y,t,d in hs)}</ol>
<div class="ctas" data-r><a class="btn mag" href="services.html#exterior">Exterior &amp; site services</a></div></div></div></section>
<section class="sec" aria-labelledby="reel-h" style="padding-bottom:70px"><div class="wrap head-row" style="margin-bottom:34px"><div><p class="kicker">Recent work</p><h2 class="h2 split" id="reel-h">From the <em>job site.</em></h2></div><p class="reel-hint">Drag or swipe →</p></div>
<div class="reel" tabindex="0" aria-label="Recent project photos">{reelh}</div></section>
<section class="sec light" aria-labelledby="rv-h"><div class="wrap rv-wrap">
<div class="big-rate" data-r="left"><p class="kicker">Google rating</p><div class="n">5.0</div><div class="st" aria-label="5 out of 5 stars">★★★★★</div><p>From 19 reviews on Google.</p><p style="margin-top:18px"><a class="btn dark sm" href="reviews.html">Read the reviews</a></p></div>
<div class="rv" aria-roledescription="carousel" aria-label="Customer reviews"><h2 class="sr" id="rv-h" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">What customers say</h2><div class="rv-track">{rvh}</div>
<div class="rv-ctl"><button class="pv" aria-label="Previous review">←</button><button class="nx" aria-label="Next review">→</button><div class="rv-dots" aria-hidden="true">{dots}</div></div></div></div></section>
<section class="sec" aria-labelledby="go-h"><div class="wrap"><div class="head-row"><div><p class="kicker">Explore</p><h2 class="h2 split" id="go-h">Pick a <em>direction.</em></h2></div></div>
<div class="cards">
<a class="card tilt" href="services.html">{pic('drywall','Crew installing drywall')}<span class="arr" aria-hidden="true">→</span><span class="in2"><small>{NS} SERVICES</small><h3>Services</h3><p>The full list, plus how a build runs from pre-construction to walkthrough.</p></span></a>
<a class="card tilt" href="projects.html">{pic('glazing','Glass double doors at a commercial entrance')}<span class="arr" aria-hidden="true">→</span><span class="in2"><small>GALLERY</small><h3>Projects</h3><p>Real photos from real jobs, plus a bathroom before &amp; after.</p></span></a>
<a class="card tilt" href="reviews.html">{pic('furniture-assembly','Crew member assembling office desks')}<span class="arr" aria-hidden="true">→</span><span class="in2"><small>5.0 ★ GOOGLE</small><h3>Reviews</h3><p>What homeowners and businesses in Laredo say.</p></span></a>
<a class="card tilt" href="contact.html">{pic('moving-truck','Sanchez Construction Services truck',attrs='style="object-position:88% 50%"')}<span class="arr" aria-hidden="true">→</span><span class="in2"><small>MARKET ST · LAREDO</small><h3>Contact</h3><p>Call, email or visit. Hours, map and a quick quote form.</p></span></a>
</div></div></section>'''

# ---------- SERVICES ----------
def svc_card(i,s):
    sid_,n,g,ph,d,alt=s
    media=f'<div class="ph">{pic(ph,alt)}</div>' if ph else f'<div class="ph type" aria-hidden="true"><span>{"".join(w[0] for w in n.replace("&","").split()[:2])}</span></div>'
    wide=' wide' if sid_ in WIDE else ''
    return f'<article class="svc{wide}" id="{sid_}" data-r>{media}<div class="bd"><span class="ix">{sid(i)} / {NS}</span><h3>{e(n)}</h3><p>{e(d)}</p></div></article>'
grph=''
k=0
for gi,(g,gt,gd) in enumerate(GROUPS):
    items=[s for s in SERV if s[2]==g]
    cards=''
    for s in items: cards+=svc_card(SERV.index(s),s)
    grph+=f'<section class="grp" id="{g}" aria-labelledby="g-{g}"><div class="wrap"><div class="grp-h"><span class="gn" aria-hidden="true">{gi+1:02d}</span><div><h2 class="h2" id="g-{g}" style="font-size:clamp(34px,4.4vw,62px)">{gt}</h2><p>{gd}</p></div></div><div class="svcs">{cards}</div></div></section>'
phases=[('Pre-Construction','Plan &amp; budget','This phase includes constant monitoring and interaction. We keep an eye on budgets to ensure the lowest costs, stay on top of schedules for timely delivery and work closely with the design team to create your vision.'),
        ('Construction','Build &amp; manage','Working with trusted subcontractors, we keep them accountable throughout the entire build. From sequence to production and quality control, we stay focused on the goal.'),
        ('Post-Construction','Close out','The last step in any build. This phase includes site cleanup, systems training, final inspections and move-in coordination. After completion, we have a final walkthrough to ensure your complete satisfaction.')]
tlh=''.join(f'<div class="tl-step"><div class="stake">{i+1}</div><div data-r><span class="tag">Phase {i+1} · {t}</span><h3>{n}</h3><p>{d}</p></div></div>' for i,(n,t,d) in enumerate(phases))
services=phero('dump-trailer-loader','We do it all',f'{NS} services. <span style="color:var(--y)">One call.</span>','Commercial and residential construction, interiors, exterior and site work, ranch and hauling. Here is everything on our list, and how a build runs.','Services','Wheel loader filling a dump trailer with material')+f'''
<nav class="svc-nav" aria-label="Service groups"><div class="wrap">{''.join(f'<a href="#{g}">{gt}</a>' for g,gt,_ in GROUPS)}<a href="#process">How it works</a></div></nav>
{grph}
<section class="sec light bp-l" id="process" aria-labelledby="proc-h" style="margin-top:80px;scroll-margin-top:120px"><div class="wrap"><div class="head-row"><div><p class="kicker">How it works</p><h2 class="h2 split" id="proc-h">Three phases. <em>No loose ends.</em></h2></div><p class="lead" data-r>Every build follows the same path, from the first budget check to the final walkthrough.</p></div>
<div class="tl"><div class="tl-line" aria-hidden="true"><i></i></div>{tlh}</div></div></section>'''

# ---------- PROJECTS ----------
GAL=[('roofing-shingles','Roofing','exterior'),('gazebo','Gazebo assembly','assembly'),('painting','Painting','interior'),('parking-lot-aerial','Parking lot restriping','exterior'),
     ('flooring-tile','Flooring installation','interior'),('dump-trailer-loader','Dump trailer services','ranch'),('glazing','Glazing','interior'),('masonry','Masonry','exterior'),('furniture-assembly','Furniture assembly','assembly'),
     ('remodel-arch','Remodels','build interior'),('cement-slab','Cement slabs','exterior'),('suspended-ceiling','Suspended ceiling','interior'),('ranch-services','Ranch services','ranch'),('roofing-deck','Roofing','exterior'),
     ('block-fence-1','Block fence','exterior'),('flooring-wood','Flooring','interior'),('asphalt','Asphalt','exterior'),('dump-trailer-gravel','Dump trailer services','ranch'),('drywall','Drywall','interior'),('block-fence-2','Block fence','exterior'),('moving-truck','Moving services','ranch')]
ALT={'cabin-finish-out':'Finished cabin interior with bed, seating and wood-look floor','roofing-shingles':'Shingle bundles staged on a roof','gazebo':'Gazebo with curtains and string lights at dusk','painting':'Painter rolling an interior wall','parking-lot-aerial':'Aerial view of a paved, striped parking lot','flooring-tile':'Crew member setting floor tile','dump-trailer-loader':'Wheel loader filling a dump trailer','glazing':'Glass double doors at a commercial entrance','masonry':'Crew working along a block wall','furniture-assembly':'Crew member assembling office desks','remodel-arch':'Crew working in an arched living room','cement-slab':'Concrete pour from a mixer truck','suspended-ceiling':'New suspended ceiling with panel lights','ranch-services':'Equipment clearing brush on ranch land','roofing-deck':'Roofers on a roof deck with underlayment','block-fence-1':'Pallets of block delivered for a fence','flooring-wood':'Crew installing wood-look flooring','asphalt':'Freshly laid asphalt','dump-trailer-gravel':'Dump trailer loaded with gravel','drywall':'Two crew members hanging drywall','block-fence-2':'Masons laying block for a fence','moving-truck':'Company truck loaded for a move'}
galh=''.join(f'<figure data-cat="{c}"><button type="button" data-full="assets/img/{n}.webp" data-cap="{e(t)}" aria-label="Open photo: {e(t)}">{pic(n,ALT[n])}</button><figcaption>{e(t)}</figcaption></figure>' for n,t,c in GAL)
filters=[('all','All'),('build','Build &amp; remodel'),('interior','Interiors'),('exterior','Exterior &amp; site'),('ranch','Ranch &amp; hauling'),('assembly','Assembly')]
projects=phero('cabin-finish-out','Our work','Built for <span style="color:var(--y)">beauty &amp; efficiency.</span>','We know how to make the most out of limited space. If you don’t have room to build out, we’ll build up to incorporate all you need.','Projects','Finished cabin interior with wood-look floors')+f'''
<section class="sec light" aria-labelledby="ba-h"><div class="wrap ba-wrap">
<div><p class="kicker">Before &amp; after</p><h2 class="h2 split" id="ba-h">Tub to <em>walk-in shower.</em></h2><p class="lead" data-r style="margin-top:22px">A dated tub-and-tile bath turned into a walk-in shower with marble-look tile, a niche, black fixtures and a frameless glass door. Drag the handle to compare.</p>
<div class="ctas" data-r style="margin-top:26px"><a class="btn dark" href="services.html#bathroom">Bathroom remodeling</a></div></div>
<div class="ba" data-r="zoom"><img src="assets/img/bath-before.webp" width="860" height="974" alt="Before: tub with sliding glass doors and beige tile" loading="lazy"><img class="aft" src="assets/img/bath-after.webp" width="860" height="974" alt="After: walk-in shower with marble-look tile and frameless glass" loading="lazy"><span class="knob" aria-hidden="true"></span><span class="ba-l b" aria-hidden="true">Before</span><span class="ba-l a" aria-hidden="true">After</span><input type="range" min="0" max="100" value="50" aria-label="Before and after comparison slider"></div>
</div></section>
<section class="sec" aria-labelledby="gal-h"><div class="wrap"><div class="head-row"><div><p class="kicker">Gallery</p><h2 class="h2 split" id="gal-h">On the <em>job.</em></h2></div><p class="lead" data-r>Tap any photo to open it full size.</p></div>
<div class="filters" role="group" aria-label="Filter projects">{''.join(f'<button type="button" data-f="{f}" aria-pressed="{"true" if f=="all" else "false"}">{t}</button>' for f,t in filters)}</div>
<div class="gal">{galh}</div></div></section>
<div class="lbx" role="dialog" aria-modal="true" aria-label="Photo viewer"><button class="x" aria-label="Close">×</button><button class="pv" aria-label="Previous photo">←</button><figure><img alt=""><figcaption></figcaption></figure><button class="nx" aria-label="Next photo">→</button></div>'''

# ---------- REVIEWS ----------
rch=''.join(f'<figure class="rcard" data-r><span class="q" aria-hidden="true">”</span><div class="st" aria-label="5 out of 5 stars">★★★★★</div><blockquote>{e(t)}</blockquote><figcaption><cite>{e(n)} · {src}</cite></figcaption></figure>' for n,src,t,_ in REV)
reviews=phero('masonry','Reviews','Rated 5.0. <span style="color:var(--y)">Built on trust.</span>','Homeowners and businesses in Laredo rate Sanchez Construction Services 5.0 from 19 reviews on Google. Here are a few in their own words.','Reviews','Crew in safety vests working along a block wall')+f'''
<section class="sec light bp-l" aria-labelledby="rv2-h"><div class="wrap">
<div class="head-row"><div><p class="kicker">In their words</p><h2 class="h2 split" id="rv2-h">Timely. Professional. <em>Trustworthy.</em></h2></div>
<div class="big-rate" data-r="right" style="max-width:340px"><div class="n">5.0</div><div class="st" aria-label="5 out of 5 stars">★★★★★</div><p>19 Google reviews</p><p style="margin-top:16px"><a class="btn dark sm" href="{GMAPS}" target="_blank" rel="noopener">See all on Google</a></p></div></div>
<div class="rgrid">{rch}</div>
<p style="margin-top:30px;color:#555;font-size:14px">Reviews are quoted word for word from Google, except where marked as shown on the company’s previous website.</p></div></section>'''

# ---------- CONTACT ----------
hours=''.join(f'<li data-d="{d}"><span>{n}</span><span>{h}</span></li>' for d,n,h in DAYS)
faqh=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in FAQ)
opts=''.join(f'<option>{e(s[1])}</option>' for s in SERV)
contact=phero('moving-truck','Contact','Tell us about <span style="color:var(--y)">your project.</span>','Send us a message, or call us for a quote. Tell us more about your project, and we will connect you with the services to fit your needs.','Contact','Sanchez Construction Services company truck')+f'''
<section class="sec light" aria-labelledby="c-h"><div class="wrap">
<h2 class="h2 split" id="c-h" style="margin-bottom:40px">Give us <em>a call!</em></h2>
<div class="cgrid">
<div class="cbox" data-r><p class="kicker">Reach us</p>
<p style="font:900 clamp(26px,2.6vw,38px)/1 var(--disp);font-stretch:125%;margin:0 0 10px;white-space:nowrap"><a href="{TEL}" style="text-decoration:none">{PHONE}</a></p>
<p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>{NAME}<br>2507 Market Street, Laredo, Texas 78043</p>
<div class="ctas">{b_call('dark')}<a class="btn" href="{DIR}" target="_blank" rel="noopener">Get directions</a></div>
<h3 style="font-size:22px;margin:34px 0 10px">Hours</h3><p style="margin:0 0 6px">{STATUS.replace('class="status"','class="status" style="background:#18191C;color:#fff"')}</p><ul class="hours">{hours}</ul></div>
<div class="cbox" id="quote" data-r style="scroll-margin-top:100px"><p class="kicker">Get a quote</p><h3 style="font-size:28px;margin-bottom:18px">Request a quote</h3>
<form class="form" id="quote-form"><div class="row"><label>Name<input name="name" autocomplete="name" required></label><label>Phone<input name="phone" type="tel" autocomplete="tel"></label></div>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Project type<select name="type">{opts}<option>Something else</option></select></label>
<label>Project details<textarea name="msg" rows="5" placeholder="What do you need built, fixed or restored? Where, and when?"></textarea></label>
<button class="btn dark" type="submit">Send by email</button><p style="font-size:13px;color:#666;margin:0">Opens your email app with your message ready to send to {EMAIL}.</p></form></div>
</div>
<div style="margin-top:28px;border-radius:var(--r);overflow:hidden;height:420px"><iframe class="mapf" title="Map to {NAME}, 2507 Market St, Laredo TX" src="{MAPEMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
<section class="sec" aria-labelledby="faq-h" style="background:var(--chalk2);color:#18191C"><div class="wrap" style="max-width:900px"><p class="kicker" style="color:#B07D00">FAQ</p><h2 class="h2 split" id="faq-h" style="margin-bottom:30px">Good <em style="color:var(--red)">questions.</em></h2><div class="faq">{faqh}</div></div></section>'''

nf=f'''<section class="nf bp"><div class="wrap"><p class="kicker" style="justify-content:center">Error 404</p><h1>404</h1><h2 style="font-size:clamp(26px,3vw,40px);margin:10px 0 20px">This page is still under construction.</h2><p class="lead" style="margin:0 auto 28px">The page you were looking for isn’t here. Head back to the homepage or give us a call.</p><div class="ctas" style="justify-content:center"><a class="btn" href="/sanchezconstructiontx-demo/">Back to home</a>{b_call('ghost')}</div></div></section>'''

PAGES=[
 ('index.html','Sanchez Construction Services | General Contractor in Laredo, TX',f'General contractor in Laredo, TX. Commercial & residential construction, repairs, roofing, remodeling, concrete, asphalt & more. 5.0★ on Google. Call {PHONE}.',home,[biz(reviews_ld()),{"@type":"WebSite","name":NAME,"url":BASE}],
  '<link rel="preload" as="image" href="assets/img/dump-trailer-loader.webp" fetchpriority="high">'),
 ('services.html','Construction Services in Laredo, TX | Sanchez Construction Services',f'{NS} services in Laredo, TX: commercial & residential construction, remodels, roofing, painting, drywall, flooring, masonry, cement slabs, asphalt, ranch, dump trailer & moving.',services,[biz(),crumbs_ld('Services','services.html')]+[{"@type":"Service","name":s[1],"description":s[4],"provider":{"@id":BASE+"#business"},"areaServed":"Laredo, TX","url":BASE+"services.html#"+s[0]} for s in SERV],''),
 ('projects.html','Projects & Gallery | Sanchez Construction Services, Laredo TX','Photos of real Sanchez Construction Services jobs in Laredo: roofing, remodels, a bathroom before & after, cabins, gazebos, masonry, concrete, asphalt and parking lots.',projects,[biz(),crumbs_ld('Projects','projects.html'),{"@type":"ImageGallery","name":"Sanchez Construction Services projects","image":[BASE+f"assets/img/{n}.webp" for n,_,_ in GAL]}],''),
 ('reviews.html','Reviews | Sanchez Construction Services, Laredo TX','Sanchez Construction Services is rated 5.0 from 19 Google reviews. Read what Laredo homeowners and businesses say.',reviews,[biz(reviews_ld()),crumbs_ld('Reviews','reviews.html')],''),
 ('contact.html','Contact & Quote | Sanchez Construction Services, Laredo TX',f'Call {PHONE}, email {EMAIL} or visit 2507 Market St, Laredo, TX 78043. Mon–Fri 8 AM–6 PM. Request a construction quote.',contact,[biz(),crumbs_ld('Contact','contact.html'),{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}],''),
]
for f,t,d,b,ld,pre in PAGES: (OUT/f).write_text(page(f,t,d,b,ld,pre))
p404=page('404.html','Page not found | Sanchez Construction Services','This page could not be found.',nf,[biz()]).replace('<meta name="robots" content="index,follow">','<meta name="robots" content="noindex">')
# 404 is served at any path: use absolute asset paths
p404=p404.replace('href="assets/','href="/sanchezconstructiontx-demo/assets/').replace('src="assets/','src="/sanchezconstructiontx-demo/assets/').replace('href="favicon.ico"','href="/sanchezconstructiontx-demo/favicon.ico"').replace('href="apple-touch-icon.png"','href="/sanchezconstructiontx-demo/apple-touch-icon.png"')
for h,_ in NAV: p404=p404.replace(f'href="{h}"',f'href="/sanchezconstructiontx-demo/{h}"')
p404=p404.replace('href="contact.html#quote"','href="/sanchezconstructiontx-demo/contact.html#quote"')
(OUT/'404.html').write_text(p404)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{"" if f=="index.html" else f}</loc><lastmod>2026-11-25</lastmod></url>' for f,*_ in PAGES)+'</urlset>\n')
(OUT/'llms.txt').write_text(f'''# {NAME}
> General contractor in Laredo, Texas. Commercial and residential construction, including new construction and repairs/restorations. Rated 5.0 from 19 Google reviews.

- Address: 2507 Market St, Laredo, TX 78043
- Phone: {PHONE}
- Email: {EMAIL}
- Hours: Monday–Friday 8 AM–6 PM; Saturday and Sunday closed
- Google Maps: {GMAPS}

## Services ({NS})
{chr(10).join('- '+s[1]+': '+s[4] for s in SERV)}

## How a build runs
- Pre-Construction: budgets, schedules and close work with the design team.
- Construction: trusted subcontractors kept accountable; sequence, production and quality control.
- Post-Construction: site cleanup, systems training, final inspections, move-in coordination and a final walkthrough.

## Pages
- [Home]({BASE}): overview, featured parking lot project, reviews
- [Services]({BASE}services.html): all services and the three-phase process
- [Projects]({BASE}projects.html): photo gallery and bathroom before/after
- [Reviews]({BASE}reviews.html): Google reviews quoted word for word
- [Contact]({BASE}contact.html): phone, email, hours, map, quote form, FAQ
''')
(OUT/'.nojekyll').write_text('')
print('built',len(PAGES)+1,'pages ->',OUT)
