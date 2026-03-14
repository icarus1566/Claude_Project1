# Linux 운영 서버 (RHEL 9.6 + Podman) 실행 절차

이 절차는 lfnovo 프로젝트의 Layer 1 (Directive)에 따라 작성되었습니다.

## 1. 사전 준비
RHEL 9.6에서 podman과 podman-compose가 설치되어 있어야 합니다.
GPU 패스스루를 위해 `nvidia-container-toolkit` 설정이 완료되어 있어야 합니다.

## 2. 오프라인 이미지 적재 (폐쇄망인 경우)
외부 통신이 가능한 PC에서 다음 명령으로 이미지를 추출합니다.
```bash
# 인터넷망 PC
podman pull docker.io/qdrant/qdrant:latest
podman save -o qdrant.tar qdrant/qdrant:latest
```
서버 반입 후 렌더링 :
```bash
# RHEL 9.6 서버
podman load -i qdrant.tar
```

## 3. 볼륨 권한 확인
SELinux가 활성화 된 경우 볼륨 마운트에 권한 문제가 발생할 수 있습니다. `storage/` 하위 폴더들에 대해 `:z` 마운트 플래그를 추가하거나 `chcon`을 적용하세요.

## 4. 실행
```bash
podman-compose -f deploy/common/compose.yaml up -d
```
