print("O teste começou")

import cv2
from Segmentação import segmentar_vegetacao
from Analise import calcular_cobertura_vegetal


# 1. Carrega a imagem
imagem = cv2.imread("imagem_teste.jpg")

if imagem is None:
    print("Erro: imagem não encontrada.")
    exit()

# 2. Faz a segmentação
mascara = segmentar_vegetacao(imagem)

# 3. Faz a análise
cobertura = calcular_cobertura_vegetal(mascara)

# 4. Mostra o resultado no terminal
print(f"Cobertura vegetal: {cobertura:.2f}%")

# 5. Salva a máscara para podermos visualizar
cv2.imwrite("mascara_teste.png", mascara)

print("Máscara salva como: mascara_teste.png")