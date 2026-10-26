# Balayage « search … then <effet> » (26/10/2026)

Origine : Safe House #30 (54007) n'a rien fait en partie réelle. La première explication (la pioche était dans le `if face:` de la recherche) s'est révélée DOUTEUSE (voir §3) ; la cause réelle de la partie de l'utilisateur est un piège d'interface sur téléphone (corrigé dans `ui-app`).

## 1. Méthode

- Scripts examinés : **7 817 fichiers** de `src/cards/pack` (hors `__init__.py`) ; **497** utilisent `Search.*`.
- Analyse AST (`scratchpad/sw/balayage.py` et `balayage2.py`, lancés en `python -I`) :
  1. un effet INDÉPENDANT du résultat placé DANS le `if <résultat de recherche>:` (62 résultats, 28 cartes, dont les faux positifs de type « sinon, cherche » ou boucle `break`) ;
  2. un effet placé APRÈS le `if` et indépendant du résultat (35 résultats), croisé avec le texte imprimé.
- Chaque carte retenue a été confrontée à son texte imprimé (`data/cards.json`) et au Rules Reference v1.8, mot « THEN » (p. 44) : *« If the pre-"then" text of an effect does not fully resolve, the post-"then" text does not attempt to resolve. »* ; mot « SEARCH » : on cherche, on ajoute la carte trouvée, et on remélange le deck fouillé (le moteur le fait déjà dans `Search.SearchForCards` tant que `not_move` n'est pas posé).

## 2. Résultat

**Aucun défaut avéré nouveau.** Un effet qui ne dépend pas de la carte trouvée est bien placé hors du `if` partout où le texte n'a pas de « Then » ; un effet « Then » est bien conditionné partout (27018 Across the Spider-Verse, 39049 Cultist, hz003 Targeting Goggles, 4 cartes « si tu ne trouves pas, surge »).

| Cartes | Texte | Verdict |
|---|---|---|
| ss007, ss008 Spider-pathy | « …put it into play engaged with you. Draw 1 card. » (pas de « Then ») | ok : la pioche est hors du `if` |
| wc013 Transmutation | « Search… Then, shuffle… Draw 1 card. » | ok : la pioche est une phrase à part |
| wd150, 59026, 41020, 23024, 41008, 15027, 48002, 27040, 53041, 32088a | effet suivant dans une phrase indépendante | ok : hors du `if` |
| dt062 « That All You Got? » | « …Reveal that attachment → draw 3 cards » | ok : révéler est un COÛT, pas de pioche sans pièce |
| 24042, sk183, te004, te102, te103, 27135, 42027, 18011 | « si rien n'est entré en jeu, surge / défausse » | ok |
| 16059, 04077, 32101, 48034, 55005a, ip016 | « si X est en jeu … sinon cherche X et révèle-le » | ok (faux positifs : le `if` teste la présence en jeu) |
| 36020, ul035 | « …si cet allié est encore en jeu en fin de phase, ajoute-le à la main » | ok |
| 03001b, 45017 Suit Up, 62022, campaign_setup `EachPlayerSearchAllyToHand`, sk037b | recherche puis ajout à la main (+ remélange automatique) | ok |
| sk272, sk276, 38009, 56159, bl016, hz003 | l'effet suivant dépend de la carte trouvée | ok (hz003 déjà corrigé le 26/10) |
| ze014, sb018, dt075, 56072, 56059, 56096b | boucles / recherches de l'équipe ennemie | texte lu ; code non relu ligne à ligne (faux positifs de l'analyse) |

## 3. DOUTEUX : « Then » après « put it into play » (Safe House #30 et Cultist)

- **54007 Safe House #30** : « …search the encounter deck for a minion and put it into play engaged with you. (Shuffle.) **Then, draw 1 card.** »
  Le script actuel (corrigé le 26/10 par une fork) pioche TOUJOURS, même sans sbire trouvé, au motif que « la recherche a eu lieu ». Mais la partie avant « Then » contient « put it into play » : sans sbire, elle ne se résout pas **entièrement**, et la règle « Then » dit que la partie après « Then » ne tente alors pas de se résoudre. Lecture stricte = pas de pioche sans sbire (c'était le code ORIGINAL). Les autres cartes du projet suivent la lecture stricte : 27018 (choisir un joueur seulement si l'allié est mis en jeu), 39049 Cultist (« Then, discard Cultist » seulement si The Kraken est mis en jeu), hz003 (corrigé le 26/10 selon la même règle). À l'inverse, Spider-pathy (ss007/ss008) n'a PAS de « Then » : la pioche est inconditionnelle.
- **Question à poser à l'utilisateur, carte montrée (`assets/pics/54007.jpg`)** : sans sbire dans le deck de rencontre, Safe House #30 doit-elle faire piocher ?
  - A (recommandée, lecture stricte de la règle « Then », cohérente avec Cultist et 27018) : non, pas de pioche ;
  - B (code actuel) : oui, la recherche a eu lieu.
  Si A : remettre `initiator.DrawUp(1, effect)` DANS le `if face:` de `src/cards/pack/winter/winter_soldier/54007.py` et changer le cas `[ws]` « aucun sbire » de `tools/cas/winter_safe_house.py` pour attendre `taille_main` 1.
- Rien n'a été modifié dans le code par ce balayage.

## 4. Limites

- L'analyse ne voit que les motifs `X = Search.…(…)` suivis d'un `if X`. Un résultat de recherche passé en rappel (`process_choose`), ou un effet décidé par un autre helper (`Find.FindAndReveal`), n'est pas couvert.
- Les 6 cartes marquées « code non relu » n'ont pas de défaut vu dans le texte, mais leur code n'a pas été lu ligne à ligne.
