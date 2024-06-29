import streamlit as st
import random
from datetime import datetime

import xml.etree.ElementTree as ET
from io import BytesIO


def num_aleatorio():
    """Generates a random string of 15 characters.

    Returns:
      str: A random string of 15 characters.
  """
    f = ""
    for i in range(1, 16):
        # Use random.uniform to generate a random float between 0 and 1
        x = random.uniform(0, 1) * 3.72158 * i
        # Use string formatting to get the last character of x
        x = str(x)[-1]
        f += x
    return f


def dv_mod11(v_nr):
    """Calculates the DV (verification digit) using the Mod11 algorithm.

  Args:
      v_nr (str): The number to calculate the DV for.

  Returns:
      int: The calculated DV (verification digit).
  """
    v_soma = 0
    v_mult = 2

    for i in range(len(v_nr) - 1, -1, -1):
        # Convert character to integer and handle potential errors
        try:
            digit = int(v_nr[i])
        except ValueError:
            raise ValueError("Invalid character in input string")

        v_soma += digit * v_mult
        v_mult = (v_mult + 1) % 10  # Efficiently wrap v_mult around 2-9

    dv = v_soma % 11
    return 0 if dv in (0, 1) else 11 - dv


def generate_chave_nfe(pedido, data, cliente):
    """Generates a NFe key string with DV (verification digit).

  Args:
      pedido (str): The order number (assumed to be a string).
      data (datetime.date): The order date.
      cliente (str): The customer ID.

  Returns:
      str: The complete NFe key string with DV.
  """
    # Generate random string
    random_string = num_aleatorio()

    # Format date and order number
    formatted_date = data.strftime("%y%d%m")
    formatted_pedido = pedido.zfill(4)

    # Construct the base key string
    base_chave = f"{datetime.now().strftime('%S%M')}{formatted_pedido}{formatted_date}{cliente}{random_string}"

    # Check if the first character is 0 and adjust if needed
    if base_chave[0] == "0":
        base_chave = "3" + base_chave[1:]

    # Calculate and append DV
    dv = dv_mod11(base_chave)
    chave_nfe = base_chave + str(dv)

    return chave_nfe


def create_element(parent, tag, text=None, attrib={}):
    element = ET.SubElement(parent, tag, attrib)
    if text:
        element.text = text
    return element


def process_txt_to_xml(txt_content):
    lines = txt_content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        parts = line.strip().split('|')

        if parts[0] == 'B':
            cUF = parts[1]
            aamm = parts[7][2:4] + parts[7][0:2]
            # cnpj = parts[2]
            modelo = parts[4]
            serie = parts[5]
            nNF = parts[6]
            tpEmis = parts[13]
            cNF = parts[14]
            # cDV= parts[15]     
            data = datetime.now().date()
            chave_nfe = generate_chave_nfe(parts[6], data, '01')
        elif parts[0] == 'C02':
            cnpj = parts[1]
            # chave_nfe = generate_chave_nfe(cNF, datetime.now().date(), cnpj)
            cNF = num_aleatorio()
            cDV = dv_mod11(cNF)
            chave_nfe = 'NFe' + cUF + aamm + cnpj + modelo + serie + nNF + tpEmis + cNF + cDV
            break

    ET.register_namespace('', "http://www.portalfiscal.inf.br/nfe")
    nfeProc = ET.Element('nfeProc', attrib={'xmlns': "http://www.portalfiscal.inf.br/nfe", 'versao': '4.00'})
    NFe = create_element(nfeProc, 'NFe', attrib={'xmlns': "http://www.portalfiscal.inf.br/nfe"})
    infNFe = create_element(NFe, 'infNFe', attrib={'Id': chave_nfe, 'versao': '4.00'})

    det_counter = 1  # Contador para elementos <det>

    for line_number, line in enumerate(lines, start=1):
        parts = line.strip().split('|')

        if parts[0] == 'A':
            # Informações do documento
            pass  # Esses dados não estão explicitamente no exemplo de XML fornecido

        elif parts[0] == 'B':
            ide = create_element(infNFe, 'ide')
            create_element(ide, 'cUF', parts[1])
            create_element(ide, 'cNF', chave_nfe[34:42])
            create_element(ide, 'natOp', parts[3])
            # create_element(ide, 'indPag', '?')
            create_element(ide, 'mod', parts[4])
            create_element(ide, 'serie', parts[5])
            create_element(ide, 'nNF', parts[6])
            create_element(ide, 'dhEmi', parts[7])
            if len(parts[8]) > 0:
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
            create_element(ide, 'procEmi', '3')
            create_element(ide, 'verProc', '4.01_sebrae_b039')

        elif parts[0] == 'C':
            parts1 = parts
            continue

        elif parts[0] == 'C02':
            parts2 = parts
            continue

        elif parts[0] == 'C05':
            parts3 = parts
            emit = create_element(infNFe, 'emit')
            create_element(emit, 'CNPJ', parts2[1])
            create_element(emit, 'xNome', parts1[1])
            create_element(emit, 'xFant', parts1[2])
            enderEmit = create_element(emit, 'enderEmit')
            create_element(enderEmit, 'xLgr', parts3[1])
            if len(parts3[2]) > 0:
                create_element(enderEmit, 'nro', parts3[2])
            else:
                create_element(enderEmit, 'nro', 'S/N')
            if len(parts3[3]) > 0:
                create_element(enderEmit, 'xCpl', parts3[3])
            create_element(enderEmit, 'xBairro', parts3[4])
            create_element(enderEmit, 'cMun', parts3[5])
            create_element(enderEmit, 'xMun', parts3[6])
            create_element(enderEmit, 'UF', parts3[7])
            create_element(enderEmit, 'CEP', parts3[8])
            create_element(enderEmit, 'cPais', parts3[9])
            create_element(enderEmit, 'xPais', parts3[10])
            create_element(enderEmit, 'fone', parts3[11])
            create_element(emit, 'IE', parts1[3])
            create_element(emit, 'CRT', parts1[7])

        elif parts[0] == 'E':
            parts1 = parts
            continue
        elif parts[0] == 'E02':
            parts2 = parts
            continue
        elif parts[0] == 'E05':
            parts3 = parts
            dest = create_element(infNFe, 'dest')
            create_element(dest, 'CNPJ', parts2[1])
            create_element(dest, 'xNome', parts1[1])
            enderDest = create_element(dest, 'enderDest')
            create_element(enderDest, 'xLgr', parts3[1])
            create_element(enderDest, 'nro', parts3[2])
            if len(parts3[3]) > 0:
                create_element(enderDest, 'xCpl', parts3[3])
            create_element(enderDest, 'xBairro', parts3[4])
            create_element(enderDest, 'cMun', parts3[5])
            create_element(enderDest, 'xMun', parts3[6])
            create_element(enderDest, 'UF', parts3[7])
            create_element(enderDest, 'CEP', parts3[8])
            create_element(enderDest, 'cPais', parts3[9])
            create_element(enderDest, 'xPais', parts3[10])
            if len(parts3[11]) > 0:
                create_element(enderDest, 'fone', parts3[11])
            create_element(dest, 'indIEDest', parts1[2])
            create_element(dest, 'IE', parts1[3])

        elif parts[0] == 'H':
            det = create_element(infNFe, 'det', attrib={'nItem': str(det_counter)})
            det_counter += 1

        elif parts[0] == 'I':
            # if len(parts) < 15:
            #     print(f"Erro na linha {line_number}: esperados 15 campos, mas encontrados {len(parts)}")
            #     continue
            prod = create_element(det, 'prod')
            create_element(prod, 'cProd', parts[1])
            if len(parts[2]) > 0:
                create_element(prod, 'cEAN', parts[2])
            else:
                create_element(prod, 'cEAN', 'SEM GTIN')
            create_element(prod, 'xProd', parts[4])
            create_element(prod, 'NCM', parts[5])
            create_element(prod, 'CFOP', parts[7])
            create_element(prod, 'uCom', parts[8])
            create_element(prod, 'qCom', parts[9])
            create_element(prod, 'vUnCom', parts[10])
            create_element(prod, 'vProd', parts[11])
            if len(parts[12]) > 0:
                create_element(prod, 'cEANTrib', parts[12])
            else:
                create_element(prod, 'cEANTrib', 'SEM GTIN')
            create_element(prod, 'uTrib', parts[14])
            create_element(prod, 'qTrib', parts[15])
            create_element(prod, 'vUnTrib', parts[16])
            create_element(prod, 'indTot', parts[21])

        elif parts[0] == 'N10g':
            imposto = create_element(det, 'imposto')
            icms = create_element(imposto, 'ICMS')
            icmssn500 = create_element(icms, 'ICMSSN500')
            create_element(icmssn500, 'orig', parts[1])
            create_element(icmssn500, 'CSOSN', parts[2])
            create_element(icmssn500, 'vBCSTRet', parts[3])
            create_element(icmssn500, 'pST', parts[4])
            create_element(icmssn500, 'vICMSSubstituto', parts[5])
            if len(parts) >= 7:
                create_element(icmssn500, 'vICMSSTRet', parts[6])

        # elif parts[0] == 'N10':
        #     if len(parts) < 7:
        #         print(f"Erro na linha {line_number}: esperados 7 campos, mas encontrados {len(parts)}")
        #         continue
        #     ICMS = create_element(imposto, 'ICMS')
        #     ICMSSN500 = create_element(ICMS, 'ICMSSN500')
        #     create_element(ICMSSN500, 'orig', parts[1])
        #     create_element(ICMSSN500, 'CSOSN', parts[2])
        #     create_element(ICMSSN500, 'vBCSTRet', parts[3])
        #     create_element(ICMSSN500, 'pST', parts[4])
        #     create_element(ICMSSN500, 'vICMSSubstituto', parts[5])
        #     create_element(ICMSSN500, 'vICMSSTRet', parts[6])

        elif parts[0] == 'Q04':
            # if len(parts) < 2:
            #     print(f"Erro na linha {line_number}: esperados 2 campos, mas encontrados {len(parts)}")
            #     continue
            PIS = create_element(imposto, 'PIS')
            PISNT = create_element(PIS, 'PISNT')
            create_element(PISNT, 'CST', parts[1])

        elif parts[0] == 'S04':
            # if len(parts) < 2:
            #     print(f"Erro na linha {line_number}: esperados 2 campos, mas encontrados {len(parts)}")
            #     continue
            COFINS = create_element(imposto, 'COFINS')
            COFINSNT = create_element(COFINS, 'COFINSNT')
            create_element(COFINSNT, 'CST', parts[1])

        elif parts[0] == 'W02':
            # if len(parts) < 16:
            #     print(f"Erro na linha {line_number}: esperados 16 campos, mas encontrados {len(parts)}")
            #     continue
            parts1 = parts
            continue
        elif parts[0] == 'W04c':
            parts2 = parts
            continue
        elif parts[0] == 'W04e':
            parts3 = parts
        elif parts[0] == 'W04g':
            parts4 = parts
            total = create_element(infNFe, 'total')
            ICMSTot = create_element(total, 'ICMSTot')
            create_element(ICMSTot, 'vBC', parts1[1])
            create_element(ICMSTot, 'vICMS', parts1[2])
            create_element(ICMSTot, 'vICMSDeson', parts1[3])
            create_element(ICMSTot, 'vFCPUFDest', parts2[1])
            create_element(ICMSTot, 'vICMSUFDest', parts3[1])
            create_element(ICMSTot, 'vICMSUFRemet', parts4[1])
            create_element(ICMSTot, 'vFCP', parts1[4])
            create_element(ICMSTot, 'vBCST', parts1[5])
            create_element(ICMSTot, 'vST', parts1[6])
            create_element(ICMSTot, 'vFCPST', parts1[7])
            create_element(ICMSTot, 'vFCPSTRet', parts1[8])
            create_element(ICMSTot, 'qBCMono', parts1[9])
            create_element(ICMSTot, 'vICMSMono', parts1[10])
            create_element(ICMSTot, 'qBCMonoReten', parts1[11])
            create_element(ICMSTot, 'vICMSMonoReten', parts1[12])
            create_element(ICMSTot, 'qBCMonoRet', parts1[13])
            create_element(ICMSTot, 'vICMSMonoRet', parts1[14])
            if len(parts1) > 15:
                create_element(ICMSTot, 'vProd', parts1[15])
                create_element(ICMSTot, 'vFrete', parts1[16])
                create_element(ICMSTot, 'vSeg', parts1[17])
                create_element(ICMSTot, 'vDesc', parts1[18])
                create_element(ICMSTot, 'vII', parts1[19])
                create_element(ICMSTot, 'vIPI', parts1[20])
                create_element(ICMSTot, 'vIPIDevol', parts1[21])
                create_element(ICMSTot, 'vPIS', parts1[22])
                create_element(ICMSTot, 'vCOFINS', parts1[23])
                create_element(ICMSTot, 'vOutro', parts1[24])
                create_element(ICMSTot, 'vNF', parts1[25])
                create_element(ICMSTot, 'vTotTrib', parts1[26])

        elif parts[0] == 'X':
            # if len(parts) < 5:
            #     print(f"Erro na linha {line_number}: esperados 5 campos, mas encontrados {len(parts)}")
            #     continue
            transp = create_element(infNFe, 'transp')
            create_element(transp, 'modFrete', parts[1])
            # transporta = create_element(transp, 'transporta')
            # create_element(transporta, 'xNome', parts[2])
            # vol = create_element(transp, 'vol')
            # create_element(vol, 'qVol', parts[3])
            # create_element(vol, 'pesoL', parts[4])
            # create_element(vol, 'pesoB', parts[5])

        elif parts[0] == 'Y02':
            # if len(parts) < 4:
            #     print(f"Erro na linha {line_number}: esperados 4 campos, mas encontrados {len(parts)}")
            #     continue
            parts1 = parts
            continue
        elif parts[0] == 'Y07':
            parts2 = parts
            continue
        elif parts[0] == 'YA':
            parts3 = parts

            cobr = create_element(infNFe, 'cobr')
            fat = create_element(cobr, 'fat')
            create_element(fat, 'nFat', parts1[1])
            create_element(fat, 'vOrig', parts1[2])
            create_element(fat, 'vDesc', parts1[3])
            create_element(fat, 'vLiq', parts1[4])
            dup = create_element(cobr, 'dup')
            create_element(dup, 'nDup', parts2[1])
            create_element(dup, 'dVenc', parts2[2])
            create_element(dup, 'vDup', parts2[3])

        elif parts[0] == 'YA01':
            pag = create_element(infNFe, 'pag')
            detPag = create_element(pag, 'detPag')
            create_element(detPag, 'indPag', parts[1])
            create_element(detPag, 'tPag', parts[2])
            create_element(detPag, 'vPag', parts[4])

        elif parts[0] == 'Z':
            infAdic = create_element(infNFe, 'infAdic')
            create_element(infAdic, 'infCpl', parts[2])

    infRespTec = create_element(infNFe, 'infRespTec')
    create_element(infRespTec, 'CNPJ', '43728245000142')
    create_element(infRespTec, 'xContato', 'suporte')
    create_element(infRespTec, 'email', 'suporteemissores@sebraesp.com.br')
    create_element(infRespTec, 'fone', '08005700800')

    # protNFe = create_element(nfeProc, 'protNFe', attrib={'versao': '4.00'})
    # infProt = create_element(protNFe, 'infProt')
    # create_element(infProt, 'tpAmb', '1')
    # create_element(infProt, 'verAplic', '6.0')
    # create_element(infProt, 'chNFe', '510500042420035722343256826829877')
    # create_element(infProt, 'dhRecbto', '2017-02-03T18:23:20-02:00')
    # create_element(infProt, 'nProt', '152170667241354')
    # create_element(infProt, 'digVal', '2qhZfVTlC2Tqz+RWdhXnbnJT0V4=')
    # create_element(infProt, 'cStat', '100')
    # create_element(infProt, 'xMotivo', 'Autorizado o uso da NF-e')

    xml_buffer = BytesIO()
    tree = ET.ElementTree(nfeProc)
    # tree.write(xml_path, encoding='utf-8', xml_declaration=True)

    tree.write(xml_buffer, encoding='utf-8', xml_declaration=True)
    st.balloons()
    return xml_buffer.getvalue().decode('utf-8')

