import streamlit as st
import subprocess
import json
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="The Hindu News Summarizer", page_icon="🗞️", layout="wide")

st.title("🗞️ The Hindu News Summarizer")

OUTPUT_FILE = Path("src/response.json")

def fetch_news_subprocess():
    """Run the scraper pipeline as a subprocess."""
    result = subprocess.run(
        ["uv", "run", "python", "src/pipeline.py"],
        capture_output=True, text=True
    )
    print(f"Return code : {result.returncode}")
    if result.returncode == 0:
        try:
            if OUTPUT_FILE.exists():
                with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data
            else:
                st.error("No output file found.")
                return None
        except json.JSONDecodeError:
            st.error("Failed to parse JSON output from pipeline.")
            return []
    else:
        st.error(result.stderr)
        return []

# --- UI ---
if st.button("🔄 Fetch Latest News"):
    with st.spinner("Fetching latest news from The Hindu..."):
        news_data = fetch_news_subprocess()
        if news_data:
            st.caption(f"News fetched at : {news_data['fetched_at']}")
            for article in news_data["results"]:
                st.subheader(article['title'])
                st.write(article['summary'])
                st.markdown(f"[Read full article]({article['url']})")
        else:
            st.warning("No news articles found.")
