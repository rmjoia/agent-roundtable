# Suggested gates

Paste into `team.config.yaml` and adjust paths (here `backend/` and `frontend/`):

```yaml
gates:
  pre_commit:
    - { name: "backend: build",  paths: "^backend/",  cwd: backend,  run: "dotnet build --nologo -warnaserror" }
    - { name: "backend: test",   paths: "^backend/",  cwd: backend,  run: "dotnet test --nologo --filter \"Category!=Integration\"" }
    - { name: "frontend: lint",  paths: "^frontend/", cwd: frontend, run: "CI=1 npx ng lint" }
    - { name: "frontend: build", paths: "^frontend/", cwd: frontend, run: "CI=1 npx ng build" }
    - { name: "frontend: test",  paths: "^frontend/", cwd: frontend, run: "CI=1 npx ng test --watch=false" }
```

A test step that runs zero tests should fail; add a count check if your runner exits 0 on an empty run.
