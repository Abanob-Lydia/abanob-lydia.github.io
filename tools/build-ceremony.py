"""Builds ceremony/index.html — the church-only invitation — from the main index.html.

Run after any change to index.html:   python3 tools/build-ceremony.py
Everything about the reception is removed from the page source itself (not just hidden),
and the link preview points to the ceremony address, never the main one.
"""
import re, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
URL = "https://abanob-lydia.github.io/ceremony/"

def cut(s, start, end, label):
    a = s.find(start)
    if a < 0:
        sys.exit(f"build-ceremony: could not find {label}")
    b = s.find(end, a)
    if b < 0:
        sys.exit(f"build-ceremony: could not find end of {label}")
    return s[:a] + s[b + len(end):]

def sub(s, old, new, label):
    if old not in s:
        sys.exit(f"build-ceremony: could not find {label}")
    return s.replace(old, new)

s = src
# assets live one folder up
s = sub(s, '<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="../">', "charset")
# link preview + canonical point here, not to the main invitation
s = sub(s, '<meta property="og:url" content="https://abanob-lydia.github.io/">',
        f'<meta property="og:url" content="{URL}">\n<link rel="canonical" href="{URL}">\n<meta name="robots" content="noindex">', "og:url")
# remove the reception card
s = cut(s, '  <section class="venue rv">\n    <svg class="cor tl"><use href="#cor"/></svg><svg class="cor tr"><use href="#cor"/></svg><svg class="cor bl"><use href="#cor"/></svg><svg class="cor br"><use href="#cor"/></svg>\n    <h2 class="h"><span class="kick">The</span>Wedding Reception</h2>',
        '</section>\n', "reception section")
# remove the hall sketch script
a = s.find("{const P=[],p=(d,t)=>P.push([d,t]);\n p('M4 186H316')")
b = s.find("draw($('#hall')", a)
if a < 0 or b < 0:
    sys.exit("build-ceremony: could not find hall sketch script")
b = s.find("}\n", b) + 2
s = s[:a] + s[b:]
# calendar: ceremony only, 6–8 PM
s = sub(s, "&dates=20270128T160000Z/20270128T220000Z", "&dates=20270128T160000Z/20270128T180000Z", "calendar dates")
s = re.sub(r"Holy matrimony at 6:00 PM, St\. Mary Church, El Nozha\.\\nReception follows at [^\"]*", "Holy Matrimony at 6:00 PM, St. Mary Church, El Nozha.", s)

for word in ("Reception", "Opulence", "Sheraton", "Rocket", "FOLLOWING THE CEREMONY", "QF3UVmJGjoC9kZSe9", "#hall"):
    if word in s:
        sys.exit(f"build-ceremony: '{word}' is still in the ceremony page")

out = root / "ceremony" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(s, encoding="utf-8")
print("wrote", out.relative_to(root))
