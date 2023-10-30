import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import StackingClassifier
from sklearn.naive_bayes import GaussianNB
st.set_page_config(page_title="HNN",page_icon="logo1.png",layout="wide")
with st.sidebar:
    selected=option_menu("Menu",["Predictor"])
if (selected=="Predictor"):
        bg="""
        <style>
        [data-testid="stAppViewContainer"]>.main{
        background-image: linear-gradient(to right bottom,#FFFFFF,#87CEEB);
        background-attachment:local;
        color:#FFFFFF;
        }
        </style>"""
        title="""
        <style>
        [class="css-zt5igj e16nr0p33"]{
            color:black;
            text-align:center;
            font-weight:bold; 
            font-size:80px; 
            }
        </style>"""
        Button="""
        <style>
        [class="css-1x8cf1d edgvbvh5"]{
            width:200px;
            height:50px;
            color:white;
            background-color:green;
            text-align:center;
            display:block;
            margin: 0 auto;
            }
        </style>"""
        btext="""
        <style>
        [data-testid="stMarkdownContainer"]{
        font-size:50px;
        }
        </style>"""
        sb="""
        <style>
        [class="css-vk3wp9 e1fqkh3o11"]{
        background-image: linear-gradient(to right bottom,#FFC0CB,#FFFFFF);
        }
        </style>"""
        hide="""
        <style>
        #MainMenu{visibility:hidden;}
        footer {visibility:hidden;}
        header{visibility:hidden;}
        </style>"""
        st.markdown(hide,unsafe_allow_html=True)
        st.markdown(title,unsafe_allow_html=True)
        st.markdown(bg,unsafe_allow_html=True)
        st.markdown(Button,unsafe_allow_html=True)
        st.markdown(btext,unsafe_allow_html=True)
        st.markdown(sb,unsafe_allow_html=True)
        st.title('Health Network Navigator')
        html_code = """
        <b><marquee Scrollamount="20" behavior="alternate" loop="" height="40px" style="font-family:Verdana;font-size:20px;color:red;background-color:black;">Symptoms <span style="color:white">Pettu </span>Doctor <span style="color:white">Pattu</span></marquee></b>
        """
        st.write(html_code, unsafe_allow_html=True)
        data=pd.read_csv('class.csv')
        data=data.replace(np.nan,0)
        d={}
        for i in data.columns:
            a=np.array(data[i]).tolist()
            a=[i for i in a if i!=0]
            d[i]=a
        data2=pd.read_csv('Testing.csv')
        placeholder=st.empty()    
        with placeholder.form("entry_form",clear_on_submit=True):
            col=[]*3
            col=st.columns(3)
            k=0
            a={}
            for i in data2.columns[:-1]:
                a[i]=0
            for i in d.keys():
                if k>=3:k=0
                with col[k]:
                    st.write(f'<span style="color:pink;font-size:25px"><b>{i.capitalize()}</b></span>',unsafe_allow_html=True)
                    for j in d[i]:
                        b=st.checkbox(j.capitalize())
                        if b: 
                          a[j]=1   
                k+=1      
            b=st.form_submit_button("Predict & Navigate")
        def model(a):
            train_df = pd.read_csv("Training.csv")
            x_train = train_df[train_df.columns[:-1]]
            y_train = train_df[train_df.columns[-1]]
            rfc_mdl = RandomForestClassifier(n_estimators = 100,n_jobs = -1)
            nb_clf = GaussianNB()
            svm_clf = SVC()
            models = [("RandomForestClassifier",rfc_mdl),("NaviesBayes",nb_clf),("SupportVectorMachine",svm_clf)]
            stacking = StackingClassifier(estimators = models,final_estimator=LogisticRegression(),n_jobs = -1)
            stacking.fit(x_train,y_train)
            arr = np.array(np.array(a))
            c=stacking.predict(arr.reshape(1,-1))
            return c 
        if b:
            if all(ele == 0 for ele in list(a.values())):
                placeholder.empty() 
                st.write('<span style="font-size: 30px;"><b>Congrats <span style="color:pink;">❤</span> you are Healthy</b></span>',unsafe_allow_html=True)
            else:
                with st.spinner('Results Loading...'):
                    res=model(list(a.values())) 
                str1=''
                for i in a.keys():
                    if a[i]==1:str1=str1+i+' , '
                data1=pd.read_csv("doctors4.csv")
                data4=pd.read_csv("precaution.csv")
                link=data1[data1["Prognosis"]==res[0]]["Map_Link"]
                name=data1[data1["Prognosis"]==res[0]]["Specailist"]
                hospital=data1[data1["Prognosis"]==res[0]]["Hospital"]
                precaution=data4[data4["prognosis"]==res[0]]["Introduction"]
                remedy=data4[data4["prognosis"]==res[0]]["Remedies"] 
                placeholder.empty()    
                st.write(f'<span style="font-size:20px;color:green;">You may have <span style="font-size:25px;color:black;"><b>{res[0].capitalize()}</b></span> based on given symptoms <span style="color:red;">{str1[:-2]}</span></span>',unsafe_allow_html=True)
                st.write(f'<br><span style="font-size: 25px;color:black;"><b>{res[0].capitalize()}: </b></span><span style="font-size: 20px;color:green;">{precaution.tolist()[0]}</span>',unsafe_allow_html=True)
                st.write(f'<br><span style="font-size: 25px;color:black;"><b>The following remedies might help you:</b></span><br><span style="font-size: 20px;color:green;">{remedy.tolist()[0]}</span>',unsafe_allow_html=True)
                for i in range(len(link.tolist())):
                        st.write(f"{''.join(['-' for i in range(10)])}")
                        st.write(f'<span style="font-size: 20px;color:green;">You can consult this doctor: <span style="font-size:25px;color:black;"><b>{name.tolist()[i]}</b></span><br>at <span style="font-size:25px;color:black;"><b>{hospital.tolist()[i]}</b></span><br>for hospital address tap link <b><a href={link.tolist()[i]}><span style="font-size:25px;color:black;">Map_Link</span></a></b></span>',unsafe_allow_html=True)
                
                        
  
