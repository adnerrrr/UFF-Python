from pplay.window import *
from pplay.keyboard import *
from pplay.sprite import *
from pplay.collision import *
from random import randint

janela = Window(1200,700)
janela.set_title("Bolinha")
mesa = Sprite("mesa.png")

velx = 700
vely = 400
balx = 1200/2 - 50/2
baly = 700/2 - 50/2
ybar = 0
ybarin = 480
inicio = 1 
ponto_player = 0
ponto_pc = 0
fim = 0

bola = Sprite("bola.png")
barra1 = Sprite("barra.png") 
barra2 = Sprite("barra.png")
#barra3 = Sprite("barra.png")

bola.set_position(balx, baly)
barra1.set_position((1200 - 30), (700/2 - 200/2))
barra2.set_position((0), (700/2 - 200/2))
#b3x, b3y = randint(240, 960), randint(0, 500)
tempo = 0

while True:
    mesa.draw()
    janela.draw_text("{} x {}".format(ponto_player, ponto_pc), 573, 20, 30)

    if Window.keyboard.key_pressed("space"):
        inicio = 0
        if fim == 1:
            ponto_pc = 0
            ponto_player = 0
    
    match inicio:
        case 1 if ponto_player == 3:
            janela.draw_text("GAME OVER", 475, 200, 50)
            janela.draw_text("O jogador venceu!", 463, 450, 40)
            fim = 1
            
        case 1 if ponto_pc == 3:
            janela.draw_text("GAME OVER", 475, 200, 50)
            janela.draw_text("A máquina venceu!", 463, 450, 40)
            fim = 1

        case 0:    
            up = Window.keyboard.key_pressed("w")
            down = Window.keyboard.key_pressed("s")
            if down:
                ybar = 600
                if barra2.y >= 500:
                    ybar = 0
            if up:
                ybar = -600
                if barra2.y <= 0:
                    ybar = 0
            if up and down:
                ybar = 0
            barra2.move_y(ybar * janela.delta_time())
            ybar = 0


            if bola.collided(barra1) or bola.collided(barra2):
                
                if velx < 0:
                    bola.x += 1
                    if velx in range(-1500, 1500):
                        velx -= 10
                else:
                    bola.x -= 1
                    if velx in range(-1500, 1500):
                        velx += 10  
                velx *= -1
                        

            if bola.y <= 0 or bola.y + 50 >= janela.height:
                vely *= -1
                if vely > 0:
                    bola.y += 1
                    if velx % 3 == 0:
                        vely += 20
                else:
                    bola.y -= 1
                    if velx % 3 == 0:
                        vely -= 20

            bola.move_x(velx * janela.delta_time())
            bola.move_y(vely * janela.delta_time())
            
            barra1.move_key_y(0.6)

            # if (bola.y + 25) < (barra1.y + 50):
            #     if barra1.y <= 0:
            #         pass
            #     else:
            #         barra1.move_y(-ybarin * janela.delta_time())

            # if (bola.y + 25) > (barra1.y + 50):
            #     if barra1.y >= 500:
            #         pass
            #     else:
            #         barra1.move_y(ybarin * janela.delta_time())
            
            # tempo += janela.delta_time()
            # if tempo >= 5:
            #     barra3.set_position(b3x, b3y)
            #     barra3.draw()
            #     if bola.collided(barra3):
            #         if velx < 0:
            #             bola.x += 1
            #         else:
            #             bola.x -= 1
            #         velx *= -1
            #     if tempo >= 10:
            #         tempo = 0
            #         b3x, b3y = randint(240, 960), randint(0, 500)

            if bola.x < 0:
                bola.set_position(balx, baly)
                barra1.set_position((1200 - 30), (700/2 - 200/2))
                barra2.set_position((0), (700/2 - 200/2))
                velx = 500
                vely = 400
                inicio = 1
                ponto_pc += 1
 
            if bola.x > 1150:
                bola.set_position(balx, baly)
                barra1.set_position((1200 - 30), (700/2 - 200/2))
                barra2.set_position((0), (700/2 - 200/2))
                velx = 500
                vely = 400
                inicio = 1
                ponto_player += 1

    if Window.keyboard.key_pressed("esc"):
        break

    bola.draw()
    barra1.draw()
    barra2.draw()
    janela.update()
