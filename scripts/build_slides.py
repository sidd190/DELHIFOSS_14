"""Render the audience deck. Its source contains slide content only."""
import json
from html import escape
from pathlib import Path
R = Path(__file__).resolve().parents[1]
slides = json.loads((R / 'presentation/slides.source.json').read_text())
css = (R / 'presentation/slides.css').read_text()
parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Your Threat Model Has an Opponent</title><style>', css, '</style><main id="stage">']
for i, slide in enumerate(slides):
    parts.append(f'<section class="slide {slide["kind"]} {"active" if i == 0 else ""}" aria-label="Slide {i+1}: {escape(slide["title"])}">{slide["body"]}</section>')
parts.append('''</main><nav id="controls" aria-label="Slide controls"><button id="prev" aria-label="Previous slide">←</button><span id="count"></span><button id="next" aria-label="Next slide">→</button><button id="full">Fullscreen F</button></nav><script>
const all=[...document.querySelectorAll('.slide')],stage=document.querySelector('#stage');let current=0,uiTimeout;
function resize(){const scale=Math.min(innerWidth/1280,innerHeight/720);stage.style.transform=`scale(${scale})`;stage.style.marginLeft=`${Math.max(0,(innerWidth-1280*scale)/2)}px`}
function show(n){current=Math.max(0,Math.min(all.length-1,n));all.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',i===current?'false':'true')});document.querySelector('#count').textContent=`${current+1} / ${all.length}`;history.replaceState(null,'','#'+(current+1))}
function full(){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen?.()}
document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);document.querySelector('#full').onclick=full;
addEventListener('mousemove',()=>{document.body.classList.add('ui');clearTimeout(uiTimeout);uiTimeout=setTimeout(()=>document.body.classList.remove('ui'),1800)});
addEventListener('keydown',e=>{if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(all.length-1);if(e.key.toLowerCase()==='f')full()});
addEventListener('resize',resize);const first=Number(location.hash.slice(1));show(Number.isFinite(first)&&first>0?first-1:0);resize();
</script></html>''')
(R / 'presentation/slides.html').write_text(''.join(parts))
print(f'Built {len(slides)} audience slides')
