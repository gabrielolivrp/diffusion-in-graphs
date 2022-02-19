class Graph:
    def __init__(self):
        # Dígrafo no formato de matriz binária
        self.__graph = None
        # Quantidade de relacionamento
        self.__edge = 0
        self.__size = 0

    def load(self, filename):
        try:
            file = open(filename, 'r')
            content = file.readlines()
            for line in content:  # Percorrendo cada linha do arquivo
                line = line.split(' ')
                # Caso o primeiro caracter for igual a 'c' então é uma linha de comentário e não precisa ser tratada
                if line[0] == 'c':
                    continue
                # Linha que indica o tamanho do dígrafo é o número de relacionamentos
                elif line[0] == 'p':
                    self.__size = int(line[2])
                    self.__edge = int(line[3])
                    self.__graph = self.__create_matrix(self.__size)
                elif line[0] == 'e':  # Nós que se relaciona
                    self.add_edge(int(line[1]) - 1, int(line[2]) - 1)

                file.close()
        except Exception as e:
            raise e

    def node_src(self):
        """
        Retorna todos os nós fontes do dígrafo, sendo aqueles nós que se relaciona com outros,
        mas nenhum se relaciona com ele.

        Conjunto de retorno:
            Ex: [{
                'node': <número do nó>,
                'degree': <seu grau>,
                'node_achieved': <nós alcançados pela transitividade>,
                'node_achieved_len': <quantidade de nós alcançado>
            }]
        """
        src = []
        for x in range(self.__size):
            lin, col = 0, 0

            # Para ser um nó fonte esta variavel 'col' deve ser igual a 0, pois nenhum nó se relaciona com ela
            for i in range(self.__size):
                col += self.__graph[i][x]
                lin += self.__graph[x][i]

            if col == 0:
                src.append({
                    'node': x, 
                    'degree': lin,
                    'node_achieved': [], 
                    'node_achieved_len': 0
                })

        return src

    def src_with_node_achieved(self):
        """
        Retorna os nós fontes e os nós que são alcançado por ele
        """
        def fw(matrix, size):
            """
            Retorna uma matriz contendo a transitividade do dígrafo
            O calculo da transitividade está sendo calculado com base no algoritmo de Warshall
            """
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        if matrix[x][y] and matrix[y][z]:
                            matrix[x][z] = 1
            return matrix

        # Tamanho do dígrafo
        size = self.size()
        # Nós fontes
        node_src = self.node_src()
        # Transitividade do dígrafo
        transitivity = fw(self.to_matrix(), self.size())

        x = 0  # Posição do nó
        for node in node_src:  # Percorre todos os nós fontes
            for y in range(size):  # Um for do tamanho do dígrafo
                if transitivity[node['node']][y]:  # Verifica se possui uma relação
                    # Coloca no conjunto de nós alcançado
                    node_src[x]['node_achieved'].append(y)
                    node_src[x]['node_achieved_len'] += 1

            # Coloca no conjunto de nós alcançado
            node_src[x]['node_achieved'].append(node_src[x]['node'])
            node_src[x]['node_achieved_len'] += 1
            x += 1

        return node_src


    def add_edge(self, x, y):
        self.__graph[x][y] = 1

    def edge(self, x, y):
        return bool(self.__graph[x][y])

    def size(self):
        return self.__size

    def len_arcs(self):
        return self.__edge

    def to_matrix(self):
        graph = self.__create_matrix(self.__size)
        for x in range(self.__size):
            for y in range(self.__size):
                graph[x][y] = self.__graph[x][y]
        return graph

    @staticmethod
    def __create_matrix(size):
        return [[0 for x in range(size)] for y in range(size)]

    def __str__(self):
        s = ''
        for line in self.__graph:
            s += '[' + ', '.join(map(str, line)) + ']\n'
        return s
