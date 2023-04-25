import sys
import json
import mysql.connector
import csv
import os
import time

config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

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
    with open('/data/data_preprocess.csv', mode='w', newline='') as file:
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


if __name__ == '__main__':
    print(read_json('config.json'))