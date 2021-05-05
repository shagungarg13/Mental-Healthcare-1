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
st.image('logo.jpg')
st.markdown("---")
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
    dataframe = analysis.getDataframe()

    with st.spinner("Loading Data..."):
        st.dataframe(dataframe)

        st.markdown('---')
        cols = st.beta_columns(4)
        cols[0].markdown("### No. of Rows :")
        cols[1].markdown(f"# {dataframe.shape[0]}")
        cols[2].markdown("### No. of Columns :")
        cols[3].markdown(f"# {dataframe.shape[1]}")
        st.markdown('---')

        st.header('Summary')
        st.dataframe(dataframe.describe())
        st.markdown('---')

        types = {'object' : 'Categorical', 'int64': 'Numerical', 'float64': 'Numerical'}
        types = list(map(lambda t: types[str(t)], dataframe.dtypes))
        st.header('Dataset Columns')
        for col, t in zip(dataframe.columns, types):
            st.markdown(f"### {col}")
            cols = st.beta_columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"# {dataframe[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")


def analyseResponses():
    with st.spinner("Loading Data..."):
        st.header('Size of Companies')
        data = analysis.getCompanySizes()
        st.plotly_chart(plotPie(data.index, data.values))

        st.header('No. of Respondents')
        st.image('plotImages/techvnon-tech.png')

        st.header('Gender Distribution')
        st.image('plotImages/gender.png')

        st.header('No. of Respondents')
        st.image('plotImages/company.png')

def analyseMentalHealth():
    with st.spinner("Loading Data..."):
        st.header('Leave Ease in Companies')
        data = analysis.getLeaveEase()
        st.plotly_chart(plotBar(data, 'title', 'xlabel', 'ylabel'))

        st.header('Employees having mental health disorders at Present')
        st.image('plotImages/mental_health_now.png')

        st.header('Employees having mental health disorders at Past')
        st.image('plotImages/mental_health_past.png')

        st.header('Are Companies taking Employee Mental Health issue Seriously?')
        st.image('plotImages/company.png')

        st.header('Discussing Mental Health at Work')
        st.image('plotImages/discuss_health.png')

        st.image('plotImages/career.png')

        st.image('plotImages/share.png')

sidebar.header('Choose Your Option')
options = [ 'View Dataset', 'Analyse Company', 'Analyse Employee' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseResponses()    
elif choice == options[2]:
    analyseMentalHealth()