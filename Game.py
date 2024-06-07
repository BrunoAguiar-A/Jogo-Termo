import random
import unicodedata

"""
    1.(cria_lista_palavras) Recebe uma string com o nome do arquivo e devolve uma lista contendo as palavras do arquivo.
"""
def cria_lista_palavras(nome_arquivo):
    with open(nome_arquivo, 'r',encoding='utf-8' ) as file:
        return [linha.strip().lower() for linha in file]

"""
    2.(checa_tentativa) Recebe a palavra secreta e o chute do usuário e devolve uma lista 'feedback' de 5 elementos
    para indicar acertos e erros. A lista 'feedback' deve conter o valor 1 (verde) se a letra
    correspondente em chute ocorre na mesma posição em palavra (letra certa no lugar certo),
    deve conter 2 se a letra em chute ocorre em outra posição em palavra (letra certa no lugar errado),
    e deve conter 0 caso contrário.
"""

def checa_tentativa(palavra, chute):
    feedback = [0] * 5
    palavraVerificada = comparar_letras(palavra)
    chuteVerificado = comparar_letras(chute)
    
    letras_disponiveis = list(palavraVerificada)
    
    for i in range(5):
        if chuteVerificado[i] == palavraVerificada[i]:
            feedback[i] = 1
            letras_disponiveis[i] = None  # Remove a letra usada
    
    for i in range(5):
        if feedback[i] == 0 and chuteVerificado[i] in letras_disponiveis:
            feedback[i] = 2
            letras_disponiveis[letras_disponiveis.index(chuteVerificado[i])] = None  # Remove a letra usada
    
    return feedback

"""
    3.(imprime_resultado) Recebe a lista de tentativas e imprime as tentativas, usando * para verde, + para amarelo
    e _ para letras que não aparecem na palavra sorteada.
    A lista de tentativas tem formato [[chute1, feedback1], [chute2, feedback2], ..., [chuten, feedbackn]].
"""

def imprime_resultado(lista_tentativas):
    simbolos = {1: '*', 2: '+', 0: '_'}
    for chute, feedback in lista_tentativas:
        resultado = ''.join(simbolos[f] for f in feedback)
        print(f"{chute}")
        print(f"{resultado}")

"""
    4.(atualiza_teclado) Modifica teclado para que as letras marcadas como inexistentes no chute sejam substituídas por espaços.
"""

def atualiza_teclado(chute, feedback, teclado):
    chuteVerificado = comparar_letras(chute)
    for i in range(5):
        if feedback[i] == 0:
            tecla = chuteVerificado[i]
            for linha in range(len(teclado)):
                teclado[linha] = teclado[linha].replace(tecla, ' ')

"""
    5.(comparar_letras) Comparar, remover acentos e converter letras para minúsculas para verificação.
"""

def comparar_letras(texto):
    texto = texto.replace('ç', 'c').replace('Ç', 'C')  # Substituir 'ç' por 'c' antes de normalizar
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()


"""
    6.(obter_idioma) Verifica se o usuário digitou apenas I para Ingles ou P para Portugues se nao,
    pede para ele digitar corratamente para o programa continuar.
"""

def obter_idioma():
    while True:
        idioma = input("Qual o idioma (I para inglês ou P para português)? ").strip().upper()
        if idioma in {'I', 'P'}:
            return idioma
        print("Entrada inválida! Por favor, digite 'I' para inglês ou 'P' para português.")
"""
    7.(Termo) Programa Principal
"""

def main():
    # Chama a função responsavel por perguntar qual o idioma o jogador prefere jogar (P =  Porgugues / I =  Inglês)
    idioma = obter_idioma()

    # Carrega o arquivo de texto contendo as palavras de cada lingua
    nome_arquivo = 'words.txt' if idioma == 'I' else 'palavras.txt'
    
    palavras = cria_lista_palavras(nome_arquivo)
    palavras_normalizadas = [comparar_letras(palavra) for palavra in palavras]
    
    # Sortear uma palavra da lista
    palavra_sorteada = random.choice(palavras)
    palavra_sorteada_normalizada = comparar_letras(palavra_sorteada)
    
    # Teclado inicial
    teclado = ["q w e r t y u i o p", "a s d f g h j k l ", "z x c v b n m"]
    
    # Lista de tentativas
    lista_tentativas = []
    
    # Repetir no máximo seis vezes a tarefa de solicitar uma tentativa do usuário
    for tentativa in range(6):
        print("---------------------------------------------------------------")
        print("\n".join(teclado))
        print("---------------------------------------------------------------")
        imprime_resultado(lista_tentativas)
        
        chute = input("Digite a palavra: ").strip().lower()
        chute_normalizado = comparar_letras(chute)
        
        if len(chute) != 5 or chute_normalizado not in palavras_normalizadas:
            print("Palavra inválida!")
            continue
        
        feedback = checa_tentativa(palavra_sorteada_normalizada, chute_normalizado)
        lista_tentativas.append([chute, feedback])
        
        atualiza_teclado(chute, feedback, teclado)
        
        if chute_normalizado == palavra_sorteada_normalizada:
            imprime_resultado(lista_tentativas)
            print("PARABÉNS!")
            break
    else:
        imprime_resultado(lista_tentativas)
        print(f"Você perdeu. A palavra era {palavra_sorteada}.")

if __name__ == "__main__":
    main()
