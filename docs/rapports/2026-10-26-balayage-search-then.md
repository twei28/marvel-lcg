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

---

# Relecture ligne à ligne des six cartes survolées (26/10/2026, suite)

Texte imprimé (data/cards.json) + script lus en entier, comparés à la règle « Then » / « Search » du Rules Reference v1.8. Cas dans `tools/cas/relectures_search.py` (préfixe `[rs]`).

| Carte | Verdict | Détail |
|---|---|---|
| **dt075** Multiverse Shenanigans | **DÉFAUT, corrigé** | « choose any 3 **different** … cards » : le script appelait 3 fois `Search.Collection` sans exclure les titres déjà choisis ; le pilote prend toujours la première option : 3 exemplaires de la MÊME carte (« Hulk ») sous la carte. Correctif : `check_fn=lambda paper: paper.name not in deja_choisis`. Cas VU ROUGE (1 titre distinct au lieu de 3), vert après, rouge sans le module. Cas Action (épuiser + carte rencontre face cachée → 1 carte de côté en main) ajouté, vert / rouge sans module. La carte n'avait AUCUN cas avant. Ajouts de banc : clé `pose_sous_titres_distincts` (test_capacites.py), `Puzzle.SendGameBeginSetup()` (puzzle.py). |
| **ze014** The Mother of Night | correct | Pas de « Then » : « place 1 additional threat for each facedown card placed » = autant que de cartes posées ; `if faces:` juste. Deux recherches enchaînées, cas existants (test_capacites.py ~30290) les couvrent (3 menaces, cartes rendues à la défaite). |
| **sb018** Musha Shugyō | correct | « may search … up to 2 OATH » : boucle de 2 recherches `may=True`, arrêt au premier refus/échec ; cas existants (tools/cas/tmnt_shinobi_bushido.py) couvrent 2 OATH, défausse, « up to 2 ». Lecture « characters other than the owner » = identité du propriétaire seule (précédent 40006 Technovirus Purge). |
| **56072** Stark Tower | correct | « searches … and your team reveals it » : la révélation dépend de la trouvaille, `if face:` juste ; deck ET défausse fouillés. Cas coop ajouté (56065 en défausse de rencontre → attaché à Iron Man), vert / rouge sans module. |
| **56096b** S.H.I.E.L.D. Recruits | correct | `Players.ForEachPlayer` ne parcourt que les joueurs de la table de l'effet (`Worlds.GetPlayers` filtre sur la zone) : « each player on your team » juste. Cas coop ajoutés (1 sbire donné face cachée puis révélé ; contre-cas sans sbire), vert / rouge sans module (le contre-cas d'absence reste vert). |
| **56059** Iron Man (Leader) | correct à la lecture, NON testé | Même structure que 56072 (Setup, deck seul : `include_discard_pile=False` conforme). Carte de type Leader : non montable en coop dans le harnais. |

⚠ **Limite commune aux trois cartes Civil War** : aucun cas du dépôt ne monte le mode COMPÉTITIF (deux équipes). Mes cas rejouent la carte en mode coopératif (`Worlds.GetEnemyTeam` = premier joueur) ; le partage entre deux tables n'est pas prouvé.

## Journaux d'autoplay Warriors Three et Ch'od (8 parties chacun, relancés le 26/10/2026 après toutes les corrections)

Rhino / normal / équilibré, graines 1 à 8, `python tools/autoplay.py <game_dir> --deck <deck> --vilains rhino --difficultes normal --profils equilibre --parties 8`. 0 victoire sur 16 (cause : deck de joueur de ressources neutres du pilote, voir RECETTES : le 0 % ne mesure pas le héros).

- **Lu :** grep de tous les mots d'alerte (Traceback, Error, Exception, impossible, refus, échec, invalide, introuvable, <W>, <E>) : 0 ; lignes consécutives identiques : 0 ; le message « la boucle de jeu s'est arrêtée » est le résultat normal (verdict « terminee »). Lecture ligne à ligne des séquences touchant les cartes des deux packs, dans les journaux wt1, wt2, wt5, wt6, wt7 et co1, co3, co5 :
  - changement de héros actif par wt002 : liaisons/déliaisons des bonus correctes (Fandral ↔ Hogun ↔ Volstagg) ;
  - Artful Bladework : 4 dégâts, puis +2 SEULEMENT quand Fandral paie (wt1 lignes 81-110, wt6 lignes 392-411) ;
  - Hildegarde : bonus +1 ATQ/+1 CTR qui suit le héros actif jusqu'à la fin de phase ;
  - Fimbuldraugr (retire 1 menace) et Hridgandr (1 dégât) : Réponses déclenchées au changement de héros actif ;
  - A Questing We Shall Go! : sbire révélé, carte attachée, +5 PV (wt2 lignes 967-987) ;
  - Fenris : menace sur Countdown to Ragnarok ET sur le complot principal à chaque machination ; Fenris n'encaisse aucun dégât ; Skadihr révélée et engagée avec l'alter ego (pas d'attaque Quickstrike : règle, elle ne vise qu'un héros) ;
  - Shadow of the Past met bien Countdown en jeu ; Duel of Wits glisse une carte de la main sous elle ; Cr'reee récupérée par « Forever Friends » (défausse, recherche, mélange) puis jouée au tour 1 dans 8 parties sur 8.
- **Anomalies :** aucune qui soit un défaut de carte. Observations sans conséquence :
  1. Le message « deck va être mélangé avec défausse » apparaît à CHAQUE mélange simple (`AfterDeckShuffle` reçoit toujours la défausse liée), même quand la défausse n'est PAS fusionnée (seul `ShuffleWithDiscardPile` fusionne). Trompeur à la lecture des journaux (faux soupçon sur A Questing), cosmétique.
  2. « Hildegarde est vaincue par Hildegarde » : l'attaquante est désignée source de ses propres dégâts consécutifs (moteur, pas la carte).
- **Non exercé par le pilote** (il joue ces cartes en RESSOURCE, jamais en carte) : Rally!, Hold the Line, Mighty Endurance, Leap into Action, Revelry in Asgard, Fated Clash, Gleipnir ; et, côté Ch'od, Mentor/Duel of Wits/Plutonia/Strike and Phase/Utter Contempt n'apparaissent que dans 1 partie sur 8. Ces cartes ne sont prouvées que par leurs cas de test.
