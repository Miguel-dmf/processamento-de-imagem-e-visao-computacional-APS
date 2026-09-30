import cv2
import tkinter as tk

from pathlib import Path
from tkinter import filedialog

from Processamento import processar_imagem
from Segmentação import segmentar_vegetacao
from Analise import calcular_cobertura_vegetal


print("O teste começou")


# --------------------------------------------------
# 1. Abre o seletor de arquivos na pasta Downloads
# --------------------------------------------------

janela = tk.Tk()
janela.withdraw()

pasta_downloads = Path.home() / "Downloads"

caminho_imagem = filedialog.askopenfilename(
    initialdir=pasta_downloads,
    title="Selecione uma imagem",
    filetypes=[
        ("Imagens", "*.jpg *.jpeg *.png"),
        ("Todos os arquivos", "*.*")
    ]
)


# Caso o usuário feche sem selecionar nada
if not caminho_imagem:
    print("Nenhuma imagem selecionada.")
    exit()


# --------------------------------------------------
# 2. Processamento + filtro Gaussiano
# --------------------------------------------------

resultado = processar_imagem(
    caminho_imagem
)

imagem_filtrada = resultado["imagem_filtrada"]


# --------------------------------------------------
# 3. Segmentação
# --------------------------------------------------

mascara = segmentar_vegetacao(
    imagem_filtrada
)


# --------------------------------------------------
# 4. Análise
# --------------------------------------------------

cobertura = calcular_cobertura_vegetal(
    mascara
)

print(f"Cobertura vegetal: {cobertura:.2f}%")


# --------------------------------------------------
# 5. Salva somente para conseguirmos conferir o teste
# --------------------------------------------------

cv2.imwrite(
    "imagem_gaussiana.jpg",
    imagem_filtrada
)

cv2.imwrite(
    "mascara_teste.png",
    mascara
)

hsv = cv2.cvtColor(
    imagem_filtrada,
    cv2.COLOR_BGR2HSV
)

h, s, v = cv2.split(hsv)

cv2.imwrite("teste_h.png", h)
cv2.imwrite("teste_s.png", s)
cv2.imwrite("teste_v.png", v)

print("Teste concluído!")