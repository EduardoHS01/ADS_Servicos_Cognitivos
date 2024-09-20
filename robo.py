from operator import index, indexOf
from time import sleep
import pandas as pd
import numpy as np
class Robo:
    def __init__(self, mapa):
        self.mapa = mapa

        self.entrada = []
        self.dadosSensorFrontal = []
        self.dadosSensorDireito = []
        self.dadosSensorEsquerdo = []
        self.comHumano=False
        self.caminho = []

        self.orientacao=""
        self.simbolo = ""

        dataframe = pd.read_csv(self.mapa, header=None)

        matriz = dataframe.to_numpy()

        matriz = np.array([linha[0] for linha in matriz])

        for i, linha in enumerate(matriz):
            for j, coluna in enumerate(matriz):
                if matriz[i][j] == "E":
        #            print('A linha é:',i,'e a coluna é:',j)
                    self.entrada = [i,j]

        self.posicao = self.entrada
        if self.entrada[0] == 0:
            self.orientacao = 'S'

        elif self.entrada[0] == len(matriz[0])-1:
            self.orientacao = "N"

        if self.entrada[1] == 0:
            self.orientacao = 'O'

        elif self.entrada[1] == len(matriz[0])-1:
            self.orientacao = "L"
        def render(matriz,posicao,simbolo):
            with open("Mapa.txt", "w") as file:
                for i, linha in enumerate(matriz):
                    linha = list(linha)  # Converte a linha em uma lista, caso seja uma string
                    for j, coluna in enumerate(linha):
                        if i == posicao[0] and j == posicao[1]:
                            linha[j] = simbolo  # Atualiza a célula com "X" na posição correta
                            
                    file.write(''.join(linha))  # Converte a lista de volta para string
                    file.write('\n')  # Adiciona a nova linha após escrever a linha atual
            verificarOrientacao()
        def verificar_sensor_frontal(posicao,orientacao):
            dadoSensorFrontal=""
            if(orientacao == "S"):
                dadoSensorFrontal = matriz[posicao[0]+1][posicao[1]]
            elif(orientacao == "O"):
                dadoSensorFrontal = matriz[posicao[0]][posicao[1]-1]
            elif(orientacao == "N"):
                dadoSensorFrontal = matriz[posicao[0]-1][posicao[1]]
            elif(orientacao == "L"):
                dadoSensorFrontal = matriz[posicao[0]][posicao[1]+1]
            if(dadoSensorFrontal =="*"):
                self.dadosSensorFrontal.append("PAREDE")
            elif(dadoSensorFrontal == "H"):
                self.dadosSensorFrontal.append("HUMANO")
            elif(dadoSensorFrontal == "E"):
                self.dadosSensorFrontal.append("ENTRADA")
            elif(dadoSensorFrontal == " "):
                self.dadosSensorFrontal.append("VAZIO")
            return dadoSensorFrontal
        def verificar_sensor_direito(posicao,orientacao):
            dadoSensorDireito=""
            if(orientacao == "S"):
                dadoSensorDireito = matriz[posicao[0]][posicao[1]-1]
            elif(orientacao == "O"):
                dadoSensorDireito = matriz[posicao[0]-1][posicao[1]]
            elif(orientacao == "N"):
                dadoSensorDireito = matriz[posicao[0]][posicao[1]+1]
            elif(orientacao == "L"):
                dadoSensorDireito = matriz[posicao[0]+1][posicao[1]]
            if(dadoSensorDireito =="*"):
                self.dadosSensorDireito.append("PAREDE")
            elif(dadoSensorDireito == "H"):
                self.dadosSensorDireito.append("HUMANO")
            elif(dadoSensorDireito == "E"):
                self.dadosSensorDireito.append("ENTRADA")
            elif(dadoSensorDireito == " "):
                self.dadosSensorDireito.append("VAZIO")
            return dadoSensorDireito
        def verificar_sensor_esquerdo(posicao,orientacao):
            dadoSensorEsquerdo=""
            if(orientacao == "S"):
                dadoSensorEsquerdo = matriz[posicao[0]][posicao[1]+1]
            elif(orientacao == "O"):
                dadoSensorEsquerdo = matriz[posicao[0]+1][posicao[1]]
            elif(orientacao == "N"):
                dadoSensorEsquerdo = matriz[posicao[0]][posicao[1]-1]
            elif(orientacao == "L"):
                dadoSensorEsquerdo = matriz[posicao[0]-1][posicao[1]]
            if(dadoSensorEsquerdo =="*"):
                self.dadosSensorEsquerdo.append("PAREDE")
            elif(dadoSensorEsquerdo == "H"):
                self.dadosSensorEsquerdo.append("HUMANO")
            elif(dadoSensorEsquerdo == "E"):
                self.dadosSensorEsquerdo.append("ENTRADA")
            elif(dadoSensorEsquerdo == " "):
                self.dadosSensorEsquerdo.append("VAZIO")
            return dadoSensorEsquerdo
        def girarDireita():
            direcoes =['S','O','N','L']
            direcao_atual = self.orientacao
            for i, direcao in enumerate(direcoes):
                if direcao_atual == direcao:
                    self.caminho.append(i)
                    # Calcula o próximo índice de forma circular
                    j = (i + 1) % len(direcoes)  # Gira à direita, voltando ao início se necessário
                    self.orientacao = direcoes[j]  # Atualiza a orientação
            render(matriz,self.posicao,self.simbolo)
        def verificarOrientacao():
            if self.orientacao ==   "S":
                self.simbolo = "V"
            elif self.orientacao == "N":
                self.simbolo ="^"
            elif self.orientacao == "O":
                self.simbolo ="<"
            elif self.orientacao == "L":
                self.simbolo =">"
        def andarFrente(self, posicao, orientacao):
            self.orientacao = orientacao
            self.posicao = posicao
            self.caminho.append(posicao)
            verificarOrientacao()
            if verificar_sensor_frontal(posicao,orientacao) != "*":   
                render(matriz,self.posicao,"")
                # Atualiza a posição com base na orientação
                if orientacao == 'S':  # Sul
                    self.posicao = [posicao[0]+1, posicao[1]]  # Move para baixo (incrementa o Y)
                elif orientacao == 'N':  # Norte
                    self.posicao = [posicao[0] - 1, posicao[1]]  # Move para cima (decrementa o Y)
                elif orientacao == 'L':  # Leste
                    self.posicao = [posicao[0], posicao[1] + 1]  # Move para a direita (incrementa o X)
                elif orientacao == 'O':  # Oeste
                    self.posicao = [posicao[0], posicao[1] - 1]  # Move para a esquerda (decrementa o X)
                render(matriz,self.posicao,self.simbolo)
            elif(verificar_sensor_frontal(posicao,orientacao) == "H"):
                print("HUMANO A FRENTE")
                pegarHumano()
            elif(verificar_sensor_frontal(posicao,orientacao) == "E" and self.comHumano == True):
                print("ENTRADA A FRENTE")
                ejetarHumano()
            else:
                print("PAREDE A FRENTE")
        def calcularRota():
            rota_saida = self.caminho[::-1]  # Reverte a lista
            for indice in rota_saida:
                if isinstance(indice, list):  # Verifica se indice é uma lista
                    pass  # Se for uma lista, não faz nada (ou adicione sua lógica aqui)
                    render(matriz,indice,self.simbolo)
                    sleep(2)
                elif isinstance(indice, (int)):  # Verifica se é um número (int ou float)
                    indice = (indice % 4)   # Aplica a operação
                    for i in range(indice):
                        girarDireita()  
        def pegarHumano():
            pass
        def ejetarHumano():
            pass

        # Exemplo de uso:
        verificarOrientacao()
        render(matriz,self.posicao,self.simbolo)
        sleep(2)
        andarFrente(self,self.posicao,self.orientacao)
        sleep(2)
        andarFrente(self,self.posicao,self.orientacao)
        sleep(2)
        andarFrente(self,self.posicao,self.orientacao)
        sleep(2)
        girarDireita()
        girarDireita()
        girarDireita()
        sleep(2)
        andarFrente(self,self.posicao,self.orientacao)
        sleep(2)
        print(self.caminho)

robo = Robo("3x5.txt")
#print(robo.orientacao)
# print(robo.simbolo)
# print(robo.entrada)
#print(robo.posicao)


