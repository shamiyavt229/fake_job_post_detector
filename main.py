import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
df=pd.read_csv("data/fake_job_postings.csv")

#print(df.head())
#print(df.info())


#-------------------finding missing values---------------------------#
#print(df.isnull().sum())
#print(df[df["description"].isnull()])
#print(df.loc[df["description"].isnull(),"title"])
#print(df[df["industry"].isnull()].head())
#print(df[df["industry"].isnull()])
df = df.dropna(subset=["description"])
# drop rows with missing target values
df = df.dropna(subset=["fraudulent"])
#print(df.isnull().sum())
x=df["description"]
y=df["fraudulent"]
#------------------------preprocessing----------------------------------#
def clean_text(text):
  text=text.lower()
  text=re.sub(r"[^\w\s]","",text)
  text=re.sub(r"\s+"," ",text)
  text=text.strip()
  return text

x=x.apply(clean_text)

#print(x.isnull().sum())
#print(x.head())

#-------------------------split the data---------------------------------------#
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=43,stratify=y) 
#--------------------feature extraction----------------------------------------#
vectorizer=TfidfVectorizer()
x_train=vectorizer.fit_transform(x_train)
x_test=vectorizer.transform(x_test)
#--------------------------train the model----------------------------------------#
model=LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(x_train,y_train)
#--------------------------testing-----------------------------------------------#
#------------------------prediction----------------------------------------------#
y_predict=model.predict(x_test)
#--------------------------checking accuracy-------------------------------------#
accuracy=accuracy_score(y_test,y_predict)
print(accuracy)
cm=confusion_matrix(y_test,y_predict)
print(cm)
cr=classification_report(y_test,y_predict)
print(cr)
#-------------------------testing the model----------------------------------#
#new_job = [ "Work from home and earn ₹50,000 per week. No experience required. Immediate joining. Limited vacancies. Registration fee required before starting. Apply now!"]
#new_job_vectorizer=vectorizer.transform(new_job)
#prediction_job=model.predict(new_job_vectorizer)
#if prediction_job[0] == 0:
 # print("genuine")
#else:
 # print("fraudulent")
 #------------------------saving the vectorizer and model into a file--------------------#
with open("fake_job_model.pkl", "wb") as file:
  pickle.dump(model,file)
with open("tfidf_vectorizer.pkl", "wb") as file:
  pickle.dump(vectorizer,file)

