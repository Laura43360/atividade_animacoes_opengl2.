# Laboratório: Animações 2D e 3D com Python/OpenGL
# Instalação: python -m pip install pygame PyOpenGL

import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

# Configurações da animação
FPS = 60
VELOCIDADE = 1.0
AMPLITUDE = 2.5
PERIODO = 6.0
GIRO = 60.0

# Quadros-chave do exemplo original
QUADROS_CHAVE = [
    (0.0, -2.5, 0.0, 1.0),
    (2.0, 0.0, 90.0, 1.5),
    (4.0, 2.5, 180.0, 1.0),
    (6.0, 0.0, 270.0, 0.8),
    (8.0, -2.5, 360.0, 1.0)
]


def interpolar(inicio, fim, progresso):
    """Calcula um valor entre início e fim."""
    return inicio + (fim - inicio) * progresso


def estadoChave(t, modo):
    """Calcula as transformações entre quadros-chave."""
    duracao = QUADROS_CHAVE[-1][0]
    tempo = t % duracao

    for i in range(len(QUADROS_CHAVE) - 1):
        t_inicio, x_inicio, ang_inicio, esc_inicio = QUADROS_CHAVE[i]
        t_fim, x_fim, ang_fim, esc_fim = QUADROS_CHAVE[i + 1]

        if t_inicio <= tempo < t_fim:
            progresso = (tempo - t_inicio) / (t_fim - t_inicio)

            x = interpolar(x_inicio, x_fim, progresso)
            angulo = interpolar(ang_inicio, ang_fim, progresso)
            escala = interpolar(esc_inicio, esc_fim, progresso)

            if modo not in (1, 4):
                x = 0.0
            if modo not in (2, 4):
                angulo = 0.0
            if modo not in (3, 4):
                escala = 1.0

            return x, angulo, escala

    return 0.0, 0.0, 1.0


def estadoChave2(t, modo):
    """Calcula a animação por quadros-chave."""
    duracao = QUADROS_CHAVE[-1][0]
    tempo = t % duracao

    for i in range(len(QUADROS_CHAVE) - 1):
        t_inicio, x_inicio, ang_inicio, esc_inicio = QUADROS_CHAVE[i]
        t_fim, x_fim, ang_fim, esc_fim = QUADROS_CHAVE[i + 1]

        if t_inicio <= tempo < t_fim:
            progresso = (tempo - t_inicio) / (t_fim - t_inicio)

            x = interpolar(x_inicio, x_fim, progresso)
            angulo = interpolar(ang_inicio, ang_fim, progresso)
            escala = interpolar(esc_inicio, esc_fim, progresso)

            if modo not in (1, 4):
                x = 0.0
            if modo not in (2, 4):
                angulo = 0.0
            if modo not in (3, 4):
                escala = 1.0

            return x, angulo, escala

    return 0.0, 0.0, 1.0


def estado(t, modo):
    """Retorna posição X/Y, ângulo e escala."""

    if modo in (1, 4):
        x = AMPLITUDE * math.sin(2 * math.pi * t / PERIODO)
        y = AMPLITUDE * math.cos(2 * math.pi * t / PERIODO)
    else:
        x = 0.0
        y = 0.0

    angulo = (GIRO * t) % 360 if modo in (2, 4) else 0.0

    escala = (
        1 + 0.2 * math.sin(2 * math.pi * t / 2)
        if modo in (3, 4)
        else 1.0
    )

    return x, y, angulo, escala


def nave():
    """Desenha a nave em 2D."""

    glColor3f(0.1, 0.8, 1.0)
    glBegin(GL_TRIANGLES)

    for ponto in [(0, 0.8), (-0.5, -0.5), (0.5, -0.5)]:
        glVertex2f(*ponto)

    glEnd()

    glColor3f(1.0, 0.65, 0.15)
    glBegin(GL_TRIANGLES)

    for ponto in [(-0.2, -0.5), (0.2, -0.5), (0, -0.9)]:
        glVertex2f(*ponto)

    glEnd()


def cubo():
    """Desenha um cubo 3D."""

    vertices = [
        (-1, -1, -1), (1, -1, -1),
        (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1),
        (1, 1, 1), (-1, 1, 1)
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (3, 2, 6, 7),
        (0, 3, 7, 4),
        (1, 5, 6, 2)
    ]

    cores = [
        (0.2, 0.6, 1),
        (1, 0.5, 0.2),
        (0.3, 0.8, 0.4),
        (0.9, 0.3, 0.5),
        (0.7, 0.4, 0.9),
        (1, 0.8, 0.2)
    ]

    glBegin(GL_TRIANGLES)

    for face, cor in zip(faces, cores):
        glColor3f(*cor)

        for indice in (
            face[0], face[1], face[2],
            face[0], face[2], face[3]
        ):
            glVertex3f(*vertices[indice])

    glEnd()


def satelite():
    """Desenha um satélite com corpo central e painéis solares."""

    # Corpo central
    glPushMatrix()
    glScalef(0.4, 0.4, 0.4)
    cubo()
    glPopMatrix()

    # Painel solar esquerdo
    glPushMatrix()
    glTranslatef(-1.0, 0.0, 0.0)
    glScalef(0.5, 0.12, 0.3)
    cubo()
    glPopMatrix()

    # Painel solar direito
    glPushMatrix()
    glTranslatef(1.0, 0.0, 0.0)
    glScalef(0.5, 0.12, 0.3)
    cubo()
    glPopMatrix()


def configurar_projecao(tipo, perspectiva):
    """Configura a projeção da cena."""

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if tipo == '3D' and perspectiva:
        gluPerspective(45, 960 / 640, 0.1, 100)
    else:
        glOrtho(-6, 6, -4, 4, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)


def executar(tipo='2D', limite_segundos=None):
    """Executa a animação 2D ou 3D."""

    if tipo not in ('2D', '3D'):
        raise ValueError("Escolha '2D' ou '3D'.")

    pygame.init()

    try:
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MAJOR_VERSION, 2
        )
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MINOR_VERSION, 1
        )
        pygame.display.gl_set_attribute(
            pygame.GL_DEPTH_SIZE, 24
        )

        pygame.display.set_mode(
            (960, 640),
            pygame.DOUBLEBUF | pygame.OPENGL
        )

        glViewport(0, 0, 960, 640)
        glClearColor(0.04, 0.06, 0.12, 1)

        if tipo == '3D':
            glEnable(GL_DEPTH_TEST)
        else:
            glDisable(GL_DEPTH_TEST)

        relogio = pygame.time.Clock()
        t = 0.0
        tempo_real = 0.0
        pausado = False
        fator = VELOCIDADE
        modo = 4
        perspectiva = True
        rodando = True

        while rodando:
            dt = relogio.tick(FPS) / 1000.0
            tempo_real += dt

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                elif evento.type == pygame.KEYDOWN:
                    tecla = evento.key

                    if tecla == pygame.K_ESCAPE:
                        rodando = False

                    elif tecla == pygame.K_SPACE:
                        pausado = not pausado

                    elif tecla == pygame.K_r:
                        t = 0.0

                    elif tecla == pygame.K_UP:
                        fator = min(4, fator + 0.25)

                    elif tecla == pygame.K_DOWN:
                        fator = max(0.25, fator - 0.25)

                    elif tecla == pygame.K_p:
                        perspectiva = not perspectiva

                    elif tecla in (
                        pygame.K_1, pygame.K_2,
                        pygame.K_3, pygame.K_4
                    ):
                        modo = tecla - pygame.K_0

            if (
                limite_segundos is not None
                and tempo_real >= limite_segundos
            ):
                rodando = False

            if not rodando:
                break

            if not pausado:
                t += dt * fator

            x, y, angulo, escala = estado(t, modo)

            configurar_projecao(tipo, perspectiva)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -12)

            glPushMatrix()

            # Exercício 1: movimentação nos eixos X e Y.
            glTranslatef(x, y if tipo == '2D' else 0.0, 1)

            if tipo == '2D':
                glRotatef(angulo, 0, 0, 1)

            else:
                # Exercício 3: rotações nos eixos X, Y e Z.
                glRotatef(20 + angulo, 1, 0, 0)
                glRotatef(30 + angulo * 0.7, 0, 1, 0)
                glRotatef(angulo, 0, 0, 1)

            glScalef(escala, escala, escala)

            if tipo == '2D':
                nave()
            else:
                satelite()

            glPopMatrix()
            pygame.display.flip()

            pygame.display.set_caption(
                f'{tipo} | modo {modo} | {fator:.2f}x | '
                f'{relogio.get_fps():.0f} FPS | '
                'ESPACO pausa | R reinicia | 1-4 modos | '
                'setas velocidade | P projecao | ESC sair'
            )

    finally:
        pygame.quit()


# Experimento de câmera
RAIO_CAMERA = 12.0
PERIODO_CAMERA = 12.0


def posicao_camera(t, modo):
    """Calcula a posição da câmera e o ponto observado."""

    fase = 2 * math.pi * t / PERIODO_CAMERA

    if modo == 1:
        # Órbita: a câmera percorre um círculo.
        olho = (
            RAIO_CAMERA * math.sin(fase),
            5.0,
            RAIO_CAMERA * math.cos(fase)
        )
        alvo = (0.0, 0.0, 0.0)

    elif modo == 2:
        # Movimento lateral: câmera e alvo avançam juntos.
        x = 5.0 * math.sin(fase)
        olho = (x, 4.0, 12.0)
        alvo = (x, 0.0, 0.0)

    else:
        # Dolly: a câmera se aproxima e se afasta.
        distancia = 10.0 + 4.0 * math.cos(fase)
        olho = (0.0, 3.0, distancia)
        alvo = (0.0, 0.0, 0.0)

    return olho, alvo


def desenhar_cena_camera():
    """Desenha a grade e os cubos usados no experimento."""

    glColor3f(0.3, 0.35, 0.42)
    glBegin(GL_LINES)

    for i in range(-8, 9):
        glVertex3f(i, -1.05, -8)
        glVertex3f(i, -1.05, 8)

        glVertex3f(-8, -1.05, i)
        glVertex3f(8, -1.05, i)

    glEnd()

    # Cubos fixos em diferentes profundidades.
    for x, z, tamanho in [
        (0, 0, 1.0),
        (-3, -3, 0.8),
        (3, 3, 0.6)
    ]:
        glPushMatrix()
        glTranslatef(x, -1.0 + tamanho, z)
        glScalef(tamanho, tamanho, tamanho)
        cubo()
        glPopMatrix()


def executar_camera(limite_segundos=None):
    """Executa o experimento com movimentos de câmera."""

    pygame.init()

    try:
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MAJOR_VERSION, 2
        )
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MINOR_VERSION, 1
        )
        pygame.display.gl_set_attribute(
            pygame.GL_DEPTH_SIZE, 24
        )

        pygame.display.set_mode(
            (960, 640),
            pygame.DOUBLEBUF | pygame.OPENGL
        )

        glViewport(0, 0, 960, 640)
        glClearColor(0.04, 0.06, 0.12, 1)
        glEnable(GL_DEPTH_TEST)

        relogio = pygame.time.Clock()
        t = 0.0
        tempo_real = 0.0
        fator = 1.0
        modo = 1
        pausado = False
        perspectiva = True
        rodando = True

        nomes = {
            1: 'Orbita',
            2: 'Lateral',
            3: 'Dolly'
        }

        while rodando:
            dt = relogio.tick(FPS) / 1000.0
            tempo_real += dt

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                elif evento.type == pygame.KEYDOWN:
                    tecla = evento.key

                    if tecla == pygame.K_ESCAPE:
                        rodando = False

                    elif tecla == pygame.K_SPACE:
                        pausado = not pausado

                    elif tecla == pygame.K_r:
                        t = 0.0

                    elif tecla == pygame.K_p:
                        perspectiva = not perspectiva

                    elif tecla == pygame.K_UP:
                        fator = min(4.0, fator + 0.25)

                    elif tecla == pygame.K_DOWN:
                        fator = max(0.25, fator - 0.25)

                    elif tecla in (
                        pygame.K_1, pygame.K_2, pygame.K_3
                    ):
                        modo = tecla - pygame.K_0
                        t = 0.0

            if (
                limite_segundos is not None
                and tempo_real >= limite_segundos
            ):
                rodando = False

            if not rodando:
                break

            if not pausado:
                t += dt * fator

            configurar_projecao('3D', perspectiva)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            olho, alvo = posicao_camera(t, modo)

            gluLookAt(
                *olho, *alvo,
                0.0, 1.0, 0.0
            )

            desenhar_cena_camera()
            pygame.display.flip()

            projecao = (
                'Perspectiva' if perspectiva
                else 'Ortografica'
            )

            pygame.display.set_caption(
                f'Camera: {nomes[modo]} | {projecao} | '
                f'{fator:.2f}x | 1-3 movimentos | '
                'P projecao | ESPACO pausa | R reinicia | ESC sair'
            )

    finally:
        pygame.quit()


if __name__ == '__main__':
    print('LABORATORIO - ANIMACOES 2D E 3D')
    print('1 - Nave 2D')
    print('2 - Satelite 3D')
    print('3 - Animacao da camera')

    opcao = input('Escolha uma opcao (1, 2 ou 3): ').strip()

    if opcao == '1':
        executar('2D')
    elif opcao == '2':
        executar('3D')
    elif opcao == '3':
        executar_camera()
    else:
        print('Opcao invalida. Execute novamente e escolha 1, 2 ou 3.')