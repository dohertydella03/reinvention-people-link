import streamlit as st
import json
import os
import base64
from pathlib import Path

page_bg_img = """
<style>
[data-testid="stTab"] [data-testid="stMarkdownContainer"] p {
    font-size: 20px !important;
}

/* Active tab */
[data-testid="stTab"][aria-selected="true"] {
    color: #7500C0 !important;
    border-bottom-color: #C2A3FF !important;
}
</style>
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
logo_path = os.path.join(BASE_DIR, "logo.png")

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE_DIR_1 = Path(__file__).parent
logo_b64 = img_to_base64(BASE_DIR_1 / "logo.png")

st.set_page_config(layout="wide", page_title="Events Dashboard")

st.markdown(page_bg_img, unsafe_allow_html=True)

def load_data(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        data = json.load(f)
        key = filename.replace(".json", "")
        return data.get(key, data)

events = load_data("events.json")
training = load_data("training.json")
metadata = load_data("metadata.json")

def matches_search(item, fields):
    if not search_query:
        return True

    search_lower = search_query.lower()

    for field in fields:
        value = item.get(field)

        if isinstance(value, list):
            if any(search_lower in str(v).lower() for v in value):
                return True

        elif value and search_lower in str(value).lower():
            return True

    return False

st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
        <img src="data:image/png;base64,{logo_b64}" width="60">
        <h1 style="margin: 0; font-size: 32px;">Enterprise Opportunities & Learning Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("🔎 Filters")

search_query = st.sidebar.text_input("Keyword Search")

industry_filter = st.sidebar.multiselect(
    "Industry",
    metadata["industries_reference"]
)

capability_filter = st.sidebar.multiselect(
    "Capability",
    metadata["capabilities_reference"]
)

tab1, tab2 = st.tabs(["📅 Events", "🎓 Training"])

with tab1:

    def event_matches(event):
        if industry_filter:
            if event.get("industry") not in industry_filter:
                return False

        if capability_filter:
            if not any(cap in capability_filter for cap in (event.get("capability") or [])):
                return False
        
        if not matches_search(event, ["title", "description", "tags", "capability"]):
            return False

        return True

    filtered_events = [e for e in events if event_matches(e)]
    st.write(f"Available Events: {len(filtered_events)}")

    for event in filtered_events:
        with st.container():
            st.markdown("---")
            st.subheader(event["title"])

            if event.get("open_to_all"):
                st.success("🌍 Open to All")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"📅 {event['date_utc']}")
                st.write(f"⏰ {event['time_utc']}")

            with col2:
                st.write(f"📍 {event['location']}")

            st.markdown(f"[👉 Find Out More Here]({event['rsvp_link']})")
            st.caption("Tags: " + ", ".join(event.get("tags", [])))

with tab2:

    level_filter = st.multiselect(
        "Level",
        sorted({t["level"] for t in training})
    )

    def training_matches(course):
        if industry_filter:
            if course.get("industry") not in industry_filter:
                return False

        if capability_filter:
            if course.get("capability") not in capability_filter:
                return False

        if level_filter:
            if course.get("level") not in level_filter:
                return False
        
        if not matches_search(course, ["title", "tags", "capability", "industry"]):
            return False

        return True

    filtered_training = [t for t in training if training_matches(t)]
    st.write(f"Available Training Courses: {len(filtered_training)}")

    for course in filtered_training:
        with st.container():
            st.markdown("---")
            st.subheader(course["title"])

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"🏭 {course['industry'] or 'All Industries'}")
                st.write(f"🧠 {course['capability']}")
                st.write(f"📈 {course['level'].capitalize()}")

            with col2:
                st.write(f"🎥 {course['delivery'].replace('_',' ').title()}")
                st.write(f"⏱ {course['duration']}")

            st.markdown(f"[🚀 Launch Training]({course['link']})")
            st.caption("Tags: " + ", ".join(course.get("tags", [])))