import xml.etree.ElementTree as ET
from io import BytesIO


def create_element(parent, tag, text=None, attrib={}):
    element = ET.SubElement(parent, tag, attrib)
    if text:
        element.text = text
    return element


def process_txt_to_xml(txt_content):
    lines = txt_content.splitlines()

    ET.register_namespace('', "http://www.portalfiscal.inf.br/nfe")
    nfeProc = ET.Element('nfeProc', attrib={'xmlns': "http://www.portalfiscal.inf.br/nfe", 'versao': '4.00'})
    NFe = create_element(nfeProc, 'NFe', attrib={'xmlns': "http://www.portalfiscal.inf.br/nfe"})
    infNFe = create_element(NFe, 'infNFe', attrib={'versao': '4.00'})

    det_counter = 1  # Contador para elementos <det>

    for line_number, line in enumerate(lines, start=1):
        parts = line.strip().split('|')

        if parts[0] == 'A':
            # Informações do documento
            pass  # Esses dados não estão explicitamente no exemplo de XML fornecido

        elif parts[0] == 'B':
            ide = create_element(infNFe, 'ide')
            create_element(ide, 'cUF', parts[1])
            create_element(ide, 'cNF', '?')
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
            create_element(ide, 'cDV', '')
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
            create_element(dest, 'indIEDest', '?')
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

    xml_buffer = BytesIO()
    tree = ET.ElementTree(nfeProc)
    # tree.write(xml_path, encoding='utf-8', xml_declaration=True)

    tree.write(xml_buffer, encoding='utf-8', xml_declaration=True)
    return xml_buffer.getvalue().decode('utf-8')
