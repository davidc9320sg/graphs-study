# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes


class Node:
    def __init__(self, parents = (), children = (), name=''):
        self.parents = parents
        self.children = children
        self.name = name

    def add_parents(self, new_nodes: list):
        for n in new_nodes:
            # check if already present
            if n not in self.parents:
                self.parents = (*self.parents, n)
                # add self to other node
                if self not in n.children:
                    n.add_children([self])
            else:
                # output message
                raise Warning('node {} is already a parent of {}'.format(n.name, self.name))

    def add_children(self, new_nodes: list):
        for n in new_nodes:
            # check if already present
            if n not in self.children:
                self.children = (*self.children, n)
                # add self to other node
                if self not in n.parents:
                    n.add_parents([self])
            else:
                # output message
                raise Warning('node {} is already a child of {}'.format(n.name, self.name))

    def __repr__(self):
        parents = ','.join([n.name for n in self.parents])
        children = ','.join([n.name for n in self.children])
        return '{}|Pa:{{{}}}|Ch:{{{}}}'.format(self.name, parents, children)


def reachable(X: Node, Z: [Node, ]):
    FROM_TOP = 'from-top'
    FROM_BOTTOM = 'from-bottom'
    print('REACHABLE'.center(15))
    print('phase 1'.center(15, '+'))
    # Phase 1: insert all ancestors of Z into A ------
    L = [n for n in Z ]   # nodes to be visited
    A = []  # ancestors of Z
    while len(L) > 0:
        Y = L[0]
        L.remove(Y)
        if Y not in A:
            L = [*L, *Y.parents]
        A = [*A, Y]
    print('ancestors'.center(15, '-'))
    [print('{}'.format(n)) for n in A]
    # Phase 2: traverse active trails from X ---------
    print('phase 2'.center(15, '+'))
    # note: 0 = traverse down, 1 = traverse up
    L = [(X, FROM_BOTTOM)]    # (node, direction) to be visited
    V = []  # (node, direction) marked as visited
    R = []  # nodes reachable by active trail
    while len(L) > 0:
        # select some Y, d from L
        choice = L[0]
        Y = choice[0]   # node
        d = choice[1]   # direction
        L.remove(choice)
        not_visited = choice not in V
        print('(Y, d) = ({}, {}) | visited = {}'.format(Y.name, d, not not_visited))
        if not_visited:
            if Y not in Z:
                R = [*R, Y] # Y is reachable
            V = [*V, choice]    # mark (Y, d) as visited
            if d == FROM_BOTTOM and Y not in Z:
                # trail up through Y active if Y not in Z
                for z in Y.parents:
                    L = [*L, (z, FROM_BOTTOM)] # parents to be visited from bottom
                for z in Y.children:
                    L = [*L, (z, FROM_TOP)]   # children to be visited from top
            elif d == FROM_TOP:
                # trails down through Y
                if Y not in Z:
                    # downwards trails to Y's children are active
                    for z in Y.children:
                        L = [*L, (z, FROM_TOP)] # children to be visited from top
                if Y in A:
                    for z in Y.parents:
                        L = [*L, (z, FROM_BOTTOM)]
    print('solution'.center(15, '+'))
    for n in R:
        print(n.name)
    return R




if __name__ == '__main__':
    a = Node(name='A')
    b = Node(name='B')
    c = Node(name='C')
    d = Node(name='D')

    a.add_children([b, d])
    c.add_parents([b, d])

    graph = Graph([a, b, c, d])

    R = reachable(b, [c])