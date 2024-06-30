import streamlit as st
from functions import process_txt_to_xml

st.set_page_config(page_title='Delta Informática', page_icon=':money_with_wings:')

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


# Título da aplicação
st.title("Conversão de NFe - TXT para XML")


# Exibir o número da versão da aplicação no canto superior esquerdo
st.markdown(
    """
    <style>
    .css-10trblm {
        position: fixed;
        top: 10px;
        left: 10px;
    }
    </style>
    <div class="css-10trblm">Versão 1.02</div>
    """,
    unsafe_allow_html=True
)

# # Obter o IP do usuário
# ip_address = st.empty()
# ip_address.markdown(
#     """
#     <style>
#     .css-10trblm {
#         position: fixed;
#         top: 10px;
#         right: 10px;
#     }
#     </style>
#     <div class="css-10trblm">IP: {}</div>
#     """.format(st.session_state.get('ip_address', 'Unknown')),
#     unsafe_allow_html=True
# )

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
    1. Selecione um arquivo .txt de NF-e clicando no botão <Browse files>.
    2. Verifique o conteúdo do arquivo.
    3. Clique no botão <Converter para XML>.
    4. Selecione a pasta onde irá salvar o arquivo .xml.
    5. Clique no 'X' à direita do nome do arquivo .txt para reiniciar.
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
    st.text_area("Conteúdo do arquivo " + uploaded_file.name, file_content, height=155)
    # st.balloons()

    @st.cache_data
    def process_content(file_content):
        processed_content = process_txt_to_xml(file_content)
        return processed_content

    processed_content = process_content(file_content)
    if uploaded_file.name.endswith(".txt"):
        processed_file_name = uploaded_file.name.replace(".txt", ".xml")
    elif uploaded_file.name.endswith(".TXT"):
        processed_file_name = uploaded_file.name.replace(".TXT", ".xml")

    st.info("Arquivo processado com sucesso! Clique no botão abaixo para converter em .xml")

    # st.balloons()
    # st.snow()

    st.download_button(
        label="Converter para XML",
        data=processed_content,
        file_name=processed_file_name,
        mime="application/xml"
    )

    # color = st.color_picker("Pick A Color", "#00f900")
    # st.write("The current color is", color)
