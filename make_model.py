#This file creates and updates the model
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from DBhandler import DBhandler
from sklearn.utils import shuffle
import pandas as pd
import os
import joblib
from constants import democrat,inde,repub,assets_path
# loads database data to dataframes
def get_data_from_db():
    print('Getting the data from the database')
    demo_df=db.get_from_database(democrat)
    repub_df=db.get_from_database(repub)
    inde_df=db.get_from_database(inde)
    return demo_df,repub_df,inde_df
def prepare_data(demo_df,repub_df,inde_df):
    print('Preparing the data for model training')
    #Join and shuffle the dataframe
    df=pd.concat([demo_df,repub_df,inde_df],axis=0)
    df = shuffle(df).reset_index(drop=True).drop('id',axis=1)
    #creates x and y, x contains features and y contains labels
    x=df.drop('q15',axis=1)
    y=df['q15']
    return x,y
def model(x,y):
    print('Fitting the data to the model')
    # One hot encodes the features since all are categorical
    ohe=OneHotEncoder(sparse=False)
    x=ohe.fit_transform(x)
    #creates a decision tree classifier object
    dtc=DecisionTreeClassifier()
    #fits the decision tree classifier object on the data
    dtc.fit(x,y)
    return ohe,dtc
def save_model(ohe,dtc):
    print('Saving the model')
    #if asset path doesn't exist, create one.
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)
    # Dump the encoder and the classifer in the assets folder
    joblib.dump(dtc, assets_path+'dtclassifier')
    joblib.dump(ohe, assets_path+'encoder')
def main():
    demo_df,repub_df,inde_df=get_data_from_db()
    #checks if any dataframe is empty
    if not isinstance(demo_df,pd.DataFrame) or  not isinstance(repub_df,pd.DataFrame) or not isinstance(inde_df,pd.DataFrame):
        print('Couldnt load dataframes')
        exit(0)
    x,y=prepare_data(demo_df,repub_df,inde_df)
    ohe,dtc=model(x,y)
    save_model(ohe,dtc)

#creates a dbhandler object
db=DBhandler()
main()