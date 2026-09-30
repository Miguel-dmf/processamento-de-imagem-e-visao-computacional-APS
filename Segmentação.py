import cv2
import numpy as np


def segmentar_vegetacao(imagem):
    '''
    Identifica as regiões correspondentes à vegetação.
    Recebe:
        imagem processada.
    Retorna:
        máscara de vegetação:
        branco (255) = vegetação
        preto (0) = não vegetação
    '''
    if imagem is None:
        raise ValueError("A imagem recebida para segmentação é inválida.")

    # BGR -> HSV: facilita separar vegetação por tonalidade,
    # saturação e brilho.
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # Faixa inicial para tons de verde.
    # Estes valores serão ajustados usando as imagens reais do projeto.
    limite_inferior = np.array([25, 35, 30], dtype=np.uint8)
    limite_superior = np.array([100, 255, 255], dtype=np.uint8)

    # Cria a máscara binária.
    mascara = cv2.inRange(hsv, limite_inferior, limite_superior)

    # Remove pequenos ruídos.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mascara = cv2.morphologyEx(
        mascara, cv2.MORPH_OPEN, kernel, iterations=1
    )

    # Preenche pequenas falhas e une partes próximas.
    mascara = cv2.morphologyEx(
        mascara, cv2.MORPH_CLOSE, kernel, iterations=2
    )

    # Garante uma máscara realmente binária: 0 ou 255.
    _, mascara = cv2.threshold(
        mascara, 127, 255, cv2.THRESH_BINARY
    )

    return mascara