# SOP: 운영 서버(RHEL/Podman) 폐쇄망 배포 가이드

이 문서는 Fujitsu PRIMERGY RX2540 M8 (RHEL 9.6) 장비에서 Podman을 기반으로 lfnovo 시스템을 폐쇄망에 배포하는 절차를 설명합니다.

## 1. 개요
- **장비**: Fujitsu PRIMERGY RX2540 M8
- **OS**: RHEL 9.6 (x86_64)
- **런타임**: Podman (Docker-compatible 컨테이너 엔진)
- **환경**: 폐쇄망 (외부 인터넷 연결 불가)

## 2. 사전 준비 (인터넷 가능 환경 - 현재 PC)
폐쇄망 서버에는 인터넷이 안되므로 필요한 모든 이미지와 파일을 아카이브로 만들어야 합니다.

### 2.1 최초 전체 배포 (Full Deployment)
새 장비에 처음 배포할 때는 이미지와 모델을 모두 포함해야 합니다.
- **이미지 추출**: `execution/export_images.py` 실행.
- **압축**: `models/` 폴더와 추출된 이미지(`.tar`)를 모두 포함하여 압축.

### 2.2 증분 업데이트 (Incremental Update / Patch)
서비스 운영 중 **코드나 설정만 변경**되었을 때 사용하는 효율적인 방법입니다.
- **압축 대상**: `models/` 및 대용량 이미지를 **제외**한 소스 코드 폴더만 압축.
- **특이사항**: API 로직이 변경되어 이미지가 새로 빌드된 경우에만 해당 `.tar` 파일만 추가로 포함합니다.

## 3. 운영 서버로 이동 및 배포

### 3.1 압축 해제 및 이미지 로드
RHEL 터미널에서 아래 명령어를 실행합니다.
```bash
# 압축 해제 (기존 경로에 덮어쓰기 가능)
unzip lfnovo_production_package.zip -d /opt/lfnovo

# 신규/수정된 이미지 로드 (필요한 경우만)
podman load -i production_images/common-api.tar
```

### 3.2 권한 및 실행
```bash
# 권한 설정 (SELinux 대응)
chmod -R 777 /opt/lfnovo/lfnovo-rag-system/storage
chmod -R 777 /opt/lfnovo/lfnovo-rag-system/models
chcon -Rt svirt_sandbox_file_t /opt/lfnovo/lfnovo-rag-system/storage /opt/lfnovo/lfnovo-rag-system/models

# 시스템 실행/재시작
podman-compose -f lfnovo-rag-system/deploy/common/compose.yaml up -d
```

## 4. 확인 사항
- **SELinux**: 컨테이너가 파일을 읽지 못할 경우 `setenforce 0`으로 잠시 테스트하거나 컨테이너 볼륨 매핑 시 `:Z` 옵션을 추가하십시오.
- **네트워크**: `podman network ls`로 네트워크가 정상 생성되었는지 확인하십시오.
