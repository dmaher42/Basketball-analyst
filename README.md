# Basketball Analyst (No-Code Starter)

A Streamlit web app to upload basketball game footage, mark events (shots/possessions), and export highlight clips plus a CSV — **no coding required**.

## Quick Deploy (Streamlit Community Cloud)
Follow these exact settings when configuring or updating the deployment to avoid clone failures:

| Setting | Value |
| --- | --- |
| **Repository** | `dmaher42/Basketball-analyst` (case-sensitive) |
| **Branch** | `main` |
| **Main file path** | `app.py` |

1. Sign in at [streamlit.io](https://streamlit.io) and open the app's **⋯ → Manage app → Settings** panel (or **Deploy an app** for a fresh deployment).
2. Ensure the values match the table above. If the repository selector auto-lowercases, click **Change repository** and pick `dmaher42/Basketball-analyst` from the dropdown.
3. Save the settings and click **Reboot app**. The logs should now show a successful clone followed by the dependency install from `requirements.txt` and `packages.txt`.

Once the UI loads, you can upload a 20–30 second MP4, mark events, export highlight clips, and download the CSV summary.

## Local Run (optional)
1. Install Python 3.11 or newer.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Tips
- Keep individual highlight clips ~4–10 seconds for faster exports.
- If uploads fail, try a smaller resolution video (e.g., 720p) or split halves.
