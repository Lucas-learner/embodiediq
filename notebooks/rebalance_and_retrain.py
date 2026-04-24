import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings('ignore')

# 1. Load existing and new data
print("Loading data...")
existing = pd.read_csv('../data/raw/arxiv_papers.csv')
new_months = pd.read_csv('../data/raw/arxiv_papers_new_months.csv')

existing['published'] = pd.to_datetime(existing['published'])
new_months['published'] = pd.to_datetime(new_months['published'])

print(f"Existing: {len(existing)} papers")
print(f"New months: {len(new_months)} papers")

# 2. Downsample over-concentrated months (Mar/Apr 2026)
MAX_PER_MONTH = 50

def downsample_month(df, year, month, max_n):
    mask = (df['published'].dt.year == year) & (df['published'].dt.month == month)
    subset = df[mask]
    if len(subset) > max_n:
        keep = subset.sample(n=max_n, random_state=42)
        rest = df[~mask]
        return pd.concat([rest, keep], ignore_index=True)
    return df

existing = downsample_month(existing, 2026, 3, MAX_PER_MONTH)
existing = downsample_month(existing, 2026, 4, MAX_PER_MONTH)

print(f"After downsampling Mar/Apr: {len(existing)} papers")

# 3. Merge datasets
merged = pd.concat([existing, new_months], ignore_index=True)
merged = merged.drop_duplicates(subset=['link'])
merged['published'] = pd.to_datetime(merged['published'])

print(f"\nMerged dataset: {len(merged)} papers")
print("Monthly distribution:")
print(merged.groupby(merged['published'].dt.to_period('M')).size().sort_index())

# 4. Save balanced dataset
merged.to_csv('../data/raw/arxiv_papers.csv', index=False)
print("\nSaved to ../data/raw/arxiv_papers.csv")

# 5. Re-train BERTopic
print("\nTraining BERTopic...")
texts = merged['summary'].dropna().tolist()

vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words="english", min_df=2)

topic_model = BERTopic(
    vectorizer_model=vectorizer,
    language="english",
    nr_topics=8,
    min_topic_size=5,
    verbose=True
)

topics, probs = topic_model.fit_transform(texts)

# 6. Assign topic names
topic_names = {
    -1: "Other",
    0: "VLA_Models",
    1: "Dexterous_Manipulation",
    2: "Humanoid_Control",
    3: "Sim_to_Real",
    4: "Robot_Learning",
    5: "Grasping",
    6: "Navigation",
    7: "Multi_Modal"
}

merged['topic_id'] = topics
merged['tech_route'] = merged['topic_id'].map(topic_names)

# 7. Save results
merged.to_csv('../data/processed/papers_with_topics.csv', index=False)
topic_model.save('../data/processed/bertopic_model')

print(f"\nTopic model saved. Papers with topics saved to ../data/processed/papers_with_topics.csv")
print(merged[['title', 'topic_id', 'tech_route']].head(10))
