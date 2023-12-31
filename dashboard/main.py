import streamlit as st
import pandas as pd 
import plotly.express as px

from utils import request

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)

def clear_cache():
    st.toast('No data, please try again')
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

if 'items' not in st.session_state:
    st.session_state['items'] = request(path='items')
    st.session_state['outlets'] = request(path='outlets')
    st.session_state['sale_reports'] = request(path='sale_reports')
    # item
    st.session_state['item_identifier'] = set([item['item_identifier'] for item in st.session_state['items']])
    st.session_state['item_weight'] = [item['item_weight'] for item in st.session_state['items']]
    st.session_state['item_fat_content'] = set([item['item_fat_content'] for item in st.session_state['items']])
    st.session_state['item_type'] = set([item['item_type'] for item in st.session_state['items']])

    # outlet
    st.session_state['outlet_identifier'] = set([item['outlet_identifier'] for item in st.session_state['outlets']])
    st.session_state['outlet_establishment_year'] = set([item['outlet_establishment_year'] for item in st.session_state['outlets']])
    st.session_state['outlet_size'] = set([item['outlet_size'] for item in st.session_state['outlets']])
    st.session_state['outlet_location_type'] = set([item['outlet_location_type'] for item in st.session_state['outlets']])
    st.session_state['outlet_type'] = set([item['outlet_type'] for item in st.session_state['outlets']])

    # sale_report
    st.session_state['item_visibility'] = [item['item_visibility'] for item in st.session_state['sale_reports']]
    st.session_state['item_mrp'] = [item['item_mrp'] for item in st.session_state['sale_reports']]
    st.session_state['item_outlet_sales'] = [item['item_outlet_sales'] for item in st.session_state['sale_reports']]

with st.sidebar:
    st.title("**CONTROL PANEL**")
    with st.form('control_panel'):
        # item
        st.header('Item')
        st.multiselect(label='select item id', options=st.session_state['item_identifier'], key='item_identifier_filter')
        st.slider('Select a range of item weight', min(st.session_state['item_weight']), max(st.session_state['item_weight']), (min(st.session_state['item_weight']), max(st.session_state['item_weight'])), key='item_weight_filter')
        st.multiselect(label='Select item fat content', options=st.session_state['item_fat_content'], key='item_fat_content_filter')
        st.multiselect(label='Select item type', options=st.session_state['item_type'], key='item_type_filter')

        st.markdown("""---""")
        # outlet
        st.header('Outlet')
        st.multiselect(label='select outlet id', options=st.session_state['outlet_identifier'], key='outlet_identifier_filter')
        st.multiselect(label='select outket establish year', options=st.session_state['outlet_establishment_year'], key='outlet_establishment_year_filter')
        st.multiselect(label='select outlet size', options=st.session_state['outlet_size'], key='outlet_size_filter')
        st.multiselect(label='select outlet location', options=st.session_state['outlet_location_type'], key='outlet_location_type_filter')
        st.multiselect(label='select outlet type', options=st.session_state['outlet_type'], key='outlet_type_filter')

        st.markdown("""---""")
        # sale_report
        st.header('Sale Report')
        st.slider('Select a range of item visibility', min(st.session_state['item_visibility']), max(st.session_state['item_visibility']), (min(st.session_state['item_visibility']), max(st.session_state['item_visibility'])), key='item_visibility_filter')
        st.slider('Select a range of item mrp', min(st.session_state['item_mrp']), max(st.session_state['item_mrp']), (min(st.session_state['item_mrp']), max(st.session_state['item_mrp'])), key='item_mrp_filter')
        st.slider('Select a range of item outlet sales', min(st.session_state['item_outlet_sales']), max(st.session_state['item_outlet_sales']), (min(st.session_state['item_outlet_sales']), max(st.session_state['item_outlet_sales'])), key='item_outlet_sales_filter')

    
        submit = st.form_submit_button("Submit")
        if submit:
            st.session_state['items'] = request(path='items', params={
                'item_identifier': st.session_state['item_identifier_filter'],
                'item_weight_min': st.session_state['item_weight_filter'][0],
                'item_weight_max': st.session_state['item_weight_filter'][1],
                'item_fat_content': st.session_state['item_fat_content_filter'],
                'item_type': st.session_state['item_type_filter'],
            })
            st.session_state['outlets'] = request(path='outlets', params={
                'outlet_identifier': st.session_state['outlet_identifier_filter'],
                'outlet_establishment_year': st.session_state['outlet_establishment_year_filter'],
                'outlet_size': st.session_state['outlet_size_filter'],
                'outlet_location_type': st.session_state['outlet_location_type_filter'],
                'outlet_type': st.session_state['outlet_type_filter']
            })
            st.session_state['sale_reports'] = request(path='sale_reports', params={
                'item_identifier': st.session_state['item_identifier_filter'],
                'outlet_identifier': st.session_state['outlet_identifier_filter'],
                'item_visibility_min': st.session_state['item_visibility_filter'][0],
                'item_visibility_max': st.session_state['item_visibility_filter'][1],
                'item_mrp_min': st.session_state['item_mrp_filter'][0],
                'item_mrp_max': st.session_state['item_mrp_filter'][1],
                'item_outlet_sales_min': st.session_state['item_outlet_sales_filter'][0],
                'item_outlet_sales_max': st.session_state['item_outlet_sales_filter'][1]
            })
            st.toast('Successed!!')

# dataframe
try:
    df_item = pd.DataFrame(st.session_state['items'])
    df_outlet = pd.DataFrame(st.session_state['outlets'])
    df_sale_report = pd.DataFrame(st.session_state['sale_reports'])
    df = pd.merge(df_sale_report, df_item, on='item_identifier', how='inner')
    df = pd.merge(df, df_outlet, on='outlet_identifier', how='inner')
    df.sort_values(by=['item_outlet_sales'], ascending=True)
except:
    # df = pd.DataFrame(columns=["item_identifier","outlet_identifier","item_visibility","item_mrp","item_outlet_sales","item_weight","item_fat_content","item_type","outlet_establishment_year","outlet_size","outlet_location_type","outlet_type"])
    clear_cache()
    st.rerun()

# tab
overview, item, outlet = st.tabs(["Overview", "Item", "Outlet"])
with overview:
    # row1
    r1_col1, r1_col2, r1_col3 = st.columns(3)
    with r1_col1:
        st.metric("Sales", "${:,.0f}".format(df['item_outlet_sales'].sum()))
    with r1_col2:
        st.metric("Num outlet", df['outlet_identifier'].nunique())
    with r1_col3:
        st.metric("Num item", df['item_identifier'].nunique())
    # row2
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        row2_pie1 = px.pie(df, values='item_outlet_sales', names='outlet_type', title='Sales by outlet type')
        st.plotly_chart(row2_pie1, theme="streamlit", use_container_width=True)
    with r2_col2:
        row2_pie2 = px.pie(df, values='item_outlet_sales', names='item_type', title='Sales by Item Type')
        st.plotly_chart(row2_pie2, theme="streamlit", use_container_width=True)
    # row3
    row3_hist = px.histogram(df.sort_values(by=['item_outlet_sales'])[-10:], x='outlet_identifier', y='item_outlet_sales', title='Sales by Outlet')
    st.plotly_chart(row3_hist, theme="streamlit", use_container_width=True)
    # row4
    row4_hist = px.histogram(df.sort_values(by=['item_outlet_sales'])[-10:], x='item_identifier', y='item_outlet_sales', title='Sales by Item')
    st.plotly_chart(row4_hist, theme="streamlit", use_container_width=True)

with item:
    # row1
    col1, col2 = st.columns(2)
    with col1:
        col1_hist1 = px.pie(df, values='item_outlet_sales', names='item_fat_content', title='Sales by Item Fat Content')
        st.plotly_chart(col1_hist1, theme="streamlit", use_container_width=True)
    with col2:
        col1_hist2 = px.pie(df, values='item_outlet_sales', names='item_type', title='Sales by Item Type')
        st.plotly_chart(col1_hist2, theme="streamlit", use_container_width=True)
    # row2
    row2_hist = px.bar(df.sort_values(by=['item_outlet_sales'])[-10:], x='outlet_type', y='item_outlet_sales', color='outlet_size', title='Top 10 Sales by Item')
    st.plotly_chart(row2_hist, theme="streamlit", use_container_width=True)
    # row3
    row3_hist = px.histogram(df, x='item_weight', y='item_outlet_sales', color='item_fat_content', marginal='rug', title='Sales by Item Type and Item Weight')
    st.plotly_chart(row3_hist, theme="streamlit", use_container_width=True)
    # row4
    row4_hist = px.histogram(df, x='item_weight', y='item_outlet_sales', color='item_fat_content', marginal='rug', title='Sales by Item Type and Item Weight')
    st.plotly_chart(row3_hist, theme="streamlit", use_container_width=True)

with outlet:
    # row1
    col1, col2, col3 = st.columns(3)
    with col1:
        col1_hist = px.pie(df, values='item_outlet_sales', names='outlet_type', title='Sales by Outlet Type')
        st.plotly_chart(col1_hist, theme="streamlit", use_container_width=True)
    with col2:
        col2_pie1 = px.pie(df, values='item_outlet_sales', names='outlet_size', title='Sales by Outlet Size')
        st.plotly_chart(col2_pie1, theme="streamlit", use_container_width=True)
    with col3:
        col3_pie2 = px.pie(df, values='item_outlet_sales', names='outlet_location_type', title='Sales by Outlet Location Type')
        st.plotly_chart(col3_pie2, theme="streamlit", use_container_width=True)
    # row2
    row2_hist = px.bar(df.sort_values(by=['item_outlet_sales'])[-10:], x='outlet_type', y='item_outlet_sales', color='outlet_size', title='Sales by Outlet type and size')
    st.plotly_chart(row2_hist, theme="streamlit", use_container_width=True)
    # row3
    row3_hist = px.bar(df.sort_values(by=['item_outlet_sales'])[-10:], x='outlet_location_type', y='item_outlet_sales', color='outlet_size', title='Sales by Outlet location and size')
    st.plotly_chart(row3_hist, theme="streamlit", use_container_width=True)
    # row4
    row4_hist = px.histogram(df, x='item_visibility', y='item_outlet_sales', color='outlet_identifier', marginal='rug', title='Sales by Outlet and Item Visibility')
    st.plotly_chart(row4_hist, theme="streamlit", use_container_width=True)
    # row5
    row5_hist = px.histogram(df, x='item_mrp', y='item_outlet_sales', color='outlet_identifier', marginal='rug', title='Sales by Outlet and Item mrp')
    st.plotly_chart(row5_hist, theme="streamlit", use_container_width=True)
