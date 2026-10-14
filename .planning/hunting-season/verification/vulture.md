# Vérification groupe « vulture » (hs080 à hs103, hs151 à hs156)

31 fiches (hs083a et hs083b comptées à part). Bilan : 21 CONFORME, 10 ÉCART, 0 DOUTE de verdict (deux icônes douteuses signalées en note).

Conventions lues sur les scans : les icônes rouges en bas de carte sont des icônes de boost. Une icône en Y = 1 point de boost, une étoile rouge = icône ★ sans valeur (le [star] Boost du texte). Donc Y seul = Boost 1, étoile + Y = Boost 1, étoile seule = Boost 0, Y Y = Boost 2. Collection : « Vulture (n/24) » pour hs080 à hs103, « Red Vulture (n/6) » pour hs151 à hs156. Toutes les cartes sont recto simple sauf hs083 (1A/1B).

## Récapitulatif

| card_id | verdict | résumé |
|---|---|---|
| hs080 | CONFORME | Vulture I, HP 13 par joueur, SCH 2, ATK 2, traits et texte identiques |
| hs081 | CONFORME | Vulture II, HP 16 par joueur, SCH 2, ATK 2★ (le ★ d'ATK n'est pas dans desc), texte identique |
| hs082 | CONFORME | Vulture III, HP 19 par joueur, SCH 3, ATK 2★ (idem), texte identique |
| hs083a | CONFORME | Aerial Mayhem 1A, texte Contents et Setup identiques (note : le scan écrit « Wing Suits » en deux mots) |
| hs083b | CONFORME | 1B, menace cible 11 par joueur, départ 3 par joueur, escalade +1 par joueur, texte identique |
| hs084 | CONFORME | S.H.I.E.L.D. Wingsuits, Hero Action identique |
| hs085 | CONFORME | Armadillo HP 7, SCH 1, ATK 3★, boost ★ + Y (=1), texte identique |
| hs086 | CONFORME | White Rabbit HP 4, SCH 1, ATK 1★, boost ★ seule (=0), texte identique |
| hs087 | ÉCART | Gibbon : le JSON ajoute « of » absent du scan (cosmétique) |
| hs088 | ÉCART | Wing Harness : « two card » sur le scan, « two cards » dans le JSON (cosmétique) |
| hs089 | CONFORME | Metal Talons, boost Y Y (=2), ATK ★ non repris dans desc, texte identique |
| hs090 | ÉCART | Titre du scan « Projectil Feathers », JSON « Projectile Feathers » |
| hs091 | ÉCART | Idem hs090 (copie 12/24) |
| hs092 | ÉCART | Forcefully Elevated : aucune icône de boost sur le scan, JSON Boost 1 |
| hs093 | ÉCART | Idem hs092 |
| hs094 | CONFORME | Aerial Kidnapping, menace 3, boost 1, Surge, texte identique |
| hs095 | CONFORME | Idem hs094 (copie 16/24) |
| hs096 | CONFORME | A Feast for Vultures, menace 3, Hazard 1, boost Y Y Y (=3), texte identique |
| hs097 | CONFORME | Knocked Out of the Sky, Surge, boost 1, texte identique |
| hs098 | CONFORME | Idem hs097 |
| hs099 | CONFORME | Idem hs097 |
| hs100 | CONFORME | Sweeping Swoop, boost ★ + Y (=1), texte identique |
| hs101 | CONFORME | Idem hs100 |
| hs102 | ÉCART | Ravenous Onslaught : virgule du scan « this card, gains surge » absente du JSON (cosmétique) |
| hs103 | ÉCART | Idem hs102 |
| hs151 | CONFORME | Vulture (James Natale) HP 4, SCH 1, ATK 1★, boost Y Y Y (=3), Quickstrike, Villainous, texte identique |
| hs152 | CONFORME | The Red Vulture, menace 3 par joueur, Hazard 1, boost 3, texte identique |
| hs153 | CONFORME | Acid Expulsion, boost ★ + Y (=1), texte identique |
| hs154 | CONFORME | Idem hs153 |
| hs155 | ÉCART | Voracious Ambush : boost Y Y (=2) sur le scan, JSON Boost 1 ; structure des phrases différente |
| hs156 | ÉCART | Idem hs155 |

## Détail des ÉCART

### hs087 Gibbon
- Scan : « Forced Interrupt: When Gibbon would take any amount damage, prevent 1 of that damage. »
- JSON : « ... would take any amount **of** damage, prevent 1 of that damage. »
- Différence : le JSON corrige une coquille du scan (« of » manquant). Tout le reste est conforme (HP 4, SCH 1, ATK 2, coût 4, Guard, boost Y Y).
- Effet sur le jeu : aucun.

### hs088 Wing Harness
- Scan : « Hero Action: Exhaust your hero and discard two card from your hand → discard Wing Harness. ... »
- JSON : « discard two **cards** from your hand ».
- Différence : coquille du scan corrigée. Le scan montre aussi une icône ATK ★ (sans chiffre) et +1 SCH ; le JSON ne garde que SCH+ 1 (l'ATK ★ renvoie au +1 ATK du Forced Interrupt).
- Effet : aucun sur le texte. À vérifier seulement que le script applique bien +1 ATK.

### hs090 et hs091 Projectile Feathers
- Scan : titre « Projectil Feathers » (coquille de l'auteur), mais le corps de texte dit « Projectile Feathers ».
- JSON : name « Projectile Feathers ».
- Effet : aucun si le nom corrigé est voulu ; le JSON est cohérent avec le corps de texte. Texte et boost (Y = 1) conformes.
- Icône douteuse : « Spend ⚡⚡ resources », deux éclairs noirs ; le JSON dit [energy][energy]. La forme éclair est cohérente avec énergie mais je ne l'affirme pas.

### hs092 et hs093 Forcefully Elevated
- Scan : aucune icône de boost visible en bas (bandeau « VULTURE (13/24) » ou « (14/24) » vide à droite). Texte conforme.
- JSON : desc.Boost = "1".
- Différence : le JSON invente un boost 1 absent du scan.
- Effet : quand la carte est piochée comme boost, le JSON donnerait +1 ; le scan donnerait 0. Une Obligation n'a normalement pas de boost imprimé mais ici la décision revient à l'auteur du scan : le scan fait foi, donc Boost 0.
- Icône douteuse : « spend a [physical] resource » ; sur le scan une icône noire en forme de poing. Plausible pour physique, non certain.

### hs102 et hs103 Ravenous Onslaught
- Scan (Hero) : « If you have less than half of your maximum hit points remaining this card, gains surge. »
- JSON : « ... remaining this card gains surge. »
- Différence : virgule mal placée sur le scan, sans conséquence. Boost Y (=1) conforme.
- Effet : aucun.

### hs155 et hs156 Voracious Ambush
- Scan : « When Revealed (Hero): Vulture (James Natale) attacks your hero. If Vulture (James Natale) did not attack you this way, discard the top 6 cards of the encounter deck. If Vulture (James Natale) is in the encounter discard pile, put him into play engaged with you. » Icônes de boost : Y Y.
- JSON : « ... If Vulture (James Natale) did not attack you this way, discard the top 6 cards of the encounter deck **and if** Vulture (James Natale) is in the encounter discard pile, put him into play engaged with you. » ; Boost "1".
- Différences : (1) Boost 2 sur le scan, 1 dans le JSON. (2) Le scan a deux phrases indépendantes, le JSON fait de la mise en jeu une sous-condition de « did not attack you ».
- Effet : (1) un boost de moins que prévu. (2) Cas pratique identique car si Vulture a attaqué, il est déjà en jeu et pas dans la défausse ; différence seulement si l'on code la condition de façon stricte.

## Notes transversales
- Noms avec ✦ (Vulture, Armadillo, White Rabbit, Gibbon, Vulture (James Natale)) : le JSON les marque « * ». Conforme.
- hs083a, scan : « S.H.I.E.L.D. Wing Suits » (deux mots) dans le Setup, alors que la carte hs084 s'appelle « S.H.I.E.L.D. Wingsuits ». Le JSON reproduit fidèlement les deux. Si la recherche se fait par nom, elle échouera : à décider côté moteur.
- Les ATK ★ de hs081, hs082, hs085, hs086, hs151 (et de hs088, hs089 en pièce jointe) ne sont pas représentés dans desc.ATK ; le ★ n'a pas de valeur propre, le texte [star] le porte.
