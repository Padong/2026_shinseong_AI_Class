#!/usr/bin/env python3
"""
README.md -> index.html 빌드 스크립트
- README.md 맨 위 <details> 블록(수업 자료 링크)을 카드로 변환
- 두 번째 <details> 블록(README 작성법 가이드)을 접이식 섹션으로 변환
- 나머지(hero, CSS, footer)는 고정 템플릿 유지
"""
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("markdown 패키지가 필요합니다: pip install markdown")

ROOT = Path(__file__).parent
README = ROOT / "README.md"
OUT = ROOT / "index.html"

SITE_TITLE = "신성여고 정보과학 수업 자료실"
SITE_LEDE = "수업에서 쓰는 자료와 실습 파일을 여기서 받아가세요."
EYEBROW = "2026 · 정보과학 · 인공지능 기초"
REPO_URL = "https://github.com/Padong/2026_shinseong_AI_Class"


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
    """<details><summary>..</summary>..</details> 블록들을 순서대로 추출"""
    pattern = re.compile(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", re.DOTALL)
    return [(m.group(1).strip(), m.group(2).strip()) for m in pattern.finditer(text)]


def build_material_cards(materials_md: str) -> str:
    """마크다운 리스트(- [텍스트](url) 또는 - <a href="url" download>텍스트</a>)를 카드로 변환"""
    html = markdown.markdown(materials_md, extensions=["fenced_code"])
    items = re.findall(r"<li>(.*?)</li>", html, re.DOTALL)
    cards = []
    labels = ["P₁", "P₂", "P₃", "P₄", "P₅", "P₆"]
    for i, item in enumerate(items):
        a_match = re.search(r'<a\s+href="([^"]+)"([^>]*)>(.*?)</a>', item, re.DOTALL)
        if not a_match:
            continue
        href, attrs, text = a_match.group(1), a_match.group(2), a_match.group(3).strip()
        is_download = "download" in attrs
        label = labels[i] if i < len(labels) else f"P{i+1}"
        if is_download:
            btn = (f'<a class="btn btn-signal" href="{href}" download>다운로드 ↓</a>\n'
                   f'          <a class="card-link" href="{href}" target="_blank" rel="noopener">웹에서 바로 열기 →</a>')
        else:
            btn = f'<a class="btn btn-primary" href="{href}" target="_blank" rel="noopener">자료 열기 ↗</a>'
        cards.append(f'''      <div class="card">
        <div class="tag">{label} · 자료</div>
        <h3>{text}</h3>
        {btn}
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
