##== Filip Truntic - Diplomski rad 2025/2026. ==##

import bpy
import bmesh
from mathutils import *
from math import pi, floor, sin

import os
import warnings

import random
import string

from typing import Optional

##== ALIASI ==##


TOCKA   = 'VERT'
RUB     = 'EDGE'
POLIGON = 'FACE'

TOCKE       = 'VERTICES'
RUBOVI      = 'EDGES'
POLIGONI    = 'FACES'

# os_pomaka
Globalna        = 'GLOBAL'
Lokalna         = 'LOCAL'
Prema_Normali   = 'NORMAL'
Gimbalna        = 'GIMBAL'
Prema_Kameri    = 'VIEW'
Prema_Kursoru   = 'CURSOR'
Prema_Roditelju = 'PARENT'


##== KRAJ ALIASA ==##





IspisujDebugStatementove = False


'''
S obzirom da je objektno-orijentirana paradigma u pitanju, globalne funkcije ispod mogu se smatrati 'staticnima'.
'''

DULJINA_NASUMICNOG_STRINGA = 3
def NasumicniString(duljina = DULJINA_NASUMICNOG_STRINGA):
    assert type(duljina) == int
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k = duljina))
    
    return random_string


def DodijeliIme(ime):
    '''
    Ispod haube, svaki element prilikom dodavanja mora imati neko ime.
    Ako ga korisnik ne navede, dodjeljuje mu se nasumicni string duljine DULJINA_NASUMICNOG_STRINGA kao ime.
    '''
    if ime == None or ime == '':
        return NasumicniString()
    else:
        return ime



def PretvoriMjernuJedinicu(vektor, trazenaMjernaJedinica = None):
    '''
    Ovu funkciju korisnik ne bi trebao samostalno pozivati iz konzole / skripte.
    Funkcija definira rjecnik parova 'mjerna_jedinica':<faktor>, gdje faktor predstavlja broj kojim se mnozi vektor da bi se dobila fizicka velicina u trazenoj mjernoj jedinici.
    '''
    assert vektor is not None
    assert len(vektor) == 3
    assert trazenaMjernaJedinica in {'mm', 'deg', 'rad'}
    
    RjecnikMjernihJedinica = {
        'mm': 0.001,
        'rad': (180/pi),
        'deg': (pi/180)
    }
    
    vektor_lista = list(vektor)
    for i in range(0, 3):
        vektor_lista[i] *= RjecnikMjernihJedinica[trazenaMjernaJedinica]
    
    return tuple(vektor_lista)

def PretvoriUMilimetre(vektor):
    '''
    Funkcija prima troclani tuple (ili listu) u metrima i vraca isti takav tuple u milimetrima.
    '''
    return PretvoriMjernuJedinicu(vektor, 'mm')

def PretvoriUStupnjeve(vektor):
    '''
    Funkcija prima troclani tuple (ili listu) u radijanima i vraca isti takav tuple u stupnjevima.
    '''
    return PretvoriMjernuJedinicu(vektor, 'deg')


def PretvoriURadijane(vektor):
    '''
    Funkcija prima troclani tuple (ili listu) u stupnjevima i vraca isti takav tuple u radijanima.
    '''
    return PretvoriMjernuJedinicu(vektor, 'rad')


def IzracunajVector(arg_tuple):
    '''
    Iz troclanog tuplea (ili liste) funkcija stvara varijablu tipa Vector (iz mathutils modula), sto je opcenito potrebno za ispravan rad vektora u Blenderu.
    '''
    assert arg_tuple is not None
    
    # u slucaju da je korisnik slucajno unio listu umjesto tuplea
    try:
        assert type(arg_tuple) is not list
    except AssertionError:
        arg_tuple = tuple(arg_tuple)
        print("Slucajno je unesena lista umjesto tuplea, ali sam ju pretvorio u tuple")
    
    assert type(arg_tuple) is tuple
    assert len(arg_tuple) == 3
    #for i in arg_tuple:
    #    assert (type(i) in {int, float})

    return Vector(arg_tuple)


def PRIVATE_Import(arg_path, Visina = 0.01, ListaZaSelektiranje = None, operacija = None):
    rjecnik_operacija = {
        'IMPORT_STL',
        'IMPORT_SVG'
    }
    
    assert operacija != None
    assert type(operacija) == str
    assert operacija in rjecnik_operacija
    
    print("Operacija: " + str(operacija))
    
    if operacija == 'IMPORT_SVG':
        bpy.ops.import_curve.svg(filepath = arg_path)
        #print("arg_path: " + str(arg_path))
        #filename = arg_path.rpartition(r"'\'")[2]
        filename = str( os.path.split(arg_path)[-1] )
        #print("filename: " + str(filename))
        kolekcija = bpy.context.scene.collection.children[filename]
        
        # snimi stanje selekcije na svim objektima, i aktivan objekt
        Prije_SelekcijaObjekata = bpy.context.selected_objects
        Prije_AktivanObjekt = bpy.context.active_object
        
        # deselektiraj sve objekte u sceni
        for obj in bpy.context.scene.collection.all_objects:
            obj.select_set(False)
        
        # selektiraj sve krivulje navedene u ListaZaSelektiranje
        if ListaZaSelektiranje == None:
            ListaZaSelektiranje = []
        elif ListaZaSelektiranje != None and type(ListaZaSelektiranje) in {set, tuple, list}:
            for ime in ListaZaSelektiranje:
                assert type(ime) == str
        else:
            print("Nesto ne valja s listom objekata za selekciju u SVG-u")
            raise AssertionError
            
            
        bpy.context.view_layer.objects.active = kolekcija.objects[0]
        for obj in kolekcija.objects:
            obj.select_set(True)
            bpy.ops.object.convert(target = 'MESH')
            bpy.ops.object.mode_set(mode = 'EDIT')
            
            #bpy.ops.mesh.select_all(action = 'SELECT')
            #bpy.ops.mesh.select_all(action = 'TOGGLE')
            
            if obj.name in ListaZaSelektiranje:
                bpy.ops.mesh.select_all(action = 'SELECT')
            
            bpy.ops.object.mode_set(mode = 'OBJECT')
            #obj.select_set(False)
        bpy.ops.object.join()
        novi_objekt = kolekcija.objects[0]
        novi_objekt_OOP = PostojeciObjekt(novi_objekt)
        
        #SelekcijaTocaka_ListaZaSelektiranje = SelekcijaTocaka(novi_objekt_OOP)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.solidify(thickness = Visina)
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.select_all(action = 'TOGGLE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #novi_objekt_OOP.PostaviSelekcijuTocaka( SelekcijaTocaka_ListaZaSelektiranje )
        

        # vrati stanje selekcije na svim objektima
        # (prvo deselektiraj sve objekte i ponovo selektiraj ako su u Prije_SelekcijaObjekata,
        # i jos aktivan objekt)
        for obj in bpy.context.scene.collection.all_objects:
            obj.select_set(False)
        for obj in Prije_SelekcijaObjekata:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = Prije_AktivanObjekt
        
        # stavi objekt u Scene Collection i izbrisi .svg kolekciju
        bpy.context.scene.collection.objects.link(novi_objekt)
        bpy.data.collections.remove( kolekcija )
        
        return PostojeciObjekt(novi_objekt)
    
    
    Prije_AktivnaKolekcija_Layer = DohvatiAktivnuLayerKolekciju()
    
    #ukljuci privremenu kolekciju u scenu
    #privremena kolekcija je inicijalno prazna i u nju se dodaje novi objekt
    #s ciljem da bi se mogla dobiti referenca na novi objekt koji se upravo stvara
    kolekcija_temp = bpy.data.collections['kolekcija_temp']
    bpy.context.scene.collection.children.link(kolekcija_temp)
    #kolekcija_temp_layer = NadiOdgovarajucuLayerKolekciju(kolekcija_temp)
    
    #bpy.context.view_layer.active_layer_collection = kolekcija_temp_layer
    PostaviAktivnuKolekciju(kolekcija_temp)
    
    
    #obavi import
    if operacija == 'IMPORT_STL':
        bpy.ops.wm.stl_import(filepath = arg_path)
    

    #zato sto smo prije pozvali PostaviAktivnuKolekciju(kolekcija_temp), znamo da se novi objekt nalazi u 'kolekcija_temp' kolekciji
    # trazimo jedini objekt koji se nalazi u 'kolekcija_temp' kolekciji
    #povezi objekt sa Scene Collectionom i iskljuci ga iz privremene kolekcije
    novi_objekt = kolekcija_temp.objects[0]
    bpy.context.scene.collection.objects.link(novi_objekt)
    kolekcija_temp.objects.unlink(novi_objekt)
    
    
    #iskljuci privremenu kolekciju iz scene
    bpy.context.scene.collection.children.unlink(kolekcija_temp)
    
    #vrati kontekst
    PostaviAktivnuKolekciju(Prije_AktivnaKolekcija_Layer)
    
    
    return PostojeciObjekt(novi_objekt)
    
    


def Uvezi_STL(ApsolutnaPutanja = None):
    novi_objekt = PRIVATE_Import(
        arg_path = ApsolutnaPutanja,
        operacija = 'IMPORT_STL'
    )
    return novi_objekt

def Uvezi_SVG(ApsolutnaPutanja = None, Visina = 0.01, ListaZaSelektiranje = None):
    novi_objekt = PRIVATE_Import(
        arg_path = ApsolutnaPutanja,
        Visina = Visina,
        ListaZaSelektiranje = ListaZaSelektiranje,
        operacija = 'IMPORT_SVG'
    )
    return novi_objekt



def ProvjeriIspravnostUnesenihArgumenata(objekt, vektor, neSmijeBitiNula = False):
    try:
        assert objekt != None
        assert objekt.data != None
        assert bpy.context.scene.collection.objects.find(objekt.name) != -1
    except AssertionError:
        print('Nesto ne valja, uneseni objekt nije ispravan')
        return False

    try:
        assert vektor is not None
        assert type(vektor) in {list, tuple, int, float}
        for i in vektor:
            assert type(i) in {int, float}
    except AssertionError:
        print('Nesto ne valja, uneseni vektor nije ispravan')
        return False
    
    if neSmijeBitiNula == True:
        try:
            for i in vektor:
                assert i != 0
        except AssertionError:
            print("Jedna od komponenata vektora je nula, u ovom vektoru ne bi smjelo biti nula")
            return False
    
    return True




def NadiOdgovarajucuLayerKolekciju(kolekcija):
    '''
    Ova funkcija nije namijenjena za direktno pozivanje iz konzole / skripte.
    '''
    assert kolekcija is not None
    return bpy.context.view_layer.layer_collection.children[kolekcija.name]

def PostaviAktivnuKolekciju(kolekcija):
    '''
    Ova funkcija nije namijenjena za direktno pozivanje iz konzole / skripte.
    '''
    assert kolekcija is not None
    try:
        bpy.context.view_layer.active_layer_collection = kolekcija
    except TypeError:
        bpy.context.view_layer.active_layer_collection = NadiOdgovarajucuLayerKolekciju(kolekcija)
    
    return True

def DohvatiAktivnuLayerKolekciju():
    '''
    Ova funkcija nije namijenjena za direktno pozivanje iz konzole / skripte.
    '''
    return bpy.context.view_layer.active_layer_collection




def InstancirajNoviPrimitivniObjekt(GeometrijskoTijelo = None, rezolucija = 32):
    '''
    Ova funkcija nije namijenjena za direktno pozivanje iz konzole / skripte.
    '''
    
    
    assert GeometrijskoTijelo is not None
    assert GeometrijskoTijelo in {
        'KOCKA',
        'KUGLA',
        'VALJAK',
        'STOZAC',
        'KRIVULJA',
        'KRUZNICA'
    }
    
    assert type(rezolucija) is int
    assert rezolucija > 0
    
    '''
    #if rezolucija is not None:
    #    print('rezolucija: ' + str(rezolucija))
    #    print('tip varijable rezolucija: ' + str( type(rezolucija) ))
    
    '''
    
    Prije_AktivnaKolekcija_Layer = DohvatiAktivnuLayerKolekciju()
    
    #ukljuci privremenu kolekciju u scenu
    #privremena kolekcija je inicijalno prazna i u nju se dodaje novi objekt
    #s ciljem da bi se mogla dobiti referenca na novi objekt koji se upravo stvara
    kolekcija_temp = bpy.data.collections['kolekcija_temp']
    bpy.context.scene.collection.children.link(kolekcija_temp)
    #kolekcija_temp_layer = NadiOdgovarajucuLayerKolekciju(kolekcija_temp)
    
    #bpy.context.view_layer.active_layer_collection = kolekcija_temp_layer
    PostaviAktivnuKolekciju(kolekcija_temp)
    
    #obavi trazenu operaciju
    if GeometrijskoTijelo   == 'KOCKA':
        bpy.ops.mesh.primitive_cube_add()
    elif GeometrijskoTijelo == 'KUGLA':
        bpy.ops.mesh.primitive_uv_sphere_add(segments = rezolucija, ring_count = floor(rezolucija / 2) )
    elif GeometrijskoTijelo == 'VALJAK':
        bpy.ops.mesh.primitive_cylinder_add(vertices = rezolucija)
    elif GeometrijskoTijelo == 'STOZAC':
        bpy.ops.mesh.primitive_cone_add(vertices = rezolucija)
    elif GeometrijskoTijelo == 'KRIVULJA':
        bpy.ops.curve.primitive_bezier_curve_add(scale = (1,1,1))
    elif GeometrijskoTijelo == 'KRUZNICA':    
        bpy.ops.curve.primitive_bezier_circle_add(scale = (1,1,1))
    
    #zato sto smo prije pozvali PostaviAktivnuKolekciju(kolekcija_temp), znamo da se novi objekt nalazi u 'kolekcija_temp' kolekciji
    # trazimo jedini objekt koji se nalazi u 'kolekcija_temp' kolekciji
    #povezi objekt sa Scene Collectionom i iskljuci ga iz privremene kolekcije
    novi_objekt = kolekcija_temp.objects[0]
    bpy.context.scene.collection.objects.link(novi_objekt)
    kolekcija_temp.objects.unlink(novi_objekt)
    
    
    #iskljuci privremenu kolekciju iz scene
    bpy.context.scene.collection.children.unlink(kolekcija_temp)
    
    #vrati kontekst
    PostaviAktivnuKolekciju(Prije_AktivnaKolekcija_Layer)
    
    
    
    
    return novi_objekt


# ova metoda bi trebala biti staticna
# jer u sceni uvijek postoji samo jedan kursor
def ProvjeriArgument_Tuple(arg):
    assert type(arg) == tuple
    assert len(arg) == 3
    for i in range(0, len(arg)):
        assert type(arg[i]) in {int, float}
    
    return True

def ProvjeriArgument_ListaKoordinata(koordinate):
    assert koordinate is not None
    assert type(koordinate) == list
    for k in koordinate:
        assert type(k) == Vector
    
    return True


def PostaviKursor( lokacija = (0,0,0), rotacija = (0,0,0) ):
    if lokacija is None and rotacija is None:
        print('Potreban mi je barem jedan argument u ovoj funkciji')
        raise AssertionError

    if lokacija is not None and type(lokacija) != Vector:
        print('Lokacija: ' + str(lokacija) )
        assert ProvjeriArgument_Tuple(lokacija)
        bpy.context.scene.cursor.location = Vector(lokacija)
    if rotacija is not None and type(rotacija) != Vector:
        assert ProvjeriArgument_Tuple(rotacija)
        bpy.context.scene.cursor.rotation_euler = Euler( lokacija, 'XYZ' )
    return

def DohvatiKursor_Lokacija():
    return bpy.context.scene.cursor.location

def DohvatiKursor_Rotacija():
    return bpy.context.scene.cursor.rotation_euler

def PremjestiNaKursor():
    area_type = 'VIEW_3D'
    areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]

    if len(areas) <= 0:
        raise Exception(f"Nesto ne valja, treba mi barem jedan prozor tipa {area_type}.")

    with bpy.context.temp_override(
        window = bpy.context.window,
        area = areas[0],
        region = [region for region in areas[0].regions if region.type == 'WINDOW'][0],
        screen = bpy.context.window.screen
    ):
        bpy.ops.view3d.snap_selected_to_cursor(use_offset = True)





# primjer upotrebe ove Snimi i VratiSelekcijuObjekata:
# kontekst = SnimiSelekcijuObjekata()
# <neki posao koji ukljucuje promjenu selekcije objekata>
# VratiSelekcijuObjekata(kontekst)
def SnimiSelekcijuObjekata() -> dict:
    Prije_SelekcijaObjekata = bpy.context.selected_objects
    Prije_AktivanObjekt = bpy.context.active_object
    #Prije_ObjektniMod = 
    
    selekcija = {
        'Prije_SelekcijaObjekata'   : Prije_SelekcijaObjekata,
        'Prije_AktivanObjekt'       : Prije_AktivanObjekt
    }
    
    for obj in bpy.context.scene.collection.all_objects:
        obj.select_set(False)
    
    return selekcija


def VratiSelekcijuObjekata(kontekst : dict):
    for obj in bpy.context.scene.collection.all_objects:
        obj.select_set(False)
    for obj in kontekst['Prije_SelekcijaObjekata']:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = kontekst['Prije_AktivanObjekt']
    
    return True





##== sve iznad je static ==##


class Objekt:
    '''
    Ovo je 'apstraktna' klasa, koja nije namijenjena za instanciranje u programu.
    Klase koje naslijeduju ovu klasu (npr. Kocka, Stozac, Valjak, PostojeciObjekt itd.) se mogu instancirati.
    '''
    #def __init__(self, objekt):
    #    self.objekt = objekt
    
    #def __init__(self):
    #    self.objekt = InstancirajNoviPrimitivniObjekt('KOCKA')
    #    print('Izvrtio sam konstruktor')
    #    print('Ime objekta: ' + self.objekt.name)
    
    
    ## DEFAULTNI KONSTRUKTOR (ZA PRIMITIVNE OBJEKTE)
    #def PRIVATE_Konstruktor(self, dimenzije = (1,1,1), pozicija = (0,0,0), rotacija = (0,0,0), centriraj = True):
    #    self.PRIVATE_PozicionirajNoviObjekt(dimenzije, pozicija, rotacija, centriraj)
    
    def __repr__(self):
        return "Objekt (" + self.objekt.name + ")"
    
    
    def __init__(self, *args, **kwargs):
        
        #Konstruktor vraca True ako se uspjesno instanciralo, inace False
        
        try:
        
            #provjeravamo je li postoje argumenti dimenzije, pozicija, rotacija itd itd
            
            kwargs['dimenzije'           ]
            kwargs['pozicija'            ]
            kwargs['rotacija'            ]
            kwargs['centriraj'           ]
            kwargs['GeometrijskoTijelo'  ]
            kwargs['rezolucija'          ]

            if IspisujDebugStatementove == True:
                print("Usao sam u konstruktor za PRIMITIVNE objekte")
                print("Dimenzije: "             + str( kwargs['dimenzije']          ))
                print("Pozicija: "              + str( kwargs['pozicija']           ))
                print("Rotacija: "              + str( kwargs['rotacija']           ))
                print("Centriraj: "             + str( kwargs['centriraj']          ))
                print("GeometrijskoTijelo: "    + str( kwargs['GeometrijskoTijelo'] ))
                print("Rezolucija: "            + str( kwargs['rezolucija']         ))    
            
        
            assert kwargs['GeometrijskoTijelo'  ] != None
            assert kwargs['GeometrijskoTijelo'  ] in {
                'KOCKA',
                'KUGLA',
                'VALJAK',
                'STOZAC'
            }

            assert type( kwargs['rezolucija'] ) is int
            assert kwargs['rezolucija'] > 0
                    
            self.objekt = InstancirajNoviPrimitivniObjekt(
                GeometrijskoTijelo = kwargs['GeometrijskoTijelo'  ],
                rezolucija = kwargs['rezolucija']
            )
            self.PRIVATE_PozicionirajNoviObjekt(
                dimenzije   = kwargs['dimenzije'           ],
                pozicija    = kwargs['pozicija'            ],
                rotacija    = kwargs['rotacija'            ],
                centriraj   = kwargs['centriraj'           ]
            )
            
            #return True
            return
        
        except KeyError:
            try:
                # u keyword argumentima se nalazi objekt
                objekt = kwargs['objekt'              ]
                
                if IspisujDebugStatementove == True:
                    print("Usao sam u konstruktor za POSTOJECE objekte")
                
                if type( objekt ) == bpy.types.Object:
                    self.objekt = objekt
                elif type( objekt ) == Objekt:
                    self.objekt = objekt.objekt
                else:
                    raise AssertionError
            except KeyError:
                try:
                    # u argumentima se nalazi
                    assert len(args) == 1
                    objekt = args[0]
                    
                    if IspisujDebugStatementove == True:
                        print("Usao sam u konstruktor za POSTOJECE objekte (bez keyword argumenta)")
                    
                    if type( objekt ) == bpy.types.Object:
                        self.objekt = objekt
                    elif type( objekt ) == Objekt:
                        self.objekt = objekt.objekt
                    else:
                        raise AssertionError
                except KeyError:
                    print("Nesto ne valja! Ne mogu naci dobre argumente")
                    raise Exception
                except AssertionError:
                    print("Nesto ne valja! Uneseni objekt zapravo nije objekt")
                    raise Exception
            except AssertionError:
                print("Nesto ne valja! Uneseni objekt zapravo nije objekt")
                raise Exception

    
    #funkcije ispod su za extrude / programsko stvaranje geometrije
    
    
    
    '''
    def PRIVATE_EditMode_AzurirajSelekcije(self, SkupSelekcijaZaAzuriranje):
        # u slucaju da se pod SkupSelekcijaZaAzuriranje nalaze neki objekti tipa SelekcijaTocaka
        # koje se zeli azurirati
        if SkupSelekcijaZaAzuriranje != None:
            try:
                for S in SkupSelekcijaZaAzuriranje:
                    assert type(SkupSelekcijaZaAzuriranje) == SelekcijaTocaka
                #nakon sto mo se uvjerili da su svi clanovi stvarno tipa SelekcijaTocaka,
                # sad ih mozemo sve po redu azurirati
                for S in SkupSelekcijaZaAzuriranje:    
                    S.AzurirajSelekciju()
            except TypeError:
                # umjesto vise objekata tipa SelekcijaTocaka koji su upakirani u jedan list/tuple/set,
                # dobili smo jedan objekt tipa SelekcijaTocaka
                # sto je isto sasvim prihvatljivo, samo treba uzeti u obzir da se nad pojedinacnim objektima ne moze iterirati
                # zato ovaj dodatan slucaj
                
                assert type(SkupSelekcijaZaAzuriranje) == SelekcijaTocaka
                SkupSelekcijaZaAzuriranje.AzurirajSelekciju()
            except AssertionError:
                print("Nesto ne valja, SkupSelekcijaZaAzuriranje nije tipa SelekcijaTocaka")
        else:
            return
    '''

    
    
    def EditMode_Udi(self, SkupSelekcijaZaAzuriranje = None, mod = None):
        '''
        Udi u edit mode.
        
        Ako trenutno imamo instancirane neke objekte tipa SelekcijaTocaka, potrebno ih je unijeti kao argument u ovu funkciju da bi i dalje ostali upotrebljivi nakon ulaska/izlaska u editm mode.
        
        VAZNO: pozivanje ove metode ce unistiti sve prethodne reference na vertexe, edgeve i faceve u tekucem objektu.
        Ako se probaju pozvati takve prethodne reference nakon pokretanja ove metode, dogodit ce se crash.
        '''
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        if mod != None:
            assert mod in {TOCKA, RUB, POLIGON}
            bpy.ops.mesh.select_mode(type = mod)
        
        
        #self.PRIVATE_EditMode_AzurirajSelekcije(SkupSelekcijaZaAzuriranje)
        

    
    def EditMode_Izadi(self, SkupSelekcijaZaAzuriranje = None):
        '''
        VAZNO: pozivanje ove metode ce unistiti sve prethodne reference na vertexe, edgeve i faceve u tekucem objektu.
        Ako se probaju pozvati takve prethodne reference nakon pokretanja ove metode, dogodit ce se crash.
        '''
        
        # obavi trazenu operaciju
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        #self.PRIVATE_EditMode_AzurirajSelekcije(SkupSelekcijaZaAzuriranje)
    
    
    
    def OsvjeziMesh_Toggle(self):
        '''
        Neka specificna svojstva pojedinacnog mesha (npr. selekcija vertexa, edgeova i faceova) se ne azuriraju sve dok korisnik izricito ne izade i ude u edit mode.
        Ova funkcija sluzi bas za takve slucajeve.
        
        Ako se scena nalazi u EDIT modeu, stavlja ga na OBJECT mode, i obratno.
        '''
        bpy.ops.object.editmode_toggle()
    
    
    
    

    def PRIVATE_TransformacijaGeometrije(self, pomak, os_pomaka, operacija = None):
        assert self.ProvjeriIspravnost_OsPomaka(os_pomaka)
        
        assert operacija != None
        assert operacija in {
            'TRANSLATION',
            'ROTATION',
            'RESIZE'
        }
        
        pomak = IzracunajVector(pomak)
        
        
        # snimi kontekst
        kontekst = SnimiSelekcijuObjekata()
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.context.view_layer.objects.active = self.objekt
        self.objekt.select_set(True)
        self.EditMode_Udi()
        
        if operacija == 'TRANSLATION':
            bpy.ops.transform.translate(
                value = pomak,
                orient_type = os_pomaka
            )
        elif operacija == 'ROTATION':
            bpy.ops.transform.rotate(
                value = pomak[0],
                orient_axis = 'X'
            )
            #print("Napravio sam X rotaciju")
            bpy.ops.transform.rotate(
                value = pomak[1],
                orient_axis = 'Y'
            )
            #print("Napravio sam Y rotaciju")
            bpy.ops.transform.rotate(
                value = pomak[2],
                orient_axis = 'Z'
            )
            #print("Napravio sam Z rotaciju")
        elif operacija == 'RESIZE':
            bpy.ops.transform.resize(
                value = pomak,
                orient_type = os_pomaka
            )
        else:
            warning.warn("Nesto ne valja, ne mogu izvesti operaciju transformiranja geometrije")
        
        
        # vrati kontekst
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        VratiSelekcijuObjekata(kontekst)
        
        return
    
    def TranslatirajGeometriju(self, pomak, os_pomaka):
        self.PRIVATE_TransformacijaGeometrije(pomak = pomak, os_pomaka = os_pomaka, operacija = 'TRANSLATION')
        return
    
    def RotirajGeometriju(self, pomak, os_pomaka):
        self.PRIVATE_TransformacijaGeometrije(pomak = pomak, os_pomaka = os_pomaka, operacija = 'ROTATION')
        return
    
    def SkalirajGeometriju(self, pomak, os_pomaka):
        self.PRIVATE_TransformacijaGeometrije(pomak = pomak, os_pomaka = os_pomaka, operacija = 'RESIZE')
        return
    
    def CentrirajObjekt(self, tip = None):
        assert tip in [
            'GEOMETRY_ORIGIN',
            'ORIGIN_GEOMETRY',
            'ORIGIN_CURSOR',
            'ORIGIN_CENTER_OF_MASS',
            'ORIGIN_CENTER_OF_VOLUME']
        
        # snimi i vrati kontekst prije i poslije izvedbe operatora
        
        kontekst = SnimiSelekcijuObjekata()
        PostaviAktivanObjekt(self)
        
        bpy.ops.object.origin_set(type = tip)
        
        VratiSelekcijuObjekata(kontekst)
        
        #return True
    
    def ProvjeriIspravnost_OsPomaka(self, ulaz : str = None):
        try:
            assert ulaz != None
            assert type(ulaz) == str
            assert ulaz in {
                'GLOBAL',
                'LOCAL',
                'NORMAL',
                'GIMBAL',
                'VIEW',
                'CURSOR',
                'PARENT'
            }
            return True
        except AssertionError:
            print("Nesto ne valja, os_pomaka nije unesena ispravno")
            return False


    def PRIVATE_Extrude(self, pomak, os_pomaka, pomakniDoKursora, selekcijaTocaka, operacija = None):
        '''
        Izvedi extrude operaciju nad trenutno selektiranim vertexima.
        Ako se u argumentu selekcijaTocaka nalazi neki objekt tipa SelekcijaTocaka, funkcija ignorira prethodno selektirane vertexe i izvodi operaciju samo nad onim tockama koje se nalaze u selekcijaTocaka.
        Funkcija vraca referencu na extrudeanu geometriju u obliku varijable tipa SelekcijaTocaka.

        Ako je pomakniDoKursora True, argument pomak se ignorira i extrudeana geometrija se pomice tocno na kursor.
        '''
        
        # Ukoliko se koristi mnogostrukost, (mozda?) nije moguce koristiti pomakniDoKursora.
        #Da bi se funkcija mogla izvrsiti, potrebno je biti u edit modeu.
        
        assert ProvjeriArgument_Tuple(pomak)
        
        assert self.ProvjeriIspravnost_OsPomaka(os_pomaka)
        
        assert operacija != None
        assert operacija in {
            'EXTRUDE',
            'EXTRUDE_MANIFOLD',
            'DUPLICATE'
        }
        #bpy.ops.mesh.extrude_manifold( TRANSFORM_OT_translate = { 'value':(0,0,0) }, 'orient_type':'GLOBAL', ... )
        
        
        # snimi kontekst:
        kontekst = SnimiSelekcijuObjekata()
        Prije_ObjektniMod = self.objekt.mode
        
        #if selekcijaTocaka != None and type(selekcijaTocaka) == SelekcijaTocaka:
        #    self.PostaviSelekcijuTocaka( selekcijaTocaka )
        

        bpy.context.view_layer.objects.active = self.objekt
        self.objekt.select_set(True)
        self.EditMode_Udi()
        
        # obavi trazenu operaciju
        if operacija == 'EXTRUDE':        
            bpy.ops.mesh.extrude_region_move( TRANSFORM_OT_translate = {
                    'value': pomak,
                    'orient_type': os_pomaka
                }
            )
        elif operacija == 'EXTRUDE_MANIFOLD':
            bpy.ops.mesh.extrude_manifold( TRANSFORM_OT_translate = {
                    'value': pomak,
                    'orient_type': os_pomaka
                }
            )        
        elif operacija == 'DUPLICATE':
            bpy.ops.mesh.duplicate_move( TRANSFORM_OT_translate = {
                    'value': pomak,
                    'orient_type': os_pomaka
                }
            )
        
        # snap to cursor
        if pomakniDoKursora == True:
            PremjestiNaKursor()
        
        # vrati kontekst
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        VratiSelekcijuObjekata(kontekst)
        
        # stvorena geometrija bi sada trebala biti selectana
        # vrati referencu na tu istu stvorenu geometriju
        #return SelekcijaTocaka(self.objekt)

    
    def OPERATOR_Ekstrudiraj(self, pomak = (0,0,0), os_pomaka = 'NORMAL', pomakniDoKursora = False, selekcijaTocaka = None ):
        self.PRIVATE_Extrude(pomak, os_pomaka, pomakniDoKursora, selekcijaTocaka, operacija = 'EXTRUDE')
        return

    def OPERATOR_Ekstrudiraj_Mnogostruko(self, pomak = (0,0,0), os_pomaka = 'NORMAL', pomakniDoKursora = False, selekcijaTocaka = None ):
        self.PRIVATE_Extrude(pomak, os_pomaka, pomakniDoKursora, selekcijaTocaka, operacija = 'EXTRUDE_MANIFOLD')
        return
    
    def DuplicirajGeometriju(self, pomak = (0,0,0), os_pomaka = 'NORMAL', pomakniDoKursora = False, selekcijaTocaka = None ):
        self.PRIVATE_Extrude(pomak, os_pomaka, pomakniDoKursora, selekcijaTocaka, operacija = 'DUPLICATE')
        return
    
    def IzgladiRubove(self, NacinRada : str = 'EDGES', Sirina : int = 0, BrojSegmenata : int = 1):
        assert NacinRada in {'VERTICES', 'EDGES'}
        
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        # snimi kontekst
        kontekst = SnimiSelekcijuObjekata()
        
        # postavi ovaj objekt aktivnim
        bpy.context.view_layer.objects[self.objekt.name].select_set(True)
        bpy.context.view_layer.objects.active = self.objekt
        
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.bevel(
            affect = NacinRada,
            offset = Sirina,
            segments = BrojSegmenata
        )
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        
        # vrati kontekst
        VratiSelekcijuObjekata(kontekst)
        
        return

    def Prepolovi(
        self,
        Ravnina_Tocka   = (0,0,0),
        Ravnina_Normala = (0,0,0),
        PopuniRez = False,
        IzbrisiUnutarnjuGeometriju = False,
        IzbrisiVanjskuGeometriju = False
    ):
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        # snimi selekciju objekata prije
        kontekst = SnimiSelekcijuObjekata()
        
        # snimi selekciju tocaka
        #Prije_SelekcijaTocaka = SelekcijaTocaka( self.objekt )
        
        # postavi ovaj objekt aktivnim i selektiranim
        bpy.context.view_layer.objects[self.objekt.name].select_set(True)
        bpy.context.view_layer.objects.active = self.objekt
        
        # selektiraj svu geometriju na tekucem objektu
        self.OsvjeziMesh_Toggle()
        self.SelektirajSve()
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.bisect(
            plane_co = Vector(Ravnina_Tocka),
            plane_no = Vector(Ravnina_Normala),
            use_fill = PopuniRez,
            clear_inner = IzbrisiUnutarnjuGeometriju,
            clear_outer = IzbrisiVanjskuGeometriju
        )
        
        #print("plane_co: " + str( Vector(Ravnina_Tocka) ) )
        #print("plane_no: " + str( Vector(Ravnina_Normala) ) )
        #print("use_fill: " + str( PopuniRez             ) )
        #print("plane_co: " + str( Vector(Ravnina_Tocka) ) )
        #print("plane_co: " + str( Vector(Ravnina_Tocka) ) )
        
        
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        
        
        # vrati selekciju objekata
        VratiSelekcijuObjekata(kontekst)
        
        # vrati i selekciju tocaka, ako je objekt prije bio u objektnom modu
        #if Prije_ObjektniMod == 'OBJECT':
        #    self.PostaviSelekcijuTocaka( Prije_SelekcijaTocaka )
        
        return
    

    def PRIVATE_InsetOutset(self, Debljina, Dubina, SelektirajNovuGeometriju, operacija = None):
        assert operacija != None
        assert operacija in {'INSET', 'OUTSET'}
        
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        # snimi kontekst
        kontekst = SnimiSelekcijuObjekata()
        
        bpy.context.view_layer.objects[self.objekt.name].select_set(True)
        bpy.context.view_layer.objects.active = self.objekt
        
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        if operacija == 'INSET':
            bpy.ops.mesh.inset(
                thickness = Debljina,
                depth = Dubina,
                use_select_inset = SelektirajNovuGeometriju,
                use_outset = False
            )
        elif operacija == 'OUTSET':
            bpy.ops.mesh.inset(
                thickness = Debljina,
                depth = Dubina,
                use_select_inset = SelektirajNovuGeometriju,
                use_outset = True
            )
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        
        # vrati kontekst
        VratiSelekcijuObjekata(kontekst)
        
        
        return

    def Izvedi_Inset(self, Debljina = 0, Dubina = 0, SelektirajNovuGeometriju = False):
        self.PRIVATE_InsetOutset(
            Debljina = Debljina,
            Dubina = Dubina,
            SelektirajNovuGeometriju = SelektirajNovuGeometriju,
            operacija = 'INSET')
        return

    def Izvedi_Outset(self, Debljina = 0, Dubina = 0, SelektirajNovuGeometriju = False):
        self.PRIVATE_InsetOutset(
            Debljina = Debljina,
            Dubina = Dubina,
            SelektirajNovuGeometriju = SelektirajNovuGeometriju,
            operacija = 'OUTSET')
        return





    def SelektirajSljedeci(self, BrojKoraka = 1):
        # snimi kontekst
        Prije_ObjektniMod = self.objekt.mode
        
        # obavi trazenu operaciju
        for i in range(0, brojKoraka):
            try:
                bpy.ops.mesh.select_next_item()
            except Exception:
                print("Nesto ne valja, otisao sam previse koraka unazad")
                return
        
        #vrati kontekst
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        
        return

    def SelektirajPrethodni(self, BrojKoraka = 1):
        # snimi kontekst
        Prije_ObjektniMod = self.objekt.mode
        
        # obavi trazenu operaciju
        for i in range(0, brojKoraka):
            try:
                bpy.ops.mesh.select_prev_item()
            except Exception:
                print("Nesto ne valja, otisao sam previse koraka unazad")
                return
        
        #vrati kontekst
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        
        return

    def Deselektiraj_Sahovnica(self, PreskociSvakuNtuPlohu = 1, SelektirajSvakuNtuPlohu = 1, Pomak = 0):
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_nth(skip = PreskociSvakuNtuPlohu, nth = SelektirajSvakuNtuPlohu, offset = Pomak)
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        return

    def SelektirajNemnogostrukePlohe(self):
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_non_manifold(extend = False)
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        return        

    def SelektirajSve(self):
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        return

    def DeselektirajSve(self):
    # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.select_all(action = 'TOGGLE')
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        return

    def SelektirajVise(self, UkljuciDijagonalnePlohe = False):
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_more(use_face_step = UkljuciDijagonalnePlohe)
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        return

    def SelektirajManje(self, UkljuciDijagonalnePlohe = False):
        # snimi prethodni objektni mode
        Prije_ObjektniMod = self.objekt.mode
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_less(use_face_step = UkljuciDijagonalnePlohe)
        
        # vrati prethodni objektni mode
        bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        return
    
    
    
    def STARO_StvoriTocku(self, lokacija = None, ostaniUEditModeu = False):
        '''
        Stvara tocku na koordinatama kursora i vraca referencu na stvorenu tocku.
        Ako u argumentu nije dana lokacija, tocka se stvara tamo gdje se nalazi kursor.
        
        Funkcija po defaultu ostavlja scenu u edit modeu, osim ako je ostaniUEditModeu = True - tada funkcija vraca scenu u koji god je objektni mod bio aktualan prije izvrsenja funkcije.
        '''
        if lokacija is None:
            lokacija = DohvatiKursor_Lokacija()
        elif lokacija is not None:
            assert ProvjeriArgument_Tuple(lokacija)


        # snimi kontekst:
        # prethodni object mode (Object mode, Edit mode, Sculpt mode itd.)
        # prethodna lokacija kursora
        Prije_ObjektniMod = self.objekt.mode
        Prije_KursorLokacija = DohvatiKursor_Lokacija()
        
        
        # 'staticna' funkcija, pa ne treba self. prije poziva funkcije
        PostaviKursor(lokacija)
        
        # stvori novu pojedinacnu tocku
        bpy.ops.mesh.primitive_vert_add()
        
        
        # sad kad znamo da je mesh osvjezen i da su selektirane tocke azurirane, 
        # tek sad mozemo dohvatiti novu tocku
        #nova_tocka = self.DohvatiSelekcijuTocaka()
        #assert len(nova_tocka) == 1
        #assert type(nova_tocka[0]) == bpy.types.MeshVertex
        
        # vrati kontekst
        # objekt mod, ali samo ako je ostaniUEditModeu == False, sto je defaultno ponasanje funkcije
        if ostaniUEditModeu == False:
            bpy.ops.object.mode_set(mode = Prije_ObjektniMod)
        PostaviKursor( lokacija = Prije_KursorLokacija )
        
        
        #return nova_tocka



    def STARO_StvoriRubIzDvijeTocke(self, tocka_A = None, tocka_B = None):
        assert type(tocka_A) == bpy.types.MeshVertex
        assert type(tocka_B) == bpy.types.MeshVertex
        # TODO: povezi ove dvije tocke
        
        # snimi kontekst:
        # selektirane tocke
        # Prije_SelekcijaTocaka = self.DohvatiSelekcijuTocaka()

        bpy.ops.mesh.edge_face_add()
        self.OsvjeziMesh_Toggle()

        # vrati kontekst
        # self.PostaviSelekcijuTocaka(Prije_SelekcijaTocaka)
   
    
    def PRIVATE_PozicionirajNoviObjekt(self, dimenzije, pozicija, rotacija, centriraj):
        '''
        Ovu funkciju korisnik ne bi trebao pozivati samostalno / direktno iz konzole. Funkcija se koristi pri odredivanju pozicije upravo stvorenog objekta
        '''
        #novi_objekt = self.objekt
        
        if centriraj == False and pozicija == (0,0,0):
            pozicija = (dimenzije[0] / 2, dimenzije[1] / 2, dimenzije[2] / 2)

        self.Dimenzioniraj(dimenzije)
        self.Pozicija(pozicija)
        self.Rotacija_Apsolutna(rotacija)
        
        #return novi_objekt


    def Translatiraj( self, translacija = (0,0,0) ):
        '''
        Translatiraj()
        Translatiraj zadani objekt prema zadanom vektoru (zbroji postojece koordinate lokacije s argumentom translacija).
        objekt - varijabla tipa bpy_types.Object
        translacija - tuple od tocno tri clana, list je isto podrzan
        Primjer upotrebe: Translatiraj(objekt = Kocka(), translacija = (2,2,3) )
        '''
        #assert ProvjeriIspravnostUnesenihArgumenata(objekt, translacija)
        translacija = IzracunajVector( translacija )
        
        self.objekt.location = self.objekt.location + translacija
        
        return True


    def Pozicija( self, pozicija = (0,0,0)  ):
        '''
        Pozicija()
        Lokacija zadanog objekta postaje jednaka zadanom vektoru, neovisno o tome gdje se model prethodno nalazio.
        objekt - varijabla tipa bpy_types.Object
        pozicija - tuple od tocno tri clana, list je isto podrzan
        Primjer upotrebe: Pozicija(objekt = Kocka(), pozicija = (2,2,3) )
        '''
        #assert ProvjeriIspravnostUnesenihArgumenata(objekt, pozicija)
        if pozicija == None:
            pozicija = (0,0,0)
        
        print("Pozicija: " + str(pozicija))
        
        pozicija = IzracunajVector( pozicija )
        
        self.objekt.location = pozicija


    def Rotacija_Apsolutna( self, rotacija = (0,0,0)  ):
        '''
        Rotacija_Apsolutna()
        Rotacija zadanog objekta postaje jednaka zadanom vektoru, neovisno o tome gdje se model prethodno nalazio.
        objekt - varijabla tipa bpy_types.Object
        rotacija - tuple od tocno tri clana, list je isto podrzan. Po defaultu u stupnjevima
        Primjer upotrebe: Pozicija(objekt = Kocka(), rotacija = (0,45,180) )
        '''
        #assert ProvjeriIspravnostUnesenihArgumenata(objekt, rotacija)
        
        if rotacija == None:
            rotacija = (0,0,0)
        
        rotacija = IzracunajVector( PretvoriUStupnjeve(rotacija)  )
        
        self.objekt.rotation_euler  = Euler(rotacija, 'XYZ')


    def Rotacija_Relativna( self, rotacija = (0,0,0)  ):
        '''
        Rotacija_Relativna()
        Zbroji trenutnu rotaciju i argument rotacija.
        objekt - varijabla tipa bpy_types.Object
        rotacija - tuple od tocno tri clana, list je isto podrzan. Po defaultu u stupnjevima
        Primjer upotrebe: Pozicija(objekt = Kocka(), rotacija = (0,45,180) )
        '''
        #assert ProvjeriIspravnostUnesenihArgumenata(objekt, rotacija)
        
        if rotacija == None:
            rotacija = (0,0,0)
        
        rotacija = IzracunajVector( PretvoriUStupnjeve(rotacija) )
        
        self.objekt.rotation_euler  = Euler( rotacija + Vector(self.objekt.rotation_euler) )



    def Dimenzioniraj( self, dimenzije = (1,1,1)  ):
        '''
        Dimenzioniraj()
        Postavi dimenzije zadanog objekta tako da odgovaraju argumentu dimenzije.
        objekt - varijabla tipa bpy_types.Object
        dimenzije - tuple od tocno tri clana, list je isto podrzan
        Primjer upotrebe: Dimenzioniraj(objekt = Kocka(), dimenzije = (2,2,4) )
        '''
        #assert ProvjeriIspravnostUnesenihArgumenata(objekt, dimenzije, neSmijeBitiNula = True)
        objekt = self.objekt
        
        # iznimka za ovu Dimenzioniraj() i Skaliraj()
        if type(dimenzije) == int or type(dimenzije) == float:
            dimenzije = (dimenzije, dimenzije, dimenzije)
        
        dimenzije = IzracunajVector( dimenzije )
        
        objekt.dimensions = dimenzije
        
        # zapamti selektirane objekte prije izvodenja ove funkcije
        Prije_AktivanObjekt = bpy.context.view_layer.objects.active
        Prije_Objekt_JeLiSelectan = bpy.context.view_layer.objects[objekt.name].select_get()
        
        # selektiraj objekt i ucini ga aktivnim
        bpy.context.view_layer.objects[objekt.name].select_set(True)
        bpy.context.view_layer.objects.active = objekt
        
        # apliciraj skalu
        bpy.ops.object.transform_apply(location = False, rotation = False, scale = True)
        
        # vrati selekciju objekata kakva je bila prije izvodenja funkcije
        bpy.context.view_layer.objects[objekt.name].select_set(Prije_Objekt_JeLiSelectan)
        bpy.context.view_layer.objects.active = Prije_AktivanObjekt
        
        return


    def Skaliraj( self, skala = (1,1,1)  ):
        '''
        Skaliraj()
        Skaliraj zadani objekte prema zadanom skala argumentu.
        objekt - varijabla tipa bpy_types.Object
        skala - tuple od tocno tri clana, list je isto podrzan
        Primjer upotrebe: Skaliraj(objekt = Kocka(), skala = (2,2,4) )
        '''
        #assert ProvjeriIspravnostUnesenihArgumenata(objekt, skala, neSmijeBitiNula = True)
        objekt = self.objekt
        
        # iznimka za ovu Dimenzioniraj() i Skaliraj()
        if type(skala) in {int, float}:
            skala = (skala, skala, skala)

        # skalu ne treba pretvarati u milimetre, jer se radi o faktoru a ne o konkretnoj fizickoj velicini
        skala = IzracunajVector(skala)
        
        #print("Skala objekta: " + str(skala))
        objekt.scale = skala
        #print("Skala objekta nakon stavljanja: " + str(objekt.scale))
        
        # zapamti selektirane objekte prije izvodenja ove funkcije
        kontekst = SnimiSelekcijuObjekata()
        
        # selektiraj objekt i ucini ga aktivnim
        PostaviAktivanObjekt(objekt)
        
        # apliciraj skalu
        bpy.ops.object.transform_apply(location = False, rotation = False, scale = True)
        #print("Skala objekta nakon applyanja: " + str(objekt.scale))
        
        # vrati selekciju objekata kakva je bila prije izvodenja funkcije
        VratiSelekcijuObjekata(kontekst)
        
        return

    def DohvatiDimenzije(self):
        return self.objekt.dimensions

    def DohvatiPoziciju(self):
        return self.objekt.location

    def Krivulja(self, *args,
            SkalirajKrivulju = None,
            OsDeformacije = 'Z'
            #DuljinaHandlea = 250,
            #UnistiKrivulju = True
        ):
        assert OsDeformacije in {'X', 'Y', 'Z', '-X', '-Y', '-Z'}
        OsDeformacije_Rjecnik = {
            'X':'POS_X',
            'Y':'POS_Y',
            'Z':'POS_Z',
            '-X':'NEG_X',
            '-Y':'NEG_Y',
            '-Z':'NEG_Z'
        }

        
        
        for a in args:
            assert ProvjeriArgument_Tuple(a) == True
        
        
        
        
        curve_mesh = bpy.data.curves.new(name = 'curve_mesh', type = 'CURVE')
        curve_obj = bpy.data.objects.new('curve_obj', curve_mesh)
        bpy.context.scene.collection.objects.link(curve_obj)
        
        spline = curve_obj.data.splines.new('BEZIER')
        #spline = curve_obj.data.splines[0]
        assert type(spline) == bpy.types.Spline
        print("Koordinate prve tocke: " + str(spline.bezier_points[0].co))
        # pri stvaranju splinea, jedan point ce vec postojati
        # zato '-1'
        spline.bezier_points.add(len(args) - 2)
        
        for i in range(0, len(args) - 1):
            # spline pointovi iz nekog razloga prihvacaju samo 4d vektor, a ne i 3d vektor
            #spline.bezier_points[i].co = Vector(args[i]).to_4d()
            point = spline.bezier_points[i]
            point.co = Vector(args[i])
            point.handle_left_type  = 'AUTO' # 'ALIGNED' ili 'AUTO'
            point.handle_right_type = 'AUTO'
            
            #point.handle_left   = point.co + Vector((-DuljinaHandlea,0 ,0))
            #point.handle_right  = point.co + Vector((DuljinaHandlea ,0 ,0))
            
            #point.handle_left_type  = 'AUTO'
            #point.handle_right_type = 'AUTO'
        
        
        
        kontekst = SnimiSelekcijuObjekata()
        
        #bpy.ops.curve.primitive_bezier_curve_add(scale = (1,1,1))
        #curve_obj = InstancirajNoviPrimitivniObjekt(GeometrijskoTijelo = 'KRIVULJA')
        
        
        if SkalirajKrivulju != None:
            assert ProvjeriArgument_Tuple(SkalirajKrivulju) == True
            curve_obj.scale = Vector(SkalirajKrivulju)
        
        
        mod = self.objekt.modifiers.new(name = 'krivulja', type = 'CURVE')
        mod.object = curve_obj
        mod.deform_axis = OsDeformacije_Rjecnik[OsDeformacije]
        
        
        
        PostaviAktivanObjekt(self)
        bpy.ops.object.modifier_apply(modifier = mod.name)
        
        VratiSelekcijuObjekata(kontekst)
        
        '''
        if UnistiKrivulju == True:
            bpy.data.objects.remove(curve_obj)
        '''
        
        return True

    def Kruznica(self,
        SkalirajKrivulju = None,
        SkalirajObjekt = None,
        OsDeformacije = 'Z',
        #UnistiKrivulju = True,
        RotacijaObjekta = (0,0,0) # Rotacija preimenovana u RotacijaObjekta
    ):
        '''
        Iskrivljuje objekt po krivulji slicno Krivulja() funkciji, samo sto umjesto proizvoljnih tocaka
        krivulju cini savrsena kruznica.
        '''
        assert OsDeformacije in {'X', 'Y', 'Z', '-X', '-Y', '-Z'}
        OsDeformacije_Rjecnik = {
            'X':'POS_X',
            'Y':'POS_Y',
            'Z':'POS_Z',
            '-X':'NEG_X',
            '-Y':'NEG_Y',
            '-Z':'NEG_Z'
        }
        
        
        
        kontekst = SnimiSelekcijuObjekata()
        
        curve_obj = InstancirajNoviPrimitivniObjekt(GeometrijskoTijelo = 'KRUZNICA')
        
        PostaviAktivanObjekt(curve_obj)
        #print("Trenutno aktivan objekt (prvi):" + bpy.context.active_object.name)
        
        # postavi i primijeni rotaciju i skalu
        
        
        #print("Argument Rotacija u kruznici:" + str(Rotacija))
        curve_obj.rotation_euler = Euler( PretvoriUStupnjeve(tuple(RotacijaObjekta)) )
        bpy.ops.object.transform_apply(rotation = True, scale = True)
        

        mod = self.objekt.modifiers.new(name = 'kruznica', type = 'CURVE')
        mod.object = curve_obj
        mod.deform_axis = OsDeformacije_Rjecnik[OsDeformacije]

        PostaviAktivanObjekt(self)
        
        print("Trenutno aktivan objekt (drugi) :" + bpy.context.active_object.name)
        print("Ime curve modifiera prije applyajanja :" + mod.name)
        print("Target curve modifiera prije applyajanja :" + mod.object.name)
        print("Os deformacije prije applyajanja: " + mod.deform_axis)
        
        

        VratiSelekcijuObjekata(kontekst)
        
        if SkalirajKrivulju != None:
            assert ProvjeriArgument_Tuple(SkalirajKrivulju) == True
            print("Skaliram krivulju za " + str(SkalirajKrivulju) + " (unutar Kruznica() funkcije)")
            curve_obj.scale = Vector(SkalirajKrivulju)
        
        if SkalirajObjekt != None:
            assert ProvjeriArgument_Tuple(SkalirajObjekt) == True
            print("Skaliram objekt za " + str(SkalirajObjekt) + " (unutar Kruznica() funkcije)")
            self.objekt.scale = SkalirajObjekt
            print("Skala objekta sada iznosi " + str(self.objekt.scale))
        
        
        ##bpy.ops.object.modifier_apply(modifier = mod.name)
        #bpy.ops.object.convert(target = 'MESH')
        
        '''
        if UnistiKrivulju == True:
            bpy.data.objects.remove(curve_obj)
        '''
        
        return True
        

    def PRIVATE_Boolean(self, target, sacuvajTarget, operacija = None):
        '''
        PRIVATE_Boolean()
        Za svaku od tri PRIVATE_Boolean operacije (Unija, Presjek, Razlika) postoji zasebna funkcija - Unija(), Presjek() i Razlika(), koje se ponasaju kao omotaci za PRIVATE_Boolean().
        Za direktno pozivanje funkcije, preporuca se koristiti navedene funkcije umjesto PRIVATE_Boolean().
        U slucaju da se PRIVATE_Boolean ipak direktno poziva iz konzole / skripte, primjer upotrebe:
        PRIVATE_Boolean(Kocka(), Stozac(), operacija = 'UNION')
        '''
        #assert objekt != None
        #assert objekt.data != None
        #assert bpy.context.scene.collection.objects.find(objekt.name) != -1
        
        # target je tipa Objekt, ne referenca na sami objekt
        
        #assert target != None
        #assert target.objekt != None
        assert ProvjeriIspravnostUnesenogObjekta(target) == True ### TODO - Provjeri ovo!
        assert bpy.context.scene.collection.objects.find(target.objekt.name) != -1
        
        assert operacija is not None
        assert operacija in {'UNION','INTERSECT','DIFFERENCE'}
        
        objekt = self.objekt
        target = target.objekt
        
        modifier = objekt.modifiers.new(name = 'boolean', type = 'BOOLEAN')
        #modifier.solver = 'MANIFOLD'
        modifier.solver = 'EXACT'
        modifier.operation  = operacija
        modifier.object     = target
        
        # zapamti selektirane objekte prije izvodenja ove funkcije
        Prije_AktivanObjekt = bpy.context.view_layer.objects.active
        Prije_Objekt_JeLiSelectan = bpy.context.view_layer.objects[objekt.name].select_get()
        Prije_Target_JeLiSelectan = bpy.context.view_layer.objects[target.name].select_get()
        
        # selektiraj objekt i ucini ga aktivnim
        bpy.context.view_layer.objects[objekt.name].select_set(True)
        bpy.context.view_layer.objects.active = objekt
        
        # apliciraj modifier
        bpy.ops.object.modifier_apply(modifier = modifier.name)
        
        # vrati selekciju objekata kakva je bila prije izvodenja funkcije
        bpy.context.view_layer.objects[objekt.name].select_set(Prije_Objekt_JeLiSelectan)
        bpy.context.view_layer.objects[target.name].select_set(Prije_Target_JeLiSelectan)
        bpy.context.view_layer.objects.active = Prije_AktivanObjekt
        
        if sacuvajTarget == False:
            target.name = 'nepotrebno'
            bpy.context.scene.collection.objects.unlink(target)
        
        return
        

    def Unija(self, target = None, sacuvajTarget = True):
        '''
        Unija()
        Stvori PRIVATE_Boolean uniju dva objekta - objekt i target.
        target se po defaultu brise iz tekuce .blend datoteke, osim ako je argument sacuvajTarget postavljen na True.
        Primjer upotrebe:
        Unija( Kocka(), Stozac() )
        '''
        self.PRIVATE_Boolean(target, sacuvajTarget, 'UNION')
        return

    def Presjek(self, target = None, sacuvajTarget = True):
        '''
        Presjek()
        Stvori PRIVATE_Boolean presjek dva objekta - objekt i target.
        target se po defaultu brise iz tekuce .blend datoteke, osim ako je argument sacuvajTarget postavljen na True.
        Primjer upotrebe:
        Presjek( Kocka(), Stozac() )
        '''
        self.PRIVATE_Boolean(target, sacuvajTarget, 'INTERSECT')
        return

    def Razlika(self, target = None, sacuvajTarget = True):
        '''
        Razlika()
        Stvori PRIVATE_Boolean razliku dva objekta - objekt i target.
        target se po defaultu brise iz tekuce .blend datoteke, osim ako je argument sacuvajTarget postavljen na True.
        Primjer upotrebe:
        Razlika( Kocka(), Stozac() )
        '''
        self.PRIVATE_Boolean(target, sacuvajTarget, 'DIFFERENCE')
        return


def ProbajIscupatiIzTuplea(ulaz):
    '''
    Ako smo pod *args dobili tuple (arg1, arg2, arg3...) umjesto pojedinacnih argumenata arg1, arg2, arg3,
    Pod *args se zapravo nalazi ((arg1, arg2, arg3...)) umjesto ocekivanog (arg1, arg2, arg3...).
    Ako je takav slucaj, ova funkcija cupa argumente iz tuplea ((arg1, arg2, arg3...)) i pretvara ga u (arg1, arg2, arg3...).
    '''
    if len(ulaz) == 1 and type(ulaz[0]) in {list, tuple}:
        return ulaz[0]
    else:
        return ulaz


def VektorRotacije_U_Matricu(tuple):
    eul = Euler(tuple)
    #mat_rot = eul.to_matrix().to_4x4()
    mat_rot = eul.to_matrix()
    #mat_loc = mathutils.Matrix.Translation((2.0, 3.0, 4.0))
    #mat = mat_loc @ mat_rot.to_4x4()
    
    #mat_rot = mathutils.Matrix.Rotation(math.radians(45.0), 4, 'Z')
    return mat_rot


class PrazanObjekt(Objekt):
    #def __repr__(self):
    #    return "Objekt (" + self.objekt.name + ")"
    
    
    def PRIVATE_PozicionirajNoviPRAZANObjekt(self, pozicija, rotacija):
        #self.Dimenzioniraj(dimenzije)
        self.Pozicija(pozicija)
        self.Rotacija_Apsolutna(rotacija)
        return
    
    def PRIVATE_InstancirajPrazanObjekt(self):
        
        self.mesh        = bpy.data.meshes.new("PrazanMesh")
        self.objekt = bpy.data.objects.new("PrazanObjekt", self.mesh)
        bpy.context.collection.objects.link(self.objekt)
        
        return self.objekt
    
    
    def __init__(self, *args, **kwargs):
        
        if IspisujDebugStatementove == True:
            print("Usao sam u konstuktor za PRAZAN objekt")
        
        self.objekt = self.PRIVATE_InstancirajPrazanObjekt()
        
        pozicija = None
        rotacija = None
        
        try:
            pozicija = kwargs['pozicija']
        except KeyError:
            pass
        
        try:
            rotacija = kwargs['rotacija']
        except KeyError:
            pass

        if pozicija == None:
            try:
                pozicija = args[0]
            except Exception:
                pass

        if rotacija == None:
            try:
                rotacija = args[1]
            except Exception:
                pass

        # u slucaju da neki od keyword argumenata nije dobro imenovan
        self.PRIVATE_PozicionirajNoviPRAZANObjekt(
            pozicija    = pozicija,
            rotacija    = rotacija
        )




        ##############


        self.bm = bmesh.new()

        # Custom integer ID stored on every vertex
        self.id_layer_vertex = self.bm.verts.layers.int.new("vertex_id")
        # ADDED
        self.id_layer_edge = self.bm.edges.layers.int.new("edge_id")
        self.id_layer_face = self.bm.faces.layers.int.new("face_id")

        # Python-side name database
        self.vertex_names = {}
        self.next_id_vertex = 0

        #ADDED
        self.edge_names = {}
        self.next_id_edge = 0

        self.face_names = {}
        self.next_id_face = 0




    def StvoriTocku(self, pozicija, ime = None):
        #global self.next_id_vertex
        
        ime = DodijeliIme(ime)
        
        # defaultna metoda
        v = self.bm.verts.new(pozicija)

        v[self.id_layer_vertex] = self.next_id_vertex
        self.vertex_names[ime] = self.next_id_vertex
        self.next_id_vertex += 1
        
        return v

    # ADDED
    # promjenjeno
    def StvoriRub(self, *args, ime = None):
        #global self.next_id_edge
        
        args = ProbajIscupatiIzTuplea(args)
        
        for a in args:
            if type(a) != bmesh.types.BMVert:
                raise Exception("Jedan od argumenata nije tocka!")
        
        ime = DodijeliIme(ime)
        
        try:
        
            v = self.bm.edges.new(tuple(args))

            #defaultno ime
            #name = 'A'

            v[self.id_layer_edge] = self.next_id_edge
            self.edge_names[ime] = self.next_id_edge
            self.next_id_edge += 1
            return v
        
        except ValueError:
            # u slucaju da ovaj rub vec postoji
            #warnings.warn("Rub vec postoji! Vracam None kao povratni tip")
            #return None
            
            raise Exception("Ne mogu stvoriti rub s navedenim tockama jer taj rub vec postoji!")



    def StvoriPlohu(self, *args, ime = None):
        '''
        U argumentu su smiju nalaziti samo tocke, ne i rubovi.
        '''
        #global self.next_id_face
        #print("tuple(args) u StvoriPlohu: " + str(tuple(args)))
        
        args = ProbajIscupatiIzTuplea(args)
        
        ime = DodijeliIme(ime)
        
        # TODO: sto ako su uneseni edgevi
        
        # na pocetku ne znamo je li se radi o edgevima ili facevima
        args_areVerts = True
        args_areEdges = True
        
        for a in args:
            if type(a) != bmesh.types.BMVert:
                args_areVerts = False
                break
        
        for a in args:
            if type(a) != bmesh.types.BMEdge:
                args_areEdges = False
                break
        
        if args_areVerts == True and args_areEdges == False:
            # svi argumenti su vertexi, a moraju biti bar 3 vertexa da bi se mogla stvoriti ploha
            if len(args) < 3:
                raise Exception("Ne mogu stvoriti plohu s manje od 3 tocke!")
            
            # sortiraj vertexove iz args mozda?
        
            v = self.bm.faces.new(tuple(args))

            #defaultno ime
            #name = 'A'

            v[self.id_layer_face] = self.next_id_face
            self.face_names[ime] = self.next_id_face
            self.next_id_face += 1
            return v
            
        
         # u slucaju da se u argumentu nalaze edgevi
        elif args_areVerts == False and args_areEdges == True:
            #assert len(args) == 2
        
            '''
            verts_collected = []
            
            # iscupaj sve tocke iz danih edgeva,
            # i stavi ih u set jer ne smije biti duplica
            for a in args:
                verts = a.verts
                for element in verts:
                    if element not in verts_collected:
                        verts_collected.append(element) # treba mi a,b umjesto (a,b)
                    else:
                        continue
            
            args = verts_collected
            '''
            
            bmesh.ops.holes_fill(self.bm, edges = list(args))
        
        else:
            raise Exception("Nesto ne valja, argumenti nisu ispravno uneseni u StvoriPlohu()")
        
        
        



    '''
    def DohvatiTocku(self, ime = None):
        target_id = self.vertex_names[ime]

        for v in self.bm.verts:
            if v[self.id_layer_vertex] == target_id:
                return v
        return None


    def DohvatiRub(self, ime = None):
        target_id = self.edge_names[ime]

        for v in self.bm.edges:
            if v[self.id_layer_edge] == target_id:
                return v
        return None


    def DohvatiPlohu(self, ime = None):
        target_id = self.face_names[ime]

        for v in self.bm.faces:
            if v[self.id_layer_face] == target_id:
                return v
        return None
    '''





    def EkstrudirajTocku(self, TockaPostojeca, offset, ImeNovogRuba = None, ImeNoveTocke = None):
        #global self.next_id_vertex
        #TockaPostojeca = DohvatiTocku(TockaPostojeca_name)
        
        assert TockaPostojeca != None
        assert type(TockaPostojeca) == bmesh.types.BMVert
        
        assert offset != None
        assert type(offset) in {list,tuple}
        assert len(offset) == 3
        
        ImeNovogRuba = DodijeliIme(ImeNovogRuba)
        ImeNoveTocke = DodijeliIme(ImeNoveTocke)
        

        if TockaPostojeca is None:
            raise ValueError(f"Vertex '{TockaPostojeca_name}' does not exist")

        
        new_position = (
            TockaPostojeca.co.x + offset[0],
            TockaPostojeca.co.y + offset[1],
            TockaPostojeca.co.z + offset[2],
        )
        
        
        new_vert = self.StvoriTocku(new_position, ime = ImeNoveTocke)
        new_edge = self.StvoriRub(TockaPostojeca, new_vert, ime = ImeNovogRuba)
        
        # umjesto da se vrati referenca na jedan pojedinacni vert
        # vrati reference na novu tocku i novi rub
        return {'NovaTocka':new_vert, 'NoviRub':new_edge}


    def EkstrudirajRub(self, RubPostojeci, offset, ImeNovogRuba = None, PopuniPlohu = True):
        assert RubPostojeci != None
        assert type(RubPostojeci) == bmesh.types.BMEdge
        
        assert offset != None
        assert type(offset) in {list,tuple}
        assert len(offset) == 3
        
        
        ImeNovogRuba = DodijeliIme(ImeNovogRuba)
        
        # prvi vertex ce biti dolje/lijevo, drugi ce biti gore/desno
        new_verts = []
        for v in RubPostojeci.verts:
            new_item = self.EkstrudirajTocku(v, offset)['NovaTocka']
            new_verts.append(new_item)
        
        new_edge = self.StvoriRub(new_verts[0], new_verts[1])
        new_face = None
        
        if PopuniPlohu == True:
            # proslijedi pojedinacne tocke
            RubPostojeci_verts = RubPostojeci.verts
            
            #self.StvoriPlohu(RubPostojeci_verts[0], RubPostojeci_verts[1], new_verts[1], new_verts[0])
            self.StvoriPlohu(RubPostojeci_verts[0], new_verts[0], new_verts[1], RubPostojeci_verts[1])
            '''
            RubPostojeci_verts[1] <---- new_verts[1]
                                            |
                                            |
            RubPostojeci_verts[0] ----> new_verts[0]
            '''
            

        return {'NoveTocke':new_verts, 'NoviRub':new_edge, 'NovaPloha':new_face}


    def RotirajTocke(self, *args, rotacija = None, centar = None):
        args = ProbajIscupatiIzTuplea(args)
        
        assert ProvjeriArgument_Tuple(rotacija)
        if centar != None:
            assert ProvjeriArgument_Tuple(centar)
        else:
            centar = (0,0,0)

        
        bmesh.ops.rotate(
            self.bm,
            cent = tuple(centar),
            verts = list(args),
            matrix = VektorRotacije_U_Matricu(rotacija)
        )
        
        return True



    def DohvatiSveTockeIzPlohe(self, face):
        # radi i za rubove
        return face.verts

    def DohvatiSveRuboveIzPlohe(self, face):
        return face.edges

    def IzracunajCentarTocaka(self, *args):
        if len(args) < 2:
            raise Exception("Ne mogu izracunati centar od samo jednog elementa")

        zbroj = {'x':0, 'y':0, 'z':0}
        for a in args:
            if type(a) != bmesh.types.BMVert:
                raise Exception("Barem jedan od argumenata nije tocka")
            zbroj['x'] += a.co.x
            zbroj['y'] += a.co.y
            zbroj['z'] += a.co.z
        
        zbroj['x'] /= len(args)
        zbroj['y'] /= len(args)
        zbroj['z'] /= len(args)
        
        return (zbroj['x'], zbroj['y'], zbroj['z'])

    def IzracunajCentarRuba(self, arg):
        if type(arg) != bmesh.types.BMEdge:
            raise Exception("Barem jedan od argumenata nije rub")
        verts = arg.verts
        
        zbroj = {'x':0, 'y':0, 'z':0}
        
        for a in verts:

            zbroj['x'] += a.co.x
            zbroj['y'] += a.co.y
            zbroj['z'] += a.co.z
        
        zbroj['x'] /= len(verts)
        zbroj['y'] /= len(verts)
        zbroj['z'] /= len(verts)
        
        return (zbroj['x'], zbroj['y'], zbroj['z'])
        

    def IzvediPromjene(self):
        self.bm.to_mesh(self.mesh)
        self.mesh.update()
        return True




def StvoriPrazanObjekt(*args, **kwargs):
    return PrazanObjekt(*args, **kwargs)


def StvoriTocku(objekt, pozicija, ime = None)  -> Optional[bmesh.types.BMVert]:
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    return objekt.StvoriTocku(pozicija, ime = ime)

def StvoriRub(objekt, *args, ime = None)       -> Optional[bmesh.types.BMEdge]:
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    return objekt.StvoriRub(*args, ime = ime)

def StvoriPlohu(objekt, *args, ime = None)     -> Optional[bmesh.types.BMFace]:
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    return objekt.StvoriPlohu(*args, ime = ime)


def EkstrudirajTocku(objekt,
    TockaPostojeca,
    offset,
    ImeNovogRuba = None,
    ImeNoveTocke = None
) -> Optional[dict]:
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.EkstrudirajTocku(
        TockaPostojeca,
        offset,
        ImeNovogRuba = ImeNovogRuba,
        ImeNoveTocke = ImeNoveTocke
    )

def EkstrudirajRub(objekt,
    RubPostojeci,
    offset,
    ImeNovogRuba = None,
    #ImenaNovihTocaka = None,
    PopuniPlohu = True
) -> Optional[dict]:
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.EkstrudirajRub(
        RubPostojeci,
        offset,
        ImeNovogRuba = ImeNovogRuba,
        #ImenaNovihTocaka = ImenaNovihTocaka,
        PopuniPlohu = PopuniPlohu
    )

def RotirajTocke(objekt, *args, rotacija = None, centar = None):
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.RotirajTocke(*args, rotacija = rotacija, centar = centar)

def DohvatiSveTockeIzPlohe(objekt, face):
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    # moze u teoriji i raditi za edgeove, ali bolje ne
    return objekt.DohvatiSveTockeIzPlohe(face)

def DohvatiSveRuboveIzPlohe(objekt, face):
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.DohvatiSveRuboveIzPlohe(face)

def IzracunajCentarTocaka(objekt, *args):
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.IzracunajCentarTocaka(*args)

def IzracunajCentarRuba(objekt, arg):
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.IzracunajCentarRuba(arg)

def IzvediPromjene(objekt):
    assert JeLiOvaVarijablaTipa_PrazanObjekt(objekt) == True
    
    return objekt.IzvediPromjene()




def Valjak_Iscrtavanje(objekt, Radijus, Visina, BrojPloha):
    '''
    Stvori valjak bez oslanjanja na Blenderove ugrađene primitivne objekte.
    '''
    TrenutniRub_DonjaTocka  = StvoriTocku(objekt, (0, 0, 0) )
    TrenutniRub_GornjaTocka = StvoriTocku(objekt, (0, 0, Visina) )
    TrenutniRub             = StvoriRub(objekt, TrenutniRub_DonjaTocka, TrenutniRub_GornjaTocka)

    RuboviDonji     = [TrenutniRub_DonjaTocka   ]
    RuboviGornji    = [TrenutniRub_GornjaTocka  ]

    PrviRub_DonjaTocka  = TrenutniRub_DonjaTocka
    PrviRub_GornjaTocka = TrenutniRub_GornjaTocka

    for i in range(0, BrojPloha):
        if i == BrojPloha - 1:
            StvoriPlohu( objekt,
                TrenutniRub_DonjaTocka,
                PrviRub_DonjaTocka,
                PrviRub_GornjaTocka,
                TrenutniRub_GornjaTocka
            )
            break
        
        #h = a.StvoriRub(TrenutniRub_DonjaTocka, TrenutniRub_GornjaTocka)
        #geometrija_nastala = EkstrudirajRub(objekt, TrenutniRub, (0, 1, 0) )
        
        duljinaPlohe = 2 * Radijus * sin(pi/BrojPloha)
        
        geometrija_nastala = EkstrudirajRub(objekt, TrenutniRub, (0, duljinaPlohe, 0) )
        RuboviDonji.append(geometrija_nastala['NoveTocke'][0])
        RuboviGornji.append(geometrija_nastala['NoveTocke'][1])
        
        #CentarRotacije = a.IzracunajCentarRuba(TrenutniRub)
        #CentarRotacije = (0,0,0)
        
        #print("Donji rub za i = " + str(i) + " : " + str(RuboviDonji[0].co))
        #print("Gornji rub za i = " + str(i) + " : " + str(RuboviGornji[0].co))
        
        TrenutniRub             = geometrija_nastala['NoviRub'   ]
        TrenutniRub_DonjaTocka  = geometrija_nastala['NoveTocke' ][0]
        TrenutniRub_GornjaTocka = geometrija_nastala['NoveTocke' ][1]
        
        RotirajTocke( objekt,
            TrenutniRub_DonjaTocka,
            TrenutniRub_GornjaTocka,
            rotacija = (0, 0, (2*pi)/(BrojPloha) )
        )


    StvoriPlohu(objekt, RuboviDonji)
    StvoriPlohu(objekt, RuboviGornji)




# u klasi Objekt se nalaze dva konstruktora:
# 1) konstruktor za primitivne objekte, koji se moze pozvati s 4 razlicita argumenta: 'KOCKA', 'VALJAK','STOZAC','KUGLA'
# za sve objekte (osim kocke) pozeljno je navesti rezoluciju. Ako nije navedena, rezolucija se postavlja na defaultnu vrijednost, 32
# 2) konstruktor za postojece objekte
# ako korisnik zeli u Pythonu dobiti varijablu tipa Objekt a koja se odnosi na neki 3D objekt iz Blendera
# funkcije ispod su wrapperi za navedene slucajeve
# npr.
# a = Kocka() --> stvorena je kocka, varijabla a se odnosi na tu istu kocku i tip varijable a je Objekt
# b = Kugla() --> stvorena je kugla, varijabla b se odnosi na tu istu kocku i tip varijable b je Objekt
# neovisno o tome kako i iz cega je objekt instanciran, tip stvorenog objekta ce uvijek biti Objekt (ne bpy.types.Object iz bpy, nego specificno Objekt iz module_OOP.py)


def Kocka( dimenzije = (1,1,1), pozicija = (0,0,0), rotacija = (0,0,0), centriraj = True, rezolucija = 32 ):
    return Objekt(
        dimenzije = dimenzije,
        pozicija = pozicija,
        rotacija = rotacija,
        centriraj = centriraj,
        GeometrijskoTijelo = 'KOCKA',
        rezolucija = rezolucija
    )

def Kugla( dimenzije = (1,1,1), pozicija = (0,0,0), rotacija = (0,0,0), centriraj = True, rezolucija = 32 ):
    return Objekt(
        dimenzije = dimenzije,
        pozicija = pozicija,
        rotacija = rotacija,
        centriraj = centriraj,
        GeometrijskoTijelo = 'KUGLA',
        rezolucija = rezolucija
    )

def Stozac( dimenzije = (1,1,1), pozicija = (0,0,0), rotacija = (0,0,0), centriraj = True, rezolucija = 32 ):
    return Objekt(
        dimenzije = dimenzije,
        pozicija = pozicija,
        rotacija = rotacija,
        centriraj = centriraj,
        GeometrijskoTijelo = 'STOZAC',
        rezolucija = rezolucija
    )

def Valjak( dimenzije = (1,1,1), pozicija = (0,0,0), rotacija = (0,0,0), centriraj = True, rezolucija = 32 ):
    return Objekt(
        dimenzije = dimenzije,
        pozicija = pozicija,
        rotacija = rotacija,
        centriraj = centriraj,
        GeometrijskoTijelo = 'VALJAK',
        rezolucija = rezolucija
    )


def PostojeciObjekt(objekt):
    return Objekt(objekt = objekt)
    



##== ispod su proceduralne funkcije koje se ponasaju kao wrapperi za objektne funkcije ==##
# npr. za nesto sto se ispod haube poziva sa a.Extrudiraj,
# korisnik ce to pozvati sa Extrudiraj(a)

def ProvjeriIspravnostUnesenogObjekta(objekt):
    '''
    Provjeri je li argument tipa Objekt.
    '''
    try:
        assert objekt != None
        #assert type(objekt) in {Objekt, Kocka, Stozac, Valjak, Kugla, PostojeciObjekt}
        assert type(objekt) in {Objekt, PrazanObjekt} 
        return True
    except AssertionError:
        return False

def JeLiOvaVarijablaTipa_PrazanObjekt(objekt):
    try:
        assert objekt != None
        assert type(objekt) in {PrazanObjekt} 
        return True
    except AssertionError:
        return False    

def TranslatirajGeometriju(objekt = None, pomak = (0,0,0), os_pomaka = 'NORMAL'):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.TranslatirajGeometriju(pomak = pomak, os_pomaka = os_pomaka)
    return True

def RotirajGeometriju(objekt = None, rotacija = (0,0,0),  os_pomaka = 'NORMAL'):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.RotirajGeometriju(pomak = rotacija, os_pomaka = os_pomaka)
    return True

def SkalirajGeometriju(objekt = None, faktor = (1,1,1),  os_pomaka = 'NORMAL'):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SkalirajGeometriju(pomak = faktor, os_pomaka = os_pomaka)
    return True

def CentrirajObjektPoVolumenu(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    return objekt.CentrirajObjekt(tip = 'ORIGIN_CENTER_OF_VOLUME')

def CentrirajObjektPoPovrsini(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    return objekt.CentrirajObjekt(tip = 'ORIGIN_CENTER_OF_MASS')



def OPERATOR_Ekstrudiraj(objekt = None, pomak = (0,0,0), os_pomaka = 'NORMAL', pomakniDoKursora = False, selekcijaTocaka = None):
    '''
    OPERATOR_Ekstrudiraj selektiranu geometriju.
    Ako je pomakniDoKursora == DA, pomak se ignorira i geometrija se pomice do kursora.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.OPERATOR_Ekstrudiraj(pomak = pomak, os_pomaka = os_pomaka, pomakniDoKursora = pomakniDoKursora, selekcijaTocaka = selekcijaTocaka)
    return True

def OPERATOR_Ekstrudiraj_Mnogostruko(objekt = None, pomak = (0,0,0), os_pomaka = 'NORMAL', pomakniDoKursora = False, selekcijaTocaka = None ):
    '''
    OPERATOR_Ekstrudiraj selektiranu geometriju na nacin da se ne stvara nova nemnogostruka geometrije.
    Ako je pomakniDoKursora == DA, pomak se ignorira i geometrija se pomice do kursora.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.OPERATOR_Ekstrudiraj_Mnogostruko(pomak = pomak, os_pomaka = os_pomaka, pomakniDoKursora = pomakniDoKursora, selekcijaTocaka = selekcijaTocaka)
    return True

def DuplicirajGeometriju(objekt = None, pomak = (0,0,0), os_pomaka = 'NORMAL', pomakniDoKursora = False, selekcijaTocaka = None ):
    '''
    Dupliciraj selektiranu geometriju (slicno ekstrudiranju, samo sto nova geometrija nije povezana sa starom).
    Ako je pomakniDoKursora == DA, pomak se ignorira i geometrija se pomice do kursora.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.DuplicirajGeometriju(pomak = pomak, os_pomaka = os_pomaka, pomakniDoKursora = pomakniDoKursora, selekcijaTocaka = selekcijaTocaka)
    return True


def Izvedi_Inset(objekt = None, Debljina = 0, Dubina = 0, SelektirajNovuGeometriju = False):
    '''
    Ekvivalentno Inset operaciji unutar grafičkog sučelja - unutar jedne plohe se generira nova, koncentricna ploha.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Izvedi_Inset(Debljina = Debljina, Dubina = Dubina, SelektirajNovuGeometriju = SelektirajNovuGeometriju)
    return True

def Izvedi_Outset(objekt = None, Debljina = 0, Dubina = 0, SelektirajNovuGeometriju = False):
    '''
    Slicno inset operaciji, samo sto je stvorena geometrija povrsinom veca, u usporedbi s Inset operacijom gdje je stvorena geometrija manja povrsinom.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Izvedi_Outset(self, Debljina = Debljina, Dubina = Dubina, SelektirajNovuGeometriju = SelektirajNovuGeometriju)
    return True



def Prepolovi(
        objekt = None,
        Ravnina_Tocka   = (0,0,0),
        Ravnina_Normala = (0,0,0),
        PopuniRez = False
    ):
    '''
    Prepolovi objekt po ravnini koja odgovara zadanim koordinatama.
    Ekvivalentno Bisect funkciji iz grafičkog sučelja.
    Funkcija razdvaja postojeci 3D model na dva 3D modela i vraca tuple na oba modela.
    
    Napomena: zbog ogranicenja unutar Blendera, argument Ravnina_Normala nije moguce unijeti u stupnjevima kao i svaki drugi vector.
    Umjesto (x,y,z) gdje x,y,z ∈ [0°,360°],
    u ovoj specificnoj funkciji vrijedi x,y,z ∈ [-1,1], gdje se [-1,1] preslikava u [-45°,45°].
    
    Napomena 2: tijekom izvodenja, funkcija selektiru svu geometriju na objektu i vraca selekciju na prijasnje stanje - osim ako je funkcija pozvana iz edit modea. U tom slucaju nije moguce vratiti selekciju i nakon izvodenja sva geometrija ce biti selektirana
    
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    
    duplikat = objekt.objekt.copy();
    duplikat.data = duplikat.data.copy()
    bpy.context.scene.collection.objects.link(duplikat);
    #bpy.context.view_layer.objects.active = duplikat;
    duplikat_OOP = PostojeciObjekt( duplikat );
    
    
    objekt.Prepolovi(
        Ravnina_Tocka   = Ravnina_Tocka,
        Ravnina_Normala = Ravnina_Normala,
        PopuniRez = PopuniRez,
        IzbrisiUnutarnjuGeometriju  = True,
        IzbrisiVanjskuGeometriju    = False
    );
    
    


    duplikat_OOP.Prepolovi(
        Ravnina_Tocka   = Ravnina_Tocka,
        Ravnina_Normala = Ravnina_Normala,
        PopuniRez = PopuniRez,
        IzbrisiUnutarnjuGeometriju  = False,
        IzbrisiVanjskuGeometriju    = True
    );
    

    
    return (objekt, duplikat_OOP)


def IzgladiRubove(objekt : Objekt = None, NacinRada : str = 'EDGES', Sirina : int = 0, BrojSegmenata : int = 1):
    '''
    Ekvivalentno Bevel operaciji iz grafičkog sučelja.
    Funkcija izgladuje rubove selektirane plohe.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.IzgladiRubove(
        NacinRada = NacinRada,
        Sirina = Sirina,
        BrojSegmenata = BrojSegmenata
    )
    return


def Ploha_IzaberiTocku_Normala(objekt = None, izbor = {'LIJEVO_DOLJE'}, ZbrojiSPostojecomSelekcijom = False ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Ploha_IzaberiTocku_Normala(
        izbor = izbor,
        ZbrojiSPostojecomSelekcijom = ZbrojiSPostojecomSelekcijom
    )
    return True

def Ploha_IzaberiRub_Normala(objekt = None, izbor = {'LIJEVO'}, ZbrojiSPostojecomSelekcijom = False ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Ploha_IzaberiRub_Normala(
        izbor = izbor,
        ZbrojiSPostojecomSelekcijom = ZbrojiSPostojecomSelekcijom
    )
    return True


def Ploha_IzaberiSusjednuPlohu(objekt = None, izbor = {'LIJEVO'}, ZbrojiSPostojecomSelekcijom = False ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Ploha_IzaberiSusjednuPlohu(
        izbor = izbor,
        ZbrojiSPostojecomSelekcijom = ZbrojiSPostojecomSelekcijom
    )
    return True



def SelektirajSljedeci(objekt = None, BrojKoraka = 1):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SelektirajSljedeci(
        BrojKoraka = BrojKoraka
    )
    return True

def SelektirajPrethodni(objekt = None, BrojKoraka = 1):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SelektirajPrethodni(
        BrojKoraka = BrojKoraka
    )
    return True

def Deselektiraj_Sahovnica(objekt = None, PreskociSvakuNtuPlohu = 1, SelektirajSvakuNtuPlohu = 1, Pomak = 0):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Deselektiraj_Sahovnica(
        PreskociSvakuNtuPlohu = PreskociSvakuNtuPlohu,
        SelektirajSvakuNtuPlohu = SelektirajSvakuNtuPlohu,
        Pomak = Pomak
    )
    return True

def SelektirajNemnogostrukePlohe(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SelektirajNemnogostrukePlohe()
    return True


def SelektirajSve(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SelektirajSve()
    return True

def DeselektirajSve(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.DeselektirajSve()
    return True

def SelektirajVise(objekt = None, UkljuciDijagonalnePlohe = False):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SelektirajVise( UkljuciDijagonalnePlohe = UkljuciDijagonalnePlohe)
    return True

def SelektirajManje(objekt = None, UkljuciDijagonalnePlohe = False):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.SelektirajManje( UkljuciDijagonalnePlohe = UkljuciDijagonalnePlohe)
    return True


def PostaviSelekcijuTocaka(objekt = None, selekcijaTocaka = None, ZbrojiSPostojecomSelekcijom = False):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.PostaviSelekcijuTocaka(
        selekcijaTocaka = selekcijaTocaka,
        ZbrojiSPostojecomSelekcijom = ZbrojiSPostojecomSelekcijom
    )
    return True




def Translatiraj( objekt = None, translacija = (0,0,0) ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Translatiraj(translacija = translacija)
    
def Pozicija( objekt = None, pozicija = (0,0,0)  ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Pozicija(pozicija = pozicija)

def Rotacija_Apsolutna( objekt = None, rotacija = (0,0,0)  ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Rotacija_Apsolutna( rotacija = rotacija  )

def Rotacija_Relativna( objekt = None, rotacija = (0,0,0)  ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Rotacija_Relativna( rotacija = rotacija  )

def Dimenzioniraj( objekt = None, dimenzije = (0,0,0)  ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Dimenzioniraj(dimenzije = dimenzije)

def Skaliraj( objekt = None, skala = (1,1,1)  ):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    objekt.Skaliraj(skala = skala)


def DohvatiDimenzije(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    return objekt.DohvatiDimenzije()

def DohvatiPoziciju(objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    return objekt.DohvatiPoziciju()

def Krivulja(objekt, *args,
        SkalirajKrivulju = None,
        OsDeformacije = 'Z'
        #DuljinaHandlea = 250
        #UnistiKrivulju = True
    ):
    '''
    Iskrivljuje objekt po Bezierovoj krivulji koja je konstruirana iz tocaka iz argumenta.
    Sve tocke trebaju biti tipa tuple i duljine 3.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    return objekt.Krivulja( *args,
        SkalirajKrivulju = SkalirajKrivulju,
        OsDeformacije = OsDeformacije
        #DuljinaHandlea = DuljinaHandlea,
        #UnistiKrivulju = UnistiKrivulju
    )

def Kruznica(objekt,
    OsDeformacije = 'Z',
    SkalirajKrivulju = None,
    SkalirajObjekt = None,
    #UnistiKrivulju = True,
    RotacijaObjekta = (0,0,0)
):
    return objekt.Kruznica(
        OsDeformacije = OsDeformacije,
        SkalirajKrivulju = SkalirajKrivulju,
        SkalirajObjekt = SkalirajObjekt,
        #UnistiKrivulju = UnistiKrivulju,
        RotacijaObjekta = RotacijaObjekta
    )



def Unija(objekt = None, target = None, sacuvajTarget = True):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    assert ProvjeriIspravnostUnesenogObjekta(target) == True
    objekt.Unija( target = target, sacuvajTarget = sacuvajTarget)

def Presjek(objekt = None, target = None, sacuvajTarget = True):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    assert ProvjeriIspravnostUnesenogObjekta(target) == True
    objekt.Presjek( target = target, sacuvajTarget = sacuvajTarget)

def Razlika(objekt = None, target = None, sacuvajTarget = True):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    assert ProvjeriIspravnostUnesenogObjekta(target) == True
    objekt.Razlika( target = target, sacuvajTarget = sacuvajTarget)



##== ispod su neke funkcije koje pojednostavljuju ceste radnje ==##
# npr. umjesto obj = bpy.data.objects['Plane'], korisnik moze pozvati
# DohvatiObjekt('Plane')



def DohvatiObjektUSceni(ime_objekta : str = None, ime_scene : str = None) -> Optional[Objekt]:
    '''
    Ako scena nije navedena, objekt se trazi u aktivnoj sceni.
    Ako je navedena scena, objekt se trazi u navedenoj sceni.
    '''
    assert ime_objekta != None
    try:
        bpy.data.objects[ime_objekta]
    except KeyError:
        print("Nesto ne valja, objekt ne postoji u tekucoj .blend datoteci")
        return None
    
    
    if ime_scene == None:
        try:
            objekt = bpy.context.scene.objects[ime_objekta]
            return PostojeciObjekt(objekt)
        except KeyError:
            print("Nesto ne valja, objekt ne postoji u aktivnoj sceni")
            return None
    
    elif ime_scene != None:
        try:
            objekt = bpy.data.scenes[ime_scene].objects[ime_objekta]
            return PostojeciObjekt(objekt)
        except KeyError:
            print("Nesto ne valja, objekt ne postoji u navedenoj sceni")
            return None

''' #TODO
def DohvatiObjektUKolekciji(ime_objekta : str = None, ime_kolekcije : str = None) -> Optional[Objekt]:
    #TODO
    pass
    return None
'''

def DohvatiObjekt(ime_objekta : str = None) -> Optional[Objekt]:
    '''
    Dohvati objekt trazenog imena, pri cemu se ne uzima u obzir u kojoj je sceni objekt.
    '''
    assert ime_objekta != None
    try:
        objekt = bpy.data.objects[ime_objekta]
    except KeyError:
        print("Nesto ne valja, objekt ne postoji u tekucoj .blend datoteci")
        return None
    
    # provjeri je li objekt postoji u aktivnoj sceni
    # ovo ne utjece na izvrsenje programa, samo daje korisniku Warning
    try:
        bpy.context.scene.objects[ime_objekta]
    except KeyError:
        #raise Warning("Oprez, objekt postoji u .blend datoteci ali ne i u aktivnom view layeru odnosno sceni")
        warnings.warn("Oprez, objekt postoji u .blend datoteci ali ne i u aktivnom view layeru odnosno sceni")
    return PostojeciObjekt(objekt)


def PostaviAktivanObjekt(objekt = None) -> bool:
    '''
    Ekvivalentno selektiranju objekta u grafickom sucelju.
    Korisnik moze kao argument predati ili objekt ili ime trazenog objekta.
    Vraca True ako je uspjelo, inace False.
    
    Mozda bi bilo 'ispravnije' nazvati funkciju 'SelektirajObjekt()', ali ovako je konzistentno s OOP paradigmom.
    '''
    #print("Tip varijable objekt:" + str(type(objekt)))
    
    try:
        assert objekt != None
    except AssertionError:
        raise Exception("Dobio sam None kao argument!")
        return False
    
    
    try:
        # dobili smo ime objekta
        assert type(objekt) == str
        ime_objekta = objekt
    except AssertionError:
        # dobili smo objekt a ne string
        #print("tip objekta unutar PostaviAktivanObjekt(): " + str(type(objekt)))
        if ProvjeriIspravnostUnesenogObjekta(objekt) == True:
            ime_objekta = objekt.objekt.name
        elif type(objekt) == bpy.types.Object:
            ime_objekta = objekt.name
        else:
            raise Exception("Nesto ne valja, nisam dobio validan objekt")
        #except Exception:
        #    print("Nesto ne valja, nisam dobio niti ime objekta niti varijablu tipa PostojeciObjekt")
    
    assert type( ime_objekta ) == str
    
    try:
        povrat = bpy.context.scene.objects[ime_objekta]
    except KeyError:
        povrat = bpy.data.objects[ime_objekta]
        #raise Warning("Ne mogu selektirati, vracam se iz funkcije. Objekt postoji u .blend datoteci ali ne i u tekucem view layeru odnosno sceni")
        warnings.warn("Ne mogu selektirati, vracam se iz funkcije. Objekt postoji u .blend datoteci ali ne i u tekucem view layeru odnosno sceni")
        return False
    except Exception:
        #raise Warning("Ne mogu selektirati, objekt ne postoji u .blend datoteci.")
        warnings.warn("Ne mogu selektirati, objekt ne postoji u .blend datoteci.")
        return False
    
    assert povrat != None
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    povrat.select_set(True)
    bpy.context.view_layer.objects.active = povrat
    return True
    
    


def DohvatiAktivanObjekt() -> Optional[Objekt]:
    try:
        objekt = bpy.context.active_object
        return PostojeciObjekt(objekt)
    except Exception:
        print("Nesto ne valja, nijedan objekt u sceni nije aktivan")
        return None


def DohvatiImeObjekta(objekt : Objekt = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    return objekt.objekt.name

def PostaviImeObjekta(objekt : Objekt = None, ime : str = None):
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    assert type(ime) == str
    assert ime != None
    assert ime != ''
    
    objekt.name = ime
    
    # moze se dogoditi da vec postoji objekt s istim imenom koje korisnik zeli postaviti,
    # pa se objekt koji zelimo imenovati s "ime" zapravo zove "ime.001" ili slicno
    # provjeri je li to slucaj
    
    if objekt.name == ime:
        return True
    else:
        #raise Warning("Upozorenje: vec postoji objekt s trazenim imenom, pa se objekt zapravo zove " + str(objekt.name))
        warnings.warn("Upozorenje: vec postoji objekt s trazenim imenom, pa se objekt zapravo zove " + str(objekt.name))
        return False


def DuplicirajObjekt(objekt : Objekt = None) -> Optional[Objekt]:
    '''
    Dupliciraj objekt i stavi ga u sve kolekcije u kojima i originalni objekt zivi.
    '''
    assert ProvjeriIspravnostUnesenogObjekta(objekt) == True
    
    objekt_bpy = objekt.objekt
    povrat = objekt_bpy.copy()
    povrat.data = povrat.data.copy()
    
    KolekcijeUKojimaSeOvajObjektPojavljuje = objekt_bpy.users_collection
    for kol in KolekcijeUKojimaSeOvajObjektPojavljuje:
        kol.objects.link(povrat)
    
    return PostojeciObjekt(povrat)

class PRIVATE_KolekcijaObjekata:
    '''
    Klasa sadrzi svojstvo lista, koje sadrzi listu objekata tipa Objekt.
    Ovu klasu korisnik ne bi trebao direktno pozivati iz konzole ili koda.
    '''
    
    def PRIVATE_DodajClanUListu(self, argument, UkljuciRekurzivneKolekcije = False) -> bool:
        '''
        Funkcija prima jedan pojedinacan argument i pokusava ga dodati u self.lista ako postoje uvjeti za to.
        '''
        if type(argument) == bpy.types.Object:
            self.lista.append( PostojeciObjekt( argument ) )
        elif type(argument) == bpy.types.Collection:
            #print("Ovaj dio posla se obavlja u svakom slucaju")
            kolekcija = argument
            for obj in kolekcija.objects:
                #print("ime objekta: " + obj.name)
                self.lista.append( PostojeciObjekt( obj ) )
            
            
            if UkljuciRekurzivneKolekcije == True:
                #print("... a ovaj jos dodatno ako treba uzeti u obzir rekurzivnu djecu")
                for kol in kolekcija.children_recursive:
                    for obj in kol.objects:
                        self.lista.append( PostojeciObjekt( obj ) )
        
        elif type(argument) == Objekt:
            self.lista.append(argument)
        else:
            warnings.warn("Nesto ne valja s argumentom " + str(argument) + ", ne mogu ga dodati u kolekciju")
            return False
        return True
    
    def PRIVATE_Konstruktor(
        self,
        *args,
        **kwargs
    ):
        
        # obidi svaki argument koji postoji u args i kwargs,
        # i probaj ga dodati u listu ako je to izvedivo
        
        for argument in args:
            if type(argument) in {set, list, tuple}:
                for clan in argument:
                    assert self.PRIVATE_DodajClanUListu(clan) == True
            else:
                assert self.PRIVATE_DodajClanUListu(argument) == True
        
        # sve isto kao gornja for petlja
        # samo sto se obilazi kwargs umjesto args
        for argument in kwargs.items():
            if type(argument) in {set, list, tuple}:
                for clan in argument:
                    assert self.PRIVATE_DodajClanUListu(clan) == True
            else:
                assert self.PRIVATE_DodajClanUListu(argument) == True
        
        
        


    def __init__(
        self,
        *args,
        **kwargs
    ):
        self.lista = []
        
        self.PRIVATE_Konstruktor(
            *args,
            **kwargs
        )
    
        for clan in self.lista:
            assert type(clan) == Objekt

    def DohvatiListuObjekata(self) -> list:
        return self.lista
    

    def PostaviListuObjekata(self, *args, **kwargs):
        self.lista = []
        
        self.PRIVATE_Konstruktor(
            *args,
            **kwargs
        )
    
        for clan in self.lista:
            assert type(clan) == Objekt


    def DodajUListuObjekata(self, *args, **kwargs):
        #self.lista = []
        
        self.PRIVATE_Konstruktor(
            *args,
            **kwargs
        )
    
        for clan in self.lista:
            assert type(clan) == Objekt


    def DohvatiObjektPoImenu(self, trazeno_ime : str = None) -> Optional[Objekt]:
        assert trazeno_ime != None
        assert trazeno_ime != ''
        
        for obj in self.lista:
            if DohvatiImeObjekta(obj) == trazeno_ime:
                return obj
            else:
                continue
        
        # prosao sam cijelu listu i nisam nasao Objekt trazenog imena
        warnings.warn("U ovoj kolekciji ne postoji objekt trazenog imena")
        return None
    
    
    '''
    def DodajObjektUKolekciju(self, objekt : Objekt = None) -> bool:
        try:
            assert ProvjeriIspravnostUnesenogObjekta(objekt)
        except AssertionError:
            warnings.warn("Trazeni objekt nije tipa Objekt, ne mogu ga dodati u kolekciju")
            return False
        
        self.lista.append(objekt)
        return True
    '''


    def PoredajObjekteAbecedno_Uzlazno(self) -> list:
        '''
        Listu unutar objekta sortiraj abecedno po imenu, uzlazno, i vrati novu listu.
        '''
        self.lista.sort( key = DohvatiImeObjekta )
        return self.lista

    
    def PoredajObjekteAbecedno_Silazno(self) -> list:
        '''
        Listu unutar objekta sortiraj abecedno po imenu, silazno, i vrati novu listu.
        '''
        self.lista.sort( key = DohvatiImeObjekta, reverse = True )
        return self.lista
    



### TODO ###
# funkcije ispod su proceduralni omotaci za PRIVATE_KolekcijaObjekata i sve pripadne metode
def KolekcijaObjekata(*args, **kwargs):
    return PRIVATE_KolekcijaObjekata(*args, **kwargs)


def DohvatiListuObjekata(Kolekcija_argument) -> list:
    #print("Kolekcija_argument: "    + str(Kolekcija_argument)   )
    
    assert type(Kolekcija_argument) == PRIVATE_KolekcijaObjekata
    return Kolekcija_argument.DohvatiListuObjekata()

def PostaviListuObjekata(Kolekcija_argument, *args, **kwargs):
    assert type(Kolekcija_argument) == PRIVATE_KolekcijaObjekata
    return Kolekcija_argument.PostaviListuObjekata(*args, **kwargs)


def DodajUListuObjekata(Kolekcija_argument, *args, **kwargs):
    #print("Kolekcija_argument: "    + str(Kolekcija_argument)   )
    #print("*args:  "                + str(*args             )   )
    #print("**kwargs:  "             + str(**kwargs          )   )
    
    assert type(Kolekcija_argument) == PRIVATE_KolekcijaObjekata
    return Kolekcija_argument.DodajUListuObjekata(*args, **kwargs)


def DohvatiObjektPoImenu(Kolekcija_argument, trazeno_ime : str = None) -> Optional[Objekt]:
    assert type(Kolekcija_argument) == PRIVATE_KolekcijaObjekata
    return Kolekcija_argument.DohvatiObjektPoImenu(*args, **kwargs)


def PoredajObjekteAbecedno_Uzlazno(Kolekcija_argument) -> list:
    assert type(Kolekcija_argument) == PRIVATE_KolekcijaObjekata
    return Kolekcija_argument.PoredajObjekteAbecedno_Uzlazno()

def PoredajObjekteAbecedno_Silazno(Kolekcija_argument) -> list:
    assert type(Kolekcija_argument) == PRIVATE_KolekcijaObjekata
    return Kolekcija_argument.PoredajObjekteAbecedno_Silazno()


def PRIVATE_IscupajKolekcijuPoImenuIzListeKolekcija(lista_kolekcija : list = None, trazeno_ime : str = None) -> Optional[bpy.types.Collection]:
    '''
    Ovu funkciju korisnik u teoriji moze pozivati, ali nije preporucljivo s obzirom da se oslanja na bpy.data sintaksu koju korisnik vjerojatno ne poznaje.
    '''
    try:
        assert lista_kolekcija != None
        assert type(lista_kolekcija) == list
        
        assert trazeno_ime != None
        assert trazeno_ime != ''
        assert type(trazeno_ime) == str
        
        for kol in lista_kolekcija:
            print("Trenutni kol koji obilazim: " + str(kol.name))
            if kol.name == trazeno_ime:
                return kol
            else:
                continue

        warnings.warn("Kolekcija trazenog imena ne postoji u ovoj listi")        
        return None
    
    except AssertionError:
        raise Exception("Nesto ne valja s ovom listom kolekcija")

'''
### TODO
def DohvatiKolekcijuUSceni(
    ime_kolekcije: str = None,
    UkljuciRekurzivneKolekcije = False,
    ime_scene : str = None
    ) -> Optional[PRIVATE_KolekcijaObjekata]:
    
    
    Ako scena nije navedena, kolekcija se trazi u aktivnoj sceni.
    Ako je navedena scena, kolekcija se trazi u navedenoj sceni.
    
    Funkcija vraca kolekciju objekata tipa Objekt, gdje su sadrzani svi objekti iz kolekcije.
    
    
    assert ime_kolekcije != None
    try:
        bpy.data.collections[ime_kolekcije]
    except KeyError:
        print("Nesto ne valja, kolekcija ne postoji u tekucoj .blend datoteci")
        return None
    
    
    if ime_scene == None:
        try:
            #povrat = bpy.context.scene.objects[ime_kolekcije]
            #povrat = bpy.context.scene.collection.children_recursive[ime_kolekcije] # od svih kolekcija u sceni, nadi onu s imenom <ime_kolekcije>
            kolekcija = PRIVATE_IscupajKolekcijuPoImenuIzListeKolekcija(
                lista_kolekcija = bpy.context.scene.collection.children_recursive,
                trazeno_ime = ime_kolekcije
            )
        except KeyError:
            print("Nesto ne valja, kolekcija ne postoji u aktivnoj sceni")
            return None
    
    elif ime_scene != None:
        try:
            #objekt = bpy.data.scenes[ime_scene].objects[ime_kolekcije]
            #kolekcija = bpy.data.scenes[ime_scene].collection.children_recursive[ime_kolekcije]
            kolekcija = PRIVATE_IscupajKolekcijuPoImenuIzListeKolekcija(
                lista_kolekcija = bpy.data.scenes[ime_scene].collection.children_recursive,
                trazeno_ime = ime_kolekcije
            )
            
            #return PostojeciObjekt(objekt)
            #return PRIVATE_KolekcijaObjekata(kolekcija) ###TODO staviti nesto u return
        except KeyError:
            print("Nesto ne valja, kolekcija ne postoji u navedenoj sceni")
            return None
    
    return PRIVATE_KolekcijaObjekata(
                kolekcija = kolekcija,
                UkljuciRekurzivneKolekcije = UkljuciRekurzivneKolekcije
            )
'''

'''
### TODO
def DohvatiKolekciju(
    ime_kolekcije : str = None,
    UkljuciRekurzivneKolekcije = False
    ) -> Optional[PRIVATE_KolekcijaObjekata]:
    
    Dohvati kolekciju trazenog imena, pri cemu se ne uzima u obzir u kojoj je sceni objekt.
    
    assert ime_kolekcije != None
    try:
        #objekt = bpy.data.objects[ime_objekta]
        kolekcija = bpy.data.collections[ime_kolekcije]
    except KeyError:
        print("Nesto ne valja, kolekcija ne postoji u tekucoj .blend datoteci")
        return None
    
    # provjeri je li objekt postoji u aktivnoj sceni
    # ovo ne utjece na izvrsenje programa, samo daje korisniku Warning
    try:
        #bpy.context.scene.objects[ime_objekta]
        #bpy.context.scene.collection.children_recursive[ime_kolekcije]
        assert PRIVATE_IscupajKolekcijuPoImenuIzListeKolekcija(
                lista_kolekcija = bpy.context.scene.collection.children_recursive,
                trazeno_ime = ime_kolekcije
        ) != None
    except AssertionError:
        #raise Warning("Oprez, objekt postoji u .blend datoteci ali ne i u aktivnom view layeru odnosno sceni")
        warnings.warn("Oprez, kolekcija postoji u .blend datoteci ali ne i u aktivnom view layeru odnosno sceni")
    
    return PRIVATE_KolekcijaObjekata(
                kolekcija = kolekcija,
                UkljuciRekurzivneKolekcije = UkljuciRekurzivneKolekcije
            )
'''




'''
def Ispisi(ispis) -> None:
    print(str(ispis))
    return
'''

def String(ulaz):
    return str(ulaz)

def DecimalniBroj(ulaz):
    return float(ulaz)

def CijeliBroj(ulaz):
    return int(ulaz)

def TipVarijable(ulaz):
    return type(ulaz)
