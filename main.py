from pygame import *
import random
import sys


init()
mixer.init()


fonte_padrao = font.SysFont("Arial", 40)
fonte_pequena = font.SysFont("Arial", 25)


# JOGO DA FORCA

def forca_pygame():
    tela = display.set_mode((800, 600))
    display.set_caption("Forca - PyGame")
    clock = time.Clock()
    
    temas_frutas = ["MACA", "BANANA", "LARANJA", "MELANCIA", "UVA"]
    palavra = random.choice(temas_frutas)
    letras_certas = []
    vidas = 6
    estado = "JOGANDO"
    modo_palavra = False
    chute_total = ""
    
    running = True
    while running:
        clock.tick(30)
        tela.fill((255, 255, 255))
        
        for ev in event.get():
            if ev.type == QUIT:
                running = False
            
            if ev.type == KEYDOWN and estado == "JOGANDO":
                if ev.key == K_RETURN:
                    if modo_palavra:
                        if chute_total == palavra:
                            for letra in palavra:
                                if letra not in letras_certas:
                                    letras_certas.append(letra)
                        else:
                            vidas -= 1
                        chute_total = ""
                        modo_palavra = False
                    else:
                        modo_palavra = True
                
                elif modo_palavra:
                    if ev.key == K_BACKSPACE:
                        chute_total = chute_total[:-1]
                    elif ev.key >= K_a and ev.key <= K_z:
                        chute_total += chr(ev.key).upper()

                elif ev.key >= K_a and ev.key <= K_z:
                    letra = chr(ev.key).upper()
                    if letra in palavra:
                        if letra not in letras_certas:
                            letras_certas.append(letra)
                    else:
                        vidas -= 1
            
            if ev.type == KEYDOWN and estado != "JOGANDO":
                if ev.key == K_SPACE: 
                    palavra = random.choice(temas_frutas)
                    letras_certas = []
                    vidas = 6
                    estado = "JOGANDO"
                    modo_palavra = False
                    chute_total = ""
                elif ev.key == K_ESCAPE: 
                    running = False
                    
        draw.line(tela, (0,0,0), (100, 500), (300, 500), 5)
        draw.line(tela, (0,0,0), (200, 500), (200, 100), 5)
        draw.line(tela, (0,0,0), (200, 100), (400, 100), 5)
        draw.line(tela, (0,0,0), (400, 100), (400, 150), 5)
        
        if vidas <= 5: draw.circle(tela, (0,0,0), (400, 180), 30, 5) 
        if vidas <= 4: draw.line(tela, (0,0,0), (400, 210), (400, 350), 5) 
        if vidas <= 3: draw.line(tela, (0,0,0), (400, 230), (350, 300), 5) 
        if vidas <= 2: draw.line(tela, (0,0,0), (400, 230), (450, 300), 5) 
        if vidas <= 1: draw.line(tela, (0,0,0), (400, 350), (350, 450), 5) 
        if vidas <= 0: 
            draw.line(tela, (0,0,0), (400, 350), (450, 450), 5) 
            estado = "PERDEU"
            
        texto_palavra = ""
        vitoria = True
        for letra in palavra:
            if letra in letras_certas:
                texto_palavra += letra + " "
            else:
                texto_palavra += "_ "
                vitoria = False
                
        if vitoria and estado == "JOGANDO":
            estado = "VENCEU"
            
        img_texto = fonte_padrao.render(texto_palavra, True, (0,0,0))
        tela.blit(img_texto, (400, 500))

        if modo_palavra:
            display_chute = fonte_pequena.render("CHUTE A PALAVRA: " + chute_total, True, (0, 0, 255))
            tela.blit(display_chute, (400, 450))
        
        if estado == "VENCEU":
            msg = fonte_padrao.render("VENCEU! Espaço para reiniciar ou ESC para sair.", True, (0, 255, 0))
            tela.blit(msg, (100, 50))
        elif estado == "PERDEU":
            msg = fonte_padrao.render(f"PERDEU! A palavra era {palavra}. Espaço/ESC", True, (255, 0, 0))
            tela.blit(msg, (50, 50))
            
        display.update()
    display.quit()


# PEDRA, PAPEL E TESOURA

def ppt_texto():
    opcoes = ["PEDRA", "PAPEL", "TESOURA"]
    pontos_jogador = 0
    
    while True:
        print("\n=== PEDRA, PAPEL E TESOURA ===")
        print(f"Sua pontuação: {pontos_jogador}")
        print("1 - Pedra | 2 - Papel | 3 - Tesoura | 0 - Sair")
        
        escolha = input("Sua escolha: ")
        if escolha == '0': break
        if escolha not in ['1', '2', '3']:
            print("Inválido!")
            continue
            
        jogador = opcoes[int(escolha) - 1]
        pc = random.choice(opcoes)
        
        print(f"\nVocê jogou: {jogador}")
        print(f"Computador jogou: {pc}")
        
        if jogador == pc:
            print("EMPATE!")
        elif (jogador == "PEDRA" and pc == "TESOURA") or \
             (jogador == "TESOURA" and pc == "PAPEL") or \
             (jogador == "PAPEL" and pc == "PEDRA"):
            print("VOCÊ VENCEU A RODADA!")
            pontos_jogador += 1
        else:
            print("COMPUTADOR VENCEU A RODADA!")

def ppt_pygame():
    tela = display.set_mode((800, 600))
    display.set_caption("Jokenpo - PyGame")
    
    
    pontos = 0
    escolha_jogador = ""
    escolha_pc = ""
    resultado = "Escolha sua jogada!"
    
    opcoes = ["PEDRA", "PAPEL", "TESOURA"]
    
    running = True
    while running:
        tela.fill((200, 200, 200))
        
        for ev in event.get():
            if ev.type == QUIT:
                running = False
                
            if ev.type == MOUSEBUTTONDOWN:
                mx, my = ev.pos
                
                if 400 < my < 550:
                    if 100 < mx < 250: escolha_jogador = "PEDRA"
                    elif 325 < mx < 475: escolha_jogador = "PAPEL"
                    elif 550 < mx < 700: escolha_jogador = "TESOURA"
                    
                    if escolha_jogador != "":
                        escolha_pc = random.choice(opcoes)
                        if escolha_jogador == escolha_pc:
                            resultado = "EMPATE!"
                        elif (escolha_jogador == "PEDRA" and escolha_pc == "TESOURA") or \
                             (escolha_jogador == "TESOURA" and escolha_pc == "PAPEL") or \
                             (escolha_jogador == "PAPEL" and escolha_pc == "PEDRA"):
                            resultado = "VOCÊ VENCEU!"
                            pontos += 1
                        else:
                            resultado = "VOCÊ PERDEU!"

       
        draw.rect(tela, (100,100,100), (100, 400, 150, 150)) 
        tela.blit(fonte_padrao.render("PEDRA", True, (255,255,255)), (120, 460))
        
        draw.rect(tela, (200,200,200), (325, 400, 150, 150), 5) 
        tela.blit(fonte_padrao.render("PAPEL", True, (0,0,0)), (350, 460))
        
        draw.rect(tela, (255,100,100), (550, 400, 150, 150)) 
        tela.blit(fonte_pequena.render("TESOURA", True, (0,0,0)), (580, 460))
        
        
        tela.blit(fonte_padrao.render(f"Pontos: {pontos}", True, (0,0,0)), (50, 50))
        tela.blit(fonte_padrao.render(f"PC Jogou: {escolha_pc}", True, (255,0,0)), (400, 150))
        tela.blit(fonte_padrao.render(f"Você Jogou: {escolha_jogador}", True, (0,0,255)), (100, 150))
        tela.blit(fonte_padrao.render(resultado, True, (0,0,0)), (250, 250))
        
        display.update()
    display.quit()


# CALCULADORA

def calc_texto():
    print("\n=== CALCULADORA VAGABUNDA ===")
    memoria = None
    
    while True:
        if memoria is None:
            num1 = input("Digite o 1º número (ou 'S' para sair): ")
            if num1.upper() == 'S': break
            num1 = float(num1)
        else:
            num1 = memoria
            print(f"Memória atual: {num1}")
            
        op = input("Operação (+, -, *, /, C para limpar): ")
        if op.upper() == 'C':
            memoria = None
            continue
            
        num2 = input("Digite o 2º número: ")
        num2 = float(num2)
        
        if op == '+': memoria = num1 + num2
        elif op == '-': memoria = num1 - num2
        elif op == '*': memoria = num1 * num2
        elif op == '/': 
            if num2 != 0: memoria = num1 / num2
            else: print("Erro: Divisão por zero"); memoria = None
        else:
            print("Operação inválida!")
            
        if memoria is not None:
            print(f"RESULTADO: {memoria}")

def calc_pygame():
    tela = display.set_mode((400, 600))
    display.set_caption("Calculadora de Celular")
    
    
    botoes = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['C', '0', '=', '+']
    ]
    
    memoria = ""
    operacao = ""
    numero_atual = ""
    visor = "0"
    
    running = True
    while running:
        tela.fill((30, 30, 30))
        
        for ev in event.get():
            if ev.type == QUIT:
                running = False
            
            if ev.type == MOUSEBUTTONDOWN:
                mx, my = ev.pos
                
                
                if my > 150:
                    coluna = mx // 100
                    linha = (my - 150) // 112 
                    
                    if coluna < 4 and linha < 4:
                        tecla = botoes[linha][coluna]
                        
                        if tecla in "0123456789":
                            numero_atual += tecla
                            visor = numero_atual
                        elif tecla in "+-*/":
                            if numero_atual != "":
                                memoria = numero_atual
                            numero_atual = ""
                            operacao = tecla
                        elif tecla == "=":
                            if memoria != "" and numero_atual != "":
                                n1 = float(memoria)
                                n2 = float(numero_atual)
                                if operacao == '+': res = n1 + n2
                                elif operacao == '-': res = n1 - n2
                                elif operacao == '*': res = n1 * n2
                                elif operacao == '/': res = n1 / n2 if n2 != 0 else 0
                                
                                visor = str(res)
                                memoria = str(res) 
                                numero_atual = ""
                        elif tecla == "C":
                            visor = "0"
                            numero_atual = ""
                            memoria = ""
                            operacao = ""

        
        draw.rect(tela, (200, 200, 200), (10, 10, 380, 130))
        tela.blit(fonte_padrao.render(visor, True, (0,0,0)), (20, 50))
        
        
        y_atual = 150
        for linha in botoes:
            x_atual = 0
            for tecla in linha:
                draw.rect(tela, (80, 80, 80), (x_atual+5, y_atual+5, 90, 100))
                tela.blit(fonte_padrao.render(tecla, True, (255,255,255)), (x_atual + 35, y_atual + 35))
                x_atual += 100
            y_atual += 112
            
        display.update()
    display.quit()


#  JOGO DE ADIVINHAÇÃO

def adiv_texto():
    print("\n=== JOGO DE ADIVINHAÇÃO ===")
    print("1 - Eu (usuário) vou adivinhar")
    print("2 - Computador vai adivinhar")
    modo = input("Escolha o modo: ")
    
    if modo == '1':
        secreto = random.randint(1, 1023)
        tentativas = 0
        while True:
            chute = int(input("Chute um número (1 a 1023): "))
            tentativas += 1
            if chute < secreto: print("-1 (O número é MAIOR)")
            elif chute > secreto: print("1 (O número é MENOR)")
            else:
                print(f"0 (ACERTOU! Em {tentativas} tentativas)")
                break
    elif modo == '2':
        print("Pense em um número de 1 a 1023.")
        minimo = 1
        maximo = 1023
        tentativas = 0
        
        while True:
            chute = (minimo + maximo) // 2
            tentativas += 1
            print(f"\nO computador chutou: {chute}")
            resp = input("Digite -1 (seu num é maior), 1 (seu num é menor) ou 0 (acertou): ")
            
            if resp == '0':
                print(f"O PC acertou em {tentativas} tentativas!")
                break
            elif resp == '-1':
                minimo = chute + 1
            elif resp == '1':
                maximo = chute - 1

def adiv_pygame():
    tela = display.set_mode((800, 600))
    display.set_caption("Adivinhação - PyGame")
    
    
    minimo = 1
    maximo = 1023
    chute = (minimo + maximo) // 2
    tentativas = 0
    estado = "JOGANDO"
    
    running = True
    while running:
        tela.fill((200, 240, 255))
        
        for ev in event.get():
            if ev.type == QUIT:
                running = False
                
            if ev.type == MOUSEBUTTONDOWN and estado == "JOGANDO":
                mx, my = ev.pos
                if 400 < my < 500:
                    if 100 < mx < 250: 
                        minimo = chute + 1
                        tentativas += 1
                        chute = (minimo + maximo) // 2
                    elif 325 < mx < 475: 
                        tentativas += 1
                        estado = "FIM"
                    elif 550 < mx < 700: 
                        maximo = chute - 1
                        tentativas += 1
                        chute = (minimo + maximo) // 2
                        
        tela.blit(fonte_padrao.render("Pense em um número de 1 a 1023", True, (0,0,0)), (150, 50))
        tela.blit(fonte_padrao.render(f"O PC CHUTA: {chute}", True, (255,0,0)), (250, 200))
        
        if estado == "JOGANDO":
           
            tela.blit(fonte_pequena.render("-1 (É Maior)", True, (255,255,255)), (110, 440))
            
          
            draw.rect(tela, (100,255,100), (325, 400, 150, 100))
            tela.blit(fonte_padrao.render("0 (Acertou)", True, (0,0,0)), (330, 435))
            
            
            draw.rect(tela, (255,100,100), (550, 400, 150, 100))
            tela.blit(fonte_pequena.render("1 (É Menor)", True, (255,255,255)), (560, 440))
        else:
            tela.blit(fonte_padrao.render(f"PC VENCEU em {tentativas} tentativas!", True, (0,150,0)), (200, 350))
            tela.blit(fonte_pequena.render("Feche a janela para voltar", True, (0,0,0)), (280, 450))

        display.update()
    display.quit()



# MENU PRINCIPAL 

while True:
    
    print("MENU DA ATIVIDADE 7")
    print("1 - Jogo da Forca (Texto)")
    print("2 - Jogo da Forca (PyGame)")
    print("3 - Pedra, Papel, Tesoura (Texto)")
    print("4 - Pedra, Papel, Tesoura (PyGame)")
    print("5 - Calculadora (Texto)")
    print("6 - Calculadora (PyGame)")
    print("7 - Adivinhação (Texto)")
    print("8 - Adivinhação (PyGame)")
    print("0 - SAIR")
    
    escolha = input("Escolha uma opção: ")
    
    if escolha == '1': forca_texto()
    elif escolha == '2': forca_pygame()
    elif escolha == '3': ppt_texto()
    elif escolha == '4': ppt_pygame()
    elif escolha == '5': calc_texto()
    elif escolha == '6': calc_pygame()
    elif escolha == '7': adiv_texto()
    elif escolha == '8': adiv_pygame()
    elif escolha == '0':
        break
    else:
        print("Opção inválida!")

quit()