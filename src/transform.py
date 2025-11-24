import pandas as pd

def transform_data(df_covid):

    df_covid_copy = df_covid.copy()
    
    df_covid_copy.dropna(subset = ['Increase rate'], how='all', inplace=True)

    df_covid_copy["year"]=df_covid_copy['Date'].dt.year
    df_covid_copy["month"]=df_covid_copy['Date'].dt.strftime('%b') #df_covid_copy['Date'].dt.month

    df_covid_copy.sort_values(by = 'Date', ascending = True)

    df_covid_copy.to_csv('data/processed/df_covid_processed.csv')

    return df_covid_copy