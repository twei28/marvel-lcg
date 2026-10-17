# Aspects TMNT (Inkwire) : coquilles et choix tranchés

Liste tenue pour pouvoir y revenir. Chaque ligne dit ce que le scan imprime, ce qui a été décidé, et
l'effet en jeu. « Réponse du 17/10/2026 » = tranché par l'utilisateur.

## A. Règles générales

| # | Sujet | Décision | Effet |
|---|---|---|---|
| G1 | Reskin dont seule l'IMAGE change | Art alternatif de l'officielle, proposé à tous les héros ; version TMNT d'office pour un héros TMNT | Pas de carte en double. **APPLIQUÉ le 17/10/2026, branche `conversion-art-seul`** : 67 cartes converties (`tools/convertir_reskins_art_seul.py` ; colonne `converti_art_alternatif_de` de `tools/tmnt_aspects_numerotation.tsv`, numérotation figée, aucun id réattribué). Les 3 ressources doubles ub011, ub016, ub054 restent des cartes (collection `tmnt`) |
| G2 | Reskin où la MOINDRE autre chose change (nom, traits, texte, coût, ressource, unicité, bandeau) | Carte exclusive TMNT | 89 cartes concernées |
| G3 | Bandeau « ✦ titre d'origine » imprimé sous le titre (ex. Bo-Wing « ✦ Winter Soldier ») | L'unicité se juge sur LES DEUX titres (`unique_also`) | Bo-Wing et Winter Soldier ne coexistent pas |
| G4 | Rampage X avec moins de X cartes dans le deck | Jouable, on défausse ce qui reste | Déjà codé |
| G5 | Même titre qu'un héros ou allié TMNT (Nobody, Alopex, Venus, Splinter) | Même personnage : unicité normale, ils ne coexistent pas | Un joueur Alopex ne peut pas poser l'alliée Alopex |
| G6 | Intensified | Une par personnage, deux si Solide ; option de préparation te201 | Déjà codé |

## B. Coquilles de l'auteur : décision prise

| Carte | Scan imprime | Décision | Effet en jeu |
|---|---|---|---|
| ua019 Flow of Battle | « Prerequisite (MARTIAL ARTIST) » (mot jamais défini) | Jouable seulement si l'identité a le trait MARTIAL ARTIST | Spider-Man ne peut pas la poser, Daredevil oui |
| ua037 Slash | « take 3 damage » sans sujet | Vous (l'identité) subissez les 3 dégâts | Slash reste à 5 PV |
| ua033 Pete | « After you deal damage » | Identité + cartes que vous jouez ; un allié qui attaque ne compte pas | Precision Strike déclenche Pete |
| uj002 Chance Encounter | « Attach to a scheme » (officielle : « side scheme ») | **Coquille : manigance annexe seulement** | Comme l'officielle 26034. À reprendre dans le code (le code actuel suit le scan) |
| uj036 Venus (Bonnie) | « a discard pile » (Manifold : « discard pile ») | Coquille : comme Manifold, SA défausse | Identique à Manifold (code déjà ainsi) |
| uj040 Zone of Silence | « 4 card cards » | Texte affiché corrigé en « 4 cards » (choix pris sans te le demander, cosmétique) | Aucun effet de jeu |
| up030 Redirection Mastery | « After you exactly defend an attack » | Défense exacte : l'attaque vaut exactement votre DEF | Rare à déclencher, renvoie toute la DEF. **Script à écrire (la carte ne fait rien aujourd'hui)** |
| up018 « I Can Do This All Day » | « Hero Action » avec « When » (officielle : Hero Interrupt) | Coquille : Hero Interrupt ; texte affiché corrigé | Se joue pendant l'attaque d'un ennemi (code déjà ainsi) |
| up024 Nobody | Même titre que l'allié d'Alopex (ta002) | Ils ne coexistent pas (G5) | Code déjà ainsi |
| ul001 Alopex, ul039 Venus, ul029 Splinter | Même titre qu'un héros / allié | Ne coexistent pas (G5) | Code déjà ainsi |
| ul019 Old Hob | Trait « MUTANIMALS » | Coquille : MUTANIMAL | Splinter Dojo Training et Attack Training s'y attachent. **À reprendre dans le code (suit le scan)** |
| ul033 Take a Stand, ub002 Assess the Situation | Trait TACTIC absent | Oubli : on remet TACTIC | À reprendre dans le code |
| ub047 Sky Wagon | Trait LOCATION absent | Oubli : on remet LOCATION | À reprendre dans le code |
| ul031 Suit Up | « attached to AN ally » (officielle : « THAT ally ») | **Lecture littérale** (contre la recommandation) | Recherche plus large : toute amélioration attachable à un allié. **Script à reprendre** |
| ul038 « Unified Stike » | « Hero Response: When » et titre « Stike » | Hero Interrupt, titre corrigé « Unified Strike » | À reprendre dans le code (titre) |

## C. Coquilles cosmétiques gardées en l'état (non bloquantes)

- ul025 « Shugun » (texte de Shōgun), ul041 « Musroom », ul031 citation « TIme » : texte affiché tel qu'imprimé.
  Question posée dans le fichier de Leadership, pas encore tranchée.

## D. Corrections d'officielles faites par les agents en route (à relire)

- 56010 Two-Gun Kid : le second ennemi pouvait être le même que le premier.
- 62020 Hulk (Luke Cage) : l'ATK par compteur rage ne se recalculait pas.
- 60029 Stick : les deux options du « choose » étaient deux Interruptions distinctes.
- 58031 Cameo : plantait en autoplay (allié créé dans le scénario au lieu du joueur).
- Cost `Exhaust` : une carte qui « ne s'incline pas pour défendre » peut défendre même inclinée (aussi 53011).
- Nouveau message `WhenCalculatingAttackDamage` (Tonfa).
- Non corrigés : 61016 Spider-Woman (Réponse jamais déclenchée), 33021 Danger Room (trait MUTANT non exigé).

## E. Encore à trancher

- ul044 « You Got This! » : ressource physique (scan) ou énergie (officielle).
- ub019 Honorable Blades : Usagi Yōjimbō n'existe pas dans la base ; scan « Yōjimō ».
- Basic : alliés homonymes de héros ou alliés TMNT (Leonardo, Donatello, Michelangelo, Raphael, Casey Jones, Jennika, Slash, Splinter), sous-titres Leo / Donnie / Mikey / Raph / Jenny = alter egos des héros.
- Dual : Q-UD1 (sous-titres identiques aux alter egos), Q-UD2 Heavy Metal (« a status card »), Q-UD3 Stealth Fighter (« Interrupt: After… »), Q-UD4 Sōhei (alter ego).
- Coquilles de chiffres à confirmer : Jōtarō coût 3 (le tableau disait 2), « Hero Response » de Atilla (« Forced Response » codé tel quel), Fugitoid, Gofu Talisman (lectures prises par l'agent Basic, non posées).
- Cartes Chain Reaction et Combo Move : créées comme nouvelles, car introuvables dans la base.
- Deck-builder : voir G1/G2 (fenêtre « arts alternatifs ? Oui / Non / Ne plus proposer »), à coder.

## F. Réponses du 17/10/2026 APPLIQUÉES au code (branche `retouches-cartes`)

Mise à jour des sections B et E ci-dessus : tout ce qui y est marqué « à reprendre dans le code » ou « à trancher » pour les
cartes suivantes est fait (ul044 et ub019 de la section E aussi ; Q-UD2, Q-UD3, Q-UD4 de la section E aussi). Chaque carte : cas,
substitution rougie, gabarit PROCESSUS-CARTE mis à jour (`aspects-<aspect>-gabarits.md`), « Carte terminée : OUI ».

| Carte | Décision | Ce qui a changé |
|---|---|---|
| uj002 Chance Encounter | « Attach to a SIDE scheme » (coquille) | `ability_link 26034`, script propre supprimé, texte « side scheme » / FR « manigance annexe » |
| ul019 Old Hob | trait MUTANIMAL (pas MUTANIMALS) | trait corrigé, « MUTANIMALS » retiré de `CardFace.TRAITS` ; Splinter Dojo Training et Attack Training s'y attachent (cas) |
| ul033 Take a Stand, ub002 Assess the Situation | trait TACTIC remis | `traits: ["TACTIC"]` |
| ub047 Sky Wagon | traits du scan NYC, VEHICLE confirmés (PAS LOCATION) | rien (cas de donnée ajouté) |
| ul031 Suit Up | lecture littérale « attached to AN ally », recherche large | script réécrit (voir gabarit) |
| ul038 | titre « Unified Strike », Hero Interrupt | titre corrigé (cards.json), texte affiché « Hero Interrupt » / FR « Interruption de héros » |
| ub019 Honorable Blades | INTÉGRÉE : Team-Up Leonardo + Usagi Yōjimbō (= allié `up041`) | entrée + script `ub019.py` (`desc.TeamUp`, `.SetTarget("TeamUp")`), texte FR |
| ud005 Sōhei | « your hero +2 hand size » vaut aussi en alter ego | script corrigé (plus de test `Hero.IsType`) |
| up030 Redirection Mastery | « défense exacte » (attaque, boosts compris, == DEF) | script écrit + **extension moteur** : `Message.AfterUnitDefendEnd.damage_before_defense / defense_value` |
| up018 | Hero Interrupt | texte affiché corrigé |
| ua019, ua037, ua033, uj036, uj040, ul044, ud003, ud004 | réponses rendues (voir gabarits) | aucun changement de code |

Toutes les unicités homonymes (même titre = même personnage : Alopex, Nobody, Venus, Splinter, Slash, Old Hob / White Wolf...)
restent « ne coexistent pas » (décision G5, code déjà ainsi). L'unicité par sous-titre (Q-UD1) et le deck-builder / arts
alternatifs sont traités par d'autres agents.
