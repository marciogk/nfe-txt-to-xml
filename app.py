import streamlit as st
from functions import process_txt_to_xml

st.set_page_config(page_title='txt to xml')

# Esconder o menu do Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .viewerBadge_link__1S137 {display: none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
  '''<style>
    #MainMenu{visibility: hidden;} footer{visibility: hidden;}
    #root>div:nth-child(1)>div>div>div>div>section>div{padding-top: .2rem;
  </style>''', unsafe_allow_html=True
)

# st.header("This is a header") # adds subheader
# st.subheader("This is a subheader") # adds a smaller subheader

# Título da aplicação
st.title("Conversão de NFe - TXT para XML")


# Exibir o número da versão da aplicação no canto superior esquerdo
st.markdown(
    """
    <style>
    .css-1l02zno {
        font-size: 0.8em;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Número da versão da aplicação, no canto inferior direito
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Descrição da aplicação
st.markdown(
    """
    Esta aplicação converte arquivos .txt de Notas Fiscais Eletrônicas (NF-e) em arquivos .xml.
    """
)

# Instruções para o usuário
st.markdown(
    """
    **Instruções:**
    1. Selecione um arquivo .txt de NF-e.
    2. Clique no botão "Converter para XML".
    3. Selecione a pasta onde irá salvar o arquivo .xml.
    """
)

# Botão para upload do arquivo .txt
uploaded_file = st.file_uploader("Selecione o arquivo .TXT", type="txt")


if uploaded_file is not None:
    # Leitura do conteúdo do arquivo
    file_content = uploaded_file.read().decode("utf-8")

    # se o usuário não selecionar um arquivo .txt
    if not uploaded_file.name.endswith(".txt") and not uploaded_file.name.endswith(".TXT"):
        st.error("Por favor, selecione um arquivo .txt")
        st.stop()

    # se o usuário não cancelar o upload
    if file_content == "":
        st.error("Por favor, selecione um arquivo .txt")
        st.stop()

    # Exibição do conteúdo do arquivo
    st.text_area("Conteúdo do arquivo " + uploaded_file.name, file_content, height=310)

    @st.cache_data
    def process_content(file_content):
        processed_content = process_txt_to_xml(file_content)
        return processed_content

    processed_content = process_content(file_content)
    if uploaded_file.name.endswith(".txt"):
        processed_file_name = uploaded_file.name.replace(".txt", ".xml")
    elif uploaded_file.name.endswith(".TXT"):
        processed_file_name = uploaded_file.name.replace(".TXT", ".xml")

    st.success("Arquivo processado com sucesso! Clique no botão abaixo para converter em .xml")

    st.download_button(
        label="Converter para XML",
        data=processed_content,
        file_name=processed_file_name,
        mime="application/xml"
    )
