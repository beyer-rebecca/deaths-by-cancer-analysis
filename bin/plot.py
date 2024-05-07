"""Generates plots for visualizing mortality from cancer in germany, with a focus on breast cancer in female population"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PRIMARY_DEATH_CAUSES = [
    'Certain infectious and parasitic diseases',
    'Malignant neoplasms',
    'Benign neoplasms',
    'Diseases of the blood and blood-forming organs',
    'Endocrine, nutritional and metabolic diseases',
    'Mental and behavioural disorders',
    'Diseases of the nervous system and sensory organs',
    'Diseases of the circulatory system',
    'Diseases of the respiratory system',
    'Diseases of the digestive system',
    'Diseases of the skin and subcutaneous tissue',
    'Diseases of musculoskeletal sys. a. connec. tissue',
    'Diseases of the genitourinary system',
    'Pregnancy, childbirth and the puerperium',
    'Certain conditions origin. in the perinatal period',
    'Congenital malform.,deform. a. chromosomal abnorm.',
    'Symp., signs a. abnormal clinical a. lab. findings',
    'Other ill-defined and unknown causes of mortality',
    'External causes of morbidity and mortality',
    'Total'
]

CANCER_TYPES = [
    "Malignant neoplasms",
    "Malignant neoplasms of lip, oral cavity, pharynx",
    "Malignant neoplasms of oesophagus",
    "Malignant neoplasms of stomach",
    "Malignant neoplasms of colon",
    "Malig. neopl. of rectum, anus, rectosigmoid junction",
    "Malig. neoplasms of liver, intrahepatic bile ducts",
    "Malignant neoplasms of pancreas",
    "Malignant neoplasms of bronchus and lung",
    "Melanoma and other malignant neoplasms of skin",  
    "Malignant neoplasms of breast",
    "Malignant neoplasms of cervix uteri", 
    "Malig. neopl. of corpus uteri, uterus, part unspec.",  
    "Malignant neoplasms of ovary",
    "Malignant neoplasms of prostate",
    "Malignant neoplasms of kidney, except renal pelvis",
    "Malignant neoplasms of bladder",
    "Malig. neopl.of lymphoid, haematopoietic, rel. tissue"
]

def _read_csv():
    """Read and preprocess the dataset."""
    df = pd.read_csv(
        '../data/death_counts_DE_causes_2003-2022_gender_age.csv',
        header=[0,1,2,3], 
        encoding='ANSI', 
        engine='python', 
        delimiter=';', 
        skiprows=5, 
        skipfooter=4
        )
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    df = _preprocess_data(df)
    return df

def _preprocess_data(df):
    """Convert data to long format and clean it."""
    long_format_df = df.melt(
        id_vars=[
            'Unnamed: 0_level_0 Unnamed: 0_level_1 Unnamed: 0_level_2 Unnamed: 0_level_3',
            'Unnamed: 1_level_0 Unnamed: 1_level_1 Unnamed: 1_level_2 Unnamed: 1_level_3'
        ],
        var_name='Demographics',
        value_name='Number of Deaths'
    )

    long_format_df['Sex'] = long_format_df['Demographics'].apply(lambda x: x.split()[1])
    long_format_df['Age Group'] = long_format_df['Demographics'].apply(
        lambda x: ' '.join(x.split()[4:])
    )
    long_format_df = long_format_df.drop('Demographics', axis=1)
    long_format_df.columns = ['Year', 'Cause of Death', 'Number of Deaths', 'Sex', 'Age Group']
    long_format_df['Age Group'] = long_format_df['Age Group'].str.replace('groups ', '')
    long_format_df.tail(20)
    long_format_df = long_format_df[long_format_df['Age Group'] != 'age unknown']
    long_format_df['Number of Deaths'] = pd.to_numeric(
        long_format_df['Number of Deaths'], errors='coerce'
    ).astype('Int64')
    return long_format_df


def plot_cause_of_death_distribution():
    """Creates a pie chart illustrating the percentage distribution of mortality causes in Germany"""

    def preprocess_df(df):
        df = df[
            (df['Year'] == 2022) &
            (df['Cause of Death'].isin(PRIMARY_DEATH_CAUSES))
        ]

        cause_totals = df.groupby('Cause of Death')['Number of Deaths'].sum()
        total_deaths = cause_totals['Total']
        percentages = (cause_totals / total_deaths * 100).sort_values(ascending=False)
        percentages = percentages.drop('Total')

        low_bound = 4 # percentage
        significant_causes = percentages[percentages >= low_bound]
        other_causes_percentage = percentages[percentages < low_bound].sum()
        significant_causes['Other'] = other_causes_percentage

        return significant_causes

    def plot(df):
        gray_shades = ['#A9A9A9', '#D3D3D3']  
        colors = [
            gray_shades[i % 2] if cause != 'Malignant neoplasms' else 'indianred' 
            for i, cause in enumerate(df.index)
            ]
        colors[0] = '#D3D3D3'

        plt.figure(figsize=(18, 6))
        plt.pie(df, labels=df.index, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title('Proportion of Mortality by Cause in Germany in 2022')
        plt.axis('equal') 
        plt.show()
    
    df = _read_csv()
    df = preprocess_df(df)
    plot(df)


def plot_cancer_type_mortality_by_sex():
    """Create a bar plot showing the number of deaths of female and male population in Germany, depending on type of cancer"""
    
    def preprocess_df(df):
        df = df[
            (df['Year'] == 2022) &
            (df['Cause of Death'].isin(CANCER_TYPES))
        ]

        df_cancer_mortality = df.groupby(['Cause of Death', 'Sex'])['Number of Deaths'].sum().reset_index()
        df_cancer_mortality = df_cancer_mortality.rename({
            'Melanoma and other malignant neoplasms of skin': 'Malignant neoplasms of skin'
        })

        female_reproductive_cancers = [
            'Malignant neoplasms of cervix uteri', 
            'Malig. neopl. of corpus uteri, uterus, part unspec.', 
            'Malignant neoplasms of ovary' 
        ]

        female_reproductive_totals = df_cancer_mortality[df_cancer_mortality['Cause of Death'].isin(female_reproductive_cancers)]
        female_reproductive_totals = female_reproductive_totals.groupby('Sex')['Number of Deaths'].sum().reset_index()
        female_reproductive_totals['Cause of Death'] = 'Malignant neoplasms of female reproductive system'

        df_cancer_mortality = pd.concat([df_cancer_mortality, female_reproductive_totals]).reset_index(drop=True)
        df_cancer_mortality = df_cancer_mortality[~df_cancer_mortality['Cause of Death'].isin(female_reproductive_cancers)]
        df_cancer_mortality = df_cancer_mortality [df_cancer_mortality['Cause of Death'] != 'Malignant neoplasms']
        
        return df_cancer_mortality

    def plot(df):
        cancer_types_aliases = {
            "Malig. neoplasms of liver, intrahepatic bile ducts": "liver, intrahepatic bile duct",
            "Malignant neoplasms of bladder": "bladder",
            "Malignant neoplasms of breast": "breast",
            "Malignant neoplasms of bronchus and lung": "bronchus and lung",
            "Malignant neoplasms of colon": "colon",
            "Malignant neoplasms of kidney, except renal pelvis": "kidney, except renal pelvis",
            "Malignant neoplasms of lip, oral cavity, pharynx": "lip, oral cavity, pharynx",
            "Malignant neoplasms of oesophagus": "oesophagus",
            "Malignant neoplasms of pancreas": "pancreas",
            "Malignant neoplasms of prostate": "prostate",
            "Malignant neoplasms of stomach": "stomach",
            "Melanoma and other malignant neoplasms of skin": "skin",
            "Malignant neoplasms of female reproductive system": "female reproductive system"
        }

        plt.figure(figsize=(12,5))
        sns.set(style="whitegrid")

        bar_plot = sns.barplot(
            x='Cause of Death',
            y='Number of Deaths',
            hue='Sex',
            data=df,
            palette={'Female': 'tab:blue', 'Male': 'tab:orange'},
        )

        plt.title('Comparison of Cancer Types Mortability in 2022 by Sex')
        plt.xlabel('Type of Cancer')
        plt.ylabel('Number of Deaths')
        plt.xticks(rotation=90, ticks=np.arange(len(cancer_types_aliases)), labels=list(cancer_types_aliases.values()))

        plt.tight_layout()
        plt.show()

    df = _read_csv()
    df = preprocess_df(df)
    plot(df)


def plot_breast_cancer_mortality_trends():
    """Creates a bar chart showing the number of deaths in the female population in Germany due to breast cancer in the period 2003-20022."""
    def preprocess_df(df):
        df = df[
            (df['Sex'] == 'Female') &
            (df['Cause of Death'] == 'Malignant neoplasms of breast')
        ]

        df_cancer_mortality = df.groupby(['Cause of Death', 'Sex'])['Number of Deaths'].sum().reset_index()
        df = df.groupby(['Year'])['Number of Deaths'].sum().reset_index()
        df = df.sort_values('Year')
        return df
    
    def plot(df):
        plt.figure(figsize=(10, 5))
        plt.plot(df['Year'], df['Number of Deaths'], marker='o', linestyle='-', color='tab:blue')
        plt.xticks(df['Year'], df['Year'], rotation=45)
        plt.ylim(bottom=0,top=22000)

        plt.title('Breast Cancer Mortality Trends in Women, 2003-2022')
        plt.xlabel('Year')
        plt.ylabel('Number of Deaths')

        plt.show()
    
    df = _read_csv()
    df = preprocess_df(df)
    plot(df)


def plot_breast_cancer_mortality_by_age():
    """Creates a line chart showing the number of deaths in the female population from breast cancer in Germany, depending on age."""
    def preprocess_df(df):
        df = df[
            (df['Year'] == 2022) &
            (df['Sex'] == 'Female') &
            (df['Cause of Death'] == 'Malignant neoplasms of breast')
        ]

        df.reset_index(drop=True)
        df = df.drop(['Cause of Death', 'Year', 'Sex'], axis=1)

        df = df.fillna(value=0)

        return df
        
    def plot(df):
        ages = {
            'under 1 year': '<1*',
            '1 to under 15 years': '1-14*',
            '15 to under 20 years': '15-19*',
            '20 to under 25 years': '20-24',
            '25 to under 30 years': '25-29',
            '30 to under 35 years': '30-34',
            '35 to under 40 years': '35-39',
            '40 to under 45 years': '40-44',
            '45 to under 50 years': '45-49',
            '50 to under 55 years': '50-54',
            '55 to under 60 years': '55-59',
            '60 to under 65 years': '60-64',
            '65 to under 70 years': '65-69',
            '70 to under 75 years': '70-74',
            '75 to under 80 years': '75-79',
            '80 to under 85 years': '80-84',
            '85 years and over': '>85'
        }

        plt.figure(figsize=(10, 5))
        sns.barplot(data=df, x='Age Group', y='Number of Deaths', color='tab:blue')

        plt.title('Age-Specific Breast Cancer Mortality in Women from Year 2022')
        plt.xlabel('Age')
        plt.ylabel('Number of Deaths')
        plt.xticks(ticks=np.arange(len(ages)), labels=list(ages.values()), rotation=45)
        plt.legend(handles=[plt.Line2D([0], [0], color='w', label='* no data available')], loc='upper left')

        plt.tight_layout() 
        plt.show()
        
    df = _read_csv()
    df = preprocess_df(df)
    plot(df)

def print_breast_cancer_mortality_median_age():
    """Calculates the average age at which women in Germany died of breast cancer in 2022 using the median and standard deviation."""

    def preprocess_df(df):
        df = df[
            (df['Year'] == 2022) &
            (df['Sex'] == 'Female') &
            (df['Cause of Death'] == 'Malignant neoplasms of breast')
        ]

        df.reset_index(drop=True)
        df = df.drop(['Cause of Death', 'Year', 'Sex'], axis=1)
        return df
    
    def calculate_median_age(df):
        age_midpoints = {
            'under 1 year': 0.5,
            '1 to under 15 years': 7.5,
            '15 to under 20 years': 17.5,
            '20 to under 25 years': 22.5,
            '25 to under 30 years': 27.5,
            '30 to under 35 years': 32.5,
            '35 to under 40 years': 37.5,
            '40 to under 45 years': 42.5,
            '45 to under 50 years': 47.5,
            '50 to under 55 years': 52.5,
            '55 to under 60 years': 57.5,
            '60 to under 65 years': 62.5,
            '65 to under 70 years': 67.5,
            '70 to under 75 years': 72.5,
            '75 to under 80 years': 77.5,
            '80 to under 85 years': 82.5,
            '85 years and over': 90   # Assumption for '85 and older'
        }

        ages = []
        for age_group, midpoint in age_midpoints.items():
            if age_group in df['Age Group'].values:
                deaths_in_group = df[df['Age Group'] == age_group]['Number of Deaths'].values[0]
                ages.extend([midpoint] * deaths_in_group)

        median_age = np.median(ages) 
        std = np.std(ages)
        print(f"The median age of death from breast cancer for women in 2022 is: {median_age:.2f} ± {std:.2f} ages")
    
    df = _read_csv()
    preprocess_df(df)
    calculate_median_age(df)


if __name__ == "__main__":
    print_breast_cancer_mortality_median_age()
