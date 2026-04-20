import pandas as pd
import matplotlib.pyplot as plt

# =====================
# 1. LOAD DATA
# =====================
df = pd.read_csv('netflix_titles.csv')

# =====================
# 2. DATA CLEANING
# =====================
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df['duration'] = df['duration'].fillna(df['duration'].mode()[0])

# Extract year once (reuse later)
df['year'] = df['date_added'].dt.year

# =====================
# 3. BAR CHART (Type)
# =====================
type_count = df['type'].value_counts()

plt.figure(figsize=(10,5))
plt.bar(type_count.index, type_count.values, color=["orange","skyblue"], edgecolor='black')
plt.title("Number of Movies and TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")

# =====================
# 4. PIE CHART (Ratings)
# =====================
ratings_count = df['rating'].value_counts()

plt.figure(figsize=(8,8))
plt.pie(ratings_count, labels=ratings_count.index, autopct='%1.1f%%')
plt.title("Content Ratings Distribution")


# =====================
# 5. LINE PLOT (Releases Over Time)
# =====================
year_counts = df['year'].value_counts().sort_index()

plt.figure(figsize=(10,5))
plt.plot(year_counts.index, year_counts.values, marker='o')
plt.title("Netflix Releases Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Releases")
plt.grid()

# =====================
# 6. HISTOGRAM (Movie Duration)
# =====================
movies = df[df['type'] == 'Movie'].copy()

movies['duration'] = movies['duration'].str.replace(' min','')
movies['duration'] = pd.to_numeric(movies['duration'], errors='coerce')

plt.figure(figsize=(10,5))
plt.hist(movies['duration'].dropna(), bins=20, edgecolor='black')
plt.title("Distribution of Movie Duration")
plt.xlabel("Minutes")
plt.ylabel("Number of Movies")

# =====================
# 7. TOP COUNTRIES
# =====================
country_df = df.dropna(subset=['country']).copy()

country_df['country'] = country_df['country'].str.split(',')
country_df = country_df.explode('country')
country_df['country'] = country_df['country'].str.strip()

top_countries = country_df['country'].value_counts().head(10)

plt.figure(figsize=(10,5))
plt.barh(top_countries.index, top_countries.values, edgecolor='black')
plt.title("Top 10 Countries by Content")
plt.xlabel("Number of Shows")
plt.ylabel("Country")
plt.gca().invert_yaxis()  # makes highest on top

fig, axs = plt.subplots(2, 3, figsize=(18,10))  # 2 rows, 3 columns

# =====================
# 1. BAR CHART (Type)
# =====================
type_count = df['type'].value_counts()
axs[0,0].bar(type_count.index, type_count.values, color=["orange","skyblue"], edgecolor='black')
axs[0,0].set_title("Movies vs TV Shows")

# =====================
# 2. PIE CHART (Ratings)
# =====================
ratings_count = df['rating'].value_counts()
axs[0,1].pie(ratings_count, labels=ratings_count.index, autopct='%1.1f%%')
axs[0,1].set_title("Ratings Distribution")

# =====================
# 3. LINE PLOT (Year)
# =====================
year_counts = df['year'].value_counts().sort_index()
axs[0,2].plot(year_counts.index, year_counts.values, marker='o')
axs[0,2].set_title("Releases Over Time")

# =====================
# 4. HISTOGRAM (Duration)
# =====================
axs[1,0].hist(movies['duration'].dropna(), bins=20, edgecolor='black')
axs[1,0].set_title("Movie Duration")

# =====================
# 5. TOP COUNTRIES
# =====================
axs[1,1].barh(top_countries.index, top_countries.values, edgecolor='black')
axs[1,1].set_title("Top Countries")

# =====================
# 6. EMPTY SPACE (optional)
# =====================
axs[1,2].axis('off')  # hide last plot if unused

plt.tight_layout()
plt.show()