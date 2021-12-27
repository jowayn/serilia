import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode

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
