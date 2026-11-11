sirina = 2
visina = 1
visina_bazna = 2.5
sinusoida_slika = 0.9
N = 5





BrojIteracija = 360*N

ListaEdgeLoopova = []

# ---------------------------------------------------------
# 1. Iscrtaj tocke
# ---------------------------------------------------------
zupcanik  = StvoriPrazanObjekt()

#xs = (x * 0.1 for x in range(0, 10)) --> [0.1,0.2,...,0.9,1]
za i u (x * (pi/16) za x u raspon(0, BrojIteracija)):
    oscilator = Nista
    
    ako sin(i) >= sinusoida_slika:
        oscilator = sinusoida_slika
    inace_ako sin(i) <= - sinusoida_slika:
        oscilator = - sinusoida_slika
    inace:
        oscilator = sin(i)
    
    potvrdi oscilator nije_jednako None
    
    
    koordinate_0 = [0,       -i, 0                  ]
    koordinate_1 = [sirina,  -i, 0                  ]
    koordinate_2 = [sirina,  -i, oscilator + visina ]
    koordinate_3 = [0,       -i, oscilator + visina ]
    
    koordinate = [koordinate_0, koordinate_1, koordinate_2, koordinate_3]
    
    
    '''
    # zasada tocke napreduju samo po jednoj osi,
    # ova mala petlja svaku tocku oblikuje u krug
    za broj u koordinate:
        #broj[0] += sin(i)
        #broj[1] += cos(i)
        x = broj[0]
        y = broj[1]
        broj[0] += sqrt( abs( pow(radijus,2) - pow(y,2) ) )
        broj[1] += sqrt( abs( pow(radijus,2) - pow(x,2) ) )
    '''
    
    koordinate_2[2] += visina_bazna
    koordinate_3[2] += visina_bazna
    
    tocka_0 = StvoriTocku(zupcanik, koordinate_0)
    tocka_1 = StvoriTocku(zupcanik, koordinate_1)
    tocka_2 = StvoriTocku(zupcanik, koordinate_2)
    tocka_3 = StvoriTocku(zupcanik, koordinate_3)
    
    tocke = [tocka_0, tocka_1, tocka_2, tocka_3]

    ListaEdgeLoopova.append(tuple(tocke))


# ---------------------------------------------------------
# 2. Iscrtaj faceove
# ---------------------------------------------------------

BrojEdgeLoopova = duljina(ListaEdgeLoopova)
za i u raspon(1, BrojEdgeLoopova):
    
    BrojTocaka = duljina(ListaEdgeLoopova[i])
    za j u raspon( 0, BrojTocaka):
        StvoriPlohu(zupcanik,
            ListaEdgeLoopova[i  ][(j) % BrojTocaka  ],
            ListaEdgeLoopova[i-1][(j) % BrojTocaka  ],
            ListaEdgeLoopova[i-1][(j+1) % BrojTocaka],
            ListaEdgeLoopova[i  ][(j+1) % BrojTocaka]
        )


IzvediPromjene(zupcanik)

sirina_2 = 0.02
Kruznica(zupcanik,
    RotacijaObjekta     = (0,90,0),
    SkalirajObjekt      = (0.05,sirina_2,0.05),
    OsDeformacije       = 'Z',
)



Rotacija_Apsolutna(zupcanik, (90,0,0))


unutrasnjost  = StvoriPrazanObjekt()

Valjak_Iscrtavanje(unutrasnjost, 1, sirina, 20)
IzvediPromjene(unutrasnjost)

Rotacija_Apsolutna(unutrasnjost, (90,0,90))
CentrirajObjektPoPovrsini(unutrasnjost)
Pozicija(unutrasnjost, (sirina_2 ,0,0))
Skaliraj(unutrasnjost, (1.1,1.1,sirina_2))

rupa = StvoriPrazanObjekt()
Valjak_Iscrtavanje(rupa, 1, sirina, 20)
IzvediPromjene(rupa)

Rotacija_Apsolutna(rupa, (90,0,90))
CentrirajObjektPoPovrsini(rupa)
Pozicija(rupa, (sirina_2 ,0,0))
Skaliraj(rupa, (0.25,0.25,1))

Razlika(unutrasnjost, rupa, sacuvajTarget = Ne)




#Skaliraj(zupcanik, skala = (0.05,0.1,0.05))
#zupcanik.objekt.scale = Vector((0.05,0.1,0.05))


'''
faktor = 100
Krivulja(zupcanik,
    (faktor,0,0),
    (0,0,faktor),
    #(0,0,-faktor),
    #(0,-faktor,0),
    #SkalirajKrivulju = (3,3,3),
    UnistiKrivulju = Ne
)
'''


#for obj in SviObjekti:
#    IzvediPromjene(obj)