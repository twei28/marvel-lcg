# Donatello (TMNT Heroes, Inkwire) : phase A (construction), 15/10/2026

**Statut : CONSTRUIT, NON VALIDE.** Aucun harnais lancé (test_capacites,
autoplay, verifier_tous_les_decks, substituer_pack) : rien n'a été joué.
Aucun `PROCESSUS-CARTE.md` n'est rempli : aucune carte n'est « terminée ».

Source : `TMNT Heroes-20261014T200300Z-1-001.zip` / `TMNT Heroes/Donatello v3/`
(24 PNG, lus un à un à l'outil Read). Branche : `worktree-agent-ae1da92d63a1aa083`.
Auteur dans `cards.json` (`custom`) : **Inkwire** (filigrane « TMNT Heroes By: Inkwire »).
Prefixe `td` (libre : vérifié dans cards.json, cards_custom.json et
`tools/prefixes_fanmade.json`, déclaré par `verifier_prefixes.py` : OK).
Set `164. Custom (Donatello)`, pack `donatello`.

## 1. card_id créés (18 card_id ; 24 scans = 18 cartes + 5 doublons de copie + l'insert de règles)

| card_id | nom | type | exemplaires | script |
|---|---|---|---|---|
| td001a | * Donatello | Hero | 1 | oui |
| td001b | * Donnie | AlterEgo | 1 | oui |
| td002 | * Metalhead | Ally | x1 | oui |
| td003 | Bō Tobu | Event | x2 (scans 2 et 3) | oui |
| td004 | Chūdan-Ura-Uke | Event | x2 (scans 4 et 5) | oui |
| td005 | Improvised Tactics | Event | x2 (scans 6 et 7) | oui |
| td006 | Singularity | Event | x1 | oui |
| td007 | Inspired Brilliance | Resource (RES `BG`) | x2 (scans 9 et 10) | aucun texte, aucun script |
| td008 | * Donnie's Lab | Support | x1 | oui |
| td009 | * Anti-Gravity Gauntlet | Upgrade | x1 | oui |
| td010 | * Truevision Goggles | Upgrade | x1 | oui |
| td011 | * Donatello's Bō | Upgrade (Restricted) | x1 | oui |
| td012 | * Donatello's Shell | Upgrade | x1 | oui |
| td013 | Broken Shell | Obligation (GiveTo « Donnie ») | x1 | oui (set Donatello) |
| td014 | Exterminate! | SideScheme némésis (1/5) | x1 | oui |
| td015 | * Baxter Stockman | Minion némésis (2/5) | x1 | oui |
| td016 | Plague of M.O.U.S.E.R.s | Minion némésis (3/5 et 4/5) | x2 | oui |
| td017 | Flight of Flyborgs | Minion némésis (5/5) | x1 | oui |

`hero_deck` = 15 cartes (x/15 imprimés : 1+2+2+2+1+2+1+1+1+1+1), `nemesis_set` =
`td014, td015, td016, td016, td017`, `obligations` = `td013`, `player_deck` VIDE
(aucune decklist d'aspect dans le zip, PROCESSUS-HEROS étape 3).

Lectures de scan à connaître (vérifiées, pas devinées) :
- **Ressources** (comparées par image à `01091` Avengers Mansion, RES=B) :
  icône « nœuds bleus » = mental (B), éclair jaune = énergie (Y), poing rouge =
  physique (R), étoile verte = wild (G). Inspired Brilliance = B + G.
- **Sbires** (comparés à `01167` Vulture) : le disque orange est les PV (Baxter 3,
  Metalhead 1, essaims « ★ »), les marques rouges du coin sont le BOOST (Baxter 2,
  Mousers 1, Flyborgs 3, obligation 2, manigance 2).
- **Acceleration** de td014 : icône comparée par image à `01109` Bomb Scare.
- Les étoiles creuses sous ATQ/CTR de Metalhead = dégâts consécutifs (`2*`).
- Menace de td014 : « 2 » + icône joueur = `2*` (par joueur).

## 2. Fichiers modifiés ou créés

Dans `Fusion/marvel-lcg-src/` (copie vivante) :
- `data/cards.json` (pack `donatello` en queue + checksum recalculé, algorithme
  calibré d'abord sur l'état d'origine : identique), `data/sets_info.json`
  (`164. Custom (Donatello)` + checksum).
- `deck/starter/donatello.json`, `data/nemesis/donatello_nemesis.json`.
- `src/cards/pack/donatello/{__init__.py, donatello/, donatello_nemesis/}` :
  helpers + `td001a, td001b, td002-td006, td008-td013` (dossier `donatello/`),
  `td014-td017` (dossier `donatello_nemesis/`).
- `src/game/card/face/card_face.py` : traits `NINJA, TURTLE, TEENAGER, BO, NYC,
  SEWERS, MOUSERS, FLYBORGS, SWARM` et compteur `swarm` (déclaratif).
- `tools/prefixes_fanmade.json` : préfixe `td`.
- `public/js/prepare/heros-info.js` : bio `td001a` (FR + EN, culture seulement).
Hors moteur :
- `ui-app/src/board/textes-fr-fanmade.ts` : `td001a`-`td017` (sauf `td007`, sans
  texte imprimé).
- `docs/reference/mots-cles/{cloak,swarm,tuck}.md` + index README.
- Images : 18 JPEG 615x882 (petit côté 615, q88, comme `outils/uniformiser-scans.py`)
  écrits dans `assets/pics/td*.jpg` (**gitignoré**) ET copiés dans
  `.planning/tmnt/pics-donatello/` (suivi, pour ne pas les perdre à la fusion) :
  **à recopier dans `Fusion/marvel-lcg-src/assets/pics/` de la copie principale.**
  `outils/uniformiser-scans.py` n'a pas été lancé (chemins `/mnt/c/...` en dur, absents
  ici) : même règle appliquée par un script jetable ; pas de sauvegarde des
  originaux 1500x2150, ils restent dans le zip.

Vérifications statiques faites (rien n'a monté de partie) : JSON valides,
checksums, `verifier_prefixes.py` OK, 18 modules compilent (ast), tout
attribut appelé existe dans `src/` (script jetable calibré par une erreur
volontaire `Faces.RemoveStatus`, vue et rejetée), légalité du deck (aucune
signature étrangère, tous les traits déclarés). `verifier_appels_modules.py` NON
lancé : il réécrit `launch.json`.

## 3. Points d'intégration avec les 3 autres héros (fusion des worktrees)

Fichiers partagés touchés par les quatre agents, donc conflits attendus à la
fusion (tous triviaux, ajouts en queue) : `data/cards.json`, `data/sets_info.json`,
`tools/prefixes_fanmade.json`, `card_face.py` (liste `TRAITS`, énum `COUNTER`),
`heros-info.js`, `textes-fr-fanmade.ts`, `docs/.../mots-cles/README.md`.
- **Checksums** : après fusion, relancer `recalculer_checksums.py` sur
  `cards.json` et `sets_info.json` (sinon rejet silencieux).
- **Numéro de set** : j'ai pris `164`, les trois autres ont pu prendre le même ;
  `verifier_prefixes.py` refuse les doublons : renuméroter (165, 166, 167).
- Traits `NINJA`, `TURTLE`, etc. : déclarés aussi par les autres : doublons sans
  effet (Literal de typage).

## 4. Questions en attente (6)

Format : carte, texte imprimé, options (effet en jeu), recommandée en premier.

### Q-TD-05 : td005 Improvised Tactics, « Cloak »
Texte : « Cloak two friendly characters. » Mot-clé maison **jamais défini** (ni
insert, ni règles officielles, ni moteur ; fiche `mots-cles/cloak.md`).
1. **(recommandée) Chercher d'abord la définition dans les packs Leonardo /
   Michelangelo / Raphael**, qui emploient probablement le même mot ; sinon
   demander à l'utilisateur. En attendant : option offerte mais INERTE (état
   actuel). Effet : « choose two » se joue à deux options réelles seulement
   (piocher + étourdir/désorienter).
2. Cloak = donner une carte d'état Tenace à chaque cible. Effet : la carte devient
   un bouclier collectif (2 personnages protégés), très fort.
3. Cloak = « ne peut pas être ciblé par les attaques ennemies jusqu'au début de
   votre prochain tour ». Effet : furtivité, ni dégâts ni état ; plus de code et
   de risques (ciblage).
4. Autre (précise).

### Q-TD-03 : td003 Bō Tobu, deux titres pour une même carte
Les deux exemplaires (scans 2 et 3) ont le texte, le coût et l'icône identiques,
mais « Bō Tobu » (macron, scan 2) et « Bo Tobu » (scan 3). Un seul card_id.
1. **(recommandée) Nom « Bō Tobu »** (macron, comme Chūdan-Ura-Uke et Donatello's
   Bō). Effet : cosmétique ; l'image utilisée est celle du scan 2.
2. Nom « Bo Tobu ». Effet : cosmétique ; l'image devient celle du scan 3.
3. Deux card_id distincts (td003/td003b). Effet : deux noms à l'écran, deux
   modules, un deck à 11+1 ids ; aucun effet de jeu.

### Q-TD-12 : td012 Donatello's Shell, « play, spend, or discard ... as if in your hand »
Le moteur rend « play » et « spend » (zone `is_like_in_hand`), pas « discard ».
1. **(recommandée) Accepter la limite** : une carte glissée se joue et se dépense,
   mais ne peut pas servir de coût « discard 1 card from your hand » (td001b,
   td009, cartes officielles). Effet : la Carapace est un peu moins souple que
   l'imprimé, sans aucun risque de crash.
2. Étendre à td001b et td009 seulement (coût de défausse sur main + carte
   glissée). Effet : fidèle sur les deux cartes du pack, rien sur les cartes
   officielles ; code de coût sur mesure.
3. Autre (précise).

### Q-TD-14 : td014 / td015, trait « MOUSER » vs « MOUSERS »
td014 : « a MOUSER or FLYBORG minion » (singulier) ; lignes de traits et td015 :
« MOUSERS », « FLYBORGS » (pluriel).
1. **(recommandée) Trait pluriel MOUSERS / FLYBORGS** (seul lisible sur les
   cartes). Effet : td014 et td015 se comprennent entre eux.
2. Ajouter aussi les traits singuliers MOUSER / FLYBORG aux sbires. Effet :
   aucun changement de jeu, deux traits par sbire.

### Q-TD-16 : td016 / td017, PV « ★ » des essaims
« Hit points are equal to the number of swarm counters. » ATQ et MNG suivent le
compteur ; les PV NE sont PAS suivis (`desc.HP = "1"`, mort donnée à la main au
dernier compteur ; les dégâts ne s'inscrivent jamais, ils retirent des compteurs).
1. **(recommandée) Garder ainsi.** Effet : règles identiques ; seul l'affichage
   du chiffre de PV diffère ; à tester : Déferlement / surplus de dégâts.
2. Suivre les PV dynamiquement (`ThisGainKeyword(health=...)`). Effet : affichage
   exact, mais risque de mort immédiate à l'entrée en jeu (base 0) et
   comportement non prouvé.

### Q-TD-02 : td002 Metalhead, interruption jouée depuis la main
« spend a [mental] resource → play Metalhead from your hand or Donatello's Shell
without paying his resource cost. » Écrit en capacité ordinaire à coût `B`
(`SetPlay()` imposerait le coût imprimé 2). Pas un doute de texte : un doute
d'ENGIN (une capacité hors `Play` sur une carte en main est-elle offerte ?).
1. **(recommandée) Garder le montage et le prouver en phase C** (cas : Metalhead en
   main puis sous la Carapace, Donatello se défend).
2. S'il n'est pas offert : passer par une capacité `Play` (`SetPlay`) + réduction
   de coût à 0 et coût `B` supplémentaire (`IgnoreThisCostIf`). Effet : même jeu,
   mais deux coûts à synchroniser.

## 5. Capacités à tester en phase C (par card_id)

Règle : un cas par capacité, jusqu'au bout, preuve par substitution
(`substituer_pack.py`), limites avec témoin d'épuisement, contre-cas dans
l'AUTRE forme pour tout bonus d'identité. Doivent passer aussi :
`verifier_tous_les_decks` (deck `donatello`, **injouable possible** : voir td012/td013),
`test_cards`, `audit_cartes`, 8 parties d'autoplay + témoin.

- **td001a** Kashikoi : coût `BB` payé, 2 cartes piochées, **limite une fois par
  round avec témoin d'épuisement** (second déclenchement refusé, chiffre =
  taille de main), injouable en alter ego.
- **td001b** : coût défausse 1 carte ; cherche td011 OU td012 dans deck ET
  défausse (chaque zone), UNE seule carte, **mise en jeu inclinée**, s'attache à
  l'identité, deck mélangé ; sans carte cible : rien ne plante.
- **td002** : Ténacité à l'entrée ; interruption proposée depuis la MAIN et
  depuis la CARAPACE quand Donatello (forme héros) se défend ; coût `B` payé ;
  carte jouée sans payer son coût 2 ; non proposée en alter ego ni si Metalhead
  est déjà en jeu ; dégâts consécutifs ATQ/CTR `2*`.
- **td003** : prévient exactement 3 dégâts d'une attaque (pas d'autres sources),
  retire 3 menaces d'UNE manigance ; avec 2 dégâts seulement.
- **td004** : prévient 3 ; inflige 3 à l'attaquant (vivant) ; attaquant mort entre
  temps.
- **td005** : coût = incliner une amélioration TECH ; « choose two » = deux options
  DIFFÉRENTES ; piocher 2 ; étourdir OU désorienter ; option Cloak = stub inerte
  (Q-TD-05) ; sans amélioration TECH la carte n'est pas jouable.
- **td006** : injouable sans Gauntlet en jeu (et jouable avec) ; 10 dégâts avec
  Déferlement + Perçant + À Distance (contre un sbire Tenace / avec Riposte) ;
  bonus +3 du Gauntlet appliqué (carte d'ATTACK).
- **td008** : n'agit qu'en alter ego ; incline ; ramène une carte ANDROID, ITEM ou
  TECH de la défausse (chaque trait) ; pas une autre.
- **td009** : +1 ATQ **en forme héros seulement** (contre-cas : alter ego) ;
  interruption sur un événement ATTACK : incline + défausse 1 carte -> +3 dégâts
  de CET événement seulement ; pas sur un événement non-ATTACK.
- **td010** : +1 CTR sur le contre de base seulement (pas ATQ/DEF) ; défausse
  facultative d'un statut d'ennemi (sonné / désorienté / tenace, choix) ; +1 CTR
  offert même sans ennemi à statut.
- **td011** : Restreint (limite de 2) ; redresse Donatello ; entre inclinée via
  td001b.
- **td012** : range UNE carte de la main (max 1 : seconde action refusée,
  **témoin d'épuisement**) ; la carte rangée est jouable ET dépensable comme en
  main ; « discard as if in hand » NON couvert (Q-TD-12) ; action héros seulement.
- **td013** : à la remise : bascule en alter ego puis -5 PV avec plancher à 1
  (cas PV 4, PV 11, déjà en alter ego) ; **ne peut pas repasser en forme héros**
  (et le jeu ne plante pas) ; retrait par `BB` OU par défausse de la Carapace EN
  JEU ; retirée de la partie (pas défaussée). Fait partie du deck de départ :
  `verifier_tous_les_decks`.
- **td014** : une fois déjouée, cherche un sbire MOUSERS ou FLYBORGS dans deck
  rencontre ET défausse, le met en jeu engagé avec le PREMIER joueur (2 joueurs) ;
  menace 2 par joueur ; icône d'accélération compte (+1 menace sur la manigance
  principale) ; sans sbire cible : rien ne plante.
- **td015** : ne peut pas subir de dégâts tant qu'un MOUSERS / FLYBORGS est en jeu,
  peut en subir sinon ; Coup Rapide ; quand il allait attaquer, il manigance à la
  place ; PV 3, MNG 2, ATQ 0.
- **td016 / td017** : entrent avec 2 / 4 compteurs `swarm` ; ATQ et MNG = compteurs ;
  dégâts remplacés par retrait de compteurs (3 dégâts sur 2 compteurs), mort au
  dernier compteur ; Déferlement / surplus (Q-TD-16) ; « after you defeat » après
  la mort donnée à la main.
- **Héros entier** : affichage du panneau de bio au survol dans le wizard
  (`td001a`), tooltips FR de chaque carte (déployer `ui-app/deployer.sh` : pas fait,
  consigne « ne rien déployer »), une partie complète jouée.
