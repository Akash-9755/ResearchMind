import html
import sys

import streamlit as st

st.set_page_config(
    page_title="ResearchMind",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Import your agents. If this fails, show exactly why instead of a blank crash.
# ---------------------------------------------------------------------------
try:
    from agent import build_search_agent, build_reader_agent, writer_chain, critic_chain
except Exception as import_error:
    st.error("Could not import from agent.py")
    st.exception(import_error)
    st.caption(f"Streamlit is running with this Python: {sys.executable}")
    st.caption("Keep app.py in the same folder as agent.py and tools.py, and start it with: python -m streamlit run app.py")
    st.stop()

# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
AGENTS = [
    {"key": "search", "name": "Search Agent", "desc": "Gathers recent web information"},
    {"key": "reader", "name": "Reader Agent", "desc": "Scrapes & extracts deep content"},
    {"key": "writer", "name": "Writer Chain", "desc": "Drafts the full research report"},
    {"key": "critic", "name": "Critic Chain", "desc": "Reviews & scores the report"},
]
STATE_LABEL = {"idle": "WAITING", "running": "WORKING", "done": "DONE", "error": "FAILED"}
EXAMPLES = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #09090B; --card: #111114; --card-hi: #16161A; --line: #232328;
  --text: #ECE9E2; --soft: #BDBAB2; --muted: #8B8B93;
  --orange: #FF8A2B; --orange2: #FF5A1F; --amber: #FFC15E; --coral: #FF6B6B; --sand: #E8D5B5;
}

html, body, .stApp, button, input, [data-testid="stMarkdownContainer"] { font-family: 'DM Sans', system-ui, sans-serif; }
.stApp {
  background: radial-gradient(900px 380px at 50% -90px, rgba(255,122,41,.14), transparent 70%), var(--bg);
  color: var(--text);
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"], #MainMenu, footer { display: none; }
[data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] { display: none; }
.block-container { max-width: 1080px; padding-top: 2.4rem; padding-bottom: 2rem; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color: var(--text); }

/* ---------- hero ---------- */
.hero { text-align: center; margin-bottom: 1.6rem; }
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: .72rem; letter-spacing: .22em; color: var(--orange); }
.hero-title {
  font-family: 'Syne', sans-serif; font-weight: 700; font-size: clamp(2.8rem, 8vw, 5.4rem);
  letter-spacing: -0.035em; line-height: 1.05; margin: .9rem 0 1.1rem 0; color: #F4F1EA;
}
.hero-title span { color: var(--orange); }
.hero-sub { color: var(--soft); font-size: 1.02rem; line-height: 1.65; max-width: 540px; margin: 0 auto; }
.rule { height: 1px; margin: 2rem 0 2.2rem 0; background: linear-gradient(90deg, transparent, #2C2C32 20%, #2C2C32 80%, transparent); }

/* ---------- left column: input ---------- */
.field-label { font-family: 'JetBrains Mono', monospace; font-size: .72rem; letter-spacing: .16em; color: var(--orange); margin: 0 0 .5rem 0; }
.try-label { font-family: 'JetBrains Mono', monospace; font-size: .68rem; letter-spacing: .16em; color: var(--muted); margin: 1.2rem 0 .5rem 0; }

.stTextInput div[data-baseweb="input"] {
  background: #1B1B1F; border: 1px solid #2C2C32; border-radius: 10px;
  transition: border-color .15s ease, box-shadow .15s ease;
}
.stTextInput div[data-baseweb="input"]:hover { border-color: rgba(255,138,43,.55); }
.stTextInput div[data-baseweb="input"]:focus-within { border-color: var(--orange); box-shadow: 0 0 0 3px rgba(255,138,43,.16); }
.stTextInput input { color: var(--text); font-size: .95rem; padding: .7rem .9rem; background: transparent; }
.stTextInput input::placeholder { color: var(--muted); opacity: 1; }

/* chips (every normal button) */
.stButton > button {
  background: #141417; border: 1px solid #26262B; border-radius: 6px; padding: .28rem .7rem; min-height: 0;
  color: var(--soft); font-size: .78rem; font-weight: 500;
  transition: transform .15s ease, border-color .15s ease, color .15s ease, box-shadow .15s ease;
}
.stButton > button p { color: inherit; font-size: inherit; }
.stButton > button:hover { transform: translateY(-2px); border-color: var(--orange); color: var(--orange); box-shadow: 0 8px 18px -12px var(--orange); }
.stButton > button:focus-visible { outline: 2px solid var(--orange); outline-offset: 2px; }

/* main run button */
.stButton:has(button[kind="primary"]), .stButton:has(button[data-testid="stBaseButton-primary"]) { width: 100%; }
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {
  width: 100%; padding: .8rem 1rem; border: none; border-radius: 10px; font-size: .95rem; font-weight: 600;
  background: linear-gradient(90deg, #FF8A2B, #FF5A1F); color: #1A0D05;
  box-shadow: 0 0 28px rgba(255,106,31,.32);
}
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="stBaseButton-primary"]:hover {
  color: #1A0D05; filter: brightness(1.07); box-shadow: 0 0 40px rgba(255,106,31,.5); transform: translateY(-2px);
}
.stButton > button:disabled { opacity: .45; transform: none; box-shadow: none; filter: none; }

/* ---------- right column: pipeline ---------- */
.pipe-h { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.4rem; color: #F4F1EA; margin: .2rem 0 1rem 0; }
.step {
  display: grid; grid-template-columns: 30px 1fr auto; column-gap: 8px; row-gap: 6px; align-items: baseline;
  background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 15px 18px; margin-bottom: 14px;
  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease, background .2s ease;
}
.step:hover { transform: translateY(-3px); border-color: rgba(255,138,43,.5); background: var(--card-hi); box-shadow: 0 14px 28px -18px var(--orange); }
.step-num { font-family: 'JetBrains Mono', monospace; font-size: .72rem; color: var(--orange); }
.step-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: .98rem; color: #F4F1EA; }
.step-state { font-family: 'JetBrains Mono', monospace; font-size: .66rem; letter-spacing: .14em; color: #5E5E66; }
.step-desc { grid-column: 2 / 4; font-size: .8rem; color: var(--muted); }
.step.running { border-color: var(--orange); animation: glow 1.4s ease-in-out infinite; }
.step.running .step-state, .step.done .step-state { color: var(--orange); }
.step.done { border-color: rgba(255,138,43,.35); }
.step.error { border-color: #C0392B; }
.step.error .step-state { color: #FF6B6B; }
@keyframes glow { 50% { box-shadow: 0 0 0 3px rgba(255,138,43,.16), 0 0 22px -4px rgba(255,138,43,.5); } }
@media (prefers-reduced-motion: reduce) { .step.running { animation: none; } .step, .step:hover, .stButton > button { transition: none; } }

/* ---------- results ---------- */
.results-h { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.9rem; color: #F4F1EA; margin: 2.4rem 0 1rem 0; letter-spacing: -0.02em; }
.results-h span { color: var(--orange); }
.sec-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.45rem; color: var(--c); margin: .1rem 0 .1rem 0; }
.sec-sub { font-family: 'JetBrains Mono', monospace; font-size: .7rem; letter-spacing: .1em; color: var(--muted); margin-bottom: .9rem; text-transform: uppercase; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { background: transparent; color: var(--muted); font-weight: 500; padding: 10px 16px; border-radius: 8px 8px 0 0; transition: color .15s ease, background .15s ease; }
.stTabs [data-baseweb="tab"]:hover { color: var(--orange); background: rgba(255,138,43,.07); }
.stTabs [aria-selected="true"] { color: #F4F1EA; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--orange); height: 2px; }
.stTabs [data-baseweb="tab-border"] { background: var(--line); }

.st-key-card_report   { --c: var(--orange); }
.st-key-card_feedback { --c: var(--coral); }
.st-key-card_search   { --c: var(--amber); }
.st-key-card_scraped  { --c: var(--sand); }
[class*="st-key-card_"] {
  background: var(--card); border: 1px solid var(--line); border-left: 3px solid var(--c); border-radius: 12px;
  padding: 1.3rem 1.6rem; margin-top: .9rem; transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}
[class*="st-key-card_"]:hover { transform: translateY(-3px); border-color: var(--c); box-shadow: 0 16px 30px -20px var(--c); }
[class*="st-key-card_"] h1, [class*="st-key-card_"] h2, [class*="st-key-card_"] h3, [class*="st-key-card_"] h4 { font-family: 'Syne', sans-serif; }
[class*="st-key-card_"] h1 { color: #F4F1EA; }
[class*="st-key-card_"] h2 { color: var(--orange); }
[class*="st-key-card_"] h3 { color: var(--amber); }
[class*="st-key-card_"] h4 { color: var(--sand); }
[class*="st-key-card_"] p, [class*="st-key-card_"] li { color: #D8D5CE; line-height: 1.75; }
[class*="st-key-card_"] a { color: var(--orange); }
[class*="st-key-card_"] code { background: #1C1C20; color: var(--amber); }

[data-testid="stDownloadButton"] button {
  background: transparent; border: 1px solid #34343A; border-radius: 8px; color: var(--soft);
  transition: transform .15s ease, border-color .15s ease, color .15s ease, box-shadow .15s ease;
}
[data-testid="stDownloadButton"] button p { color: inherit; }
[data-testid="stDownloadButton"] button:hover { transform: translateY(-2px); border-color: var(--orange); color: var(--orange); box-shadow: 0 8px 18px -12px var(--orange); }

[data-testid="stAlert"] { background: #2A1315; border: 1px solid #5B2226; border-radius: 10px; }
[data-testid="stAlert"] p { color: #FFC9C9; }

.footer { text-align: center; font-family: 'JetBrains Mono', monospace; font-size: .68rem; letter-spacing: .06em; color: #5E5E66; margin: 3.5rem 0 .5rem 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_text(content) -> str:
    """Agent output can be a str or a list of content blocks; always return plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(str(block.get("text", "")))
            else:
                parts.append(str(getattr(block, "text", block)))
        return "\n".join(p for p in parts if p)
    return str(content)


def md(text: str) -> str:
    """Escape $ so prices in a report don't get rendered as LaTeX."""
    return text.replace("$", "\\$")


def card(key: str):
    """A keyed container (needs a recent Streamlit); falls back to a plain one."""
    try:
        return st.container(key=key)
    except TypeError:
        return st.container()


def render_pipeline(status: dict) -> str:
    cards = []
    for i, a in enumerate(AGENTS, start=1):
        s = status.get(a["key"], "idle")
        cards.append(
            f'<div class="step {s}">'
            f'<div class="step-num">{i:02d}</div>'
            f'<div class="step-name">{a["name"]}</div>'
            f'<div class="step-state">{STATE_LABEL[s]}</div>'
            f'<div class="step-desc">{a["desc"]}</div></div>'
        )
    return "".join(cards)


def section(title: str, sub: str, color: str) -> str:
    return f'<div class="sec-title" style="--c:{color}">{title}</div><div class="sec-sub">{sub}</div>'


# ---------------------------------------------------------------------------
# Pipeline steps (same logic and prompts as pipeline.py)
# ---------------------------------------------------------------------------
def run_search(topic: str) -> str:
    agent = build_search_agent()
    result = agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    return to_text(result["messages"][-1].content)


def run_reader(topic: str, search_results: str) -> str:
    agent = build_reader_agent()
    result = agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{search_results[:800]}"
        )]
    })
    return to_text(result["messages"][-1].content)


def run_writer(topic: str, search_results: str, scraped: str) -> str:
    research_combined = (
        f"SEARCH RESULTS : \n {search_results} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {scraped}"
    )
    return to_text(writer_chain.invoke({"topic": topic, "research": research_combined}))


def run_critic(report: str) -> str:
    return to_text(critic_chain.invoke({"report": report}))


def set_topic(value: str):
    st.session_state["topic_input"] = value


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero">'
    '<div class="eyebrow">MULTI-AGENT AI SYSTEM</div>'
    '<div class="hero-title">Research<span>Mind</span></div>'
    '<div class="hero-sub">Four specialized AI agents collaborate — searching, scraping, writing, '
    "and critiquing — to deliver a polished research report on any topic.</div></div>"
    '<div class="rule"></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Two columns: input (left) and pipeline (right)
# ---------------------------------------------------------------------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="field-label">RESEARCH TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        key="topic_input",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
    run_clicked = st.button("⚡ Run Research Pipeline", type="primary", disabled=not topic.strip())

    st.markdown('<div class="try-label">TRY →</div>', unsafe_allow_html=True)
    for i, ex in enumerate(EXAMPLES):
        st.button(ex, key=f"example_{i}", on_click=set_topic, args=(ex,))

with right:
    st.markdown('<div class="pipe-h">Pipeline</div>', unsafe_allow_html=True)
    pipe_slot = st.empty()
    pipe_slot.markdown(render_pipeline(st.session_state.get("status", {})), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if run_clicked:
    status = {a["key"]: "idle" for a in AGENTS}
    ctx = {"current": None}
    state = {"topic": topic.strip()}

    def advance(key, fn):
        ctx["current"] = key
        status[key] = "running"
        pipe_slot.markdown(render_pipeline(status), unsafe_allow_html=True)
        out = fn()
        status[key] = "done"
        pipe_slot.markdown(render_pipeline(status), unsafe_allow_html=True)
        return out

    try:
        state["search_results"] = advance("search", lambda: run_search(state["topic"]))
        state["scraped_content"] = advance("reader", lambda: run_reader(state["topic"], state["search_results"]))
        state["report"] = advance("writer", lambda: run_writer(state["topic"], state["search_results"], state["scraped_content"]))
        state["feedback"] = advance("critic", lambda: run_critic(state["report"]))
        st.session_state["result"] = state
        st.toast("Research complete", icon="✅")
    except Exception as e:
        if ctx["current"]:
            status[ctx["current"]] = "error"
            pipe_slot.markdown(render_pipeline(status), unsafe_allow_html=True)
        st.error(f"The {ctx['current'] or 'pipeline'} step failed.")
        st.exception(e)  # full traceback, so the real cause is visible
    finally:
        st.session_state["status"] = status

# ---------------------------------------------------------------------------
# Results (kept in session_state so they survive reruns)
# ---------------------------------------------------------------------------
result = st.session_state.get("result")
if result:
    st.markdown(
        f'<div class="results-h">Results <span>/ {html.escape(result["topic"])}</span></div>',
        unsafe_allow_html=True,
    )

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["Final report", "Critic feedback", "Search results", "Scraped content"]
    )

    with tab_report:
        with card("card_report"):
            st.markdown(section("Final report", "Drafted by the writer chain", "var(--orange)"), unsafe_allow_html=True)
            st.markdown(md(result["report"]))
        st.download_button(
            "Download report (.md)",
            data=result["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        with card("card_feedback"):
            st.markdown(section("Critic feedback", "Review by the critic chain", "var(--coral)"), unsafe_allow_html=True)
            st.markdown(md(result["feedback"]))

    with tab_search:
        with card("card_search"):
            st.markdown(section("Search results", "Gathered by the search agent", "var(--amber)"), unsafe_allow_html=True)
            st.markdown(md(result["search_results"]))

    with tab_scraped:
        with card("card_scraped"):
            st.markdown(section("Scraped content", "Extracted by the reader agent", "var(--sand)"), unsafe_allow_html=True)
            st.markdown(md(result["scraped_content"]))

st.markdown(
    '<div class="footer">ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit</div>',
    unsafe_allow_html=True,
)