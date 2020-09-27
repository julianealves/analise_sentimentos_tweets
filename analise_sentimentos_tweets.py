#       UNIVERSIDADE FEDERAL DO RIO GRANDE SO SUL
#       INSTITUTO DE INFORMATICA
#       CLASSIFICACAO E PESQUISA DE DADOS
#       TRABALHO FINAL (analise de sentimentos de tweets)
#
# @author: Juliane da Rocha Alves e Victor de Souza Arnt

import csv
from unicodedata import normalize
from tempfile import NamedTemporaryFile
import shutil
import os

class Palavra():
    """
    Classe representa uma palavra do dicionario e possui como atributo
    o numero de Tweets em que essa palavra aparece,
    o score de sentimento e o score acumulativo

    EN: The class represents a word from the dictionary and has as attribute
    the number of Tweets in which that word appears,
    the feeling score and the cumulative score
    """
    def __init__(self):
        self.palavra = ''
        self.scoreSentimento = 0
        self.scoreAcumulativo = 0
        self.nroTweets = 0

    def setPalavra(self, palavra):
        self.palavra = palavra

    def setScoreSentimento(self, polaridade):
        self.scoreSentimento = polaridade/self.nroTweets

    def attScoreAcumulativo(self):
        #Atualiza o score acumulativo
        #Update the cumulative score
        self.scoreAcumulativo = self.scoreSentimento*self.nroTweets

    def incNroTweets(self):
        #incrementa a quantidade de tweets em que a palavra foi utilizada
        #Increase the quantity of tweet the word appears
        self.nroTweets = self.nroTweets + 1
    def setNroTweets(self,NT):
        self.nroTweets=NT

    def getScoreSentimento(self):
        return self.scoreSentimento

    def getScoreAcumulativo(self):
        return self.scoreAcumulativo

    def getNroTweets(self):
        return self.nroTweets

    def getPalavra(self):
        return self.palavra

class Dicionario():
    """
    Classe possui um dicionario que contem palavras de tweets

    EN: The class has a dictionary which contains words from tweets
    """
    def __init__(self):
        #Hash com encadeamento fechado
        #Tabela de tamanho 2087
        #Hash with closed thread (size = 2087)
        self.M = 2087
        self.dicionario = [None for i in range(self.M)]
        #Lista de stop words
        #List of stop words
        self.stopWords = []
        #numero de chaves
        #Number of keys
        self.N=0
        #lista para auxiliar a criacao do arquivo invertido
        #Aux list to create am inverted file
        self.listaInvertida = []

    def getM(self):
        return self.M

    def setNewM(self):
        self.M=self.M*2

    def nullN(self):
        self.N=0

    def funcaoHash(self, palavra):
        """
        Funcao de Hash Modular (EN: Hash modular function)
        https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/st-hash.html
        """
        h = 0
        for i in range(len(palavra)):
            h = (31 * h + ord(palavra[i])) % self.getM()
        return h

    def rehash(self):
        #copia dicionario para tabela auxiliar
        listaAux=self.dicionario
        #aumenta dicionario
        self.setNewM()
        #zera dicionario
        self.dicionario=[None for i in range(self.M)]
        self.nullN()
        #extrai dicionario antigo
        for j in range(len(listaAux)):
            chave = listaAux[j]
            if chave != None:
                for i in range(len(chave)):
                    obj = chave[i]
                    palavra = obj.getPalavra()
                    nrotweets=obj.getNroTweets()
                    polaridade=obj.getNroTweets()*obj.getScoreSentimento()
                    dicionario.RehashinserePalavra(palavra,polaridade,nrotweets)

    def RehashinserePalavra(self, palavra, polaridade,nrotweets):
        """
        Insere a palavra no dicionario atualizando a quantidade de Tweets em que
        a palavra aparece, assim como o score de sentimento e o score acumulativo.
        Trata das colisoes no dicionario inserindo uma lista encadeada no endereco
        em que ocorreu a colisao.
        """
        #Calcula o endereco da palavra a ser inserida
        hashing = self.funcaoHash(palavra)
        #Recupera o valor que contiver no endereco calculado
        chave = self.dicionario[hashing]
        #Verifica se na posicao calculada nao tem nada
        if chave == None:
            #Insere a palavra no dicionario
            objPalavra = Palavra()
            objPalavra.setPalavra(palavra)
            objPalavra.setNroTweets(nrotweets)
            objPalavra.setScoreSentimento(polaridade)
            objPalavra.attScoreAcumulativo()
            #Insere uma lista com a palavra para poder fazer tratamento de
            #colisoes utilizando uma lista encadeada
            self.dicionario[hashing] = [objPalavra]
            self.N = self.N+1

        #Tratamento da colisao
        else:
            #Insere a palavra no dicionario
            objPalavra = Palavra()
            objPalavra.setPalavra(palavra)
            objPalavra.setNroTweets(nrotweets)
            objPalavra.setScoreSentimento(polaridade)
            objPalavra.attScoreAcumulativo()
            #Insere na lista a nova palavra para atualizar o Dicionario
            chave.append(objPalavra)
            self.N = self.N+1
            #Salva a lista atualizada no dicionario
            self.dicionario[hashing] = chave

    def inserePalavra(self, palavra, polaridade):
        """
        Insere a palavra no dicionario atualizando a quantidade de Tweets em que
        a palavra aparece, assim como o score de sentimento e o score acumulativo.
        Trata das colisoes no dicionario inserindo uma lista encadeada no endereco
        em que ocorreu a colisao.
        """
        #Calcula o endereco da palavra a ser inserida
        hashing = self.funcaoHash(palavra)
        #Recupera o valor que contiver no endereco calculado
        chave = self.dicionario[hashing]
        #Verifica se na posicao calculada nao tem nada
        if chave == None:
            #Insere a palavra no dicionario
            objPalavra = Palavra()
            objPalavra.setPalavra(palavra)
            objPalavra.incNroTweets()
            objPalavra.setScoreSentimento(polaridade)
            objPalavra.attScoreAcumulativo()
            #Insere uma lista com a palavra para poder fazer tratamento de
            #colisoes utilizando uma lista encadeada
            self.dicionario[hashing] = [objPalavra]
            self.N = self.N+1
        #Tratamento da colisao
        else:
            inserida = False
            #Percorre as palavras inseridas na lista na posicao calculada
            for i in range(len(chave)):
                obj = chave[i]
                palavraInserida = obj.getPalavra()
                #verifica se a palavra ja havia sido inserida anteriormente
                if palavraInserida == palavra:
                    #Atualiza o score de scoreSentimento
                    #Atualiza o score scoreAcumulativo
                    #Incrementa o numero de tweets
                    obj.incNroTweets()
                    obj.setScoreSentimento(polaridade)
                    obj.attScoreAcumulativo()
                    #Atualiza a lista
                    chave[i] = obj
                    inserida = True
                    break
            #Se a palavra ainda nao havia sido inserida
            if inserida == False:
                #Insere a palavra no dicionario
                objPalavra = Palavra()
                objPalavra.setPalavra(palavra)
                objPalavra.incNroTweets()
                objPalavra.setScoreSentimento(polaridade)
                objPalavra.attScoreAcumulativo()
                #Insere na lista a nova palavra para atualizar o Dicionario
                chave.append(objPalavra)
                #Salva a lista atualizada no dicionario
                self.N = self.N+1
                #print(self.N,'/',self.M)
                self.dicionario[hashing] = chave

    def chrRemove(self, old, to_remove):
        """
        Remove os caracteres passados como parametro
        """
        new_string = old
        for x in to_remove:
            new_string = new_string.replace(x, '')
        return new_string

    def removerAcentos(self, txt):
        """
        Remove o acento da palavra passada como parametro
        """
        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

    def tratarTweet(self, row, predict, linha, path):
        score = 0
        if predict == False:
            tweet, polaridade = row
        else:
            tweet = row[0]
        #Remove os caracteres especiais do Tweet
        tweet = self.chrRemove(tweet, "$(#!@?;:.,/_|+=-)&*%{[]}~^<>1234567890\'\"\\")
        #Remove o acento das palavras
        tweet = self.removerAcentos(tweet)
        #Splita o tweet por um espaco em branco para pegar todas as palavras do tweet
        tweet = tweet.split(' ')

        tweets = []
        #coloca todas as palavras em letra maiuscula
        for palavra in tweet:
            tweets.append(palavra.upper())
        #Pega somente as palavras que sao diferentes
        tweet = list(set(tweets))
        #Percorre todas as palavras do tweet
        for palavra in tweet:
            isStop = False
            #Verifica se a palavra eh uma stop word
            for stopword in self.stopWords:
                if palavra == stopword:
                    isStop = True
            if self.N<self.M/2:
                if isStop == False:
                #Verifica se a palavra tem mais do que dois caracteres
                    if len(palavra) > 2:
                    #Insere a palavra no dicionario e salva o tweet
                        if predict == False:
                            self.inserePalavra(palavra, int(polaridade))
                            self.salvarTweet(palavra, linha, path)

                        else:
                            score = score + self.getScorePalavra(palavra)
            else:
            #Aumenta tabela
                self.rehash()

        #Se predicao esta habilitada, faz a predicao do tweet
        if predict == True:
            self.salvarPredict(row, score)

    def salvarTweet(self, palavra, linha, path):
        if (len(self.listaInvertida) == 0):
            #coloca a linha e o nome do arquivo na lista
            self.listaInvertida.append(palavra + "," + path + ":" + str(linha))
        else:
            isFound = False
            #procura se a palavra jah esta na lisa
            for i in range(len(self.listaInvertida)):
                row = self.listaInvertida[i].split(",")
                #verifica se a palavra jah estava salva na lista
                if (row[0] == palavra):
                    isFound = True
                    conteudo = ''
                    for j in range(1, len(row)):
                        #split em path e linha onde esta a palavra
                        linhas = row[j].split(":")
                        for k in range(0, len(linhas), 2):
                            if (linhas[k] == path and int(linhas[k+1]) == int(linha)):
                                #palavra duplicada na mesma linha
                                pass
                            elif (len(linhas) > 1):
                                #concatena a informacao ja existente com a nova informacao
                                conteudo = conteudo + linhas[k] + ":" + linhas[k+1] + ","
                    #atualiza a lista
                    self.listaInvertida[i] = palavra + "," + conteudo + path + ":" + str(linha)
            #se a palavra ainda nao foi adicionada na lista, adiciona
            if (isFound == False):
                #se a palavra nao estava na lista invertida, adiciona
                self.listaInvertida.append(palavra + "," + path + ":" + str(linha))

    def getScorePalavra(self, palavra):
        #Calcula o endereco da palavra a ser pesquisada
        hashing = self.funcaoHash(palavra)
        #Recupera o valor que contiver no endereco calculado
        chave = self.dicionario[hashing]
        #Se nao houvar nada no enderco, retorna o score como sendo 0
        if chave == None:
            return 0
        else:
            #Percorre as palavras inseridas na lista na posicao calculada
            for i in range(len(chave)):
                obj = chave[i]
                palavraProcurada = obj.getPalavra()
                #verifica se a palavra se encontra na lista
                if palavraProcurada == palavra:
                    #retorna o score da palavra
                    return obj.getScoreSentimento()
        #Se nao encontra a palavra, retorna 0
        return 0

    def salvarPredict(self, row, score):
        '''
            Salva em arquivo csv o resultado das predicoes
        '''
        #calculo do score
        if (score < -0.1):
            scoreTweet = -1
        elif (score > 0.1):
            scoreTweet = 1
        else:
            scoreTweet = 0

        with open('tweetsPolarizados.csv', 'a', encoding="utf8", newline='') as csvfile:
            wr = csv.writer(csvfile, delimiter=',')
            wr.writerow([row[0], scoreTweet])


    def ReadTweetFile(self, path = "pt", predict = False):
        '''
            Le o arquivo que contem os tweets

            Keyword arguments:
            path -- nome do arquivo
            predict -- Flag para avisar se eh para fazer a predicao de Tweets
            ou adicinar novas palavras
        '''
        linha = 0
        with open(path + '.csv','r', encoding="utf8") as text:
            fileReader = csv.reader(text, delimiter=',')
            for row in fileReader:
                if len(row) > 0:
                    linha = linha + 1
                    self.tratarTweet(row, predict, linha, path + ".csv")

    def readStopWords(self, path="stopwords"):
        '''
            Le o arquivo que contem stop words em portugues

            Keyword arguments:
            path -- nome do arquivo
        '''
        with open(path + '.csv','r') as text:
            fileReader = csv.reader(text)
            for row in fileReader:
                if len(row) > 0:
                    #Remove o acento das stop words
                    stopWord = self.removerAcentos(row[0])
                    #Transforma todas as stopwords em letra maiuscula
                    self.stopWords.append(stopWord.upper())

    def criarArquivoInvertido(self):
        with open('arquivoInvertido.csv', 'w', encoding="utf8") as csvfile:
            wr = csv.writer(csvfile, delimiter='\n')
            wr.writerow([i for i in self.listaInvertida])

    def procurarPalavra(self, palavra):
        #Remove os caracteres especiais da palavra
        palavra = self.chrRemove(palavra, "$(#!@?;:.,/_|+=-)&*%{[]}~^<>1234567890\'\"\\")
        #Remove o acento da palavra
        palavra = self.removerAcentos(palavra)
        #coloca a palavra com letra maiuscula
        palavra = palavra.upper()
        #lista de arquivos onde esta a palavra
        tweets = []
        polaridades = []
        linhas = []
        oldPath = ''
        mesmoArquivo = True
        palavraAchada=0
        with open('arquivoInvertido.csv', 'r', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if (len(row) > 0):
                    #procura palavra no arquivo invertido
                    if(row[0] == palavra):
                        palavraAchada=palavraAchada+1
                        for i in range(1, len(row)):
                            #da um split em path e linha de onde esta a palavra
                            path, linha = row[i].split(":")
                            if (i == 1):
                                oldPath = path
                            #verifica se a palavra esta em mais de um arquivo
                            if(path == oldPath):
                                mesmoArquivo = True
                                linhas.append(int(linha))
                            else:
                                #pega os tweets que contem a palavra
                                self.pegarTweets(oldPath, linhas, tweets, polaridades)
                                linhas = []
                                linhas.append(int(linha))
                                oldPath = path

        #verifica se a palavra existe no arquivo
        if(palavraAchada>0):
        #pega os tweets que contem a palavra
            self.pegarTweets(oldPath, linhas, tweets, polaridades)
        else:
            print('Desculpe, a palavra '+palavra+' não está em nosso banco de dados de tweets!')

        #imprime os tweets que contem a palavra
        self.printTweets(tweets, polaridades)

    def pegarTweets(self, path, linhas, tweets, polaridades):
        i = 0
        with open(path,'r', encoding="utf8") as text:
            fileReader = csv.reader(text)
            for row in fileReader:
                if len(row) > 0:
                    i = i + 1
                    for j in linhas:
                        if (j == i):
                            #Verifica se a linha atual que esta sendo lida dos arquivos
                            #eh a linha onde se encontra a palavra. Se for,
                            #adiciona o tweet e a polaridade nas listas
                            tweets.append(row[0])
                            polaridades.append(row[1])

    def printTweets(self, tweets, polaridades):
        #printa os valores contidos nas listas tweets e polaridades
        for i in range(len(tweets)):
            print("TWEET: ", tweets[i], " POLARIDADE: ", polaridades[i])

    def getPalavraDicionario(self, palavra):
        #Remove os caracteres especiais da palavra
        palavra = self.chrRemove(palavra, "$(#!@?;:.,/_|+=-)&*%{[]}~^<>1234567890\'\"\\")
        #Remove o acento da palavra
        palavra = self.removerAcentos(palavra)
        #coloca a palavra com letra maiuscula
        palavra = palavra.upper()
        #Calcula o endereco da palavra a ser pesquisada
        hashing = self.funcaoHash(palavra)
        #Recupera o valor que contiver no endereco calculado
        chave = self.dicionario[hashing]
        #Se nao houvar nada no enderco, retorna o score como sendo 0
        if chave == None:
            return 0
        else:
            #Percorre as palavras inseridas na lista na posicao calculada
            for i in range(len(chave)):
                obj = chave[i]
                palavraProcurada = obj.getPalavra()
                #verifica se a palavra se encontra na lista
                if palavraProcurada == palavra:
                    print("\n")
                    print("********************************************")
                    print("PALAVRA: ", obj.getPalavra())
                    print("NUMERO DE TWEETS EM QUE APARECE: ", obj.getNroTweets())
                    print("SCORE DE SENTIMENTO: ", obj.getScoreSentimento())
                    print("SCORE ACUMULADO: ", obj.getScoreAcumulativo())

if __name__ == '__main__':
    dicionario = Dicionario()
    #Le o arquivo de stop words
    dicionario.readStopWords()
    #Popula o dicionario
    dicionario.ReadTweetFile()
    #Popula o dicionario com outro arquivo
    #dicionario.ReadTweetFile(path = "teste2")
    #Salva o arquivo invertido
    dicionario.criarArquivoInvertido()
    #Popula o dicionario com outro arquivo
    #dicionario.ReadTweetFile(path = "teste1")
    #Salva o arquivo invertido
    #dicionario.criarArquivoInvertido()
    #Faz a predicao de tweets
    dicionario.ReadTweetFile(path="tweetsparaPrevisaoUFT8", predict = True)
    #Procura os tweets com determinada palavra
    dicionario.procurarPalavra("bing")
    #Coloca na tela as informacoes contidas no dicionario sobre a palavra passada por parametro
    dicionario.getPalavraDicionario("bing")
