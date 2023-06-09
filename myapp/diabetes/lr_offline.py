import sys
import json
import mysql.connector
import csv
import os
import time
import numpy as np

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import pickle

import pandas as pd
import matplotlib.pyplot as plt

cur_file_path = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(cur_file_path, 'config.json')
dataset_file_path = os.path.join(cur_file_path,'data','data_preprocess.csv')
model_file_path = os.path.join(cur_file_path, 'data', 'model_fitted.sav')
confusion_matrix_file_path = os.path.join(cur_file_path, 'data', 'confusion_matrix.txt')

age_hist_file_path = os.path.join(cur_file_path, 'static', 'age_hist.png')
gender_pie_file_path = os.path.join(cur_file_path, 'static', 'gender_pie.png')
symptom_hist_file_path = os.path.join(cur_file_path, 'static', 'symptom_hist.png')


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data

def to_csv(config_file=config_file_path):
    config = read_json(config_file)

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["mysql_username"],
        password=config["mysql_password"],
        database=config["database_name"]
    )

    mycursor = mydb.cursor()
    mycursor.execute("""
        SELECT 
            diagnosis.Diagnosis_ID AS id, 
            patient.Age, 
            patient.Gender, 
            symptom.Polyuria, 
            symptom.Polydipsia, 
            symptom.sudden_weight_loss, 
            symptom.weakness, 
            symptom.Polyphagia, 
            symptom.Genital_thrush, 
            symptom.visual_blurring, 
            symptom.Itching, 
            symptom.Irritability, 
            symptom.delayed_healing, 
            symptom.partial_paresis, 
            symptom.muscle_stiffness, 
            symptom.Alopecia, 
            symptom.Obesity, 
            diagnosis.Prediction AS class
        FROM 
            diagnosis
            INNER JOIN patient ON diagnosis.Patient_ID = patient.Patient_ID
            INNER JOIN symptom ON diagnosis.Symptom_ID = symptom.Symptom_ID
    """)

    rows = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    # Creating a CSV file and writing the data to it
    with open(dataset_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing the header row
        writer.writerow(['id', 'Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden_weight_loss', 'weakness', 'Polyphagia', 'Genital_thrush', 'visual_blurring', 'Itching', 'Irritability', 'delayed_healing', 'partial_paresis', 'muscle_stiffness', 'Alopecia', 'Obesity', 'class'])
        # Writing the data rows
        for row in rows:
            writer.writerow(row)

def save_record(patient_info, config_file=config_file_path):

    # Connect to MySQL server
    config = read_json(config_file)

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["mysql_username"],
        password=config["mysql_password"],
        database=config["database_name"]
    )
    cursor = mydb.cursor()

    # Insert patient information into patient table
    add_patient = ("INSERT INTO patient "
                "(Patient_ID, Patient_Name, Age, Gender) "
                "VALUES (%s, %s, %s, %s)")
    patient_data = (patient_info['patient_id'], patient_info['patient_name'], patient_info['age'], patient_info['gender'])
    cursor.execute(add_patient, patient_data)

    # Get the symptom ID for the symptoms entered in the form
    symptom_query = "SELECT Symptom_ID FROM symptom WHERE "
    symptom_query += "Polyuria = %s AND Polydipsia = %s AND Sudden_weight_loss = %s AND Weakness = %s "
    symptom_query += "AND Polyphagia = %s AND Genital_thrush = %s AND Visual_blurring = %s "
    symptom_query += "AND Itching = %s AND Irritability = %s AND Delayed_healing = %s "
    symptom_query += "AND Partial_paresis = %s AND Muscle_stiffness = %s AND Alopecia = %s "
    symptom_query += "AND Obesity = %s"

    symptom_data = (patient_info['polyuria'], patient_info['polydipsia'], patient_info['sudden_weight_loss'], patient_info['weakness'], 
                    patient_info['polyphagia'], patient_info['genital_thrush'], 
                    patient_info['visual_blurring'], patient_info['itching'], patient_info['irritability'], 
                    patient_info['delayed_healing'], patient_info['partial_paresis'], 
                    patient_info['muscle_stiffness'], patient_info['alopecia'], patient_info['obesity'])
    cursor.execute(symptom_query, symptom_data)
    result = cursor.fetchone()
    symptom_id = result[0]

    # Insert diagnosis into diagnosis table
    add_diagnosis = ("INSERT INTO diagnosis "
                    "(Diagnosis_ID, Patient_ID, Symptom_ID, Prediction) "
                    "VALUES (%s, %s, %s, %s)")
    diagnosis_data = (int(time.time()), patient_info['patient_id'], symptom_id, patient_info['diabetes'])
    cursor.execute(add_diagnosis, diagnosis_data)

    # Commit changes and close connection
    mydb.commit()
    cursor.close()
    mydb.close()

def logistic_regression(dataset=dataset_file_path):
    # load the dataset
    data = pd.read_csv(dataset)

    # separate the features and target variable
    X = data.iloc[:, 1:-1]
    y = data.iloc[:, -1]

    # split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # create a logistic regression model
    log_reg = LogisticRegression()

    # fit the model on the training data
    log_reg.fit(X_train, y_train)

    # Predict test set labels
    y_pred = log_reg.predict(X_test) 

    # Obtain confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Save confusion matrix to file
    np.savetxt(confusion_matrix_file_path, cm, fmt='%d')

    # save the model to disk
    pickle.dump(log_reg, open(model_file_path, 'wb'))

def predict(patient_info, model=model_file_path):
    loaded_model = pickle.load(open(model, 'rb'))

    X = []
    for key, value in patient_info.items():
        X.append(value)
    print(X)
    new_X = np.array(X).reshape(1,-1)
    y_predict = loaded_model.predict(new_X)
    print(y_predict)
    return y_predict

def stat_plots(dataset=dataset_file_path):

    def age_hist_plt(file=age_hist_file_path):
        df = pd.read_csv(dataset)

        # Filter the population with class == 1
        df_class1 = df[df['class'] == 1]

        # Create a histogram of Age
        plt.hist(df_class1['Age'], bins=10, color='lightblue')

        # Add x and y axis labels and a title
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.title('Histogram of Age for population with diabetes')

        # Save the plot to a file path
        plt.savefig(file)
        plt.close()
    
    def gender_pie_plt(file=gender_pie_file_path):
        # Read the dataset
        df = pd.read_csv(dataset)

        # Replace gender values
        gender_dict = {0: 'Female', 1: 'Male'}
        df['Gender'] = df['Gender'].replace(gender_dict)

        # Filter by class == 1
        df_class1 = df[df['class'] == 1]

        # Create the pie chart
        fig, ax = plt.subplots()
        color = ['lightblue', 'pink']
        ax.pie(df_class1['Gender'].value_counts(), labels=df_class1['Gender'].value_counts().index, autopct='%1.1f%%', colors=color)
        ax.set_title('Gender Distribution for Class 1 Diabetes')

        # Add legend on the side
        ax.legend(title='Gender', loc='center left', bbox_to_anchor=(1, 0.5))

        # Save the figure
        fig.savefig(file)
        plt.close()

    def symptom_hist_plt(file=symptom_hist_file_path):
        # Read the dataset
        df = pd.read_csv(dataset)

        # Filter the rows with class == 1
        df = df[df['class'] == 1]

        # Select the symptom columns
        symptom_columns = ['Polyuria', 'Polydipsia', 'sudden_weight_loss', 'weakness', 'Polyphagia', 'Genital_thrush', 'visual_blurring', 'Itching', 'Irritability', 'delayed_healing', 'partial_paresis', 'muscle_stiffness', 'Alopecia', 'Obesity']
        symptoms = df[symptom_columns]

        # Calculate the frequency of each symptom
        freq = symptoms.sum()

        # Plot the histogram
        fig = plt.figure(figsize=(10,5))
        plt.bar(symptom_columns, freq, color='lightblue')
        plt.xticks(rotation=90)
        plt.title('Symptom frequency for diabetes')
        plt.xlabel('Symptoms')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(file)
        plt.close()

    
    age_hist_plt()
    gender_pie_plt()
    symptom_hist_plt()


if __name__ == '__main__':
    logistic_regression()