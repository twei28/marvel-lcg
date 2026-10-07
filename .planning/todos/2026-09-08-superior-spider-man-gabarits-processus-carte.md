# Superior Spider-Man — gabarits `PROCESSUS-CARTE.md`, carte par carte

> **Mise à jour du 07/10/2026 (audit du backlog)** : Même cas que Spider-Man 2099 : cartes faites (21/21 substitutions rouges). Reste : preuve visuelle de la biographie au survol. Partie humaine hors backlog.

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
- **su008** Mastermind — attache a Contingency Plan + fouille du deck
  rencontre. **2 cas, 2/2 rouges sous substitution (09/09/2026)**.
  ⚠⚠ LA SECONDE CAPACITE ETAIT CASSEE, ET DEUX FOIS. Elle n'a jamais eu de cas
  parce qu'on la croyait sans cle de verification ; en lui en ecrivant une, le
  09/09/2026, elle a rendu deux defauts : (1) la condition lisait
  `message.defeated_unit` (inexistant) puis se repliait sur `message.trigger`,
  qui designe le TUEUR — elle pesait donc la menace posee sur le HEROS, toujours
  nulle, et la capacite ne partait jamais ; (2) le choix des trois cartes du
  dessus n'avait pas de `from_where=["EncounterDeckTop"]`, donc aucune carte du
  deck n'etait une cible legale et rien n'etait defausse. Les deux corriges.
  ⚠ Le cas DESIGNE la carte a defausser, et ce n'est pas le dessus du deck : la
  distribution normale d'une carte de rencontre emporte le dessus de toute
  facon, un cas ecrit sur « une des trois » restait vert sans le module. **OUI**
- **su009** Mechanical Arms — track sur attaque de base + redressement. 1 cas.
  **OUI**
- **su010** Spider-Bot — les DEUX branches (track / retrait). 2 cas. **OUI**
- **su011** Web-Shooters — trait AERIAL + contre-cas dans l'autre forme. 2 cas.
  **OUI**
- **su012** Contingency Plan — Action de defausse + « jouable comme si en
  main ». **2 cas, 2/2 rouges sous substitution (09/09/2026)**. La seconde
  capacite avait ete declaree non testable ; c'etait vrai de la CLE `jouer`,
  pas du moteur : `face.IsLikeInHand()` (card.py:237) envoie
  `CheckIfFaceIsLikeInHand`, le message meme qu'ecoute
  `YouMayPlayCardLikeInHand`. Le cas mesure les DEUX bouts — la carte posee
  l'est, une carte de la defausse ne l'est pas. La carte, elle, etait juste.
  **OUI**
- **su013** / **su014** Ghost of a Conscience / Crisis of Conscience — les deux
  obligations, une par alter-ego, chacune sur son deck. 2 cas. **OUI**
- **su015** Goblin Protocol — la menace des sbires pistes compte pour le
  vilain. 1 cas. **OUI**
- **su016** * Hobgoblin — Forced Response apres son attaque. 1 cas. **OUI**
- **su017** Lunatic Laugh — degats indirects + desorientation des personnages
  reellement touches. 1 cas. **OUI**
- **su018** Goblin Glider — attache a l'ennemi aux PV IMPRIMES les plus hauts,
  Action a deux energies, et la branche SURGE. **3 cas, 2/3 rouges**.
  ⚠⚠ LA CLAUSE « without another Goblin Glider attached » NE FILTRAIT RIEN :
  le module cherchait le planeur deja pose dans `GetPlacedCardArea()` et
  `GetAttachedUpgrades()`, or Goblin Glider est une ATTACHMENT — il fallait
  `GetAttachedAttachments()` (card_face.py:1077). Deux planeurs se posaient donc
  sur le meme Rhino. Corrige le 09/09/2026. Le defaut n'apparait qu'avec DEUX
  exemplaires en jeu, ce qu'aucun cas ne montait avant celui du surge.
  ⚠ Le surge se monte SANS toucher au vilain : il suffit que tous les ennemis
  portent deja un planeur. Les deux exemplaires distincts se fabriquent par
  `Puzzle.CreateEncounterDeck('su018', 'su018')`, `Puzzle.Reveal` rendant deux
  fois la MEME carte (`FindOrCreateFace`).
  ⚠ Le cas « s'attache a l'ennemi aux PV les plus hauts » RESTE VERT sans le
  module (mesure du 09/09/2026) : une attachment se pose de toute facon sur le
  vilain. Il est conserve pour ce qu'il decrit, mais ce qui PROUVE l'attache,
  c'est le cas du surge. **OUI**
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

**Heros termine : NON** — il ne manque que ce qui ne peut pas s'automatiser :
la preuve de la biographie dans le wizard et une partie humaine.

⚠ MISE A JOUR DU 09/09/2026 : les TROIS capacites declarees « hors de portee du
harnais » le 08/09 sont desormais MESUREES (su008, su012, su018). Aucune ne
l'etait vraiment ; il manquait une cle, une commande ou une lecture. Et deux des
trois cartes etaient CASSEES, ce que seule l'ecriture de leur cas a revele.
Batterie du pack : **32/32 cas**.
