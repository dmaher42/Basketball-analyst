# Basketball Analyst (No-Code Starter)

A Streamlit web app to upload basketball game footage, mark events (shots/possessions), and export highlight clips plus a CSV — **no coding required**.

## Quick Deploy (Streamlit Community Cloud)
Follow these exact settings when configuring or updating the deployment to avoid clone failures:

| Setting | Value |
| --- | --- |
| **Repository** | `dmaher42/basketball-analyst` (case-sensitive; capital **B**) |
| **Branch** | `main` |
| **Main file path** | `app.py` |

1. Sign in at [streamlit.io](https://streamlit.io) and open the app's **⋯ → Manage app → Settings** panel (or **Deploy an app** for a fresh deployment).
2. Ensure the values match the table above. If the repository selector auto-lowercases, click **Change repository** and pick `dmaher42/Basketball-analyst` from the dropdown so the clone uses the capital **B**.
3. Save the settings and click **Reboot app**. The logs should now show a successful clone followed by the dependency install from `requirements.txt` and `packages.txt` (look for Streamlit to install `moviepy`, `imageio`, `imageio-ffmpeg`, and `opencv-python-headless`).
4. If the repo still will not appear, re-authorize Streamlit Cloud in GitHub (**Settings → Applications → Authorized OAuth Apps → Streamlit → Configure**) and grant access to `dmaher42/Basketball-analyst`, then repeat the steps above.

Once the UI loads, you can upload a 20–30 second MP4, mark events, export highlight clips, and download the CSV summary.

### Troubleshooting failed clones

If the Streamlit Community Cloud logs still report:

```
Failed to download the sources for repository: 'basketball-analyst', branch: 'main'
```

double-check that the deployment is pointed at `dmaher42/Basketball-analyst` **with the capital “B”** and the branch is set to `main`. GitHub treats repository names case-insensitively in the browser, but Streamlit needs the exact casing when it clones. Selecting the repository from the dropdown (instead of typing it manually) resolves the issue.

## Local Run (optional)
1. Install Python 3.11 or newer.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Tips
- Keep individual highlight clips ~4–10 seconds for faster exports.
- If uploads fail, try a smaller resolution video (e.g., 720p) or split halves.
