import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import *
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

analysis = Analyse()

st.title('Data Analysis in Mental Health Care')
sidebar = st.sidebar

def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title = title, desc = desc, data = "")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')

def viewDataset():
    st.header('Data Used in Project')
    st.dataframe(analysis.getDataframe())

def analyseCompany():
    st.header('Size of Companies')
    data = analysis.getCompanySizes()
    st.plotly_chart(plotPie(data.index, data.values))

def analyseEmployee():
    st.header('Leave Ease in Companies')
    data = analysis.getLeaveEase()
    st.plotly_chart(plotBar(data, 'title', 'xlabel', 'ylabel'))

def viewReport():
    reports = sess.query(Report).all()
    titlesList = [ report.title for report in reports ]
    selReport = st.selectbox(options = titlesList, label="Select Report")
    
    reportToView = sess.query(Report).filter_by(title = selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)

sidebar.header('Choose Your Option')
options = [ 'View Dataset', 'Analyse Company', 'Analyse Employee' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseCompany()    
elif choice == options[2]:
    analyseEmployee()