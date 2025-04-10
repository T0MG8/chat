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
            "keywords": ["dataframe", "samenvoegen", "merge", "hoe voeg", "samengaan", "combineer", "merge"],
            "answer": "Je kunt twee DataFrames samenvoegen met `.merge()`. Bijvoorbeeld:\n```python\ndf_merged = df1.merge(df2, on='kolomnaam')\n```"
        },
        {
            "keywords": ["dataframe", "toevoegen", "rij", "hoe voeg", "nieuwe rij", "rij toevoegen"],
            "answer": "Je kunt een rij toevoegen met `.loc[]` of `pd.concat()`. Bijvoorbeeld:\n```python\ndf.loc[len(df)] = [waarde1, waarde2]\n```"
        },
        {
            "keywords": ["dataframe", "kolom", "verwijderen", "hoe verwijder", "kolom verwijderen", "verwijder kolom"],
            "answer": "Gebruik `drop()` om een kolom te verwijderen:\n```python\ndf = df.drop('kolomnaam', axis=1)\n```"
        },
        {
            "keywords": ["null", "missende", "waardes", "verwijderen", "hoe verwijder", "null waarden", "leeg", "dropna"],
            "answer": "Gebruik `dropna()` om rijen met missende waardes te verwijderen:\n```python\ndf = df.dropna()\n```"
        },
        {
            "keywords": ["dataframe", "kolom", "toevoegen", "hoe voeg", "kolom toevoegen"],
            "answer": "Gebruik `df['nieuwe_kolom'] = waarde` om een kolom toe te voegen. Bijvoorbeeld:\n```python\ndf['leeftijd_plus_1'] = df['leeftijd'] + 1\n```"
        },
        {
            "keywords": ["dataframe", "filteren", "selecteren", "hoe filter", "voorwaarde", "filteren op"],
            "answer": "Gebruik een voorwaarde binnen `[]` om te filteren. Bijvoorbeeld:\n```python\nfiltered_df = df[df['leeftijd'] > 30]\n```"
        }
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