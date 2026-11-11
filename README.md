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
<summary>Klikni za prikaz</summary>
 
</details>



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
