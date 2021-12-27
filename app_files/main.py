import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode

df_template = pd.DataFrame(
    '',
    index=range(10),
    columns=['srcip','sport','dstip','dsport','sttl','dttl','tcprtt','synack','ct_state_ttl','Label']
)

with st.form('example form') as f:
    st.header('Submit IP Entry')
    response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=True)
    st.form_submit_button()

st.subheader("Submitted Data")
st.write(response['data'])  

@st.cache()
def get_data_ex7():
    df = pd.read_csv("xy_split0_b.csv")
    return df

data = get_data_ex7()

st.subheader("Edit Data")
gb = GridOptionsBuilder.from_dataframe(data)
#make all columns editable
gb.configure_columns(['srcip','sport','dstip','dsport','sttl','dttl','tcprtt','synack','ct_state_ttl','Label'], editable=True)


js = JsCode("""
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;
    
    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    api.flashCells({
      rowNodes: [rowNode],
      columns: [col],
      flashDelay: 10000000000
    });

};
""")
gb.configure_grid_options(onCellValueChanged=js) 
go = gb.build()
st.markdown("""

""")

ag = AgGrid(data, gridOptions=go,  key='grid1', allow_unsafe_jscode=True, reload_data=False)

st.subheader("Returned Data")
st.dataframe(ag['data'])

st.subheader("Concatenated Data")

def get_df1():
    df_temp = response['data']
    df_temp = df_temp.astype(str)
    df1 = pd.DataFrame(df_temp)
    return df1

def get_df2():
    df2 = pd.DataFrame(ag['data'])
    df2 = df2.astype(str)
    return df2

df1 = get_df1()
df2 = get_df2()
df3 = pd.concat([df1,df2])
st.dataframe(df3)
