#Bibliotecas usadas
import scipy.io as sio
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation# não é usada mais
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
#----------------


#Criação de dois vetores vasioz
VetorPos = [0]
#vetor com valores do limiar
VetorLimiar = [0]
#vetor com dados do arquivo aberto
dadoBruto = [0]
#valores após aplicação do filtro
suavizado = [0]
# Vetor de tempo para valores lidos
n2 = [0]
#Esvaziar vetores
VetorPos.remove(0)
VetorLimiar.remove(0)
suavizado.remove(0)
dadoBruto.remove(0)
n2.remove(0)

#Poisição do primeiro dado relevante
startpoint = 0

#Sensor que sera utilizado do arquivo aberto
SensorEscolhido = 0

#Quantidade de sensores no arquivo aberto
NumSensores = 0

#APENAS PARA TESTES
arqv = 'DB2_s1/dado1_filtrado.mat'  # Localização Arquivo
Var = 'emg1_filtrado'  # Nome variavel do Arquivo .mat
kc = 1 # Valore de teste para constante k(não é UTILIZADO ATUALMENTE)
#------------------


#posição inicial
P0 = 1
#posição final
Pn = 70000

#variavel auxiliar para filtragem do sinal
acumulate = 1

#Ared deve ser igual a 1 para media movel
Ared = 100  # Arredondar a cada




#Configurações plot original (NÂO É USADO MAIS)
fig, ax = plt.subplots()
fig.set_tight_layout(True)

fy = [0]
xi = [0]

ax.set_xlim(0, 100)
ax.set_ylim(0, 300)
#-------------------------



n_IntervalManual = 0
#Lógica Criar intervalos manualmente
'''
------------------ Pegar X ------- Botão pegar X clicado
Acompanhar posição do mouse em relação ao grafico
    Guardar posição x do grafico aou clicar dentro do grafico
------------------ Pegar x1 ------- Botão pegar Y clicado
Acompanhar posição do mouse em relação ao grafico
    Guardar posição x do grafico aou clicar dentro do grafico
'''


#Função para animação de grafico original (NÃO É USADO MAIS)
def anim(i):
    if i < 600:
        ax.set_xlim(i, i + 100)
# --------------------------------

#Abrir arquivos .mat de nome armazenado na string Arq
def openMAT(Arq):
    #Arquivo
    file = sio.loadmat(Arq)
    print(type(file))
    #Acumulador auxiliar para arredondamento
    lj = 0
    #Default abrir primeiro sensor no arquivo
# LEMBRETE: Permitir que usuario escolha
    sensor = 0

    #vars = str(sio.whosmat(Arq))#DB2_s1/dado1 DB2_s1/S1_E1_A1
    global acumulate

    #Pn representa o numero de dados que sera aberto
# LEMBRETE: permitir que usuario escolha
    global Pn

    #PROGRAMAR MEDIA MOVEL
    #Ared é igual a 1 pois o vetor final tera o mesmo tamanho do inicial
    #Ared = 1
    #
    #tRATAR ZEROS, começar de -99 a 0, terminar de Pn a Pn + 99
    #Quando valores não existirem considerar como zero

    #Tenta Abrir o .mat de duas maneiras diferentes, uma como lista de sensores, outra como matriz
    try:
        #Analisa uma quantidade de dados igual a Pn definido por padrão
    # LEMBRETE: definir pn por tamanho do vetor
        #Pega o nome da variavel armazenando os sensores
        Var = str(sio.whosmat(Arq)[0][0])
        #print(Var)

        #Começa a realizar media estatica
        for i in range(startpoint + 1, startpoint + int(Pn / Ared)):  # tirar 0 de 100000
            #Arredondar a cada 100
            for j in range(1, Ared + 1):
                #Acumula a soma dos modulos
                if file[Var][SensorEscolhido][lj + j] >= 0:
                    acumulate += file[Var][SensorEscolhido][lj + j]
                else:
                    acumulate -= file[Var][SensorEscolhido][lj + j]

                # após 100 elementos guarda o valor arredondado
                if j % Ared == 0:
                    suavizado.append(acumulate / Ared)
                #Armazena todas os dados do sensor na variavel dado bruto
                dadoBruto.append(file[Var][SensorEscolhido][lj + j])
            #zera acumulador
            acumulate = 0

            #Contador para ignorar partes ja arredondas
            lj += Ared

        # Preenche vetor auxiliar tempo para valores da variavel suavizado
        for i in range(int(P0), int((Pn - startpoint) / Ared)):  # tirar 0 de 1001
            n2.append(i)

        #Guarda valores na variavel VetorPos
    # LEMBRETE: remover n2
        VetorPos = n2

    except:
        print('EXECUTADOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo')
        # Pega o nome da variavel armazenando os sensores
        Var = str(sio.whosmat(Arq)[0][0])
        #print(str(sio.whosmat(Arq)[0]))
        #print(Var)

        # definir valores de P0 e Pn baseados no arquivo

        #Quantitade de sensores disponiveis
        NumSensores = int(len(file[Var][sensor]))

        #Pn é definido apartir do tamanho dos sensores de dados
        Pn = int(len(file[Var]))
    # LEMBRETE: permitir definição de limite maximo para tamanho

        #Calculo media fixa
        for i in range(startpoint , startpoint + int(Pn / Ared)-1):  # tirar 0 de 100000
            # Arredondar a cada 100
            for j in range(1, Ared + 1):
                # Acumula a soma dos modulos
                if file[Var][lj + j][sensor] >= 0:
                    acumulate += file[Var][lj + j][sensor]
                else:
                    acumulate -= file[Var][lj + j][sensor]

                # após 100 elementos guarda o valor arredondado
                if j % Ared == 0:
                    suavizado.append(acumulate / Ared)

                # Armazena todas os dados do sensor na variavel dado bruto
                dadoBruto.append(file[Var][lj + j][sensor])

            #Zera acumulador
            acumulate = 0

            # Contador para ignorar partes ja arredondas
            lj += Ared

        #print(suavizado)

        # Preenche vetor auxiliar tempo para valores da variavel suavizado
        for i in range(int(P0), int((Pn - startpoint) / Ared)):  # tirar 0 de 1001
            n2.append(i)

        # Guarda valores na variavel VetorPos
    # LEMBRETE: remover n2
        VetorPos = n2


#Abre arquivos CSV
def openCSV(Arq):
    #Abre arquivo de nome na string Arq usando ; como parametro
    file = pd.read_csv(Arq, delimiter=';')
    print(type(file))
    #    EXEMPLI:#   teste = pd.read_csv('Planilha1.csv', delimiter=';')
    print(file['11'])# sensor escolhido
    print(file.iloc[1, 0])  # pega elemento da (linha,coluna)

    # Acumulador auxiliar para arredondamento
    lj = 0

    #acumulador auxiliar
    global acumulate

    #Defini posição final baseado no vetor lido
  # LEMBRETE: trocar posicao_final por Pn
    posicao_final = len(file[SensorEscolhido])

    #Calcula media fixa do arquivo CSV
    for i in range(startpoint + 1, startpoint + int(posicao_final / Ared)):  # tirar 0 de 100000
        #Calcula media a cada 100 valores
        for j in range(1, Ared + 1):

            #Soma modulo dos valores
            if file[SensorEscolhido][lj + j] >= 0:# LEMBRETE: -CHECAR ORGANIZAÇÃO DE ARQUIVOS CSV E TXT PARA SABER COMO IMPORTAR dados
                acumulate += file[SensorEscolhido][lj + j]
            else:
                acumulate -= file[SensorEscolhido][lj + j]

            #Guarda a media dos 100 valores acumulados dentro da variavel suavizado
            if j % Ared == 0:
                suavizado.append(acumulate / Ared)
            #Guarda todos os valores lidos dentro da variavel dadobruto
            dadoBruto.append(file[SensorEscolhido][lj + j])

        #zera acumulador
        acumulate = 0

        # Contador para ignorar partes ja arredondas
        lj += Ared

    file.close()

#Abrir Arquivos de texto
#   LEMBRETE: Abrir arquivos de texto salvos pelo programa
def openTXT(Arq):
    file = pd.read_csv(Arq, delimiter=';')
    #       teste2 = pd.read_csv('Planilha1 (cópia).txt', delimiter=';')
    print(file['11'])
    print(file.iloc[1, 0])
    file.close()

#Abrir Arquivo de dados
def getDATA(Arq, Escolhaformat):
    # Escolher formato do arquivo que vai ser aberto e chamar resoectiva função
    Choices = {
        ".mat": openMAT,
        ".csv": openCSV,
        ".txt": openTXT
    }
    #escolhe função baseado na variavel Escolhaformat e passa a variavel Arq para as funções
    #Usando openMat como default caso o formato não seja escolhido
    Choices.get(Escolhaformat, openMAT)(Arq)

#====Função Principal====
#-Abre as janelas
#-Abre os arquivos e processa seus dados
#-
def SEG(Arquivo, Var, k):

    # Janela do programa
    class MatplotlibWidget(QMainWindow):
        #Inicializa janela do programa
        def __init__(self):
            QMainWindow.__init__(self)

            #Define qual tela esta sendo mostrada
            self.m = "B"

            #Carrega UI para abrir arquivos
            loadUi("AbrirArquivos.ui", self)

            #Associa o botão bt_abrirArq com a função openArq
            self.bt_abrirArq.clicked.connect(self.openArq)

        #Função para voltar a tela de abertura de arquivos
        def ImportarArq(self):
            # Carrega UI para abrir arquivos
            loadUi("AbrirArquivos.ui", self)

            # Associa o botão bt_abrirArq com a função openArq
            self.bt_abrirArq.clicked.connect(self.openArq)

# CONTINUAR A FORMATAR DAQUI:::::::::
        def openArq(self):
            self.Mtrack = 0;
            #LEMBRETE: CHECAR TAMANHO DO ARQUIVO PARA PROCESSAR DADOS
            try:
                if self.FormatArq.currentText() == ".mat":
                    file = sio.loadmat(self.NomeArq.text() + self.FormatArq.currentText())
                if self.FormatArq.currentText() == ".csv":
                    file = pd.read_csv(self.NomeArq.text() + self.FormatArq.currentText(), delimiter=';')
                if self.FormatArq.currentText() == ".txt":
                    file = pd.read_csv(self.NomeArq.text() + self.FormatArq.currentText(), delimiter=';')
                suavizado.clear()
                n2.clear()

                getDATA(self.NomeArq.text() + self.FormatArq.currentText(), self.FormatArq.currentText())
                # ------------Criar função para abrir arquivos------------------
                # animation = FuncAnimation(fig, func=anim, frames=np.arange(0, 650, 2), interval=60)

                # Abre no porcessamento que realiza o calculo do limiar para
                if self.Modo_abrir.currentText() == "Processamento Automatico":

                    loadUi("processamento_automatico.ui", self)
                    self.actionImport.triggered.connect(self.ImportarArq)
                    self.actionExport.triggered.connect(self.ExportArq)

                    self.m = "A"

                    self.setWindowTitle("Processamento de sEMG")

                    self.bt_update.clicked.connect(self.update_graph)  # trpcar ŕa botão update

                    self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

                    self.IntervalosManual = []
                    self.Linhas = 0

                    self.Box_Del = QLineEdit()

                    self.verticalLayout_5.addWidget(self.Box_Del)

                    self.bt_Add.clicked.connect(self.insert_normal_textbox)
                    self.bt_del.clicked.connect(self.remRow)
                    # self.bt_play.clicked.connect(self.printManual)

                    self.MplWidget.canvas.mpl_connect("button_press_event", self.on_press)
                    self.MplWidget.setMouseTracking(True)
                    self.mouse_bt.clicked.connect(self.PegarcordMouse)


                if self.Modo_abrir.currentText() == "Intervalos manuais":

                    loadUi("Processamento_Manual.ui", self)
                    self.actionImport.triggered.connect(self.ImportarArq)
                    self.actionExport.triggered.connect(self.ExportArq)
                    self.m = "M"
                    self.setWindowTitle("Processamento de sEMG")

                    self.bt_update.clicked.connect(self.printManual)  # trpcar ŕa botão update

                    self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

                    self.IntervalosManual = []
                    self.Linhas = 0

                    self.Box_Del = QLineEdit()

                    self.verticalLayout_5.addWidget(self.Box_Del)

                    self.bt_Add.clicked.connect(self.insert_normal_textbox)
                    self.bt_del.clicked.connect(self.remRow)
                    # self.bt_play.clicked.connect(self.printManual)

                    self.MplWidget.canvas.mpl_connect("button_press_event", self.on_press)
                    self.MplWidget.setMouseTracking(True)
                    self.mouse_bt.clicked.connect(self.PegarcordMouse)
            except:
                #caso ocorra algum problema na abertura do arquivo essa mensagem de erro aparece no console
                print("arquivo não encontrado")

        def insert_normal_textbox(self):

            self.xi_txt = QLineEdit()
            label1 = QLabel("Xi= ")
            label2 = QLabel('Xf= ')
            self.xf_txt = QLineEdit()

            self.grid = QGridLayout()

            # self.delete_btn.clicked.connect(self.remRow)
            #self.xi_btn = QPushButton('Mouse')
            #self.xf_btn = QPushButton('Mouse')
            '''self.xi_btn, self.xf_btn,'''
            self.IntervalosManual.append([label1, label2, self.xf_txt, self.xi_txt])
            self.grid.addWidget(self.IntervalosManual[self.Linhas][0], self.Linhas, 0)
            self.grid.addWidget(self.IntervalosManual[self.Linhas][3], self.Linhas, 1)
            #self.grid.addWidget(self.IntervalosManual[self.Linhas][2], self.Linhas, 2)

            self.grid.addWidget(self.IntervalosManual[self.Linhas][1], self.Linhas, 3)
            self.grid.addWidget(self.IntervalosManual[self.Linhas][2], self.Linhas, 4)
            #self.grid.addWidget(self.IntervalosManual[self.Linhas][3], self.Linhas, 5)

            self.Linhas += 1
            self.verticalLayout_4.addLayout(self.grid)


            global n_IntervalManual
            n_IntervalManual+= 1
        def remRow(self):
            if self.Box_Del.text().isdigit():
                if int(self.Box_Del.text()) > 0 and (int(self.Box_Del.text()) - 1) < self.Linhas:
                    for i in range(0, 4):
                        self.grid.removeWidget(self.IntervalosManual[int(self.Box_Del.text()) - 1][0])
                        self.IntervalosManual[int(self.Box_Del.text()) - 1][0].deleteLater()
                        del self.IntervalosManual[int(self.Box_Del.text()) - 1][0]
                    self.IntervalosManual.remove(self.IntervalosManual[int(self.Box_Del.text()) - 1])
                    self.Linhas -= 1
                    if self.Linhas < 0:
                        self.Linhas = 1
                    global n_IntervalManual
                    n_IntervalManual -= 1
            else:
                print(self.Box_Del.text())
            self.printManual()

        def remRow(self):
            if self.Box_Del.text().isdigit():
                if int(self.Box_Del.text()) > 0 and (int(self.Box_Del.text()) - 1) < self.Linhas:
                    for i in range(0, 4):
                        self.grid.removeWidget(self.IntervalosManual[int(self.Box_Del.text()) - 1][0])
                        self.IntervalosManual[int(self.Box_Del.text()) - 1][0].deleteLater()
                        del self.IntervalosManual[int(self.Box_Del.text()) - 1][0]
                    self.IntervalosManual.remove(self.IntervalosManual[int(self.Box_Del.text()) - 1])
                    self.Linhas -= 1
                    if self.Linhas < 0:
                        self.Linhas = 1
                    global n_IntervalManual
                    n_IntervalManual -= 1
            else:
                print(self.Box_Del.text())
            #self.printManual()


        def update_graph(self):
            startpoint = P0 - 1
            global acumulate
            n = [startpoint]

            lj = 0

            VetorLimiar.clear()
            ''' IMPRIMIR DADO BRUTO
            n00 = []
            for i in range(0,Pn-100):
                n00.append(i)
            self.MplWidget.canvas.axes.plot(n00,dadoBruto)
            self.MplWidget.canvas.draw()
            '''
            # ---------------------------------------------
            # Criar funcção que pega intervalos fornecidos pelo usuario
            #
            # -----------------------

            M_lb = 0  # medialinhabase(0 a 30)
            Dp = 0  # desvio padrão
            contp = 0
            for i in self.IntervalosManual:
                if ((i[2].text().isdigit()) and (i[3].text().isdigit())):
                    xi = int(i[3].text())
                    xf = int(i[2].text())
                    for x in range(xi,xf):
                        M_lb += suavizado[x]
                        Dp += M_lb - suavizado[x]
                        contp+=1



            if(contp != 0):
                M_lb /= contp
                Dp /= contp
            Dp = math.sqrt(Dp)
            try:
                k = float(self.txt_K.text())
            except ValueError:
                k = 0.5

            self.limiar = M_lb + Dp * k

            print(M_lb)

            l = [0]
            l.clear()
            for i in range(int(P0), int(Pn / Ared)):  # tirar 0 de 1001
                l.append(self.limiar)
                VetorLimiar.append(self.limiar)

            plt.plot(n2, suavizado)


            plt.plot(n2, l)
            # plt.show()

            ant = 0
            x1 = 0
            x2 = 0
            y1 = self.limiar
            y2 = 300
            test = 0
            seq = 0
            uma = 0

            self.tol = 3
            self.Max_tol = 0
            try:
                self.Max_tol = int(self.Tol_txt.text())
            except:
                self.Max_tol = 0

            self.min_interval = 10
            try:
                self.min_interval = int(self.min_interv.text())
            except:
                self.min_interval = 10
            #############################

            INTERVALO = 100  # Pegar de caixa de texto om intervalo de tempo
            comeco = 0
            if (self.tam_graf.text().isdigit()) and int(self.tam_graf.text()) > 0 and int(self.tam_graf.text()) < int(Pn / Ared):
                INTERVALO = int(self.tam_graf.text())
            comeco = startpoint  # Pegar caixa inicio intervalo
            if (self.x0_graf.text().isdigit()) and int(self.x0_graf.text()) > 0 and int(self.x0_graf.text())+ INTERVALO < int(Pn / Ared):
                comeco = int(self.x0_graf.text())
            self.MplWidget.canvas.axes.clear()

            self.tol = 3



            ant = 0
            seq = 0
            self.MplWidget.canvas.axes.clear()

            CopVetPos = [0]
            CopSuav = [0]
            CopLimiar = [0]
            CopVetPos.remove(0)
            CopSuav.remove(0)
            CopLimiar.remove(0)
            for i in range(comeco, comeco+INTERVALO):
                CopVetPos.append(i)
                CopSuav.append(suavizado[i])
                CopLimiar.append(VetorLimiar[i])
                if (suavizado[i] >= self.limiar and ant == 1):
                    self.tol = 0
                    seq += 1
                if (suavizado[i] < self.limiar and ant == 1) or (i == comeco+INTERVALO-1 and ant == 1):
                    if (self.tol > self.Max_tol) or i == comeco+INTERVALO-1:
                        ant = 0
                        x2 = i
                        if (seq >= self.min_interval or i == comeco+INTERVALO-1):
                            self.MplWidget.canvas.axes.plot([x1, x2], [(self.limiar) , (self.limiar)])

                            rectangle = plt.Rectangle((x1, 0), x2 - x1, y2, fc='r')  # (x,y) começo (x,y) final

                            self.MplWidget.canvas.axes.plot([x1-1,x1-1],[0,self.limiar])
                            self.MplWidget.canvas.axes.plot([x2, x2], [0, self.limiar])
                            # print(x1)
                            # print(x2)
                            # print(seq)
                        # n_sinais+=1
                        seq = 0
                        self.tol = 0
                    else:
                        self.tol += 1
                if suavizado[i] >= self.limiar and ant == 0:
                    x1 = i
                    ant = 1
            CopVetPos.remove(CopVetPos[0])
            CopSuav.remove(CopSuav[0])
            CopLimiar.remove(CopLimiar[0])
            self.MplWidget.canvas.axes.plot(CopVetPos, CopSuav)
            self.MplWidget.canvas.axes.plot(CopVetPos, CopLimiar)
            self.MplWidget.canvas.axes.legend(('EMG', 'limiar'), loc='lower right')
            self.MplWidget.canvas.axes.set_title('Sinal sEMG')
            self.MplWidget.canvas.draw()
            l.clear
        def printManual(self):

            Y_Maxima = 150

            INTERVALO = 100 # Pegar de caixa de texto om intervalo de tempo
            comeco = 0
            if (self.tam_graf.text().isdigit()) and int(self.tam_graf.text()) > 0 and int(self.tam_graf.text()) < int(Pn / Ared):
                INTERVALO = int(self.tam_graf.text())
            comeco = startpoint # Pegar caixa inicio intervalo
            if (self.x0_graf.text().isdigit()) and int(self.x0_graf.text()) > 0 and int(self.x0_graf.text()) < int(Pn / Ared) and int(self.x0_graf.text()) + INTERVALO<int(Pn / Ared) :
                comeco = int(self.x0_graf.text())
            self.MplWidget.canvas.axes.clear()
            t = [0]
            suavs = [0]
            t.remove(0)
            suavs.remove(0)

            self.MplWidget.canvas.axes.legend(('EMG', 'limiar'), loc='upper right')
            self.MplWidget.canvas.axes.set_title('Sinal sEMG')
            for i in range(comeco,comeco+INTERVALO):
                if i < int(Pn / Ared):
                    t.append(i)
                    suavs.append(suavizado[i])

            self.MplWidget.canvas.axes.plot(t,suavs)
            #self.MplWidget.canvas.axes.plot(VetorPos, suavizado)
            #self.MplWidget.canvas.axes.plot(VetorPos, VetorLimiar)

            for i in self.IntervalosManual:

                if(i[2].text().isdigit()) and (i[3].text().isdigit()) :

                    if int(i[2].text()) < comeco+INTERVALO and int((i[3].text()))> comeco and int(i[2].text()) > comeco and int((i[3].text()))< comeco + INTERVALO:
                        xi = int(i[3].text())
                        xf = int(i[2].text())
                        self.MplWidget.canvas.axes.plot([xi, xi], [0, suavizado[xi]])
                        self.MplWidget.canvas.axes.plot([xf, xf], [0, suavizado[xf]])
                        self.MplWidget.canvas.axes.plot([xi, xf], [suavizado[xf], suavizado[xf]]);
                    elif int(i[2].text()) < comeco+INTERVALO and int(i[2].text()) > comeco:
                        print("caso1")
                        xi = comeco
                        xf = int(i[2].text())
                        self.MplWidget.canvas.axes.plot([xi, xi], [0, suavizado[xi]])
                        self.MplWidget.canvas.axes.plot([xf, xf], [0, suavizado[xf]])
                        self.MplWidget.canvas.axes.plot([xi, xf], [suavizado[xf], suavizado[xf]]);
                    elif int((i[3].text()))> comeco and int((i[3].text()))< comeco + INTERVALO:
                        print("caso2")
                        xi = int(i[3].text())
                        xf = comeco+INTERVALO
                        self.MplWidget.canvas.axes.plot([xi, xi], [0, suavizado[xi]])
                        self.MplWidget.canvas.axes.plot([xf, xf], [0, suavizado[xf]])
                        self.MplWidget.canvas.axes.plot([xi, xf], [suavizado[xf], suavizado[xf]]);
            self.MplWidget.canvas.draw()#Desenhar resultado


       # def mousePressEvent(self, QMouseEvent):
            #print(QMouseEvent.pos())

        #def mouseReleaseEvent(self, QMouseEvent):
                # cursor = QtGui.QCursor() Não entendi
                # print(cursor.pos())
            #print(QMouseEvent.pos(), "----")
        def on_press(self, event):
            #testa se o mouse esta coletando o segundo dado
            if self.Mtrack == 2:
                if self.Box_Del.text().isdigit():
                    if int(self.Box_Del.text()) > 0 and (int(self.Box_Del.text()) - 1) < self.Linhas:
                        Y_Maxima = 150
                        INTERVALO = 100  # Pegar de caixa de texto om intervalo de tempo
                        comeco = 0
                        if (self.tam_graf.text().isdigit()) and int(self.tam_graf.text()) > 0 and int(
                                self.tam_graf.text()) < int(Pn / Ared):
                            INTERVALO = int(self.tam_graf.text())
                        comeco = startpoint  # Pegar caixa inicio intervalo
                        if (self.x0_graf.text().isdigit()) and int(self.x0_graf.text()) > 0 and int(
                                self.x0_graf.text()) + INTERVALO < int(Pn / Ared):
                            comeco = int(self.x0_graf.text())

                        PixelDistCanvas = 53
                        PixelDistZero = 10

                        print(str((event.x - PixelDistCanvas - PixelDistZero)*((INTERVALO)/283) +comeco))

                        self.IntervalosManual[int(self.Box_Del.text())-1][2].setText(str(int((event.x - PixelDistCanvas - PixelDistZero)*((INTERVALO)/283) +comeco)))
                        # self.label_2.setText('Mouse coords: ( %d : %d )' % ((event.x - PixelDistCanvas-PixelDistZero + comeco)*((INTERVALO-comeco)/283),event.y))
                self.Mtrack = 0
                if self.m == "A":
                    self.update_graph()
                if self.m == "M":
                    self.printManual()
            #testa se o mouse esta coletando o primeiro dado
            if self.Mtrack == 1:
                #Checa se o indice de intervalo selecionado é um digito numerico
                if self.Box_Del.text().isdigit():
                    #Checa se o indice é maior que zero e menor que o Numero atual de indices
                    if int(self.Box_Del.text()) > 0 and (int(self.Box_Del.text()) - 1) < self.Linhas:
                        Y_Maxima = 150

                        #valor padrão para o intervalo é 100
                        INTERVALO = 100
                        #valo padrão para x0
                        comeco = 0
                        #checa se o intervalo digitado é numerp maior que zero e é menor que a quantidade de dados
                        if (self.tam_graf.text().isdigit()) and int(self.tam_graf.text()) > 0 and int(
                                self.tam_graf.text()) < int(Pn / Ared):
                            INTERVALO = int(self.tam_graf.text())
                        comeco = startpoint  # Pegar caixa inicio intervalo
                        if (self.x0_graf.text().isdigit()) and int(self.x0_graf.text()) > 0 and int(
                                self.x0_graf.text()) + INTERVALO < int(Pn / Ared):
                            comeco = int(self.x0_graf.text())

                        PixelDistCanvas = 53
                        PixelDistZero = 10

#DB2_s1/S1_E2_A1
                        print('pos pixel:' + str(event.x))
                        print('calculos' +str((event.x - PixelDistCanvas - PixelDistZero)*((INTERVALO)/283) +comeco))
                        print('começo:'+str(comeco))
                        print('intervalo:' + str(INTERVALO))
                        self.IntervalosManual[int(self.Box_Del.text())-1][3].setText(str(int((event.x - PixelDistCanvas - PixelDistZero)*((INTERVALO)/283) +comeco)))
                        # self.label_2.setText('Mouse coords: ( %d : %d )' % ((event.x - PixelDistCanvas-PixelDistZero + comeco)*((INTERVALO-comeco)/283),event.y))
                self.Mtrack = 2
        def ExportArq(self):
            loadUi("salvar.ui",self)
            self.Lx0 = []
            self.Lxi = []
            if self.m == "M":
                for i in self.IntervalosManual:
                    if ((i[2].text().isdigit()) and (i[3].text().isdigit())):
                        xi = int(i[3].text())
                        self.Lx0.append(xi)
                        xf = int(i[2].text())
                        self.Lxi.append(xf)
                self.bt_save.clicked.connect(self.salvarMA)
            if self.m == "A":
                self.bt_save.clicked.connect(self.salvarAU)
        def salvarMA(self):
            file = open(self.name_txt.text()+"EMG","w+")

            file.write("Intervalos com sinal:\n")

            for i in range(0,len(self.Lx0)):
                file.write("[{},{}]\n".format(self.Lx0[i], self.Lxi[i]))


            #Imprime intervalos sem sinal (não funciona se intervalos não estiverem em ordem crescente)
            file.write("Intervalos sem sinal:\n")
            if self.Lx0[0] !=0:
                file.write("[{},{}]\n".format(0, self.Lx0[0] - 1))
            for i in range(0, len(self.Lx0)):
                if i < len(self.Lx0) - 1:
                    file.write("[{},{}]\n".format(self.Lxi[i] + 1, self.Lx0[i + 1] - 1))
                elif self.Lxi[i] < Pn / Ared:
                    file.write("[{},{}]\n".format(self.Lxi[i] + 1, int(Pn / Ared)))


            loadUi("Processamento_Manual.ui", self)
            self.actionImport.triggered.connect(self.ImportarArq)
            self.actionExport.triggered.connect(self.salvarMA)
            self.setWindowTitle("Processamento de sinais sEMG")

            self.bt_update.clicked.connect(self.printManual)  # trpcar ŕa botão update

            self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

            self.IntervalosManual = []
            self.Linhas = 0

            self.Box_Del = QLineEdit()

            self.verticalLayout_5.addWidget(self.Box_Del)

            self.bt_Add.clicked.connect(self.insert_normal_textbox)
            self.bt_del.clicked.connect(self.remRow)
            # self.bt_play.clicked.connect(self.printManual)

            self.MplWidget.canvas.mpl_connect("button_press_event", self.on_press)
            self.MplWidget.setMouseTracking(True)
            self.mouse_bt.clicked.connect(self.PegarcordMouse)
            file.close()
        def salvarAU(self):
            file = open(self.name_txt.text()+"EMG","w+")

            file.write("Intervalos com sinal:\n")

            seq = 0
            x1 = 0
            ant = 0
            self.tol = 0
            x0s = []
            x2s = []
            for i in range(0, len(suavizado)):
                if (suavizado[i] >= self.limiar and ant == 1):
                    seq += 1
                    self.tol = 0
                if (suavizado[i] < self.limiar and ant == 1) or (i == len(suavizado)-1 and ant == 1):
                    if (self.tol > self.Max_tol) or (i == len(suavizado)-1):
                        ant = 0
                        x2 = i
                        x2s.append(x2)
                        x0s.append(x1)
                        if (seq >= self.min_interval or i == len(suavizado)-1):
                            file.write("[{},{}]\n".format(x1,x2))
                        seq = 0
                        self.tol = 0
                    else:
                        self.tol += 1
                if suavizado[i] >= self.limiar and ant == 0:
                    x1 = i
                    ant = 1
            file.write("Intervalos sem sinal:\n")
            file.write("[{},{}]\n".format(0, x0s[0]-1))
            for i in range(0,len(x0s)):
                if i < len(x0s)-1:
                    file.write("[{},{}]\n".format(x2s[i]+1, x0s[i+1]-1))
                elif x2s[i] < Pn/Ared:
                    file.write("[{},{}]\n".format(x2s[i]+1, Pn/Ared))


            loadUi("processamento_automatico.ui", self)
            self.actionImport.triggered.connect(self.ImportarArq)
            self.actionExport.triggered.connect(self.ExportArq)


            self.setWindowTitle("Processamento de sEMG")

            self.bt_update.clicked.connect(self.update_graph)  # trpcar ŕa botão update

            self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

            self.IntervalosManual = []
            self.Linhas = 0

            self.Box_Del = QLineEdit()

            self.verticalLayout_5.addWidget(self.Box_Del)

            self.bt_Add.clicked.connect(self.insert_normal_textbox)
            self.bt_del.clicked.connect(self.remRow)
            # self.bt_play.clicked.connect(self.printManual)

            self.MplWidget.canvas.mpl_connect("button_press_event", self.on_press)
            self.MplWidget.setMouseTracking(True)
            self.mouse_bt.clicked.connect(self.PegarcordMouse)
            file.close()
        def PegarcordMouse(self):
            self.Mtrack = 1;

    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()

    #plt.show()
# Opções de variaveis
# ---------------'''
'''
variaveis = sio.whosmat('DB2_s1/dado1_filtrado.mat')
vars = str(variaveis)
print(vars)'''
# ---------------


SEG(arqv, Var, kc)  # Adicionar variaveis (y inicial) e y final, x final

# Arq = sio.loadmat('DB2_s1/dado1.mat')

startpoint = 0

#SensorEscolhido = 1
#getDATA(arqv, '.csv')# NOME DO ARQUIVO e FORMATO DO ARQUIVO
#print(suavizado)

