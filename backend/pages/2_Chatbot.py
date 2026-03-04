import streamlit as st
import json
import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import base64

load_dotenv()

st.set_page_config(layout="wide", page_title="Career Assistant")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

robot_b64 = img_to_base64(os.path.join(BASE_DIR, "robot.png"))

st.markdown("""
<style>
[data-testid="stTab"] [data-testid="stMarkdownContainer"] p { font-size: 20px !important; }
[data-testid="stTab"][aria-selected="true"] { color: #7500C0 !important; border-bottom-color: #C2A3FF !important; }
[data-testid="stTab"]:hover [data-testid="stMarkdownContainer"] p { color: #A100FF !important; }

.chat-user {
    background: #f3eeff;
    border-left: 4px solid #A100FF;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 15px;
}
.chat-assistant {
    background: #f9f9f9;
    border-left: 4px solid #ddd;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 15px;
}
.profile-card {
    background: #E6DCFF;
    color: black;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.profile-card h3 { margin: 0 0 4px 0; font-size: 20px; }
.profile-card p  { margin: 2px 0; font-size: 13px; opacity: 0.9; }
.suggestion-btn  { margin: 4px 2px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    dataset_path = os.path.join(DATA_DIR, "enterprise_opportunities_dataset.json")
    profile_path = os.path.join(DATA_DIR, "profile.json")

    with open(dataset_path, "r") as f:
        dataset = json.load(f)
    with open(profile_path, "r") as f:
        profile = json.load(f)

    return dataset, profile

dataset, profile_data = load_all_data()
profile = profile_data["profile"]

def build_system_prompt(dataset: dict, profile: dict) -> str:
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # Serialise data — keep it tight but complete
    dataset_str  = json.dumps(dataset,      indent=None, separators=(",", ":"))
    profile_str  = json.dumps(profile,      indent=None, separators=(",", ":"))

    return f"""You are a helpful, friendly Career & Learning Assistant for Accenture employees.
Today's date is {today}.

## YOUR ROLE
Help employees with:
1. Discovering upcoming events (networking, development) relevant to their interests
2. Recommending training courses that match their goals or capability transitions
3. Identifying colleagues to contact who have made similar career transitions
4. Explaining step-by-step career transition pathways
5. Drafting professional outreach messages to community leads or contacts
6. Answering questions about the employee's own profile, progress, and development goals

## EMPLOYEE PROFILE
The employee you are speaking with has this Workday profile:
{profile_str}

## ORGANISATIONAL DATA
You have access to the following enterprise dataset containing events, training courses, contacts, and career transition pathways:
{dataset_str}

## HOW TO RESPOND
- Be conversational, warm, and concise. Avoid walls of text.
- When listing events or training, show: title, date, format, and RSVP/link.
- When recommending contacts, include their name, role, transition story, and email.
- When asked to draft a message, write a ready-to-send, professional but friendly email or Teams message.
- Always cross-reference the employee's profile — personalise recommendations based on their current role, career pathway, skills, and development goals.
- If an event is not open_to_all, note it politely and suggest alternatives.
- Reference the employee by their preferred name ({profile["personal"]["preferred_name"]}).
- When referencing their career pathway, acknowledge what steps they have already completed and focus on what is next.
- Keep responses focused. If the user asks a broad question, ask a clarifying follow-up rather than dumping everything at once.
- Format responses with markdown (bold, bullet points, headers) for readability in Streamlit.

## CONSTRAINTS
- Only reference events, training, contacts, and pathways that exist in the dataset.
- Do not invent links, email addresses, or event details.
- If something is not in the data, say so honestly and suggest the closest alternative.
"""

with st.sidebar:
    emp = profile["personal"]
    job = profile["employment"]["current_role"]
    pathway = profile["career_development"]

    st.markdown(f"""
    <div class="profile-card" style="background-color: #C2A3FF !important;">
        <h3>👧🏾 {emp['preferred_name']} {profile['personal']['last_name']}</h3>
        <p>🏢 {job['title']}</p>
        <p>🏭 {job['industry_group']}</p>
        <p>⚙️ {job['capability']}</p>
        <p>📍 {emp['location']['city']} · {emp['location']['work_arrangement']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**🎯 Active Pathway**  \n{pathway['current_pathway_title']}")
    progress = pathway["pathway_progress"]
    st.progress(progress["percent_complete"] / 100,
                text=f"Step {progress['current_step']} of {progress['steps_total']}: {progress['current_step_title']}")

    st.markdown("---")
    st.markdown("**💡 Try asking:**")

    suggestions = [
        "What should I do next on my career pathway?",
        "Show me upcoming cyber events I can attend",
        "Who can I contact about moving into Cyber Security?",
        "Draft an email to Alex CyberLead introducing myself",
        "What training do you recommend for me right now?",
        "Am I on track with my development goals?",
    ]

    for s in suggestions:
        if st.button(s, key=f"sugg_{s}", use_container_width=True):
            st.session_state.pending_suggestion = s

    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
        <img src="data:image/png;base64,{robot_b64}" width="45" style="margin-bottom:8px;">
        <h2 style="margin: 0; font-size: 32px;">Personal Career & Learning Assistant</h2>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_suggestion" in st.session_state:
    suggestion = st.session_state.pop("pending_suggestion")
    st.session_state.messages.append({"role": "user", "content": suggestion})

for msg in st.session_state.messages:
    css_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
    icon      = "👧🏾" if msg["role"] == "user" else "🤖"
    st.markdown(
        f'<div class="{css_class}">{icon} {msg["content"]}</div>',
        unsafe_allow_html=True,
    )

user_input = st.chat_input("Ask about events, training, contacts or your career pathway...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(
        f'<div class="chat-user">👧🏾 {user_input}</div>',
        unsafe_allow_html=True,
    )

if (st.session_state.messages
        and st.session_state.messages[-1]["role"] == "user"):

    system_prompt = build_system_prompt(dataset, profile)
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                max_tokens=1024,
    
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
            )
            assistant_reply = response.choices[0].message.content

        except Exception as e:
            assistant_reply = f"⚠️ Sorry, I hit an error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.markdown(
        f'<div class="chat-assistant">"🤖" {assistant_reply}</div>',
        unsafe_allow_html=True,
    )
    st.rerun()