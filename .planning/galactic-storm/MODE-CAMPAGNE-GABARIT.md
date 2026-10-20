# Galactic Storm : mode campagne (chantier B)

Date : 21/10/2026. Référence : `docs/packs/galactic-storm/REGLES.md` §4 (mode
campagne) et §7/9/10/11/13 (instructions de campagne par scénario, un bloc par
scénario). Modèle suivi : `src/cards/pack/mts/campaign.py` (The Mad Titan's
Shadow), la boîte la plus proche en volume (234 lignes) et déjà conçue pour
être réutilisée par d'autres boîtes (`WriteCampaignLogAtGameOver`,
`FaceExists`, `ExpertMayPlaceAccelerationToHeal` importés directement).

## Ce qui a été construit

- **`Fusion/marvel-lcg-src/data/campagnes/galactic_storm.json`** : les 5
  scénarios dans l'ordre (Kree Sentry, Majestrix's Verdict, Hala Ultimatum,
  Earth Under Siege, Supreme Intelligence), avec leurs champs de victoire
  déclaratifs (lus par le panneau de récompenses de l'écran, `ui-app/src/
  board/campagne/`). `expert.pv_persistants = true` + `victoire_commune_expert`
  (PV restants par joueur) comme les autres boîtes.
- **`Fusion/marvel-lcg-src/src/cards/pack/galactic_storm/campaign.py`** :
  `CampaignSetup(level)`, câblée dans la face 1A de la manigance principale de
  chaque scénario (`gs079a`, `gs117a`, `gs141a`, `gs161a`, `gs198a`, un
  `*CampaignSetup(N)` ajouté à chacune, modèle `mts/ebony_maw/21074a.py`).
  - Alliés recrutés + réserve de campagne (« Campaign Pool: <nom> ») pour les
    3 alliés de base (Rick Jones, Gladiator, Lauri-Ell) et les Starjammers
    basiques (Ch'od, Corsair, Hepzibah, Korvus, Raza) — Gladiator (le SBIRE
    Imperial Guard gs098, à ne pas confondre avec l'ALLIÉ DE CAMPAGNE gs225 du
    même nom) détecté en pile de victoire via `FaceExists(.., in_victory=True)`.
  - Imperial Guard : cartes non-traîtrises utilisées (gs091-gs111) enregistrées
    au carnet (« Imperial Guard Removed »), scénarios 1 et 2 seulement (le
    scénario 3 ne l'emploie pas, le scénario 4 ne le mentionne pas dans ses
    instructions de victoire malgré sa présence dans l'encounter deck — lu
    tel quel dans REGLES.md §11).
  - Time Pressure (round du cadran) : enregistrée aux scénarios 2-4,
    REMPLACÉE SEULEMENT SI LA NOUVELLE VALEUR EST PLUS HAUTE (texte imprimé
    pris au pied de la lettre, voir « Écart assumé » plus bas).
  - Scénario 5 (Supreme Intelligence), mise en place : Nega-Bomb (gs222a) en
    jeu avec menace = Time Pressure × nombre de joueurs (remplace sa menace
    imprimée 8[par héros]) ; les deux Green Interference (gs223) mélangées au
    deck de rencontre ; pour chaque bonne devinette « Odd card » (case saisie
    par le joueur, voir plus bas), le groupe choisit un allié IDENTITY-SPECIFIC
    à ajouter à la réserve ; chaque joueur peut ensuite mélanger un allié de la
    réserve dans son deck.
  - Expert : PV persistants + soin par pion accélération réutilisés tels
    quels depuis `mts.campaign` (`ExpertCampaignSetPlayersHPToTheirRemainingHP`,
    `ExpertMayPlaceAccelerationToHeal`), aucun code propre nécessaire.
- **`tools/epreuves_campagnes.py`** : 3 épreuves (boucle complète victoire →
  mise en place suivante), **3/3 vertes** :
  1. victoire Kree Sentry avec Gladiator vaincu : Rick Jones + Gladiator
     recrutés, Imperial Guard retirée notée ;
  2. victoire Kree Sentry sans Gladiator : seul Rick Jones recruté (contre-cas) ;
  3. Time Pressure cumulée → menace de départ de la Nega-Bombe au scénario 5
     (la preuve la plus importante : un carnet ENTRANT change vraiment la mise
     en place de la partie SUIVANTE).
- `test_cards` 7019/7019, `verifier_appels_modules galactic_storm` : OK.
- Corrections au passage : `data/sets_info.json` « 144. Custom (Galactic
  Storm) » listait 4 scénarios sur 5 (Earth Under Siege manquait) et un
  `max_id` périmé (`gs223` au lieu de `gs349`) — aucun rapport avec la
  campagne, trouvé en vérifiant l'enregistrement du pack, corrigé.

## Pièges trouvés en écrivant les épreuves (jamais vus sans elles)

- **`RecruteAllie` écrasait la liste au lieu de l'allonger** quand elle est
  appelée deux fois dans le MÊME `collect_fn` (Rick Jones puis Gladiator à la
  même victoire) : elle relisait le carnet ENTRANT à chaque appel au lieu du
  dict `updates` en cours de construction. Rick Jones disparaissait du carnet
  sortant dès que Gladiator était recruté la même partie. Corrigé.
- **Une carte « utilisée » peut avoir déjà quitté le jeu à l'instant de la
  victoire** : Gladiator (gs098), vaincu, est en pile de victoire — pas « en
  jeu ». Le premier jet ne vérifiait que `in_play=True` pour le retrait
  Imperial Guard et manquait donc exactement le cas qui compte le plus (un
  méchant/sbire vaincu). Corrigé (`in_play=True OR in_victory=True`).
- **Un environnement Imperial Guard est TOUJOURS en jeu dès que le modulaire
  est actif** (le set en choisit un au hasard à la mise en place, c'est la
  règle « SETTING », déjà câblée au lot GS-4) : une épreuve qui ne pose aucun
  Imperial Guard explicitement voit quand même ce card_id dans le relevé — pas
  un bug, mais une épreuve mal conçue au premier jet (corrigée).

## Ce qui N'EST PAS mécaniquement enforcé (choix assumé, documenté dans
`campaign.py` lui-même)

- **La rotation à 3 identités** (« unlike other campaigns, players do NOT
  choose a single hero ») : choisir QUELLE identité amener à quel scénario, et
  la restriction de deckbuilding associée (« no unique card matching the
  log »), se jouent ENTRE deux parties, au moment de construire le deck
  suivant. **Vérifié avant d'écrire une ligne de code : aucune campagne de ce
  dépôt n'implémente de restriction de deckbuilding** (grep exhaustif sur
  tous les `campaign.py` existants). Ce n'est donc pas un trou propre à
  Galactic Storm : ce moteur ne contrôle cette classe de règle nulle part,
  et le jeu de plateau lui-même ne la vérifie pas mécaniquement non plus
  (le joueur la respecte en la lisant sur son carnet). Pas de code ajouté ;
  le carnet continue d'enregistrer l'identité jouée à chaque partie (déjà
  fait nativement par `WriteCampaignLogAtGameOver`, réutilisé).
- **Retrait Imperial Guard pas réellement exclu du tirage aléatoire futur** :
  noté au carnet (affiché au joueur), mais le tirage « 1 environnement + 6
  sbires au hasard » (`data/encounter_sets/gs_imperial_guard.json`,
  `random_pick`) ne lit pas cette liste. Écart mineur documenté en tête de
  `campaign.py` : à reprendre si on veut la fidélité totale (il faudrait
  paramétrer `CardFactory.RandomPick` avec une liste d'exclusion).
- **Odd cards** : le livret lui-même dit que c'est une devinette facultative,
  non vérifiée mécaniquement même au jeu de plateau (« players may still
  discuss them to determine which was the Odd card »). Implémenté fidèlement
  comme une case saisie par le joueur (« Odd Guesses Correct », 0 à 4), pas
  comme une comparaison automatique aux solutions imprimées.
- **Time Pressure, texte pris au pied de la lettre** : « if the round dial is
  higher than the Time Pressure value recorded, replace it with the dial
  value » — la valeur ne BAISSE jamais, même si elle semble aller à l'encontre
  de l'esprit « fewer rounds, better position » décrit juste au-dessus dans le
  même livret. Appliqué tel qu'imprimé (règle du projet : fidélité à 100 %,
  ne jamais « corriger » un texte qui semble bizarre sans trancher avec
  l'utilisateur) — **point à confirmer avec l'utilisateur si besoin**, pas
  encore posé en question.

## Reste à faire pour une fidélité totale

- Trancher avec l'utilisateur le point Time Pressure ci-dessus (lecture
  littérale retenue par défaut, pas encore validée).
- Exclusion réelle des cartes Imperial Guard retirées du tirage aléatoire
  futur (actuellement informationnel seulement).
- « Each player may choose one identity-specific ally in their deck and
  replace it with a campaign identity-specific ally » (scénario 5) :
  implémenté de façon SIMPLIFIÉE (mélanger un allié de la réserve dans son
  deck, sans retirer/remplacer un allié existant précis) — le remplacement
  ciblé n'a pas été construit faute de temps.
- Aucune partie manuelle/autoplay complète des 5 scénarios enchaînés n'a été
  jouée : seules les épreuves ciblées (3/3) et la construction (`test_cards`)
  sont vérifiées. Une vraie partie de bout en bout reste le seul juge final
  (comme toujours, voir PROCESSUS-CARTE.md §"Ce que ces blocs ne peuvent pas
  voir").
