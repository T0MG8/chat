import streamlit as st

st.title("Database")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Een slimme trefwoord-zoek functie
def keyword_answer(question):
    q = question.lower()

    rules = [
        {
            "keywords": ["dataframe", "samenvoegen", "merge"],
            "answer": "Je kunt twee DataFrames samenvoegen met `.merge()`. Bijvoorbeeld:\n```python\ndf_merged = df1.merge(df2, on='kolomnaam')\n```"
        },
        {
            "keywords": ["dataframe", "toevoegen", "rij"],
            "answer": "Je kunt een rij toevoegen met `.loc[]` of `pd.concat()`. Bijvoorbeeld:\n```python\ndf.loc[len(df)] = [waarde1, waarde2]\n```"
        },
        {
            "keywords": ["dataframe", "kolom", "verwijderen"],
            "answer": "Gebruik `drop()` om een kolom te verwijderen:\n```python\ndf = df.drop('kolomnaam', axis=1)\n```"
        },
        {
            "keywords": ["null", "missende", "waardes", "verwijderen"],
            "answer": "Gebruik `dropna()` om rijen met missende waardes te verwijderen:\n```python\ndf = df.dropna()\n```"
        },
    ]

    for rule in rules:
        if all(keyword in q for keyword in rule["keywords"]):
            return rule["answer"]

    return "Hmm, ik weet hier (nog) geen antwoord op. Probeer het anders te formuleren!"

# React to user input
if prompt := st.chat_input("Waar heb je hulp bij?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = keyword_answer(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})