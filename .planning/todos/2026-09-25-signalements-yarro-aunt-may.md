# Signalements 21 et 22 de Yarro (25/09/2026) : Aunt May & Uncle Ben

Lus en production le 25/09 au soir (lecture seule de `narwhal.db`).

**Ce que le joueur voit.** Rapport 21, en alter-ego : « Impossible d'utiliser
l'action de tante May et oncle Ben car le deck est vide (je suppose ?) ».
Rapport 22, une minute plus tard : « ça passe côté héros, donc ça ne doit pas
être dû au deck vide ». Même partie : SP//dr, Ultron, round 6.

**Cause.** Le coût de `31007` exigeait EXACTEMENT 2 cartes du deck (3 en
alter-ego). Mesure au harnais : l'Action n'est offerte que si le deck en
contient au moins autant. Le deck de Yarro en avait 2, d'où « héros oui,
alter-ego non ». Sa première intuition était la bonne.

**Règle.** Aucun ruling sur la carte. Rules Reference, entrée Empty Player
Deck : si le deck s'épuise pendant une défausse, on remélange la défausse,
on prend 1 carte rencontre, et rien n'est défaussé du nouveau deck.
Arbitrage utilisateur du 25/09/2026 : l'Action reste utilisable, on
défausse ce qui reste.

**Correctif.** `src/cards/pack/spdr/spdr/31007.py` : nombre défaussé plafonné
à la taille du deck. Le remélange et la carte rencontre viennent de la règle
générique du moteur (`process_after_shuffle`, player.py). 4 cas neufs dans
`tools/test_capacites.py` (deck court dans les deux formes, deck de 5 dans
les deux formes), 7/7 cas SP//dr verts, substitution 4/4 rouges.

**Reste.** Non déployé. Répondre à Yarro depuis l'admin et passer les deux
rapports en « Traité » après déploiement.

## Extension à toutes les cartes (25/09/2026, remarque de l'utilisateur)

Le premier correctif ne touchait que 31007 : erreur, il fallait recenser le
mécanisme avant de corriger. Recensement :

- **Pioche** : non concernée. `DrawCards` continue après le remélange
  (`continue_after_shuffle=True`), conforme au Rules Reference.
- **Effets qui défaussent le dessus du deck** (116 appels) : déjà conformes,
  la défausse s'arrête au remélange. il021/il022 testent le nombre défaussé
  parce que leur texte l'exige.
- **Coûts `CostFunc.DiscardDeckTopCards("YourDeck", N)`** (25 cartes, dont
  gb011-gb014, nv002, nv003, 04164, 21038-21061, 40038-40160...) : BUG. Le
  coût était déclaré impayé si le deck avait moins de N cartes, alors que
  les cartes étaient déjà défaussées. Corrigé dans
  `src/game/ability/cost_func.py` : le coût est payé quand la défausse
  s'arrête parce que le deck s'est vidé. Cas neufs gb012 (1 carte et 5
  cartes), rouge prouvé avec l'ancien moteur.
- **Coûts `CostFunc.Discard("YourPlayerDeckTop")`** : 44056 et 16052 ne
  défaussent qu'1 carte (jamais plus que le deck), 31007 corrigée à part.
- **Deck rencontre** (51015, 53002, 53010) : non modifié. La règle citée ne
  vaut que pour le deck joueur.

## Déployé (nuit du 25 au 26/09/2026)

Batterie complète : 2475/2479. Les 4 rouges (sg006, sg007, sg009, sg013)
sont connus depuis le 31/08 (`2026-08-31-cas-rouges-sg-ss.md`), messages
identiques, et restent rouges à l'identique avec l'ancien `cost_func.py`.
Aucune table allumée au moment du déploiement. Site HTTP 200.

## Signalement n°29 de Yarro (30/09/2026) : T'Challa (51002) sans « Black Panther »

**Ce que le joueur voit.** « L'allié T'Challa n'active pas la special ability
Black Panther lorsqu'il utilise un pouvoir de base. » Journal joint : Shuri en
ALTER-EGO (`51001b`), Kimoyo Beads en jeu, T'Challa contre 2 menaces, aucun
Special.

**Cause.** Pas de défaut : la carte est imprimée « Hero Response » et le moteur
réserve tout type Hero à la forme héros (`ability.py`, `player_is_hero`).
Shuri était en alter-ego.

**Preuve.** 2 cas neufs dans `tools/test_capacites.py` (`51002 T'Challa`) :
forme héros, 5 -> 2 menaces (thwart + Kimoyo) ; alter-ego, 5 -> 3. 2/2 verts.

**Reste.** Répondre à Yarro depuis l'admin puis passer le rapport en « Traité »
(rien n'est écrit en prod à ce jour). Non commité.

## Signalement n°30 de Yarro (30/09/2026) : ordre de défausse des cartes payées

**Ce que le joueur demande.** Pouvoir choisir dans quel ordre les cartes payées
partent à la défausse, parce que Neena Thurman (40037b) échange une carte de la
main avec le DESSUS de la défausse : la dernière carte défaussée compte.

**Cause.** Pas de défaut. Le moteur défausse déjà les cartes payées dans
l'ordre des clics (`basculerRessource` -> `resources` -> `SpendResource` ->
`DiscardResourcesArea`), la dernière est au-dessus. Ce n'était juste écrit nulle
part.

**Décision (option B, choisie par l'utilisateur).** On garde l'ordre des clics,
sans clic en plus, et on le rend visible : `World.DiscardResourcesArea` écrit
une ligne au journal dès 2 cartes défaussées
(`Message.AfterCardsPaidOrder_Text`, traduite dans `translate_fr.json`).

**Preuve.** `tools/test_capacites.py` : 2 cas d'ordre (Wolfsbane 40051 payée
Genius puis Pip, et l'inverse, `defausse_dessus` vérifié), 1 cas journal (la
ligne existe à 2 cartes), 1 témoin (absente à 1 carte). 4/4 verts. Le harnais
respecte maintenant l'ordre de `payer_avec` (résolution carte par carte).

**Reste.** Répondre à Yarro et passer n°29 et n°30 en « Traité » sur le go de
l'utilisateur. Non commité, non déployé.

## Signalements n°31 et n°32 de Phocéa (30/09/2026)

**n°32, Gamora refusée au deck-builder : CORRIGÉ, pas déployé.** Cause :
`deck/starter/gamora.json` ne déclarait aucun `hors_aspect`, alors que
Skilled Tactician (18001b) autorise 6 événements attaque/menace d'autres
aspects. Ajouté (`types: ["Event"]`, traits ATTACK/THWART). Preuve : 4 tests
neufs dans `tools/tests-lanceur/regles-aspect.test.mjs` (6 légaux, 7e refusé,
allié ATTACK et événement sans trait refusés, même deck chez Spider-Man
refusé), 65/65 sur tout le dossier.

**n°31, The Power of Leadership non doublé sur Ant-Man (coût 0) : DIAGNOSTIQUÉ,
non corrigé (utilisateur : « n°32 seulement »).** Cause :
`src/game/ability/factory/resources.py:50`, condition `res.val <= message.cost.val`
qui écarte le doublement quand la carte payée coûte 0 (Ant-Man 12011 lit
`message.overpaid`). Correctif = moteur partagé : cas Ant-Man + 01072 au
harnais, puis batterie des cartes concernées (PROCESSUS-CARTE §6bis).

État en prod le 30/09/2026 : n°29 à n°32 tous « traité » (classés depuis
`/admin`). Le correctif n°30 (ordre de défausse dans le journal) et le n°32
(Gamora) ne sont PAS en ligne : déploiement plus tard, sur le « déploie » de
l'utilisateur. Le n°31 n'est pas un bug (Rules Reference, entrée « Cost » :
le surpaiement n'est pas du paiement) ; cas de harnais Ant-Man + 01072 écrit
mais pas encore vert (Peter Parker ajoute 1 ressource, mise en place en forme
héros à finir). Textes de réponse rédigés le 30/09, à envoyer par l'utilisateur.
