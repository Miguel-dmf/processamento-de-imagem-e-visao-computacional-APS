import cv2


def calcular_cobertura_vegetal(mascara):
    """
    Calcula a porcentagem de pixels classificados como vegetação.
    Recebe:
        máscara de vegetação.
    Retorna:
        porcentagem de cobertura vegetal, de 0 a 100.
    """
    if mascara is None:
        raise ValueError("A máscara recebida para análise é inválida.")

    # A máscara deve ser uma imagem em escala de cinza/binária.
    if len(mascara.shape) != 2:
        raise ValueError(
            "A máscara deve ser uma imagem em escala de cinza (binária)."
        )

    # Total de pixels da imagem.
    total_pixels = mascara.shape[0] * mascara.shape[1]

    if total_pixels == 0:
        return 0.0

    # Na máscara:
    # 0 = não vegetação
    # 255 = vegetação
    pixels_vegetacao = cv2.countNonZero(mascara)

    cobertura = (pixels_vegetacao / total_pixels) * 100

    return cobertura
