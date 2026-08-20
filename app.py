"""
Streamlit front-end for the news scraping workflow.

Editorial "wire terminal" design: newsprint paper background, a serif
masthead, monospace bylines (nod to the scraping/data-feed nature of the
tool), and a single restrained ink-red accent used only for the dispatch
button and the perforation marks on each article card.

Run with:
    streamlit run app.py

Requires (in addition to your existing project deps):
    pip install streamlit openpyxl

IMPORTANT:
1. This file assumes it lives next to your existing `main.py` (the one
   that defines `scrape_news`) at the project root, so `src/` is a
   sibling package. Adjust the import below if your layout differs.
2. Keep the `.streamlit/config.toml` next to this file. It forces a
   light Streamlit theme so the native inputs/dropdowns/header render
   with the same palette as the custom CSS below — without it,
   Streamlit auto-detects your OS/browser dark mode and renders its
   own widgets dark, which is what caused the unreadable dark boxes
   and black top bar in earlier versions of this file.
"""

import io
import sys
import traceback
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

# ------------------------------------------------------------------
# Make sure the project root (where main.py + src/ live) is importable
# ------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from main import scrape_news
except ImportError:
    st.set_page_config(page_title="News Wire", page_icon="📰")
    st.error(
        "Couldn't import `scrape_news` from `main.py`. "
        "Place this file next to main.py at your project root, "
        "or edit the import at the top of app.py to match your layout."
    )
    st.stop()


# ====================================================================
# PAGE CONFIG + STYLE
# ====================================================================

st.set_page_config(
    page_title="News Wire — Scraper Terminal",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

    :root{
        --paper:#EAE6DA;
        --card:#F6F3EA;
        --ink:#1C1B18;
        --ink-soft:#5B584E;
        --rule:#C9C2AE;
        --wire:#A93226;
        --wire-dark:#832B22;
    }

    /* ---------- Global reset ---------- */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"]{
        background-color:var(--paper) !important;
    }
    [data-testid="stHeader"]{
        border-bottom:1px solid var(--rule);
    }
    #MainMenu, footer{ visibility:hidden; }
    html, body, [class*="css"], p, span, label, div{
        font-family:'Inter', sans-serif;
        color:var(--ink);
    }
    .block-container{ padding-top:2rem; max-width:1150px; }

    /* ---------- Masthead ---------- */
    .masthead{
        text-align:center;
        padding:0.6rem 0 1rem 0;
        border-top:3px double var(--ink);
        border-bottom:3px double var(--ink);
        margin-bottom:1.4rem;
    }
    .masthead h1{
        font-family:'Source Serif 4', serif;
        font-weight:700;
        font-size:2.7rem;
        letter-spacing:0.04em;
        margin:0.2rem 0 0 0;
        color:var(--ink);
    }
    .masthead .tagline{
        font-family:'IBM Plex Mono', monospace;
        font-size:0.75rem;
        letter-spacing:0.18em;
        text-transform:uppercase;
        color:var(--ink-soft);
    }

    /* ---------- Dispatch (search) panel ---------- */
    div[data-testid="stForm"]{
        background-color:var(--card) !important;
        border:1px solid var(--rule);
        border-radius:8px;
        padding:1.6rem 1.8rem 1.2rem 1.8rem;
        box-shadow:0 4px 18px rgba(28,27,24,0.06);
    }
    .panel-label{
        font-family:'IBM Plex Mono', monospace;
        font-size:0.72rem;
        letter-spacing:0.14em;
        text-transform:uppercase;
        color:var(--wire-dark) !important;
        margin-bottom:0.3rem;
        font-weight:600;
    }

    /* Text inputs — force every descendant, don't rely on top-level bg alone */
    div[data-testid="stTextInput"] *,
    div[data-testid="stDateInput"] *,
    div[data-testid="stSelectbox"] *{
        color:var(--ink) !important;
        background-color:transparent !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child{
        background-color:#FFFFFF !important;
        border:1px solid var(--rule) !important;
        border-radius:6px !important;
    }
    div[data-testid="stTextInput"] input::placeholder{
        color:#9A9585 !important;
    }
    div[data-testid="stSelectbox"] svg,
    div[data-testid="stDateInput"] svg{
        fill:var(--ink) !important;
    }

    /* Dropdown / calendar popovers render in a portal outside the form —
       target by role/data-baseweb since they sit at the document root.
       Substring-match data-baseweb ("*=") so this holds regardless of the
       exact internal name (menu/popover/list) this Streamlit version uses. */
    [data-baseweb*="menu"],
    [data-baseweb*="popover"],
    [data-baseweb*="list"],
    [role="listbox"],
    [role="option"]{
        background-color:#FFFFFF !important;
        color:var(--ink) !important;
    }
    [data-baseweb*="menu"] *,
    [data-baseweb*="popover"] *,
    [data-baseweb*="list"] *,
    [role="listbox"] *{
        background-color:#FFFFFF !important;
        color:var(--ink) !important;
    }
    [role="option"]:hover,
    [aria-selected="true"]{
        background-color:var(--paper) !important;
    }
    [data-baseweb*="popover"],
    [data-baseweb*="menu"]{
        border:1px solid var(--rule) !important;
        border-radius:6px !important;
        box-shadow:0 8px 24px rgba(28,27,24,0.15) !important;
    }
    div[data-baseweb="calendar"] [aria-selected="true"] > div{
        background-color:var(--wire) !important;
        color:#FFFFFF !important;
    }

    /* Radio buttons */
    div[data-testid="stForm"] [data-testid="stRadio"] label{
        color:var(--ink) !important;
    }
    div[data-testid="stForm"] [data-testid="stRadio"] p{
        color:var(--ink) !important;
        font-weight:500;
    }

    /* Focus ring for accessibility */
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within{
        outline:2px solid var(--wire) !important;
        outline-offset:1px;
    }

    /* Hide the default deploy/hamburger toolbar so it doesn't clash with the masthead */
    [data-testid="stToolbarActions"]{ display:none !important; }

    /* Submit button — target both possible Streamlit wrappers and force
       every descendant's color so no inner span/p can stay dark-on-dark */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stForm"] .stButton button{
        background-color:var(--ink) !important;
        border:1px solid var(--ink) !important;
        border-radius:6px !important;
        font-family:'IBM Plex Mono', monospace !important;
        letter-spacing:0.1em;
        font-weight:600;
        padding:0.6rem 1rem;
        font-size:0.95rem;
        width:100%;
        transition:all 0.15s ease;
    }
    div[data-testid="stFormSubmitButton"] button *,
    div[data-testid="stForm"] .stButton button *{
        color:var(--paper) !important;
        background-color:transparent !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stForm"] .stButton button:hover{
        background-color:var(--wire) !important;
        border-color:var(--wire) !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover *,
    div[data-testid="stForm"] .stButton button:hover *{
        color:#FFFFFF !important;
    }

    /* ---------- Status / ticker line ---------- */
    .ticker{
        font-family:'IBM Plex Mono', monospace;
        font-size:0.82rem;
        letter-spacing:0.06em;
        color:var(--ink);
        border-top:1px solid var(--rule);
        border-bottom:1px solid var(--rule);
        padding:0.6rem 0.2rem;
        margin:1.6rem 0 1.1rem 0;
    }
    .ticker b{ color:var(--wire); }

    /* ---------- Article card ---------- */
    .clip{
        position:relative;
        background-color:var(--card);
        border:1px solid var(--rule);
        border-radius:8px;
        padding:1.2rem 1.3rem 1.05rem 1.3rem;
        margin-bottom:1.2rem;
        height:100%;
        box-shadow:0 2px 10px rgba(28,27,24,0.05);
        transition:box-shadow 0.15s ease, transform 0.15s ease;
    }
    .clip:hover{
        box-shadow:0 6px 20px rgba(28,27,24,0.1);
        transform:translateY(-1px);
    }
    .clip::before{
        content:"";
        position:absolute;
        top:-1px; left:0; right:0;
        height:2px;
        background-image:repeating-linear-gradient(90deg, var(--wire) 0 6px, transparent 6px 12px);
        opacity:0.7;
    }
    .clip .byline{
        font-family:'IBM Plex Mono', monospace;
        font-size:0.7rem;
        letter-spacing:0.08em;
        text-transform:uppercase;
        color:var(--wire-dark);
        margin-bottom:0.4rem;
        font-weight:600;
    }
    .clip h3{
        font-family:'Source Serif 4', serif;
        font-size:1.18rem;
        line-height:1.32;
        margin:0 0 0.55rem 0;
        color:var(--ink);
    }
    .clip p{
        font-size:0.89rem;
        line-height:1.55;
        color:var(--ink-soft);
        margin:0 0 0.85rem 0;
    }
    .clip a.read{
        font-family:'IBM Plex Mono', monospace;
        font-size:0.76rem;
        letter-spacing:0.06em;
        text-transform:uppercase;
        color:var(--ink);
        text-decoration:none;
        border-bottom:1px solid var(--ink);
        padding-bottom:1px;
        transition:color 0.15s ease, border-color 0.15s ease;
    }
    .clip a.read:hover{
        color:var(--wire);
        border-color:var(--wire);
    }

    /* ---------- Empty state ---------- */
    .empty-state{
        text-align:center;
        padding:3rem 1rem;
        border:1px dashed var(--rule);
        border-radius:4px;
        font-family:'IBM Plex Mono', monospace;
        color:var(--ink-soft);
        letter-spacing:0.04em;
        margin-top:1.2rem;
        background-color:var(--card);
    }

    div[data-testid="stDownloadButton"] button{
        background-color:#FFFFFF !important;
        border:1px solid var(--ink) !important;
        color:var(--ink) !important;
        font-family:'IBM Plex Mono', monospace !important;
        letter-spacing:0.05em;
        border-radius:6px !important;
    }
    div[data-testid="stDownloadButton"] button:hover{
        border-color:var(--wire) !important;
        color:var(--wire) !important;
    }
    </style>

    <div class="masthead">
        <div class="tagline">Automated Dispatch Terminal</div>
        <h1>THE NEWS WIRE</h1>
        <div class="tagline">Scrape &middot; Clean &middot; File</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ====================================================================
# REFERENCE DATA
# ====================================================================

LANGUAGES = {
    "English": "en", "Arabic": "ar", "German": "de", "Spanish": "es",
    "French": "fr", "Italian": "it", "Portuguese": "pt", "Russian": "ru",
    "Chinese": "zh",
}
COUNTRIES = {
    "Pakistan": "pk", "United States": "us", "United Kingdom": "gb",
    "India": "in", "Canada": "ca", "Australia": "au", "UAE": "ae",
}
CATEGORIES = [
    "General", "Technology", "Business", "Science",
    "Health", "Sports", "Entertainment",
]
SORT_OPTIONS = {"Newest": "publishedAt", "Relevancy": "relevancy", "Popularity": "popularity"}


# ====================================================================
# STATE
# ====================================================================

if "result" not in st.session_state:
    st.session_state.result = None
if "df" not in st.session_state:
    st.session_state.df = None
if "error" not in st.session_state:
    st.session_state.error = None


def get_field(article, *keys, default=""):
    """Best-effort field lookup across possibly-varying cleaned-data keys."""
    for key in keys:
        value = article.get(key) if isinstance(article, dict) else None
        if isinstance(value, dict):
            value = value.get("name")
        if value:
            return value
    return default


# ====================================================================
# DISPATCH PANEL (search form)
# ====================================================================

with st.form("search_form"):
    st.markdown('<div class="panel-label">Search keyword</div>', unsafe_allow_html=True)
    keyword = st.text_input("Search keyword", placeholder="e.g. artificial intelligence", label_visibility="collapsed")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel-label">Search type</div>', unsafe_allow_html=True)
        search_type = st.radio(
            "Search type", ["All Articles", "Top Headlines"],
            horizontal=True, label_visibility="collapsed",
        )
    with c2:
        st.markdown('<div class="panel-label">Category</div>', unsafe_allow_html=True)
        category = st.selectbox("Category", CATEGORIES, label_visibility="collapsed")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel-label">Language</div>', unsafe_allow_html=True)
        language_label = st.selectbox("Language", list(LANGUAGES.keys()), label_visibility="collapsed")
    with c4:
        st.markdown('<div class="panel-label">Country</div>', unsafe_allow_html=True)
        country_label = st.selectbox("Country", list(COUNTRIES.keys()), label_visibility="collapsed")

    c5, c6, c7 = st.columns([1, 1, 1])
    with c5:
        st.markdown('<div class="panel-label">Sort by</div>', unsafe_allow_html=True)
        sort_label = st.selectbox("Sort by", list(SORT_OPTIONS.keys()), label_visibility="collapsed")
    with c6:
        st.markdown('<div class="panel-label">Date from</div>', unsafe_allow_html=True)
        date_from = st.date_input("Date from", value=date.today() - timedelta(days=7), label_visibility="collapsed")
    with c7:
        st.markdown('<div class="panel-label">Date to</div>', unsafe_allow_html=True)
        date_to = st.date_input("Date to", value=date.today(), label_visibility="collapsed")

    st.write("")
    submitted = st.form_submit_button("🔎  SEARCH NEWS")

if submitted:
    if not keyword.strip():
        st.session_state.error = "Enter a search keyword before dispatching a search."
        st.session_state.result = None
    else:
        st.session_state.error = None
        with st.spinner("Dispatching request to the wire…"):
            try:
                # NOTE: the current scrape_news() workflow only accepts
                # keyword / language / sort_by. Category, country, date
                # range and "Top Headlines" are captured in the UI above
                # but need matching support added to NewsAPI (e.g. a
                # get_top_headlines() method with category/country params)
                # before they can be wired through here.
                result = scrape_news(
                    keyword=keyword.strip(),
                    language=LANGUAGES[language_label],
                    sort_by=SORT_OPTIONS[sort_label],
                )
                st.session_state.result = result
                st.session_state.df = pd.DataFrame(result.get("articles", []))
            except Exception as exc:  # noqa: BLE001
                st.session_state.error = f"The scrape failed: {exc}"
                st.session_state.result = None
                st.session_state.df = None
                with st.expander("Full error trace"):
                    st.code(traceback.format_exc())

if search_type == "Top Headlines" and submitted:
    st.info(
        "Heads up — the backend currently only implements the "
        "\"All Articles\" (everything) endpoint, so this search ran "
        "against that instead of Top Headlines.",
        icon="ℹ️",
    )

if st.session_state.error:
    st.error(st.session_state.error)


# ====================================================================
# RESULTS
# ====================================================================

if st.session_state.result:
    result = st.session_state.result
    df = st.session_state.df
    articles = result.get("articles", [])
    total = result.get("total_results", len(articles))

    st.markdown(
        f'<div class="ticker">🛰 DISPATCH RECEIVED &nbsp;—&nbsp; '
        f'<b>{len(articles)}</b> ARTICLES FILED &nbsp;'
        f'(<b>{total}</b> TOTAL MATCHES ON THE WIRE)</div>',
        unsafe_allow_html=True,
    )

    dl1, dl2, _ = st.columns([1, 1, 4])
    with dl1:
        st.download_button(
            "📥 Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="news_export.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dl2:
        try:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Articles")
            st.download_button(
                "📊 Download Excel",
                data=buf.getvalue(),
                file_name="news_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except ImportError:
            st.caption("Install `openpyxl` to enable Excel export.")

    if not articles:
        st.markdown(
            '<div class="empty-state">No dispatches matched this search. '
            "Try a broader keyword or a wider date range.</div>",
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns(2)
        for i, article in enumerate(articles):
            title = get_field(article, "title", default="Untitled dispatch")
            source = get_field(article, "source", "source_name", "sourceName", default="Unknown source")
            published = get_field(article, "publishedAt", "published_at", "date")
            try:
                published = pd.to_datetime(published).strftime("%d %b %Y")
            except Exception:  # noqa: BLE001
                published = published or "Undated"
            description = get_field(article, "description", "content", default="No description available.")
            url = get_field(article, "url", "link", default="#")

            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="clip">
                        <div class="byline">{source} &middot; {published}</div>
                        <h3>{title}</h3>
                        <p>{description}</p>
                        <a class="read" href="{url}" target="_blank" rel="noopener noreferrer">Read Article →</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
else:
    st.markdown(
        '<div class="empty-state">Awaiting dispatch — fill in a keyword above '
        "and press Search News to pull the latest wire copy.</div>",
        unsafe_allow_html=True,
    )