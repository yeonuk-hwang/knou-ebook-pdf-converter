# KNOU-eBook-PDF-converter

eBook Viewer를 OCR이 적용된 검색 가능한 PDF로 변환하는 프로그램입니다.

## 주요 기능

- 이북 페이지 자동 캡처
- OCR을 통한 텍스트 추출
- 검색 가능한 PDF 생성

## ⚠️ 법적 고지사항

**본 도구는 개인적인 학습 목적으로만 사용해야 합니다.**

- 저작권법에 따라 캡처한 콘텐츠를 무단 배포하거나 상업적으로 사용할 수 없습니다.
- 개인 학습 목적 외의 사용은 법적 제재를 받을 수 있습니다.
- 캡처한 콘텐츠의 사용으로 인한 모든 법적 책임은 사용자에게 있습니다.

## 설치 방법

### 1. 필수 요구사항

- [uv](https://docs.astral.sh/uv/): Python package manager

### 2. uv 설치

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

자세한 설치 방법은 [uv 공식 문서](https://docs.astral.sh/uv/getting-started/installation/)를 참고하세요.

### 3. 프로젝트 설정

```bash
# 저장소 클론
git clone https://github.com/yeonuk-hwang/knou-ebook-pdf-converter.git
cd knou-ebook-pdf-converter

# 가상환경 생성 및 의존성 설치
uv sync --frozen

# Playwright 브라우저 설치
uv run playwright install
```

## 실행 방법

```bash
uv run main.py
```

## 사용 방법

### 기본 사용법

1. 프로그램 실행 후 자동으로 열리는 브라우저에서 KNOU 이북 사이트에 로그인합니다.
2. 원하는 교재를 선택하고 반드시 **구 PDF 뷰어**로 엽니다.
3. 메인 메뉴에서 원하는 작업을 선택합니다:
   - 1: 이북 페이지 캡처 - 현재 열린 교재의 페이지들을 자동으로 캡처
   - 2: 캡처된 이미지로 PDF 생성 - OCR 처리 후 검색 가능한 PDF 생성
   - 3: 종료

### 작업 순서

1. 먼저 옵션 1로 모든 페이지를 캡처합니다.
2. 캡쳐된 페이지들을 교재는 `images/textbook` 워크북은 `images/workbook` 폴더에 분류해주세요
3. 분류가 완료되면 옵션 2로 PDF를 생성합니다.
4. 생성된 PDF는 `output` 폴더에서 확인할 수 있습니다.

## 주의사항

### 사용 전 확인사항

- 반드시 구 PDF 뷰어로 이북을 열어야 합니다 (신규 뷰어 미지원)

### 파일 관리

- 캡처된 이미지는 자동으로 `images` 폴더에 저장됩니다.
- 최종 PDF는 `output` 폴더에 생성됩니다

### OCR 관련

- 상업용 OCR 도구에 비해 인식률이 다소 낮을 수 있습니다
- 중요한 내용은 반드시 원본과 대조 확인하세요

## 문제 해결

- 브라우저 실행 오류 시: `playwright install` 명령어로 브라우저를 재설치해보세요

## 기여하기

- 버그 리포트나 기능 제안은 Issue를 통해 제출해주세요

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
