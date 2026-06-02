# ============================================================
#  Netflix Content Visualization — EDA & Visualizations
#  Tools : Pandas · Matplotlib · Seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ── Palette & global style ──────────────────────────────────
NETFLIX_RED   = "#E50914"
NETFLIX_BLACK = "#141414"
NETFLIX_DARK  = "#221F1F"
NETFLIX_GREY  = "#B3B3B3"
ACCENT1       = "#F5F5F1"          # off-white
ACCENT2       = "#831010"          # deep red
ACCENT3       = "#FF6B6B"          # coral

PALETTE = [NETFLIX_RED, "#FF6B6B", "#FF9F43", "#54A0FF",
           "#5F27CD", "#00D2D3", "#1DD1A1", "#FECA57",
           "#C8D6E5", "#576574"]

plt.rcParams.update({
    "figure.facecolor": NETFLIX_BLACK,
    "axes.facecolor":   NETFLIX_DARK,
    "axes.edgecolor":   NETFLIX_GREY,
    "axes.labelcolor":  ACCENT1,
    "axes.titlecolor":  ACCENT1,
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
    "xtick.color":      NETFLIX_GREY,
    "ytick.color":      NETFLIX_GREY,
    "text.color":       ACCENT1,
    "grid.color":       "#2E2B2B",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.6,
    "legend.facecolor": NETFLIX_DARK,
    "legend.edgecolor": NETFLIX_GREY,
    "font.family":      "DejaVu Sans",
    "savefig.facecolor": NETFLIX_BLACK,
    "savefig.bbox":     "tight",
    "savefig.dpi":      150,
})

OUT = "/home/claude/netflix_project/visualizations"

# ════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN DATA
# ════════════════════════════════════════════════════════════
print("=" * 55)
print("  Netflix Content Visualization — EDA")
print("=" * 55)

df = pd.read_csv("/home/claude/netflix_project/data/netflix_titles.csv")

print(f"\n📦 Raw Shape       : {df.shape}")
print(f"🔑 Columns         : {list(df.columns)}")
print(f"\n🕳  Missing Values :\n{df.isnull().sum()}")

# --- Clean date_added → year_added
df["date_added"]  = df["date_added"].astype(str).str.strip()
df["year_added"]  = df["date_added"].str.extract(r"(\d{4})").astype(float)

# --- Duration split
movies = df[df["type"] == "Movie"].copy()
shows  = df[df["type"] == "TV Show"].copy()
movies["duration_min"]     = movies["duration"].str.extract(r"(\d+)").astype(float)
shows["duration_seasons"]  = shows["duration"].str.extract(r"(\d+)").astype(float)

print(f"\n✅ Movies  : {len(movies):,}")
print(f"✅ TV Shows: {len(shows):,}")
print(f"\nData cleaned successfully!")


# ════════════════════════════════════════════════════════════
# HELPER
# ════════════════════════════════════════════════════════════
def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)
    print(f"   ✔  saved → {name}.png")


# ════════════════════════════════════════════════════════════
# 2. OVERVIEW DASHBOARD  (2 × 2)
# ════════════════════════════════════════════════════════════
print("\n[1/7] Overview Dashboard …")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Netflix Content Overview", fontsize=20, fontweight="bold",
             color=NETFLIX_RED, y=0.97)

# ── 2a. Movie vs TV Show (donut) ────────────────────────────
ax = axes[0, 0]
counts = df["type"].value_counts()
wedge_props = dict(width=0.5, edgecolor=NETFLIX_BLACK, linewidth=2)
wedges, texts, autotexts = ax.pie(
    counts.values, labels=counts.index, autopct="%1.1f%%",
    colors=[NETFLIX_RED, "#54A0FF"], wedgeprops=wedge_props,
    startangle=90, textprops={"color": ACCENT1, "fontsize": 12})
for at in autotexts:
    at.set_fontsize(11); at.set_fontweight("bold"); at.set_color(NETFLIX_BLACK)
ax.set_title("Content Type Distribution", pad=15)

# ── 2b. Content added per year (bar) ────────────────────────
ax = axes[0, 1]
yearly = df["year_added"].dropna().value_counts().sort_index()
yearly = yearly[yearly.index >= 2010]
bars = ax.bar(yearly.index.astype(int), yearly.values,
              color=NETFLIX_RED, edgecolor=NETFLIX_BLACK, linewidth=0.8)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 5, str(int(h)),
            ha="center", va="bottom", fontsize=8, color=NETFLIX_GREY)
ax.set_title("Content Added Per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Titles")
ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 2c. Top 10 countries ────────────────────────────────────
ax = axes[1, 0]
top_countries = df["country"].value_counts().head(10)
colors_c = [NETFLIX_RED if i == 0 else PALETTE[i % len(PALETTE)]
            for i in range(len(top_countries))]
bars = ax.barh(top_countries.index[::-1], top_countries.values[::-1],
               color=colors_c[::-1], edgecolor=NETFLIX_BLACK, linewidth=0.6)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 8, bar.get_y() + bar.get_height() / 2, str(int(w)),
            va="center", fontsize=8, color=NETFLIX_GREY)
ax.set_title("Top 10 Countries by Content")
ax.set_xlabel("Number of Titles")
ax.xaxis.grid(True); ax.set_axisbelow(True)

# ── 2d. Rating distribution ────────────────────────────────
ax = axes[1, 1]
ratings_order = ["G", "PG", "PG-13", "R", "TV-Y", "TV-Y7",
                 "TV-G", "TV-PG", "TV-14", "TV-MA", "NR"]
rating_counts = df["rating"].value_counts().reindex(ratings_order, fill_value=0)
bars = ax.bar(rating_counts.index, rating_counts.values,
              color=PALETTE[:len(rating_counts)],
              edgecolor=NETFLIX_BLACK, linewidth=0.8)
for bar in bars:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, h + 3, str(int(h)),
                ha="center", va="bottom", fontsize=7.5, color=NETFLIX_GREY)
ax.set_title("Content Ratings Distribution")
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Titles")
ax.yaxis.grid(True); ax.set_axisbelow(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, "01_overview_dashboard")


# ════════════════════════════════════════════════════════════
# 3. GENRE ANALYSIS
# ════════════════════════════════════════════════════════════
print("[2/7] Genre Analysis …")

# Explode multi-genre column
all_genres = []
for row in df["listed_in"].dropna():
    all_genres.extend([g.strip() for g in row.split(",")])
genre_counts = pd.Series(Counter(all_genres)).sort_values(ascending=False).head(15)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Genre Analysis", fontsize=20, fontweight="bold",
             color=NETFLIX_RED, y=1.01)

# Top genres — horizontal bar
ax = axes[0]
colors_g = [NETFLIX_RED if i == 0 else PALETTE[i % len(PALETTE)]
            for i in range(len(genre_counts))]
ax.barh(genre_counts.index[::-1], genre_counts.values[::-1],
        color=colors_g[::-1], edgecolor=NETFLIX_BLACK, linewidth=0.6, height=0.7)
for i, (val, label) in enumerate(zip(genre_counts.values[::-1], genre_counts.index[::-1])):
    ax.text(val + 5, i, str(val), va="center", fontsize=9, color=NETFLIX_GREY)
ax.set_title("Top 15 Genres on Netflix")
ax.set_xlabel("Number of Titles")
ax.xaxis.grid(True); ax.set_axisbelow(True)

# Genre split by type
ax = axes[1]
top10_genres = genre_counts.head(10).index.tolist()
movie_genre  = []
show_genre   = []
for g in top10_genres:
    m = movies["listed_in"].dropna().str.contains(g).sum()
    s = shows["listed_in"].dropna().str.contains(g).sum()
    movie_genre.append(m)
    show_genre.append(s)

x = np.arange(len(top10_genres))
w = 0.4
b1 = ax.bar(x - w / 2, movie_genre, w, label="Movie",   color=NETFLIX_RED,  edgecolor=NETFLIX_BLACK)
b2 = ax.bar(x + w / 2, show_genre,  w, label="TV Show", color="#54A0FF", edgecolor=NETFLIX_BLACK)
ax.set_xticks(x)
ax.set_xticklabels([g[:16] for g in top10_genres], rotation=45, ha="right", fontsize=8)
ax.set_title("Movies vs TV Shows per Genre (Top 10)")
ax.set_ylabel("Number of Titles")
ax.legend()
ax.yaxis.grid(True); ax.set_axisbelow(True)

plt.tight_layout()
save(fig, "02_genre_analysis")


# ════════════════════════════════════════════════════════════
# 4. CONTENT TRENDS OVER TIME
# ════════════════════════════════════════════════════════════
print("[3/7] Content Trends …")

fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Content Trends Over Time", fontsize=20, fontweight="bold",
             color=NETFLIX_RED, y=0.97)

# ── 4a. Area chart: Movies vs TV Shows added per year ───────
ax = axes[0, 0]
trend = df.dropna(subset=["year_added"])
trend = trend[trend["year_added"] >= 2010]
pivot = trend.groupby(["year_added", "type"]).size().unstack(fill_value=0)
years_range = pivot.index.astype(int)
if "Movie" in pivot.columns:
    ax.fill_between(years_range, pivot["Movie"],   alpha=0.7, color=NETFLIX_RED, label="Movie")
    ax.plot(years_range, pivot["Movie"], color=NETFLIX_RED, lw=2)
if "TV Show" in pivot.columns:
    ax.fill_between(years_range, pivot["TV Show"], alpha=0.5, color="#54A0FF", label="TV Show")
    ax.plot(years_range, pivot["TV Show"], color="#54A0FF", lw=2)
ax.set_title("Movies vs TV Shows Added Per Year")
ax.set_xlabel("Year"); ax.set_ylabel("Titles Added")
ax.legend(); ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 4b. Release year histogram ───────────────────────────────
ax = axes[0, 1]
release_data = df[df["release_year"] >= 1990]["release_year"]
ax.hist(release_data, bins=30, color=NETFLIX_RED, edgecolor=NETFLIX_BLACK,
        linewidth=0.5, alpha=0.9)
ax.set_title("Distribution of Release Years")
ax.set_xlabel("Release Year"); ax.set_ylabel("Number of Titles")
ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 4c. Top genres trend over time (line) ───────────────────
ax = axes[1, 0]
top5 = genre_counts.head(5).index.tolist()
trend2 = df.dropna(subset=["year_added", "listed_in"])
trend2 = trend2[trend2["year_added"] >= 2014]
for i, genre in enumerate(top5):
    mask  = trend2["listed_in"].str.contains(genre, na=False)
    g_yr  = trend2[mask].groupby("year_added").size()
    ax.plot(g_yr.index.astype(int), g_yr.values,
            marker="o", markersize=4, lw=2,
            color=PALETTE[i], label=genre)
ax.set_title("Top 5 Genre Trends (2014 → 2021)")
ax.set_xlabel("Year"); ax.set_ylabel("Titles Added")
ax.legend(fontsize=8, loc="upper left")
ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 4d. Month-wise additions heatmap ─────────────────────────
ax = axes[1, 1]
months_map = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
              "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
df["month_added"] = df["date_added"].str.extract(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)"
)[0].map(months_map)
heatmap_data = df.dropna(subset=["year_added","month_added"])
heatmap_data = heatmap_data[heatmap_data["year_added"] >= 2015]
pivot_h = heatmap_data.groupby(["year_added","month_added"]).size().unstack(fill_value=0)
pivot_h.index = pivot_h.index.astype(int)
pivot_h.columns = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"][:len(pivot_h.columns)]
sns.heatmap(pivot_h, annot=True, fmt="d", cmap="Reds",
            linewidths=0.3, linecolor=NETFLIX_BLACK,
            annot_kws={"size": 8}, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title("Monthly Content Additions Heatmap (2015–2021)")
ax.set_xlabel("Month"); ax.set_ylabel("Year")

plt.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, "03_content_trends")


# ════════════════════════════════════════════════════════════
# 5. RATINGS DEEP DIVE
# ════════════════════════════════════════════════════════════
print("[4/7] Ratings Deep Dive …")

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Ratings Deep Dive", fontsize=20, fontweight="bold",
             color=NETFLIX_RED, y=1.01)

# ── 5a. Overall ratings (pie) ────────────────────────────────
ax = axes[0]
rc = df["rating"].value_counts()
explode = [0.05] * len(rc)
wedges, texts, autotexts = ax.pie(
    rc.values, labels=rc.index, autopct="%1.1f%%",
    colors=PALETTE[:len(rc)], explode=explode,
    startangle=140, textprops={"color": ACCENT1, "fontsize": 9},
    wedgeprops={"edgecolor": NETFLIX_BLACK, "linewidth": 1.5})
for at in autotexts:
    at.set_fontsize(8); at.set_color(NETFLIX_BLACK); at.set_fontweight("bold")
ax.set_title("Overall Ratings Distribution")

# ── 5b. Rating by type (grouped bar) ─────────────────────────
ax = axes[1]
top_ratings = df["rating"].value_counts().head(8).index.tolist()
movie_r = [movies[movies["rating"] == r].shape[0] for r in top_ratings]
show_r  = [shows[shows["rating"] == r].shape[0]  for r in top_ratings]
x = np.arange(len(top_ratings))
w = 0.4
ax.bar(x - w/2, movie_r, w, label="Movie",   color=NETFLIX_RED,  edgecolor=NETFLIX_BLACK)
ax.bar(x + w/2, show_r,  w, label="TV Show", color="#54A0FF", edgecolor=NETFLIX_BLACK)
ax.set_xticks(x); ax.set_xticklabels(top_ratings, fontsize=10)
ax.set_title("Rating Split: Movies vs TV Shows")
ax.set_ylabel("Number of Titles")
ax.legend(); ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 5c. Stacked bar: ratings trend over years ─────────────────
ax = axes[2]
top4_ratings = df["rating"].value_counts().head(4).index.tolist()
trend_r = df.dropna(subset=["year_added"])
trend_r = trend_r[trend_r["year_added"] >= 2015]
pivot_r = trend_r[trend_r["rating"].isin(top4_ratings)].groupby(
    ["year_added","rating"]).size().unstack(fill_value=0)
pivot_r.index = pivot_r.index.astype(int)
bottom = np.zeros(len(pivot_r))
for i, col in enumerate(top4_ratings):
    if col in pivot_r.columns:
        ax.bar(pivot_r.index, pivot_r[col], bottom=bottom,
               label=col, color=PALETTE[i], edgecolor=NETFLIX_BLACK, linewidth=0.5)
        bottom += pivot_r[col].values
ax.set_title("Rating Trends Over Years (Top 4)")
ax.set_xlabel("Year"); ax.set_ylabel("Number of Titles")
ax.legend(fontsize=9); ax.yaxis.grid(True); ax.set_axisbelow(True)

plt.tight_layout()
save(fig, "04_ratings_deep_dive")


# ════════════════════════════════════════════════════════════
# 6. COUNTRY-WISE ANALYSIS
# ════════════════════════════════════════════════════════════
print("[5/7] Country Analysis …")

fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Country-wise Content Analysis", fontsize=20, fontweight="bold",
             color=NETFLIX_RED, y=1.01)

# ── 6a. Top 15 countries — bubble chart ─────────────────────
ax = axes[0]
top15 = df["country"].value_counts().head(15)
y_pos = range(len(top15))
scatter = ax.scatter(top15.values, list(y_pos),
                     s=top15.values / top15.max() * 3000,
                     c=[PALETTE[i % len(PALETTE)] for i in range(len(top15))],
                     alpha=0.85, edgecolors=NETFLIX_BLACK, linewidths=1.5)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(top15.index, fontsize=10)
for i, (val, y) in enumerate(zip(top15.values, y_pos)):
    ax.text(val + 5, y, str(val), va="center", fontsize=9, color=NETFLIX_GREY)
ax.set_title("Top 15 Countries — Content Volume (Bubble)")
ax.set_xlabel("Number of Titles")
ax.xaxis.grid(True); ax.set_axisbelow(True)

# ── 6b. Content type ratio per top-10 country ────────────────
ax = axes[1]
top10_c = df["country"].value_counts().head(10).index.tolist()
movie_pct = []
show_pct  = []
for c in top10_c:
    sub  = df[df["country"] == c]
    tot  = len(sub)
    mp   = sub[sub["type"] == "Movie"].shape[0] / tot * 100
    sp   = sub[sub["type"] == "TV Show"].shape[0] / tot * 100
    movie_pct.append(mp); show_pct.append(sp)

x = np.arange(len(top10_c))
b1 = ax.barh(x, movie_pct, color=NETFLIX_RED, label="Movie", edgecolor=NETFLIX_BLACK)
b2 = ax.barh(x, show_pct, left=movie_pct, color="#54A0FF", label="TV Show", edgecolor=NETFLIX_BLACK)
ax.set_yticks(x); ax.set_yticklabels(top10_c, fontsize=10)
ax.set_xlabel("Percentage (%)")
ax.set_title("Movie vs TV Show % per Country (Top 10)")
ax.legend(); ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.axvline(50, color=NETFLIX_GREY, lw=1, linestyle="--", alpha=0.5)

plt.tight_layout()
save(fig, "05_country_analysis")


# ════════════════════════════════════════════════════════════
# 7. DURATION ANALYSIS
# ════════════════════════════════════════════════════════════
print("[6/7] Duration Analysis …")

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Duration Analysis", fontsize=20, fontweight="bold",
             color=NETFLIX_RED, y=1.01)

# ── 7a. Movie runtime distribution ────────────────────────────
ax = axes[0]
m_dur = movies["duration_min"].dropna()
ax.hist(m_dur, bins=40, color=NETFLIX_RED, edgecolor=NETFLIX_BLACK,
        linewidth=0.4, alpha=0.9)
ax.axvline(m_dur.mean(), color="#FECA57", lw=2, linestyle="--",
           label=f"Mean: {m_dur.mean():.0f} min")
ax.axvline(m_dur.median(), color="#00D2D3", lw=2, linestyle="--",
           label=f"Median: {m_dur.median():.0f} min")
ax.set_title("Movie Runtime Distribution")
ax.set_xlabel("Duration (minutes)"); ax.set_ylabel("Count")
ax.legend(); ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 7b. TV Show seasons distribution ──────────────────────────
ax = axes[1]
s_seas = shows["duration_seasons"].dropna().value_counts().sort_index()
ax.bar(s_seas.index.astype(int), s_seas.values,
       color=["#54A0FF" if i == 0 else PALETTE[(i+1) % len(PALETTE)] for i in range(len(s_seas))],
       edgecolor=NETFLIX_BLACK, linewidth=0.8)
for i, (x_val, y_val) in enumerate(zip(s_seas.index.astype(int), s_seas.values)):
    ax.text(x_val, y_val + 1, str(int(y_val)), ha="center", fontsize=9, color=NETFLIX_GREY)
ax.set_title("TV Show Season Count Distribution")
ax.set_xlabel("Number of Seasons"); ax.set_ylabel("Number of Shows")
ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── 7c. Movie duration by rating (violin) ─────────────────────
ax = axes[2]
top5_r  = movies["rating"].value_counts().head(5).index.tolist()
plot_df = movies[movies["rating"].isin(top5_r)][["rating","duration_min"]].dropna()
parts = ax.violinplot(
    [plot_df[plot_df["rating"] == r]["duration_min"].values for r in top5_r],
    positions=range(len(top5_r)), showmedians=True, showextrema=True)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(PALETTE[i]); pc.set_alpha(0.75)
parts["cmedians"].set_color("#FECA57"); parts["cmedians"].set_linewidth(2)
parts["cmaxes"].set_color(NETFLIX_GREY); parts["cmins"].set_color(NETFLIX_GREY)
parts["cbars"].set_color(NETFLIX_GREY)
ax.set_xticks(range(len(top5_r))); ax.set_xticklabels(top5_r)
ax.set_title("Movie Duration by Rating (Violin)")
ax.set_ylabel("Duration (minutes)")
ax.yaxis.grid(True); ax.set_axisbelow(True)

plt.tight_layout()
save(fig, "06_duration_analysis")


# ════════════════════════════════════════════════════════════
# 8. COMPREHENSIVE SUMMARY DASHBOARD
# ════════════════════════════════════════════════════════════
print("[7/7] Summary Dashboard …")

fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor(NETFLIX_BLACK)
fig.suptitle("Netflix Content — Comprehensive Summary Dashboard",
             fontsize=22, fontweight="bold", color=NETFLIX_RED, y=0.98)

# Grid spec: 3 rows × 4 cols
gs = fig.add_gridspec(3, 4, hspace=0.45, wspace=0.4)

# ── KPI Cards (row 0) ────────────────────────────────────────
kpi_data = [
    ("Total Titles",   f"{len(df):,}",          NETFLIX_RED),
    ("Movies",         f"{len(movies):,}",       "#FF6B6B"),
    ("TV Shows",       f"{len(shows):,}",        "#54A0FF"),
    ("Countries",      f"{df['country'].nunique()}",  "#FECA57"),
]
for i, (label, value, color) in enumerate(kpi_data):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(color + "33")          # transparent tint
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.05, 0.05), 0.90, 0.90,
        boxstyle="round,pad=0.02",
        facecolor=color + "22",
        edgecolor=color, linewidth=2,
        transform=ax.transAxes, clip_on=False))
    ax.text(0.5, 0.62, value,  ha="center", va="center",
            transform=ax.transAxes, fontsize=26, fontweight="bold", color=color)
    ax.text(0.5, 0.30, label, ha="center", va="center",
            transform=ax.transAxes, fontsize=11, color=NETFLIX_GREY)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")

# ── Top genres (row 1, col 0–1) ─────────────────────────────
ax = fig.add_subplot(gs[1, :2])
top8 = genre_counts.head(8)
bars = ax.barh(top8.index[::-1], top8.values[::-1],
               color=[PALETTE[i % len(PALETTE)] for i in range(len(top8))],
               edgecolor=NETFLIX_BLACK, linewidth=0.6, height=0.6)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 3, bar.get_y() + bar.get_height()/2, str(int(w)),
            va="center", fontsize=8, color=NETFLIX_GREY)
ax.set_title("Top 8 Genres")
ax.xaxis.grid(True); ax.set_axisbelow(True)

# ── Yearly trend (row 1, col 2–3) ─────────────────────────────
ax = fig.add_subplot(gs[1, 2:])
if "Movie" in pivot.columns:
    ax.plot(pivot.index.astype(int), pivot["Movie"],
            color=NETFLIX_RED, lw=2.5, marker="o", markersize=5, label="Movie")
if "TV Show" in pivot.columns:
    ax.plot(pivot.index.astype(int), pivot["TV Show"],
            color="#54A0FF", lw=2.5, marker="s", markersize=5, label="TV Show")
ax.fill_between(pivot.index.astype(int),
                pivot.get("Movie", 0), alpha=0.15, color=NETFLIX_RED)
ax.fill_between(pivot.index.astype(int),
                pivot.get("TV Show", 0), alpha=0.15, color="#54A0FF")
ax.set_title("Yearly Content Growth")
ax.set_xlabel("Year"); ax.set_ylabel("Titles")
ax.legend(); ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── Top 8 countries (row 2, col 0–1) ────────────────────────
ax = fig.add_subplot(gs[2, :2])
top8c = df["country"].value_counts().head(8)
colors_8 = [NETFLIX_RED if i == 0 else PALETTE[i % len(PALETTE)]
            for i in range(len(top8c))]
ax.bar(top8c.index, top8c.values, color=colors_8,
       edgecolor=NETFLIX_BLACK, linewidth=0.6)
ax.set_xticklabels(top8c.index, rotation=35, ha="right", fontsize=9)
ax.set_title("Top 8 Countries")
ax.set_ylabel("Titles")
ax.yaxis.grid(True); ax.set_axisbelow(True)

# ── Rating donut (row 2, col 2) ──────────────────────────────
ax = fig.add_subplot(gs[2, 2])
rc2 = df["rating"].value_counts().head(6)
ax.pie(rc2.values, labels=rc2.index, autopct="%1.0f%%",
       colors=PALETTE[:len(rc2)], startangle=90,
       wedgeprops={"width": 0.55, "edgecolor": NETFLIX_BLACK, "linewidth": 1.5},
       textprops={"color": ACCENT1, "fontsize": 9})
ax.set_title("Rating Mix")

# ── Movie runtime distribution (row 2, col 3) ────────────────
ax = fig.add_subplot(gs[2, 3])
ax.hist(movies["duration_min"].dropna(), bins=30,
        color=NETFLIX_RED, edgecolor=NETFLIX_BLACK, linewidth=0.4, alpha=0.9)
ax.axvline(movies["duration_min"].dropna().mean(), color="#FECA57",
           lw=1.5, linestyle="--", label="Mean")
ax.set_title("Movie Runtime")
ax.set_xlabel("Minutes"); ax.set_ylabel("Count")
ax.legend(fontsize=8); ax.yaxis.grid(True); ax.set_axisbelow(True)

save(fig, "07_summary_dashboard")


# ════════════════════════════════════════════════════════════
# PRINT SUMMARY STATISTICS
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  📊  SUMMARY STATISTICS")
print("=" * 55)
print(f"  Total Titles          : {len(df):,}")
print(f"  Movies                : {len(movies):,}  ({len(movies)/len(df)*100:.1f}%)")
print(f"  TV Shows              : {len(shows):,}  ({len(shows)/len(df)*100:.1f}%)")
print(f"  Countries             : {df['country'].nunique()}")
print(f"  Unique Ratings        : {df['rating'].nunique()}")
print(f"  Year Range            : {int(df['release_year'].min())} – {int(df['release_year'].max())}")
print(f"  Avg Movie Duration    : {movies['duration_min'].mean():.1f} min")
print(f"  Most Common Rating    : {df['rating'].mode()[0]}")
print(f"  Top Country           : {df['country'].value_counts().idxmax()}")
print(f"  Top Genre             : {genre_counts.idxmax()}")
print("=" * 55)
print(f"\n✅ All 7 charts saved to: {OUT}/")
