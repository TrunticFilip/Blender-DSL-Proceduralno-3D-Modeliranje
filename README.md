# Blender DSL za proceduralno 3D modeliranje
Ovaj domenski jezik, koji sam izradio za diplomski rad, omogućuje proceduralno 3D modeliranje putem koda, slično OpenSCAD jeziku. Korisnik može kroz kod iscrtavati pojedinačne vertexe, edgeve i faceove, stvarati Blenderove ugrađene primitivne objekte, izvoditi Boolean operatore itd.
Iako je DSL prvenstveno usmjeren na proceduralno 3D modeliranje, moguće je proširiti opseg programa s dodatnim, vlastitim funkcionalnostima.

Glavna prednost ovog DSL-a jest da, za razliku od ugrađenog API-a, nije potrebno dubinsko poznavanje kompletne Blender API arhitekture, a moguće je obaviti gotovo isti posao.

U prijevodu, jedan podskup Blender API-a se kroz ovaj program prezentira na način jednostavniji prosječnom korisniku Blendera, a ciljani use case je 3D modeliranje putem koda.


## Upute za korištenje:
- text datablock naziva 'PokreniMe.py' (referencira se na datoteku `PokreniMe.py`) - pokretanjem ove skripte izvršava se kod u DSL-u
- text datablock naziva 'KOD' - sadrži kod DSL-a koji se izvršava
- text datablock naziva 'module_OOP.py' (referencira se na datoteku `module_OOP.py`) - sadrži svu programsku logiku koja se u KOD može koristiti kao modul

Nekoliko pokaznih primjera nalazi se u folderu `primjeri`. Popis svih prevedenih ključnih riječi i operatora nalazi se u PokreniMe.py u `RJECNIK_KLJUCNIH_RIJECI`. Moguće je dodavati i nove članove u navedenu varijablu, pod pretpostavkom da postoje u Pythonu (DSL je ostvaren kroz sloj predprocesiranja koda u KOD gdje se izvorne, postojeće ključne riječi prevode u odgovarajući pojam koji je naveden u `RJECNIK_KLJUCNIH_RIJECI`. Nije moguće prevesti nešto što ne postoji in the first place.)

### Popis dostupnih funkcija:

<details>
<summary>Popis 1</summary>
<table>
<tr><td>Popis funkcija</td></tr>
<tr><td> <code> Kugla( dimenzije =  (1,1,1), pozicija =  (0,0,0), rotacija =  (0,0,0), centriraj =  Da, rezolucija =  32  ) </code> <br><br> <b>Opis</b>: Stvara objekt u obliku kugle pozivajući se na Blenderove ugrađene primitivne objekte. Povratna vrijednost je objekt stvoren pozivom ove funkcije.  <br> <br>
<b>Parametri</b>:
<ul>
	<li> dimenzije: tročlani tuple gdje svaki član mora biti tipa int ili float. Parametar opisuje dimenziju po x,y odnosno z osi izraženu u milimetrima</li>
	<li> pozicija: tročlani tuple gdje svaki član mora biti tipa int ili float, određuje početne (x,y,z) koordinate stvorenog objekta u prostoru</li>
	<li> rotacija - tročlani tuple gdje svaki član mora biti tipa int ili float, određuje početnu rotaciju objekta u stupnjevima </li>
	<li> centriraj - Da/Ne Bool vrijednost koja, ukoliko istinita, postavlja pozicijske koordinate na takav način da se centar objekta nalazi u središtu koordinatnog sustava </li>
	<li> rezolucija - int broj veći od nule, određuje broj poligona koji se nalaze na najkraćem obilasku oko objekta, slično $fn parametru u OpenSCAD domenskom jeziku </li>
</ul>
<b>Povratni tip</b>: Objekt <br> <br>
-	<code>Kocka(…)</code>, <code>Valjak(…)</code>, <code>Stozac(…)</code> – metode koje obavljaju funkcionalno isti posao kao Kugla(), uz razliku da je rezultirajući objekt u obliku kocke, valjka odnosno stožca. <code>Kocka()</code> je jedina od ovih metoda koja ne uvažava parametar rezolucija.
<br><br>
</td></tr>

<tr><td> <code> PostojeciObjekt(objekt) </code> <br><br> <b>Opis</b>: Stvara i vraća varijablu tipa Objekt na objekt koji već postoji u Blenderovom grafičkom sučelju, ali na kojega se korisnik još ne može programski referencirati. Dok Kugla(), primjerice, predstavlja programski omotač za Blenderove primitivne objekte, PostojeciObjekt(objekt) obavlja funkcionalno isti posao, samo što se radi o vlastitom, složenom objektu umjesto primitivnoga. <br> <br>
<b>Parametri</b>:
<ul> <li>objekt – trodimenzionalni model tipa bpy.types.Object na koji će se stvoreni Objekt referencirati </li>
</ul>
Povratni tip: Objekt <br> <br>
Primjer upotrebe:
<pre><code># u sceni već postoji objekt naziva 'ObjektKojiVecPostoji'
a = bpy.data.objects['ObjektKojiVecPostoji']
b = PostojeciObjekt(a)
</pre></code>
<br>
 </td></tr>

<tr><td> <code> Uvezi_STL(ApsolutnaPutanja = Nista) </code> <br><br> <b>Opis</b>: Uvozi .stl datoteku s navedenom apsolutnom putanjom. <br> <br>
Parametri:
<ul><li> ApsolutnaPutanja – string koji predstavlja putanju do .stl datoteke </ul></li>
<b>Povratni tip</b>: Objekt <br> <br>
</td></tr>

<tr><td> <code> Uvezi_SVG(ApsolutnaPutanja = Nista, Visina = 0.01, ListaZaSelektiranje = Nista) </code> <br><br>
<b>Opis</b>: Uvozi .svg datoteku s navedenom apsolutnom putanjom.
Parametri:
<ul>
<li>ApsolutnaPutanja – string koji predstavlja putanju do .stl datoteke
<li>Visina – visina 3D modela iscrtanog iz .svg datoteke, izražena u milimetrima
<li>ListaZaSelektiranje – popis imena pathova koji će biti odabrani prilimom uvoza, varijabla tipa list ili tuple
</ul>
<b>Povratni tip</b>: Objekt
<br><br>
</tr></td>

<tr><td> <code> Pozicija( objekt = Nista, pozicija = (0,0,0)  )</code> <br><br>
Opis: Postavlja objekt u pitanju na zadane koordinate u prostoru. <br><br>
Parametri:
<ul>
<li> objekt – objekt tipa Objekt 
<li> pozicija – tročlani tuple gdje je svaki član tipa int ili float
</ul>
Povratni tip: Ništa <br><br>
Primjer upotrebe:
<pre><code>a = Kocka() # u varijabli a nalazi se Objekt
Pozicija(a, pozicija = (1,2,3))
</code></pre>
<br>
 </td></tr>

<tr><td> <code> Rotacija_Apsolutna( objekt = Nista, rotacija = (0,0,0)  )</code> 
<br><br><b>Opis</b>: Postavlja rotaciju objekta na koordinate zadane u stupnjevima. <br><br> <b>Parametri</b>:
<ul>
<li>objekt – objekt tipa Objekt 
<li>rotacija - tročlani tuple gdje je svaki član tipa int ili float.
</ul>
Upotreba je ista kao i s <code>Pozicija( … )</code> metodom.
Također, postoji i metoda <code>Rotacija_Relativna</code> koja radi funkcionalno isti posao kao Rotacija_Apsolutna, uz razliku da relativna rotacija zbraja argument s postojećom rotacijom.
<br><br>
 </td></tr>

<tr><td> <code> Dimenzioniraj( objekt = Nista, dimenzije = (0,0,0)  )</code>
<br><br><b>Opis</b>: Postavlja dimenzije objekta na zadane.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – objekt tipa Objekt 
<li>rotacija - tročlani tuple gdje je svaki član tipa int ili float.
</ul>
<br><br>
</td></tr>

<tr><td> <code> Skaliraj( objekt = Nista, skala = (1,1,1) )</code> <br><br>
<b>Opis</b>: Umanjuje odnosno povećava skalu objekta za navedeni faktor.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – objekt tipa Objekt 
<li>skala - tročlani tuple gdje je svaki član tipa int ili float
</ul>
Upotreba je ista kao i s Pozicija( … ) metodom.
<br><br>
</td></tr>

<tr><td> <code> DohvatiDimenzije(objekt = Nista)</code> <br><br>
<b>Opis</b>: Dohvaća dimenzije traženog objekta u obliku tročlanog tuple objekta.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – traženi objekt tipa Objekt
</ul>
Povratni tip: tuple
<br><br>
</td></tr>

<tr><td> <code> DohvatiPoziciju(objekt = Nista)</code> <br><br>
<b>Opis</b>: Dohvaća poziciju traženog objekta u obliku tročlanog tuple objekta.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – traženi objekt tipa Objekt
</ul>
<br>
<b>Povratni tip</b>: tuple </td></tr>


<tr><td> <code> CentrirajObjektPoVolumenu(objekt = Nista)</code> <br><br>
<b>Opis</b>: Postavlja centar objekta u centar volumena.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – traženi objekt tipa Objekt
</ul>
Funkcija <code>CentrirajObjektPoPovrsini(objekt = Nista)</code> radi funkcionalno isti posao kao <code>CentrirajObjektPoVolumenu( … )</code>, uz razliku da se objekt centrira prema površini umjesto prema volumenu.
<br><br>
</td></tr>

<tr><td> <code> Unija(objekt = Nista, target = Nista, sacuvajTarget = Da) </code> <br><br> <b>Opis</b>: Izvršava operator unije nad objektom.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – prvi objekt tipa Objekt koji sudjeluje u operaciji, u objekt pod varijablom objekt pohranjuje se rezultat operacija
<li>target - drugi objekt tipa Objekt koji sudjeluje u operaciji
</ul>
Funkcije Razlika(…) i Presjek(…) obavljaju funkcionalno isti posao kao i Unija(…), uz razliku da se izvršavaju operacije razlike odnosno presjeka.
<br><br>
</td></tr>

<tr><td> <code> Kruznica(objekt, OsDeformacije = 'Z', SkalirajKrivulju = Nista, SkalirajObjekt = Nista, UnistiKrivulju = Da, RotacijaObjekta = (0,0,0) ) </code> <br><br>
<b>Opis</b>: Manipulira geometrijom objekta na taj način da ga se proba deformirati u oblik kružnice.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – objekt tipa Objekt koji se deformira
<li>OsDeformacije – os prema kojoj se objekt deformira po kružnici, str iz skupa {'X','Y','Z','-X','-Y','-Z'}
<li>SkalirajKrivulju – tročlani tuple gdje je svaki član tipa int ili float, skalira krivulju za navedeni faktor
<li>SkalirajObjekt – tročlani tuple gdje je svaki član tipa int ili float, skalira objekt za navedeni faktor
<li>UnistiKrivulju – bool vrijednost koja, ako Da, briše objekt krivulje
<li>RotacijaObjekta – tročlani tuple gdje je svaki član tipa int ili float, rotira objekt za navedeni faktor
</ul>
</td></tr>

<tr><td> <code> Krivulja(objekt, *args, SkalirajKrivulju = Nista, OsDeformacije = 'Z') </code> <br><br>
Opis: Manipulira geometrijom objekta na taj način da ga se proba deformirati u oblik Bezierove krivulje s navedenim točkama. Slično Kružnica(…) metodi, uz razliku da se geometrija deformira s obzirom na krivulju s proizvoljnim točkama, za razliku od unaprijed definirane kružnice.
Parametri:
<ul>
<li>objekt – objekt tipa Objekt koji se deformira
<li>SkalirajKrivulju – tročlani tuple gdje je svaki član tipa int ili float, skalira krivulju za navedeni faktor
<li>OsDeformacije – os prema kojoj se objekt deformira po krivulji, str iz skupa {'X','Y','Z','-X','-Y','-Z'}
</ul>
<br>
</td></tr>

<tr><td> <code> DuplicirajObjekt(objekt = Nista) </code> <br><br>
<tr><td> <b>Opis</b>: Stvara kopiju trodimenzionalnog modela te vraća objekt tipa Objekt koji se refencira na kopiju.<br>
<b>Parametri</b>:
<ul>
<li>objekt – objekt koji se duplicira
</ul>
<b>Povratni tip</b>: Objekt </td></tr>
<br><br>
</td></tr>

<tr><td> <code> DohvatiObjektUSceni(ime_objekta = Nista, ime_scene = Nista) </code> <br><br>
<tr><td><b>Opis</b>: Dohvaća objekt traženog imena, pri čemu je obim traženja ograničen na navedenu scenu. Ukoliko objekt traženog imena postoji ali nije u istoj sceni, metoda ga neće pronaći.<br>
Ako scena nije navedena, objekt se traži u aktivnoj sceni. Ako scena je navedena, objekt se traži u navedenoj sceni. <br><br>
Parametri:
<ul>
<li>ime_objekta – ime objekta koji se dohvaća
<li>ime_scene - ime scene u kojoj se traži objekt
</ul>
<b>Povratni tip</b>: Objekt
<br><br>
</td></tr>

<tr><td> <code> PostaviAktivanObjekt(objekt = Nista) </code> <br><br>
<b>Opis</b>: Dohvaća objekt traženog imena, pri čemu je obim traženja ograničen na navedenu scenu. Ukoliko objekt traženog imena postoji ali nije u istoj sceni, metoda ga neće pronaći.<br>
Ako scena nije navedena, objekt se traži u aktivnoj sceni. Ako scena je navedena, objekt se traži u navedenoj sceni.<br><br>
<b>Parametri</b>:
<ul>
<li>ime_objekta – ime objekta koji se dohvaća
<li>ime_scene - ime scene u kojoj se traži objekt
</ul>
<b>Povratni tip</b>: Objekt
<br><br>
</td></tr>

<tr><td> <code> DohvatiAktivanObjekt() </code> <br><br>
<b>Opis</b>: Dohvaća objekt koji je trenutno aktivan u grafičkom sučelju, u Objekt programskom omotaču.<br><br>
<b>Povratni tip</b>: Objekt
<br><br>
</td></tr>

<tr><td> <code> DohvatiImeObjekta(objekt = Nista) </code> <br><br>
<b>Opis</b>: Svaki objekt ima svoje ime u grafičkom sučelju, koje ne mora biti isto kao ime varijable u kodu. Metoda dohvaća ime objekta vidljivo u grafičkom sučelju.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – objekt tipa Objekt čije ime se traži
</ul>
<b>Povratni tip</b>: str
<br><br>
</td></tr>

<tr><td> <code> PostaviImeObjekta(objekt = Nista, ime = Nista) </code> <br><br>
<b>Opis</b>: Postavlja ime objekta vidljivo iz grafičkog sučelja, te vraća Da ako je objekt uspješno preimenovan. Dodatno, u konzolu ispisuje upozorenje ako već postoji objekt s istim imenom, s obzirom da u jednoj .blend datoteci ne mogu postojati dva različita objekta s istim imenom.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – objekt tipa Objekt čije ime se postavlja
<li>ime  - string koji predstavlja novo ime objekta
</ul>
<b>Povratni tip</b>: bool
<br><br><br>
</td></tr>
</table>
</details>

Sve do sada navedene metode  obavljale su se na objektu tipa `Objekt`. Sve daljnje metode pozivaju se na objektu tipa `PrazanObjekt`, koji nasljeđuje klasu `Objekt`. Posljedično, metode iz ovog potpoglavlja mogu se izvoditi samo na objektima tipa `PrazanObjekt`.

<details>
<summary>Popis 2</summary>
<table>
<tr><td> <code> StvoriPrazanObjekt(pozicija = (0,0,0), rotacija = (0,0,0)) </code> <br><br>
<b>Opis</b>: Stvara prazan objekt tipa PrazanObjekt s mogućnošću navođenja početne pozicije odnosno rotacije.<br><br>
<b>Parametri</b>:
<ul>
<li>pozicija - tročlani tuple gdje svaki član mora biti tipa int ili float, određuje početne (x,y,z) koordinate stvorenog objekta u prostoru
<li>rotacija - tročlani tuple gdje svaki član mora biti tipa int ili float, određuje početnu rotaciju objekta u stupnjevima
Povratni tip: PrazanObjekt
</ul>
<br><br>
</td></tr>

<tr><td> <code> StvoriTocku(objekt, pozicija, ime = Nista) </code> <br><br>
<b>Opis</b>: Stvara točku u navedenom objektu i vraća referencu na istu. Moguće je navesti ime koje se povezuje s točkom, ukoliko se referenca na točku izgubi.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt u kojoj se stvara točka
<li>pozicija – pozicijske koordinate na kojime se stvara točka
<li>ime – ime koje se povezuje s točkom
</ul>
<b>Povratni tip</b>: točka (<code>bmesh.types.BMVert</code>)

Primjer upotrebe:<br>
<pre><code>a = StvoriPrazanObjekt()
StvoriTocku(a, pozicija)
</code></pre>
<br>
</td></tr>

<tr><td> <code> StvoriRub(objekt, *args, ime = Nista) </code> <br><br>
<b>Opis</b>: Stvara rub iz navedenih točaka i vraća referencu na stvoreni rub. Moguće je navesti ime koje se povezuje s rubom, ukoliko se referenca na rub izgubi.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt u kojoj se stvara rub
<li>*args – točke iz kojih se stvara rub, mora ih biti točno dvije
<li>ime – ime koje se povezuje s rubom
</ul><br>
<b>Povratni tip</b>: rub (<code>bmesh.types.BMEdge</code>)
<br><br>
</td></tr>

<tr><td> <code> StvoriPlohu(objekt, *args, ime = Nista) </code> <br><br>
<b>Opis</b>: Stvara plohu iz navedenih točaka i vraća referencu na stvorenu plohu. Moguće je navesti ime koje se povezuje s plohom, ukoliko se referenca na plohu izgubi.
Potrebno je najmanje tri točke da bi se mogla stvoriti ploha.<br><br>
</td></tr>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt u kojoj se stvara ploha
<li>*args – točke iz kojih se stvara ploha, mora ih biti najmanje tri
<li>ime – ime koje se povezuje s plohom
<b>Povratni tip</b>: ploha (<code>bmesh.types.BMFace</code>)
<br><br>
</td></tr>

<tr><td> <code> EkstrudirajTocku(objekt, TockaPostojeca, offset, ImeNovogRuba = Nista, ImeNoveTocke = Nista) </code> <br><br>
<b>Opis</b>: Ekstrudira navedenu točku za offset u pozicijskim koordinatama i vraća rječnik koji sadrži reference na nastalu geometriju.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt u kojoj se stvaraju rubovi
<li>TockaPostojeca – točka koja se ekstrudira
<li>offset – tročlani tuple gdje je svaki član tipa int ili float
<li>ImeNovogRuba – ime koje se povezuje s novim rubom
<li>ImeNoveTocke – ime koja se povezuje s nastalom točkom
</ul><br>
<b>Povratni tip</b>: dict u obliku <code>{'NovaTocka' : nova_tocka, 'NoviRub' : novi_rub}</code>
<br><br>
</td></tr>

<tr><td> <code> EkstrudirajRub(objekt, RubPostojeci, offset, ImeNovogRuba = Nista, PopuniPlohu = Da) </code> <br><br>
<b>Opis</b>: Ekstrudira navedeni rubi vraća rječnik koji sadrži reference na nastalu geometriju.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt u kojoj se izvodi operacija ekstrudiranja
<li>RubPostojeci – rub koji se ekstrudira
<li>ImeNovogRuba – ime koje se povezuje s novim rubom
<li>PopuniPlohu – bool varijabla koja, ukoliko istinita, stvara plohu između postojećeg i novog ruba
</ul>
<b>Povratni tip</b>: dict u obliku <code>{'NoveTocke' : new_verts, NoviRub' : new_edge, 'NovaPloha' : new_face}</code>
<br><br>
</td></tr>

<tr><td> <code> DohvatiSveTockeIzPlohe(objekt, ploha) </code> <br><br>
<b>Opis</b>: Dohvaća sve točke iz navedene plohe.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt koji sadrži plohu u pitanju
<li>ploha – ploha koja sadrži tražene točke
</ul><br>
<b>Povratni tip</b>: uređena kolekcija točaka (<code>bmesh.types.BMVertSeq</code>)
<br><br>
</td></tr>

<tr><td> <code> DohvatiSveRuboveIzPlohe(objekt, ploha) </code> <br><br>
<b>Opis</b>: Dohvaća sve rubove iz navedene plohe.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt koji sadrži plohu u pitanju
<li>ploha – ploha koja sadrži tražene točke
</ul>
<br>
<b>Povratni tip</b>: uređena kolekcija rubova (<code>bmesh.types.BMEdgeSeq</code>)
<br><br>
</td></tr>

<tr><td> <code> IzracunajCentarTocaka(objekt, *args) </code> <br><br>
<b>Opis</b>: Vraća koordinatu koja odgovara aritmetičkoj sredini svih navedenih točaka.<br><br>
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt koja sadrži navedene točke
<li>*args – sve točke koje se uzimaju u obzir
</ul><br>
<b>Povratni tip</b>: tročlani tuple gdje je svaki član tipa int ili float

- Metoda <code>IzracunajCentarRuba(objekt, arg)</code> radi funkcionalno isti posao kao i <code>IzracunajCentarTocaka(objekt, *args)</code>, uz razliku da se radi o jednom rubu umjesto o više točaka.
<br><br>
</td></tr>

<tr><td> <code> Valjak_Iscrtavanje(objekt, Radijus, Visina, BrojPloha) </code> <br><br>
<b>Opis</b>: Iscrtava valjak bez oslanjanja na Blenderove ugrađene primitivne objekte.
<b>Parametri</b>:
<ul>
<li>objekt – varijabla tipa PrazanObjekt u kojoj se iscrtava valjak
<li>Radijus – radijus valjka, tipa int ili float
<li>Visina – visina valjka, tipa int ili float
<li>BrojPloha – broj ploha u valjku, tipa int
</ul>
<br>
</td></tr>
</table>
</details>
Za sve funkcije navedene u ovoj tablici, potrebno je pozvati funkciju <code>IzvediPromjene(objekt)</code> da bi se promjene iz navedenih funkcija zapravo primijenile. Također, funkcije koje mijenjaju poziciju, rotaciju ili dimenzije objekta, kao što su primjerice <code>Skaliraj()</code> i <code>Dimenzioniraj()</code>, neće ispravno raditi ukoliko su pozvane prije <code>IzvediPromjene(objekt)</code> .


## Što je API, i koji problem ovaj program rješava?
Neki posao koji se obavlja kroz defaultno, grafičko sučelje, često se može rješiti i kroz programsko sučelje, odnosno API.

Jedan elementaran primjer - u .blend fileu postoji jedna primitivna kocka naziva 'Kocka'. Potrebno je napraviti duplikat objekta (dva različita objecta koji se referenciraju na isti mesh) i translatirati ga za jedan metar po globalnoj X-osi.
### Grafičko sučelje:
Lijevi klik na traženu kocku -> Alt + D -> Enter -> G
 -> 1 -> Enter

### Programsko sučelje:
```python
import bpy
kocka_object = bpy.data.objects['Kocka'] # pod pretpostavkom da navedeni objekt u 3D viewportu ima naziv 'Kocka'
kocka_mesh = kocka_object.data

pomak = 2

kockaduplikat_object = kocka_object.copy()
kockaduplikat_mesh = kocka_mesh
bpy.context.scene.collection.objects.link(kockaduplikat_object)
kockaduplikat_object.location.x += pomak
```


Za jedan jednostavan primjer poput gore navedenog, grafičko sučelje radi posao intuitivno, na način na koji je poznat prosječnom Blender korisniku.
Međutim, što ako taj isti posao treba napraviti 100 puta, umjesto samo jednom?
Programsko sučelje zaobilazi upravo taj problem, na način da se posao izvrši putem koda. U prethodnom primjeru, u postupak se može staviti proizvoljan broj ponavljanja kroz for petlju, na način kako je prikazano u sljedećemn programskom bloku:

```python
import bpy
kocka_object = bpy.data.objects['Kocka'] # pod pretpostavkom da navedeni objekt u 3D viewportu ima naziv 'Kocka'
kocka_mesh = kocka_object.data

pomak = 2

broj_ponavljanja = 5
x_trenutni = kocka_object.location.x

for i in range(0, broj_ponavljanja):
    kockaduplikat_object = kocka_object.copy()
    kockaduplikat_mesh = kocka_mesh
    bpy.context.scene.collection.objects.link(kockaduplikat_object)
    kockaduplikat_object.location.x += pomak
    x_trenutni += pomak
    kockaduplikat_object.location.x = x_trenutni
```

Iz navedenoga je vidljivo da je programsko sučelje, odnosno API, samo programski način rješavanja grafičkog posla. Navedeno se u načelu može primijeniti i na puno drugih programa pored Blendera.

Jedna mana API-a jest da, koliko god je moćan i dobro razrađen, nije trivijalan za pohvatati. Prosječan korisnik Blendera ili sličnih programa je potkovan u 3D modeliranju, animiranju i sličnim vještinama, a malo slabije u programiranju.

Ovaj DSL doskače tom problemu i pokušava izvući best of both worlds - mogućnost programskog rješavanja posla i jednostavnost korištenja - uz uvjet da je ciljani use case trenutno ograničen na 3D modeliranje putem koda.
