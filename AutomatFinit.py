class AutomatFinit:
    def __init__(self, stari, alfabet, start, stari_finale, muchii):
        self.stari = stari
        self.alfabet = alfabet
        self.start = start
        self.stari_finale = stari_finale
        self.muchii = muchii
        self.lista_adj = {}

    def creeaza_lista_adj(self):
        for stare in self.stari:
            self.lista_adj[stare] = []
            for muchie in self.muchii:
                if muchie[0] == stare:
                    self.lista_adj[stare].append([muchie[1], muchie[2]])

    def verifica_determinism(self):
        current_node = self.start
        visited = {}
        for stare in self.stari:
            visited[stare] = False
        visited[current_node] = True
        queue = [current_node]
        while queue != []:
            current_node = queue.pop()
            alphabet_values = []
            for elem in self.lista_adj[current_node]:
                alphabet_values += elem[0]
                if visited[elem[1]] == False:
                    queue.append(elem[1])
                    visited[elem[1]] = True
            if len(alphabet_values) != len(set(alphabet_values)):
                return False

        return True

    def testeaza_atom(self, secventa):
        subsecventa = ""
        subsecventa_valida = None
        current_node = self.start
        i = 0
        while i < len(secventa):
            if self.stari_finale.count(current_node):
                # Am ajuns in stare finala
                subsecventa_valida = subsecventa

            not_stuck = False
            for elem in self.lista_adj[current_node]:
                if elem[0].count(secventa[i]) > 0:
                    subsecventa += secventa[i]
                    current_node = elem[1]
                    not_stuck = True
                    break

            if not_stuck is False:
                if self.stari_finale.count(current_node):
                    # Am ajuns in stare finala
                    subsecventa_valida = subsecventa
                break
            i += 1

        if i == len(secventa) and self.stari_finale.count(current_node):
            subsecventa_valida = subsecventa

        return subsecventa_valida


