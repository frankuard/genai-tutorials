import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional

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

/* ── Movie card ── */
.movie-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(8px);
}

.movie-title-text {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #f0932b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.3rem 0;
}

.movie-year {
    color: rgba(180,180,220,0.55);
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, rgba(240,147,43,0.2), rgba(240,100,43,0.2));
    border: 1px solid rgba(240,147,43,0.45);
    border-radius: 30px;
    color: #f0b03b;
    font-size: 0.9rem;
    font-weight: 700;
    padding: 0.3rem 1rem;
    margin-bottom: 1.2rem;
}

.info-row {
    display: flex;
    gap: 0.7rem;
    align-items: flex-start;
    margin-bottom: 0.75rem;
}

.info-label {
    color: #667eea;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    min-width: 80px;
    padding-top: 0.08rem;
}

.info-value {
    color: rgba(220,220,240,0.92);
    font-size: 0.92rem;
    line-height: 1.6;
    flex: 1;
}

.genre-pill {
    display: inline-block;
    background: linear-gradient(135deg, rgba(102,126,234,0.18), rgba(118,75,162,0.18));
    border: 1px solid rgba(102,126,234,0.35);
    border-radius: 20px;
    color: #a0a8ff;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.18rem 0.75rem;
    margin: 0.15rem 0.2rem 0.15rem 0;
}

.summary-card {
    background: rgba(102,126,234,0.07);
    border-left: 3px solid #667eea;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    color: rgba(215,215,238,0.9);
    font-size: 0.93rem;
    line-height: 1.75;
    font-style: italic;
}

.field-divider {
    border: none;
    border-top: 1px solid rgba(102,126,234,0.15);
    margin: 0.75rem 0;
}

hr { border-color: rgba(102,126,234,0.2) !important; }
</style>
""", unsafe_allow_html=True)


# ── Movie schema (mirrors core.py exactly) ─────────────────────────────────────
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


# ── Env & cached model ──────────────────────────────────────────────────────────
load_dotenv()

@st.cache_resource(show_spinner=False)
def load_model():
    return init_chat_model("openai/gpt-oss-120b", model_provider="groq")


# ── Parser & prompt (mirrors core.py exactly) ──────────────────────────────────
parser = PydanticOutputParser(pydantic_object=Movie)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
     Extract movie information from the paragraph
     {format_instructions},
     """),
    ("human", "{paragraph}")
])


# ── Render the structured Movie result ─────────────────────────────────────────
def render_movie(movie: Movie):
    if movie.rating is not None:
        filled = int(round(movie.rating / 2))
        stars = "\u2605" * filled + "\u2606" * (5 - filled)
        rating_html = f'<div class="rating-badge">{stars}&nbsp; {movie.rating}/10</div>'
    else:
        rating_html = ""

    genre_pills = "".join(
        f'<span class="genre-pill">{g}</span>' for g in (movie.genre or ["\u2014"])
    )
    cast_str = ", ".join(movie.cast) if movie.cast else "Not mentioned"
    year_str = str(movie.release_year) if movie.release_year else "Year unknown"

    st.markdown(f"""
    <div class="movie-card">
        <p class="movie-title-text">{movie.title}</p>
        <p class="movie-year">&#128197; {year_str}</p>
        {rating_html}
        <hr class="field-divider">
        <div class="info-row">
            <span class="info-label">Genre</span>
            <span class="info-value">{genre_pills}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Director</span>
            <span class="info-value">{movie.director or "Not mentioned"}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Cast</span>
            <span class="info-value">{cast_str}</span>
        </div>
        <hr class="field-divider">
        <div class="summary-card">"{movie.summary}"</div>
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
3. View the structured movie card on the right.
4. Download the raw JSON with the **⬇️ Download** button.
    """)
    st.markdown("---")
    st.markdown("**Output schema**")
    st.markdown("""
| Field | Type |
|---|---|
| `title` | string |
| `release_year` | int? |
| `genre` | list |
| `director` | string? |
| `cast` | list |
| `rating` | float? |
| `summary` | string |
    """)
    st.markdown("")
    st.markdown('<span class="tag-success">✓ Pipeline Ready</span>', unsafe_allow_html=True)


# ── Hero banner ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <p class="hero-title">&#127916; Movie Info Extractor</p>
  <p class="hero-subtitle">
    Paste any movie-related paragraph and get a clean structured card &mdash;
    title, year, genre, director, cast, rating &amp; summary &mdash; powered by AI.
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
            "concepts include relativity, wormholes, black holes, and time dilation. Hans Zimmer "
            "composed the iconic organ-heavy score. The film was praised for its visual effects "
            "and grossed over $700 million worldwide. IMDb rating: 8.7/10."
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
                f'&#128202; {word_count} words · {char_count} chars</p>',
                unsafe_allow_html=True,
            )

    # Example expander
    with st.expander("💡 Try an example"):
        if st.button("Load Interstellar Example", key="ex_btn"):
            st.session_state["load_example"] = True
            st.rerun()


# ── Right: Output ────────────────────────────────────────────────────────────────
with col_out:
    st.markdown("### 📤 Extracted Movie Card")

    if extract_btn:
        if not paragraph.strip():
            st.warning("⚠️ Please enter a paragraph before extracting.")
        else:
            with st.spinner("🧠 Analyzing with AI…"):
                try:
                    model = load_model()
                    final_prompt = PROMPT.invoke({
                        "paragraph": paragraph,
                        "format_instructions": parser.get_format_instructions(),
                    })
                    response = model.invoke(final_prompt)
                    movie: Movie = parser.parse(response.content)
                    st.session_state["movie"] = movie
                    st.session_state["raw_json"] = movie.model_dump_json(indent=2)
                except Exception as e:
                    st.error(f"❌ Extraction failed: {e}")
                    st.session_state.pop("movie", None)
                    st.session_state.pop("raw_json", None)

    if "movie" in st.session_state:
        movie: Movie = st.session_state["movie"]
        raw_json: str = st.session_state["raw_json"]

        dl_col, _ = st.columns([1, 3])
        with dl_col:
            st.download_button(
                label="⬇️ Download JSON",
                data=raw_json,
                file_name="movie_extraction.json",
                mime="application/json",
                use_container_width=True,
            )

        render_movie(movie)

        with st.expander("🔍 Raw JSON"):
            st.code(raw_json, language="json")
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
            <p style="font-size:3rem; margin:0;">&#127902;</p>
            <p style="font-size:1rem; margin-top:0.8rem; font-weight:500;">
                Movie card will appear here
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
