import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎬 Movie Info Extractor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 70%, #0f3460 100%);
    min-height: 100vh;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.hero-banner {
    background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 50%, rgba(240,147,43,0.10) 100%);
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(10px);
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f0932b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
}

.hero-subtitle {
    color: rgba(200,200,230,0.75);
    font-size: 1.05rem;
    margin-top: 0.6rem;
    font-weight: 400;
}

.section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(102,126,234,0.25);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.3s ease, transform 0.2s ease;
}

.section-card:hover {
    border-color: rgba(102,126,234,0.55);
    transform: translateY(-2px);
}

.section-title {
    color: #667eea;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

.section-body {
    color: rgba(220,220,240,0.9);
    font-size: 0.95rem;
    line-height: 1.7;
    white-space: pre-wrap;
}

textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(102,126,234,0.35) !important;
    border-radius: 12px !important;
    color: #e0e0f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.3s ease !important;
}

textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102,126,234,0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2.2rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.45) !important;
}

[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.85) !important;
    border-right: 1px solid rgba(102,126,234,0.2) !important;
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: rgba(200,200,230,0.85) !important;
}

.model-badge {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
    border: 1px solid rgba(102,126,234,0.35);
    border-radius: 20px;
    color: #a0a8ff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.8rem;
    display: inline-block;
}

.tag-success {
    background: linear-gradient(135deg, rgba(56,239,125,0.15), rgba(17,153,142,0.15));
    border: 1px solid rgba(56,239,125,0.35);
    border-radius: 8px;
    color: #56e0a0;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.25rem 0.8rem;
    display: inline-block;
}

.result-container {
    max-height: 72vh;
    overflow-y: auto;
    padding-right: 0.4rem;
}

.result-container::-webkit-scrollbar { width: 5px; }
.result-container::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
}
.result-container::-webkit-scrollbar-thumb {
    background: rgba(102,126,234,0.4);
    border-radius: 4px;
}

hr { border-color: rgba(102,126,234,0.2) !important; }
</style>
""", unsafe_allow_html=True)


# ── Env & cached model ──────────────────────────────────────────────────────────
load_dotenv()

@st.cache_resource(show_spinner=False)
def load_model():
    return init_chat_model("openai/gpt-oss-120b", model_provider="groq")


# ── Prompt (mirrors core.py exactly) ───────────────────────────────────────────
PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are an information extraction assistant.

Analyze the following text and extract the most useful information about the movie.

Provide the answer in clear, simple plain text. Do not use JSON.

Include the following sections:

Movie Information:
- Movie name
- Release year
- Genre
- Director
- Writers
- Main cast and the characters they play

Story Information:
- Main characters
- Setting
- Main plot
- Important events
- Important locations

Themes:
- Main themes explored in the movie

Scientific or Technical Concepts:
- Important scientific or technical concepts mentioned
- Brief explanation of each concept

Production Information:
- Composer or music
- Important collaborators
- Other notable production details

Reception:
- Critical reception or impact mentioned in the text

Quick Summary:
- Give a short summary of the entire text in 2 to 4 sentences.

Important rules:
- Only use information provided in the text.
- Do not invent information.
- If something is not mentioned, say "Not mentioned."
- Keep the information concise and easy to read.
- Do not use JSON.
- Do not provide unnecessary explanations.
"""),
    ('human', """
 Extract information from this paragraph:

 {paragraph}
 """)
])


# ── Section metadata ────────────────────────────────────────────────────────────
SECTIONS = {
    "Movie Information": "🎬",
    "Story Information": "📖",
    "Themes": "💡",
    "Scientific or Technical Concepts": "🔬",
    "Production Information": "🎵",
    "Reception": "⭐",
    "Quick Summary": "📝",
}


def parse_sections(raw: str) -> dict:
    """Parse the LLM plain-text response into named sections."""
    sections = {}
    current_key = None
    current_lines = []

    for line in raw.splitlines():
        stripped = line.strip()
        matched = None
        for key in SECTIONS:
            if stripped.lower().startswith(key.lower()):
                matched = key
                break
        if matched:
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = matched
            current_lines = []
        else:
            if current_key is not None:
                current_lines.append(line)

    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


def render_results(raw_text: str):
    sections = parse_sections(raw_text)

    if not sections:
        st.markdown(f'<div class="section-card"><div class="section-body">{raw_text}</div></div>',
                    unsafe_allow_html=True)
        return

    for name, body in sections.items():
        icon = SECTIONS.get(name, "📌")
        safe_body = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f"""
        <div class="section-card">
          <div class="section-title">{icon}&nbsp; {name}</div>
          <div class="section-body">{safe_body}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    st.markdown("**Model**")
    st.markdown('<span class="model-badge">openai/gpt-oss-120b · Groq</span>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown("**How to use**")
    st.markdown("""
1. Paste a movie-related paragraph into the text area.
2. Click **⚡ Extract Info**.
3. View structured results on the right panel.
4. Download results with the **⬇️ Download** button.
    """)
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("""
Powered by a **LangChain + Groq** pipeline.
Extracts 7 structured sections from any movie text.
    """)
    st.markdown("")
    st.markdown('<span class="tag-success">✓ Pipeline Ready</span>', unsafe_allow_html=True)


# ── Hero banner ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <p class="hero-title">🎬 Movie Info Extractor</p>
  <p class="hero-subtitle">
    Paste any movie-related paragraph and get a fully structured breakdown —
    cast, plot, themes, production, and more — powered by AI.
  </p>
</div>
""", unsafe_allow_html=True)


# ── Two-column layout ────────────────────────────────────────────────────────────
col_in, col_out = st.columns([1, 1], gap="large")

# ── Left: Input ─────────────────────────────────────────────────────────────────
with col_in:
    st.markdown("### 📥 Input Paragraph")

    # Example loader
    if "load_example" not in st.session_state:
        st.session_state["load_example"] = False

    default_text = ""
    if st.session_state["load_example"]:
        default_text = (
            "Interstellar (2014) is a science fiction epic directed by Christopher Nolan and "
            "written by Christopher and Jonathan Nolan. It stars Matthew McConaughey as Cooper, "
            "a former NASA pilot and widowed farmer, along with Anne Hathaway as Dr. Brand, "
            "Jessica Chastain as Murphy, and Michael Caine as Professor Brand. The story follows "
            "a team of astronauts who travel through a wormhole near Saturn in search of a new "
            "habitable planet for humanity, as Earth faces an extinction-level crop blight. The "
            "film explores themes of love, time, sacrifice, and human survival. Key scientific "
            "concepts include relativity, wormholes, black holes, and time dilation, advised by "
            "physicist Kip Thorne. Hans Zimmer composed the iconic organ-heavy score. The film "
            "was praised for its visual effects, emotional depth, and scientific accuracy, grossing "
            "over $700 million worldwide."
        )
        st.session_state["load_example"] = False

    paragraph = st.text_area(
        label="paragraph",
        value=default_text,
        height=340,
        placeholder=(
            "e.g. Interstellar (2014) is a science fiction film directed by Christopher Nolan. "
            "It stars Matthew McConaughey as Cooper, a former NASA pilot who leads a team of "
            "explorers through a wormhole in search of a new home for humanity..."
        ),
        label_visibility="collapsed",
        key="para_input",
    )

    # Stats row
    word_count = len(paragraph.split()) if paragraph.strip() else 0
    char_count = len(paragraph)

    btn_col, stat_col = st.columns([1, 2])
    with btn_col:
        extract_btn = st.button("⚡ Extract Info", use_container_width=True)
    with stat_col:
        if paragraph.strip():
            st.markdown(
                f'<p style="color:rgba(190,190,220,0.6);font-size:0.82rem;margin-top:0.65rem;">'
                f'📊 {word_count} words · {char_count} chars</p>',
                unsafe_allow_html=True,
            )

    # Example expander
    with st.expander("💡 Try an example"):
        if st.button("Load Interstellar Example", key="ex_btn"):
            st.session_state["load_example"] = True
            st.rerun()


# ── Right: Output ────────────────────────────────────────────────────────────────
with col_out:
    st.markdown("### 📤 Extracted Information")

    if extract_btn:
        if not paragraph.strip():
            st.warning("⚠️ Please enter a paragraph before extracting.")
        else:
            with st.spinner("🧠 Analyzing with AI…"):
                try:
                    model = load_model()
                    final_prompt = PROMPT.invoke({"paragraph": paragraph})
                    response = model.invoke(final_prompt)
                    st.session_state["result"] = response.content
                except Exception as e:
                    st.error(f"❌ Extraction failed: {e}")
                    st.session_state.pop("result", None)

    if "result" in st.session_state:
        raw = st.session_state["result"]

        dl_col, _ = st.columns([1, 3])
        with dl_col:
            st.download_button(
                label="⬇️ Download",
                data=raw,
                file_name="movie_extraction.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        render_results(raw)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            border: 1.5px dashed rgba(102,126,234,0.3);
            border-radius: 16px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: rgba(180,180,220,0.45);
            margin-top: 0.5rem;
        ">
            <p style="font-size:3rem; margin:0;">🎞️</p>
            <p style="font-size:1rem; margin-top:0.8rem; font-weight:500;">
                Results will appear here
            </p>
            <p style="font-size:0.85rem; margin-top:0.3rem;">
                Paste a paragraph and click <strong>⚡ Extract Info</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="text-align:center; color:rgba(150,150,190,0.45); font-size:0.78rem; margin-top:0.5rem;">
    Built with LangChain · Groq · Streamlit &nbsp;|&nbsp; Data Extraction Pipeline
</p>
""", unsafe_allow_html=True)
