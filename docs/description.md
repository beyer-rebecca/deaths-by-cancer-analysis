# Description of Dataset for Project 1 and Associated Research Questions


## Motivation

I selected the dataset ["Causes of death statistics - Deaths: Germany, years, causes of deaths, age groups" (Tabelle 23211-0004)](https://www-genesis.destatis.de/genesis//online?operation=table&code=23211-0004&bypass=true&levelindex=1&levelid=1714304169630#abreadcrumb)
from the Causes of Death statistics vom Statistisches Bundesamt (Destatis). 
I find the data set interesting because a family member died due to breast cancer and I wanted to find out more about the significance of cancer and breast cancer as a cause of death in the German population.


## Description of the Dataset

The data set I have chosen provides the mortality in Germany over the last two decades covering the years 2003 to 2022.
It contains data on the absolute number of deaths, classified by different causes of death, including different types of cancer, amongst them breast cancer. Gender (women, men) and age groups (5-year blocks) are also taken into account, providing a detailed picture of how mortality rates vary across different demographic groups and time periods. 


## Research Questions and Narrative

I want to examine the broader context of cancer mortality in Germany, look at breast cancer specifically and then analyse the data to investigate age-related patterns and changes in breast cancer deaths over time. 

-  **Cancer's Proportion of Mortality in Germany**: What percentage of all deaths in Germany in 2022 were due to cancer, and how does this compare to other leading causes of death? 
-  **Comparison of Cancer Types by Mortality**: Among the various types of cancer, which had the highest mortality rates in 2022, and how do these rates differ between men and women? A bar plot can compare the mortality counts for different cancers, with separate bars for men and women to reveal gender-specific trends.
-  **Age-Specific Breast Cancer Mortality in Women**: How does breast cancer mortality vary across different age groups in women in 2022? A bar plot or a series of line plots for each age group can demonstrate how age influences the risk of dying from breast cancer.
-  **Breast Cancer Mortality Trends in Women Over the Last 20 Years**: How have breast cancer mortality rates changed over the last 20 years among women? A line plot can show the trajectory of breast cancer mortality, providing insights into the effectiveness of treatment and early detection efforts.
-  **Average Age of Breast Cancer Mortality in Women**: What is the average age at which women succumb to breast cancer in 2022?

## Methodological Approach

The following plotting techniques are used:
-  **Pie Plot for Cancer's Proportion of Mortality**:  A pie plot will be used to represent the 10 leading causes of death in Germany for 2022, showcasing each cause as a percentage of total mortality. 
-  **Bar Plot for Cancer Type Comparison**: A bar plot will display the mortality counts for various types of cancer in 2022, with different bars grouped by cancer type and differentiated by color for men and women. The x-axis will label each cancer type, with a color distinction for gender, and the y-axis will show the percentage each cancer type constitutes of the total cancer deaths.
-  **Line Plot for Age-Specific Breast Cancer Mortality**: A line plot will be used to display breast cancer mortality across different age groups, segmented into 5-year groups. The x-axis will categorize the age groups, while the y-axis will enumerate the absolute number of breast cancer-related deaths.
-  **Line Plot for Breast Cancer Mortality Trends in Women Over the Last 20 Years**: A line plot will be used to show the trend in breast cancer mortality rates among women over the past 20 years. The x-axis will include years from 2002 to 2022, and the y-axis will record the absolute number of women who have died from breast cancer each year. 
-  **Average Age of Breast Cancer Mortality**: To calculate the average age at which women die from breast cancer in 2022, the mean age will be computed along with the standard deviation to provide a measure of variability around the mean.

For visualizations, calculations, and data preprocessing in Python, the matplotlib, seaborn, pandas, and numpy packages will be used.