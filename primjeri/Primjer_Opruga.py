# =========================================================
# SPRING PO PATHU
# ravna opruga + curvebend
# =========================================================

spring = StvoriPrazanObjekt(pozicija = (0,0,0), rotacija = (0,0,0))
SviObjekti = []
SviObjekti.append(spring)


turns = 10
segPerTurn = 24
majorSeg = turns*segPerTurn

springRadius = 0.45
wireRadius = 0.08
pitch = 0.35

minorSeg = 10
TWO_PI = 6.283185307179586

# ---------------------------------------------------------
# 1. RAVNA OPRUGA DUŽ X OSI
# ---------------------------------------------------------

ListaEdgeLoopova = []

za i u raspon(0, majorSeg-1):
    
    # varijabla se originalno zvala 'u',
    # ali u je vec rezervirana kljucna rijec
    # pa je preimenovana u 'u_var'
    u_var = TWO_PI*i/segPerTurn

    # napredovanje opruge duž X
    cx = pitch*u_var/TWO_PI

    # heliks oko X osi
    cy = springRadius*cos(u_var)
    cz = springRadius*sin(u_var)

    Krug = []

    za j u raspon(0, minorSeg-1):

        v = TWO_PI*j/minorSeg
        cv = cos(v)
        sv = sin(v)

        # približni lokalni presjek žice
        x = cx + wireRadius*sv
        y = cy + wireRadius*cv*cos(u_var)
        z = cz + wireRadius*cv*sin(u_var)

        #vertex spring v_${i}_${j} x y z
        tocka_nova = StvoriTocku(spring, (x,y,z))
        
        Krug.append(tocka_nova)

    ListaEdgeLoopova.append(Krug)



# ---------------------------------------------------------
# 2. FACEOVI
# ---------------------------------------------------------

BrojEdgeloopova = duljina(ListaEdgeLoopova)
za i u raspon(0, BrojEdgeloopova - 1 ): # i ide po ListaEdgeLoopova, svaki i je [...]
    #StvoriPlohu(spring, ListaEdgeLoopova[i])
    
    BrojTocaka = duljina(ListaEdgeLoopova[i]) # broj tocaka u cijelom edge loopu odnosno krugu
    
    za j u raspon(0, BrojTocaka ): #j ide po edgeloopovima, svaki j je pojedinacna tocka
        
        tocka_DoljeLijevo   = ListaEdgeLoopova[(i)      ][(j) % BrojTocaka]
        tocka_GoreLijevo    = ListaEdgeLoopova[(i+1)    ][(j) % BrojTocaka]
        tocka_GoreDesno     = ListaEdgeLoopova[(i+1)    ][(j+1)% BrojTocaka]
        tocka_DoljeDesno    = ListaEdgeLoopova[(i)      ][(j+1)% BrojTocaka]
        
        StvoriPlohu(spring,
            tocka_DoljeLijevo,
            tocka_GoreLijevo,
            tocka_GoreDesno,
            tocka_DoljeDesno
        )


# ---------------------------------------------------------
# 3. BEZIER PATH
# ---------------------------------------------------------

za obj u SviObjekti:
    IzvediPromjene(obj)

Krivulja(spring,
    (0, 0, 0)               ,
    (1.488098, 1, -5.46029) ,
    (4, 2, 1)               ,
    (6.426585, 0, 4.943438) ,
    (8, -1, 1),
    OsDeformacije = 'X',
    SkalirajKrivulju = (0.5,0.5,0.5)
)
