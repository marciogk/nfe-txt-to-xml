import streamlit as st
import xml.etree.ElementTree as ET
import os


def create_element(parent, tag, text=None, attrib={}):
    element = ET.SubElement(parent, tag, attrib)
    if text:
        element.text = text
    return element


def process_txt_to_xml(txt_path, xml_path):
    with open(txt_path, 'r') as file:
        lines = file.readlines()

    ET.register_namespace('', "http://www.portalfiscal.inf.br/nfe")
    nfeProc = ET.Element('nfeProc', attrib={'xmlns': "http://www.portalfiscal.inf.br/nfe", 'versao': '4.00'})
    NFe = create_element(nfeProc, 'NFe', attrib={'xmlns': "http://www.portalfiscal.inf.br/nfe"})
    infNFe = create_element(NFe, 'infNFe', attrib={'versao': '3.10', 'Id': 'NFe510500042420035722343256826829877'})

    det_counter = 1  # Contador para elementos <det>

    for line_number, line in enumerate(lines, start=1):
        parts = line.strip().split('|')

        if parts[0] == 'A':
            # Informações do documento
            pass  # Esses dados não estão explicitamente no exemplo de XML fornecido

        elif parts[0] == 'B':
            ide = create_element(infNFe, 'ide')
            create_element(ide, 'cUF', parts[1])
            create_element(ide, 'cNF', parts[2])
            create_element(ide, 'natOp', parts[3])
            create_element(ide, 'indPag', '2')
            create_element(ide, 'mod', parts[4])
            create_element(ide, 'serie', parts[5])
            create_element(ide, 'nNF', parts[6])
            create_element(ide, 'dhEmi', parts[7])
            create_element(ide, 'dhSaiEnt', parts[8])
            create_element(ide, 'tpNF', parts[9])
            create_element(ide, 'idDest', parts[10])
            create_element(ide, 'cMunFG', parts[11])
            create_element(ide, 'tpImp', parts[12])
            create_element(ide, 'tpEmis', parts[13])
            create_element(ide, 'cDV', parts[14])
            create_element(ide, 'tpAmb', parts[15])
            create_element(ide, 'finNFe', parts[16])
            create_element(ide, 'indFinal', parts[17])
            create_element(ide, 'indPres', parts[18])
            create_element(ide, 'procEmi', parts[19])
            create_element(ide, 'verProc', parts[20])

        elif parts[0] == 'C':
            if len(parts) < 15:
                print(f"Erro na linha {line_number}: esperados 15 campos, mas encontrados {len(parts)}")
                continue  # Pular para a próxima linha se não houver campos suficientes
            emit = create_element(infNFe, 'emit')
            create_element(emit, 'CNPJ', parts[1])
            create_element(emit, 'xNome', parts[2])
            create_element(emit, 'xFant', parts[3])
            enderEmit = create_element(emit, 'enderEmit')
            create_element(enderEmit, 'xLgr', parts[4])
            create_element(enderEmit, 'nro', parts[5])
            create_element(enderEmit, 'xBairro', parts[6])
            create_element(enderEmit, 'cMun', parts[7])
            create_element(enderEmit, 'xMun', parts[8])
            create_element(enderEmit, 'UF', parts[9])
            create_element(enderEmit, 'CEP', parts[10])
            create_element(enderEmit, 'cPais', parts[11])
            create_element(enderEmit, 'xPais', parts[12])
            create_element(emit, 'IE', parts[13])
            create_element(emit, 'CRT', parts[14])

        elif parts[0] == 'E':
            if len(parts) < 13:
                print(f"Erro na linha {line_number}: esperados 13 campos, mas encontrados {len(parts)}")
                continue
            dest = create_element(infNFe, 'dest')
            create_element(dest, 'idEstrangeiro', parts[1])
            create_element(dest, 'xNome', parts[2])
            enderDest = create_element(dest, 'enderDest')
            create_element(enderDest, 'xLgr', parts[3])
            create_element(enderDest, 'nro', parts[4])
            create_element(enderDest, 'xCpl', parts[5])
            create_element(enderDest, 'xBairro', parts[6])
            create_element(enderDest, 'cMun', parts[7])
            create_element(enderDest, 'xMun', parts[8])
            create_element(enderDest, 'UF', parts[9])
            create_element(enderDest, 'cPais', parts[10])
            create_element(enderDest, 'xPais', parts[11])
            create_element(dest, 'indIEDest', parts[12])

        elif parts[0] == 'H':
            det = create_element(infNFe, 'det', attrib={'nItem': str(det_counter)})
            det_counter += 1

        elif parts[0] == 'I':
            if len(parts) < 15:
                print(f"Erro na linha {line_number}: esperados 15 campos, mas encontrados {len(parts)}")
                continue
            prod = create_element(det, 'prod')
            create_element(prod, 'cProd', parts[1])
            create_element(prod, 'cEAN', parts[2])
            create_element(prod, 'xProd', parts[3])
            create_element(prod, 'NCM', parts[4])
            create_element(prod, 'CFOP', parts[5])
            create_element(prod, 'uCom', parts[6])
            create_element(prod, 'qCom', parts[7])
            create_element(prod, 'vUnCom', parts[8])
            create_element(prod, 'vProd', parts[9])
            create_element(prod, 'cEANTrib', parts[10])
            create_element(prod, 'uTrib', parts[11])
            create_element(prod, 'qTrib', parts[12])
            create_element(prod, 'vUnTrib', parts[13])
            create_element(prod, 'indTot', parts[14])

        elif parts[0] == 'N':
            imposto = create_element(det, 'imposto')

        elif parts[0] == 'N10':
            if len(parts) < 7:
                print(f"Erro na linha {line_number}: esperados 7 campos, mas encontrados {len(parts)}")
                continue
            ICMS = create_element(imposto, 'ICMS')
            ICMSSN500 = create_element(ICMS, 'ICMSSN500')
            create_element(ICMSSN500, 'orig', parts[1])
            create_element(ICMSSN500, 'CSOSN', parts[2])
            create_element(ICMSSN500, 'vBCSTRet', parts[3])
            create_element(ICMSSN500, 'pST', parts[4])
            create_element(ICMSSN500, 'vICMSSubstituto', parts[5])
            create_element(ICMSSN500, 'vICMSSTRet', parts[6])

        elif parts[0] == 'N11':
            if len(parts) < 2:
                print(f"Erro na linha {line_number}: esperados 2 campos, mas encontrados {len(parts)}")
                continue
            PIS = create_element(imposto, 'PIS')
            PISNT = create_element(PIS, 'PISNT')
            create_element(PISNT, 'CST', parts[1])

        elif parts[0] == 'N12':
            if len(parts) < 2:
                print(f"Erro na linha {line_number}: esperados 2 campos, mas encontrados {len(parts)}")
                continue
            COFINS = create_element(imposto, 'COFINS')
            COFINSNT = create_element(COFINS, 'COFINSNT')
            create_element(COFINSNT, 'CST', parts[1])

        elif parts[0] == 'W':
            if len(parts) < 16:
                print(f"Erro na linha {line_number}: esperados 16 campos, mas encontrados {len(parts)}")
                continue
            total = create_element(infNFe, 'total')
            ICMSTot = create_element(total, 'ICMSTot')
            create_element(ICMSTot, 'vBC', parts[1])
            create_element(ICMSTot, 'vICMS', parts[2])
            create_element(ICMSTot, 'vICMSDeson', parts[3])
            create_element(ICMSTot, 'vBCST', parts[4])
            create_element(ICMSTot, 'vST', parts[5])
            create_element(ICMSTot, 'vProd', parts[6])
            create_element(ICMSTot, 'vFrete', parts[7])
            create_element(ICMSTot, 'vSeg', parts[8])
            create_element(ICMSTot, 'vDesc', parts[9])
            create_element(ICMSTot, 'vII', parts[10])
            create_element(ICMSTot, 'vIPI', parts[11])
            create_element(ICMSTot, 'vPIS', parts[12])
            create_element(ICMSTot, 'vCOFINS', parts[13])
            create_element(ICMSTot, 'vOutro', parts[14])
            create_element(ICMSTot, 'vNF', parts[15])

        elif parts[0] == 'X':
            if len(parts) < 5:
                print(f"Erro na linha {line_number}: esperados 5 campos, mas encontrados {len(parts)}")
                continue
            transp = create_element(infNFe, 'transp')
            create_element(transp, 'modFrete', parts[1])
            transporta = create_element(transp, 'transporta')
            create_element(transporta, 'xNome', parts[2])
            vol = create_element(transp, 'vol')
            create_element(vol, 'qVol', parts[3])
            create_element(vol, 'pesoL', parts[4])
            create_element(vol, 'pesoB', parts[5])

        elif parts[0] == 'Y':
            if len(parts) < 4:
                print(f"Erro na linha {line_number}: esperados 4 campos, mas encontrados {len(parts)}")
                continue
            cobr = create_element(infNFe, 'cobr')
            dup = create_element(cobr, 'dup')
            create_element(dup, 'nDup', parts[1])
            create_element(dup, 'dVenc', parts[2])
            create_element(dup, 'vDup', parts[3])

        elif parts[0] == 'Z':
            infAdic = create_element(infNFe, 'infAdic')
            create_element(infAdic, 'infAdFisco')
            create_element(infAdic, 'infCpl')

    protNFe = create_element(nfeProc, 'protNFe', attrib={'versao': '4.00'})
    infProt = create_element(protNFe, 'infProt')
    create_element(infProt, 'tpAmb', '1')
    create_element(infProt, 'verAplic', '6.0')
    create_element(infProt, 'chNFe', '510500042420035722343256826829877')
    create_element(infProt, 'dhRecbto', '2017-02-03T18:23:20-02:00')
    create_element(infProt, 'nProt', '152170667241354')
    create_element(infProt, 'digVal', '2qhZfVTlC2Tqz+RWdhXnbnJT0V4=')
    create_element(infProt, 'cStat', '100')
    create_element(infProt, 'xMotivo', 'Autorizado o uso da NF-e')

    tree = ET.ElementTree(nfeProc)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)


st.title("Conversão de NFe - TXT para XML")
# st.markdown("<p style='font-size:24px'>TXT para XML</p>", unsafe_allow_html=True)
st.write("")
st.write(r"Os arquivos .txt existentes na pasta 'c:\NFe' serão convertidos para .xml:")
st.write("")

if 'pasta' not in st.session_state:
    st.session_state.pasta = ''


# Armazenar em cache o estado da aplicação
@st.cache_data
def cache_state():
    return st.session_state


# if st.button("Selecionar pasta dos arquivos TXT"):
#     pasta = select_folder()
#     if pasta:
#         st.write(f"Pasta selecionada: {pasta}")
#         st.session_state.pasta = pasta  # Armazenar o caminho da pasta selecionada no estado da sessão
#     else:
#         st.write("Nenhuma pasta foi selecionada.")

pasta = os.path.normpath('C:\\NFe\\')  # Caminho da pasta de arquivos TXT
st.session_state.pasta = pasta  # Armazenar o caminho da pasta selecionada no estado da sessão


if st.button("Converter"):
    # Verificar se a pasta existe
    if not os.path.exists(st.session_state.pasta):
        st.write(f"Pasta não encontrada: {st.session_state.pasta}")
    else:
        arquivos_processados = False
        for file in os.listdir(st.session_state.pasta):  # Usar o caminho da pasta selecionada no estado da sessão
            if file.lower().endswith('.txt'):  # Trata tanto '.txt' quanto '.TXT'
                st.write(f"Convertendo {file}...")
                process_txt_to_xml(os.path.join(st.session_state.pasta, file), os.path.join(st.session_state.pasta, file[:-4] + '.xml'))
                arquivos_processados = True
        if arquivos_processados:
            st.write("Arquivo(s) convertido(s) com sucesso!")
        else:
            st.write("Nenhum arquivo .txt encontrado para conversão.")
        # st.write(st.session_state.pasta)

        # Adicionar botão "Reiniciar"
        st.write("")
        if st.button("Reiniciar"):
            cache_state().clear()  # Limpar o estado da aplicação
            st.experimental_rerun()  # Reiniciar a aplicação
