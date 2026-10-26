# Arbitrages des héros fan-made (26/10/2026)

Les questions en attente des gabarits (`docs/packs/*/GABARITS.md`) ont été tranchées le 26/10/2026 dans cet ordre : d'abord le Rules Reference v1.8, puis le scan de chaque carte, puis les notices des auteurs quand le zip en contient une (Batman, Warriors Three). Le détail, carte par carte avec citation de la règle, est dans `docs/packs/<pack>/VERDICTS-REGLES-2026-10-26.md`.

## Décisions de l'utilisateur (26/10/2026)

Wasp (Hank Pym), Q1 à Q5 : option A (déjà codée).

Ces 6 doutes restaient après lecture des règles. Ils ont été posés un à un, carte montrée :

| # | Carte | Décision | Code |
|---|---|---|---|
| 1 | bm020 Detective Work, « Investigate » du Boost | ignoré (reste d'une ancienne version), seule la carte boost en plus s'applique | inchangé |
| 2 | cr011 / cr012, « Discard a card you control » | en jeu seulement | inchangé |
| 3 | rm014 Hound Program, « Hero Response » | Réponse forcée, en forme héros | inchangé |
| 4 | rz006 Wakandan Stealth Tech, résolu par Driven | UN seul Special, au choix du joueur | **à changer** |
| 5 | co012 Mentor, « your deck » du When Defeated | deck du joueur qui a vaincu Mentor | **à changer** |
| 6 | rl016 New Host | le sbire défaussé est révélé (engagé avec vous) et New Host s'y attache | inchangé |

## Corrections imposées par les règles (aucune question à poser)

Liste de travail. Pour chaque ligne, le détail est dans le fichier de verdicts du pack.

- **Transversal, Wild** (RR « Wild Resource ») : un wild dépensé compte pour UN type choisi par le joueur ; hors paiement, il ne compte que pour « wild ». Cartes touchées : Ch'od (co005, co008 à co010, co012, co013), Batgirl (bg005).
  **FAIT le 26/10/2026** (fiche `reference/mots-cles/wild-resource.md`, blocs « arbitrage Wild » des gabarits Ch'od et Batgirl) : `GetPaidResources(True)` pour co005 et bg005 ; helper `Types` à quatre types {R, B, Y, G} pour co008-co010, co012, co013, co015. Cas Ch'od / Batgirl réécrits ou ajoutés, vus ROUGES avant, VERTS après ; cas `bg003` et `bg006` (option 2) réécrits car ils encodaient « le wild ne vaut aucune ligne ». Non touché : `doctor_druid` (`BonusSelonLaMain` lit encore `GetColor(c)`, wild compté pour trois couleurs) et la ligne `bg004` de RECETTES (hors périmètre de ces correctifs).
- **Transversal, copies par titre** (RR « A copy of a card is defined by title ») : les Energy / Genius / Strength refaits sont des copies de 01088 / 01089 / 01090 pour « Max 1 per deck ». Packs : bm023-025, cr017-019, rz013-015, rl018-020, wt023-025, co017-019. Il faut les traiter en arts alternatifs (GUIDE §12 bis) et vérifier le constructeur de deck.
  **FAIT le 26/10/2026** : traité comme collection d'art des ressources doubles (précédent Gwenpool / Beast / Binary), pas comme suppression de cartes : neuf collections (`roz`, `batgirl`, `batman`, `corsair`, `hepzibah`, `raza`, `chod`, `smasher`, `warriors_three`) dans `variantes.ts` ET `COLLECTIONS_RESSOURCES` (`app.js`), par défaut au héros de même nom. Le constructeur compte DÉJÀ « Max 1 per deck » par titre (`cleCopie`) : aucun correctif, test `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs`. Hors liste initiale mais même cas : `bg020-022`, `hz016-018`, `sz016-018` (traités) ; `pd021-023` (Predator, deck les contient) NON traités.
- **Wasp** : hp007 (inclure identité et Mansion), hp009 (répartition entre manigances), hp011 / The Stinger hp012 (exactement X dégâts), hp013 (Shadow of the Past 01190 et Pursued by the Past 45075 EXISTENT dans le moteur, les brancher ; exhaust de Hank = coût de l'Action), hp017 (surge non imprimé à retirer ; trait HACKED à vérifier).
- **Batman** : bm001b (réduction par trait, soutiens compris), bm008 (DEF en plus), bm014 (Hazard 1 ; icônes de la carte du dessus de la défausse), bm015 (remélange d'une dissuasion non résolue → Two-Face), bm016 (égalité : choix du premier joueur ; icônes de boost comme bm014).
- **Corsair** : cr007-009 (dernière carte jouée sur toute la partie), cr016 (Alliance : tout coût payable à plusieurs), cr001a (la ressource est défaussée avant d'être glissée : les Réponses « after you discard » la voient).
- **Rachel Summers** : rm007 (Max par titre pour toute la table).
- **Roz** : rz002 / rz003 (tout allié Thor en jeu ; une fois par TOUR), rz006 (décision 4).
- **Warriors Three** : Q1 à Q3 (états par héros, Résistance sur Volstagg inactif, soutien du héros actif pas en jeu), Q6 (Fimbuldraugr : toutes les cartes joueur), Q9 (A Questing attaché au sbire), Q15 (« this turn » = tour du joueur).
- **Ch'od** : décision 5, plus la partie wild.
- **US Agent** : us004 (dégâts en coût : tout ou rien), us010 (Réponse reproposée à la rafale).
- **New Ultimate Winter Soldier** : uw006 (répéter inclut le coût : nouvelle défausse).
- **Raza** : rl001 (« unattached » = pas attaché à une autre carte), rl008 (vérifier le contre-cas Retaliate).
- **Spider-Punisher** : sq005 / sq012 (trait AERIAL réel), sq013 (toute amélioration WEB-SHOOTER en jeu), sq014 / rl017 (le premier joueur choisit).
- **Batgirl** : bg005 (wild), bg012 (réduction facultative, forme héros).
- **Hepzibah** : hz003 (« then » : rien si aucun événement), hz007 (effet durable jusqu'à la fin de la phase des joueurs suivante), Q5 (ajouter un cas étape du vilain).
- **Smasher** : sz001b (une fois par tour), sz004 via sz005 (« (attack) » = attaque).
- **Sunspot (Hellfire)** : so005 (seconde manigance obligatoire) ; **images so001a / so001b inversées** par rapport aux faces.
