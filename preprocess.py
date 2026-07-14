"""
BASILICA — Data Preprocessing Pipeline
Milestone 3: Data Preprocessing & Feature Engineering

Cleans the raw training data and splits it into train/validation/test sets,
stratified by intent so every split has a proportional mix of all 10 intents.
Run this any time you add more examples to training_data.csv — it's fully
reproducible (same random_state = same split every time).
"""

import re
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42  # fixed seed -> reproducible splits every run

def clean_text(text: str) -> str:
    """Lowercase, strip extra whitespace, remove stray punctuation noise."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s?']", "", text)   # keep letters, numbers, ? and '
    text = re.sub(r"\s+", " ", text)         # collapse multiple spaces
    return text

def main():
    df = pd.read_csv("training_data.csv")
    print(f"Loaded {len(df)} raw examples across {df['intent'].nunique()} intents")

    # Clean
    df["text_clean"] = df["text"].apply(clean_text)

    # Drop any accidental duplicates or empty rows after cleaning
    before = len(df)
    df = df.drop_duplicates(subset="text_clean").dropna(subset=["text_clean", "intent"])
    if len(df) < before:
        print(f"Removed {before - len(df)} duplicate/empty rows")

    # Split: 70% train, 15% validation, 15% test — stratified by intent
    train_df, temp_df = train_test_split(
        df, test_size=0.30, stratify=df["intent"], random_state=RANDOM_STATE
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, stratify=temp_df["intent"], random_state=RANDOM_STATE
    )

    train_df.to_csv("train.csv", index=False)
    val_df.to_csv("val.csv", index=False)
    test_df.to_csv("test.csv", index=False)

    print(f"\nSplit sizes:")
    print(f"  Train:      {len(train_df)} examples")
    print(f"  Validation: {len(val_df)} examples")
    print(f"  Test:       {len(test_df)} examples")
    print(f"\nSaved: train.csv, val.csv, test.csv")

    print(f"\nPer-intent counts in training set:")
    print(train_df["intent"].value_counts().sort_index().to_string())

if __name__ == "__main__":
    main()
