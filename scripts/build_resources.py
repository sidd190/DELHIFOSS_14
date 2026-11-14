"""Render the companion Markdown pages without external packages."""
from html import escape
from pathlib import Path
import re
R = Path(__file__).resolve().parents[1]
FILES = ['README.md','precogly/walkthrough.md','exercises/README.md','resources/further-reading.md','game-theory/README.md','architecture/shop-app.md','threat-model/README.md','threat-model/register.md','demo/README.md']
CSS = 'body{max-width:900px;margin:45px auto;padding:0 25px;background:#f7f8f3;color:#172e27;font:20px/1.6 Arial}h1{font:44px/1.15 Georgia}h2{font-size:28px;margin-top:40px}a{color:#245f48}pre{white-space:pre-wrap;background:#e7eddf;padding:20px;font-size:16px}code{font-size:17px}table{border-collapse:collapse;width:100%;font-size:18px}th,td{padding:12px;border:1px solid #b9cbb6;text-align:left}img{max-width:100%}li{margin:10px 0}@media(max-width:600px){body{font-size:18px}h1{font-size:34px}table{font-size:15px}}'
def inline(text,source):
    text=escape(text)
    def link(m):
        label,url=m.groups()
        if not url.startswith(('http:','https:','#')):
            target=(source.parent/url).resolve()
            if target.is_relative_to(R) and str(target.relative_to(R)) in FILES:url=url[:-3]+'.html'
        return f'<a href="{url}">{label}</a>'
    text=re.sub(r'!\[([^\]]+)\]\(([^ )]+)\)',r'<img src="\2" alt="\1">',text)
    text=re.sub(r'\[([^\]]+)\]\(([^ )]+)\)',link,text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
def render(source):
    result=[];code=False;table=False;listing=None
    def close_list():
        nonlocal listing
        if listing:result.append(f'</{listing}>');listing=None
    for line in source.read_text().splitlines():
        if line.startswith('```'):
            close_list();result.append('</pre>' if code else '<pre>');code=not code;continue
        if code:result.append(escape(line)+'\n');continue
        if line.startswith('|'):
            close_list()
            if not table:result.append('<table>');table=True
            cells=line.strip('|').split('|')
            if all(re.fullmatch(r'[\s:-]+',x) for x in cells):continue
            result.append('<tr>'+''.join('<td>'+inline(x.strip(),source)+'</td>' for x in cells)+'</tr>');continue
        if table:result.append('</table>');table=False
        match=re.match(r'^(?:- |\d+\. )(.*)',line)
        if match:
            kind='ul' if line.startswith('- ') else 'ol'
            if listing!=kind:close_list();result.append(f'<{kind}>');listing=kind
            result.append('<li>'+inline(match[1],source)+'</li>');continue
        close_list()
        heading=re.match(r'^(#{1,3}) (.*)',line)
        if heading:level=len(heading[1]);result.append(f'<h{level}>'+inline(heading[2],source)+f'</h{level}>')
        elif line.strip():result.append('<p>'+inline(line,source)+'</p>')
    close_list()
    if table:result.append('</table>')
    prefix='../'*len(source.relative_to(R).parts[:-1])
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(source.read_text().splitlines()[0].lstrip('# '))+'</title><style>'+CSS+'</style><body><a href="'+prefix+'index.html">← Resources</a>'+''.join(result)+'</body></html>'
for name in FILES:
    source=R/name;source.with_suffix('.html').write_text(render(source))
print(f'Built {len(FILES)} resource pages')
