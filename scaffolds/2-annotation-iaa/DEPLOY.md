# Deploying the dashboard

## Hugging Face Spaces (recommended for free hosting)

1. Create a new Space at https://huggingface.co/new-space
2. Pick the **Streamlit** SDK and "CPU basic — free"
3. Clone the empty Space repo
4. Copy this scaffold into it
5. Make sure `app.py` is at the repo root (Spaces looks for it there)
6. `git push` — the Space rebuilds on every push

## Streamlit Community Cloud

1. Push this scaffold to a public GitHub repo
2. Go to https://share.streamlit.io
3. Connect the repo; point at `app.py`
4. Deploys in ~2 minutes; URL ends in `.streamlit.app`

## Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then drag and drop `data/sample/annotator_a.jsonl` and `annotator_b.jsonl`.
