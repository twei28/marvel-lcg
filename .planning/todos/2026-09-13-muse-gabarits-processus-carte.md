# Muse (Rainy, set 174) — gabarits PROCESSUS-CARTE, 6 cartes

**Livré le 13/09/2026.** Préfixe `mu`. **SET MODULAIRE**, pas un héros : celui qu'on
ajoute à n'importe quel scénario, comme `necroverse` ou `intergalactic_hazards`. Sept
exemplaires pour six cartes distinctes (Obsession en double). Relevé image par image et
arbitrages dans `2026-09-13-muse-releve-des-cartes.md`.

## L'arbitrage qui tient tout le set

**Quatre cartes sur six** parlent d'« une carte avec l'image de votre identité dessus ».
Le moteur ne sait rien de ce que montre une illustration. Trois questions ont été posées
à l'utilisateur, une par carte concernée, avant la première ligne de code :

| Question | Décision |
|---|---|
| Que vaut « l'image de votre identité » ? | Les **cartes signature** (`card_class="IdentitySpecific"`), le vocabulaire de l'auteur lui-même sur `mu005` |
| `mu001` : qui encaisse « chaque personnage dont l'image était sur cette carte » ? | Le **héros dont c'est le deck**, quoi que montre la carte |
| `mu002` : que vaut « une image de cet ennemi » ? | Une carte rencontre **du même set** que l'ennemi |

Les lectures écartées sont écrites dans le relevé, avec ce qu'elles changeaient en jeu.

## Deux ajouts moteur, minimes

- Le compteur **`graffiti`** dans `CardFace.COUNTER` : sans lui, `IsCounter` refuse le
  nom et `mu004` tombe dès la création de la partie (leçon déjà payée par `ih004`).
- Le trait **`ARTIST`** dans `CardFace.TRAITS`, seul du catalogue.

## Un ajout d'outil, qui manquait vraiment

**`tools/autoplay.py --modulaires muse`**. Un set modulaire n'appartient à aucun
scénario : il n'existait **aucune façon de le faire jouer par le pilote**, et un pack
comme celui-ci ne pouvait être éprouvé que carte par carte au harnais des capacités,
jamais dans une vraie partie où ses cartes se croisent. L'option ajoute les sets nommés
au champ `encounter_sets` de la campagne montée, celui que le moteur lit déjà pour le
set « expert ».

## Ce qui a été mesuré

| Gate | Résultat |
|---|---|
| `tools/verifier_prefixes.py` | OK, `mu` réservé, 6 cartes |
| `tools/verifier_noms_modules.py .game-src muse` | OK |
| `tools/verifier_appels_modules.py .game-src <port> muse` | OK |
| `tools/verifier_desc_mots_cles.py muse` | OK, 6/6 |
| `tools/verifier_coherence_cartes.py` | textes fr 6/6, images 6/6, cas cités 100 % |
| `tools/test_cards.py` | 5571 cartes construites, **0 erreur** |
| `tools/test_capacites.py` filtre `mu00` | **12/12** |
| `tools/substituer_pack.py mu00` | **6/6** cartes avec au moins un cas rouge sans module |
| `autoplay --modulaires muse`, 4 parties | **0 traceback**, les 6 cartes vues dans chaque journal |
| `autoplay` témoin sans le set, 4 parties | 0 traceback |
| `ui-app` : `npx tsc --noEmit` | vert |

**Cas verts sans module, assumés** : un par carte, ce sont les CONTRE-CAS d'absence
d'effet (`mu001` sans carte signature, `mu002` avec une carte d'un autre set, `mu003`
avec une carte Basic, `mu006` avec une main sans signature). Ils prouvent que le filtre
filtre ; sans le module il n'y a rien non plus, c'est attendu.

## Quatre pièges payés en chemin

1. **`Surge` s'écrit dans `desc`, pas dans le script.** `ThisCardGainSurge` dans le
   corps de la capacité l'aurait donné une SECONDE fois et la traîtrise aurait révélé
   deux cartes. Attrapé par `verifier_coherence_cartes.py`, qui a signalé « Surge
   imprimé, clé desc absente ».
2. **« Give IT to them » n'est pas `GiveFacedownBoostCards`.** Cette primitive PIOCHE de
   nouvelles cartes ; `mu002` doit donner **la carte qu'on vient de défausser**, d'où
   `CanBoost.GiveBoostCard(face, effect)`. Se tromper aurait défaussé une carte ET
   pioché une seconde.
3. **Les événements signature de Spider-Man sont tous des interruptions**, injouables en
   action — et Backflip aurait en plus PRÉVENU l'attaque de Muse, rendant deux cas verts
   pour la mauvaise raison. Les cas jouent Aunt May et Spider-Tracer.
4. **Black Cat est déjà dans le deck de départ de Spider-Man** : `dans_deck_joueur`
   trouvait l'autre exemplaire et `mu005` restait vert sans son module. Le deck est vidé
   d'abord, et `taille_deck_joueur: 1` ne laisse aucun doute.

## Ce que les gates ne peuvent pas voir

- **Aucune partie jouée à la main dans le navigateur.** Le set est éprouvé carte par
  carte et joué quatre fois par le pilote, mais « est-ce que Muse est agréable à
  affronter » reste ouvert. Il n'y a pas d'outil pour cela.
- **Le set n'est pas proposé par le lanceur.** `sets_info.json` le déclare, mais rien
  n'a été vérifié côté wizard : à regarder au premier essai.
- **Les deux interruptions forcées sur le même déclencheur** (`mu003` et `mu004`) se
  cumulent quand les deux sont en jeu : la carte signature réveille Muse ET pose
  1 menace. Rien ne l'interdit, et l'autoplay l'a fait, mais aucun cas ne le mesure.

## Gabarits, une carte par section

### mu001 : Art Imitates Death
- [x] Étape 2 : `27086` Mysterio (`Players.ForEachPlayer` + `DiscardDeckTopCards`), `as025` Underworld Impact (compter puis frapper).
- [x] Étape 5 : `EACH player` → tous ; `top 3` → trois, le moteur remélange seul ; dégâts NON indirects, la carte ne le dit pas ; pas de « When Defeated ». Résultat : conforme.
- [x] Étape 6 : 3 cartes, 1 dégât chacune, 2[per_hero] menaces de départ, 2 icônes de boost. Résultat : conforme.
- [x] Étape 7 : nominal (3 signatures → 3 dégâts) + contre-cas (3 cartes Basic → 0). Rouge sans module sur le nominal. Résultat : 1/2.
- [x] Étape 7 bis : pas de limite imprimée. NON.
- [x] Étape 8 bis : NON (dégâts, déjà couverts).
Carte terminée : OUI.

### mu002 : Supply Run
- [x] Étape 2 : `15025` Luminous (lire le dessus du deck rencontre à une activation), `CanBoost.GiveBoostCard` (can_boost.py:34), `04078` Absorbing Man pour la fenêtre.
- [x] Étape 5 : `a UNIQUE enemy` → `is_unique`, pas un sbire ordinaire ; `WHEN ... activates` → INTERRUPTION, la carte de boost arrive à temps pour cette activation ; `give it TO THEM` → à l'ennemi qui s'active ; la carte est défaussée DANS TOUS LES CAS. Résultat : conforme.
- [x] Étape 6 : 1 carte, 3[per_hero] menaces, 2 icônes. Résultat : conforme (Rhino frappe à 2+1=3 avec Stampede offerte).
- [x] Étape 7 : nominal (carte du set Rhino) + contre-cas (carte du set Klaw). Rouge sans module. Résultat : 1/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, une carte CHANGE DE ZONE (défausse → pile de boost). Mesuré par les dégâts de l'activation, la seule lecture que le harnais offre.
Carte terminée : OUI.

### mu003 : * Muse
- [x] Étape 2 : `01102` Sandman (`Toughness` dans `desc`, base automatique), `11051` Ancient Grudge (`DoActivate`), `WhenPlayerPlayCard` (play.py:260).
- [x] Étape 5 : `A PLAYER` et non « vous » → en multijoueur Muse se réveille sur la carte de n'importe qui et frappe CE joueur-là, pas celui avec qui il est engagé ; `Forced INTERRUPT` → avant que la carte se résolve ; AUCUNE limite imprimée, deux signatures dans le tour font deux activations ; `ELITE` compte, il est dans `traits`. Résultat : conforme.
- [x] Étape 6 : 8 PV, CTR 2, ATQ 2, 3 icônes, Ténacité. Résultat : conforme.
- [x] Étape 7 : nominal (carte signature → 2 dégâts) + contre-cas (carte Basic → 0). Rouge sans module. Résultat : 1/2.
- [x] Étape 7 bis : NON, et c'est voulu — l'absence de limite est ce qui rend le sbire punitif.
- [x] Étape 8 bis : NON (la carte d'état Coriace vient de `desc`, chemin générique).
Carte terminée : OUI.

### mu004 : Graffitied Streets
- [x] Étape 2 : `ih004` Asteroid Belt et `27174a` Public Outcry (environnement à compteurs `Uses`), `mu003` pour la même fenêtre.
- [x] Étape 5 : « When YOU play » ici contre « when A PLAYER plays » sur `mu003` — les deux n'ont PAS la même portée et c'est imprimé ainsi ; `equal to that character's THW` → le CTR du personnage incliné ; `Exhaust a character you control` est le COÛT ; `Limit once per round PER PLAYER` et surtout pas `LimitOncePerRound` ; `Action` nue, jouable aussi en alter-ego. Résultat : conforme.
- [x] Étape 6 : 3[per_hero] compteurs, 1 menace, 1 icône. Résultat : conforme (Spider-Man a 1 de CTR, un seul compteur part, 2 restent).
- [x] Étape 7 : la menace posée, et l'Action qui retire le CTR. Les DEUX rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : OUI, limite imprimée « once per round per player ». ⚠ NON COUVERTE, et c'est écrit ici plutôt que passé sous silence : le harnais ne monte qu'un seul joueur, il ne peut donc pas montrer qu'un SECOND joueur garde son usage. Un témoin à un seul joueur prouverait la limite « once per round » et rien de la mention « per player ».
- [x] Étape 8 bis : OUI, compteurs sur une carte en jeu. Mesuré par `compteurs`.
Carte terminée : OUI, la limite par joueur exceptée.

### mu005 : Grim Inspiration
- [x] Étape 2 : `vv001b` Viv Vision (choisir dans SA défausse puis `MoveAllToDeck(..., "Top", ...)`), `27086` pour `ForEachPlayer`, `02007` pour les cartes de boost.
- [x] Étape 5 : `Surge` → BASE AUTOMATIQUE dans `desc`, aucun script ; `EACH player CHOOSES` → chacun pour soi ; un joueur sans carte signature ne fait rien, la carte ne dit pas « si vous ne pouvez pas » ; `Muse AND the villain` → les deux, et le vilain reçoit la sienne même si Muse est absent. Résultat : conforme.
- [x] Étape 6 : 1 carte remontée, 1 carte de boost chacun, 1 icône. Résultat : conforme.
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, une carte passe de la défausse au deck. Mesuré par `dans_deck_joueur` + `taille_deck_joueur`.
Carte terminée : OUI.

### mu006 : Obsession *(deux exemplaires)*
- [x] Étape 2 : `11051` Ancient Grudge, MOT POUR MOT la même structure ; `sm016` Power Surge pour le boost étoile variable.
- [x] Étape 5 : l'ordre imprimé est trompeur, on cherche et on pose Muse AVANT de l'activer ; `find Muse` sans dire où → deck rencontre ET défausse, il peut donc revenir après avoir été vaincu ; `engaged with you` → `PutIntoPlay(joueur, effect)` ; boost ÉTOILE, aucune valeur `Boost` dans `desc` ; X peut valoir ZÉRO. ⚠ « YOUR hand » sur une capacité Boost = LE JOUEUR QUI DÉFEND, le moteur le dit lui-même (sender_card.py:688). Résultat : conforme.
- [x] Étape 6 : +1 icône par carte signature en main. Résultat : conforme (2 en main → Rhino frappe à 4 ; 0 en main → 2).
- [x] Étape 7 : Muse trouvé et posé puis il frappe ; le boost à 2 signatures ; le contre-cas à 0. Résultat : 2/3.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, un sbire ENTRE EN JEU. Mesuré par `en_jeu`.
Carte terminée : OUI.
