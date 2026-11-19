# 아이폰 반 GitHub 미러 동기화 도구

대상 4개 반 (아티팩트 slug → 저장소)
- e6a 초6 A반 (짧은이름 초6A): 101079e9-829e-447c-9fd4-f312c03f560b → sydcho123-arch/eoeun-e6a
- m1a 중1 A반 (중1A): 2045cdbb-c5c5-4a9d-8601-1fa0cf55bba2 → sydcho123-arch/eoeun-m1a
- m1c 중1 C반 (중1C): ec269d2d-a4eb-4af4-84ac-ba854f4db771 → sydcho123-arch/eoeun-m1c
- m2 중2반 (중2): bdcd36c5-5af0-4c39-8d7f-51e86acee998 → sydcho123-arch/eoeun-m2

순서 (반마다)
1. add_repo(owner=sydcho123-arch, repo=eoeun-<code>, access=push) 후 git clone --depth 1
2. read_file(slug, paths=["index.html"]) 로 라이브 HTML 받기 (저장된 파일 경로 사용)
3. `python3 sync.py need <code> "<반 이름>" "<짧은이름>" <html> <repo>` → 빠진 blob id 목록
4. 빠진 id마다 read_asset(slug, id, max_bytes=4194304) → 저장된 파일을 `<repo>/a/<id>.<확장자>` 로 복사 (png/jpg/mp4/pdf/mp3 등 content_type 기준)
5. `python3 sync.py build ...` → "ok N assets"
6. git add -A, commit, `git -c push.negotiate=true push origin main`
