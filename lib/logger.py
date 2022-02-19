BASE_PATH = './logs/'


def log(graph, solutions, nodesetachieved, arguments):
    make_file_dot(graph, solutions, nodesetachieved, arguments)
    make_file_log(graph, solutions, arguments)


def make_file_dot(graph, solutions, nodesetachieved, arguments):
    node_src = [solution['node'] for solution in solutions]
    len_g = graph.size()

    header, body = '', ''
    for x in range(len_g):
        header += '	' + str(x + 1)
        if x in node_src:
            header += ' [fillcolor=yellow, style=filled]'
        elif x in nodesetachieved:
            header += ' [color=red]'
        else:
            header += ' [color=black]'
        header += ';\n'

        # Gera os relacionamentos
        for y in range(len_g):
            if graph.edge(x, y):
                body += f'	{x + 1} -> {y + 1}'
                if y in nodesetachieved and (x in nodesetachieved or x in node_src):
                    body += ' [color=red]'
                body += ';\n'

    content = f'# Dígrafo: {arguments.input}\n' + \
        'digraph {\n' + header + body + '}'

    file = open(f'{BASE_PATH}{arguments.output}.dot', 'w')
    file.write(content)
    file.close()


def make_file_log(graph, solution, arguments):
    file = open(f'{BASE_PATH}{arguments.output}.log', 'a+')
    file.writelines(
        f'{arguments.input} {graph.size()} {graph.len_arcs()} {arguments.seed} {arguments.method} {len(solution)}\n'
    )
    file.close()
