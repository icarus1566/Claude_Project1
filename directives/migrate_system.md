# SOP: lfnovo 시스템 이전 및 신규 설치 가이드

이 문서는 기존 컴퓨터에서 구동 중인 lfnovo RAG 시스템을 아무것도 설치되지 않은 신규 노트북으로 이전하는 절차를 설명합니다.

## 1. 신규 노트북 준비 (사전 설치)
새 노트북에서 다음 프로그램을 순서대로 설치해야 합니다.

1. **Docker Desktop 설치**: [docker.com](https://www.docker.com/products/docker-desktop/)에서 다운로드 및 설치.
2. **Python 설치**: [python.org](https://www.python.org/)에서 3.10 이상 버전 설치 (설치 시 'Add Python to PATH' 옵션 필수 선택).
3. **Git 설치**: [git-scm.com](https://git-scm.com/)에서 설치 (코드 관리용).

## 2. 파일 복사 (최초 설치 vs 증분 업데이트)

### 방법 A: 최초 전체 설치 (Full Setup)
모델이 없는 신규 환경에 처음 설치할 때 사용하는 방법입니다.
1. **복사할 폴더**: `d:\ALL_AI\Claude_Project1` 전체 폴더.
2. **필수 포함**: `lfnovo-rag-system\models` (수 GB 용량의 모델 파일이 포함되어야 다시 받지 않습니다).

### 방법 B: 증분 업데이트 (Incremental Update / Patch)
이미 노트북에 시스템이 설치되어 있고, **코드나 설정만 변경된 경우** 효율적인 방법입니다.
1. **복사 대상 (최소화)**: 대용량 폴더를 제외한 나머지 폴더만 압축하여 옮깁니다.
   - `directives/`
   - `execution/`
   - `lfnovo-rag-system/` (단, 하위의 `models/`, `storage/` 폴더는 제외 가능)
2. **이점**: 수십 MB 수준으로 용량이 줄어들어 전송과 업데이트가 매우 빠릅니다.

## 3. 환경 복구 및 실행
파일 복사가 완료된 후 새 노트북에서 다음 과정을 수행합니다.

1. **Docker Desktop 실행**: 엔진이 완전히 켜질 때까지 기다립니다.
2. **시스템 가동**:
   `execution\docker_manage.py` 스크립트를 사용하여 서비스를 시작합니다.
   ```powershell
   python [복사한경로]\execution\docker_manage.py --restart
   ```

## 4. 확인 및 검증
브라우저를 열어 다음 주소에 접속되는지 확인합니다.
- Open WebUI: `http://localhost:3000`
- API Health: `http://localhost:8000/api/v1/health`

---
> [!TIP]
> 모델 파일(`bge-m3`)은 한 번만 제대로 옮겨두면, 이후에는 코드만 가볍게 업데이트하며 사용할 수 있습니다.
