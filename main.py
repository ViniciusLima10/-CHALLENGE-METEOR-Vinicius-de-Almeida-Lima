from PIL import Image
import numpy as np

def contar_estrelas_e_meteoros(imagem_caminho):
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')
    
    # Inicializar contadores
    contador_estrelas = 0
    contador_meteoros = 0
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Iterar sobre todos os pixels
    for y in range(altura):
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            
            # Verificar se o pixel é branco (RGB: 255, 255, 255)
            if r == 255 and g == 255 and b == 255:
                contador_estrelas += 1
            
            # Verificar se o pixel é ermelho (RGB: 0, 0, 255)
            elif r == 255 and g == 0 and b == 0:
                contador_meteoros += 1
    
    # Retornar os resultados
    return contador_estrelas, contador_meteoros


def cortar_abaixo_da_agua(imagem_caminho, imagem_saida_caminho):
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Variável para armazenar a linha com o primeiro pixel azul
    linha_primeiro_azul = None
    
    # Iterar sobre todos os pixels
    for y in range(altura):
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            
            # Verificar se o pixel é azul (RGB: 0, 0, 255)
            if r == 0 and g == 0 and b == 255:
                linha_primeiro_azul = y
                break
        if linha_primeiro_azul is not None:
            break
    
    # Se encontramos uma linha com pixels azuis, cortamos a imagem
    if linha_primeiro_azul is not None:
        caixa_corte = (0, 0, largura, linha_primeiro_azul +1)
        imagem_cortada = imagem.crop(caixa_corte)
        imagem_cortada.save(imagem_saida_caminho)


def transformar_em_preto(imagem_caminho, imagem_saida_caminho):
    # Cores permitidas
    cores_permitidas = [(255, 255, 255), (0, 0, 255), (255, 0, 0)]
    
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Iterar sobre todos os pixels
    for y in range(altura):
        for x in range(largura):
            # Obter a cor do pixel
            cor = imagem.getpixel((x, y))
            
            # Verificar se a cor não está na lista de cores permitidas
            if cor not in cores_permitidas:
                # Definir a cor como preto
                imagem.putpixel((x, y), (0, 0, 0))
    
    # Salvar a imagem
    imagem.save(imagem_saida_caminho)




def contar_meteoros_na_cordenada_x(imagem_caminho, cordenada_x):
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')    
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Inicializar contador de meteoros na água
    meteoros_na_linha_x = 0

    for y in range(altura - 1, -1, -1):  # Começa do fim da imagem para procurar pela linha inferior
        r, g, b = imagem.getpixel((cordenada_x, y))
        # Verificar se o pixel é meteoro (RGB: 255, 0, 0)
        if r == 255 and g == 0 and b == 0:
            meteoros_na_linha_x += 1
    return meteoros_na_linha_x


def contar_meteoros_na_agua(imagem_caminho):
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Inicializar contador de meteoros na água
    meteoros_na_agua = 0
    
    # Encontrar a linha com pixels azuis (representando a água)
    linha_azul = None
    for y in range(altura - 1, -1, -1):  # Começa do fim da imagem para procurar pela linha inferior
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            # Verificar se o pixel é azul (RGB: 0, 0, 255)
            if r == 0 and g == 0 and b == 255:
                meteoros_na_agua += contar_meteoros_na_cordenada_x(imagem_caminho, x)
                
        if linha_azul is not None:
            break
    
    # Retornar o número de meteoros na água
    return meteoros_na_agua


def reduzir_meteoros_e_estrelas(imagem_caminho, imagem_saida_caminho):
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Inicializar listas para indicar a presença de meteoros e estrelas
    presenca_meteoros = [0] * largura
    presenca_estrelas = [0] * largura
    
    # Iterar sobre todos os pixels da imagem
    for x in range(largura):
        for y in range(altura):
            r, g, b = imagem.getpixel((x, y))
            # Verificar se o pixel é vermelho (meteoro)
            if r == 255 and g == 0 and b == 0:
                presenca_meteoros[x] = 1
            # Verificar se o pixel é branco (estrela)
            elif r == 255 and g == 255 and b == 255:
                presenca_estrelas[x] = 1
    
    # Criar uma nova imagem com duas linhas
    nova_imagem = Image.new("RGB", (largura, 2), color=(0, 0, 0))
    
    # Definir os pixels na nova imagem de acordo com a presença de estrelas e meteoros
    for x in range(largura):
        # Linha 0 para estrelas
        if presenca_estrelas[x] == 1:
            nova_imagem.putpixel((x, 0), (255, 255, 255))
        # Linha 1 para meteoros
        if presenca_meteoros[x] == 1:
            nova_imagem.putpixel((x, 1), (255, 0, 0))
    
    # Salvar a nova imagem
    nova_imagem.save(imagem_saida_caminho)

def contar_cores_por_linha(imagem_caminho):
    # Carregar a imagem
    imagem = Image.open(imagem_caminho)
    
    # Garantir que a imagem está em modo RGB
    imagem = imagem.convert('RGB')
    
    # Obter dimensões da imagem
    largura, altura = imagem.size
    
    # Inicializar listas para contagem de cores
    contagem_pretos = [0] * altura
    contagem_vermelhos = [0] * altura
    contagem_brancos = [0] * altura
    
    # Iterar sobre todos os pixels da imagem
    for y in range(altura):
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            # Verificar se o pixel é preto
            if r == 0 and g == 0 and b == 0:
                contagem_pretos[y] += 1
            # Verificar se o pixel é vermelho
            elif r == 255 and g == 0 and b == 0:
                contagem_vermelhos[y] += 1
            # Verificar se o pixel é branco
            elif r == 255 and g == 255 and b == 255:
                contagem_brancos[y] += 1
    
    # Retornar as contagens
    return contagem_pretos, contagem_vermelhos, contagem_brancos

def imagem_para_array_binario(caminho_imagem):
    # Abre a imagem
    imagem = Image.open(caminho_imagem)
    
    # Converte a imagem para RGB, se necessário
    imagem = imagem.convert('RGB')
    
    # Obtém os dados da imagem
    dados = np.array(imagem)
    
    # Inicializa um array binário vazio com o mesmo tamanho da imagem
    array_binario = np.zeros((dados.shape[0], dados.shape[1]), dtype=int)
    
    # Percorre cada pixel da imagem
    for y in range(dados.shape[0]):
        for x in range(dados.shape[1]):
            r, g, b = dados[y, x]
            
            # Verifica se o pixel é preto (R=0, G=0, B=0)
            if r == 0 and g == 0 and b == 0:
                array_binario[y, x] = 0
            # Verifica se o pixel é vermelho (R=255, G=0, B=0)
            elif r == 255 and g == 0 and b == 0:
                array_binario[y, x] = 1
            elif r == 255 and g == 255 and b == 255:
                array_binario[y, x] = 1
            else:
                array_binario[y, x] = 0  # Outros casos podem ser tratados como 0 ou de outra forma, se necessário
    
    # Retorna o array binário como uma string única concatenada
    return ''.join(str(e) for e in array_binario.flatten())

def binario_para_texto(binario):
    if len(binario) % 8 != 0:
        raise ValueError("O comprimento da string binária deve ser um múltiplo de 8")
    
    # Divide a string binária em pedaços de 8 bits (1 byte)
    bytes_list = [binario[i:i+8] for i in range(0, len(binario), 8)]
    
    # Converte cada byte em um caractere ASCII e junta-os em uma string
    texto = ''.join([chr(int(byte, 2)) for byte in bytes_list])
    
    return texto
# Contar estrelas e meteoros
# estrelas, meteoros = contar_estrelas_e_meteoros('meteor_challenge_01.png')


# Cortar parte da imagem abaixo dos meteoros
cortar_abaixo_da_agua('meteor_challenge_01.png', 'meteor_challenge_02.png')


# Transformar pixels não permitidos em preto
transformar_em_preto('meteor_challenge_02.png', 'meteor_challenge_03.png')

# Encontrar meteoros na agua
meteoros_na_agua = contar_meteoros_na_agua('meteor_challenge_03.png')

# tentativav de encotrar a frase escondida
reduzir_meteoros_e_estrelas('meteor_challenge_03.png', 'meteor_challenge_04.png')

array_binario = imagem_para_array_binario('meteor_challenge_04.png')
texto_escondido = binario_para_texto(array_binario)





estrelas, meteoros = contar_estrelas_e_meteoros('meteor_challenge_04.png')
print('==========================================================')
print(f'=        Number of Stars           -        {estrelas}          =')
print(f'=        Number of Meteors         -        {meteoros}          =')
print(f'=  Meteors falling on the Water    -        {meteoros_na_agua}          =')
print(f'=        Hidden Phrase             -      {texto_escondido}          =')
print('==========================================================')
