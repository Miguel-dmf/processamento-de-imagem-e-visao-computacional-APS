import cv2

from Filtro import filtro_gaussiano
from Segmentacao import segmentar_vegetacao
from Analise import calcular_cobertura_vegetal


def carregar_imagem(caminho):
    """
    Carrega uma imagem do computador.

    Parâmetro:
        caminho: caminho do arquivo da imagem

    Retorno:
        imagem carregada pelo OpenCV
    """

    imagem = cv2.imread(caminho)

    if imagem is None:
        raise FileNotFoundError(
            "Não foi possível carregar a imagem."
        )

    return imagem


def processar_imagem(caminho):
    """
    Controla todas as etapas de processamento da imagem.

    Etapas:
        1 - carrega a imagem
        2 - aplica filtro Gaussiano
        3 - faz a segmentação
        4 - calcula a cobertura vegetal
        5 - organiza os resultados
    """

    # --------------------------------------------------
    # 1. CARREGAMENTO
    # --------------------------------------------------

    imagem_original = carregar_imagem(
        caminho
    )


    # --------------------------------------------------
    # 2. FILTRO GAUSSIANO
    # --------------------------------------------------

    imagem_filtrada = filtro_gaussiano(
        imagem_original,
        tamanho=5,
        sigma=1.0
    )


    # --------------------------------------------------
    # 3. SEGMENTAÇÃO
    # --------------------------------------------------

    mascara = segmentar_vegetacao(
        imagem_filtrada
    )


    # --------------------------------------------------
    # 4. ANÁLISE
    # --------------------------------------------------

    cobertura = calcular_cobertura_vegetal(
        mascara
    )


    # --------------------------------------------------
    # 5. RESULTADOS
    # --------------------------------------------------

    resultado = {
        "imagem_original": imagem_original,
        "imagem_filtrada": imagem_filtrada,
        "mascara": mascara,
        "cobertura_vegetal": cobertura
    }


    return resultado