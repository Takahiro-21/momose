"""Split a whole-spreadsheet PDF export into one PDF per 納品書 sheet.

usage: python3 split_sheets.py <all.pdf> <out_dir> <prefix>
  e.g. python3 split_sheets.py all.pdf out はなこや納品書R8.11月分
Each 納品書 page (contains "納品書 NO.<n>" and "御中") becomes
<prefix>_NO.<n>.pdf. The 原紙 sheet sits before the NO sheets and also says
"NO.1", so when a NO appears twice the later page wins. Pages for
受付データ and 読み取りメモ have no "御中" and are skipped.
"""
import re, sys, unicodedata, pypdf

src, out, prefix = sys.argv[1:4]
r = pypdf.PdfReader(src)
pages = {}
for i, page in enumerate(r.pages):
    t = unicodedata.normalize("NFKC", page.extract_text() or "")
    m = re.search(r"納品書\s*NO\.?\s*(\d+)", t)
    if not m or "御中" not in t:
        continue
    n = int(m.group(1))
    if n in pages:
        print(f"NO.{n}: page {pages[n]+1} replaced by page {i+1} (earlier one is 原紙)")
    pages[n] = i
for n in sorted(pages):
    w = pypdf.PdfWriter(); w.add_page(r.pages[pages[n]])
    w.write(f"{out}/{prefix}_NO.{n}.pdf")
    print(f"NO.{n} <- page {pages[n]+1}")
