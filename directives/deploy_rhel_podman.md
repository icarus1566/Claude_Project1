# SOP: 운영 서버(RHEL/Podman) 폐쇄망 배포 가이드

이 문서는 Fujitsu PRIMERGY RX2540 M8 (RHEL 9.6) 장비에서 Podman을 기반으로 lfnovo 시스템을 폐쇄망에 배포하는 절차를 설명합니다.

## 1. 개요
- **장비**: Fujitsu PRIMERGY RX2540 M8
- **OS**: RHEL 9.6 (x86_64)
- **런타임**: Podman (Docker-compatible 컨테이너 엔진)
- **환경**: 폐쇄망 (외부 인터넷 연결 불가)

## 2. 사전 준비 (인터넷 가능 환경 - 현재 PC)
폐쇄망 서버에는 인터넷이 안되므로 필요한 모든 이미지와 파일을 아카이브로 만들어야 합니다.

### 2.1 도커 이미지 추출 (Save)
배포에 필요한 이미지를 `.tar` 파일로 내보냅니다.
```powershell
# API 이미지 (빌드 후 추출)
docker save rag-api -o rag-api.tar

# 외부 이미지들 추출
docker save ollama/ollama:latest -o ollama.tar
docker save ghcr.io/open-webui/open-webui:main -o open-webui.tar
docker save qdrant/qdrant:latest -o qdrant.tar
docker save minio/minio:latest -o minio.tar
docker save postgres:15-alpine -o postgresql.tar
```

### 2.2 전체 파일 압축 (Archive)
프로젝트 소스, 모델, 내보낸 이미지 파일을 하나로 묶습니다.
- **압축 대상**: `d:\ALL_AI\Claude_Project1` (소스, 모델 가중치, 위에서 저장한 .tar 이미지들 포함)
- **압축 방법 (PowerShell)**:
  ```powershell
  Compress-Archive -Path d:\ALL_AI\Claude_Project1\* -DestinationPath lfnovo_production_bundle.zip
  ```

## 3. 운영 서버로 이동 (Transfer)
USB 메모리 또는 승인된 파일 전송망을 통해 `lfnovo_production_bundle.zip` 파일을 운영 서버의 작업 디렉터리로 복사합니다.

## 4. 운영 서버 배포 (RHEL / Podman)

### 4.1 압축 해제
RHEL 터미널에서 아래 명령어를 실행합니다.
```bash
# 작업 디렉터리 생성 및 이동
mkdir -p /opt/lfnovo
mv lfnovo_production_bundle.zip /opt/lfnovo/
cd /opt/lfnovo

# 압축 해제
unzip lfnovo_production_bundle.zip
```

### 4.2 Podman 이미지 로드 (Import)
저장해온 `.tar` 이미지들을 Podman으로 불러옵니다.
```bash
podman load -i rag-api.tar
podman load -i ollama.tar
podman load -i open-webui.tar
podman load -i qdrant.tar
podman load -i minio.tar
podman load -i postgresql.tar
```

### 4.3 권한 설정 (SELinux / Volume)
RHEL에서는 SELinux 보안 정책상 볼륨 권한 문제가 발생할 수 있습니다.
```bash
# 볼륨 경로에 대한 권한 부여 (:Z 옵션 사용 준비 또는 소유권 변경)
chmod -R 777 /opt/lfnovo/lfnovo-rag-system/storage
chmod -R 777 /opt/lfnovo/lfnovo-rag-system/models
```

### 4.4 시스템 실행
Podman-compose가 설치되어 있다면 동일하게 실행 가능하며, 없을 경우 `podman` 명령어로 실행합니다.
```bash
# podman-compose 사용 시
podman-compose -f lfnovo-rag-system/deploy/common/compose.yaml up -d
```

## 5. 확인 사항
- **SELinux**: 컨테이너가 파일을 읽지 못할 경우 `setenforce 0`으로 잠시 테스트하거나 컨테이너 볼륨 매핑 시 `:Z` 옵션을 추가하십시오.
- **네트워크**: `podman network ls`로 네트워크가 정상 생성되었는지 확인하십시오.
