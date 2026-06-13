# OpenSourceGroup10

## 실행 준비

가상환경을 활성화합니다.

```bash
cd ~/OpenSourceGroup10
source .venv/bin/activate
```

MySQL 기본 DB를 적용합니다.

```bash
mysql -u school_app -p4321 school_event_db < school_event_db.sql
```

## RAG 문서 기반 건물 행사 DB 동기화

RAG 벡터DB에 저장된 공지 문서에서 건물명, 날짜, 시간, 제목을 추출해 MySQL `events` 테이블에 저장합니다.

먼저 저장 없이 확인하려면:

```bash
python scripts/sync_rag_events_to_db.py --dry-run --require-time --from-date 2026-06-14 --to-date 2026-12-31
```

실제로 DB에 저장하려면:

```bash
python scripts/sync_rag_events_to_db.py --require-time --from-date 2026-01-01 --to-date 2026-12-31
```

이 스크립트는 `index.html`의 지도 건물 목록을 기준으로 `buildings` 테이블을 보강하고, 건물과 시간이 명확한 행사만 `events`에 추가합니다.

주의: 이 기능은 `vector_store/chroma` 벡터DB가 있거나, 직접 크롤링/임베딩을 먼저 실행한 상태에서 동작합니다.

## 서버 실행

```bash
./scripts/start_all.sh
```

Windows Ollama를 WSL에서 포트 프록시로 연결해 사용하는 경우:

```bash
WINDOWS_HOST=$(ip route | awk '/^default/ {print $3; exit}')
OLLAMA_BASE_URL=http://$WINDOWS_HOST:11435 ./scripts/start_all.sh
```
