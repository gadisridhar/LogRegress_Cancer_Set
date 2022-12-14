# -*- coding: utf-8 -*-
"""LogisticRegression_Explained.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lK9dmtD3Q3IgaLILWw0lFMfRaqpEhSCX
"""

#pip install category_encoders

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, auc, accuracy_score, classification_report, ConfusionMatrixDisplay, plot_roc_curve, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
import matplotlib.pyplot as plt
import seaborn as sns
import category_encoders as ce

df = pd.read_csv('/content/sample_data/cancer.csv')

df.tail(5)

df.describe()

df.columns

df['diagnosis'].value_counts()

df['radius_mean'].isnull().sum()

#plotting the Y Variable category data
sns.countplot(x='diagnosis', data=df, palette='hls')
plt.show()

#checking the class imbalance with code

M_case_Count = len(df[df['diagnosis']=='M'])
B_case_Count = len(df[df['diagnosis']=='B'])
MPercentage = M_case_Count/(M_case_Count+B_case_Count)
BPercentage = B_case_Count/(M_case_Count+B_case_Count)
print("percentage of Diagnosis M is", MPercentage*100)
print("percentage of Diagnosis B is", BPercentage*100)

# Checking for INFLUENCE IN Y VARIABLE GIVEN THE X VARIABLES DATA
df.groupby('diagnosis').mean()

# Patients with Diagnosis Malign and Benign
# A malign tumor has irregular borders and grows faster than a benign tumor seen from the Variables 'perimeter_worst' and  'area_worst'
# Other Stats can also be read

df = df.drop(columns=['id'], axis=0)

df.head(5)

df['diagnosis'].replace(['M','B'], [1,0], inplace = True)

df

X = df.iloc[:, :30].values

print(X.shape)
print(type(X))
print(X)

y = df.iloc[:, 30].values

print(y.shape)
print(type(y))
print(y)

X_train, X_test, y_train, y_test =  train_test_split(X,y, test_size=.3, random_state=42)

print(X_train.shape)
print(X_test.shape)
print("----------------------")
print(y_train.shape)
print(y_test.shape)

dfTrain = pd.DataFrame(X_train)
dfTrain.head(5)

dfTest = pd.DataFrame(X_test)
dfTest.head(5)

#Scale them to Make all the Data units same using Standard Scaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

dfTrainScaled = pd.DataFrame(X_train)
dfTrainScaled.head(5)

dfTestScaled = pd.DataFrame(X_test)
dfTestScaled.head(5)

lr = LogisticRegressionCV(max_iter=500)

lr.fit(X_train,y_train)

testPredict = lr.predict(X_test)
trainPredict = lr.predict(X_train)

scoreTest = accuracy_score(y_test,testPredict)
print(scoreTest)

scoreTrain = accuracy_score(y_train,trainPredict)
print(scoreTrain)

# Predicting one value based on any 1 Input from TEST Data, COnsidering first sample
print(lr.predict(X_test[0].reshape(1,-1)))

# PREDITING RESULTS FOR FIRST 20 SAMPLES FROM TRAIN DATA and validate the results from TRAIN DATA ABOVE
print(lr.predict(X_train[0:20]))
#0 0 0 0 0 1 0 0 0 0
#0 0 1 1 1 0 0 1 0 1

# PREDITING RESULTS FOR FIRST 20 SAMPLES FROM TRAIN DATA and validate the results from TEST DATA ABOVE
print(lr.predict(X_test[0:20]))
#0 1 1 0 0 1 1 1 0 0
#0 1 0 1 0 1 0 0 0 1

cmTESTDATA = confusion_matrix(y_test,testPredict)
print(cmTESTDATA)

plt.figure(figsize=(10,10))
sns.heatmap(cmTESTDATA, annot=True, cmap='Blues_r', square=True)
plt.ylabel("Predicted Values")
plt.xlabel("Actual Values")
all_title = 'Accuracy Score: {0}'.format(scoreTest)
plt.title(all_title,  size=20)

cmTRAINDATA = confusion_matrix(y_train,trainPredict)
print(cmTRAINDATA)

plt.figure(figsize=(10,10))
sns.heatmap(cmTRAINDATA, annot=True, cmap='Blues_r', square=True)
plt.ylabel("Predicted Values")
plt.xlabel("Actual Values")
all_title = 'Accuracy Score: {0}'.format(scoreTrain)
plt.title(all_title,  size=20)

#  REPORT FOR TEST
classreportTestData=  classification_report(y_test,testPredict)
print(classreportTestData)

#  REPORT FOR TRAIN DATA
classreportTrainData=  classification_report(y_train,trainPredict)
print(classreportTrainData)

#MY FAV ROC CURVE FOR  MODEL ACCURACY VALIDATION
# TRAIN AND TEST DATA GETTING TPR AND FPR WITH ROC_CURVE FUNCTION
Y_PredProba_train = lr.predict_proba(X_train)
Y_PredProba_test = lr.predict_proba(X_test)

# GET THE SIMILARITY(TPR) AND 1-SPECIFICITY(FPR) TO FIND THE ROC SCORE FOR TRAIN DATA AND TEST DATA
fprTrain,tprTrain,thresholdTrain = roc_curve(y_train, Y_PredProba_train[:,1], pos_label=1)
fprTest,tprTest,thresholdTest = roc_curve(y_test, Y_PredProba_test[:,1], pos_label=1)

#plot roc curves
plt.plot(fprTest, tprTest, linestyle='--',color='red', label='ROC validation for Test Data')
plt.plot(fprTrain, tprTrain, linestyle='--',color='green', label='ROC validation for Train Data')
#plt.plot(p_fpr, p_tpr, linestyle='--', color='blue')
# title
plt.title('TEST DATA - TRAIN DATA - ROC curve')
# x label
plt.xlabel('False Positive Rate - (1-Specificity)')
# y label
plt.ylabel('True Positive rate - (Sensitivity)')
plt.legend(loc='best')
plt.savefig('ROC',dpi=300)
plt.show();

#THE MODEL GIVES BEST RESULT WHEN IT CURVE COVERS MAX AREA UNDER THE CURVE