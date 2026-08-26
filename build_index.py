#!/usr/bin/env python3
"""
README.md -> index.html 빌드 스크립트

README.md 규칙:
- 맨 위 프런트매터(title) 유지
- <details> 블록 정확히 2개, 순서대로: [1] 수업 자료 링크  [2] README 가이드
- 수업 자료 링크는 마크다운 리스트로 작성:
    - [카드 제목](링크)              <- 카드 하나 생성 (기본 버튼)
      - <a href="링크" download>파일명</a>   <- 같은 카드 안에 보조 버튼으로 추가 (2칸 들여쓰기)
  즉, 하위(들여쓰기)로 넣은 링크는 같은 카드 안 "추가 자료" 버튼이 됩니다.
"""
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("markdown 패키지가 필요합니다: pip install markdown")

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("beautifulsoup4 패키지가 필요합니다: pip install beautifulsoup4")

ROOT = Path(__file__).parent
README = ROOT / "README.md"
OUT = ROOT / "index.html"

SITE_TITLE = "신성여고 정보과학 수업 자료실"
SITE_LEDE = "수업에서 쓰는 자료와 실습 파일을 여기서 받아가세요."
EYEBROW = "2026 · 정보과학 · 인공지능 기초"
REPO_URL = "https://github.com/Padong/2026_shinseong_AI_Class"

LABELS = ["P₁", "P₂", "P₃", "P₄", "P₅", "P₆", "P₇", "P₈"]


def strip_front_matter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def extract_details_blocks(text: str):
    pattern = re.compile(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", re.DOTALL)
    return [(m.group(1).strip(), m.group(2).strip()) for m in pattern.finditer(text)]


def action_button(href: str, text: str, is_download: bool, primary: bool) -> str:
    if is_download:
        cls = "btn btn-signal" if primary else "btn btn-signal btn-sm"
        extra = f'\n        <a class="card-link" href="{href}" target="_blank" rel="noopener">웹에서 바로 열기 →</a>'
        return f'<a class="{cls}" href="{href}" download>{text} ↓</a>{extra if primary else ""}'
    cls = "btn btn-primary" if primary else "btn btn-primary btn-sm"
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{text} ↗</a>'


def build_material_cards(materials_md: str) -> str:
    html = markdown.markdown(materials_md, extensions=["fenced_code", "sane_lists"])
    soup = BeautifulSoup(html, "html.parser")
    top_ul = soup.find("ul")
    if top_ul is None:
        return ""

    cards = []
    for i, li in enumerate(top_ul.find_all("li", recursive=False)):
        # 이 li 바로 아래(중첩 목록 제외)에 있는 첫 번째 <a> = 카드의 주 링크/제목
        nested_ul = li.find("ul")
        direct_a = None
        for a in li.find_all("a", recursive=False):
            direct_a = a
            break
        if direct_a is None:
            # <li>[텍스트](url) 형태는 <a>가 li 바로 아래에 직접 옴
            direct_a = li.find("a")

        if direct_a is None:
            continue

        title = direct_a.get_text(strip=True)
        href = direct_a.get("href", "#")
        is_dl = direct_a.has_attr("download")
        label = LABELS[i] if i < len(LABELS) else f"P{i+1}"

        buttons = [action_button(href, "다운로드" if is_dl else "자료 열기", is_dl, primary=True)]

        if nested_ul:
            for sub_a in nested_ul.find_all("a"):
                sub_title = sub_a.get_text(strip=True)
                sub_href = sub_a.get("href", "#")
                sub_dl = sub_a.has_attr("download")
                buttons.append(action_button(sub_href, sub_title, sub_dl, primary=False))

        buttons_html = "\n        ".join(buttons)
        cards.append(f'''      <div class="card">
        <div class="tag">{label} · 자료</div>
        <h3>{title}</h3>
        {buttons_html}
      </div>''')

    return "\n\n".join(cards)


def fix_checklists(html: str) -> str:
    return re.sub(
        r"<li>\[ \] (.*?)</li>",
        r'<li class="checklist"><input type="checkbox" disabled> \1</li>',
        html,
    )


def build_guide_html(guide_md: str) -> str:
    html = markdown.markdown(guide_md, extensions=["fenced_code", "tables", "sane_lists"])
    return fix_checklists(html)


CSS = (ROOT / "template_style.css").read_text(encoding="utf-8")

HERO_SYMBOLS = """
      <span style="top:12%; left:8%; font-size:44px;">∧</span>
      <span style="top:60%; left:4%; font-size:30px;">¬</span>
      <span style="top:22%; left:88%; font-size:38px;">→</span>
      <span style="top:70%; left:90%; font-size:26px;">∨</span>
      <span style="top:82%; left:20%; font-size:24px;">⊢</span>
      <span style="top:10%; left:48%; font-size:22px;">∴</span>
"""


def main():
    raw = README.read_text(encoding="utf-8")
    meta, body = strip_front_matter(raw)
    blocks = extract_details_blocks(body)

    if len(blocks) < 2:
        sys.exit("README.md에 <details> 블록이 2개(수업 자료 링크, 가이드) 필요합니다.")

    materials_summary, materials_md = blocks[0]
    guide_summary, guide_md = blocks[1]

    cards_html = build_material_cards(materials_md)
    guide_html = build_guide_html(guide_md)

    page_title = meta.get("title", SITE_TITLE)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans+KR:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>

  <header class="hero">
    <div class="hero-symbols">{HERO_SYMBOLS}</div>
    <div class="hero-inner">
      <div class="eyebrow">{EYEBROW}</div>
      <h1>{SITE_TITLE}</h1>
      <p class="lede">{SITE_LEDE}</p>
    </div>
  </header>

  <section class="section">
    <div class="section-label">수업 자료</div>
    <div class="cards">
{cards_html}
    </div>
  </section>

  <div class="divider">
    <span class="glyph">⊢</span>
    <span class="label">부록 · GITHUB 사용법</span>
  </div>

  <section class="guide-shell" style="padding-top: 24px;">
    <details class="guide">
      <summary>
        <span class="marker">▸</span>
        {guide_summary}
        <span class="sub">학생용 참고 자료</span>
      </summary>
      <div class="guide-body">
{guide_html}
      </div>
    </details>
  </section>

  <footer>
    2026_shinseong_AI_Class · <a href="{REPO_URL}" target="_blank" rel="noopener">저장소 바로가기</a>
  </footer>

</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"빌드 완료: {OUT} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
