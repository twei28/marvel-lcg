# Galactic Storm, lot GS-1 (héros BINARY) : questions pour l'utilisateur (20/10/2026)

Une question par point douteux, recommandation en premier, ce que chaque option change en jeu. Contexte :
`docs/packs/galactic-storm/BINARY-GABARITS.md` (gabarits par carte), `transcriptions/binary.md`, scans
`Hero Packs/Binary (Galactic Storm expansion content)/`.

## Décisions de l'utilisateur déjà appliquées (GS-0, 20/10/2026, relayées par le coordinateur)

Closes pour ce lot, rien à reposer :
- **Q1 (GS-0)** identifiants : `gs` + numéro imprimé sur 3 chiffres ; némésis en collision 237/239/240 : identifiant
  simple pour Binary (`gs237` Touched, `gs239` Goin' Rogue, `gs240` Energy Transfer), suffixe `q` pour Quasar.
- **Q2 (GS-0)** toutes les images portées, sans chercher 305 : les 24 images Binary + 23 reskins sont toutes traitées
  (une image par card_id ; les doublons d'exemplaires 2/15, 4/15... ne servent qu'à compter les exemplaires).
- **Q3 (GS-0)** un card_id par numéro imprimé, nombre d'exemplaires dans le paquet : `gs002`, `gs003`, `gs004`,
  `gs005`, `gs010` x2 dans `hero_deck`, `gs240` x2 dans `nemesis_set`.
- **Q4 (GS-0)** « Forces Response » = coquille de « Forced Response » : aucune carte Binary ne la porte.
- **Q5 (GS-0)** le nom imprimé fait foi (« 43 Going Rogue.png » imprime « Goin' Rogue » : c'est ce nom qui est porté).
- **Q6 (GS-0)** conventions : pastille orange à chiffre = PV (Rogue gs032 : PV 5 ; Hope Summers et Nick Fury reskins :
  3, identique aux officielles) ; étoile blanche sous THW/ATK d'un allié = dégâts consécutifs (Hope Summers et Nick
  Fury reskins : `2*`, identique aux officielles) ; « ★ » devant une capacité = renvoi au texte : aucune carte Binary.
- **Q7 (GS-0)** livret 1.2 partout : la FAQ 1.2 p.22 de Binary est appliquée (Cosmic Influx après Energy Conversion :
  aucun dégât ; deckbuilding : cartes de campagne non comptées).
- **Q10 (GS-0)** ne rien inventer où le livret est vide : rien de vide ne concerne Binary.

## Q1. Identifiant de « Forgotten Life » (imprime « 4 », comme Pursued by the Flame)

Décision demandée par la mission : « donnez-leur des identifiants distincts et documentez le choix ». Choix fait :
**`gs004` = Pursued by the Flame (x2, carte signature), `gs031` = Forgotten Life**. 31 est le rang de Forgotten Life
dans la liste imprimée du deck de départ (« Obligation Cards : 31 Forgotten Life »), liste dont les autres numéros
coïncident avec les pieds de carte de la némésis (32 Rogue) ; 31 est libre dans tout le coffret (trou relevé par
l'inventaire GS-0).
1. **(Recommandé) Garder `gs031`.** Change en jeu : rien (identifiant interne, lisible contre le livret de deck).
2. `gs004b` / `gs004o` (suffixe sur le numéro imprimé) : plus proche du pied de carte, mais un suffixe `b` se lit
   « face B » partout ailleurs dans le dépôt. Change en jeu : rien.
3. Autre (préciser).

## Q2. Avengers Mansion (reskin n° 28) : trait imprimé « AVENGERS. » au lieu de « AVENGER. »

Le scan de l'auteur porte « AVENGERS. LOCATION. » ; l'officielle 01091 « AVENGER. LOCATION. ». Tout le reste (coût 4,
[mental], Max 1 per player, texte) est identique. Règle d'acceptation d'un art (GUIDE §12 bis) : les traits imprimés
doivent être identiques. **Non branchée** en attendant (`01091_binary.jpg` non produite ; la carte est quand même
dans le deck de départ, avec son art officiel).
1. **(Recommandé) Coquille de l'auteur : brancher l'art alternatif `binary` de 01091.** Change en jeu : rien (la carte
   reste 01091, trait AVENGER) ; l'image montre « AVENGERS » au lieu de « AVENGER ».
2. Ne pas la brancher : Binary joue Avengers Mansion avec l'art officiel. Change en jeu : rien.
3. Carte exclusive distincte avec le trait AVENGERS : change en jeu les cartes qui lisent le trait AVENGER
   (Avengers Assemble!, Quincarrier) : déconseillé.
4. Autre (préciser).

## Q3. Une ressource [wild] en main compte-t-elle comme une ressource [energy] ?

Touche toutes les cartes qui comptent « the number of [energy] resources in your hand » : gs001a (ATQ X et Burnout),
gs002 Cosmic Influx (« non-[energy] resource drawn »), gs003, gs004, gs005, gs009, gs011, gs240. Dans le deck de
l'auteur, les seules cartes [wild] sont les quatre SPECIALIZATION de Specialized Training (mises de côté, jamais en
main) : la question ne se pose qu'avec un deck construit. **Lecture codée (une seule fonction,
`EnergieDeLaCarte`, `galactic_storm/binary/__init__.py`)** : non, le [wild] n'est pas [energy] tant qu'il reste en
main (il ne devient un type qu'à la dépense) ; c'est aussi ce que fait le filtre `has_printed_res` du moteur.
1. **(Recommandé) Non.** Change en jeu : un [wild] en main n'augmente ni l'ATQ X, ni la Riposte de Body in Flames, ni
   les paliers de Light, Radiation, Heat ; Burnout et Energy Transfer ne le défaussent pas ; Cosmic Influx compte un
   [wild] pioché comme « non-[energy] » (1 dégât).
2. Oui, un [wild] compte comme [energy] partout. Change en jeu : l'inverse de chaque point ci-dessus (Burnout défausse
   aussi les cartes [wild], Cosmic Influx ne blesse pas sur un [wild]).
3. Autre (préciser).

## Q4. Fuel the Fire (gs003) : le soin est-il plafonné par les dégâts réellement évités ?

« for each [energy] resource in your hand prevent 1 of that damage and heal 1 damage from Binary ». Lecture codée :
littérale, **N évités et N soignés** (N = [energy] en main), même si l'attaque fait moins de N dégâts. Exemple
mesuré : 2 [energy], attaque de 2, Binary à 3 dégâts → 0 subi, 2 soignés (reste 1).
1. **(Recommandé) Soin de N, non plafonné (lecture littérale de « for each ... and »).** Change en jeu : contre une
   petite attaque, Fuel the Fire soigne davantage.
2. Soin plafonné aux dégâts évités. Change en jeu : contre une attaque de 1 avec 4 [energy], 1 évité et 1 soigné
   (au lieu de 4 soignés).
3. Autre (préciser).

## Questions ouvertes par ce lot : rien d'autre

Points tranchés sans question (lecture unique, notés dans les gabarits) : on compte des ICÔNES d'énergie (Energy
Torrent YY vaut 2 ; la liste du deck de l'auteur et la FAQ p.22 l'impliquent) ; Energy Conversion garde le nombre
d'icônes et vaut aussi à la dépense (« treat ... as if they were ») ; Burnout sous Energy Conversion défausse toute
carte à ressource de la main ; Energy Conversion x2 dans le deck (la liste imprimée oublie « x2 », les deux scans
13/15 et 14/15 et le livret p.21 le donnent) ; Rogue et Touched désignés par nom ET type (un héros officiel Rogue et
son amélioration Touched 38002 existent) ; Rogue « When Defeated: Discard Touched » ne défausse que la Touched EN JEU.
