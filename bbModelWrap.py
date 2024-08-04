import numpy as np
import platform as pf
from ctypes import *

lib_name = "./lib/libBBnetworkModel"
platform_name = pf.system()
lib_n_full = False

if platform_name == "Windows":
    lib_name += "Windows.dll"
    lib_n_full = True
elif platform_name == "Linux":
    lib_name += "Linux.so"
    lib_n_full = True
elif platform_name == "Darwin":
    print("Valitettavasti Apple laitteet eivät ole tuettuja. Ja kirjastoa ei voitu ladata.")
    print("Capitalist production, therefore, develops technology, and the combining together of various processes into a social whole,\nonly by sapping the original sources of all wealth-the soil and the labourer.")
    print("-Karl Marx")

if lib_n_full:
    bb_lib = CDLL(lib_name)
    bb_lib.generateBianconiBarabasiPy.restype = None
    bb_lib.generateBianconiBarabasiPy.argtypes = (c_int32, c_int32, c_char_p, c_double, POINTER(c_int32), POINTER(c_int32), POINTER(c_double))

def generateBianconiBarabasi(v_amount:int, e_amount:int, beta_constant:float, distr_type:str) -> tuple[dict, list]:
    edges_in_total = (10 + (v_amount-10)*e_amount)
    edge_array_c_1 = (c_int32 * (edges_in_total) )() # C tyyppinen yksiuloitteinen array, joka sisältää suorien ensimmäisen pään omaavan solmun nimen
    edge_array_c_2 = (c_int32 * (edges_in_total) )() # C tyyppinen yksiuloitteinen array, joka sisältää suorien toisen pään omaavan solmun nimen
    fit_array_c = (c_double * (v_amount) )() # C tyyppinen yksiuloitteinen array, joka listaa solmua vastaavan laadun ("fitness"), solmut nimetään indeksin mukaan, joka myös kertoo sen luonti ajan
    
    c_str_arg = distr_type.encode('utf-8')
    # tämä funktio kutsuu C++ koodia jolle on kirjoitettu ulospäin näkyvä C tyylinen API, koodi täyttää yllä määritetyt arrayt numeerisesti simuloidun Bianconi-Barabasi mallin tiedoilla
    bb_lib.generateBianconiBarabasiPy(v_amount, e_amount, c_str_arg, beta_constant, edge_array_c_1, edge_array_c_2, fit_array_c)
 
    # luetaan C luvut numpy arrayhin jotta ne voidaan käsitellä Pythonissa
    edge_arr_py1 = np.ndarray((edges_in_total, ), 'i', edge_array_c_1, order='C')
    edge_arr_py2 = np.ndarray((edges_in_total, ), 'i', edge_array_c_2, order='C')
    vertex_arr_py = np.ndarray((v_amount, ), 'd', fit_array_c, order='C')
    # yhdistetään verkoston suorien päät siten, että networkx pystyy ne lukemaan
    edge_arr_combined = np.column_stack((edge_arr_py1, edge_arr_py2)) # np.array() yhdistää suorien päiden tiedot kaksi riviseksi matriisiksi, .T transponoi matriisin siten, että jokainen suora on matriisissa parina
    # edge_arr_combined = np.array((edge_arr_py1, edge_arr_py2)).T
    edge_list = edge_arr_combined.tolist()

    # muutetaan solmujen array dict muotoon siten, että jokaisen solmun avain on sen nimi (indeksi)
    vertex_fit_dict = dict(enumerate(vertex_arr_py))

    del edge_array_c_1
    del edge_array_c_2
    del fit_array_c
    del edge_arr_combined
    del vertex_arr_py

    # palautetaan simuloidun verkoston tiedot
    return vertex_fit_dict, edge_list
