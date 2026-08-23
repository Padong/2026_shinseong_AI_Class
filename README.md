# 2026_shinseong_AI class

<details>
<summary>2026 인공지능 기초 수업자료 링크</summary>

- [1단원 자료](https://canva.link/ohxx81dg1sthqt5)
- <a href="https://raw.githubusercontent.com/padong/2026_shinseong_AI_Class/main/logic-liar-game.html" download>logic-liar-game.html 다운로드</a>

</details>

---

<details>
<summary>GitHub README.md 작성법 가이드</summary>

> 이 문서는 GitHub 저장소(repository)의 README.md 파일을 어떻게 작성하는지 안내하는 가이드입니다.

---

## 1. README.md란?

README.md는 GitHub 저장소에 접속했을 때 **가장 먼저 보이는 문서**입니다.
프로젝트를 방문한 사람에게 "이 프로젝트가 무엇인지, 어떻게 사용하는지"를 설명하는 **얼굴이자 설명서** 역할을 합니다.

- 파일 이름은 반드시 `README.md` (대문자 권장)
- `.md`는 **마크다운(Markdown)** 문법으로 작성된 파일이라는 뜻
- 저장소 루트(최상위) 폴더에 위치해야 GitHub이 자동으로 화면에 보여줌

---

## 2. 왜 잘 써야 할까?

| 좋은 README | 부실한 README |
|---|---|
| 프로젝트 이해가 빠름 | 무엇을 하는 프로젝트인지 모름 |
| 설치·실행이 쉬움 | 실행 방법을 못 찾아 포기 |
| 협업자가 기여하기 쉬움 | 기여 방법을 몰라 참여 못 함 |
| 포트폴리오로서 신뢰감을 줌 | 완성도가 낮아 보임 |

---

## 3. 마크다운(Markdown) 기초 문법

README는 마크다운 문법으로 작성합니다. 핵심 문법만 익히면 충분합니다.

<details>
<summary>마크다운 기초 문법 보기 (클릭)</summary>

````markdown
# 제목
**굵게**  *기울임*  ~~취소선~~

- 목록
1. 순서 목록

`코드`
```python
print("코드 블록")
```

[링크](https://example.com)
![이미지](이미지주소.png)
> 인용문
````

</details>

---

## 4. 기본 구조 (권장 순서)

````markdown
# 프로젝트 이름

한 줄 소개 (이 프로젝트가 무엇을 하는지)

## 소개 (Introduction)
프로젝트의 목적, 배경, 주요 기능을 설명

## 데모 / 스크린샷
실행 화면이나 예시 이미지 (선택)

## 설치 방법 (Installation)
```bash
git clone https://github.com/사용자명/저장소명.git
cd 저장소명
pip install -r requirements.txt
```

## 사용 방법 (Usage)
```bash
python main.py
```

## 기술 스택 (Tech Stack)
- Python 3.11
- Flask
- SQLite

## 폴더 구조
```
project/
├── src/
├── tests/
└── README.md
```

## 기여 방법 (Contributing)
1. 이 저장소를 Fork 합니다
2. 새 브랜치를 만듭니다 (`feature/기능명`)
3. 변경 사항을 커밋합니다
4. Pull Request를 보냅니다

## 라이선스 (License)
MIT License

## 작성자 (Author)
- 이름 / 이메일 / GitHub 프로필 링크
````

---

## 5. 항목별 작성 팁

### ① 프로젝트 제목 & 한 줄 소개
- 제목은 `#`으로 시작, 프로젝트 핵심을 한눈에 알 수 있게
- 바로 아래 한두 문장으로 "무엇을, 왜" 만들었는지 요약

### ② 설치 방법
- 복사해서 바로 실행할 수 있는 **명령어 그대로** 작성
- 운영체제별로 다르면 구분해서 표기

### ③ 사용 방법
- 실제 실행 예시, 입출력 예시를 코드 블록으로 제시
- 캡처 화면(스크린샷)을 넣으면 이해도가 크게 올라감

### ④ 뱃지(Badge) 활용 (선택, 심화)
프로젝트 상태를 한눈에 보여주는 이미지 뱃지를 넣을 수 있습니다.

```markdown
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```
→ https://shields.io 에서 다양한 뱃지를 만들 수 있음

### ⑤ 폴더 구조
- 프로젝트가 여러 파일/폴더로 구성되어 있다면 트리 구조로 표시
- 코드 블록 안에 작성하면 정렬이 깔끔함

---

## 6. 토글(접기/펼치기) 기능 넣기

GitHub 마크다운은 `<details>`와 `<summary>` HTML 태그를 지원해서, 클릭하면 펼쳐지는 **토글 버튼**을 만들 수 있습니다.
설치 방법이 여러 개거나, 긴 로그·스크린샷·FAQ처럼 평소엔 숨겨두고 싶은 내용에 유용합니다.

### 기본 문법

````markdown
<details>
<summary>클릭하면 펼쳐집니다</summary>

여기에 숨겨질 내용을 작성합니다.
마크다운 문법도 그대로 사용할 수 있습니다.

```bash
pip install -r requirements.txt
```

</details>
````

- `<summary>` 태그 안의 텍스트가 접혀있을 때 보이는 제목입니다
- `</summary>` 다음 줄은 **반드시 한 줄 띄워야** 안의 마크다운(코드블록, 목록 등)이 정상적으로 렌더링됩니다
- 기본값은 "접힌 상태"이며, `<details open>`처럼 `open` 속성을 추가하면 처음부터 펼쳐진 상태로 보여줄 수 있습니다

### 활용 예시 — 운영체제별 설치 방법

````markdown
## 설치 방법

<details>
<summary>Windows</summary>

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

</details>

<details>
<summary>macOS / Linux</summary>

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

</details>
````

### 활용 예시 — 스크린샷 여러 장 숨기기

```markdown
<details>
<summary>📸 실행 화면 더 보기</summary>

![화면1](screenshot1.png)
![화면2](screenshot2.png)

</details>
```

> 참고: 이 토글 기능은 GitHub, GitLab 등 대부분의 마크다운 렌더러에서 동작하지만, 표준 마크다운 문법이 아니라 **HTML 태그를 그대로 사용하는 방식**입니다. 즉 순수 텍스트 편집기(예: 메모장)로 열어보면 태그가 그대로 보입니다.

---

## 7. 좋은 예시 vs 나쁜 예시

**나쁜 예시**
```markdown
# 내 프로젝트

이건 제가 만든 프로젝트입니다.
```

**좋은 예시**
````markdown
# 할일 관리 앱 (Todo App)

React와 Firebase로 만든 간단한 할일 관리 웹 앱입니다.

## 주요 기능
- 할일 추가/삭제/완료 체크
- 실시간 데이터 동기화

## 설치 방법
```bash
git clone https://github.com/username/todo-app.git
npm install
npm start
```
````

---

## 8. 작성 전 체크리스트

- [ ] 프로젝트 이름과 한 줄 소개가 있는가?
- [ ] 무엇을, 왜 만들었는지 설명했는가?
- [ ] 설치 방법을 그대로 따라할 수 있는가?
- [ ] 실행/사용 예시가 있는가?
- [ ] 사용한 기술(언어, 라이브러리)을 명시했는가?
- [ ] 스크린샷이나 데모가 있으면 더 좋음
- [ ] 오탈자, 깨진 링크가 없는가?
- [ ] 마크다운 문법(제목, 코드블록 등)이 올바르게 적용되었는가?

---

## 9. 참고하면 좋은 자료

- GitHub 공식 마크다운 가이드: https://docs.github.com/ko/get-started/writing-on-github
- Shields.io (뱃지 생성): https://shields.io
- Awesome README (좋은 README 모음): https://github.com/matiassingers/awesome-readme

> 위 링크들은 실제 존재하는 공개 자료이지만, 학생들에게 배포하기 전 최신 상태인지 직접 한 번 확인해 보시길 권장합니다.

</details>
