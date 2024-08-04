import numpy as np
import platform as pf
from ctypes import *

lib_name = "./lib/bbModel"
platform_name = pf.system()
lib_n_full = False

if platform_name == "Windows":
    lib_name += "Win.dll"
    lib_n_full = True
elif platform_name == "Linux":
    lib_name += "Linux.so"
    lib_n_full = True
elif platform_name == "Darwin":
    print("Valitettavasti Apple laitteet eivät ole tuettuja. Ja kirjastoa ei voitu ladata.")
    print("Capitalist production, therefore, develops technology, and the combining together of various processes into a social whole,\nonly by sapping the original sources of all wealth-the soil and the labourer.")
    print("-Karl Marx")

if lib_n_full:
    bb_lib = cdll.LoadLibrary(lib_name)

def generateBianconiBarabasi(v_amount:int, e_amount:int, beta_constant:float, distr_type:str):
    edge_array_c = (c_int * (v_amount*v_amount)) # C tyyppinen yksiuloitteinen array, joka mallintaa verkoston vierekkyys matriisia
    fit_array_c = (c_longdouble * (v_amount)) # C tyyppinen yksiuloitteinen array, joka listaa solmut ja niiden laadun ("fitness")
    