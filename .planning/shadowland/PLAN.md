# Shadowland (MC65) : plan d'integration

Cadrage du 22/10/2026. Rien n'est ecrit dans `cards.json` ni dans le moteur.

## Decisions deja prises

- Pack scenario OFFICIEL FFG, sans heros, 3 scenarios : Shadows in the Night,
  Shadow Labyrinth, Heart of Shadow (+ sets Dark Protege, Ninja Swarm,
  Deadly Contraptions, Black Flower, Creeping Corruption).
- Prefixe **`sl`** (declare dans `tools/prefixes_fanmade.json`, verifie par
  `tools/verifier_prefixes.py`). Wave garde 65001-65019 : on ne le renumerote pas
  (decks et sauvegardes en ligne). Correspondance : 65NNN -> sl0NN, face
  conservee (65013B -> sl013b). Garder le numero officiel dans l'entree JSON.
- Scans : `.planning/shadowland/scans-marvelsimulator/` (93 webp, hors git),
  source play.marvelsimulator.com. A convertir en `assets/pics/sl0NN.jpg`
  (format 975 px comme les autres, a verifier) au moment de l'integration.
- On avance **scenario par scenario**, une carte a la fois
  (`docs/reference/PROCESSUS-CARTE.md`), questions une a une avec le scan.
  Premier scenario : Shadows in the Night.

## Ce que Shadows in the Night demande au moteur (lu sur les scans)

1. **Positions du vilain et du heros** (cartes 65003 et 65004, deux cartes
   recto-verso, mises en jeu ensemble a la mise en place) :
   - recto « The Streets Below », verso « Atop the Tenshu » ;
   - « Change the villain's position » = retourner la carte 65003 ;
   - carte 65004 : action du premier joueur, resoudre un effet puis la
     retourner ;
   - effets continus selon que les deux positions sont identiques ou non
     (+1 ATK a tous les personnages / -1 aux degats subis par attaque et menace
     non retirable du complot principal).
   Aucun equivalent dans le moteur : mecanique nouvelle (fiche `mots-cles/`
   « position » a creer avant tout code).
2. **Vilain tire au hasard** parmi 6 Dark Proteges (cartes 65012 a 65016 +
   Daredevil/White Tiger, recto A / verso B), ses 5 cartes liees melangees dans
   le deck de rencontre, les autres mises de cote.
3. **Complot principal en 2 etapes**, vilain qui se retourne : quand il serait
   vaincu face A, il passe face B, PV remis, position changee, chaque joueur
   recoit 1 carte rencontre face cachee ; vaincu face B = victoire ; etape
   terminee = defaite. Mode expert : +1 SCH, +3 PV par joueur.
4. Cartes a effets de recherche (« each player searches the encounter deck and
   discard pile for a minion and reveals it »).

Textes des cartes du pack, a relire une a une au moment de les traiter
(les noms ci-dessous viennent de la planche-contact, pas d'une lecture fine) :
65001 A Barricade of Blades, 65002 Fortress Lockdown, 65003/65004 positions,
65005 Black Tarantula, 65006 Ghost Maker, 65007 Sealed Entrances,
65008 Strategic Positioning, 65009 Surround the Fortress, 65010 Chaos in Hell's
Kitchen, 65011 Moonlit Silhouette, 65012-65016 Dark Proteges, 65017-65031 a
identifier (Ninja Swarm, a verifier a l'image).

## Ordre propose

1. Inventaire fin : lire les 93 images, fixer pour chaque numero le set, le type,
   le texte, les valeurs (fichier `docs/packs/shadowland/cartes.md`).
2. Questions de cadrage a l'utilisateur, une par une, avec scan.
3. Fiche mot-cle « position » et recette moteur (positions + vilain
   recto-verso).
4. Entrees `cards.json` / `sets_info.json` (set 209), images `sl0NN`.
5. Scripts et cas `tools/test_capacites.py`, preuve par substitution, autoplay.
6. Scenario `shadows_in_the_night` + `data/encounter_sets/`.
7. Puis Shadow Labyrinth, puis Heart of Shadow (corruption, Krahllak).

## Points ouverts

- Mode campagne : le pack se joue seul OU en mini-campagne de 3 scenarios
  (livret a lire : le PDF officiel n'est pas encore dans le depot).
- Textes francais : pas de source VF pour l'instant.
- Qualite des scans de Marvel Simulator (715 x 1028) a comparer a nos 975 px.
