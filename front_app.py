import streamlit as st
import pandas as pd
from indexing.indexing_data import IndexingPdfData
from q_and_a.q_and_a import QAndA


@st.cache_resource(show_spinner="Analyse des documents en cours...")  
def load_q_and_a(selection):
    index = None
    index = IndexingPdfData(selection)
    index.parse_all_pdf()
    index.create_vector_database()
    q_and_a = QAndA(index)
    return q_and_a

reponse = None

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        column_order=("Select", "title", "type", "content", "file_name"),
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)


def get_html_with_hover_for_selection(selection):
    html = '<h5>Liste des documents utilises pour la recherche :</h5><ul>'
    for _, row in selection.iterrows():
        html += '<li><div title="'
        html += row["content"].replace(";", ",")
        html +='">'
        html += row["file_name"]
        html += '</div>'
    html += '</ul>'
    return html


st.markdown("""<style>
            h1 {
                text-align:center;
            }
            .st-emotion-cache-13ln4jf {
                padding:1rem 1rem 10rem;
            }
            .st-emotion-cache-12fmjuu.ezrtsby2 {
                display: none;
                height: 0;
            }
            </style>""", unsafe_allow_html=True)

st.markdown("<h1>Enedis RAG</h1>", unsafe_allow_html=True)

intro = """
<p>
    Cette appication permet d'explorer les documents de reference d'Enedis et de poser des questions par rapport au contenu de ces documents
</p>"""

st.markdown(intro, unsafe_allow_html=True)

# Selection des documents
df = pd.read_csv("documents_enedis.csv", index_col=0)
filters = st.multiselect("Type de document Enedis pour filtrer", list(set(df["type"].to_list())), default=None, placeholder="Choose an option", disabled=False, label_visibility="visible")
df_filter = df.query("type == @filters")
selection = dataframe_with_selections(df_filter)


# Formulaire envoie
with st.form("Try the program !"):
    st.markdown(get_html_with_hover_for_selection(selection), unsafe_allow_html=True)
    query = st.text_input("Quelle est votre question sur les documents ?")
    s_state = st.form_submit_button("Envoyer !")
    if s_state:
        if query == "":
            st.warning("Merci de poser une question !")
        else:
            with st.spinner("Merci de patienter pour le traitement de la question..."):
                q_and_a = load_q_and_a(selection)
                reponse = q_and_a.ask_question(query)
            st.success("Question traitee")


if reponse is not None:
    st.divider()
    st.markdown(f"""
    <strong>Question: </strong><br>
    {reponse["question"]}<br><br>
    <strong>Reponse: </strong><br>
    {reponse["output_text"]}
    """, unsafe_allow_html=True)
