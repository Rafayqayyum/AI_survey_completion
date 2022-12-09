#contains the path of assets
assets_path='assets/'
#table names
democrat='democrat'
repub='republican'
inde='independent'
#max length of database String field
MAX_LENGTH=50
#database variables
database_name='survey'
username='root'
password=""
url='localhost'
database_url=f"mysql+pymysql://{username}:{password}@{url}/{database_name}"
#name of encoder file
encoder_file='encoder'
#classifier file
classifier_file='dtclassifier'
#file containing questions and choices(list of dictionaries, choices are in a list)
questions_file='questions'
#name of the counter file that tracks when to train the model
counter_file='counter'
#Name of the databset file
datafile='Political_Party_Identification_Dataset.csv'
#variable specifies when to train the model. In the current case the model will after 30 successful surveys
when_train=30