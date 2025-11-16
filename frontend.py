import streamlit as st 

st.set_page_config(
    page_title = 'AI Database Analyzer',
    page_icon = '🤖🔥',
    layout='centered'
)

st.title('🤖AI Database Analyzer')
st.markdown('Ask your questions about your database.')

user_query = st.text_area('💬Enter your question :',placeholder='eg Compare the numbers items sold per product')

if st.button('Analyze'):
    if user_query.strip() == '':
        st.warning('Please enter a query')
    else:
        with st.spinner('Analyzing your query...'):
            answer = f'Here the analysis for your query:\n\n**{user_query}**\n\n(Replace it with your AI response)'
        st.success('Analysis Done!')
        st.markdown(answer)

st.markdown("""
    <style>
    textarea{
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html = True)
