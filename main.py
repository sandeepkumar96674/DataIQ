# Import all the requirement libraries

import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration of the Page
st.set_page_config(
    page_title="DataIQ",
    page_icon="📊"
)

st.title(":red[DataIQ]")
st.subheader("Explore your data with :red[DataIQ]")

file = st.file_uploader("Drop your csv or  Excel File here",type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data=pd.read_excel(file)
    st.info("The file has been Uploaded Successfully",icon='✔️')
    st.dataframe(data)

    st.subheader(':rainbow[Basic information about the Dataset]')
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Toa and Bottom Rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} Rows and {data.shape[1]} Columns in the Dataset')
        st.subheader(':grey[Statistical Summary about the Dataset]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':grey[Top Rows]')
        toprows=st.slider('Number of Row you want',1,data.shape[0],key='top')
        st.dataframe(data.head(toprows))

        st.subheader(':grey[Bottom Rows]')
        bottomrows=st.slider('Number of Row you want',1,data.shape[0],key='bottom')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':grey[Data Type of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(":grey[Columns Name]")
        st.write(list(data.columns))

    st.subheader(':rainbow[Column Values to count]')
    with st.expander('Value Count'):

        col1,col2=st.columns(2)

        with col1:
            column = st.selectbox('Choose Column Names',options=list(data.columns))
        
        with col2:
            toprows = st.number_input('Top rows',min_value=1,step=1 )

        count = st.button("Count")
        if (count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)

            st.subheader('Visualization')
            graph1 = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_dark')
            st.plotly_chart(graph1)
            graph2 = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_dark')
            st.plotly_chart(graph2)
            graph3 = px.pie(data_frame=result,names=column,values='count',template='plotly_dark')
            st.plotly_chart(graph3)

    st.subheader(':red[Groupby] : Get Better Understanding of Data')
    st.write('The Groupby help you to Summarize your data by Specific Groups and Categories')

    with st.expander('Group By Your Columns'):
        col1,col2,col3 = st.columns(3)

        with col1:
            groupby_cols = st.multiselect("Choose Your column to Groupby", options = list(data.columns))

        with col2:
            operation_col = st.selectbox('Choose Column for Operation',options=list(data.columns))

        with col3:
            operation = st.selectbox('Choose Operation',options=['sum','count','max','min','mean','median'])

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()

            st.dataframe(result)

            st.subheader(':red[Data Visualization]')
            
            graph = st.selectbox('Choose your graph',options=['line','bar','scatter','pie','sunburst'])
            if(graph=='line'):
                x_axis=st.selectbox('Choose X axis',options = list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options = list(result.columns))

                color = st.selectbox('Color Information',options=[None] + list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)

            elif(graph == 'bar'):
                x_axis=st.selectbox('Choose X axis',options = list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options = list(result.columns))

                color = st.selectbox('Color Information',options=[None] + list(result.columns))
                facet_col = st.selectbox('Column information',options=[None] + list(result.columns))
                fig =px.bar(data_frame=result, x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)

            elif(graph == 'scatter'):
                x_axis=st.selectbox('Choose X axis',options = list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options = list(result.columns))

                color = st.selectbox('Color Information',options=[None] + list(result.columns))
                size = st.selectbox('Size Column',options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)

            elif(graph== 'pie'):
                values = st.selectbox('Choose Numerical Values',options=list(result.columns))
                name = st.selectbox('Choose Labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,labels=name)
                st.plotly_chart(fig)

            elif(graph == 'sunburst'):
                path = st.multiselect('Choose your path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)

st.caption("Created by :red[Sandeep] ✨")

sc= st.button(
    "Get Connect" 
)

if sc==True:
    st.write("(https://www.linkedin.com/in/the-sandeep-kumar) ")