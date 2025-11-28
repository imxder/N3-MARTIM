# Comparador de Imagens com Processamento Computacional

Este projeto consiste em uma aplicação desenvolvida em Python voltada para análise e comparação entre duas imagens. O sistema identifica pontos relevantes, encontra correspondências entre eles e exibe visualmente o resultado. O objetivo é verificar se duas imagens representam o mesmo ambiente ou estrutura, mesmo sob variações como ângulo, iluminação ou distância.

A aplicação utiliza métodos consolidados de detecção e correspondência de características, oferecendo um fluxo robusto de análise.

## Visão Geral do Aplicativo

O programa possui uma interface simples, permitindo ao usuário selecionar duas imagens e visualizar o resultado da comparação. A imagem final é apresentada com as correspondências válidas destacadas.

*(Aqui você pode inserir uma captura de tela da interface em funcionamento)*

## Funcionalidades

* Interface construída com Tkinter para fácil utilização.
* Seleção direta de duas imagens armazenadas no computador.
* Detecção de keypoints utilizando o algoritmo ORB.
* Aplicação de filtros de validação, incluindo o Ratio Test e o método RANSAC.
* Renderização da imagem final contendo apenas correspondências consideradas válidas.
* Salvamento automático do resultado em alta resolução no diretório `resultados/`.

## Requisitos

O projeto utiliza Python 3.x e as seguintes bibliotecas:

* opencv-python
* numpy
* pillow

Todas podem ser instaladas através do arquivo `requirements.txt` ou manualmente.

## Como Executar o Projeto

### 1. Clonar o repositório

```
git clone https://github.com/imxder/N3-MARTIM.git
cd N3-MARTIM
```

### 2. Criar o ambiente virtual

#### Windows (PowerShell)

```
python -m venv venv
./venv/Scripts/Activate.ps1
```

#### Linux ou macOS

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```
pip install -r requirements.txt
```

### 4. Iniciar o aplicativo

```
python main.py
```

Após iniciar:

* Selecione a primeira imagem.
* Selecione a segunda imagem.
* Clique no botão responsável pela comparação.

### 5. Resultado

O processamento pode levar alguns segundos. Após finalizado:

* A visualização das correspondências aparecerá na interface.
* Uma cópia em alta resolução será salva na pasta `resultados/`.

## Funcionamento Interno do Sistema

O pipeline básico segue a seguinte lógica:

1. As imagens são carregadas em escala de cinza para processamento e em cores para exibição.
2. O ORB detecta pontos de interesse e gera os respectivos descritores.
3. Um comparador baseado em busca exaustiva encontra correspondências candidatas.
4. O Ratio Test remove pareamentos ambíguos.
5. O método RANSAC filtra correspondências inconsistentes geometricamente.
6. A imagem final é construída exibindo apenas os pareamentos aprovados.

## Encerrando o Ambiente Virtual

```
deactivate
```
