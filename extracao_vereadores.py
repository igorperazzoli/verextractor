import json

from funcoes_auxiliares import *

if __name__ == "__main__":
    lista_vereadores = dict()

    lista_vereadores["Brusque"]  = busca_padrao("https://www.camarabrusque.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Camboriú"] = busca_padrao("https://www.camaracamboriu.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Caçador"] = busca_padrao("https://www.camaracacador.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Criciúma"] = busca_alternativa("https://www.camaracriciuma.sc.gov.br/vereadores/mandato:vereadores-da-legislatura-atual-2021-2024-154", "https://www.camaracriciuma.sc.gov.br")
    lista_vereadores["Florianópolis"] = busca_padrao("https://www.cmf.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Gaspar"] = busca_alternativa("https://www.camaragaspar.sc.gov.br/vereadores/mandato:2021-ate-2024-21", "https://www.camaragaspar.sc.gov.br/")
    lista_vereadores["Joaçaba"] = busca_padrao("https://www.cmj.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Lages"] = busca_padrao("https://www.camaralages.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Navegantes"] = busca_padrao("https://www.cvnavegantes.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Palhoça"] = busca_padrao("https://www.cmp.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["São José"] = busca_padrao("https://www.cmsj.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Tangará"] = busca_padrao("https://www.camaratangara.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Timbó"] = busca_padrao("https://www.camaratimbo.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")
    lista_vereadores["Videira"] = busca_padrao("https://www.camaravideira.sc.gov.br/camara/membros/exercicio/0", "dados-vereador-legislatura")

    lista_partidos = dict()
    media_idade = 0
    lista_estado_civil = dict()
    lista_escolaridade = dict()
    qt_email = 0
    qt_telefone = 0
    qt_email_e_telefone = 0
    qt_vereadores = 0
    qt_vereadores_idade = 0
    for cidade in lista_vereadores:
        for vereador in lista_vereadores[cidade]:
            v = lista_vereadores[cidade][vereador]
            qt_vereadores += 1
            
            if v["partido"] in lista_partidos:
                lista_partidos[v["partido"]] += 1
            else:
                lista_partidos[v["partido"]] = 1
            
            if v["data_nascimento"] != "Não informado":
                media_idade += calculate_age(v["data_nascimento"].split("/"))
                qt_vereadores_idade += 1

            if v["estado_civil"] in lista_estado_civil:
                lista_estado_civil[v["estado_civil"]] += 1
            else:
                lista_estado_civil[v["estado_civil"]] = 1
            
            if v["escolaridade"] in lista_escolaridade:
                lista_escolaridade[v["escolaridade"]] += 1
            else:
                lista_escolaridade[v["escolaridade"]] = 1
            
            if v["email"] == "Não informado":
                qt_email += 1

            if v["telefone"] == "Não informado":
                qt_telefone += 1

            if v["email"] == "Não informado" and v["telefone"] == "Não informado":
                qt_email_e_telefone += 1
    
    media_idade = media_idade / qt_vereadores_idade

    print("\nQuantidade de vereadores:\n"+str(qt_vereadores))
    print("\nQuantidade de vereadores por partido:\n"+str(lista_partidos))
    print("\nMédia da idade dos vereadores:\n"+str(media_idade))
    print("\nQuantidade de vereadores por estado civil:\n"+str(lista_estado_civil))
    print("\nQuantidade de vereadores por escolaridade:\n"+str(lista_escolaridade))
    print("\nQuantidade de vereadores que não informaram email:\n"+str(qt_email))
    print("\nQuantidade de vereadores que não informaram telefone:\n"+str(qt_telefone))
    print("\nQuantidade de vereadores que não informaram nem telefone e nem email:\n"+str(qt_email_e_telefone))

    # with open("dados_vereadores.json", "w", encoding="utf-8") as outfile: 
    #     json.dump(lista_vereadores, outfile, ensure_ascii=False) 

    #print(lista_vereadores)

