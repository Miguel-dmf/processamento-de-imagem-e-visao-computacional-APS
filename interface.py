import cv2
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from Processamento import processar_imagem

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Análise de Cobertura Vegetal - APS")
        self.geometry("1100x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        # aqui vem o painel esquerdo com os botões
       
        self.painel_esquerdo = ctk.CTkFrame(self, width=280, corner_radius=10)
        self.painel_esquerdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.painel_esquerdo.grid_propagate(False)

        self.lbl_titulo_imagem = ctk.CTkLabel(self.painel_esquerdo, text="Imagem", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo_imagem.pack(pady=(20, 10), padx=20, anchor="w")

        self.caminho_entrada = ctk.CTkEntry(self.painel_esquerdo, placeholder_text="Nenhuma imagem...", height=35)
        self.caminho_entrada.configure(state="readonly")
        self.caminho_entrada.pack(fill="x", pady=(0, 15), padx=20)

        self.btn_selecionar = ctk.CTkButton(
            self.painel_esquerdo, text="Selecionar Arquivo", command=self.acao_selecionar,
            fg_color="transparent", border_width=2, text_color="#DCE4EE"
        )
        self.btn_selecionar.pack(fill="x", pady=(0, 15), padx=20)

        self.btn_processar = ctk.CTkButton(
            self.painel_esquerdo, text="Processar Imagem", command=self.acao_processar, 
            height=40, font=ctk.CTkFont(weight="bold")
        )
        self.btn_processar.pack(fill="x", pady=(0, 10), padx=20)

        self.lbl_status = ctk.CTkLabel(self.painel_esquerdo, text="", text_color="#FBBF24", font=ctk.CTkFont(size=12))
        self.lbl_status.pack(pady=(0, 10), padx=20)

        self.lbl_titulo_analise = ctk.CTkLabel(self.painel_esquerdo, text="Análise", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo_analise.pack(pady=(10, 10), padx=20, anchor="w")

        self.frame_resultado = ctk.CTkFrame(self.painel_esquerdo, corner_radius=10, border_width=1)
        self.frame_resultado.pack(pady=10, padx=20, fill="x")

        self.lbl_cobertura = ctk.CTkLabel(self.frame_resultado, text="Cobertura Vegetal:\n---%", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_cobertura.pack(pady=20, padx=10)

     
        # paniel direito onde ficarão as abas (imagens filtradas e passo a passo do hsv)

        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        self.tab_principal = self.tabview.add("Resultados Principais")
        self.tab_hsv = self.tabview.add("Passo a Passo (HSV)")

        # primeira aba -- resultados principais
        self.tab_principal.grid_columnconfigure((0, 1), weight=1)
        self.tab_principal.grid_rowconfigure((0, 1), weight=1)

        self.lbl_img_orig = self.criar_container_imagem(self.tab_principal, "Imagem Original", 0, 0)
        self.lbl_img_filt = self.criar_container_imagem(self.tab_principal, "Imagem Filtrada (Gaussiano)", 0, 1)
        self.lbl_img_masc = self.criar_container_imagem(self.tab_principal, "Máscara de Vegetação", 1, 0, colspan=2)

        # segunda aba -- ciclo de hsv
        self.tab_hsv.grid_columnconfigure((0, 1, 2), weight=1)
        self.tab_hsv.grid_rowconfigure(0, weight=1)

        self.lbl_img_h = self.criar_container_imagem(self.tab_hsv, "Canal H (Matiz)", 0, 0)
        self.lbl_img_s = self.criar_container_imagem(self.tab_hsv, "Canal S (Saturação)", 0, 1)
        self.lbl_img_v = self.criar_container_imagem(self.tab_hsv, "Canal V (Brilho)", 0, 2)

    def criar_container_imagem(self, pai, titulo, linha, coluna, colspan=1):
        """função auxiliar para organizar os quadros de imagem"""
        frame = ctk.CTkFrame(pai, corner_radius=10, fg_color="#1E1E1E")
        frame.grid(row=linha, column=coluna, columnspan=colspan, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(weight="bold")).pack(pady=10)
        lbl_img = ctk.CTkLabel(frame, text="📷\n[Aguardando]", text_color="gray50")
        lbl_img.pack(expand=True, fill="both", padx=10, pady=10)
        return lbl_img

    def converter_cv2_para_ctk(self, cv2_img, is_gray=False, tamanho=(300, 200)):
        """converte as matrizes do OpenCV para o formato aceito pela interface (CTkImage)"""
        if is_gray:
            pil_img = Image.fromarray(cv2_img)
        else:
            pil_img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
        return ctk.CTkImage(light_image=pil_img, size=tamanho)

    # aqui vem os métodos de ação

    def acao_selecionar(self):
        caminho_selecionado = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png"), ("Todos os arquivos", "*.*")]
        )
        
        if caminho_selecionado:
            self.caminho_entrada.configure(state="normal")
            self.caminho_entrada.delete(0, 'end')
            self.caminho_entrada.insert(0, caminho_selecionado)
            self.caminho_entrada.configure(state="readonly")
            self.lbl_status.configure(text="")

    def acao_processar(self):
        caminho = self.caminho_entrada.get()

        if not caminho:
            self.lbl_status.configure(
                text="Erro: Selecione uma imagem primeiro!",
                text_color="#EF4444"
            )
            return

        self.lbl_status.configure(
            text="Processando imagem, aguarde...",
            text_color="#FBBF24"
        )
        self.update()

        try:
            # 1. Executa o processamento no back-end
            resultados = processar_imagem(caminho)

            # 2. Recupera as imagens e a porcentagem calculada
            imagem_original = resultados["imagem_original"]
            imagem_filtrada = resultados["imagem_filtrada"]
            mascara = resultados["mascara"]
            cobertura = resultados["cobertura_vegetal"]

            # 3. Converte a imagem filtrada para HSV
            imagem_hsv = cv2.cvtColor(
                imagem_filtrada,
                cv2.COLOR_BGR2HSV
            )

            # 4. Separa os canais H, S e V
            h, s, v = cv2.split(imagem_hsv)

            # 5. Converte as imagens para exibição na interface
            img_original_ctk = self.converter_cv2_para_ctk(
                imagem_original
            )
            img_filtrada_ctk = self.converter_cv2_para_ctk(
                imagem_filtrada
            )
            img_mascara_ctk = self.converter_cv2_para_ctk(
                mascara,
                is_gray=True
            )

            img_h_ctk = self.converter_cv2_para_ctk(
                h,
                is_gray=True
            )
            img_s_ctk = self.converter_cv2_para_ctk(
                s,
                is_gray=True
            )
            img_v_ctk = self.converter_cv2_para_ctk(
                v,
                is_gray=True
            )

            # 6. Exibe as imagens nos respectivos espaços
            self.lbl_img_orig.configure(
                image=img_original_ctk,
                text=""
            )
            self.lbl_img_filt.configure(
                image=img_filtrada_ctk,
                text=""
            )
            self.lbl_img_masc.configure(
                image=img_mascara_ctk,
                text=""
            )

            self.lbl_img_h.configure(image=img_h_ctk, text="")
            self.lbl_img_s.configure(image=img_s_ctk, text="")
            self.lbl_img_v.configure(image=img_v_ctk, text="")

            # 7. Mantém referências às imagens na memória
            self.img_original_ctk = img_original_ctk
            self.img_filtrada_ctk = img_filtrada_ctk
            self.img_mascara_ctk = img_mascara_ctk
            self.img_h_ctk = img_h_ctk
            self.img_s_ctk = img_s_ctk
            self.img_v_ctk = img_v_ctk

            # 8. Define a cor conforme a cobertura calculada
            if cobertura >= 75.0:
                cor_destaque = "#10B981"
            elif cobertura < 50.0:
                cor_destaque = "#EF4444"
            else:
                cor_destaque = "#F59E0B"

            # 9. Atualiza a porcentagem na interface
            self.lbl_cobertura.configure(
                text=f"Cobertura Vegetal:\n{cobertura:.2f}%",
                text_color=cor_destaque
            )

            # 10. Finaliza a operação
            self.tabview.set("Resultados Principais")
            self.lbl_status.configure(
                text="Processamento concluído com sucesso!",
                text_color="#10B981"
            )

        except Exception as erro:
            self.lbl_status.configure(
                text=f"Erro ao processar a imagem: {erro}",
                text_color="#EF4444"
            )
            print("Erro detalhado:", erro)

if __name__ == "__main__":
    app = App()
    app.mainloop()