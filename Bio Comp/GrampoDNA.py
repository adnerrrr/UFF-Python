from os import name, system

baseEquivalente = {
    "A" : "T",
    "T" : "A",
    "G" : "C",
    "C" : "G"
}

grampos = []

class Grampo: # classe para guardar mais facilmente as variaveis de cada grampo
    def __init__(self, prefixo, arco, sufixo, posicao):
        self.prefixo = prefixo
        self.arco = arco
        self.sufixo = sufixo
        self.posicao = posicao

def limpa(): # funcao para limpar o terminal
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def reversa(fita): # acha a reversa de uma fita
    rev = ""
    for i in range(len(fita) - 1, -1, -1):
        rev += fita[i]
    return rev

def complementar(fita): # acha a complementar de uma fita
    comp = ""
    for i in range(len(fita)):
        comp += baseEquivalente[fita[i]]
    return comp

def mostraGrampos(): # print de todos os grampos encontrados
    global grampos
    if grampos == []:
        print("Nenhum grampo encontrado")
        return
    for valor in grampos:
        print()
        printBonito(len(valor.arco) % 2, valor)
        print("Esse grampo fica na posicao " + str(valor.posicao))
        print()

def printBonito(k, gram):
    pref = gram.prefixo
    arco = gram.arco
    suf = gram.sufixo
    aux = ""
    for i in range(int((len(arco) + k)/ 2)):
        pref += " " + arco[i]
        suf += " " + arco[-1-i]
    print(pref)
    if (k == 1):
        for i in range(len(pref)):
            aux += " "
        aux += arco[int((len(arco) + 1 )/ 2)]
    print(aux)
    print(suf)

def achaGrampo(fita, pref, k):
    arco = ""
    for i in range(3, 20-k-k+1): # limita o arco pra nunca diminuir o tamanho da fita inversa
        arco = fita[k:k+i]
        suf = fita[k+i:k+i+k]
        if (pref == complementar(reversa(suf))) and (len(arco) > 2) and (len(arco) < k):
            guardaGrampo(pref, arco, suf)
    

def guardaGrampo(pref, arco, suf):
    global grampos, pos
    grampos.append(Grampo(pref, arco, suf, pos))
    pos += len(pref) * 2 + len(arco) - 1

def testaFita(fita, k):
    global pos
    pos = 0
    pref = ""
    while pos != len(fita) - 1:
        pref = fita[pos:pos+k]
        tamanho = fita[pos:pos+20] # garante que teremos ate 20 como tamanho maximo do grampo
        # nao precisa limitar o minimo de 12 pq o k e a limitacao do arco ja fazem isso
        achaGrampo(tamanho, pref, k)
        pos += 1

def main():
    global grampos
    continua = "s"
    while continua == "s":
        limpa()
        grampos = []
        fita = input("Digite a fita: ").upper()
        k = int(input("Digite o tamanho do pescoco do grampo: "))
        if k <= 4:
            print("Tamanho invalido")
        else:
            testaFita(fita,k)
            mostraGrampos()
            continua = input("Quer continuar? [S/N] ").lower()

if __name__ == "__main__":
    main()

