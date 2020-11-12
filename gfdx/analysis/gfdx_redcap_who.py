# -*- coding: utf-8 -*-
"""gfdx-redcap-WHO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15PnjmVh3usPe9A8uXL-1wlw-JHaCcvP8

## GFDX notebook: WHO Recommendation Analysis
"""


# Install package to allow import from REDCap API
from redcap import Project
import pandas as pd
import numpy as np
import os
from tqdm.notebook import tqdm  # progress bar

api_key = os.environ.get('APIKEY')


# Connecting to GFDx Redcap API
URL = 'https://redcap.emory.edu/api/'
project = Project(URL, api_key)

# Pulls out variables of interest from REDCap
fields_of_interest = ['country_code', 'standard_nutrient', 'nutrient_level', 'nutrient_compound', 'latest_intake_api', 'food_status_api']
subset = project.export_records(fields=fields_of_interest, format='df')

# Reset index
df = subset.copy()
df.reset_index(inplace=True)

# Pipeline to first dataset
food_list = ['maize_flour_arm_1', 'wheat_flour_arm_1', 'rice_arm_1', 'salt_arm_1', 'oil_arm_1']
df1 = df[df.redcap_repeat_instrument.eq('nutrients_compounds')]
df2 = df1[df1.redcap_event_name.isin(food_list)]
df3 = df2[(df.food_status_api == 1) | (df.food_status_api == 2)]
analysis = df3.copy()]

# For countries that do not have both wheat and maize flour mandatory fortification
recommended_compounds_wheat = [4, 29, 38, 50, 55, 64, 86, 104, 105] 
recommended_compounds_maize = [4, 29, 38, 50, 55, 64, 86, 104, 105, 71, 72, 3, 81]
recommended_compounds_salt = [33, 34] 

df_copy = analysis.copy()

# Stating the WHO recommended compounds
df_copy['who_compound'] = 'No WHO recommendation'

for i, row in df_copy.iterrows():
    if row.redcap_event_name == 'oil_arm_1' or row.redcap_event_name == 'rice_arm_1':
        df_copy.loc[i, 'who_compound'] = 'No WHO recommendation available for this food'
    # Salt
    elif row.redcap_event_name == 'salt_arm_1' and row.standard_nutrient == 6:
        df_copy.loc[i, 'who_compound'] = 'Potassium iodate or potassium iodide'
    # Maize
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 1:
        df_copy.loc[i, 'who_compound'] = 'Pyridoxine hydrochloride'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 8:
        df_copy.loc[i, 'who_compound'] = 'Niacinamide'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 9:
        df_copy.loc[i, 'who_compound'] = 'Riboflavin'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 11:
        df_copy.loc[i, 'who_compound'] = 'Thiamine hydrochloride'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 2:
        df_copy.loc[i, 'who_compound'] = 'Cyanocobalamin'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 5:
        df_copy.loc[i, 'who_compound'] = 'Folic acid'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 7:
        df_copy.loc[i, 'who_compound'] = 'NaFeEDTA, ferrous sulfate, ferrous fumarate, or electrolytic iron'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 12:
        df_copy.loc[i, 'who_compound'] = 'Retinyl palmitate'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.standard_nutrient == 15:
        df_copy.loc[i, 'who_compound'] = 'Zinc oxide or zinc sulfate'
    # Wheat
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.standard_nutrient == 2:
        df_copy.loc[i, 'who_compound'] = 'Cyanocobalamin'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.standard_nutrient == 5:
        df_copy.loc[i, 'who_compound'] = 'Folic acid'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.standard_nutrient == 7:
        df_copy.loc[i, 'who_compound'] = 'NaFeEDTA, ferrous sulfate, ferrous fumarate, or electrolytic iron'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.standard_nutrient == 12:
        df_copy.loc[i, 'who_compound'] = 'Retinyl palmitate'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.standard_nutrient == 15:
        df_copy.loc[i, 'who_compound'] = 'Zinc oxide or zinc sulfate'

# Stating recommendations
df_copy['compound_include'] = 'Not WHO recommended'

for i, row in df_copy.iterrows():
    if row.redcap_event_name == 'oil_arm_1' or row.redcap_event_name == 'rice_arm_1':
        df_copy.loc[i, 'compound_include'] = 'No WHO recommendation available for this food'
    elif row.nutrient_compound == 1:
        df_copy.loc[i, 'compound_include'] = 'Compound is unspecified'
    elif row.redcap_event_name == 'wheat_flour_arm_1':
        if row.nutrient_compound in recommended_compounds_wheat:
            df_copy.loc[i, 'compound_include'] = 'WHO Recommended'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound in recommended_compounds_maize:
        df_copy.loc[i, 'compound_include'] = 'WHO Recommended'
    elif row.redcap_event_name == 'salt_arm_1' and row.nutrient_compound in recommended_compounds_salt:
        df_copy.loc[i, 'compound_include'] = 'WHO Recommended'

# Fixing Electrolytic Iron
for i, row in df_copy.iterrows():
    if (row.redcap_event_name == 'maize_flour_arm_1' or row.redcap_event_name == 'wheat_flour_arm_1') and row.nutrient_compound == 38 and row.latest_intake_api < 150: # Condition for electrolytic iron
        df_copy.loc[i, 'compound_include'] = 'Not WHO Recommended'
    if (row.redcap_event_name == 'maize_flour_arm_1' or row.redcap_event_name == 'wheat_flour_arm_1') and row.standard_nutrient == 7 and row.latest_intake_api < 150: # Condition for electrolytic iron
        df_copy.loc[i, 'who_compound'] = 'NaFeEDTA, ferrous sulfate or ferrous fumarate'

# Stating the WHO recommended level
df_copy1 = df_copy.copy()

df_copy1['who_rec_level'] = 'Not WHO recommended'

for i, row in df_copy1.iterrows():
    if row.redcap_event_name == 'oil_arm_1' or row.redcap_event_name == 'rice_arm_1':
        df_copy1.loc[i, 'who_rec_level'] = 'No WHO recommendation available for this food'
    elif pd.isna(row.latest_intake_api):
        df_copy1.loc[i, 'who_rec_level'] = 'No availability/intake data'
    elif row.nutrient_compound == 1:
        df_copy1.loc[i, 'who_rec_level'] = 'Compound is unspecified'
    # Salt plus 33 percent
    elif row.redcap_event_name == 'salt_arm_1' and (row.nutrient_compound == 33 or row.nutrient_compound == 34): # Potassium iodide and potassium iodate
        if row.latest_intake_api >= 3 and row.latest_intake_api < 3.499:
            df_copy1.loc[i, 'who_rec_level'] = '86.45'
        elif row.latest_intake_api >= 3.5 and row.latest_intake_api < 4.499:
            df_copy1.loc[i, 'who_rec_level'] = '65.17'
        elif row.latest_intake_api >= 4.5 and row.latest_intake_api < 5.499:
            df_copy1.loc[i, 'who_rec_level'] = '51.87'
        elif row.latest_intake_api >= 5.5 and row.latest_intake_api < 6.499:
            df_copy1.loc[i, 'who_rec_level'] = '43.89'
        elif row.latest_intake_api >= 6.5 and row.latest_intake_api < 7.499:
            df_copy1.loc[i, 'who_rec_level'] = '37.24'
        elif row.latest_intake_api >= 7.5 and row.latest_intake_api < 8.499:
            df_copy1.loc[i, 'who_rec_level'] = '31.92'
        elif row.latest_intake_api >= 8.5 and row.latest_intake_api < 9.499:
            df_copy1.loc[i, 'who_rec_level'] = '29.26'
        elif row.latest_intake_api >= 9.5 and row.latest_intake_api < 10.499:
            df_copy1.loc[i, 'who_rec_level'] = '26.60'
        elif row.latest_intake_api >= 10.5 and row.latest_intake_api < 11.499:
            df_copy1.loc[i, 'who_rec_level'] = '23.94'
        elif row.latest_intake_api >= 11.5 and row.latest_intake_api < 12.499:
            df_copy1.loc[i, 'who_rec_level'] = '21.28'
        elif row.latest_intake_api >= 12.5 and row.latest_intake_api < 13.499:
            df_copy1.loc[i, 'who_rec_level'] = '19.95'
        elif row.latest_intake_api >= 13.5 and row.latest_intake_api < 14.5:
            df_copy1.loc[i, 'who_rec_level'] = '18.62'        
    # Maize
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 71: # Niacinamide
        df_copy1.loc[i, 'who_rec_level'] = 36
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 72: # Riboflavin
        df_copy1.loc[i, 'who_rec_level'] = 2.0
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 3: # Pyridoxine Hydrochloride
        df_copy1.loc[i, 'who_rec_level'] = 6.2
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 81: # Thiamin Hydrochloride
        df_copy1.loc[i, 'who_rec_level'] = 3.9
    elif row.redcap_event_name == 'maize_flour_arm_1' and (row.nutrient_compound == 50 or row.nutrient_compound == 55): # Ferrous sulfate, Ferrous fumarate
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '60'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '60'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '30'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '20'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 64: # NaFeEDTA
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '40'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '40'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '20'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '15'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 38: # Electrolytic iron
        if row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '60'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '40'
    elif row.redcap_event_name == 'maize_flour_arm_1' and row.nutrient_compound == 29: # Folic acid
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '5.0'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '2.6'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '1.3'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '1.0'
    elif row.redcap_event_name == 'maize_flour_arm_1' and (row.nutrient_compound == 4): # Vitamin B12
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '0.04'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '0.02'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '0.01'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '0.008'
    elif row.redcap_event_name == 'maize_flour_arm_1' and (row.nutrient_compound == 86): # Vitamin A
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '5.9'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '3'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '1.5'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '1'
    elif row.redcap_event_name == 'maize_flour_arm_1' and (row.nutrient_compound == 104 or row.nutrient_compound == 105): # Zinc oxide/Zinc sulfate
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '95'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '55'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '40'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '30'
    # Wheat
    elif row.redcap_event_name == 'wheat_flour_arm_1' and (row.nutrient_compound == 50 or row.nutrient_compound == 55): # Ferrous sulfate, Ferrous fumarate
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '60'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '60'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '30'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '20'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.nutrient_compound == 64: # NaFeEDTA
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '40'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '40'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '20'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '15'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.nutrient_compound == 38: # Electrolytic iron
        if row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '60'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '40'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and row.nutrient_compound == 29: # Folic acid
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '5.0'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '2.6'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '1.3'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '1.0'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and (row.nutrient_compound == 4): # Vitamin B12
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '0.04'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '0.02'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '0.01'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '0.008'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and (row.nutrient_compound == 86): # Vitamin A
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '5.9'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '3'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '1.5'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '1'
    elif row.redcap_event_name == 'wheat_flour_arm_1' and (row.nutrient_compound == 104 or row.nutrient_compound == 105): # Zinc oxide/Zinc sulfate
        if row.latest_intake_api < 75:
            df_copy1.loc[i, 'who_rec_level'] = '95'
        elif row.latest_intake_api >= 75 and row.latest_intake_api < 150:
            df_copy1.loc[i, 'who_rec_level'] = '55'
        elif row.latest_intake_api >= 150 and row.latest_intake_api <= 300:
            df_copy1.loc[i, 'who_rec_level'] = '40'
        elif row.latest_intake_api > 300:
            df_copy1.loc[i, 'who_rec_level'] = '30'

# Calculate final percent
def calc_pc(row):
    try: 
        return round((float(row.nutrient_level) / float(row.who_rec_level)) * 100)
    except ValueError:
        return row.who_rec_level

df_copy1['alignment_pc'] = df_copy1.apply(lambda row: calc_pc(row), axis=1)

# The wheat and maize analysis
full_merged = pd.DataFrame()

for country in df_copy1.country_code.unique():
    s = df_copy1[(df_copy1.country_code == country)]
    if 'wheat_flour_arm_1' in s.redcap_event_name.values and 'maize_flour_arm_1' in s.redcap_event_name.values:
        s2 = s[(s.redcap_event_name == 'wheat_flour_arm_1') | (s.redcap_event_name == 'maize_flour_arm_1')]
        s3 = s2[s2.redcap_event_name == 'maize_flour_arm_1']
        s4 = s2[s2.redcap_event_name == 'wheat_flour_arm_1']
        #print(s2[['country_code', 'redcap_event_name', 'standard_nutrient','nutrient_compound', 'who_level']])

        merged_df = s3.merge(s4, how='inner', left_on=["country_code", "standard_nutrient", "nutrient_compound"], right_on=["country_code", "standard_nutrient", "nutrient_compound"])
        small_merged = merged_df[(merged_df.nutrient_compound == 50) | (merged_df.nutrient_compound == 55) | (merged_df.nutrient_compound == 64)
                               | (merged_df.nutrient_compound == 38) | (merged_df.nutrient_compound == 29) | (merged_df.nutrient_compound == 4)
                               | (merged_df.nutrient_compound == 86) | (merged_df.nutrient_compound == 104) | (merged_df.nutrient_compound == 105)]
        full_merged = full_merged.append(small_merged, ignore_index=True)

# Add FAO data for wheat and maize
def added_fao(row):
    try: 
        return float(row.latest_intake_api_x) + float(row.latest_intake_api_y)
    except ValueError:
        return 'No availability/intake data'

full_merged['combined_fao'] = full_merged.apply(lambda row: added_fao(row), axis=1)

# Recalculate standard values for each food and combine
def recalculate_com_standard(row):
    try: 
        return float((row.nutrient_level_x / 1000) * (row.latest_intake_api_x)) + float((row.nutrient_level_y / 1000) * (row.latest_intake_api_y))
    except ValueError:
        return 'No availability/intake data'

full_merged['combined_level'] = full_merged.apply(lambda row: recalculate_com_standard(row), axis=1)

# Determine the WHO datum based on the combined FAO data
def who_datum_range(row):
    if row.combined_fao < 75:
        return 50
    elif row.combined_fao >= 75 and row.combined_fao < 150:
        return 113
    elif row.combined_fao >= 150 and row.combined_fao <= 300:
        return 275
    elif row.combined_fao > 300:
        return 350
    else:    
        return 'No availability/intake data'

full_merged['who_datum'] = full_merged.apply(lambda row: who_datum_range(row), axis=1)

# Based on the datum present values for each compound
def calc_who_level_datum(row):
        if row.who_datum == 'No availability/intake data':
            return 'No availability/intake data'
        elif row.nutrient_compound == 50 or row.nutrient_compound == 55: # Ferrous sulfate, Ferrous fumarate
            if row.who_datum < 75:
                return 60
            elif row.who_datum >= 75 and row.who_datum < 150:
                return 60
            elif row.who_datum >= 150 and row.who_datum <= 300:
                return 30
            elif row.who_datum > 300:
                return 20
        elif row.nutrient_compound == 64: # NaFeEDTA
            if row.who_datum < 75:
                return 40
            elif row.who_datum >= 75 and row.who_datum < 150:
                return 40
            elif row.who_datum >= 150 and row.who_datum <= 300:
                return 20
            elif row.who_datum > 300:
                return 15
        elif row.nutrient_compound == 38: # Electrolytic iron
            if row.who_datum >= 150 and row.who_datum <= 300:
                return 60
            elif row.who_datum > 300:
                return 40
        elif row.nutrient_compound == 29: # Folic acid
            if row.who_datum < 75:
                return 5.0
            elif row.who_datum >= 75 and row.who_datum < 150:
                return 2.6
            elif row.who_datum >= 150 and row.who_datum <= 300:
                return 1.3
            elif row.who_datum > 300:
                return 1.0
        elif row.nutrient_compound == 4: # Vitamin B12
            if row.who_datum < 75:
                return 0.04
            elif row.who_datum >= 75 and row.who_datum < 150:
                return 0.02
            elif row.who_datum >= 150 and row.who_datum <= 300:
                return 0.01
            elif row.who_datum > 300:
                return 0.008
        elif row.nutrient_compound == 86: # Vitamin A
            if row.who_datum < 75:
                return 5.9
            elif row.who_datum >= 75 and row.who_datum < 150:
                return 3
            elif row.who_datum >= 150 and row.who_datum <= 300:
                return 1.5
            elif row.who_datum > 300:
                return 1
        elif (row.nutrient_compound == 104 or row.nutrient_compound == 105): # Zinc oxide/Zinc sulfate
            if row.who_datum < 75:
                return 95
            elif row.who_datum >= 75 and row.who_datum < 150:
                return 55
            elif row.who_datum >= 150 and row.who_datum <= 300:
                return 40
            elif row.who_datum > 300:
                return 30

full_merged['who_level_datum'] = full_merged.apply(lambda row: calc_who_level_datum(row), axis=1)

# Recalculate WHO level recommendations
def recalculate_com_who(row):
    try: 
        return (float(row.who_level_datum) / 1000) * (row.who_datum)
    except ValueError:
        return 'No availability/intake data'

full_merged['who_level_mw'] = full_merged.apply(lambda row: recalculate_com_who(row), axis=1)

# Calculate final percent
def com_calc_pc(row):
    try: 
        return round((float(row.combined_level) / float(row.who_level_mw)) * 100)
    except ValueError:
        return 'No availability/intake data'

full_merged['align_pc_mw'] = full_merged.apply(lambda row: com_calc_pc(row), axis=1)

# Comment field for these countries
full_merged['who_level_comment'] = 'Since this country fortifies the same nutrient and compound in both wheat flour and maize flour, the nutrient level analysis were conducted together.'

# Merge wheat and maize datasets together

final_maize = full_merged[['country_code', 'redcap_event_name_x', 'redcap_repeat_instrument_x', 'redcap_repeat_instance_x', 
                  'standard_nutrient', 'nutrient_level_x', 'nutrient_compound', 'latest_intake_api_x', 'food_status_api_x', 'who_compound_x',
                  'compound_include_x', 'who_level_datum', 'align_pc_mw', 'who_level_comment']]

final_maize.rename(columns={'redcap_event_name_x':'redcap_event_name', 'redcap_repeat_instrument_x':'redcap_repeat_instrument', 'redcap_repeat_instance_x':'redcap_repeat_instance', 
                            'nutrient_level_x': 'nutrient_level', 'latest_intake_api_x':'latest_intake_api', 
                            'food_status_api_x':'food_status_api', 'who_cmpd_x':'who_cmpd', 'cmpd_include_x':'cmpd_include',
                            'who_level_datum': 'who_level', 'align_pc_mw':'align_pc'}, inplace=True)

final_wheat = full_merged[['country_code', 'redcap_event_name_y', 'redcap_repeat_instrument_y', 'redcap_repeat_instance_y', 
                  'standard_nutrient', 'nutrient_level_y', 'nutrient_compound', 'latest_intake_api_y', 'food_status_api_y', 'who_compound_y',
                  'compound_include_y', 'who_level_datum', 'align_pc_mw', 'who_level_comment']]

final_wheat.rename(columns={'redcap_event_name_y':'redcap_event_name', 'redcap_repeat_instrument_y':'redcap_repeat_instrument', 'redcap_repeat_instance_y':'redcap_repeat_instance', 
                            'nutrient_level_y': 'nutrient_level', 'latest_intake_api_y':'latest_intake_api', 
                            'food_status_api_y':'food_status_api', 'who_cmpd_y':'who_cmpd', 'cmpd_include_y':'cmpd_include',
                            'who_level_datum': 'who_level', 'align_pc_mw':'align_pc'}, inplace=True)

# Merge continuation

df_copy1['who_level_comment'] = None

for i, row in tqdm(df_copy1.iterrows()):
    for a, row2 in final_wheat.iterrows():
        if row.country_code == row2.country_code and row.redcap_event_name == row2.redcap_event_name and row.standard_nutrient == row2.standard_nutrient and row.nutrient_compound == row2.nutrient_compound: 
            df_copy1.loc[i, 'who_rec_level'] = row2.who_level
            df_copy1.loc[i, 'alignment_pc'] = row2.align_pc
            df_copy1.loc[i, 'who_level_comment'] = row2.who_level_comment
    for b, row3 in final_maize.iterrows():
        if row.country_code == row3.country_code and row.redcap_event_name == row3.redcap_event_name and row.standard_nutrient == row3.standard_nutrient and row.nutrient_compound == row3.nutrient_compound: 
            df_copy1.loc[i, 'who_rec_level'] = row3.who_level
            df_copy1.loc[i, 'alignment_pc'] = row3.align_pc
            df_copy1.loc[i, 'who_level_comment'] = row3.who_level_comment

# Is other foods fortified with the same nutrient in each country?

def get_nice_food(redcap_event_name):
    if redcap_event_name == 'salt_arm_1':
        return 'salt'
    elif redcap_event_name == 'oil_arm_1':
        return 'oil'
    elif redcap_event_name == 'wheat_flour_arm_1':
        return 'wheat flour'
    elif redcap_event_name == 'maize_flour_arm_1':
        return 'maize flour'
    elif redcap_event_name == 'rice_arm_1':
        return 'rice'
    

df_copy1['other_food'] = 'nananana'

def calc_other_foods(main_row):
    country_df = df_copy1[(df_copy1.country_code == main_row.country_code) & (df_copy1.redcap_event_name != main_row.redcap_event_name)]

    if main_row.standard_nutrient not in country_df.standard_nutrient.values:
        return 'No'
    else:
        nutrient_foods = set()
        for i, row in country_df.iterrows():
            if main_row.standard_nutrient == row.standard_nutrient:
                nutrient_foods.add(get_nice_food(row.redcap_event_name))
        
        return ", ".join(sorted(nutrient_foods)).capitalize()

df_copy1['other_food'] = df_copy1.apply(lambda row: calc_other_foods(row), axis=1)

# Create final dataset, drop variables not used to upload
final=df_copy1.copy()
final.drop(['standard_nutrient', 'nutrient_level', 'nutrient_compound', 'latest_intake_api', 'food_status_api'], axis=1, inplace=True)

# Convert country code and repeat instance to integers
final["country_code"] = final.country_code.apply(lambda x: int(x))
final["redcap_repeat_instance"] = final.redcap_repeat_instance.apply(lambda x: int(x))

# Formats data into acceptable table for import into REDCap
final.set_index(['country_code', 'redcap_event_name'], inplace=True)

# FINAL IMPORT - Import to REDCap through API
project.import_records(final)