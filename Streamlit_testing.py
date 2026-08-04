"""
streamlit_testing.py
=====================
Most Streamed Spotify Tracks 2025 — Dynamic Analytics Dashboard

Run it with (from the folder that contains this file AND the CSV):
    streamlit run streamlit_testing.py

Expected data file (same folder as this script):
    most_streamed_spotify_2025.csv

Columns used:
    rank, track, artist, billed_artist_count, is_collaboration,
    spotify_streams_total, daily_streams, daily_streams_rank,
    daily_stream_share_pct, wrapped_global_top10_rank
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Spotify 2025 Streaming Dashboard",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "most_streamed_spotify_2025.csv"

# ============================================================================
# THEME / CSS  —  dark "studio" theme with a Spotify-green signature accent
# ============================================================================
ACCENT = "#1ED760"       # signature accent — vibrant streaming green
ACCENT_2 = "#2DD4BF"     # secondary accent — teal, used for contrast in charts
WARN = "#FF6B6B"         # coral, used sparingly for negative/attention states
BG = "#0E1117"           # app background
CARD_BG = "#171B22"      # card surface
CARD_BORDER = "#242933"
TEXT_MUTED = "#9AA4B2"

CHART_TEMPLATE = "plotly_dark"
COLOR_THEMES = {
    "Signature Green": [ACCENT, ACCENT_2, "#F5C451", "#A78BFA", "#FF6B6B", "#60A5FA"],
    "Sunset": ["#FF6B6B", "#F5C451", "#FF9F1C", "#FF477E", "#7209B7", "#3A0CA3"],
    "Ocean": ["#2DD4BF", "#60A5FA", "#1ED760", "#38BDF8", "#818CF8", "#0EA5E9"],
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"]  {{
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Sora', sans-serif !important;
        letter-spacing: -0.01em;
    }}

    /* ---- top app header ---- */
    .app-hero {{
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(30,215,96,0.15) 0%, rgba(23,27,34,0.4) 60%);
        border: 1px solid {CARD_BORDER};
        margin-bottom: 1.4rem;
    }}
    .app-hero h1 {{
        margin: 0;
        font-size: 1.9rem;
        color: #F5F7FA;
    }}
    .app-hero p {{
        margin: 0.3rem 0 0 0;
        color: {TEXT_MUTED};
        font-size: 0.95rem;
    }}
    .eyebrow {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {ACCENT};
        background: rgba(30,215,96,0.12);
        border: 1px solid rgba(30,215,96,0.3);
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        margin-bottom: 0.6rem;
    }}

    /* ---- KPI cards ---- */
    .kpi-card {{
        background: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 1rem 1.1rem;
        height: 100%;
    }}
    .kpi-label {{
        font-size: 0.78rem;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }}
    .kpi-value {{
        font-family: 'Sora', sans-serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: #F5F7FA;
    }}
    .kpi-sub {{
        font-size: 0.78rem;
        color: {ACCENT};
        margin-top: 0.15rem;
    }}

    /* ---- section titles ---- */
    .section-title {{
        font-family: 'Sora', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #F5F7FA;
        margin: 0.2rem 0 0.6rem 0;
        border-left: 3px solid {ACCENT};
        padding-left: 0.6rem;
    }}

    /* ---- sidebar ---- */
    section[data-testid="stSidebar"] {{
        border-right: 1px solid {CARD_BORDER};
    }}

    /* ---- dataframe corners ---- */
    div[data-testid="stDataFrame"] {{
        border-radius: 10px;
        overflow: hidden;
    }}

    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


def kpi_card(label, value, sub=None):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def human_number(n):
    n = float(n)
    for unit, div in [("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if abs(n) >= div:
            return f"{n / div:.2f}{unit}"
    return f"{n:.0f}"


# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data
def load_data(path) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")

    df.columns = [c.strip() for c in df.columns]
    numeric_cols = ["rank", "billed_artist_count", "spotify_streams_total",
                     "daily_streams", "daily_streams_rank", "daily_stream_share_pct",
                     "wrapped_global_top10_rank"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    if "is_collaboration" in df.columns:
        df["is_collaboration"] = df["is_collaboration"].astype(bool)

    df["track_type"] = np.where(df["is_collaboration"], "Collaboration", "Solo")
    return df


data_path = DATA_FILE if os.path.exists(DATA_FILE) else None

if data_path is None:
    st.markdown('<div class="app-hero"><span class="eyebrow">Setup needed</span>'
                '<h1>🎧 Spotify 2025 Streaming Dashboard</h1>'
                f'<p>Couldn\'t find <code>{DATA_FILE}</code> next to this script. '
                'Upload it below to continue.</p></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload most_streamed_spotify_2025.csv", type=["csv"])
    if uploaded is None:
        st.stop()
    raw_df = load_data(uploaded)
else:
    raw_df = load_data(data_path)

# ============================================================================
# SIDEBAR — FILTERS & DISPLAY CONTROLS
# ============================================================================
with st.sidebar:
    st.markdown("## 🎧 Control Panel")
    st.caption("Every chart on the right reacts live to what you set here.")

    st.markdown("### 🔍 Search")
    search_term = st.text_input("Track or artist contains…", value="", placeholder="e.g. Bad Bunny")

    st.markdown("### 🎚️ Filters")
    artist_options = sorted(raw_df["artist"].unique())
    artist_filter = st.multiselect("Artist(s)", options=artist_options, default=[],
                                    help="Leave empty to include every artist")

    track_type = st.radio("Track type", ["All", "Solo", "Collaboration"], horizontal=True)

    billed_options = sorted(raw_df["billed_artist_count"].dropna().unique().astype(int).tolist())
    billed_filter = st.multiselect("Billed artist count", options=billed_options, default=[])

    rank_min, rank_max = int(raw_df["rank"].min()), int(raw_df["rank"].max())
    rank_range = st.slider("Chart rank range", rank_min, rank_max, (rank_min, rank_max))

    streams_min, streams_max = float(raw_df["spotify_streams_total"].min()), float(raw_df["spotify_streams_total"].max())
    streams_range = st.slider("Total streams range", streams_min, streams_max,
                               (streams_min, streams_max), format="%.0f")

    daily_min, daily_max = float(raw_df["daily_streams"].min()), float(raw_df["daily_streams"].max())
    daily_range = st.slider("Daily streams range", daily_min, daily_max,
                             (daily_min, daily_max), format="%.0f")

    st.markdown("### 🎛️ Display options")
    top_n = st.slider("Top N (used in rankings & charts)", 5, 50, 15)
    metric_choice = st.selectbox(
        "Primary metric",
        options=["spotify_streams_total", "daily_streams", "daily_stream_share_pct"],
        format_func=lambda x: {
            "spotify_streams_total": "Total Streams",
            "daily_streams": "Daily Streams",
            "daily_stream_share_pct": "Daily Stream Share %",
        }[x],
    )
    color_theme_name = st.selectbox("Chart color theme", options=list(COLOR_THEMES.keys()))
    color_seq = COLOR_THEMES[color_theme_name]
    show_raw_table = st.checkbox("Show raw data table in Data Explorer", value=True)

    if st.button("↺ Reset all filters"):
        st.rerun()

# ============================================================================
# APPLY FILTERS  (single filtered dataframe feeds every chart -> "dependent")
# ============================================================================
df = raw_df.copy()

if search_term.strip():
    term = search_term.strip().lower()
    df = df[df["track"].str.lower().str.contains(term) | df["artist"].str.lower().str.contains(term)]

if artist_filter:
    df = df[df["artist"].isin(artist_filter)]

if track_type != "All":
    df = df[df["track_type"] == track_type]

if billed_filter:
    df = df[df["billed_artist_count"].isin(billed_filter)]

df = df[df["rank"].between(rank_range[0], rank_range[1])]
df = df[df["spotify_streams_total"].between(streams_range[0], streams_range[1])]
df = df[df["daily_streams"].between(daily_range[0], daily_range[1])]

metric_label = {
    "spotify_streams_total": "Total Streams",
    "daily_streams": "Daily Streams",
    "daily_stream_share_pct": "Daily Stream Share %",
}[metric_choice]

# ============================================================================
# HERO HEADER
# ============================================================================
st.markdown(f"""
<div class="app-hero">
    <span class="eyebrow">2025 · Global Streaming Data</span>
    <h1>🎧 Most Streamed Spotify Tracks — 2025</h1>
    <p>{len(df):,} of {len(raw_df):,} tracks match your current filters · exploring
       <b style="color:{ACCENT}">{metric_label}</b> as the primary metric</p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("No tracks match the current filters. Try widening them from the sidebar.")
    st.stop()

# ============================================================================
# KPI CARD ROW
# ============================================================================
k1, k2, k3, k4, k5 = st.columns(5)
artist_sum = df.groupby("artist")["spotify_streams_total"].sum()
top_artist_row = artist_sum.idxmax()
top_artist_val = artist_sum.max()
collab_pct = 100 * df["is_collaboration"].mean()

with k1:
    kpi_card("Tracks in view", f"{len(df):,}", f"of {len(raw_df):,} total")
with k2:
    kpi_card("Unique artists", f"{df['artist'].nunique():,}")
with k3:
    kpi_card("Total streams (sum)", human_number(df["spotify_streams_total"].sum()))
with k4:
    kpi_card("Avg daily streams", human_number(df["daily_streams"].mean()))
with k5:
    kpi_card("Top artist here", top_artist_row, human_number(top_artist_val) + " streams")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================
tab_overview, tab_artists, tab_tracks, tab_analytics, tab_data = st.tabs(
    ["🏠 Overview", "🎤 Artists", "🎵 Tracks", "🔬 Analytics", "🗂️ Data Explorer"]
)

# ----------------------------------------------------------------------------
# TAB 1: OVERVIEW
# ----------------------------------------------------------------------------
with tab_overview:
    c1, c2 = st.columns((3, 2))

    with c1:
        section_title(f"Top {top_n} tracks by {metric_label}")
        top_tracks = df.nlargest(top_n, metric_choice).sort_values(metric_choice)
        fig = px.bar(
            top_tracks, x=metric_choice, y="track", orientation="h",
            color="track_type", color_discrete_sequence=color_seq,
            hover_data={"artist": True, metric_choice: ":,.0f"},
            labels={metric_choice: metric_label, "track": ""},
            template=CHART_TEMPLATE, height=520,
        )
        fig.update_layout(legend_title="", margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_title("Solo vs. Collaboration")
        donut_data = df["track_type"].value_counts().reset_index()
        donut_data.columns = ["Type", "Count"]
        fig = px.pie(donut_data, names="Type", values="Count", hole=0.55,
                     color_discrete_sequence=color_seq, template=CHART_TEMPLATE, height=250)
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        section_title(f"{metric_label} distribution")
        fig = px.histogram(df, x=metric_choice, nbins=30, color_discrete_sequence=[ACCENT],
                            template=CHART_TEMPLATE, height=250)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), bargap=0.05,
                           xaxis_title=metric_label, yaxis_title="Tracks")
        st.plotly_chart(fig, use_container_width=True)

    section_title("Stream volume by chart position (decay curve)")
    st.caption("Shows how quickly streaming volume falls off as chart rank increases — "
               "a classic long-tail pattern.")
    rank_trend = df.sort_values("rank")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rank_trend["rank"], y=rank_trend[metric_choice],
        mode="lines", line=dict(color=ACCENT, width=2),
        fill="tozeroy", fillcolor="rgba(30,215,96,0.12)",
        name=metric_label,
        hovertext=rank_trend["track"] + " — " + rank_trend["artist"],
        hoverinfo="text+y",
    ))
    fig.update_layout(template=CHART_TEMPLATE, height=380,
                       xaxis_title="Chart rank", yaxis_title=metric_label,
                       margin=dict(l=0, r=10, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # Wrapped Top 10 callout, only if any rows in the filtered set have it
    wrapped = df[df["wrapped_global_top10_rank"].notna()].sort_values("wrapped_global_top10_rank")
    if not wrapped.empty:
        section_title("🏆 Spotify Wrapped 2025 — Global Top 10 appearances in this view")
        st.dataframe(
            wrapped[["wrapped_global_top10_rank", "track", "artist", "spotify_streams_total"]]
            .rename(columns={"wrapped_global_top10_rank": "Wrapped Rank", "track": "Track",
                              "artist": "Artist", "spotify_streams_total": "Total Streams"}),
            use_container_width=True, hide_index=True,
        )

# ----------------------------------------------------------------------------
# TAB 2: ARTISTS
# ----------------------------------------------------------------------------
with tab_artists:
    artist_agg = (
        df.groupby("artist")
        .agg(
            total_streams=("spotify_streams_total", "sum"),
            avg_daily_streams=("daily_streams", "mean"),
            avg_daily_share=("daily_stream_share_pct", "mean"),
            track_count=("track", "count"),
            collabs=("is_collaboration", "sum"),
        )
        .reset_index()
        .sort_values("total_streams", ascending=False)
    )

    c1, c2 = st.columns((3, 2))
    with c1:
        section_title(f"Top {top_n} artists by total streams")
        top_artists = artist_agg.head(top_n).sort_values("total_streams")
        fig = px.bar(
            top_artists, x="total_streams", y="artist", orientation="h",
            color="track_count", color_continuous_scale=[ACCENT_2, ACCENT],
            labels={"total_streams": "Total Streams", "artist": "", "track_count": "# Tracks"},
            template=CHART_TEMPLATE, height=520,
        )
        fig.update_layout(margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_title("Artist streaming share (treemap)")
        tree_data = artist_agg.head(max(top_n, 10))
        fig = px.treemap(
            tree_data, path=["artist"], values="total_streams",
            color="total_streams", color_continuous_scale=[CARD_BG, ACCENT],
            template=CHART_TEMPLATE, height=520,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    section_title("Artist leaderboard")
    st.dataframe(
        artist_agg.rename(columns={
            "artist": "Artist", "total_streams": "Total Streams",
            "avg_daily_streams": "Avg Daily Streams", "avg_daily_share": "Avg Daily Share %",
            "track_count": "Tracks", "collabs": "Collaborations",
        }),
        use_container_width=True, hide_index=True,
        column_config={
            "Total Streams": st.column_config.ProgressColumn(
                "Total Streams", format="%.0f",
                min_value=0, max_value=float(artist_agg["total_streams"].max())),
        },
    )

# ----------------------------------------------------------------------------
# TAB 3: TRACKS
# ----------------------------------------------------------------------------
with tab_tracks:
    section_title("Total vs. daily streams (bubble = billed artist count)")
    fig = px.scatter(
        df, x="spotify_streams_total", y="daily_streams",
        size="billed_artist_count", color="track_type",
        color_discrete_sequence=color_seq,
        hover_name="track", hover_data={"artist": True, "daily_stream_share_pct": ":.2%"},
        labels={"spotify_streams_total": "Total Streams", "daily_streams": "Daily Streams"},
        template=CHART_TEMPLATE, height=480,
    )
    fig.update_layout(legend_title="", margin=dict(l=0, r=10, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        section_title(f"Top {top_n} tracks by daily stream share")
        top_share = df.nlargest(top_n, "daily_stream_share_pct").sort_values("daily_stream_share_pct")
        fig = px.bar(
            top_share, x="daily_stream_share_pct", y="track", orientation="h",
            color_discrete_sequence=[ACCENT_2],
            labels={"daily_stream_share_pct": "Daily Stream Share %", "track": ""},
            template=CHART_TEMPLATE, height=460,
        )
        fig.update_layout(margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_title("Daily streams by billed artist count")
        fig = px.box(
            df, x="billed_artist_count", y="daily_streams", color="billed_artist_count",
            color_discrete_sequence=color_seq,
            labels={"billed_artist_count": "Billed Artist Count", "daily_streams": "Daily Streams"},
            template=CHART_TEMPLATE, height=460,
        )
        fig.update_layout(showlegend=False, margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    section_title("Track-level table")
    st.dataframe(
        df[["rank", "track", "artist", "track_type", "billed_artist_count",
            "spotify_streams_total", "daily_streams", "daily_streams_rank",
            "daily_stream_share_pct"]]
        .rename(columns={
            "rank": "Rank", "track": "Track", "artist": "Artist", "track_type": "Type",
            "billed_artist_count": "Billed Artists", "spotify_streams_total": "Total Streams",
            "daily_streams": "Daily Streams", "daily_streams_rank": "Daily Rank",
            "daily_stream_share_pct": "Daily Share %",
        })
        .sort_values("Rank"),
        use_container_width=True, hide_index=True, height=420,
    )

# ----------------------------------------------------------------------------
# TAB 4: ANALYTICS
# ----------------------------------------------------------------------------
with tab_analytics:
    numeric_cols = ["rank", "billed_artist_count", "spotify_streams_total",
                     "daily_streams", "daily_streams_rank", "daily_stream_share_pct"]

    c1, c2 = st.columns(2)
    with c1:
        section_title("Correlation between numeric fields")
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                         color_continuous_scale="RdYlGn",
                         template=CHART_TEMPLATE, height=420)
        fig.update_layout(margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_title(f"{metric_label}: Solo vs. Collaboration")
        fig = px.violin(
            df, x="track_type", y=metric_choice, color="track_type", box=True, points="all",
            color_discrete_sequence=color_seq,
            labels={metric_choice: metric_label, "track_type": ""},
            template=CHART_TEMPLATE, height=420,
        )
        fig.update_layout(showlegend=False, margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    section_title("Chart rank vs. daily rank consistency")
    st.caption("Points near the diagonal line mean a track's overall chart position and "
               "its daily-streaming rank agree closely.")
    fig = px.scatter(
        df, x="rank", y="daily_streams_rank", color="track_type",
        color_discrete_sequence=color_seq, hover_name="track",
        labels={"rank": "Chart Rank", "daily_streams_rank": "Daily Streams Rank"},
        template=CHART_TEMPLATE, height=440,
    )
    max_axis = max(df["rank"].max(), df["daily_streams_rank"].max())
    fig.add_trace(go.Scatter(x=[0, max_axis], y=[0, max_axis], mode="lines",
                              line=dict(color=TEXT_MUTED, dash="dash"), name="Perfect agreement"))
    fig.update_layout(legend_title="", margin=dict(l=0, r=10, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# TAB 5: DATA EXPLORER
# ----------------------------------------------------------------------------
with tab_data:
    section_title("Filtered dataset")
    st.caption("This table always reflects every filter currently set in the sidebar.")

    if show_raw_table:
        st.dataframe(df.reset_index(drop=True), use_container_width=True, height=480)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=csv_bytes,
        file_name="spotify_2025_filtered.csv",
        mime="text/csv",
    )

    with st.expander("📈 Quick summary statistics"):
        numeric_cols_view = ["rank", "billed_artist_count", "spotify_streams_total",
                              "daily_streams", "daily_streams_rank", "daily_stream_share_pct"]
        st.dataframe(df[numeric_cols_view].describe().T, use_container_width=True)