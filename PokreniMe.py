##== Filip Truntic - Diplomski rad 2025/2026. ==##

import bpy
import sys
sys.modules['SveFunkcije'] = bpy.data.texts['module_OOP.py'].as_module()
from SveFunkcije import *

from math import *
from io import *

from tokenize import tokenize, untokenize, generate_tokens



'''
Iz ove datoteke pokrece se bilokoji kod napisan u domenskom jeziku.

U RJECNIK_KLJUCNIH_RIJECI se nalazi popis definiranih kljucnih rijeci i operatora,
korisnik moze dodavati i oduzimati vlastite kljucne rijeci i operatore.
Bitno je da za svaku vlastitua kljucna rijec/operator vec postoji pandan u Pythonu.
Ovaj domenski jezik moze samo zamijeniti postojece kljucne rijeci / operatore vlastitima,
ne i definirati skroz nove kljucne rijeci.

Napomena: Pod pretpostavkom da se radi o vlastitim ključnim riječima, trenutno nije moguce pokretanje pojedinačnih naredbi u interaktivnoj konzoli.
'''




RJECNIK_KLJUCNIH_RIJECI = {
    'te'        : 'and'         , # 'i' umjesto 'and' nije bas dobar izbor
    'kao'       : 'as'          ,
    'potvrdi'   : 'assert'      ,
    'nesinkrono': 'async'       ,
    'cekaj'     : 'await'       ,
    'prekini'   : 'break'       ,
    'klasa'     : 'class'       ,
    'nastavi'   : 'continue'    ,
    'funkcija'  : 'def'         ,
    'izbrisi'   : 'del'         ,
    'inace_ako' : 'elif'        ,
    'inace'     : 'else'        ,
    'osim_ako'  : 'except'      ,
    'konacno'   : 'finally'     ,
    'za'        : 'for'         ,
    'iz'        : 'from'        ,
    'globalno'  : 'global'      ,
    'ako'       : 'if'          ,
    'uvezi'     : 'import'      ,
    'u'         : 'in'          ,
    'jest'      : 'is'          ,
    'nelokalno' : 'nonlocal'    ,
    'ne'        : 'not'         ,
    'ili'       : 'or'          ,
    'prodi'     : 'pass'        ,
    'podigni'   : 'raise'       ,
    'vrati'     : 'return'      ,    
    'pokusaj'   : 'try'         ,  
    'dok'       : 'while'       ,
    'uz'        : 'with'        ,
    'pusti'     : 'yield'       ,
    
    
    'GreskaAritmetike'  : 'ArithmeticError' ,
    'GreskaPotvrdivanja': 'AssertionError'  ,
    'GreskaAtributa'    : 'AttributeError'  ,
    'OsnovnaIznimka'    : 'BaseException'   ,
    'UlazIzlazBlokiranGreska': 'BlockingIOError'   ,
    'GreskaCjevovoda'   :'BrokenPipeError'  ,
    'GreskaBuffera'     :'BufferError'      ,
    'UpozorenjeBajtovi' :'BytesWarning'     ,
    'Iznimka'           : 'Exception'       ,
    
    'DatotekaNePostojiGreska': 'FileExistsError'    ,
    'DatotekaNijePronadenaGreska':'FileNotFoundError',
    'GreskaDecimalnogBroja':'FloatingPointError'    ,
    'BuducaGreska'      : 'FutureWarning'   ,
    'IzlazGeneratora'   : 'GeneratorExit'   ,
    'GreskaUlazIlaz'    : 'IOError'         ,
    'GreskaUvoza'       : 'ImportError'     ,
    'UpozorenjeUvoza'   : 'ImportWarning'   ,
    'GreskaIndentiranja': 'IndentationError',
    'GreskaIndeksiranja': 'IndexError'      ,
    'GreskaPrekidanja'  : 'InterruptedError',
    'GreskaJestDirektorij':'IsADirectoryError',
    'GreskaKljuca'      : 'KeyError'        ,
    'PrekidTipkovnicom' : 'KeyboardInterrupt',
    'GreskaTrazenja'    : 'LookupError'     ,
    'GreskaMemorije'    : 'MemoryError'     ,
    'GreskaModulNijePronaden':'ModuleNotFoundError',
    'GreskaImena'       : 'NameError'       ,

    'GreskaNijeDirektorij'      : 'NotADirectoryError'  ,
    'NijeImplementirano'        : 'NotImplemented'      ,
    'GreskaNijeImplementirano'  : 'NotImplementedError' ,
    'GreskaOperativnogSustava'  : 'OSError'             ,
    'GreskaPrelijevanja'        : 'OverflowError'       ,
    'GreskaDopustenja'          : 'PermissionError'     ,
    'GreskaTrazenjaProcesa'     : 'ProcessLookupError'  ,
    'GreskaRekurzije'           : 'RecursionError'      ,
    'GreskaReferenciranja'      : 'ReferenceError'      ,
    'UpozorenjeResursa'         : 'ResourceWarning'     ,
    'GreskaPrilikomIzvodenja'   : 'RuntimeError'        ,
    'UpozorenjePrilikomIzvodenja':'RuntimeWarning'      ,
    'ZaustaviAsinkronuOperaciju': 'StopAsyncIteration'  ,
    'ZaustaviIteraciju'         : 'StopIteration'       ,
    'GreskaSintakse'            : 'SyntaxError'         ,
    'UpozorenjeSintakse'        : 'SyntaxWarning'       ,
    'GreskaSustava'             : 'SystemError'         ,
    'IzlazIzSustava'            : 'SystemExit'          ,
    'GreskaTabulatora'          : 'TabError'            ,
    'GreskaIstekaVremena'       : 'TimeoutError'        ,
    
    'GreskaTipa'                : 'TypeError'           ,
    'PristupanjeLokalnojVarijabliIzvanScopea': 'UnboundLocalError',
    'GreskaDekodiranjaUnicodea' : 'UnicodeDecodeError'  ,
    'GreskaKodiranjaUnicodea'   : 'UnicodeEncodeError'  ,
    'GreskaUnicodea'            : 'UnicodeError'        ,
    'GreskaPrevodenjaUnicodea'  : 'UnicodeTranslateError',
    'UpozorenjeUnicodea'        : 'UnicodeWarning'      ,
    'UpozorenjeKorisniku'       : 'UserWarning'         ,
    'GreskaVrijednosti'         : 'ValueError'          ,
    'Upozorenje'                : 'Warning'             ,
    'GreskaWindowsa'            : 'WindowsError'        ,
    'GreskaDjeljenjaSNulom'     : 'ZeroDivisionError'   ,
    
    
    'apsolutna_vrijednost'  : 'abs' ,
    'sve'                   : 'all' ,
    'bilokoji'              : 'any' ,
    'poljebajtova'          : 'bytearray'   ,
    'bajtovi'               : 'bytes',
    'mozesepozivati'        : 'callable',
    'metodaklase'           : 'classmethod',
    'kompajliraj'           : 'compile' ,
    'slozeno'               : 'complex' ,
    'autorska_prava'        : 'copyright',
    'zasluge'               : 'credits' ,
    'izbrisiatribut'        : 'delattr' ,
    'rjecnik'               : 'dict'    ,
    'direktorij'            : 'dir'     ,
    'ostatakdjeljenja'      : 'divmod'  ,
    'enumeriraj'            : 'enumerate',
    'evaluiraj'             : 'eval'    ,
    'izvrsi'                : 'exec'    ,
    'izadi'                 : 'exit'    ,
    'filtriraj'             : 'filter'  ,
    'decimalni_broj'        : 'float'   ,
    'formatiraj'            : 'format'  ,
    'zamrznutiskup'         : 'frozenset',
    'dohvatiatribut'        : 'getattr' ,
    'globalne_funkcije'     : 'globals' ,
    'imaatribut'            : 'hasattr' ,
    'pomoc'                 : 'help'    ,
    'heksadecimalni_broj'   : 'hex'     ,
    'ulaz'                  : 'input'   ,
    'cijeli_broj'           : 'int'     ,
    'jeliprimjerak'         : 'isinstance',
    'jelipotklasa'          : 'issubclass',
    'duljina'               : 'len'     ,
    'licenca'               : 'license' ,
    'lista'                 : 'list'    ,
    'lokalne_varijable'     : 'locals'  ,
    'preslikaj'             : 'map'     ,
    'najveci'               : 'max'     ,
    'pregledmemorije'       : 'memoryview',
    'najmanji'              : 'min'     ,
    'sljedeci'              : 'next'    ,
    'oktalni_broj'          : 'oct'     ,
    'otvori'                : 'open'    ,
    'potenciraj'            : 'pow'     ,
    'ispisi'                : 'print'   ,
    'svojstvo'              : 'property',
    'napusti'               : 'quit'    ,
    'raspon'                : 'range'   ,
    'obrnuto'               : 'reversed',
    'zaokruzi'              : 'round'   ,
    'skup'                  : 'set'     ,
    'postaviatribut'        : 'setattr' ,
    'sortiraj'              : 'sort'    ,
    'staticnametoda'        :'staticmethod',
    'zbroj'                 : 'sum'     ,
    'iznad'                 : 'super'   ,
    'tip'                   : 'type'    ,
    'varijable'             : 'vars'    ,
    
    
    
    'Da'                : 'True',
    'Ne'                : 'False',
    'Nista'             : 'None',
    
    'je_jednako'        : '=='  ,
    'nije_jednako'      : '!='  ,
    'vece_od'           : '>'   ,
    'vece_ili_jednako'  : '>='  ,
    'manje_od'          : '<'   ,
    'manje_ili_jednako' : '<='  ,

    
    'svoj'              : 'self'        ,
    'konstruktor'       : '__init__'    ,
    'ispisna_vrijednost': '__repr__'    ,
}





ImeTekstualnogBloka = 'KOD'



def PrevediIIzvrsiKodIzDatoteke(arg):
    
    tekst_cijeli = bpy.data.texts[arg].as_string()

    with StringIO(tekst_cijeli) as src:
        tokens = []
        
        for token in generate_tokens(src.readline):
            if token.string in RJECNIK_KLJUCNIH_RIJECI:
                t = (token.type, RJECNIK_KLJUCNIH_RIJECI[token.string])
            else:
                t = (token.type, token.string)
        
            tokens.append(t)
    
    code = untokenize(tokens)
    exec(code)



PrevediIIzvrsiKodIzDatoteke(ImeTekstualnogBloka)