
# 프로젝트 목표

- FastAPI기반 API 서버를 구축한다.
- 비동기 라이브러리와 함수를 적극적으로 사용한다.
- PostgreSQL을 사용한다.

# 구현 목표

- DockerFile 작성
  - FastAPI
  - PostgreSQL
  - Redis
  - MongoDB
  - RabbitMQ
  - Celery Worker
  - Celery Beat
- DockerCompose 작성
- 손쉬운 확장이 가능한 FastAPI, Celery 프로젝트 구조
- 손쉬운 테스트 적용이 가능한 FastAPI, Celery 프로젝트 구조

# 작업 진행 사항

- [ ] DockerFile 작성
  - [ ] FastAPI
  - [ ] PostgreSQL
  - [ ] Redis
  - [ ] MongoDB
  - [ ] RabbitMQ
  - [ ] Celery Worker
  - [ ] Celery Beat

# 작업 완료 사항

# Dev환경 세팅

- Docker 이미지 빌드
``` bash
docker build -t fastapi_toyproject_4_dev:latest . -f dockerfile.dev_env_arm
docker build -t fastapi_toyproject_4_dev:latest . -f dockerfile.dev_env_x86_64
```

- Docker 컨테이너 생성
``` bash
docker run -it --name fastapi_toyproject_4_dev_container -p 127.0.0.1:9000:8000 fastapi_toyproject_4_dev:latest
```

- Git Hooks 적용
```bash
pre-commit install
```