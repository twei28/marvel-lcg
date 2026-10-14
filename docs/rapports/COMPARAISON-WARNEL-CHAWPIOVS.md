# Comparaison avec Warnel Chawpiovs

Audit initial du 05/10/2026 entre :

- NarwhalChampions / moteur Python de ce dépôt ;
- `frwololo/warnel-chawpiovs`, commit `79b9dc1` du 05/10/2026.

## Ce que cette comparaison peut prouver

Les deux moteurs ne décrivent pas les effets de la même manière. Narwhal utilise
un module Python par identifiant de carte ; Warnel emploie des dictionnaires JSON
indexés surtout par nom et interprétés par Godot. Une égalité textuelle entre les
deux sources n'aurait donc aucun sens.

L'audit commence par les aveux explicites du code Warnel (`TODO`), puis vérifie
si la clause correspondante existe dans le module Narwhal. Cela prouve une
différence d'implémentation. Un test comportemental exécutant le même scénario
dans les deux moteurs reste nécessaire pour prouver tout le déroulé à l'écran.

## Couverture rapprochée

- 6 409 entrées de cartes dans `data/cards.json` côté Narwhal, contenu fan-made
  et faces techniques compris ;
- 2 715 entrées scriptées dans les `SetScripts_*.json` de Warnel ;
- 1 907 entrées Warnel rapprochées automatiquement d'une carte Narwhal ;
- 1 792 identifiants Narwhal distincts concernés par ce premier rapprochement.

Le rapprochement automatique est conservateur : 134 correspondances viennent
d'un identifiant explicite Warnel, 1 773 d'un nom unique. Les homonymes, les
sous-titres et les stades de vilain non résolus sont laissés hors résultat plutôt
que rapprochés au hasard.

## Les marqueurs TODO de Warnel

Les scripts Warnel contiennent 172 cartes portant une clé `TODO` :

| Catégorie | Nombre |
|---|---:|
| Effet de campagne non pris en charge | 153 |
| TODO sans explication | 12 |
| Limitation précise nommée par l'auteur | 7 |

Les 153 effets de campagne ne constituent pas 153 erreurs isolées : ils découlent
de l'absence assumée du mode campagne dans Warnel. Narwhal prend les huit
campagnes en charge.

## Sept divergences explicites

### Intelligence — `50051`

Warnel note `TODO: swap`. Son script montre les cartes Rencontre distribuées et
le sommet du deck, mais ne les échange pas. Narwhal appelle
`initiator.SwapTheseCards(faces, effect)` après les avoir montrées.

**Verdict statique : divergence certaine.**

### Iron Man — Tony Stark — `09039`

Warnel note que la réduction devrait fonctionner seulement quand l'amélioration
cible Iron Man. Son altération filtre le type `upgrade`, sans filtre de cible.
Narwhal exige `[effect.this] == message.for_targets` avant de réduire le coût.

**Verdict statique : divergence certaine et potentiellement avantageuse à tort
dans Warnel.**

### Directed Force — `41019`

Warnel note `max 1 per attack` mais son script ne porte pas cette limite. Narwhal
termine la capacité par `LimitOncePerEvent()`.

**Verdict statique : divergence certaine ; Warnel peut proposer plusieurs
exemplaires sur la même attaque.**

### Maximum Velocity — `14005`

Warnel note `max 1 per phase` sans coder cette limite. Narwhal applique
`.MaxOnePerPhase()`.

**Verdict statique : divergence certaine ; Warnel peut laisser jouer plusieurs
exemplaires pendant la même phase.**

### Across the Spider-Verse — `27018`

Warnel note `dual player`. Son script s'arrête après avoir épuisé un Web-Warrior
et mis un allié en jeu. Il ne contient pas la seconde partie : choisir un joueur,
payer trois ressources et répéter l'effet. Narwhal construit ce choix et rappelle
la même capacité après paiement.

**Verdict statique : divergence certaine, surtout visible à plusieurs joueurs.**

### Ionic Boots — `27148`

Warnel note `damage to my identity`. Son interruption filtre les dégâts d'une
attaque, mais pas explicitement l'identité du joueur qui contrôle la carte.
Narwhal écoute `AttachedVillain` attaquant et blessant `YourIdentity`.

**Verdict statique : divergence très probable ; le TODO de l'auteur confirme
que son filtre est trop large.**

### Loose Ends — `27135`

Warnel note `discard 1 if change form`. Son script cherche et révèle une
obligation, mais ne défausse pas la carte aléatoire si le joueur passe en alter
ego. Sa liste de zones ne contient pas non plus la zone « retirée de la partie ».
Narwhal enregistre temporairement le changement de forme, défausse une carte
aléatoire, recherche aussi `include_removed_area=True`, puis retire l'écouteur.

**Verdict statique : deux divergences certaines.**

## Douze TODO sans explication

Neuf concernent les preuves du conseil exécutif d'Agents of S.H.I.E.L.D. :
`Authority`, `Blackmail`, `Ideology`, `Medical Records`, `Money`, `Security
Clearance`, `Security Scanner`, `Travel` et `Wiretap`. Leur entrée Warnel ne
contient que `{"TODO": ""}` : aucun effet de mise en place n'est codé. Narwhal
les branche sur `EvidenceOpportunity(...)` et possède des épreuves dédiées dans
`tools/test_preuves_aos.py` et `tools/test_accusation_aos.py`.

Les trois autres sont `Psi-Flail Strike`, `Training Regimen` et `Powerful
Enchantments`. Contrairement aux neuf précédentes, leur script Warnel contient
un effet qui ressemble au texte imprimé. Le TODO vide ne suffit pas à annoncer
une divergence : elles doivent être testées dans les deux moteurs.

## Différences globales qui modifient certaines cartes

Warnel annonce volontairement deux écarts aux règles :

1. les héros peuvent jouer leurs tours en parallèle en multijoueur ;
2. les sbires attaquent dans leur ordre d'arrivée au lieu de laisser le joueur
   choisir leur ordre.

Ces écarts ne se rattachent pas à une seule carte. Ils peuvent néanmoins changer
le résultat des réponses, interruptions, défaites de sbires, limites par phase et
effets dépendant de l'ordre d'activation.

Son moteur porte également plusieurs limites génériques explicites dans les
commentaires, notamment un code qualifié de « very flaky » pour jouer une carte
pendant une fenêtre d'interruption et un TODO sur le remélange du deck Rencontre
vide lors de la pioche d'une carte de boost. Ce sont des pistes de tests croisés,
pas encore des divergences de cartes prouvées.

## Prochaine passe utile

L'étape suivante doit transformer chaque divergence candidate en mini-scénario
commun : même carte, même état initial, même choix, puis comparaison de l'état
final. L'ordre recommandé est :

1. les sept divergences explicites ci-dessus ;
2. les trois TODO vides mais scriptés ;
3. les cartes touchées par l'ordre des sbires ;
4. les cartes jouées dans une fenêtre d'interruption ;
5. les effets déclenchés quand le deck Rencontre se vide.

Cette méthode évite de déclarer une carte différente uniquement parce que deux
moteurs expriment la même règle avec des structures différentes.
