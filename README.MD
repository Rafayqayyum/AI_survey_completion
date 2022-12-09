This text file explains how to run the code.
Let's look at each file one by one

Base.py : Contains configuration code for sqlalchemy
democrat.py,republican.py,independent.py : These three files contain the classes of democrat, republican and independent which generate
the database tables needed to store the data of all three types of votes in different tables.

Constants.py : Contains all the constants used in the code. If you need to change path or change when to train a model refer this file.
DBhandler.py : This file contains the code for DB CRUD operations.
make_model.py : This file contains the code to train the classifier/model
load_to_database.py: This file contains the code to load the initial data to the database
main.py : This file contains the survey code. It trains the model after every when_train times a survey is taken.
when_train variable exists in the constants.py file.


How to run the code:

1. Open the terminal in the folder with the code and run command "pip install requirements.txt"
2. Open your database.
3. Update the username,password,and url of the database in constants.py file
4. Run the load_to_database.py script using terminal or any IDE.
5. Run the make_model.py file to create the model on the initial data.
6. Run the main.py.


How the code works?

The code reads mode of every question from the database and stores it for the future use. Then the 
classifier/model, encoder and questions are loaded from the assets. After that, the user is presented
with the questions one by one. After first question the model starts predicting the party affiliation 
of the person using question answered and the modes. As more and more questions are answered it uses
less and less modes and more of the questions answered. At the end of the survey, the data is logged
into the database and the code checks if the surveys taken counter exists or not. if it doesn't exist
it creates one in the assets. If it does exist, and it is less than when_train(which specifies after 
how many surveys the model will be trained again) then it is updated and stored. If the counter is larger
than the when_train constant then a new process is created to train the model and the main program just exits.



Why weren't the modes calculated on the basis of the questions answered by user?
This operation becomes more costly as the data size increases and the wait on terminal for the next question.
However, this can be done after there's enough data collected to test it's performance and if the model will
be used for something like an app/webapp etc because wait time there won't translate to the wait to answer the questions.
