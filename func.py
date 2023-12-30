import re
import sys

from AutomatFinit import AutomatFinit
from hashTable import HashTable
from hashTableLL import HashTableLL

separators = [';', ',', '{', '}', '(', ')', "\"", "<<", ">>"]
operators = ['=', '-', '+', '*', '/', '%', '==', '!=', '<', '<=', '>', '>=', '&&', '||', '&', '|']
keywords = ['for', 'while', 'if', 'do', 'using', 'namespace', 'std', 'return', '#include', 'int', 'float', 'om', 'cin', 'cout', 'iostream', 'main']
# identifiers = r"[a-zA-Z]+"
# constant_regex = {"numar_real_sau_intreg" : r"[+-]?\d+(\.\d+)?([eE][+-]?\d+)?",
#                   "numar_binar" : r"0b[01]+",
#                   "numar_hexa" : r"0x[0-9abcdefABCDEF]+",
#                   "numar_octal" : r"0[0-7]+",
#                   "caracter" : r"'[a-zA-Z0-9_ ]?'"
#                   }
comparison_begin = ['!', '=', '>', '<']

def citeste_automat(file_name):
    with open(file_name, 'r') as file:
        i = 0
        muchii = []
        for line in file:
            if i == 0:
                stari = line.strip("\n").split(",")
            elif i == 1:
                alfabet = line.strip("\n").split(",")
            elif i == 2:
                start = line.strip("\n")
            elif i == 3:
                stari_finale = line.strip("\n").split(",")
            else:
                val = line.strip("\n").split("->")
                val[1] = val[1].split(",")
                muchii.append(val)
            i+=1
        return AutomatFinit(stari, alfabet, start, stari_finale, muchii)

automat_char = citeste_automat(".\\automate\\caracter.txt")
automat_int = citeste_automat(".\\automate\\constante_intregi.txt")
automat_float = citeste_automat(".\\automate\\constante_reale.txt")
automat_id = citeste_automat(".\\automate\\identificatori.txt")
automat_char.creeaza_lista_adj()
automat_int.creeaza_lista_adj()
automat_float.creeaza_lista_adj()
automat_id.creeaza_lista_adj()
lista_automate_const = [automat_char, automat_float, automat_int]

"""
returneaza o lista de perechi ce definesc fisierul intern al MLP
"""
def extrage_fisier_intern(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()

    # print(file_content)
    internal_file_content = file_content.split("\n")
    actual_content = {}
    for elem in internal_file_content:
        elems = elem.split(" ")
        actual_content[elems[1]] = elems[0]

    # for elem, val in actual_content.items():
    #     print(elem, val)

    return actual_content

def extrage_fisier_intern_invers(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()

    # print(file_content)
    internal_file_content = file_content.split("\n")
    actual_content = {}
    for elem in internal_file_content:
        elems = elem.split(" ")
        actual_content[elems[0]] = elems[1]

    # for elem, val in actual_content.items():
    #     print(elem, val)

    return actual_content


def create_output_string(inverted_internal_map, FIP):
    s = ""
    for entry in FIP:
        s += inverted_internal_map[str(entry[0])]

    return s
"""
clasifica un atom in ID, CONST sau KEYWORD si verifica daca acesta este scris conform regulilor MLP, alfel arunca eroare
"""
def clasifica_atom(atom, lista_atomi, TS, FIP, internal_file, line=0):
    ok = 0
    if atom:
        if keywords.__contains__(atom):
            lista_atomi.append([atom, "KEYWORD"])
            FIP.append([internal_file[atom], "NONE"])
            ok = 1
        else:
            # PARTEA PENTRU TESTAT CONSTANTE
            for automat in lista_automate_const:
                ret_val = automat.testeaza_atom(atom)
                if ret_val == atom:
                    lista_atomi.append([atom, "CONSTANT"])
                    ts_index = TS.find(atom)
                    if ts_index is None:
                        ts_index = TS.add(atom)
                    FIP.append([1, ts_index])
                    ok = 1
                    break

            ret_val = automat_id.testeaza_atom(atom)
            if ret_val == atom:
                lista_atomi.append([atom, "IDENTIFIER"])
                ts_index = TS.find(atom)
                if ts_index is None:
                    ts_index = TS.add(atom)
                FIP.append([0, ts_index])
                ok = 1

        if ok == 0 and atom != " ":
            print("\033[91m ERORARE lexicala la atomul : [" + atom + "] pe linia " + str(line) + " : ATOMUL NU RESPECTA REGULILE DE DEFINIRE MLP \033[0m")
            print("COD ATOM / POZITIE IN TS")
            for elem in FIP:
                print(str(elem[0]) + " / " + str(elem[1]))

            TS.prinTable()
            sys.exit()




"""
analiza lexicala completa
"""
def analiza_lexicala(file_path, internal_file_path = ".\\utils\\internal_file.txt"):

    lista_atomi = []
    internal_file = extrage_fisier_intern(internal_file_path)
    FIP = []
    initial_TS_size = 10
    TS = HashTable(initial_TS_size)
    line = 1
    with open(file_path, "r") as file:
        file_content = file.read()

    print(file_content)
    cleaned_text = file_content.replace("\t", " ")

    print(cleaned_text)
    atom = ""
    position = 0
    while position < len(cleaned_text):
        char = cleaned_text[position]

        if char == "\n":
            position += 1
            line += 1
            continue

        if comparison_begin.__contains__(char):
            if cleaned_text[position + 1] == "=":
                clasifica_atom(atom, lista_atomi, TS, FIP, internal_file, line)
                lista_atomi.append([char + cleaned_text[position + 1], "OPERATOR"])
                FIP.append([internal_file[char + cleaned_text[position + 1]], "NONE"])
                atom = ""
                position += 2
                continue

        if char == " " and atom.count("'") != 1:
            clasifica_atom(atom, lista_atomi, TS, FIP, internal_file, line)
            atom = ""
            position += 1
            continue

        if separators.__contains__(char):
            clasifica_atom(atom, lista_atomi, TS, FIP, internal_file, line)

            lista_atomi.append([char, "SEPARATOR"])
            FIP.append([internal_file[char], "NONE"])

            atom = ""
            position += 1
            continue

        if operators.__contains__(char):
            if not (char == "-" and (cleaned_text[position-1] == "E" or cleaned_text[position-1] == "e")):
                clasifica_atom(atom, lista_atomi, TS, FIP, internal_file, line)

                if char == "<" or char == ">":
                    if cleaned_text[position + 1] == char:
                        lista_atomi.append([char + char, "SEPARATOR"])
                        FIP.append([internal_file[char + char], "NONE"])
                        position += 1
                    else:
                        lista_atomi.append([char, "OPERATOR"])
                        FIP.append([internal_file[char], "NONE"])
                elif char == "&" or char == "|":
                    if cleaned_text[position + 1] == char:
                        lista_atomi.append([char + char, "OPERATOR"])
                        FIP.append([internal_file[char + char], "NONE"])
                        position += 1
                    else:
                        lista_atomi.append([char, "OPERATOR"])
                        FIP.append([internal_file[char], "NONE"])
                else:
                    lista_atomi.append([char, "OPERATOR"])
                    FIP.append([internal_file[char], "NONE"])

                atom = ""
                position += 1
                continue


        atom += char
        position += 1

    for elem in lista_atomi:
        print(elem[0] + "  " + elem[1])


    print("\n\033[92m---ALL GOOD---\033[0m")
    return lista_atomi, FIP, TS