(()=>{
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
/* loader (home only) */
const L=$('.loader');
if(L){const fin=()=>{L.classList.add('done');setTimeout(()=>L.classList.add('gone'),1100)};
 if(RM||sessionStorage.getItem('scs-intro')){L.classList.add('gone')}else{sessionStorage.setItem('scs-intro','1');setTimeout(fin,1500)}}
/* split headline words */
$$('.split').forEach(h=>{const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const f=document.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(t=>{if(!t)return;if(/^\s+$/.test(t)){f.append(t);return}const w=document.createElement('span');w.className='w';const s=document.createElement('span');s.textContent=t;w.append(s);f.append(w)});c.replaceWith(f)}else if(c.nodeType===1)walk(c)})};walk(h);
 $$('.w>span',h).forEach((s,i)=>s.style.transitionDelay=(.12+i*.07)+'s')});
/* reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px',threshold:.08});
$$('[data-r],.split,.pillar,.stat,.tl-step').forEach(el=>RM?el.classList.add('in'):io.observe(el));
if(L&&!RM&&!L.classList.contains('gone')){$$('.hero .split').forEach(h=>{io.unobserve(h);setTimeout(()=>h.classList.add('in'),1500)})}
/* counters */
const cio=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;cio.unobserve(e.target);const el=e.target,t=parseFloat(el.dataset.count),d=+(el.dataset.dec||0),b=el.querySelector('b');if(RM){b.textContent=t.toFixed(d);return}
 const t0=performance.now(),D=1700;const step=n=>{const k=Math.min(1,(n-t0)/D),v=t*(1-Math.pow(1-k,3));b.textContent=(k<1?v:t).toFixed(d);if(k<1)requestAnimationFrame(step)};requestAnimationFrame(step)}),{threshold:.4});
$$('[data-count]').forEach(c=>cio.observe(c));
/* header, progress, parallax, mobile bar, timeline */
const hdr=$('.hdr'),pr=$('.progress'),mbar=$('.mbar'),px=$$('[data-px]'),tl=$('.tl'),tli=$('.tl-line i');
let tick=false;const onScroll=()=>{tick=false;const y=scrollY,H=document.documentElement.scrollHeight-innerHeight;
 if(pr)pr.style.transform=`scaleX(${H>0?y/H:0})`;hdr&&hdr.classList.toggle('scrolled',y>30);
 mbar&&mbar.classList.toggle('show',y>innerHeight*.55);
 if(!RM)px.forEach(el=>{const r=el.parentElement.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)el.style.transform=`translate3d(0,${(-r.top)*parseFloat(el.dataset.px)}px,0)`});
 if(tl&&tli){const r=tl.getBoundingClientRect(),k=Math.min(1,Math.max(0,(innerHeight*.7-r.top)/r.height));tli.style.transform=RM?'none':`scaleY(${k})`}};
addEventListener('scroll',()=>{if(!tick){tick=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();
/* burger */
const bg=$('.burger'),mn=$('#mnav');if(bg&&mn){bg.addEventListener('click',()=>{const o=bg.getAttribute('aria-expanded')!=='true';bg.setAttribute('aria-expanded',o);mn.classList.toggle('open',o);document.body.style.overflow=o?'hidden':''});
 $$('a',mn).forEach(a=>a.addEventListener('click',()=>{bg.setAttribute('aria-expanded','false');mn.classList.remove('open');document.body.style.overflow=''}));
 addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){bg.click();bg.focus()}})}
/* open/closed (America/Chicago) Mon-Fri 8-18 */
const st=$$('[data-status]');if(st.length){const now=new Date(),p=new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(now),g=k=>p.find(x=>x.type===k).value;
 const wd=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(g('weekday')),h=(+g('hour'))%24+(+g('minute'))/60,open=wd>=1&&wd<=5&&h>=8&&h<18;
 const msg=open?'Open now · until 6 PM':(wd>=1&&wd<=5&&h<8)?'Closed · opens 8 AM':(wd>=1&&wd<=4)?'Closed · opens 8 AM tomorrow':'Closed · opens Mon 8 AM';
 st.forEach(s=>{s.classList.add(open?'open':'closed');s.querySelector('span').textContent=msg});
 $$('.hours li[data-d]').forEach(li=>li.classList.toggle('today',+li.dataset.d===wd))}
/* magnetic buttons (button moves slightly; nothing follows the cursor) */
if(!RM&&matchMedia('(hover:hover)').matches)$$('.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.28}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});
/* tilt cards */
if(!RM&&matchMedia('(hover:hover)').matches)$$('.tilt').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform=`rotateY(${x*10}deg) rotateX(${-y*10}deg)`});c.addEventListener('pointerleave',()=>c.style.transform='')});
/* hotspots */
$$('.hs-pin').forEach(b=>{const tip=document.getElementById(b.getAttribute('aria-controls'));const set=o=>{b.setAttribute('aria-expanded',o);tip.classList.toggle('show',o)};
 b.addEventListener('click',()=>{const o=b.getAttribute('aria-expanded')!=='true';$$('.hs-pin').forEach(x=>{if(x!==b){x.setAttribute('aria-expanded','false');document.getElementById(x.getAttribute('aria-controls')).classList.remove('show')}});set(o)});
 b.addEventListener('mouseenter',()=>set(true));b.addEventListener('mouseleave',()=>set(false));b.addEventListener('blur',()=>set(false))});
/* drag reel */
$$('.reel').forEach(r=>{let d=false,sx=0,sl=0,mv=0;r.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;d=true;mv=0;sx=e.clientX;sl=r.scrollLeft});
 addEventListener('pointermove',e=>{if(!d)return;const dx=e.clientX-sx;mv=Math.max(mv,Math.abs(dx));if(mv>5)r.classList.add('drag');r.scrollLeft=sl-dx});
 addEventListener('pointerup',()=>{d=false;setTimeout(()=>r.classList.remove('drag'),0)});r.addEventListener('dragstart',e=>e.preventDefault())});
/* reviews carousel */
$$('.rv').forEach(rv=>{const cs=$$('.rv-card',rv),dots=$$('.rv-dots i',rv);let i=0,t=null,paused=false;
 const go=n=>{i=(n+cs.length)%cs.length;cs.forEach((c,k)=>{c.classList.toggle('on',k===i);c.setAttribute('aria-hidden',k!==i)});dots.forEach((d,k)=>d.classList.toggle('on',k===i))};
 const play=()=>{clearInterval(t);if(!RM)t=setInterval(()=>{if(!paused)go(i+1)},6500)};
 $('.pv',rv).addEventListener('click',()=>{go(i-1);play()});$('.nx',rv).addEventListener('click',()=>{go(i+1);play()});
 rv.addEventListener('mouseenter',()=>paused=true);rv.addEventListener('mouseleave',()=>paused=false);rv.addEventListener('focusin',()=>paused=true);rv.addEventListener('focusout',()=>paused=false);
 let tx=0;rv.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});rv.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50){go(i+(d<0?1:-1));play()}});
 go(0);play()});
/* before/after */
$$('.ba').forEach(b=>{const r=$('input',b);const u=()=>b.style.setProperty('--p',r.value+'%');r.addEventListener('input',u);u()});
/* gallery filter */
const fb=$$('.filters button');fb.forEach(b=>b.addEventListener('click',()=>{fb.forEach(x=>x.setAttribute('aria-pressed',x===b));const f=b.dataset.f;$$('.gal figure').forEach(g=>g.classList.toggle('hide',f!=='all'&&!g.dataset.cat.split(' ').includes(f)))}));
/* lightbox */
const lb=$('.lbx');if(lb){const im=$('img',lb),cap=$('figcaption',lb);let list=[],i=0,last=null;
 const show=n=>{i=(n+list.length)%list.length;const b=list[i];im.src=b.dataset.full;im.alt=b.querySelector('img').alt;cap.textContent=b.dataset.cap||''};
 const open=b=>{last=b;list=$$('.gal figure:not(.hide) button');show(list.indexOf(b));lb.classList.add('open');document.body.style.overflow='hidden';$('.x',lb).focus()};
 const close=()=>{lb.classList.remove('open');document.body.style.overflow='';im.removeAttribute('src');last&&last.focus()};
 $$('.gal button').forEach(b=>b.addEventListener('click',()=>open(b)));
 $('.x',lb).addEventListener('click',close);$('.pv',lb).addEventListener('click',()=>show(i-1));$('.nx',lb).addEventListener('click',()=>show(i+1));
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);
  if(e.key==='Tab'){const f=$$('button',lb),a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
 let sx=0;lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50)show(i+(d<0?1:-1))})}
/* services sub-nav highlight */
const sn=$$('.svc-nav a');if(sn.length){const so=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)sn.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id))}),{rootMargin:'-40% 0px -55% 0px'});$$('.grp').forEach(g=>so.observe(g))}
/* quote form -> mailto */
const qf=$('#quote-form');if(qf)qf.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(qf);const body=`Name: ${d.get('name')}\nPhone: ${d.get('phone')}\nEmail: ${d.get('email')}\nProject type: ${d.get('type')}\n\n${d.get('msg')}`;location.href=`mailto:jcsanc@sbcglobal.net?subject=${encodeURIComponent('Quote request – '+d.get('type'))}&body=${encodeURIComponent(body)}`});
/* demo pill */
const dm=$('.demo');if(dm){if(sessionStorage.getItem('scs-demo'))dm.remove();else $('button',dm).addEventListener('click',()=>{dm.remove();sessionStorage.setItem('scs-demo','1')})}
})();
