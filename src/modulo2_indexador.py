import os
import datetime
import logging
import auxiliar
import csv
import math
nome_arquivo_entrada = ''
nome_arquivo_saida = ''
lista_invertida = {}
matriz_termo_documento = {}


# ---------------------------------------------------------------------------------------------

def ler_configuracao():
    global nome_arquivo_entrada
    global nome_arquivo_saida

    try:
        logging.info('Iniciando leitura do arquivo de configuração index.cfg')
   
        nome_arquivo_configuracao = os.getcwd() + '\index.cfg'
    
        with open(nome_arquivo_configuracao, encoding="utf-8") as arquivo_configuracao:
            for linha in arquivo_configuracao:
                posicao_igual = linha.find('=')
                if posicao_igual > 0:
                    comando = linha[0:posicao_igual]
                    nome_arquivo = linha[posicao_igual+1 : len(linha)-1]
                    if comando == auxiliar.LEIA:
                        nome_arquivo_entrada = nome_arquivo
                    elif comando == auxiliar.ESCREVA:
                        nome_arquivo_saida = nome_arquivo    
   
        logging.info('Fim da leitura do arquivo de configuração index.cfg finalizada')
    except:
        logging.info('Erro ao ler o arquivo de configuração')

# ---------------------------------------------------------------------------------------------

def ler_arquivo_lista_intertida():
    try:
        logging.info('Lendo arquivo da lista invertida')
        with open(nome_arquivo_entrada, 'r') as arquivo_csv:
            reader = csv.reader(arquivo_csv, delimiter=';')
            for row in reader:
                token = row[0]
                codigos_documentos = row[1].lstrip('[').rstrip(']').replace("'", "").split(',')
                lista_invertida[token] = codigos_documentos
        logging.info('Fim da leitura do arquivo da lista invertida')            
    except:        
        logging.info('Erro ao ler o arquivo de lista invertida')

# ---------------------------------------------------------------------------------------------

def obter_frequencia_palavra (palavra,codigo_documento):
    frequencia = 0
    for codigo in lista_invertida[palavra]:
        if codigo == codigo_documento:
            frequencia=frequencia+1
    return frequencia

# ---------------------------------------------------------------------------------------------
def gerar_modelo_vetorial():
    try:
        logging.info('Gerando modelo vetorial')
        lista_palavras = lista_invertida.keys()
        lista_documentos = []
    
        # Gera uma lista de documentos não repetidos
        for documentos in lista_invertida.values():
            
            #documentos.sort()
            #print ('ordenado')
            #lista_documentos += [documentos[i] for i in range(len(documentos)-1) if documentos[i] != documentos[i+1]]
            #lista_documentos.append(documentos[-1])
            #print(lista_documentos)
            
            for documento in documentos:
                if not documento in lista_documentos:
                    lista_documentos.append(documento)
    
        # Calcula a frequência inversa das palavras (termos)
        quantidade_documentos = len(lista_documentos)
        
        frequencia_documentos = {}
        
        for palavra, documentos_com_a_palavra in lista_invertida.items():
            # O uso do set tem como finalidade elimiar documentos repetidos
            # quantidade_documentos_palavra = len(set(documentos_com_a_palavra)) .
            quantidade_documentos_palavra = len(documentos_com_a_palavra) # É para contar mesmo as repetidas...
            frequencia_documentos[palavra] = math.log(quantidade_documentos/quantidade_documentos_palavra)

        #for i in range(len(lista_documentos)):
        #    codigo_documento = lista_documentos[i]
        for codigo_documento in lista_documentos:

            pesos_palavra = []

            for palavra in lista_palavras:
                
                idf = frequencia_documentos[palavra]
                tf = obter_frequencia_palavra(palavra, codigo_documento)

                tf_idf = round(tf * idf, auxiliar.CASAS_DECIMAIS)

                pesos_palavra.append(tf_idf)

            matriz_termo_documento[codigo_documento] = pesos_palavra
    
        logging.info('Fim da geração do modelo vetorial')
        
    except:
        logging.info('Erro ao gerar o modelo vetorial')

# ---------------------------------------------------------------------------------------------
def executar():
    print ("Inicio do modulo 2")

    hora_inicio = datetime.datetime.now()
    auxiliar.configurar_log('modulo2_indexador.log')
    
    logging.info("Geração da lista invertida iniciada em "+hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
    
    ler_configuracao()
    ler_arquivo_lista_intertida()
    gerar_modelo_vetorial()
    auxiliar.gerar_arquico_cvs(nome_arquivo_saida, matriz_termo_documento)

    hora_fim = datetime.datetime.now()
    
    tempo = hora_fim - hora_inicio

    logging.info("Finalização da lista invertida em "+hora_fim.strftime("%Y-%m-%d %H:%M:%S"))
    logging.info("Tempo de processamento: "+ str(tempo.seconds) + " segundos ("+str(tempo.microseconds)+" microsegundos)")
    
    print ("Fim do modulo 2")
                
            
# ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    executar()
