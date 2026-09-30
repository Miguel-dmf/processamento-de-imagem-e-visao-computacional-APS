import cv2

from Filtro import filtro_gaussiano


def carregar_imagem(caminho):
    """
    Carrega uma imagem do computador.

    Parâmetro:
        caminho: caminho do arquivo da imagem

    Retorno:
        imagem carregada pelo OpenCV
    """

    imagem = cv2.imread(caminho)

    # Caso o arquivo não exista,
    # esteja corrompido ou não possa ser aberto.
    if imagem is None:
        raise FileNotFoundError(
            "Não foi possível carregar a imagem."
        )

    return imagem


def processar_imagem(caminho):
    """
    Controla as etapas de processamento da imagem.

    Atualmente:
        1 - carrega a imagem
        2 - aplica filtro Gaussiano

    Futuramente:
        3 - segmenta a vegetação
        4 - analisa os resultados
    """

    # --------------------------------
    # 1. CARREGAMENTO
    # --------------------------------

    imagem_original = carregar_imagem(
        caminho
    )


    # --------------------------------
    # 2. FILTRAGEM
    # --------------------------------

    imagem_filtrada = filtro_gaussiano(
        imagem_original,
        tamanho=5,
        sigma=1.0
    )


    # --------------------------------
    # 3. SEGMENTAÇÃO
    # --------------------------------

    # Ainda será implementado.
    #
    # mascara = segmentar_vegetacao(
    #     imagem_filtrada
    # )


    # --------------------------------
    # 4. ANÁLISE
    # --------------------------------

    # Ainda será implementado.
    #
    # cobertura = calcular_cobertura_vegetal(
    #     mascara
    # )


    # Organizamos os resultados.
    resultado = {
        "imagem_original": imagem_original,
        "imagem_filtrada": imagem_filtrada
    }

    return resultado