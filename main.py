import subprocess

import joblib
from democrat import Democrat
from republican import Republican
from independent import Independent
from DBhandler import DBhandler
from constants import assets_path, encoder_file, classifier_file, questions_file, counter_file, when_train
import time
import sys
from subprocess import Popen
import random
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
import os


# main class that executes the survey
class Main:
    __questions = ''
    __encoder = ''
    __model = ''
    __db = ''

    # constructor that initializes the member variables
    def __init__(self):
        self.__questions, self.__model, self.__encoder = self.__load_resources()
        self.__db = DBhandler()
        self.__get_modes()

    # functions to load the resources in the assets folder
    # Private function
    def __load_resources(self):
        questions = joblib.load(assets_path + questions_file)
        model = joblib.load(assets_path + classifier_file)
        encoder = joblib.load(assets_path + encoder_file)
        return questions, model, encoder

    # function to get the modes of the questions that haven't been answered yet from the database
    # Private function
    def __get_modes(self):
        ques_names = ['q' + str(x) for x in range(1, 16)]
        for i, x in enumerate(ques_names):
            self.__questions[i]['mode'] = self.__db.get_mode(x)

    # function to predict the party person taking the survey supports
    # Private function
    def __predict(self, answers):
        for i in range(len(answers), 14):
            answers.append(self.__questions[i]['mode'])
        encoded_answers = self.__encoder.transform([answers])
        return self.__model.predict(encoded_answers)[0]

    # menu function that displays the carries the survey
    def menu(self):
        # stores the survey answers
        answers = []
        # enumerate over all the questions
        for i, x in enumerate(self.__questions):
            # clears the terminal//works in terminal only
            os.system('cls' if os.name == 'nt' else 'clear')
            # if no question was answered don't predict anything
            if (i > 0):
                print("You are being predicted as a: " + self.__predict(answers.copy()))
            # print the question to the screen
            print(x['question'])
            # print the choices associated with the question
            for j, y in enumerate(x['choices'], start=1):
                print(str(j) + '. ' + y)
            # checks if the answer selected exists
            ans = -1
            while (ans <= 0 or ans > len(x['choices'])):
                try:
                    ans = int(input('Enter your choice: '))
                except:
                    ans = -1
            answers.append(x['choices'][ans - 1])

        check = False
        # if the user identifies as a Republican, store their data in republican table
        if answers[-1] == 'Republican':
            obj = Republican(*answers)
            check = self.__db.insert_data(obj)
        # if the user identifies as a democrat, store their data in democrat table
        elif answers[-1] == 'Democrat':
            obj = Democrat(*answers)
            check = self.__db.insert_data(obj)
        # if the user identifies as an independent, store their data in independent table
        elif answers[-1] == 'Independent':
            obj = Independent(*answers)
            check = self.__db.insert_data(obj)
        # self.__print_answers(answers)
        if check == False:
            print("Your answers will not be saved due to a database error")
        else:
            print("Your answers have been saved. Thank you for taking the survey")
        self.train_model()

    # function that trains the model once enough surveys have been done. No of surveys done is stored
    # in the counter_file and the number required to initiate the model training is in the constants folder
    def train_model(self):
        if not os.path.exists(assets_path + counter_file):
            counter = 0
            joblib.dump(counter, assets_path + counter_file)
        else:
            counter = int(joblib.load(assets_path + counter_file))
            if (counter >= when_train):
                counter = 0
                joblib.dump(counter, assets_path + counter_file)
                process = Popen(['python', 'make_model.py'], creationflags=subprocess.DETACHED_PROCESS,
                                stdin=None, stdout=None, stderr=None, close_fds=True)
            else:
                counter += 1
                joblib.dump(counter, assets_path + counter_file)
    # def __print_answers(self,answers):
    #     for i,x in enumerate(self.__questions):
    #         print(x['question'])
    #         print('Your choice: '+answers[i])


print("********Welcome to the AI automated survey********")
time.sleep(1)
main = Main()
main.menu()
