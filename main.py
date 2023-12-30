from func import analiza_lexicala, extrage_fisier_intern, extrage_fisier_intern_invers, create_output_string

# lista_atomi, FIP, TS = analiza_lexicala(".\\test_files\exemplu_simplu.cpp")
lista_atomi, FIP, TS = analiza_lexicala(".\\test_files\example1.cpp")

print("COD ATOM / POZITIE IN TS")
for elem in FIP:
    print(str(elem[0]) + " / " + str(elem[1]))

TS.prinTable()

internal_map = extrage_fisier_intern_invers(".\\utils\\internal_file.txt")
s = create_output_string(internal_map, FIP)
print(s)

f = open("outputs/output_file.txt", "w")
f.write(s)
f.close()