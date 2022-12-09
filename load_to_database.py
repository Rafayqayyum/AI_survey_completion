#This file loads the data to the database from the csv starting file.
from DBhandler import DBhandler
import joblib
import os
import pandas as pd
from constants import assets_path,democrat,repub,inde
from sqlalchemy_utils import create_database, database_exists
from constants import database_url,questions_file,datafile

#Checks if the database exists, if it doesn't it creates the database
def create_db():
    try:
        if not database_exists(database_url):
            print("Database doesn't exist yet. Creating one.")
            create_database(database_url)
    except Exception as e:
        print(str(e))
        exit()

def read_data():
    #generates the new column names for the data
    names=['q'+str(x) for x in range(1,16)]
    #opens the csv file in a dataframe
    df=pd.read_csv(datafile,names=names)
    #gets the questions from the dataset
    questions=df.iloc[0].to_list()
    #drops the questions from the database
    df=df.drop(axis=0,index=0)
    return df,questions,names

def org_questions(questions,names,df):
    questions_dict=[]
    #loop to get a list of dictionaries which contains question and choices
    for x in range(0,15):
        temp={}
        temp['question']=questions[x]
        temp['choices']=list(df[names[x]].unique())
        questions_dict.append(temp)
    return questions_dict
def split_dataset(df):
    #seperates the dataframe on the basis of the label
    demo_df=df[df['q15']=='Democrat'].reset_index(drop=True)
    repub_df=df[df['q15']=='Republican'].reset_index(drop=True)
    inde_df=df[df['q15']=='Independent'].reset_index(drop=True)
    return demo_df,repub_df,inde_df

def save_questions(questions_dict):
    #checks if the asset path exists else it creates one
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)
    #dumps the question list of dicionaries in the assets folder
    joblib.dump(questions_dict,assets_path+questions_file)

def save_data(demo_df,repub_df,inde_df):
    db=DBhandler()
    ##stores the dataframes in their own tables
    flag=db.store_into_database(democrat,demo_df)
    if flag==False:
        print('Error loading democrat data into database due to connection error.')
    flag=db.store_into_database(repub,repub_df)
    if flag==False:
        print('Error loading republican data into database due to connection error.')
    flag=db.store_into_database(inde,inde_df)
    if flag==False:
        print('Error loading independent data into database due to connection error.')

def main():
    print("Checking database.")
    create_db()
    print('Reading the data from the file...')
    df,questions,names=read_data()
    print('Extracting the questions from the file.')
    questions_dict=org_questions(questions,names,df)
    print('Preparing the data to push it into the database.')
    demo_df,repub_df,inde_df=split_dataset(df)
    print('Saving the questions into the assets folder')
    save_questions(questions_dict)
    print('Saving the data to the database')
    save_data(demo_df,repub_df,inde_df)

if __name__=="__main__":
    main()
