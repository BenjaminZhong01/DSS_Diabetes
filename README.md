# Early-Stage Diabetes Diagnosis

## Context
Diabetes, specifically type 2 diabetes,  is an endocrinological disorder that often presents without symptoms or nonspecific symptoms. Patients may present late, and therefore are at risk of developing complications of different body systems, such as eyes (diabetic retinopathy), kidneys (diabetic nephropathy), or peripheral nerves (mononeuritis multiplex). Early diagnosis and intervention is key in reducing complications and therefore improving patient prognosis. The CDSS will utilize advanced data mining methods to predict patient risk of diabetes.

## Objective
The aim is to develop a CDSS using the Early stage diabetes risk prediction dataset to provide personalized recommendations and guidance for patients. The screening tool takes in patients’ individual factors and self-reported symptoms. It predicts the likelihood of diabetes, and tracks their risk of diabetes over time and prompts users to seek medical attention. 

## Data Input
The system would require users to input basic demographic information such as age, gender, typical symptoms of diabetes from the UCI Machine Learning Repository, from the “Early stage diabetes risk prediction dataset data set” (https://archive.ics.uci.edu/ml/machine-learning-databases/00529/)

## Project Components
Analytics engine: The prediction tool will utilize supervised machine learning to classify patient risk of diabetes, where the input is a number of symptoms and patient background, and the output is the algorithm’s binary prediction on diabetes risk. The engine will rely on good data science and data mining principles to ensure good model fit, including but not limited to:
-	Data split: Split into test-train-validation sets;
-	Class imbalance: Oversampling methods to mitigate class imbalance; and utilization of explainability and interpretability methods such as SHAPley values;
-	Modeling: Supervised learning classification methods such as logistic regression, random forest classifier, and XGBoost;
-	Monitoring and Feedback: The system could also allow users to track their progress over time by providing regular feedback on their risk factors, if there are any concerning changes in their health status, prompting the user to seek medical attention if necessary.
User interface (UI): Users will interact with the tool through a simple web interface that is easy to use and navigate. In designing the UI, we will develop storyboards and personas, and list out key traits of primary user group. We will design the UI to match the persona.

## Summary
In summary, a decision support system for early stage diabetes risk prediction could help individuals understand their risk of developing diabetes and provide personalized recommendations to reduce their risk through lifestyle modifications. This could ultimately improve their health outcomes and reduce the burden of diabetes on healthcare systems.

