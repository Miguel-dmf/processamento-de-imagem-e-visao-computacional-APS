import cv2
import numpy as np


def segmentar_vegetacao(imagem):
    """
    Identifica regiões mais escuras da imagem,
    tentando separar áreas arbóreas do restante.

    Branco (255) = possível área de árvores
    Preto (0) = restante da imagem
    """

    if imagem is None:
        raise ValueError(
            "A imagem recebida para segmentação é inválida."
        )

    # --------------------------------------------------
    # 1. Converte a imagem de BGR para HSV
    # --------------------------------------------------

    hsv = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2HSV
    )

    # Separa os três canais:
    #
    # H = tonalidade
    # S = saturação
    # V = brilho
    h, s, v = cv2.split(hsv)


    # --------------------------------------------------
    # 2. Segmentação pelo brilho
    # --------------------------------------------------

    # O Otsu tenta encontrar automaticamente
    # um ponto de separação entre regiões
    # claras e escuras.
    #
    # THRESH_BINARY_INV é utilizado porque:
    #
    # áreas escuras  -> branco
    # áreas claras   -> preto

    _, mascara_brilho = cv2.threshold(
        v,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )


    # --------------------------------------------------
    # 3. Cria uma máscara ampla para tons verdes
    # --------------------------------------------------

    limite_verde_inferior = np.array(
        [25, 30, 0],
        dtype=np.uint8
    )

    limite_verde_superior = np.array(
        [100, 255, 255],
        dtype=np.uint8
    )

    mascara_verde = cv2.inRange(
        hsv,
        limite_verde_inferior,
        limite_verde_superior
    )


    # --------------------------------------------------
    # 4. Junta as duas condições
    # --------------------------------------------------

    # O pixel precisa ser:
    #
    # - verde
    # E
    # - relativamente escuro
    #
    # para ser considerado área arbórea.

    mascara = cv2.bitwise_and(
        mascara_brilho,
        mascara_verde
    )


    # --------------------------------------------------
    # 5. Remove pequenos ruídos
    # --------------------------------------------------

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )


    return mascara