import streamlit as st

st.set_page_config(
    page_title="Path Finder - Accenture Internal Networking Hub",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with st.sidebar:
    st.markdown("""
    <div style="
        padding: 24px 16px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 16px;
    ">
      <div style="
          font-family: 'Syne', sans-serif;
          font-size: 1.3rem;
          font-weight: 800;
          color: #000000;
          letter-spacing: -0.02em;
          display: flex;
          align-items: center;
          gap: 10px;
      ">
        <span style="
            width: 10px; height: 10px; border-radius: 50%;
            background: #a100ff;
            box-shadow: 0 0 12px #a100ff;
            display: inline-block;
        "></span>
        PathFinder
      </div>
      <div style="
          font-family: 'DM Sans', sans-serif;
          font-size: 0.72rem;
          color: #c2a3ff;
          margin-top: 4px;
          letter-spacing: 0.06em;
          text-transform: uppercase;
      ">
        Accenture Internal Platform
      </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>

<style>
  .block-container { padding: 0 !important; max-width: 100% !important; }

  .nx-hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 100px 40px 80px;
    background: linear-gradient(135deg, #e8e0f5 0%, #f0e8f8 25%, #e0eef8 50%, #f5f0ff 75%, #ede8f5 100%);
  }
  .nx-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.6); border: 1px solid rgba(161,0,255,0.25);
    color: #555; padding: 7px 20px; border-radius: 100px;
    font-family: 'DM Sans', sans-serif; font-size: 0.75rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 36px;
  }
  .nx-hero-title {
    display: inline-flex; align-items: center; gap: 8px;
    font-family: 'Syne', sans-serif;
    font-size: clamp(3.5rem, 9vw, 7rem);
    font-weight: 800; line-height: 1.0; letter-spacing: -0.03em;
    color: #0a0a0f; margin-bottom: 28px;
  }
  .t-grad {
    background: linear-gradient(135deg, #00d4ff, #a100ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }
  .t-accent { color: #a100ff; }
  .nx-hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(1rem, 1.6vw, 1.15rem); font-weight: 300; color: #444;
    max-width: 560px; margin: 0 auto 48px; line-height: 1.75;
  }
  .nx-hero-actions {
    display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 72px;
  }
  .nx-hero-stats {
    display: flex; gap: 64px; justify-content: center; flex-wrap: wrap;
    padding-top: 48px; border-top: 1px solid rgba(0,0,0,0.1);
  }
  .nx-stat { text-align: center; }
  .nx-stat-num {
    font-family: 'Syne', sans-serif; font-size: 3.5rem; font-weight: 200;
    display: block; letter-spacing: -0.03em; color: #A100FF;
  }
  .nx-stat-label {
    font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: #6b6b7a; margin-top: 4px;
  }
</style>

<section class="nx-hero">
  <div class="nx-eyebrow">● Path Finder - Accenture Internal Platform</div>
  <h1 class="nx-hero-title">
    Your career.<br>
    Your <span class="t-grad">connections</span>.<br>
    All in one <span class="t-accent">place</span>.
  </h1>
  <p class="nx-hero-sub">
    Path Finder is Accenture's internal networking hub - making events, contacts
    and career opportunities visible and accessible across every department.
  </p>
  <div class="nx-hero-stats">
    <div class="nx-stat"><span class="nx-stat-num">2</span><div class="nx-stat-label">Core tools in one platform</div></div>
    <div class="nx-stat"><span class="nx-stat-num">&infin;</span><div class="nx-stat-label">Cross-department connections</div></div>
    <div class="nx-stat"><span class="nx-stat-num">0</span><div class="nx-stat-label">Missed opportunities</div></div>
  </div>
</section>
""", unsafe_allow_html=True)
