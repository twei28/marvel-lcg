# Trois signalements du 20/09/2026

> **Mise à jour du 07/10/2026 (audit du backlog)** : La mention « rien n'est déployé » est PÉRIMÉE (déploiements du 25/09 et suivants). A, B, D corrigés avec preuve par substitution.

Lus en production le 20/09 au soir (`rapports` 18, 19, 20). Aucun n'est traité.
Les deux d'Aghenatak sont **le même défaut**, pas deux.

---

## A. Deux cartes restent coincées « en résolution » (n°19 et n°20)

**Ce que le joueur voit.** « Squirrel Girl a été jouée comme un support.
Impossible de l'activer d'aucune manière, ni de la défausser. » Puis :
« Piecing all together a été joué comme un support. Impossible de le contrer. »

**Ce que dit le journal, et c'est net.** Les deux rapports viennent de la MÊME
partie (Jessica Jones contre Dark Beast's Bogus Journey, round 13,
`render_id` 1845), et portent tous deux le même état de table :

```
c16 Piecing It All Together (61007, PlayerSideScheme, en résolution)
c41 Squirrel Girl           (61017, Ally,             en résolution)
```

« En résolution » est la **zone de traitement** du moteur
(`world.area_processing`), celle où une carte transite pendant qu'elle se
résout. Les deux y sont restées. C'est pour ça que rien ne marche sur elles :
elles ne sont ni en jeu, ni en défausse, elles sont en transit. Le joueur les
voit posées sur la table et les prend pour des soutiens, ce qui est une lecture
raisonnable de ce qu'il a sous les yeux.

**Ce n'est donc pas deux bugs de carte, c'est un bug de séquence de jeu**, et
les deux cartes appartiennent au paquet Jessica Jones (61xxx), le héros joué.

**Piste, à vérifier.** `PlayAnAlly` et `PlayACard`
(`src/game/player/action/player_action.py:811` et `:847`) font, dans le cas
« mise en jeu GRATUITE » :

```python
Faces.MoveAllToProcessingArea([ally], effect)
return ally.Play(player, effect, message, Resources("0"), from_area, False)
```

Si `Play` n'aboutit pas, **rien ne ramène la carte**. Elle reste où le premier
appel l'a mise. Ce chemin est celui d'une carte mise en jeu par l'effet d'une
autre, pas d'une carte jouée depuis la main en payant son coût.

**Ce qui manque pour conclure.** Le journal du rapport ne remonte pas jusqu'au
round où les deux cartes sont entrées : la fenêtre retenue commence au round 4
et le seul événement conservé est `R6 {c41} Squirrel Girl défaussé / P1`, qui
est probablement une tentative de défausse restée sans effet, pas sa mise en
jeu. Il faut reproduire : Jessica Jones, et une mise en jeu gratuite de chacune
des deux cartes.

**Aucune exception côté serveur** (`journalctl` du 20/09 à partir de 15 h :
zéro `Traceback`). Le moteur n'a pas planté, la séquence s'est arrêtée
proprement au mauvais endroit.

⚠ Le paquet `jj` n'a **aucun fichier de test** dans `tools/`.

---

## B. SP//dr : payer avec la capacité avant la main fait PERDRE la carte (n°18)

**Yarro, et sa description est exemplaire** : elle contient le défaut ET le
contournement.

> « Quand tu veux payer le coût pour jouer une carte, tu peux incliner une
> interface pour générer une ressource. Cela fonctionne mais il faut respecter
> un ordre précis si tu as un mix entre payer de ta main et payer avec la capa
> d'SP//dr. En gros si tu fais un mix et que tu choisis d'abord de payer par la
> capa, et que par exemple pour une carte qui coûte 2 tu n'inclines qu'une
> interface, il va te l'incliner et mettre la carte que tu veux en défausse.
> Pour jouer la carte il faut d'abord payer une carte de ta main et ensuite
> déclencher la capa. »

**Ce que ça veut dire.** Un paiement incomplet n'est pas annulé : la ressource
est consommée (l'interface reste inclinée) ET la carte part à la défausse sans
avoir été jouée. Le joueur perd la carte et la ressource.

**Pourquoi c'est sérieux.** Ce n'est pas un défaut d'affichage ni une gêne :
c'est une **perte sèche de matériel** au milieu d'un tour, sur un ordre de
clics que rien n'interdit à l'écran. Et le contournement n'est devinable par
personne.

Journal du rapport : 308 lignes, héros SP//dr Suit, les lignes 54 à 61 montrent
bien l'alternance `gains resource` / `exhausted` pendant un paiement.

---

## C. Ce qu'il reste à faire

1. Reproduire A avec Jessica Jones, sur les deux cartes, et trouver pourquoi
   `Play` n'aboutit pas. Écrire le cas qui manque.
2. Reproduire B : jouer une carte à coût 2 en inclinant l'interface AVANT de
   défausser une carte de la main. Vérifier qu'un paiement incomplet rend la
   ressource et ne défausse rien.
3. Répondre aux deux joueurs. Yarro attend depuis le 19/09 au soir sur un
   autre sujet (Echo), et depuis le 20/09 à 13 h 34 sur celui-ci.

---

## B : CORRIGÉ le 21/09/2026

Commits `ab0b6e7e`, `d4d1fc43`, `7a26226b`. Rapport complet dans
`.planning/rapports/2026-09-20-spdr-paiement-incomplet.md`.

**Le défaut n'était pas dans SP//dr, il était dans le moteur.**
`EffectChecker.check_pay` dépensait tout PUIS constatait le manque, et
`PlayerAction.ResolveEffect` défaussait la carte. Toute carte qui laisse
choisir combien on paie tombait dedans.

**Ce qui le prouve, et c'est le plus parlant :** trois témoins d'extensions
sans rapport entre elles gravaient ce défaut comme si c'était la règle, et sont
passés au ROUGE dès la réparation. `sd011` (Speed), `ar010` (Ares), `bl002`
(Blade), ce dernier attendant « main vide alors que la seule carte de la main
n'a pas pu être jouée », ce qui n'est défendable sous aucune lecture des
règles. La revue a vérifié les trois un par un : aucun n'a été affaibli, deux
documentaient explicitement le défaut dans leur commentaire.

**Le correctif** rend le paiement atomique : le réservoir est testé avant le
point de non-retour, et ce qui a été engagé est rendu.

⚠ **Deux limites, dites et non cachées :**
1. Le rendu sait défaire une carte inclinée et un déplacement de zone. Il ne
   sait PAS défaire un jeton retiré, un compteur posé, ni les effets déjà
   déclenchés par la fenêtre `WhenCardBeSpendAsResource` (18 fichiers) ou par
   l'`ex_operation` du payeur (11 cartes recensées). Ceux-là sont journalisés
   quand c'est un coût, muets quand c'est un effet. Un rendu partiel reste
   préférable à la perte sèche : le joueur récupère sa carte, qui est le
   matériel rare.
2. L'écran laisse toujours choisir « une interface » pour un coût de deux sans
   rien dire. Le paiement est maintenant refusé proprement au lieu de coûter la
   carte, mais **prévenir le joueur reste à faire côté plateau**.

**Première ronde de revue : le correctif ne couvrait qu'une carte sur 107.**
Il ne balayait que `paying_effect.cost_func`, alors que 106 cartes portent leur
coût d'inclinaison sur `cost_check_effect.cost_func` — dont `50044` Fury's
Watch, la carte officielle que le rapport donnait en preuve de généricité.
Élargi à l'union des deux, avec un témoin `50044` qui mord.

**Seconde ronde : ce témoin pouvait passer au vert sans rien mesurer.** Son
attendu décrivait un état « rien ne s'est passé ». Il exige désormais que le
jeton retiré soit tombé à 1 — c'est-à-dire que la LIMITE connue du correctif
garde le témoin du correctif. Vérifié dans les deux sens.

## A : CORRIGÉ le 21/09/2026

Commit `54462b83`. Rapport complet dans
`.planning/rapports/2026-09-21-cartes-coincees-en-resolution.md`.

**La piste `PlayAnAlly` / `PlayACard` n'était pas la bonne, et le défaut est
plus large qu'elle.** Ce n'est pas la mise en jeu qui échoue : c'est la
**recherche** qui ne se referme jamais. `Search.SearchForCards` SORT la carte
trouvée du deck et la pose dans la zone de traitement pour la montrer au
joueur ; à charge ensuite de l'opération appelante de la consommer. Quand elle
ne le fait pas, rien ne ramenait la carte.

Les deux cartes du signalement sont les deux proies de ce trou dans le paquet
Jessica Jones : `61008` Calling in Favors sort un ALLIÉ du deck (d'où Squirrel
Girl) puis demande « veux-tu le jouer ? » ; `61019` Strategy Session sort une
MANIGANCE ANNEXE (d'où Piecing It All Together) puis demande « veux-tu la
prendre ? ». Les deux laissent le droit de refuser, et refuser laissait la
carte posée sur la table pour le reste de la partie.

**Générique**, et une troisième carte le prouve dans un pack sans rapport :
`62022` Dynamic Duo (Luke Cage) cherche sans filtre puis ne garde que les
Team-Up ; toute autre carte tirée restait coincée. 223 fichiers de cartes
appellent `Search.*`.

**Le correctif** referme le sas tout seul : ce que personne n'a réclamé à la
fin de la résolution rentre dans son deck, qui est remélangé.

⚠ **Deux limites, dites et non cachées :**
1. Une carte cherchée, CHOISIE, mais qu'on n'arrive pas à payer est toujours
   **défaussée** au lieu de retourner au deck (`PlayCardsLikeInTurn`). C'est un
   second défaut, plus petit, de la même famille que celui de Yarro ; il n'est
   pas traité et aucun témoin ne le couvre.
2. L'écran ne dit rien au joueur qui refuse : la carte disparaît de la table
   sans un mot. Une ligne « la carte cherchée retourne dans votre deck » reste
   à faire côté plateau.

---

## D. À ÉCRIRE : une carte cherchée mais impayable finit à la DÉFAUSSE

Trouvé en corrigeant A, **pas traité**, et le relecteur suit l'analyse.

Quand une recherche sort une carte du deck et que le joueur **accepte** de la
jouer mais n'arrive pas à en payer le coût, `PlayCardsLikeInTurn`
(`src/game/player/action/player_action.py`, `if not played and
if_not_play_discard_it`) la **défausse**. Le chemin jumeau
`PlayOneCardLikeInTurn` fait pareil.

Le sas de recherche ne voit rien : la carte n'est plus dans la zone de
traitement, elle est dans la défausse. Le filet du 21/09 ne mord donc pas.

**Pourquoi c'est un défaut.** Aucune lecture des règles ne soutient qu'une
carte sortie d'un DECK par une recherche, et qu'on n'a pas réussi à jouer,
parte à la défausse. Elle doit retourner au deck, qui est remélangé. C'est la
même famille que le signalement B de Yarro (« un paiement incomplet ne doit
rien coûter »), un cran plus loin.

**Ce qu'il faut.** Un témoin dans `tools/test_capacites.py` : `61008` Calling
in Favors, recherche ACCEPTÉE sur un allié trop cher pour la main du moment
(la réduction de 2 ne suffisant pas), attendu `dans_deck_joueur: [<allié>]` et
`aucune_en_resolution: True`. Rouge aujourd'hui, l'allié finissant en défausse.
Aucun témoin ne couvre ce cas.

⚠ Ne pas le traiter en même temps que A : c'est le chemin « jouer », pas le
chemin « chercher », et il touche deux méthodes partagées par tout le moteur.

## D : CORRIGÉ le 25/09/2026

`PlayCardsLikeInTurn` (`player_action.py`) consulte désormais le MÊME sas de
recherche que `CloseSearchTransit` (`by_effect.context.search_transit`) au
moment précis où il défausserait la carte impayable. Si cette carte y a une
entrée (elle vient d'une recherche encore ouverte sur ce `by_effect`), elle
retourne à son deck d'origine et est remélangée au lieu d'être défaussée ;
sinon (main ordinaire, chemin A/B d'Echo…) le comportement historique — la
défausser — ne change pas.

Témoin ajouté, exactement comme prévu ci-dessus : `61008` Calling in Favors,
Luke Cage (61003, coût 3, réduit à 1) recherché et accepté, main sans aucune
ressource ET identité alter-ego épuisée (sinon le coût réduit à 1 se payait
quand même avec la ressource gratuite du tour). `main_exclusive: []` ne vide
RIEN — `if cas.get("main_exclusive")` est un test de vérité Python, une
liste vide y est fausse — piège trouvé en écrivant ce cas, noté dans le
commentaire du cas pour ne pas le refaire.

Preuve par substitution faite (rouge sans le correctif : Luke Cage disparaît,
ni en jeu ni dans le deck — perdu en défausse ; vert avec). Non-régression :
les 9 autres cas de recherche existants (61008/61019/01095), les 18 cas Echo,
le cas Daredevil du 25/09, et Dynamic Duo (62022) — tous verts. Construction
des 5778 cartes du jeu : 0 erreur (fonction moteur partagée). Autoplay :
8 parties Jessica Jones contre Rhino, 0 traceback, 2/8 bloquées (mieux que le
témoin `spider_man`, 3/8, mesuré la même session).

---

## Reste ouvert

- ~~Répondre aux deux joueurs~~ réglé par l'utilisateur (25/09/2026).
- **Rien n'est déployé** : les correctifs (A, B, D, Echo, Daredevil) sont sur
  le disque, pas mis en prod.
