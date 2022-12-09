from democrat import Democrat
from republican import Republican
from independent import Independent
import pandas as pd
from Base import Session,engine,Base
#Database handler class performs all the database related operations
class DBhandler:
    # initalizes the tables in the database if they don't exist
    def __init__(self):
        try:
            Base.metadata.create_all(engine)
        except:
            print("Cannot connect to database. Make sure it is up and the url provided is right")
            exit()
    #creates a session to perform CRUD operations
    def __create_session(self):
        try:
            session=Session()
            return session
        except:
            return None
    #Stores a dataframe into the database/ created to store inital data table by table
    def store_into_database(self,table,df):
        session= self.__create_session()
        if session==None:
            return False
        try:
            df.to_sql(table,engine,if_exists='append',index=False)
            session.commit()
            session.close()
            return True
        except:
            session.rollback()
            return False
    #reads the database table to a dataframe
    def get_from_database(self,table):
        session= self.__create_session()
        if session==None:
            return None
        try:
            df=pd.read_sql(table,engine)
            session.close()
            return df
        except:
            return None
    #inserts a object into the database
    def insert_data(self,obj):
        session= self.__create_session()
        if session==None:
            return False
        try:
            session.add(obj)
            session.commit()
            session.close()
            return True
        except:
            session.rollback()
            return False
    #calculates the mode of the data for assisting the predictions
    #gets the highest occuring value in a column from all the tables and calculates which value
    #occurs the maximum times
    def get_mode(self,column):
        session= self.__create_session()
        if session==None:
            return False
        demo_mode=session.execute(f'SELECT {column},count(*) FROM democrat GROUP BY {column} ORDER BY COUNT(*) DESC LIMIT 1;').fetchone()
        repub_mode=session.execute(f'SELECT {column},count(*) FROM republican GROUP BY {column} ORDER BY COUNT(*) DESC LIMIT 1;').fetchone()
        inde_mode=session.execute(f'SELECT {column},count(*) FROM independent GROUP BY {column} ORDER BY COUNT(*) DESC LIMIT 1;').fetchone()
        session.commit()
        session.close()
        dic={}
        #creates a dictionary to store count of repeating values
        for x in [demo_mode,repub_mode,inde_mode]:
            dic[x[0]]=dic.get(x[0],0)+x[1]
        # return the value that returns maximum times
        return max(dic,key=lambda x:x[1])