import numpy as np

def criar_kernel_gaussiano(tamanho, sigma):
    """
    Cria manualmente um kernel Gaussiano.
    """

    if tamanho <= 1 or tamanho % 2 == 0:
        raise ValueError(
            "O tamanho do kernel deve ser ímpar e maior que 1."
        )

    if sigma <= 0:
        raise ValueError(
            "O sigma deve ser maior que zero."
        )

    # Encontra o centro do kernel.
    meio = tamanho // 2

    # Exemplo para tamanho 5:
    # [-2, -1, 0, 1, 2]
    eixo = np.arange(
        -meio,
        meio + 1
    )

    # Cria as coordenadas X e Y.
    x, y = np.meshgrid(
        eixo,
        eixo
    )

    # Calcula os pesos Gaussianos.
    kernel = np.exp(
        -(x ** 2 + y ** 2)
        / (2 * sigma ** 2)
    )

    # Faz com que a soma dos pesos seja igual a 1.
    kernel = kernel / np.sum(kernel)

    return kernel


def filtro_gaussiano(
    imagem,
    tamanho=5,
    sigma=1.0
):
    """
    Aplica manualmente o filtro Gaussiano.
    """

    # Cria o kernel.
    kernel = criar_kernel_gaussiano(
        tamanho,
        sigma
    )

    # Adiciona uma terceira dimensão ao kernel
    # para trabalhar com os canais B, G e R.
    kernel_3d = kernel[:, :, np.newaxis]

    # Quantidade necessária de pixels nas bordas.
    padding = tamanho // 2

    # Adiciona bordas temporárias à imagem.
    imagem_expandida = np.pad(
        imagem,
        (
            (padding, padding),
            (padding, padding),
            (0, 0)
        ),
        mode="edge"
    )

    # Obtém o tamanho da imagem.
    altura, largura, canais = imagem.shape

    # Cria uma imagem vazia para receber o resultado.
    resultado = np.zeros_like(
        imagem,
        dtype=np.float32
    )

    # Percorre todos os pixels.
    for y in range(altura):
        for x in range(largura):

            # Seleciona a vizinhança do pixel atual.
            regiao = imagem_expandida[
                y:y + tamanho,
                x:x + tamanho
            ]

            # Multiplica os pixels pelos pesos
            # do filtro Gaussiano e soma.
            valor_pixel = np.sum(
                regiao * kernel_3d,
                axis=(0, 1)
            )

            # Salva o novo valor.
            resultado[y, x] = valor_pixel

    # Limita os valores entre 0 e 255.
    resultado = np.clip(
        resultado,
        0,
        255
    )

    # Converte novamente para o formato comum de imagem.
    return resultado.astype(np.uint8)