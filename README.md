# fastapi-wrapper

To initialize the wrapper, you need to provide the following parameters:

```bash
uv venv --python 3.11 
source .venv/bin/activate
uv pip install -r pyproject.toml 

# Optional: 
uv lock
```

To run the app
```bash
uvicorn app.main:app --reload
```
