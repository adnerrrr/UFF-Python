from pplay.window import *
from pplay.sprite import *
from pplay.keyboard import *
from pplay.collision import *
from pplay.mouse import *
from pplay.gameimage import *
from random import randint

# VARIÁVEIS
tela = 0
nome = ""
tempo = 0
tempo_reset = 0
timer = 2
timer2 = 0
timer3 = 0
timer4 = 0
alt = 700
larg = 1200
janela = Window(larg, alt)
mouse = janela.get_mouse()
vel = 300
mob_vel = 100
janela.set_title("Space Invaders")
tiros = []
monstros = []
mobtiro = []
n = 5
m = 5
frame = 0
time = 1
fps = 1
pontos = 0
multiply = 6
pos_init_x = 550
pos_init_y = 600
vida = 3
dano = False
desenha = 1
gameState = ""
rank_pontos = []
rank_nomes = []
over = False

# SPRITES
jogar = Sprite("jogar.png")
dificuldade = Sprite("dificuldade.png")
rank = Sprite("rank.png")
sair = Sprite("sair.png")
facil = Sprite("facil.png")
medio = Sprite("medio.png")
dificil = Sprite("dificil.png")
nave = Sprite("nave.png")
fundo = Sprite("fundo.png")
derrota = Sprite("derrota.png")
main_menu = Sprite("main_menu.png")
name_filler = Sprite("filler.png")

# POSIÇÕES
jogar.set_position(300, 90)
dificuldade.set_position(200, 225)
rank.set_position(300, 360)
sair.set_position(300, 495)
facil.set_position(300, 225)
medio.set_position(300, 360)
dificil.set_position(300, 495)
derrota.set_position(200, 90)
nave.set_position(pos_init_x, pos_init_y)
main_menu.set_position(300, 500)
name_filler.set_position(190, 360)
nivel = 1

# MODULOS
def menu():
    jogar.draw()
    dificuldade.draw()
    rank.draw()
    sair.draw()
def dif_menu():
    facil.draw()
    medio.draw()
    dificil.draw()
def movimentacao():
    if (nave.x < 0):
        vel = 0
        nave.x += 1
    elif (nave.x > 1150):
        vel = 0
        nave.x -= 1
    else:
        vel = 300
    if Window.keyboard.key_pressed("A"):
        nave.move_x(-vel * janela.delta_time())
    if Window.keyboard.key_pressed("D"):
        nave.move_x(vel * janela.delta_time())
def atirar():
    tiro = Sprite("tiro.png")
    tiro.set_position(nave.x + 22, 589)
    tiros.append(tiro)
def desenhaTiro():
    for bala in tiros:
        bala.draw()
        bala.move_y(-200 * janela.delta_time())
        if bala.y < 0:    
            tiros.pop(0)
    for bala in mobtiro:
        bala.draw()
        bala.move_y(200 * janela.delta_time())
        if bala.y > 700:
            mobtiro.pop(0)
def mobatirar(x,y):
    tiro = Sprite("tiro.png")
    tiro.set_position(x + 25, y + 50)
    mobtiro.append(tiro)
def colisao():
    global pontos
    cont = -1
    for bala in tiros:
        cont += 1
        for i in range(len(monstros)): #0 ate 3
            for j in range(len(monstros[i]) - 1, -1, -1): #3 ate 0
                if monstros[i][j].collided(bala):
                    tiros.pop(cont)
                    monstros[i].pop(j)
                    pontos += multiply
        if monstros != [] and monstros[i] == []:
            monstros.pop(i)
def gera_monstro(n, m):
    for i in range(n):
        linha = []
        for j in range(m):
            monstro = Sprite("monstro.png")
            monstro.set_position(10 + i*55, 20 + j*55)
            linha.append(monstro)
        monstros.append(linha)
def move_monstro():
    global mob_vel, tela, gameState, multiply
    
    for i in range(len(monstros)):
        for j in range(len(monstros[i])):
            if monstros[i][j]:
                monstros[i][j].x += mob_vel * janela.delta_time()
                monstros[i][j].draw()

    for i in range(len(monstros)):
        if monstros[i] and (monstros[i][0].x > larg - 55 or monstros[i][0].x < 0):
            if multiply > 1:
                multiply -= 1
            mob_vel *= -1
            if mob_vel > 0:
                for i in range(len(monstros)):
                    for j in range(len(monstros[i])):
                        monstros[i][j].x += 1
            else:
                for i in range(len(monstros)):
                    for j in range(len(monstros[i])):
                        monstros[i][j].x -= 1
            for i in range(len(monstros)):
                for j in range(len(monstros[i])):
                    monstros[i][j].y += 60
                    if monstros[i][j].y >= nave.y:
                        gameState = "name"
                        tela = 4
def hit():
    global dano, vida
    for bala in mobtiro:
        if bala.collided(nave):
            vida -= 1
            nave.set_position(pos_init_x, pos_init_y)
            dano = True
def endGame():
    global n, m, mob_vel, gameState, nome, pontos, multiply
    if gameState == "win":
        multiply = 6
        mob_vel = 100
        if n < 20:
            n += 1
        else:
            m += 1
        gera_monstro(n,m)
        gameState = ""
    elif gameState == "defeat":
        with open ("ranking.txt", "a") as arq:
            arq.write(f"{nome} | {pontos}\n")
        gameState = ""
    elif gameState == "rank":
        ranking()
        gameState = ""
    if gameState == "name":
        if input_letra():
            gameState = "defeat"
def changeLevel():
    global mob_vel, vida, pontos, tiros, mobtiro, monstros, n, m, nome, multiply
    mob_vel = 100
    vida = 3
    pontos = 0
    multiply = 6
    tiros = []
    mobtiro = []
    monstros = [] 
    n = 5
    m = 5
    nome = ""
def ranking():
    global rank_pontos, rank_nomes
    rank_pontos = []
    rank_nomes = []
    with open ("ranking.txt", "r") as arq:
        conteudo = arq.readlines()
    for linha in conteudo:
        linha_atual = (linha.strip()).split("| ")
        rank_nomes.append(linha_atual[0])
        rank_pontos.append(int(linha_atual[1]))

    for i in range(len(rank_pontos) - 1):
        for j in range(len(rank_pontos) - i - 1):
            if rank_pontos[j] < rank_pontos[j+1]:
                rank_nomes[j], rank_nomes[j+1] = rank_nomes[j+1], rank_nomes[j]
                rank_pontos[j], rank_pontos[j+1] = rank_pontos[j+1], rank_pontos[j]
def input_letra():
    global timer4, nome
    timer4 += janela.delta_time()
    if timer4 >= 0.15:
        if Window.keyboard.key_pressed("a"):
            nome += "a"
            timer4 = 0
        elif Window.keyboard.key_pressed("b"):
            nome += "b"
            timer4 = 0
        elif Window.keyboard.key_pressed("c"):
            nome += "c"
            timer4 = 0
        elif Window.keyboard.key_pressed("d"):
            nome += "d"
            timer4 = 0
        elif Window.keyboard.key_pressed("e"):
            nome += "e"
            timer4 = 0
        elif Window.keyboard.key_pressed("f"):
            nome += "f"
            timer4 = 0
        elif Window.keyboard.key_pressed("g"):
            nome += "g"
            timer4 = 0
        elif Window.keyboard.key_pressed("h"):
            nome += "h"
            timer4 = 0
        elif Window.keyboard.key_pressed("i"):
            nome += "i"
            timer4 = 0
        elif Window.keyboard.key_pressed("j"):
            nome += "j"
            timer4 = 0
        elif Window.keyboard.key_pressed("k"):
            nome += "k"
            timer4 = 0
        elif Window.keyboard.key_pressed("l"):
            nome += "l"
            timer4 = 0
        elif Window.keyboard.key_pressed("m"):
            nome += "m"
            timer4 = 0
        elif Window.keyboard.key_pressed("n"):
            nome += "n"
            timer4 = 0
        elif Window.keyboard.key_pressed("o"):
            nome += "o"
            timer4 = 0
        elif Window.keyboard.key_pressed("p"):
            nome += "p"
            timer4 = 0
        elif Window.keyboard.key_pressed("q"):
            nome += "q"
            timer4 = 0
        elif Window.keyboard.key_pressed("r"):
            nome += "r"
            timer4 = 0
        elif Window.keyboard.key_pressed("s"):
            nome += "s"
            timer4 = 0
        elif Window.keyboard.key_pressed("t"):
            nome += "t"
            timer4 = 0
        elif Window.keyboard.key_pressed("u"):
            nome += "u"
            timer4 = 0
        elif Window.keyboard.key_pressed("v"):
            nome += "v"
            timer4 = 0
        elif Window.keyboard.key_pressed("w"):
            nome += "w"
            timer4 = 0
        elif Window.keyboard.key_pressed("x"):
            nome += "x"
            timer4 = 0
        elif Window.keyboard.key_pressed("y"):
            nome += "y"
            timer4 = 0
        elif Window.keyboard.key_pressed("z"):
            nome += "z"
            timer4 = 0
        elif Window.keyboard.key_pressed("space"):
            nome += " "
            timer4 = 0
        elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            nome = nome[:len(nome)-1]
            timer4 = 0
        if Window.keyboard.key_pressed("enter"):
            return True
    janela.draw_text(nome, 200, 400 , 40, (255,255,255))

def explosion():
    global dano, vida
    vida -= 1
    nave.set_position(pos_init_x, pos_init_y)
    dano = True
    nave_reset()

def nave_reset():
    global nave
    nave = Sprite("nave.png")
    nave.set_position(pos_init_x, pos_init_y)

def overcharge():
    global nave, over
    pos1 = nave.x
    pos2 = nave.y
    nave = Sprite("nave_red.png")
    nave.set_position(pos1, pos2)


# GAMELOOP
while True:
    fundo.draw()
    endGame()
    frame += 1
    time += janela.delta_time()
    janela.draw_text(f"{fps:.0f}", 20, 10, 20,(255,255,255))
    if time >= 1:
        fps = frame / time
        time = 0
        frame = 0
    match tela:
        case 0: # MENU PRINCIPAL
            menu()
            timer += janela.delta_time()
            if timer >= 2.5:
                if mouse.is_button_pressed(1) and mouse.is_over_object(dificuldade):
                    timer = 2
                    tela = 1
                if mouse.is_button_pressed(1) and mouse.is_over_object(jogar):
                    timer = 2
                    tela = 2
                if mouse.is_button_pressed(1) and mouse.is_over_object(sair):
                    timer = 2
                    break
                if mouse.is_button_pressed(1) and mouse.is_over_object(rank):
                    gameState = "rank"
                    tela = 3
        case 1: # MENU DIFICULDADE
            dif_menu()
            timer += janela.delta_time()
            if timer >= 2.5:
                if mouse.is_button_pressed(1) and mouse.is_over_object(facil):
                    if nivel != 1:
                        changeLevel()
                    nivel = 1
                    gera_monstro(n, m)
                    tela = 2
                if mouse.is_button_pressed(1) and mouse.is_over_object(medio):
                    if nivel != 2:
                        changeLevel()
                    nivel = 2
                    gera_monstro(n, m)
                    tela = 2
                if mouse.is_button_pressed(1) and mouse.is_over_object(dificil):
                    if nivel != 3:
                        changeLevel()
                    nivel = 3
                    gera_monstro(n, m)
                    tela = 2
            if Window.keyboard.key_pressed("esc"):
                tela = 0
        case 2: # JOGO
            if monstros == []:
                gameState = "win"
            if vida == 0:
                gameState = "name"
                tela = 4
                
            if not dano:
                nave.draw()
            if dano:
                timer3 += janela.delta_time()
                if 0.002 < timer3 % 0.5 <= 0.45:
                    nave.draw()
                if timer3 >= 2:
                    timer3 = 0
                    dano = False
                
            movimentacao()
            
            
            timer += janela.delta_time()
            timer2 += janela.delta_time()

            if (monstros != []) and (timer2 >= 0.5):
                linha_vazia = False
                if len(monstros) > 1:
                    l = randint(0, len(monstros) - 1)
                else:
                    l = 0
                if len(monstros[l]) > 1:
                    c = randint(0, len(monstros[l]) - 1)
                else:
                    linha_vazia = True
                if not linha_vazia:
                    mobatirar(monstros[l][c].x, monstros[l][c].y)
                timer2 = 0

            if monstros != []:
                colisao()
            if mobtiro != [] and not dano:
                hit()

            move_monstro()
            desenhaTiro()

            if (Window.keyboard.key_pressed("SPACE")):
                tempo_reset = 0
                tempo += janela.delta_time()
            else:
                tempo = 0
                tempo_reset += janela.delta_time()
            
            if over and tempo_reset >= 2:
                nave_reset()
                over = False

            if tempo >= 5:
                overcharge()
                over = True
            
            if tempo >= 8:
                explosion()
                over = False
                tempo = 0

            if (Window.keyboard.key_pressed("SPACE")) and (timer >= nivel/3):
                atirar()
                timer = 0
            janela.draw_text(f"{pontos}", 50, 50, 50, (255, 255, 255))
            janela.draw_text(f"HP: {vida}", 1050, 50, 50, (255, 255, 255))
            if Window.keyboard.key_pressed("esc"):
                timer = 2
                tela = 0
        case 3: # RANK
            for i in range(len(rank_nomes)):
                if i < 5:
                    janela.draw_text(f"{rank_nomes[i]}" , 400, 150 + 50*i, 50, (255,255,255))
                    janela.draw_text(f"{rank_pontos[i]}", 800, 150 + 50*i, 50, (255,255,255))
            main_menu.draw()
            if mouse.is_button_pressed(1) and mouse.is_over_object(main_menu):
                changeLevel()
                timer = 2
                tela = 0   
        case 4: # DERROTA
            derrota.draw()
            main_menu.draw()
            name_filler.draw()
            if gameState == "" and mouse.is_button_pressed(1) and mouse.is_over_object(main_menu):
                changeLevel()
                timer = 2
                tela = 0
    janela.update()
