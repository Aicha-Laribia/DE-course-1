#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import unicodedata
from sqlalchemy import create_engine


pg_username = "aicha"
pg_password = "root"
pg_host = "pgdatabase"
pg_port = "5432"
pg_database = "startups"
table_name = "startups_morocco_data_2024"

# ==========================================
# 1. DATA ACQUISITION & INITIAL INSPECTION
# ==========================================

url = "https://raw.githubusercontent.com/Aicha-Laribia/data/main/bdd-startups-2024.xlsx"
df = pd.read_excel(url, engine='openpyxl')

print("--- Initial Head ---")
print(df.head())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Data Shape ---")
print(df.shape)

print("\n--- Secondary Head Check ---")
print(df.head())

print("\n--- Unique Cities Before Cleaning ---")
print(df['City'].unique())


# ==========================================
# 2. DATA CLEANING: CITY COLUMN
# ==========================================

# Convert to uppercase
df['City'] = df['City'].str.upper()

print("\n--- Unique Cities After Uppercase ---")
print(df['City'].unique())

# Strip trailing/leading spaces
df['City'] = df['City'].str.strip()

# Comprehensive city mapping list
city_mapping = {
    # Variations of existing Moroccan Cities (Accents & Typos)
    'FEZ': 'FES',
    'FÈS': 'FES',
    'TANGER': 'TANGIER',
    'TANGER-ASSILAH': 'TANGIER',
    'MOHAMMADIA': 'MOHAMMEDIA',
    'BERRCHID': 'BERRECHID',
    'CASZBLANCA': 'CASABLANCA',
    'MARRAKESH': 'MARRAKECH',
    'MEKNÈS': 'MEKNES',
    'TÉTOUAN': 'TETOUAN',
    'KÉNITRA': 'KENITRA',
    'KHÉMISSAT': 'KHMISSAT', 
    'KHEMISSET': 'KHMISSAT',
    'SALÉ': 'SALE',
    'MÁLAGA': 'MALAGA',

    # Ben Guerir variations
    'BENGUERIR': 'BEN GUERIR',
    'BENGUERIR (THE GREEN CITY OF BENGUERIR)': 'BEN GUERIR',
    'BEN_GUERIR': 'BEN GUERIR',

    # Beni Mellal variations
    'BÉNI MELLAL': 'BENI MELLAL',
    'BENI_MELLAL': 'BENI MELLAL',

    # Skhirate-Temara standard
    'SKHIRATE-TÉMARA': 'TEMARA',

    # Multi-City or Contextual Cleanups
    'CASABLANCA, MOROCCO': 'CASABLANCA',
    'ABU DHABI + RABAT BASED SARL': 'RABAT',
    'CASABLANCA - MARRAKECH AND FES': 'CASABLANCA',
    'CASABLANCA/DUBAI/LONDON': 'CASABLANCA'
}

# Apply the city mapping
df['City'] = df['City'].replace(city_mapping)

print("\n--- Unique Cities After Mapping ---")
print(df['City'].unique())


# ==========================================
# 3. DATA CLEANING: MAIN SECTOR COLUMN
# ==========================================

print("\n--- Unique Sectors Before Cleaning ---")
print(df['Main sector'].unique())

def pre_clean_sector(text):
    if not isinstance(text, str):
        return text

    # Strip whitespace and convert to upper case
    text = " ".join(text.split()).upper()

    # Replace underscores with spaces
    text = text.replace('_', ' ')

    # Strip French accents programmatically
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    # Remove apostrophes or weird spacing around them
    text = text.replace("DINF", "D INF") 

    return text

# Apply pre-cleaning pipeline
df['Main sector'] = df['Main sector'].apply(pre_clean_sector)

# Map the unified variations to standardized sectors
sector_mapping = {
    # French to English unification
    'SPORT ELECTRONIQUE': 'SPORTS TECH',
    'SECURITE DES SYSTEMES D INFORMATION': 'CYBERSECURITY',

    # Snake_case/Abbreviation cleanups
    'CLEAN TECH': 'CLEANTECH',
    'CONSTRUTECH': 'PROPTECH',       
    'TREE D TECHNOLOGY': '3D TECH',  
    'LEGAL TECH': 'LEGALTECH',
    'INSUR TECH': 'INSURTECH',
    'MED TECH': 'HEALTHTECH',         

    # Long parenthetical entries cleanup
    'MARTECH (MARKETING / ADVERTISING /DIGITAL & SOCIAL MEDIA)': 'MARTECH',
    'IMMERSIVE TECH (AR, VR, MR, GAMING)': 'IMMERSIVE TECH',
    'LEADS GENERATION OPTIMIZATION': 'MARTECH' 
}

# Apply final sector mapping
df['Main sector'] = df['Main sector'].replace(sector_mapping)

print("\n--- Unique Sectors After Mapping ---")
print(df['Main sector'].unique())


# ==========================================
# 4. FINAL QUALITY CHECKS
# ==========================================

print("\n--- Unique Raison Social ---")
print(df['Raison social'].unique())

print("\n--- Unique BD Source ---")
print(df['BD source'].unique())

print("\n--- Null Value Matrix ---")
print(df.isnull())

print("\n--- Columns with Missing Values ---")
print(df.isna().any())


# ==========================================
# 5. DATABASE INGESTION
# ==========================================

# Create target PostgreSQL engine
engine = create_engine(f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')

# Print target schema structure description


# Write dataframe to database
df.to_sql(name=table_name, con=engine, if_exists='replace') 
print(f"\nData successfully exported to database table '{table_name}'.")