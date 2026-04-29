import random
import pygame


def limpar_tela_terminal():
    print("\n" * 3)


def pedir_sim_ou_nao(texto):
    resposta = input(texto).strip().lower()
    while not (resposta == "s" or resposta == "n"):
        resposta = input("Digite apenas s ou n: ").strip().lower()
    return resposta == "s"


def desenhar_texto(pygame, tela, texto, tamanho, cor, x, y, centro=True):
    fonte = pygame.font.SysFont("arial", tamanho)
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    if centro:
        retangulo.center = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(imagem, retangulo)
    return retangulo


def desenhar_botao(pygame, tela, retangulo, texto, cor, cor_texto=(255, 255, 255)):
    pygame.draw.rect(tela, cor, retangulo, border_radius=8)
    pygame.draw.rect(tela, (30, 30, 30), retangulo, 2, border_radius=8)
    desenhar_texto(
        pygame,
        tela,
        texto,
        24,
        cor_texto,
        retangulo.centerx,
        retangulo.centery,
        True,
    )


# -------------------- FORCA - PRINCIPAL --------------------


def escolher_palavra_forca():
    palavras = ["python", "teclado", "monitor", "mouse", "arquivo", "janela"]
    return random.choice(palavras)


def mostrar_forca(palavra, letras_certas, vidas):
    desenho = [
        "  +---+",
        "  |   |",
        "      |",
        "      |",
        "      |",
        "      |",
        "=========",
    ]

    erros = 6 - vidas
    if erros > 0:
        desenho[2] = "  O   |"
    if erros > 1:
        desenho[3] = "  |   |"
    if erros > 2:
        desenho[3] = " /|   |"
    if erros > 3:
        desenho[3] = " /|\\  |"
    if erros > 4:
        desenho[4] = " /    |"
    if erros > 5:
        desenho[4] = " / \\  |"

    for linha in desenho:
        print(linha)

    palavra_mostrada = ""
    for letra in palavra:
        if letra in letras_certas:
            palavra_mostrada = palavra_mostrada + letra + " "
        else:
            palavra_mostrada = palavra_mostrada + "_ "

    print("\nPalavra:", palavra_mostrada)
    print("Vidas:", vidas)


def entrada_forca():
    chute = input("Digite uma letra ou chute a palavra inteira: ").strip().lower()
    while not chute.isalpha():
        chute = input("Digite somente letras: ").strip().lower()
    return chute


def jogar_forca_terminal():
    reiniciar = True
    while reiniciar:
        limpar_tela_terminal()
        palavra = escolher_palavra_forca()
        letras_certas = []
        letras_erradas = []
        vidas = 6
        venceu = False

        while vidas > 0 and not venceu:
            mostrar_forca(palavra, letras_certas, vidas)
            print("Letras erradas:", letras_erradas)
            chute = entrada_forca()

            if len(chute) > 1:
                if chute == palavra:
                    venceu = True
                else:
                    vidas = 0
            elif chute in letras_certas or chute in letras_erradas:
                print("Voce ja tentou essa letra.")
            elif chute in palavra:
                letras_certas.append(chute)
            else:
                letras_erradas.append(chute)
                vidas = vidas - 1

            venceu = True
            for letra in palavra:
                if letra not in letras_certas:
                    venceu = False

            if len(chute) > 1 and chute == palavra:
                venceu = True

        mostrar_forca(palavra, letras_certas, vidas)
        if venceu:
            print("Voce venceu! A palavra era:", palavra)
        else:
            print("Voce perdeu! A palavra era:", palavra)

        reiniciar = pedir_sim_ou_nao("Jogar forca de novo? (s/n): ")


# -------------------- FORCA - PYGAME --------------------


def desenhar_boneco_forca(pygame, tela, erros):
    preto = (20, 20, 20)
    pygame.draw.line(tela, preto, (80, 420), (260, 420), 5)
    pygame.draw.line(tela, preto, (130, 420), (130, 100), 5)
    pygame.draw.line(tela, preto, (130, 100), (300, 100), 5)
    pygame.draw.line(tela, preto, (300, 100), (300, 145), 5)

    if erros > 0:
        pygame.draw.circle(tela, preto, (300, 175), 30, 4)
    if erros > 1:
        pygame.draw.line(tela, preto, (300, 205), (300, 300), 4)
    if erros > 2:
        pygame.draw.line(tela, preto, (300, 230), (255, 270), 4)
    if erros > 3:
        pygame.draw.line(tela, preto, (300, 230), (345, 270), 4)
    if erros > 4:
        pygame.draw.line(tela, preto, (300, 300), (260, 365), 4)
    if erros > 5:
        pygame.draw.line(tela, preto, (300, 300), (340, 365), 4)


def jogar_forca_pygame():
    pygame.init()
    tela = pygame.display.set_mode((800, 520))
    pygame.display.set_caption("Forca")
    relogio = pygame.time.Clock()

    palavra = escolher_palavra_forca()
    letras_certas = []
    letras_erradas = []
    entrada = ""
    mensagem = "Digite letras pelo teclado. Enter chuta palavra."
    fim = False
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_r:
                    palavra = escolher_palavra_forca()
                    letras_certas = []
                    letras_erradas = []
                    entrada = ""
                    mensagem = "Novo jogo!"
                    fim = False
                elif not fim:
                    if evento.key == pygame.K_BACKSPACE:
                        entrada = entrada[:-1]
                    elif evento.key == pygame.K_RETURN:
                        if entrada.isalpha():
                            if len(entrada) == 1:
                                if entrada in palavra and entrada not in letras_certas:
                                    letras_certas.append(entrada)
                                elif entrada not in letras_erradas:
                                    letras_erradas.append(entrada)
                            else:
                                if entrada == palavra:
                                    for letra in palavra:
                                        if letra not in letras_certas:
                                            letras_certas.append(letra)
                                else:
                                    while len(letras_erradas) < 6:
                                        letras_erradas.append("?")
                            entrada = ""
                        else:
                            mensagem = "Digite somente letras."
                    elif evento.unicode.isalpha():
                        entrada = entrada + evento.unicode.lower()

        venceu = True
        for letra in palavra:
            if letra not in letras_certas:
                venceu = False

        if venceu:
            fim = True
            mensagem = "Voce venceu! Aperte R para reiniciar."
        elif len(letras_erradas) > 5:
            fim = True
            mensagem = "Voce perdeu! Palavra: " + palavra + ". Aperte R."

        tela.fill((242, 245, 248))
        desenhar_texto(pygame, tela, "Jogo da Forca", 38, (20, 20, 20), 400, 40)
        desenhar_boneco_forca(pygame, tela, len(letras_erradas))

        palavra_mostrada = ""
        for letra in palavra:
            if letra in letras_certas:
                palavra_mostrada = palavra_mostrada + letra.upper() + " "
            else:
                palavra_mostrada = palavra_mostrada + "_ "

        desenhar_texto(pygame, tela, palavra_mostrada, 46, (30, 60, 120), 560, 170)
        desenhar_texto(pygame, tela, "Entrada: " + entrada, 28, (20, 20, 20), 560, 250)
        desenhar_texto(
            pygame,
            tela,
            "Erradas: " + " ".join(letras_erradas),
            24,
            (160, 40, 40),
            560,
            310,
        )
        desenhar_texto(pygame, tela, mensagem, 24, (20, 20, 20), 400, 470)
        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()


# -------------------- PEDRA, PAPEL E TESOURA --------------------


def resultado_ppt(jogador, computador):
    if jogador == computador:
        return "empate"
    if jogador == "pedra" and computador == "tesoura":
        return "vitoria"
    if jogador == "tesoura" and computador == "papel":
        return "vitoria"
    if jogador == "papel" and computador == "pedra":
        return "vitoria"
    return "derrota"


def jogar_ppt_terminal():
    opcoes = ["pedra", "papel", "tesoura"]
    pontos = 0
    reiniciar = True

    while reiniciar:
        print("\nPedra, Papel e Tesoura")
        jogador = input("Escolha pedra, papel ou tesoura: ").strip().lower()
        while jogador not in opcoes:
            jogador = input("Escolha apenas pedra, papel ou tesoura: ").strip().lower()

        computador = random.choice(opcoes)
        resultado = resultado_ppt(jogador, computador)

        print("Voce:", jogador)
        print("Computador:", computador)

        if resultado == "vitoria":
            pontos = pontos + 1
            print("Voce venceu!")
        elif resultado == "derrota":
            print("Voce perdeu!")
        else:
            print("Empate!")

        print("Pontuacao:", pontos)
        reiniciar = pedir_sim_ou_nao("Jogar de novo? (s/n): ")


def criar_imagem_ppt(pygame, tipo):
    imagem = pygame.Surface((150, 150), pygame.SRCALPHA)
    preto = (30, 30, 30)
    azul = (80, 140, 220)
    verde = (70, 170, 100)
    vermelho = (210, 80, 80)

    if tipo == "pedra":
        pygame.draw.circle(imagem, azul, (75, 75), 52)
        pygame.draw.circle(imagem, preto, (75, 75), 52, 3)
    elif tipo == "papel":
        pygame.draw.rect(imagem, verde, (38, 25, 74, 100), border_radius=4)
        pygame.draw.rect(imagem, preto, (38, 25, 74, 100), 3, border_radius=4)
        pygame.draw.line(imagem, preto, (52, 55), (98, 55), 2)
        pygame.draw.line(imagem, preto, (52, 78), (98, 78), 2)
        pygame.draw.line(imagem, preto, (52, 101), (88, 101), 2)
    else:
        pygame.draw.line(imagem, vermelho, (45, 115), (105, 35), 12)
        pygame.draw.line(imagem, vermelho, (105, 115), (45, 35), 12)
        pygame.draw.line(imagem, preto, (45, 115), (105, 35), 4)
        pygame.draw.line(imagem, preto, (105, 115), (45, 35), 4)

    return imagem


def jogar_ppt_pygame():
    pygame.init()
    tela = pygame.display.set_mode((820, 520))
    pygame.display.set_caption("Pedra, Papel e Tesoura")
    relogio = pygame.time.Clock()
    opcoes = ["pedra", "papel", "tesoura"]
    imagens = {}
    for opcao in opcoes:
        imagens[opcao] = criar_imagem_ppt(pygame, opcao)

    botoes = {
        "pedra": pygame.Rect(80, 310, 180, 70),
        "papel": pygame.Rect(320, 310, 180, 70),
        "tesoura": pygame.Rect(560, 310, 180, 70),
    }
    jogador = ""
    computador = ""
    mensagem = "Escolha uma opcao."
    pontos = 0
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for opcao in opcoes:
                    if botoes[opcao].collidepoint(evento.pos):
                        jogador = opcao
                        computador = random.choice(opcoes)
                        resultado = resultado_ppt(jogador, computador)
                        if resultado == "vitoria":
                            pontos = pontos + 1
                            mensagem = "Voce venceu!"
                        elif resultado == "derrota":
                            mensagem = "Voce perdeu!"
                        else:
                            mensagem = "Empate!"

        tela.fill((245, 245, 242))
        desenhar_texto(pygame, tela, "Pedra, Papel e Tesoura", 36, (20, 20, 20), 410, 38)
        desenhar_texto(pygame, tela, "Pontos: " + str(pontos), 26, (20, 20, 20), 410, 85)
        desenhar_texto(pygame, tela, "Voce", 28, (20, 20, 20), 205, 140)
        desenhar_texto(pygame, tela, "Computador", 28, (20, 20, 20), 615, 140)

        if not jogador == "":
            tela.blit(imagens[jogador], (130, 165))
        if not computador == "":
            tela.blit(imagens[computador], (540, 165))

        for opcao in opcoes:
            desenhar_botao(pygame, tela, botoes[opcao], opcao.upper(), (50, 90, 150))

        desenhar_texto(pygame, tela, mensagem, 30, (20, 20, 20), 410, 450)
        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()


# -------------------- CALCULADORA --------------------


def calcular(a, operador, b):
    if operador == "+":
        return a + b
    if operador == "-":
        return a - b
    if operador == "*":
        return a * b
    if operador == "/":
        if b == 0:
            return None
        return a / b
    return None


def jogar_calculadora_terminal():
    memoria = None
    continuar = True

    while continuar:
        print("\nCalculadora")
        if memoria is None:
            primeiro = input("Digite o primeiro numero: ").strip()
            while not primeiro.replace(".", "", 1).isdigit():
                primeiro = input("Digite um numero valido: ").strip()
            numero1 = float(primeiro)
        else:
            print("Memoria:", memoria)
            usar = pedir_sim_ou_nao("Usar a memoria como primeiro numero? (s/n): ")
            if usar:
                numero1 = memoria
            else:
                primeiro = input("Digite o primeiro numero: ").strip()
                while not primeiro.replace(".", "", 1).isdigit():
                    primeiro = input("Digite um numero valido: ").strip()
                numero1 = float(primeiro)

        operador = input("Digite a operacao (+, -, *, /): ").strip()
        while operador not in ["+", "-", "*", "/"]:
            operador = input("Digite somente +, -, * ou /: ").strip()

        segundo = input("Digite o segundo numero: ").strip()
        while not segundo.replace(".", "", 1).isdigit():
            segundo = input("Digite um numero valido: ").strip()
        numero2 = float(segundo)

        resultado = calcular(numero1, operador, numero2)
        if resultado is None:
            print("Nao da para dividir por zero.")
        else:
            memoria = resultado
            print("Resultado:", resultado)

        continuar = pedir_sim_ou_nao("Fazer outra conta? (s/n): ")


def formatar_numero(numero):
    if numero is None:
        return "0"
    if int(numero) == numero:
        return str(int(numero))
    return str(round(numero, 4))


def jogar_calculadora_pygame():
    pygame.init()
    tela = pygame.display.set_mode((360, 560))
    pygame.display.set_caption("Calculadora")
    relogio = pygame.time.Clock()

    botoes_texto = [
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "C", "0", "=", "+",
    ]
    botoes = []
    for i in range(len(botoes_texto)):
        x = 25 + (i % 4) * 80
        y = 160 + (i // 4) * 80
        botoes.append(pygame.Rect(x, y, 65, 65))

    tela_numero = "0"
    memoria = None
    numero1 = None
    operador = None
    digitando_segundo = False
    mensagem = "Memoria: vazia"
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(botoes)):
                    if botoes[i].collidepoint(evento.pos):
                        valor = botoes_texto[i]

                        if valor.isdigit():
                            if tela_numero == "0" or digitando_segundo:
                                tela_numero = valor
                                digitando_segundo = False
                            else:
                                tela_numero = tela_numero + valor
                        elif valor == "C":
                            tela_numero = "0"
                            numero1 = None
                            operador = None
                            digitando_segundo = False
                            mensagem = "Memoria: " + formatar_numero(memoria)
                        elif valor in ["+", "-", "*", "/"]:
                            numero1 = float(tela_numero)
                            operador = valor
                            digitando_segundo = True
                            mensagem = formatar_numero(numero1) + " " + operador
                        elif valor == "=" and operador is not None:
                            numero2 = float(tela_numero)
                            resultado = calcular(numero1, operador, numero2)
                            if resultado is None:
                                tela_numero = "0"
                                mensagem = "Erro: divisao por zero"
                            else:
                                memoria = resultado
                                tela_numero = formatar_numero(resultado)
                                mensagem = "Memoria: " + formatar_numero(memoria)
                            operador = None
                            digitando_segundo = True

        tela.fill((235, 238, 240))
        pygame.draw.rect(tela, (25, 30, 36), (25, 35, 310, 95), border_radius=8)
        desenhar_texto(pygame, tela, tela_numero[-12:], 42, (255, 255, 255), 45, 65, False)
        desenhar_texto(pygame, tela, mensagem, 18, (70, 70, 70), 30, 135, False)

        for i in range(len(botoes)):
            valor = botoes_texto[i]
            cor = (70, 90, 120)
            if valor in ["+", "-", "*", "/", "="]:
                cor = (210, 110, 60)
            if valor == "C":
                cor = (170, 60, 60)
            desenhar_botao(pygame, tela, botoes[i], valor, cor)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()


# -------------------- ADIVINHACAO --------------------


def pedir_numero_inteiro(texto, minimo, maximo):
    valor = input(texto).strip()
    while not valor.isdigit() or int(valor) < minimo or int(valor) > maximo:
        valor = input("Digite um numero entre " + str(minimo) + " e " + str(maximo) + ": ").strip()
    return int(valor)


def usuario_adivinha_terminal():
    numero = random.randint(1, 1023)
    tentativas = 0
    acertou = False

    while not acertou:
        chute = pedir_numero_inteiro("Digite seu chute: ", 1, 1023)
        tentativas = tentativas + 1
        if numero < chute:
            print("-1")
        elif numero > chute:
            print("1")
        else:
            print("0")
            print("Voce acertou em", tentativas, "tentativas.")
            acertou = True


def computador_adivinha_terminal():
    print("Pense em um numero entre 1 e 1023.")
    minimo = 1
    maximo = 1023
    tentativas = 0
    acertou = False

    while not acertou and minimo <= maximo:
        chute = (minimo + maximo) // 2
        tentativas = tentativas + 1
        print("Computador chutou:", chute)
        dica = input("Digite -1 se seu numero e menor, 1 se e maior, 0 se acertou: ").strip()
        while dica not in ["-1", "0", "1"]:
            dica = input("Digite apenas -1, 0 ou 1: ").strip()

        if dica == "-1":
            maximo = chute - 1
        elif dica == "1":
            minimo = chute + 1
        else:
            print("Computador acertou em", tentativas, "tentativas.")
            acertou = True


def jogar_adivinhacao_terminal():
    reiniciar = True
    while reiniciar:
        print("\nJogo de Adivinhacao")
        modo = input("Quem vai adivinhar? usuario ou computador: ").strip().lower()
        while not (modo == "usuario" or modo == "computador"):
            modo = input("Digite usuario ou computador: ").strip().lower()

        if modo == "usuario":
            usuario_adivinha_terminal()
        else:
            computador_adivinha_terminal()

        reiniciar = pedir_sim_ou_nao("Jogar de novo? (s/n): ")


def jogar_adivinhacao_pygame():
    pygame.init()
    tela = pygame.display.set_mode((760, 520))
    pygame.display.set_caption("Adivinhacao")
    relogio = pygame.time.Clock()

    botao_usuario = pygame.Rect(130, 210, 210, 70)
    botao_computador = pygame.Rect(420, 210, 210, 70)
    botao_menor = pygame.Rect(90, 360, 170, 60)
    botao_acertou = pygame.Rect(295, 360, 170, 60)
    botao_maior = pygame.Rect(500, 360, 170, 60)
    botao_reiniciar = pygame.Rect(285, 440, 190, 50)

    modo = "menu"
    numero = random.randint(1, 1023)
    entrada = ""
    tentativas = 0
    mensagem = "Escolha quem vai adivinhar."
    minimo = 1
    maximo = 1023
    chute_computador = 512
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif modo == "usuario":
                    if evento.key == pygame.K_BACKSPACE:
                        entrada = entrada[:-1]
                    elif evento.key == pygame.K_RETURN and entrada.isdigit():
                        chute = int(entrada)
                        if chute > 0 and chute <= 1023:
                            tentativas = tentativas + 1
                            if numero < chute:
                                mensagem = "-1"
                            elif numero > chute:
                                mensagem = "1"
                            else:
                                mensagem = "0 - acertou em " + str(tentativas) + " tentativas"
                                modo = "fim"
                        entrada = ""
                    elif evento.unicode.isdigit():
                        entrada = entrada + evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if modo == "menu":
                    if botao_usuario.collidepoint(evento.pos):
                        modo = "usuario"
                        numero = random.randint(1, 1023)
                        entrada = ""
                        tentativas = 0
                        mensagem = "Digite o chute e aperte Enter."
                    elif botao_computador.collidepoint(evento.pos):
                        modo = "computador"
                        minimo = 1
                        maximo = 1023
                        tentativas = 1
                        chute_computador = (minimo + maximo) // 2
                        mensagem = "Use os botoes para responder."
                elif modo == "computador":
                    if botao_menor.collidepoint(evento.pos):
                        maximo = chute_computador - 1
                    elif botao_maior.collidepoint(evento.pos):
                        minimo = chute_computador + 1
                    elif botao_acertou.collidepoint(evento.pos):
                        mensagem = "0 - computador acertou em " + str(tentativas) + " tentativas"
                        modo = "fim"

                    if modo == "computador":
                        if minimo <= maximo:
                            chute_computador = (minimo + maximo) // 2
                            tentativas = tentativas + 1
                        else:
                            mensagem = "Respostas impossiveis. Reinicie."
                            modo = "fim"
                elif modo == "fim":
                    if botao_reiniciar.collidepoint(evento.pos):
                        modo = "menu"
                        mensagem = "Escolha quem vai adivinhar."

        tela.fill((244, 246, 250))
        desenhar_texto(pygame, tela, "Jogo de Adivinhacao", 38, (20, 20, 20), 380, 45)

        if modo == "menu":
            desenhar_botao(pygame, tela, botao_usuario, "Usuario", (55, 110, 170))
            desenhar_botao(pygame, tela, botao_computador, "Computador", (55, 110, 170))
        elif modo == "usuario":
            desenhar_texto(pygame, tela, "Numero entre 1 e 1023", 28, (20, 20, 20), 380, 130)
            desenhar_texto(pygame, tela, "Chute: " + entrada, 36, (20, 20, 20), 380, 230)
            desenhar_texto(pygame, tela, "Tentativas: " + str(tentativas), 24, (20, 20, 20), 380, 305)
        elif modo == "computador":
            desenhar_texto(pygame, tela, "Computador chutou:", 28, (20, 20, 20), 380, 135)
            desenhar_texto(pygame, tela, str(chute_computador), 60, (30, 80, 150), 380, 220)
            desenhar_botao(pygame, tela, botao_menor, "-1 menor", (170, 70, 70))
            desenhar_botao(pygame, tela, botao_acertou, "0 acertou", (70, 150, 90))
            desenhar_botao(pygame, tela, botao_maior, "1 maior", (70, 90, 170))
        elif modo == "fim":
            desenhar_botao(pygame, tela, botao_reiniciar, "Reiniciar", (70, 120, 170))

        desenhar_texto(pygame, tela, mensagem, 26, (20, 20, 20), 380, 475)
        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()


# -------------------- MENUS --------------------


def menu_terminal():
    rodando = True
    while rodando:
        print("\n===== Gincana de Jogos =====")
        print("1 - Forca no terminal")
        print("2 - Forca no PyGame")
        print("3 - Pedra, Papel e Tesoura no terminal")
        print("4 - Pedra, Papel e Tesoura no PyGame")
        print("5 - Calculadora no terminal")
        print("6 - Calculadora no PyGame")
        print("7 - Adivinhacao no terminal")
        print("8 - Adivinhacao no PyGame")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            jogar_forca_terminal()
        elif opcao == "2":
            jogar_forca_pygame()
        elif opcao == "3":
            jogar_ppt_terminal()
        elif opcao == "4":
            jogar_ppt_pygame()
        elif opcao == "5":
            jogar_calculadora_terminal()
        elif opcao == "6":
            jogar_calculadora_pygame()
        elif opcao == "7":
            jogar_adivinhacao_terminal()
        elif opcao == "8":
            jogar_adivinhacao_pygame()
        elif opcao == "0":
            rodando = False
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu_terminal()
