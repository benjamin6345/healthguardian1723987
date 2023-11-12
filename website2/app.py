import streamlit as st
import pickle
import numpy as np
from collections import defaultdict

st.title("HeartGuardian")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Basic Information基本資料")

    weight = st.slider("Weight體重(Kg)", 35, 200, 1)
    height = st.slider("Height高度(m)", 0.80, 2.7, 0.01)
    age = st.slider("Age年齡", 1, 140, 1)
    
    smoke = st.radio("Smoke(d)(曾)吸煙", ["Yes是", "No否"])
    drinks = st.radio("Drinks/Drank(曾)喝酒", ["Yes是", "No否"])
    
    
    
with col2:
    st.subheader("Health History健康歷史")
    stroke = st.radio("Have/Had Stroke(曾)中風", ["Yes是", "No否"])
    diabetic = st.radio("Had/Has Diabetes(曾)有糖尿病", ["Yes是", "Yes(During Pregnancy)是（當懷孕)","No否"])
    asthma = st.radio("Have/Had Asthma(曾)患哮喘", ["Yes是", "No否"])

with open("model.pkl", 'rb') as file:
    model = pickle.load(file)

def submit_actions():
    BMI = weight / (height * height)
    BMI = BMI / 35
    smoke_final = 1 if smoke == 'Yes是' else 0
    alcohol_final = 1 if drinks == 'Yes是' else 0
    age_final = age/80
    diabetic_final = 1 if diabetic == 'Yes是' else 2 if diabetic == "Yes(During Pregnancy)是（當懷孕)" else 0
    asthma_final = 1 if asthma == 'Yes是' else 0
    stroke_final = 1 if stroke == 'Yes是' else 0
    
    result = [BMI, smoke_final, alcohol_final, age_final, diabetic_final, asthma_final, stroke_final]

    arr = np.array(result).reshape(1, -1)
    y_pred = np.round(model.predict(arr))[0]
    result = 'High' if y_pred == 1 else 'Low'
    comment = 'Professional Body Checks are Recommended' if y_pred == 1 else 'Professional Body Checks are not Necessary'
    st.subheader(f'Risk of having Heart Disease: {result}')
    st.markdown(comment)
    
button = st.button("Submit提交", on_click=submit_actions)