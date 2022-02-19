import random
import argparse
from lib.graph import Graph
from lib.logger import log


def remove_duplicate_elements(_set):
    return list(set(_set))


def order_nodes(_set):
    return sorted(_set, key=lambda node: node['node_achieved_len'], reverse=True)


def union_len(_set, node2):
    return len(remove_duplicate_elements(_set + node2))

def random_solution(graph, n_porce):
    node_src = graph.src_with_node_achieved()  # Nós fontes
    node_len = len(node_src)                  # Quantidade de nós fontes

    # list_node_solution   => Conjunto com todos os nós fontes que serão util
    # node_set_achieved  => Conjunto de todos os nós já atigindos
    list_node_solution, node_set_achieved = [], []

    v = 0  # Total de vezes que o loop rodou
    # Enquanto a quantidade de nós não for atingida ele ira sortear outros nós fontes
    while len(node_set_achieved) < n_porce:
        # Verifica se já sorteou todos os nós fontes,
        # caso seja verdade e não tiver encontrado uma solução ele retorna nulo
        if v >= node_len:
            return None, None

        node = random.choice(node_src)  # Sortear outro no fonte
        # Cardinalidade da união do conjunto de nós já atigindos
        count = union_len(node_set_achieved, node['node_achieved'])
        if count > len(node_set_achieved):  # Verifica se os nós já foram atingido
            node_set_achieved = remove_duplicate_elements(
                node_set_achieved + node['node_achieved'])
            list_node_solution.append(node)
        # Remove da lista de nós fontes para não ser sorteado novamente
        node_src.remove(node)
        v += 1

    return list_node_solution, node_set_achieved


def greedy_solution(graph, n_porce):
    node_src = order_nodes(graph.src_with_node_achieved())

    # list_node_solution  => Conjunto com todos os nós que serão util
    # node_set_achieved => Conjunto de todos os nós que são atingido
    list_node_solution, node_set_achieved = [], []

    # Nó com maior percentual de alcance
    node_set_achieved = remove_duplicate_elements(
        node_set_achieved + node_src[0]['node_achieved'])
    list_node_solution.append(node_src[0])

    count = 0
    # Verificação para saber se ele já cobre a quantidade necessaria
    if node_src[0]['node_achieved_len'] >= n_porce:
        return list_node_solution, node_set_achieved
    else:
        for node in node_src[1::]:  # Percorre todo o conjunto de nós fontes pulando o primeiro indice

            # Tamanho da união do conjunto de nós atingido com os atigindos pelo nó src
            # Caso a cardinalidade da união for menor ou igual a cardinalidade do conjunto solução
            # então todos os nós atingidos são os mesmos
            count = union_len(node_set_achieved, node['node_achieved'])
            if count > len(node_set_achieved):  # Verifica se os nós já foram atingido
                node_set_achieved = remove_duplicate_elements(
                    node_set_achieved + node['node_achieved'])  # Elimina os elementos duplicado
                list_node_solution.append(node)
                if count >= n_porce:  # Verifica se já alcançou a meta
                    break

        if count >= n_porce:  # Caso tenha chegado na meta retorna os nós que serão utilizado
            return list_node_solution, node_set_achieved
        else:  # Caso contrario retorna nulo
            return None, None


def solver(arguments):
    # Sementa para geração de números aleatórios
    random.seed(arguments.seed)

    # Instância do dígrafo
    graph = Graph()

    # Carregamento do arquivo para o formato de matriz binária
    graph.load(arguments.input)

    # Número de nós que deverá ser atingido
    n_porce = int((graph.size() * arguments.percentage) / 100)

    solutions, node_set_achieved = None, []
    if arguments.method.lower() == 'g':
        solutions, node_set_achieved = greedy_solution(graph, n_porce)
    elif arguments.method.lower() == 'a':
        solutions, node_set_achieved = random_solution(graph, n_porce)
    else:
        print('Error: Método de solução inválida')
        exit(1)
    # Caso tenha encontrado alguma solução então ele gera os arquivos de logs
    if solutions and node_set_achieved:
        log(graph, solutions, node_set_achieved, arguments)

        print('**Melhor Solução**')
        print('Nós fontes que deveram ser utilizado: ', end='')
        for solution in solutions:
            print(f'{solution["node"] + 1} ', end=' ')
    else:  # Mostra que não achou uma solução para a porcentagem encontrada
        print('Não existe nós suficientes para cobrir esta porcentagem\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Problema da Mínima Difusão Parcial em Grafos Direcionados'
    )
    parser.add_argument(
        'seed',
        help='Valor inteiro de semente informada pelo usuário que será usada para inicializar o gerador de números aleatórios', 
        type=int
    )
    parser.add_argument(
        'percentage',
        help='Valor correspondente à p-difusão alvo, ou seja, qual é o valor percentual p de nós que devem ser atingidos na rede para considerar a difusão bem sucedida',
        type=int
    )
    parser.add_argument(
        'method',
        help='Letra que indica qual método utilizar: \'g\' para algoritmo guloso, \'a\' para método aleatório'
    )
    parser.add_argument(
        'input',
        help='Nome do arquivo de que contem a descrição de um grafo no formato ASCII DIMACS'
    )
    parser.add_argument(
        'output',
        help='Nome do arquivo de saída gerado automaticamente pelo aplicativo e que contêm o log dos calculos realizados'
    )

    solver(parser.parse_args())
