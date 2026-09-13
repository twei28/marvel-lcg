# Muse (Rainy) : relevé des cartes, image par image

**Archive** `Muse-20260902T074120Z-1-001.zip`, 7 fichiers, extraite dans
`/tmp/muse/Muse/`. Numérotation imprimée : **MUSE (n/7)**. Auteur **Rainy**,
mention « MC Custom Content By: Rainy » au pied de chaque carte.

**Ce n'est pas un héros ni un vilain : c'est un SET MODULAIRE**, celui qu'on
ajoute à n'importe quel scénario. Modèle du dépôt : `necroverse` (BLUEHG, 8
cartes) et `intergalactic_hazards`. Il lui faut donc un
`data/encounter_sets/muse.json`, une entrée `encounters` dans `sets_info.json`,
et aucun deck de départ.

## Les sept cartes

| Fichier | N° | Carte | Type | Chiffres | Texte |
|---|---|---|---|---|---|
| `1 Art Imitates Death.jpg` | 1/7 | **Art Imitates Death** | Manigance annexe | 2 menaces par héros, 2 icônes de boost | **Une fois révélée** : défaussez les 3 cartes du dessus du deck de chaque joueur. Pour chaque carte défaussée ainsi, infligez 1 dégât à chaque personnage dont l'image était sur cette carte. |
| `2 Supply Run.jpg` | 2/7 | **Supply Run** | Manigance annexe | 3 menaces par héros, 2 icônes | **Interruption forcée** : quand un ennemi unique (★) s'active, défaussez la carte du dessus du deck rencontre. Si elle porte une image de cet ennemi, donnez-la lui en carte de boost face cachée. |
| `3 Muse.jpg` | 3/7 | **★ Muse** | Sbire | 8 PV, CTR 2, ATQ 2, 3 icônes. ARTIST. CRIMINAL. ELITE. | Ténacité. **Interruption forcée** : quand un joueur joue une carte qui porte l'image de son identité, Muse s'active contre ce joueur. |
| `4 Graffitied Streets.jpg` | 4/7 | **Graffitied Streets** | Environnement | Réserve (3 compteurs graffiti par héros), 1 icône. LOCATION. | **Interruption forcée** : quand vous jouez une carte qui porte l'image de votre identité, placez 1 menace sur la manigance principale. — **Action** : inclinez un personnage que vous contrôlez → retirez d'ici autant de compteurs graffiti que son CTR. (Limite une fois par round et par joueur.) |
| `5 Grim Inspiration.jpg` | 5/7 | **Grim Inspiration** | Traîtrise | Déferlement, 1 icône | **Une fois révélée** : chaque joueur choisit une carte signature de sa pile de défausse et la place sur le dessus de son deck. Donnez à Muse et au vilain une carte de boost face cachée. |
| `6 Obsession.jpg` | 6/7 | **Obsession** | Traîtrise | boost ÉTOILE | **Une fois révélée** : Muse s'active contre vous. S'il n'est pas en jeu, cherchez Muse et mettez-le en jeu engagé avec vous. — ★ **Boost** : cette carte gagne +X icônes de boost, X étant le nombre de cartes de votre main qui portent l'image de votre identité. |
| `7 Obsession.jpg` | 7/7 | **Obsession** | Traîtrise | — | **Second exemplaire**, comparé au pixel sur sa zone de règles : identique à 6/7, seul le numéro de collection change. |

Six cartes distinctes, sept exemplaires.

## L'arbitrage central : « l'image de votre identité »

**Quatre cartes sur six** le disent (1/7, 3/7, 4/7, 6/7), et le moteur ne sait
rien de ce que montre une illustration.

**Décision utilisateur du 13/09/2026** : ce sont les **cartes signature**, celles
que le moteur marque `card_class="IdentitySpecific"`. C'est le vocabulaire de
l'auteur lui-même, qui écrit noir sur blanc « an identity-specific card » sur
Grim Inspiration (5/7).

Les deux autres lectures ont été écartées : « les cartes qui portent ton nom »
attraperait des alliés homonymes d'un autre aspect, imprévisible pour le
joueur ; « vraiment l'illustration » demanderait de relever à l'œil ce que
montrent des milliers d'images, une liste fausse dès le premier oubli.

## Deux arbitrages qui en découlent

**Art Imitates Death (1/7)** : « chaque personnage dont l'image était sur cette
carte ». Une carte signature ne montre pas toujours le héros — Nova Prime montre
Nova Prime. **Décision utilisateur** : c'est le **héros dont c'est le deck** qui
encaisse, quoi que montre la carte. Simple à anticiper, jusqu'à 3 dégâts par
joueur, et c'est ce que raconte l'illustration : Muse peint le héros sur son mur.

**Supply Run (2/7)** : « si elle porte une image de cet ennemi ». Même problème,
côté ennemi. **Décision utilisateur** : une carte rencontre **du même set que
l'ennemi** (une carte Muse pour Muse, une carte Rhino pour Rhino). Le vilain se
renforce de ses propres cartes, ce que dit l'illustration, et cela se prévoit.

## Points d'attention déjà visibles

- **Ténacité** sur un sbire : mot-clé officiel, `desc.Toughness`, aucun script
  (voir `62001a` Luke Cage et `04092`).
- **« Uses (3 par héros) »** sur un ENVIRONNEMENT : la réserve de compteurs se
  déclare dans `desc`, mais la valeur par héros doit être vérifiée contre une
  carte officielle qui en fait autant.
- **Deux interruptions forcées sur le même déclencheur** (3/7 et 4/7) : jouer
  une carte signature. Si les deux sont en jeu, la carte jouée réveille Muse ET
  pose 1 menace. C'est cumulatif, rien ne l'interdit.
- **« Muse s'active contre vous »** (6/7) et « contre ce joueur » (3/7) : une
  activation d'ennemi hors de la phase du méchant, mécanisme que le moteur
  connaît (`Puzzle.Attack` côté harnais, `DoAttacks`/`DoSchemes` côté carte).
- **Obsession cherche Muse et le met en jeu** : le sbire peut donc arriver sans
  passer par le deck de rencontre, y compris depuis la défausse.
- **Boost ÉTOILE** sur Obsession : aucune valeur `Boost` dans `desc`, une
  capacité `WhenCardBecomeBoost` à la place (vérifié contre `01144a`).

## Décompte

| Bloc | Cartes |
|---|---|
| Manigances annexes | 2 |
| Sbire | 1 |
| Environnement | 1 |
| Traîtrises | 2 distinctes, 3 exemplaires |
| **Total** | **6 distinctes, 7 exemplaires** |
