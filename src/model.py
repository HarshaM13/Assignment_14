import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def pred_model(df_covid):

    y = df_covid[['Deaths']]
    X = df_covid.drop(columns = ['Deaths',"Date"], axis = 1)

    # Initial split to create training and temp sets (temp will later be split into test and validation)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)  # 70% train, 30% temp (test/val)

    # Split the temp set into validation and test sets (50-50 split of the 30%, so 15% each)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    numerical = ['Confirmed', 'Recovered','Increase rate']
    categorical = ['month', 'year'] 

    #split train data
    X_train_numerical = X_train[numerical]
    X_train_categorical = X_train[categorical]

    #split Validation data
    X_val_numerical = X_val[numerical]
    X_val_categorical = X_val[categorical]

    #split test data
    X_test_numerical = X_test[numerical]
    X_test_categorical = X_test[categorical]

    MinMaxtransformer = MinMaxScaler().fit(X_train_numerical)

    #Train
    X_train_normalized = MinMaxtransformer.transform(X_train_numerical)
    X_train_minmax = pd.DataFrame(X_train_normalized,columns=X_train_numerical.columns)
    #X_train_minmax.head()

    #Validation
    X_val_normalized = MinMaxtransformer.transform(X_val_numerical)
    X_val_minmax = pd.DataFrame(X_val_normalized,columns=X_val_numerical.columns)
    #X_val_minmax.head()

    #Test
    X_test_normalized = MinMaxtransformer.transform(X_test_numerical)
    X_test_minmax = pd.DataFrame(X_test_normalized,columns=X_test_numerical.columns)


    X_train_categorical_ohe = X_train_categorical[['month', 'year']]
    X_val_categorical_ohe = X_val_categorical[['month', 'year']]
    X_test_categorical_ohe = X_test_categorical[['month', 'year']]


    #Fit ONLY the train set. 
    encoder = OneHotEncoder(handle_unknown='ignore', drop='first').fit(X_train_categorical_ohe)


    #Train
    encoded_for_p_train = encoder.transform(X_train_categorical_ohe).toarray()
    cols = encoder.get_feature_names_out(input_features=X_train_categorical_ohe.columns)
    X_train_ohe = pd.DataFrame(encoded_for_p_train, columns=cols)
    #X_train_ohe.head()


    #Validation
    encoded_for_p_val = encoder.transform(X_val_categorical_ohe).toarray()
    cols = encoder.get_feature_names_out(input_features=X_val_categorical_ohe.columns)
    X_val_ohe = pd.DataFrame(encoded_for_p_val, columns=cols)
    #X_val_ohe.head()


    #Test
    encoded_for_p_test = encoder.transform(X_test_categorical_ohe).toarray()
    cols = encoder.get_feature_names_out(input_features=X_test_categorical_ohe.columns)
    X_test_ohe = pd.DataFrame(encoded_for_p_test, columns=cols)
    #X_test_ohe.head()


    #Reset Indices in Train
    X_train_ohe = X_train_ohe.reset_index(drop = True)


    #Reset Indices in Validation
    X_val_ohe = X_val_ohe.reset_index(drop = True)


    #Reset Indices in Test
    X_test_ohe = X_test_ohe.reset_index(drop = True)




    X_train_cat_treated = X_train_ohe
    X_val_cat_treated = X_val_ohe
    X_test_cat_treated = X_test_ohe


    ###Reset Indices###
    X_train_minmax = X_train_minmax.reset_index(drop = True)
    X_val_minmax = X_val_minmax.reset_index(drop = True)
    X_test_minmax = X_test_minmax.reset_index(drop = True)



    #####Concat#####

    #Train
    X_train_scaled_minmax = pd.concat([X_train_minmax,X_train_cat_treated], axis = 1)

    #Validation
    X_val_scaled_minmax = pd.concat([X_val_minmax,X_val_cat_treated], axis = 1)

    #Test
    X_test_scaled_minmax = pd.concat([X_test_minmax,X_test_cat_treated], axis = 1)


    y_train = y_train.reset_index(drop = True)
    y_val = y_val.reset_index(drop = True)
    y_test = y_test.reset_index(drop = True)



    #Define the linear regression model
    LinReg = LinearRegression()
    LinReg

    #fit the training set onto the Linear Regression Model
    LinReg.fit(X_train_scaled_minmax,y_train)

    #Predict our y results using our X_val_scaled data, 
    #which was based on the rules in our training set.
    y_val_pred = LinReg.predict(X_val_scaled_minmax)

    # Convert predictions to a Series with the same index as X_val
    y_val_pred_series = pd.Series(y_val_pred.flatten().round(2), index=X_val.index, name='Predicted_Deaths')


    # Add predictions to df_covid at the correct rows
    df_covid.loc[y_val_pred_series.index, 'Predicted_Deaths'] = y_val_pred_series

    df_covid.dropna(subset = ['Predicted_Deaths'], how='all', inplace=True)

    df_covid.reset_index(drop=True).sort_values(by = 'Date', ascending = True)

    df_covid.to_csv('data/processed/df_covid_val_pred.csv')

    return df_covid