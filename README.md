# fastapi-wrapper

<p align="left">
  <a href="https://fishwongy.github.io/post/20250203_fastapi_f1" target="_blank"><img src="https://img.shields.io/badge/Blog-Read%20About%20This%20Project-blue.svg" /></a>
  <!--<a href="https://twitter.com/intent/follow?screen_name=fishwongxd" target="_blank"><img src="https://img.shields.io/twitter/follow/fishwongxd?style=social" /></a>-->
</p>

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
