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
    pris au pied de la lettre — confirmé avec l'utilisateur le 21/10/2026,
    aucun changement).
  - **Imperial Guard, exclusion RÉELLE** (décision utilisateur du 21/10/2026) :
    `CorrigerImperialGuardExclue`, appelée après la mise en place aux
    scénarios 1, 2 et 4, remplace toute carte déjà notée « Imperial Guard
    Removed » si le tirage aléatoire du modulaire l'a quand même repiochée
    (environnement en jeu ou sbire dans le deck de rencontre), par une autre
    carte du même groupe encore disponible. `CardFactory.RandomPick`
    lui-même n'a pas été touché (mécanisme partagé, réutilisable par
    d'autres packs à l'avenir) : la correction reste confinée à ce pack.
  - Scénario 5 (Supreme Intelligence), mise en place : Nega-Bomb (gs222a) en
    jeu avec menace = Time Pressure × nombre de joueurs (remplace sa menace
    imprimée 8[par héros]) ; les deux Green Interference (gs223) mélangées au
    deck de rencontre ; pour chaque bonne devinette « Odd card » (case saisie
    par le joueur, voir plus bas), le groupe choisit un allié IDENTITY-SPECIFIC
    à ajouter à la réserve ; chaque joueur peut ensuite mélanger un allié de la
    réserve dans son deck ; **et désormais, remplacement CIBLÉ** (décision
    utilisateur du 21/10/2026) : `chaque_joueur_peut_remplacer_un_allie`
    retire un allié IDENTITY-SPECIFIC du deck (`ClassCard.IsClass`, base
    native) et pose un allié de la réserve à sa place, fidèle au texte
    imprimé.
  - Expert : PV persistants + soin par pion accélération réutilisés tels
    quels depuis `mts.campaign` (`ExpertCampaignSetPlayersHPToTheirRemainingHP`,
    `ExpertMayPlaceAccelerationToHeal`), aucun code propre nécessaire.
- **`tools/epreuves_campagnes.py`** : 5 épreuves (boucle complète victoire →
  mise en place suivante), **5/5 vertes** :
  1. victoire Kree Sentry avec Gladiator vaincu : Rick Jones + Gladiator
     recrutés, Imperial Guard retirée notée ;
  2. victoire Kree Sentry sans Gladiator : seul Rick Jones recruté (contre-cas) ;
  3. Time Pressure cumulée → menace de départ de la Nega-Bombe au scénario 5
     (la preuve la plus importante : un carnet ENTRANT change vraiment la mise
     en place de la partie SUIVANTE) ;
  4. une carte Imperial Guard déjà retirée de la campagne (carnet entrant)
     n'est pas repiochée au scénario suivant, remplacée par une autre du
     même groupe ;
  5. remplacement ciblé d'un allié d'identité (Epoch, Quasar) par un allié de
     campagne (Binary) disponible en réserve.
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
  fait nativement par `WriteCampaignLogAtGameOver`, réutilisé). Confirmé
  avec l'utilisateur le 21/10/2026 : pas de nouveau chantier moteur pour ça.
- **Odd cards** : le livret lui-même dit que c'est une devinette facultative,
  non vérifiée mécaniquement même au jeu de plateau (« players may still
  discuss them to determine which was the Odd card »). Implémenté fidèlement
  comme une case saisie par le joueur (« Odd Guesses Correct », 0 à 4), pas
  comme une comparaison automatique aux solutions imprimées.
- **Time Pressure, texte pris au pied de la lettre** : « if the round dial is
  higher than the Time Pressure value recorded, replace it with the dial
  value » — la valeur ne BAISSE jamais, même si elle semble aller à l'encontre
  de l'esprit « fewer rounds, better position » décrit juste au-dessus dans le
  même livret. **Confirmé avec l'utilisateur le 21/10/2026** : lecture
  littérale retenue, aucun changement.

## Trouvé en terminant l'investigation gs224/gs226 (21/10/2026)

- **gs224 et gs226 sont maintenant 13/13 en preuve par substitution**, voir
  CAMPAGNE-ALLIEES-GABARITS.md pour le détail des deux pièges de cas de test
  (un crochet fermant dans le prompt, `hors_jeu` trivialement vrai sur une
  carte face cachée) et du vrai bug trouvé au passage dans `gs226.py`
  (`message.damage_targets` n'existe pas, corrigé en `took_damage_targets` —
  Lauri-Ell plantait en partie réelle des qu'elle blessait un ennemi).
- Nouvelle commande `Puzzle.GiveFacedownBoost(cible, carte)` ajoutée à
  `game/puzzle/puzzle.py` (seeder une pile de boost hors activation, utile à
  tout futur pack qui mesure ce genre de capacité).
- **Bug de données pré-existant trouvé en chaînant la campagne vers le
  scénario 2** : `gs120b` (Shi'ar Throne face B) n'avait aucun `desc.Class`
  dans `data/cards.json`, ce qui faisait planter `CheckPrintedValue`
  (`assert self.card_classes != []`) dès que `CreateSetAside` construisait
  la mise en place réelle de Majestrix's Verdict — jamais détecté avant
  faute d'un test qui montait cette mise en place en entier. Corrigé
  (`"Class": "Encounter"`, modèle `16142` Milano/`60153` Ben Urich), checksum
  de `cards.json` recalculé (`tools/recalculer_checksums.py`).

## Reste à faire pour une fidélité totale

- Partie/autoplay complète des 5 scénarios enchaînés : demandée par
  l'utilisateur, en cours.
- Pages de livret pour l'écran de campagne (`pages_regles`, `intro`/`regles`/
  `epilogue` par scénario) : demandées par l'utilisateur, en cours.
