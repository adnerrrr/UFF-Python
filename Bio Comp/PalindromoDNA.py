from os import name, system

# Faça um programa na sua linguagem de programação favorita (python ou linguagem C (ou C++)) que dado 
# um valor k (inteiro e par). encontre todas as sub-cadeias que sejam palíndromos maximais de tamanho k (k>=4), 
# e imprima o palíndromo a posição de início de cada sub-cadeia correspondente (se um palíndromo se repetir, 
# você pode só imprimir as posições onde ele aparece e imprimi-lo apenas uma vez).

# Teste seu programa para as sequências abaixo:

# ACTATCCGCGTTTTTTCCAAAGTGAGCAAAAATGAAAGCTACGATCCCCCCCCCCTGAAGTTATATG
# AGTGTTTTTGATAGAGCGTAAATATAAAACGTTTTATAGCCGTAATCGAAAAGCGCGATACTAAAAAAAAAACTATGAAAAAAAACTCTTG

bases = {
    "A" : "T",
    "T" : "A",
    "C" : "G",
    "G" : "C"
} # dicionario para traducao das fitas

dados = ["", 0]

def reversa(fitaOG):
    fitaR = ""
    for i in range(len(fitaOG)):
        fitaR += bases[fitaOG[i]] # cria a fita complementar
    return fitaR

def limitaSequencia(fitaOG, fitaR, pos):
    global dados

    for i in range(len(fitaOG), pos, -1): # percorre a sequencia de tras pra frente procurando letras iguais

        if (fitaOG[pos] == fitaR[i-1]):
            # quando achar letras iguais checamos se e palindromo
            if checaPalindromo(fitaOG[pos:i], fitaR[pos:i]):
                if (fitaOG[pos:i] not in dados) and (fitaOG[pos:i] not in dados[-2]): # garante que nao tem repeticao e que o palindromo e maximal
                    dados += [fitaOG[pos:i], pos+1]

    if pos != len(fitaOG):
        limitaSequencia(fitaOG, fitaR, pos+1) # garante recursividade para checar toda a fita original

def checaPalindromo(seq1, seq2):
    seq = inverte(seq2)
    for i in range(len(seq1)): # compara a sequencia original com a complementar invertida
        if seq1[i] != seq[i]:
            return False
    return True        

def inverte(seq): # inverte a sequencia complementar para facilitar a comparacao com a original
    inv = ""
    for i in range(len(seq) - 1, -1, -1):
        inv += seq[i]
    return inv 

def limpa(): # funcao para limpar o terminal
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def principal():
    limpa()
    fita = input("Digite uma fita de DNA: ").upper()
    k = int(input("Qual o tamanho dos palindromos que quer encontrar? "))

    if k < 4:
        print("k tem que ser maior ou igual a 4")
        principal()
        return
    
    fitaR = reversa(fita)
    limitaSequencia(fita, fitaR, 0)
    
    for i in range(0,len(dados),2):
        if len(dados[i]) == k:
            print("Sequencia: " + dados[i] + " | Posicao: " + str(dados[i+1]))

def main():
    global dados
    y = True
    while y:
        principal()
        dados = ["", 0]
        if input("Gostaria de testar outra sequencia? (s/n) ") != "s":
            y = False # mantem o loop ativo ate que o usuario nao queira mais usar

if __name__ == "__main__":
    main()