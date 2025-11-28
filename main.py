import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def analisar_semelhanca(caminho_a, caminho_b):
    LIMIAR_RATIO = 0.85
    MINIMO_INLIERS = 10

    try:
        cinza_a = cv2.imread(caminho_a, cv2.IMREAD_GRAYSCALE)
        cinza_b = cv2.imread(caminho_b, cv2.IMREAD_GRAYSCALE)

        cor_a = cv2.imread(caminho_a)
        cor_b = cv2.imread(caminho_b)

        if cinza_a is None or cinza_b is None:
            raise IOError("Erro ao carregar uma das imagens.")

    except Exception as erro:
        messagebox.showerror("Falha no carregamento", str(erro))
        return None

    detector = cv2.ORB_create(nfeatures=10000)
    pontos_a, descritores_a = detector.detectAndCompute(cinza_a, None)
    pontos_b, descritores_b = detector.detectAndCompute(cinza_b, None)

    emparelhador = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    if descritores_a is None or descritores_b is None or len(descritores_a) < 2 or len(descritores_b) < 2:
        print("Pontos insuficientes para comparação.")
        return cv2.drawMatches(cor_a, pontos_a, cor_b, pontos_b, [], None)

    pares = emparelhador.knnMatch(descritores_a, descritores_b, k=2)

    bons_pares = []
    if pares and all(len(p) == 2 for p in pares):
        for melhor, segundo in pares:
            if melhor.distance < LIMIAR_RATIO * segundo.distance:
                bons_pares.append(melhor)

    print(f"Bons pares após o filtro: {len(bons_pares)}")

    if len(bons_pares) > MINIMO_INLIERS:
        origem = np.float32([pontos_a[m.queryIdx].pt for m in bons_pares]).reshape(-1, 1, 2)
        destino = np.float32([pontos_b[m.trainIdx].pt for m in bons_pares]).reshape(-1, 1, 2)

        H, mascara = cv2.findHomography(origem, destino, cv2.RANSAC, 5.0)

        if mascara is not None:
            mascara_lista = mascara.ravel().tolist()
            total_inliers = sum(mascara_lista)

            print(f"Inliers detectados: {total_inliers}")

            if total_inliers > MINIMO_INLIERS:
                print("Resultado: imagens do mesmo local.")

                params_linhas = dict(matchColor=(0, 255, 0), matchesMask=mascara_lista, singlePointColor=None, flags=2)
                imagem_linhas = cv2.drawMatches(cor_a, pontos_a, cor_b, pontos_b, bons_pares, None, **params_linhas)

                params_pontos = dict(matchColor=(0, 255, 0), matchesMask=mascara_lista, singlePointColor=None, flags=6)
                imagem_linhas_pontos = cv2.drawMatches(cor_a, pontos_a, cor_b, pontos_b, bons_pares, None, **params_pontos)

                kp_a_validos = [pontos_a[m.queryIdx] for i, m in enumerate(bons_pares) if mascara_lista[i] == 1]
                kp_b_validos = [pontos_b[m.trainIdx] for i, m in enumerate(bons_pares) if mascara_lista[i] == 1]

                img_a_kp = cv2.drawKeypoints(cor_a, kp_a_validos, None, color=(0, 0, 255), flags=4)
                img_b_kp = cv2.drawKeypoints(cor_b, kp_b_validos, None, color=(0, 0, 255), flags=4)

                h1, w1 = img_a_kp.shape[:2]
                h2, w2 = img_b_kp.shape[:2]

                sem_linhas = np.zeros((max(h1, h2), w1 + w2, 3), dtype="uint8")
                sem_linhas[:h1, :w1] = img_a_kp
                sem_linhas[:h2, w1:w1+w2] = img_b_kp

                pasta_saida = "resultados"
                os.makedirs(pasta_saida, exist_ok=True)

                cv2.imwrite(os.path.join(pasta_saida, "comparacao_linhas.png"), imagem_linhas)
                cv2.imwrite(os.path.join(pasta_saida, "comparacao_linhas_pontos.png"), imagem_linhas_pontos)
                cv2.imwrite(os.path.join(pasta_saida, "comparacao_pontos.png"), sem_linhas)

                print("Arquivos salvos na pasta 'resultados'.")

                return imagem_linhas

    print("Resultado: locais diferentes.")
    return cv2.drawMatches(cor_a, pontos_a, cor_b, pontos_b, [], None)



caminho_1 = ""
caminho_2 = ""

def escolher_img1():
    global caminho_1
    arquivo = filedialog.askopenfilename(
        title="Escolha a primeira imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if arquivo:
        caminho_1 = arquivo
        label_img1.config(text=f"Imagem 1: {os.path.basename(arquivo)}", fg="green")

def escolher_img2():
    global caminho_2
    arquivo = filedialog.askopenfilename(
        title="Escolha a segunda imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if arquivo:
        caminho_2 = arquivo
        label_img2.config(text=f"Imagem 2: {os.path.basename(arquivo)}", fg="green")

def executar_comparacao():
    if not caminho_1 or not caminho_2:
        messagebox.showwarning("Atenção", "Selecione as duas imagens antes de continuar.")
        return

    status.config(text="Processando...", fg="blue")
    janela.update_idletasks()

    resultado = analisar_semelhanca(caminho_1, caminho_2)

    if resultado is None:
        status.config(text="Falha no processamento.", fg="red")
        return

    status.config(text="Concluído! Resultados em /resultados", fg="green")

    largura_max = 1200
    h, w = resultado.shape[:2]
    if w > largura_max:
        esc = largura_max / w
        nova_altura = int(h * esc)
        resultado = cv2.resize(resultado, (largura_max, nova_altura))

    rgb = cv2.cvtColor(resultado, cv2.COLOR_BGR2RGB)
    imagem_tk = ImageTk.PhotoImage(Image.fromarray(rgb))

    painel_resultado.config(image=imagem_tk)
    painel_resultado.image = imagem_tk




janela = tk.Tk()
janela.title("Verificação de Similaridade - ORB & RANSAC")
janela.geometry("1280x800")

frame_topo = tk.Frame(janela, pady=10)
frame_topo.pack()

btn_img1 = tk.Button(frame_topo, text="Carregar Imagem 1", width=20, command=escolher_img1)
btn_img1.pack(side=tk.LEFT, padx=10)

label_img1 = tk.Label(frame_topo, text="Nenhuma", fg="gray", width=30)
label_img1.pack(side=tk.LEFT)

btn_img2 = tk.Button(frame_topo, text="Carregar Imagem 2", width=20, command=escolher_img2)
btn_img2.pack(side=tk.LEFT, padx=10)

label_img2 = tk.Label(frame_topo, text="Nenhuma", fg="gray", width=30)
label_img2.pack(side=tk.LEFT)

frame_botao = tk.Frame(janela, pady=10)
frame_botao.pack()

btn_comparar = tk.Button(
    frame_botao,
    text="COMPARAR",
    command=executar_comparacao,
    width=30,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 12, "bold")
)
btn_comparar.pack()

status = tk.Label(janela, text="Selecione duas imagens para iniciar", font=("Helvetica", 10))
status.pack(pady=5)

frame_resultado = tk.Frame(janela, bg="gray", borderwidth=1, relief=tk.SUNKEN)
frame_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

painel_resultado = tk.Label(frame_resultado, bg="gray")
painel_resultado.pack(fill=tk.BOTH, expand=True)

janela.mainloop()
