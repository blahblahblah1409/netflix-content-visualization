import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# --- Reference Data ---
genres = [
    "Dramas", "Comedies", "Documentaries", "Action & Adventure",
    "Thrillers", "Horror Movies", "Romantic Movies", "Sci-Fi & Fantasy",
    "International Movies", "Children & Family Movies", "Anime Series",
    "Crime TV Shows", "Reality TV", "Stand-Up Comedy", "Music & Musicals",
    "Sports Movies", "Classic Movies", "LGBTQ Movies", "Independent Movies"
]

countries = [
    "United States", "India", "United Kingdom", "Canada", "France",
    "Japan", "South Korea", "Germany", "Spain", "Australia",
    "Mexico", "Brazil", "Italy", "Turkey", "Nigeria",
    "Thailand", "Philippines", "Egypt", "Argentina", "Sweden"
]

ratings = ["G", "PG", "PG-13", "R", "TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA", "NR"]

country_weights   = [0.30, 0.13, 0.08, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.03,
                     0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.02]
genre_weights     = [0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05,
                     0.04, 0.04, 0.03, 0.03, 0.02, 0.01, 0.01, 0.01, 0.00]
rating_weights    = [0.02, 0.04, 0.10, 0.12, 0.03, 0.03, 0.04, 0.07, 0.14, 0.38, 0.03]

directors = [f"Director_{i}" for i in range(1, 300)]
cast_pool = [f"Actor_{i}" for i in range(1, 500)]

n = 6000
show_ids   = [f"s{i}" for i in range(1, n + 1)]
types      = np.random.choice(["Movie", "TV Show"], n, p=[0.70, 0.30])
titles     = [f"{'Movie' if t == 'Movie' else 'Show'} Title {i}" for i, t in enumerate(types, 1)]
dirs       = [random.choice(directors) if random.random() > 0.10 else np.nan for _ in range(n)]

def rand_cast():
    k = random.randint(2, 6)
    return ", ".join(random.sample(cast_pool, k)) if random.random() > 0.05 else np.nan

casts       = [rand_cast() for _ in range(n)]
ctry        = np.random.choice(countries, n, p=country_weights)
years       = np.random.choice(range(2008, 2022), n,
                               p=[0.01,0.01,0.02,0.03,0.04,0.05,0.06,0.07,
                                  0.09,0.10,0.12,0.13,0.13,0.14])
added_years = np.where(np.array(years) + 1 <= 2021, np.array(years) + 1, 2021)
date_added  = [
    f"{random.choice(['January','February','March','April','May','June','July','August','September','October','November','December'])} {random.randint(1,28)}, {y}"
    for y in added_years
]
release_yr  = years.tolist()
rtgs        = np.random.choice(ratings, n, p=rating_weights)

def rand_duration(t):
    if t == "Movie":
        return f"{random.randint(60, 180)} min"
    else:
        return f"{random.randint(1, 8)} Season{'s' if random.randint(1,8) > 1 else ''}"

durations = [rand_duration(t) for t in types]

def rand_genres():
    k = random.randint(1, 3)
    return ", ".join(random.sample(genres, k))

listed_in   = [rand_genres() for _ in range(n)]
description = [f"A compelling story about themes related to {random.choice(genres).lower()}." for _ in range(n)]

df = pd.DataFrame({
    "show_id": show_ids, "type": types, "title": titles,
    "director": dirs, "cast": casts, "country": ctry,
    "date_added": date_added, "release_year": release_yr,
    "rating": rtgs, "duration": durations,
    "listed_in": listed_in, "description": description
})

df.to_csv("/home/claude/netflix_project/data/netflix_titles.csv", index=False)
print(f"Dataset created: {len(df)} rows, {len(df.columns)} columns")
print(df.head(3))
