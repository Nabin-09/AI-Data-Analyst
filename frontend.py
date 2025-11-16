import streamlit as st 
from backend import get_data_from_database  # FIX: Import from backend instead of main
import pandas as pd

st.set_page_config(
    page_title='AI Database Analyzer',
    page_icon='🤖🔥',
    layout='centered'
)

st.title('🤖AI Database Analyzer')
st.markdown('Ask your questions about your database.')

user_query = st.text_area('💬Enter your question:', placeholder='eg Compare the numbers items sold per product')

if st.button('Analyze'):
    if user_query.strip() == '':
        st.warning('Please enter a query')
    else:
        with st.spinner('Analyzing your query...'):
            response = get_data_from_database(user_query)
            
        # FIX: Handle response properly
        if response['success']:
            st.success('Analysis Done!')
            
            # Display the generated SQL query
            with st.expander("📝 Generated SQL Query"):
                st.code(response['query'], language='sql')
            
            # Display results
            if response['data']:
                # Convert to DataFrame for better display
                df = pd.DataFrame(response['data'])
                st.dataframe(df, use_container_width=True)
            else:
                st.info('Query executed successfully but returned no results.')
        else:
            st.error(f"❌ Error: {response['error']}")
            if response['query']:
                with st.expander("📝 Generated SQL Query (Failed)"):
                    st.code(response['query'], language='sql')

st.markdown("""
    <style>
    textarea{
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)
