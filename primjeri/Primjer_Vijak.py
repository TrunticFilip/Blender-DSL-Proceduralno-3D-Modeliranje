# =========================================================
# PUNI M6 VIJAK S HELIKALNIM NAVOJEM
# =========================================================

PI = 3.141592653589793
TWO_PI = 6.283185307179586

pitch = 1.0
around = 36
axialPerPitch = 12

boltLength = 25.0

boltMajorR = 3.0
boltMinorR = 2.45
boltDepth = boltMajorR-boltMinorR



# ---------------------------------------------------------
# PUNA JEZGRA
# ---------------------------------------------------------
SviObjekti = []

Jezgra  = StvoriPrazanObjekt(pozicija = (0,0,0), rotacija = (0,0,0))
SviObjekti.append(Jezgra)
Valjak_Iscrtavanje(Jezgra, boltMinorR, boltLength, 48)


# ---------------------------------------------------------
# HELIKALNI NAVOJ
# ---------------------------------------------------------

bolt_thread = StvoriPrazanObjekt(pozicija = (0,0,0), rotacija = (0,0,0))
SviObjekti.append(bolt_thread)


boltAxial = 25*axialPerPitch

ListaEdgeLoopova = []

za iy u raspon(0, boltAxial):

    y = iy/axialPerPitch

    EdgeLoop_Y = []

    za ia u raspon(0, around): # originalno around - 1
        angle = ia*TWO_PI/around
        phase = TWO_PI*y/pitch-angle
        wave = 0.5+0.5*cos(phase)
        rr = boltMinorR+boltDepth*wave

        x = cos(angle)*rr
        z = sin(angle)*rr

        #vertex bolt_thread b_${iy}_${ia} x y z
        #ime_ovo = 'b_' + str(iy) + '_' + str(ia)
        tocka_nova = StvoriTocku(bolt_thread, (x,y,z) )
        EdgeLoop_Y.append(tocka_nova)
        
        
        '''
        if ia == 0:
            tocka_najdonja = tocka_nova
        
        if ia > 0:
            StvoriRub(bolt_thread, tocka_zadnja, tocka_nova)
            tocka_zadnja = tocka_nova
        '''

    
    ListaEdgeLoopova.append(EdgeLoop_Y)




# ---------------------------------------------------------
# FACEOVI NAVOJA
# ---------------------------------------------------------

BrojEdgeloopova = duljina(ListaEdgeLoopova)
za i u raspon(0, BrojEdgeloopova - 1 ): # i ide po ListaEdgeLoopova, svaki i je [...]
    BrojTocaka = duljina(ListaEdgeLoopova[i]) # broj tocaka u cijelom edge loopu
    
    za j u raspon(0, BrojTocaka ): #j ide po edgeloopovima, svaki j je pojedinacna tocka
        
        
        #if j == BrojEdgeloopova - 1:

        tocka_DoljeLijevo   = ListaEdgeLoopova[(i)      ][(j) % BrojTocaka]
        tocka_DoljeDesno    = ListaEdgeLoopova[(i+1)    ][(j) % BrojTocaka]
        tocka_GoreDesno     = ListaEdgeLoopova[(i+1)    ][(j+1)% BrojTocaka]
        tocka_GoreLijevo    = ListaEdgeLoopova[(i)      ][(j+1)% BrojTocaka]
    
        #tocka_DoljeLijevo   = ListaEdgeLoopova[(i)      % BrojEdgeloopova][ (j)      % BrojTocaka ]
        #tocka_DoljeDesno    = ListaEdgeLoopova[(i+1)    % BrojEdgeloopova][ (j)      % BrojTocaka ]
        #tocka_GoreDesno     = ListaEdgeLoopova[(i+1)    % BrojEdgeloopova][ (j+1)    % BrojTocaka ]
        #tocka_GoreLijevo    = ListaEdgeLoopova[(i)      % BrojEdgeloopova][ (j+1)    % BrojTocaka ]
        
        StvoriPlohu(bolt_thread,
            tocka_DoljeLijevo,
            tocka_DoljeDesno,
            tocka_GoreDesno,
            tocka_GoreLijevo
        )




# ---------------------------------------------------------
# GLAVA VIJKA
# M6 ključ 10 mm
# ---------------------------------------------------------
headRadius = 5.7735
headHeight = 4.0

#cylinder bolt_head headRadius headHeight 6
#position bolt_head 0 -headHeight/2 0


Glava   = StvoriPrazanObjekt(pozicija = (0,0,0), rotacija = (0,0,0))
SviObjekti.append(Glava)
Valjak_Iscrtavanje(Glava, headRadius, headHeight, 6)



za obj u SviObjekti:
    IzvediPromjene(obj)


Rotacija_Apsolutna(bolt_thread, (90,0,0))

dimenzija_jezgra_z = DohvatiDimenzije(Jezgra)[2]

CentrirajObjektPoPovrsini(Glava)
CentrirajObjektPoPovrsini(Jezgra)

Pozicija( Glava, (0,0,0))
Pozicija( Jezgra, (0,0, dimenzija_jezgra_z / 2))


### ===
### B
### ===



'''
#TrenutniRub_DonjaTocka  = a.StvoriTocku((0, 0, 0))
#TrenutniRub_GornjaTocka = a.StvoriTocku((0, 0, Visina))
#TrenutniRub             = a.StvoriRub(TrenutniRub_DonjaTocka, TrenutniRub_GornjaTocka)



z = a.StvoriTocku("C", (0, 1, 1))
w = a.StvoriTocku("D", (0, 1, 0))

#print("je li x dobro dohvaca tocku: " + str(a.DohvatiTocku("A") == x))

h = a.StvoriRub("H",x,y)
g = a.StvoriRub("G",z,w)
p = a.StvoriPlohu("a", x,y,z,w)

#a.EkstrudirajTocku(a.DohvatiTocku("A"), "B", (0,0,3))
#a.EkstrudirajTocku(a.DohvatiTocku("B"), "C", (3,0,3))

t = a.EkstrudirajRub(h, "T", (2,2,0))

v = a.DohvatiRub("T")
print("je li v dobro dohvaca tocku: " + str(a.DohvatiRub("T") == v))
'''
