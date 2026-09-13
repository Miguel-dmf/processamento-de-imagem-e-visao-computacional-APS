def processar_imagem(imagem):

    imagem_filtrada = filtro_media(imagem)

    mascara = segmentar_vegetacao(imagem_filtrada)

    cobertura = calcular_cobertura_vegetal(mascara)

    resultado = {
        "imagem_original": imagem,
        "imagem_filtrada": imagem_filtrada,
        "mascara": mascara,
        "cobertura_vegetal": cobertura
    }

    return resultado