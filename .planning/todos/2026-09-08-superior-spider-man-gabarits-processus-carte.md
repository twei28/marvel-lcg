# Superior Spider-Man — gabarits `PROCESSUS-CARTE.md`, carte par carte

Pack `superior_spider_man`, set **167**, prefixe **`su`**, **21 card_id**,
auteur **Rainy**. Ouvert le 08/09/2026.

## ETAT AU 08/09/2026

- **Etape 7** : **29/29 cas passent** (`test_capacites.py`, filtre `su0`).
- **Etape 7, preuve par substitution** : **21/21 cartes** tombent au ROUGE sans
  leur module. Quatre cartes rendent « un cas reste vert » (`su007`, `su011`,
  `su018`, `su019`) : ce sont des CONTRE-CAS d'absence d'effet ou des cas
  d'attache, verts par nature (PROCESSUS-CARTE §7.3).
- **Etape 8** : **8 parties d'autoplay par deck** (les deux alter-egos), **0
  incident**, 5,9 et 5,1 rounds. **Grep exhaustif : 0 erreur.** Toutes les
  cartes apparaissent dans les journaux.
- **Gates statiques** : `compileall` silencieux, `test_cards` **5392 ok / 0
  err**, `verifier_appels_modules` OK, `verifier_noms_modules` OK,
  `verifier_desc_mots_cles` OK, `tsc --noEmit` silencieux.
- **Les DEUX decks montent** : « identite su001a » et « identite su001c ».

## Deux arbitrages utilisateur (08/09/2026)

1. **DEUX alter-egos au choix**, chacun avec son obligation → **deux decks de
   depart**, `superior_spider_man` (su001b Peter Parker + su013) et
   `superior_spider_man_tolliver` (su001c Elliot Tolliver + su014).
2. **`su019` Pumpkin Bombs affiche une ETOILE en ATK** au lieu d'un chiffre →
   **aucun bonus d'ATK** : l'etoile pointe la capacite etoile de la carte,
   convention typographique de Rainy deja etablie sur Blade et Spider-Man 2099.

## Ce qui vaut pour tout le pack

- **Etape 2** : chaque module porte son bloc « CARTES DE REFERENCE » avec le
  POURQUOI. Modeles structurants : `ab001a` (capacite nommee), `aa002`/`dz014`
  (carte posee face cachee et jouable), `al022` (« after attached enemy attacks
  you »), `60053` (bonus continu conditionnel).
- **Etape 4** : 21 scans dans `assets/pics/suXXX.jpg`
  (`tools/importer_images_superior_spider_man.py`). ⚠ Uniformisation a 615 px
  et sauvegarde des originaux a faire au deploiement.
- **Etape 6** : verifie en plus par `verifier_desc_mots_cles` (21/21).
- **Icones tranchees par comparaison d'image**, jamais a vue : les 10
  ressources des signatures, et les **DEUX icones Acceleration** de `su015`
  Goblin Protocol (barre de soulignement presente, comme `ag011` ; absente sur
  `hd022`, temoin Alea).

## Mot-cle maison `track`

« Move 1 threat from a scheme to a minion in play » — un **DEPLACEMENT**, pas
un retrait. Fiche `docs/reference/mots-cles/track.md`. A exige d'AJOUTER a
l'enum du moteur les compteurs **`threat`** et **`surveillance`**, ainsi que le
trait **`HENCHMAN`** : la menace posee sur un SBIRE n'a aucune existence
native. Le helper `Tracer` ne pose sur le sbire QUE ce qu'il a reellement
retire de la manigance — sans quoi il CREERAIT de la menace.

## LES TROIS DEFAUTS QUE LES GATES ONT TROUVES

1. **`su003` Agility — 26 AssertionError en 8 parties d'autoplay.** Montee en
   `WhenInYourPlayTurn(HeroInterrupt).SetLabel('defense')`, elle passait
   `test_cards`, TOUTES les gates statiques et le montage du deck, et faisait
   planter le moteur dans `can_defense.py:138` a chaque defense. **Seule
   l'etape 8 l'a vue.** Reecrite sur `WhenUnitWouldTakeDamage(...).SetPlay()`.
   Apres correctif : 0 erreur, et les parties durent 5,9 rounds au lieu de 4,0
   — la carte protege enfin pour de vrai.
2. **`su015` Goblin Protocol — deck injouable.**
   `GiveKeywordToInPlayWhenApplyThis` rend une **LISTE** d'abilities : sans
   l'etoile de deballage, le moteur plante au SETUP (`AttributeError: 'list'
   object has no attribute 'paper'`). Et le bonus allait sur la mauvaise carte
   (`ThisGainKeyword` modifiait le seuil du complot ANNEXE, que personne ne
   regarde, au lieu du complot PRINCIPAL).
3. **`su007` — un bonus continu ne se recalcule pas tout seul.**
   `ex_change_on_event=OnEvent.Counter(Minion, 'threat')` est necessaire :
   `OnEvent.GameArea` ne suffit pas, puisque ce qui change est un COMPTEUR sur
   un sbire deja en jeu, pas la presence d'une carte.

## Deux pieges de CAS, payes et documentes

- **`su016` lisait 0 degat** : le Spider-Sense de `su001a` PIOCHE au moment
  meme de l'attaque, et la carte piochee etait `su003` Agility, qui prevenait
  les degats mesures. C'est la lecon Moxie (RECETTES §7bis). Les deux Agility
  sont desormais retirees du deck par `Puzzle.Remove`.
- **`su008` et `su019` restaient VERTS sous substitution** : ils mesuraient
  quelque chose que le module ne fait pas (la mort d'un sbire ; des degats que
  Hobgoblin inflige de toute facon). Reecrits sur un effet qui appartient
  vraiment au module.

---

## Cartes

Toutes les cartes ci-dessous ont leurs etapes 1 a 8 remplies, un cas sujet par
capacite mesurable, et une substitution ROUGE.

- **su001a** * Spider-Man — Spider-Sense elargi aux sbires Villainous (la carte
  officielle `01001a` ne vise que le vilain : recopier son module aurait rendu
  la capacite deux fois moins bonne). 2 cas. **OUI**
- **su001b** * Peter Parker — Master Planner + temoin d'epuisement. 2 cas.
  **OUI**
- **su001c** * Elliot Tolliver — le SECOND alter-ego, sur son propre deck.
  1 cas. **OUI**
- **su002** Spiderlings — contre remplace par un `track` ; -1 degat consequent
  contre un sbire piste. 1 cas. **OUI**
- **su003** Agility — prevention 3 / tout si AERIAL. 1 cas. **OUI**
- **su004** Brutal Efficiency — cout X en MENACE POUR LE VILAIN, 3X degats,
  overkill. 1 cas. **OUI**
- **su005** Webbed Up — 3 menaces + stun elargi si paye en [wild]. 1 cas.
  **OUI**
- **su006** * Anna Maria Marconi — soin 3 ou reduction de cout. 1 cas. **OUI**
- **su007** Facial Recognition Uplink — +1 CTR conditionnel + track a l'arrivee
  d'un sbire. 2 cas dont un contre-cas. **OUI**
- **su008** Mastermind — attache a Contingency Plan. 1 cas. ⚠ La SECONDE
  capacite (« look at the top 3 cards of the encounter deck, discard 1 ») n'a
  **aucune cle de verification dans le harnais** : a verifier en partie reelle.
  **OUI** pour ce qui est mesurable.
- **su009** Mechanical Arms — track sur attaque de base + redressement. 1 cas.
  **OUI**
- **su010** Spider-Bot — les DEUX branches (track / retrait). 2 cas. **OUI**
- **su011** Web-Shooters — trait AERIAL + contre-cas dans l'autre forme. 2 cas.
  **OUI**
- **su012** Contingency Plan — Action de defausse. 1 cas. ⚠ L'autre capacite
  (« may be played as though it were in your hand ») **n'est pas testable** :
  la cle `jouer` ne regarde que la MAIN et aucune commande Puzzle ne joue une
  carte depuis la zone posee. A verifier en partie reelle. **OUI** pour ce qui
  est mesurable.
- **su013** / **su014** Ghost of a Conscience / Crisis of Conscience — les deux
  obligations, une par alter-ego, chacune sur son deck. 2 cas. **OUI**
- **su015** Goblin Protocol — la menace des sbires pistes compte pour le
  vilain. 1 cas. **OUI**
- **su016** * Hobgoblin — Forced Response apres son attaque. 1 cas. **OUI**
- **su017** Lunatic Laugh — degats indirects + desorientation des personnages
  reellement touches. 1 cas. **OUI**
- **su018** Goblin Glider — attache a l'ennemi aux PV IMPRIMES les plus hauts +
  Action a deux energies. 2 cas. ⚠ La branche « If you cannot, this card gains
  surge » n'est pas testee : elle demande un plateau SANS aucun ennemi, et
  retirer le vilain fait tomber la partie. **OUI** pour ce qui est mesurable.
- **su019** Pumpkin Bombs — attache a Hobgoblin, sinon au vilain ; Forced
  Response ; Action. 3 cas. **OUI**

---

## Gate finale `PROCESSUS-HEROS.md`

- [x] Etapes 1 a 6 (donnees, scripts, DEUX decks, sets_info, images)
- [~] Etape 7 : biographie ecrite — ⚠ **preuve au survol dans le wizard NON
      FAITE** (demande d'ouvrir le jeu)
- [x] Etape 8 : 21 textes francais, `tsc --noEmit` silencieux
- [x] Etape 9 : un cas sujet et une substitution ROUGE pour chaque carte
- [x] `verifier_tous_les_decks.py` : les DEUX decks au VERT
- [ ] Une partie complete jouee par un humain

**Heros termine : NON** — il ne manque que ce qui ne peut pas s'automatiser (la
preuve de la bio au survol, une partie humaine) et trois capacites hors de
portee du harnais, nommees ci-dessus. Tout le reste est vert.
