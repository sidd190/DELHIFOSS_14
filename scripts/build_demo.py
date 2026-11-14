"""Build the standalone GitHub Pages demo from the same local matrix example."""
from pathlib import Path
R = Path(__file__).resolve().parents[1]
page = (R / 'demo/matrix.html').read_text(encoding='utf-8')
page = page.replace('href="../index.html">← Talk kit', 'href="https://github.com/sidd190/DELHIFOSS_14">← Talk resources')
page = page.replace('<title>Which attack is dominated?</title>', '<title>Which attack is dominated? · Your Threat Model Has an Opponent</title><meta name="description" content="Explore attacker choices and strict dominance with an editable loss matrix from the DelhiFOSS talk.">')
(R / 'docs').mkdir(exist_ok=True)
(R / 'docs/index.html').write_text(page, encoding='utf-8')
(R / 'docs/.nojekyll').write_text('', encoding='utf-8')
print('Built docs/index.html for GitHub Pages')
