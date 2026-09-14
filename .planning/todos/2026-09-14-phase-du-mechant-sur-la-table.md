# La phase du méchant jouée SUR LA TABLE

**Demande de l'utilisateur, 14/09/2026**, après avoir vu une vidéo de
`play.marvelsimulator.com` et m'avoir envoyé cinq captures de leur phase du
méchant.

Ce qu'il a retenu, dans ses mots : « les cartes boost sortent vraiment du
paquet pour se mettre à côté, pour ensuite voir à combien ; idem pour la carte
d'activation, elle sort du paquet et elle s'affiche, et ça j'aime vraiment
bien ; j'aime bien aussi les traits qui montrent qui va être attaqué ».

Les trois gestes racontent la même chose : **on voit d'où ça vient et où ça
va**, au lieu de le lire dans un cartouche.

## ⚠ Ceci revient sur une décision prise, et l'utilisateur le sait

La spec `docs/superpowers/specs/2026-09-07-scene-phase-mechant-design.md`,
décidée avec lui après une vraie partie (Taskmaster contre Ant-Man), dit en
décision n°2 : « plus aucune carte n'est agrandie sur place dans la table,
**plus de trait**, plus de cartouche collé à la main ».

Le premier des trois défauts qui avaient motivé ce choix est le seul qui
compte encore ici : **la table est en avance sur le récit**. Le moteur envoie
un monde déjà à jour ; la scène centrale contourne le problème en portant ses
propres chiffres et en assombrissant la table.

Le point lui a été dit avant qu'il tranche. Il a choisi la table en
connaissance de cause.

## Ce qui est décidé

Cinq questions, une à la fois.

| Question | Décision |
|---|---|
| **Où tester** | **Serveur de développement seulement.** Rien en production tant qu'il n'a pas validé. |
| **Où jouer la phase** | **Sur la table**, comme eux. La scène centrale n'est pas utilisée dans ce mode. |
| **Rythme** | **Ça se déroule seul et vite, et ça s'arrête quand le joueur peut agir.** ⚠ RÉPONSE RÉVISÉE, voir ci-dessous. |
| **Étendue du trait** | **Tout ce qui va d'une carte à une autre** : activations du méchant et des sbires, attaques et manigances, et les effets des cartes rencontre. |
| **Remplacement** | **Un troisième mode, à côté** : « Détaillé / Sur la table / Instantané ». Rien de ce qui marche n'est touché, et ne pas le choisir suffit à revenir en arrière. |

## ⚠ Le rythme a été demandé DEUX FOIS, et la seconde réponse annule la première

Premier tour : « un clic par étape ». Puis, dans le message suivant :
« l'idée, c'est que ce soit assez clair sans forcément que ça prenne beaucoup
de temps », et il décrit un ENTRE-DEUX entre le mode Détaillé (« très clair »)
et le mode Instantané (« ça va très vite »).

Les deux ne tiennent pas ensemble : **le mode Détaillé a DÉJÀ un clic par
étape**. Un troisième mode au même rythme n'aurait pas été un entre-deux, juste
le même temps en plus joli. La contradiction lui a été montrée, et il a tranché
pour la troisième voie.

**Décision retenue** : ça se déroule tout seul et vite, SAUF quand le joueur a
une vraie décision à prendre (défendre, une interruption, un choix de cible) ;
là ça l'attend.

✅ **Vérifié avant de l'inscrire** : `DeroulePhase.tsx` distingue déjà les deux
sortes d'attente (`questionAuJoueur`, `attendUnAutreJoueur`, `enAttente`), et
son commentaire documente même un défaut passé où elles avaient été confondues
(« La suite arrive… » s'affichait par-dessus la question). La brique tourne,
elle est à réutiliser et non à écrire.

## Ce que la première enquête a établi

✅ **L'étendue la plus large est tenable sans toucher aux 6000 cartes.**
`FaitMechant` (`WorldStat.RecordFaitMechant`, côté Python) porte déjà
`auteur`, `cible` et le nombre en clair, et il voyage avec le monde. Le trait
se déduit donc des faits déjà émis. La limite, à dire au joueur : **ne sera
relié que ce que le moteur rapporte comme fait**. Un effet qui n'en émet pas
n'aura pas de trait, et se traitera au cas par cas.

⚠ **LE RISQUE N'EST PAS « FAIRE RECULER LA TABLE », IL EST PLUS ÉTROIT.**
Pour dessiner un trait et un montant, nul besoin de rembobiner la table : les
deux cartes y sont, à leur place. Le vrai problème est **les cartes qui ont
quitté la table pendant la phase** : sur les captures de l'utilisateur, Nick
Fury est présent à l'image 4 et absent à l'image 5. Un trait vers une carte
qui n'existe plus n'a nulle part où pointer.

Trois issues possibles, à trancher par la mesure et non par le raisonnement :
la remettre le temps de l'étape, ancrer le trait sur sa dernière position
connue, ou rejouer la phase depuis une photo du monde d'avant.

## ⚠ Prérequis : les animations

`2026-09-14-animations-molles.md`. L'utilisateur demande ici « un entre-deux
qui fasse plus jeu de cartes, où on voit vraiment les cartes bouger ». Des
cartes molles ruineraient tout l'effet : la durée de vol est FIXE (250 ms quelle
que soit la distance), donc rien ne pèse. À traiter avant ou en même temps, pas
après.

## Ce qu'on ne fait pas

- Aucune reprise de leur code ni de leurs images : ce sont des **principes
  d'affichage** qu'on reprend, pas une mise en œuvre.
- La scène centrale du mode Détaillé n'est ni retirée ni modifiée.

## Statut

Décisions prises le 14/09/2026, **non commencé**.

Première étape prévue : une **preuve de faisabilité** sur une seule activation
(le méchant attaque un héros), pour mesurer le cas « la cible a quitté la
table » avant de construire quoi que ce soit d'autre.
