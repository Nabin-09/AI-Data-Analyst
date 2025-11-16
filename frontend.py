# frontend.py - Complete Updated Code

import streamlit as st 
from backend import get_data_from_database
import pandas as pd

st.set_page_config(
    page_title='AI Database Analyzer',
    page_icon='🤖🔥',
    layout='centered'
)

st.title('🤖 AI Database Analyzer')
st.markdown('Ask your questions about your database using natural language.')

user_query = st.text_area(
    '💬 Enter your question:', 
    placeholder='e.g., Show me the top 10 products by revenue'
)

if st.button('🔍 Analyze', type='primary'):
    if user_query.strip() == '':
        st.warning('⚠️ Please enter a query')
    else:
        with st.spinner('🤔 Analyzing your query...'):
            response = get_data_from_database(user_query)
            
        if response['success']:
            st.success('✅ Analysis Done!')
            
            # Display the generated SQL query
            with st.expander("📝 Generated SQL Query"):
                st.code(response['query'], language='sql')
            
            # Display results with column names
            if response['data']:
                df = pd.DataFrame(response['data'], columns=response['columns'])
                
                st.subheader("📊 Query Results")
                st.dataframe(df, use_container_width=True)
                
                # Show summary
                st.caption(f"**Total records returned:** {len(df)}")
                
                # Optional: Download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv",
                )
            else:
                st.info('ℹ️ Query executed successfully but returned no results.')
        else:
            st.error(f"❌ Error: {response['error']}")
            if response['query']:
                with st.expander("📝 Generated SQL Query (Failed)"):
                    st.code(response['query'], language='sql')

# Custom CSS
st.markdown("""
    <style>
    textarea {
        font-size: 16px !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)
