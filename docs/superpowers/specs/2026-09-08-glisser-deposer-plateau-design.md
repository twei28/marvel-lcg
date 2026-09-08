# Glisser-déposer sur le plateau : conception

Spec du 08/09/2026, écrite après arbitrage question par question avec
l'utilisateur. Concerne `ui-app`, le plateau React.

**But** : pouvoir jouer à la souris comme on jouerait avec de vraies cartes.
On prend le héros, on le pose sur Rhino, il attaque. On prend un événement de
la main, on le pose sur la manigance, il se joue. Le clic actuel ne bouge pas
d'un pouce : le glisser s'ajoute, il ne remplace rien.

---

## 1. Les gestes retenus

| Ce qu'on prend | Ce qu'on vise | Ce qui se passe |
|---|---|---|
| Le héros | un ennemi | il l'attaque |
| Le héros | une manigance | il la contre |
| Le héros | l'ennemi qui l'attaque | il se défend |
| Un allié | un ennemi, une manigance | il attaque, il contre |
| Une carte de la main | sa cible imprimée | elle se joue sur elle |
| Une carte de la main | la zone qui lui revient | elle se joue sans cible |
| Une carte de la main | la carte qu'on est en train de payer | elle sert de ressource |
| Une carte de la main, au mulligan | la défausse | elle est écartée |
| Une amélioration ou un allié déjà en jeu | la cible de sa capacité | la capacité se déclenche |

**Écarté par l'utilisateur** : glisser un allié sur l'ennemi qui attaque pour
qu'il défende à la place du héros. Le geste existe dans les règles, il n'est
pas demandé ici. Le clic continue de l'offrir.

---

## 2. Ce que le plateau fait déjà, et qui sert de fondation

Relevé le 08/09/2026 sur l'état du code. **Aucun glisser-déposer n'existe
aujourd'hui** : tout passe par clic, menu, clic sur la cible.

Ce qui est déjà là et qu'on réutilise tel quel :

- **Le moteur dit les cibles légales.** Chaque option qu'il propose porte
  `all_legal_targets`, la liste des cartes qu'elle peut viser, et
  `target_num_range`, combien il en faut (`src/board/ask.ts`, type `Option`).
  Le glisser n'a donc rien à deviner : il lit.
- **Une carte porte son identité dans le DOM.** `ScanCard` rend un
  `<article data-card-id="...">`, le même attribut sur le rendu ordinateur et
  sur le rendu mobile. C'est à la fois la poignée du glisser et la zone
  d'atterrissage, sans toucher au composant.
- **Le conteneur sait déjà retrouver la carte sous le pointeur.** `Board`
  écoute `onPointerUp` sur le cadre du plateau et remonte au
  `closest('.scan-card')`. Le glisser se greffe au même endroit, avec
  `pointerdown` et `pointermove` en plus.
- **Lancer une action avec sa cible déjà remplie est une fonction existante.**
  `choisirOption(option, ciblesInitiales)` dans `src/board/interaction.ts`.
  C'est exactement ce que fait aujourd'hui le clic sur une cible quand une
  seule action la vise. Un lâcher, c'est le même appel.
- **La surbrillance des cibles valides est écrite.** `idsPulsePourOption` et
  `ajouterPulse` dans `src/board.tsx`, plus les classes CSS
  `state-targetable` et `is-target-pulse` de `ScanCard.css`. Le retour visuel
  du glisser est donc gratuit à 80 %.
- **Les rectangles à l'écran se calculent déjà.** `boitesDesCartes` dans
  `src/board/placement/boites.ts` rend la position de n'importe quel jeu de
  cartes, l'échelle de la scène comprise. Sert au test de survol et au tracé
  du trait.
- **Les zones du plateau sont nommées.** `construirePlateau`
  (`src/board/zones.ts`) produit douze emplacements : `rencontre`,
  `complot-principal`, `complots-secondaires`, `terrain-combat`,
  `terrain-soutien`, `reserve`, `main`, `nemesis`, `deck-special`,
  `piles-joueur`, `piles-rencontre`, `annexes`. Ce sont les zones
  d'atterrissage du point 5.
- **Un hook de geste sert de modèle.** `useAppuiLong`
  (`src/board/mobile/useAppuiLong.ts`) montre la forme attendue : une réf, un
  seuil, et un `vientDeDeclencher()` qui neutralise le clic qui suivrait.

---

## 3. Le geste, temps par temps

1. **Appui** sur une carte agissante. Rien ne bouge encore. On mémorise le
   point de départ et on capture le pointeur.
2. **Déplacement.** Tant qu'on reste sous un seuil de quelques pixels, c'est
   un clic : on ne fait rien. Au-delà, le glisser commence.
   Ce seuil est ce qui permet au clic actuel de survivre intact.
3. **Le glisser commence.** La carte se soulève sous le pointeur. Les cibles
   possibles s'allument, le reste s'assombrit. Une étiquette apparaît près du
   pointeur. Un trait relie la carte à ce qui est visé.
4. **Survol.** L'étiquette dit ce qui va se passer : « Attaquer Rhino »,
   « Contrer Le casse », « Jouer Feinte sur Hydra Bomber ». Sur une cible
   impossible, elle dit le refus.
5. **Lâcher sur une cible valide.** L'action part immédiatement, comme un clic
   aujourd'hui. Si elle réclame un paiement ou d'autres cibles, le plateau
   enchaîne sur ce qu'il demande déjà maintenant.
6. **Lâcher ailleurs.** La carte revient à sa place et une bulle courte dit
   pourquoi. Voir le point 6.

**Décision** : le lâcher engage. Pas de « Confirmer » supplémentaire. C'est le
comportement du clic actuel, et un geste volontaire de plusieurs centimètres
est déjà une confirmation.

⚠ **Ce point a demandé une correction, le 08/09/2026 au premier essai** : le
plateau redemandait quand même confirmation. Sa « validation courte » ne part
que si l'action n'avait **qu'une seule** cible légale, au motif qu'un joueur
qui vient de choisir parmi plusieurs gagne à jeter un dernier regard. Ce motif
tombe quand la cible a été désignée d'un geste : redemander, c'est faire faire
deux fois le même choix. La règle a donc été étendue au geste, et à lui seul.
Tous les autres garde-fous restent : rien ne part tout seul s'il reste un
paiement facultatif, un surpaiement récompensé, une cible répétable ou une
cible de plus à prendre.

---

## 4. Lever l'ambiguïté

Glisser le héros sur un ennemi peut correspondre à plusieurs actions : son
attaque de base, une capacité de son identité, un événement qu'il tient.

- **Une seule action possible vers cette cible** : elle part, sans rien
  demander.
- **Plusieurs** : un menu court s'ouvre au point exact du lâcher, listant les
  actions, la cible déjà retenue.

C'est déjà la règle du clic sur une cible : `optionsDisponiblesVersCible` en
compte une, elle part ; il en compte plusieurs, `MenuActionsCarte` s'ouvre.
Le glisser réutilise cette fonction et ce menu, avec un point d'ancrage
différent.

Il manque la fonction symétrique : **pour une source qu'on soulève, quelles
cartes peut-elle viser.** Elle se déduit de `all_legal_targets` des options
dont `bind_id` est la source. C'est le seul calcul neuf de tout le chantier.

---

## 5. Où atterrit une carte qui ne vise personne

Décision de l'utilisateur : **chaque chose dans sa zone.** Pas de cadre
« Jouer » générique.

**⚠ CORRIGÉ À L'IMPLÉMENTATION, LE 08/09/2026, PAR UNE PARTIE RÉELLE.**

La première version de cette section déduisait la zone du TYPE de carte : un
allié à la ligne de combat, un soutien à l'aire du héros. Le moteur dit autre
chose. Jouer une carte de la main n'est pas une action sans cible : c'est une
option `Play` de portée [1, 1] qui **vise l'identité**. Une règle écrite sur le
type de carte se serait donc trompée sur toutes les cartes de la main.

Et une zone vide n'existe pas dans la page : `emplacement()` (zones.ts) la
supprime quand tous ses groupes sont vides. Au premier tour, la ligne de combat
n'est pas dessinée, donc le tout premier allié de la partie aurait été
impossible à poser.

**La règle retenue, tirée du moteur et non devinée** : une zone accepte la
carte quand elle contient **exactement une** cible légale, et lâcher dans la
zone revient à lâcher sur cette carte. On jette donc son allié dans l'aire de
son héros, là où vit l'identité qu'il rejoint, sans avoir à viser la carte au
pixel près. Une zone qui en contiendrait deux serait ambiguë : elle n'est pas
proposée, et le joueur vise la carte précise.

Vérifié en partie réelle : glisser Daredevil depuis la main vers l'aire du
héros affiche « Jouer · Peter Parker », allume l'identité, et le lâcher
enchaîne sur l'étape de paiement.

Une amélioration qui s'attache, un attachement qui vise un ennemi : ils ont une
cible, ils se lâchent sur leur porteur, sans passer par les zones.

---

## 6. Le lâcher raté

La carte retourne à sa place, en glissant, et une bulle courte dit pourquoi :
« Rhino ne peut pas être attaqué : Hydra Soldier le protège. »

Le plateau sait déjà formuler ces refus. `verdictCiblage`
(`src/board/MenuActionsCarte.tsx`) produit aujourd'hui « Peut être attaqué »,
« Ne peut pas être attaqué » et la raison, affichés dans le menu de ciblage.
On réemploie la même source, dans une bulle éphémère.

Un lâcher dans le vide, sur le fond du plateau, ne dit rien : la carte revient,
c'est tout. Il n'y a pas de refus à expliquer, il n'y avait pas de cible.

---

## 7. Le retour visuel

Les quatre éléments ont été retenus.

1. **Les cibles possibles s'allument** dès que le glisser commence, le reste
   s'assombrit. C'est ce qui apprend le jeu tout seul : on voit ce qu'on peut
   faire avant de le faire.
   ⚠ **On assombrit, on ne rend pas transparent** (corrigé le 08/09/2026 au
   premier essai). Avec de la transparence, le bleu de la table passait au
   travers et teintait toutes les cartes en bleu. Un filtre agit sur les pixels
   de la carte, sans rien laisser passer derrière, comme le plateau le fait
   déjà pour une carte désactivée.
2. **La carte se soulève** : un peu plus grande, légèrement inclinée, une
   ombre portée. Elle suit le pointeur.
3. **Une étiquette suit le pointeur** et nomme l'action à venir.
4. **Un trait part de la carte** et pointe la cible survolée.

Le trait et l'étiquette vivent dans une couche au-dessus du plateau, comme les
couches existantes (`CoucheCurseurs`, `CoucheAnimations`). Ils ne touchent
jamais à la mise en page des cartes.

---

## 8. Découpage du code

**Créés**

- `src/board/glisser/useGlisser.ts` : le hook de geste. Pointer Events,
  capture du pointeur, seuil de déclenchement, `vientDeDeclencher()` pour
  neutraliser le clic qui suit. Modèle : `useAppuiLong`.
- `src/board/glisser/cibles.ts` : le calcul neuf. Pour une source, la liste
  des cartes et des zones qu'elle peut viser, et pour un couple source-cible,
  les options qui s'appliquent.
- `src/board/glisser/CoucheGlisser.tsx` : la carte soulevée, l'étiquette, le
  trait, la bulle de refus.
- `src/board/glisser/depot.ts` : le test de survol. Quelle carte ou quelle
  zone se trouve sous le pointeur, à partir de `boitesDesCartes`.

**Modifiés**

- `src/board/Board.tsx` : brancher `pointerdown` et `pointermove` à côté du
  `pointerup` existant, et marquer les zones d'atterrissage.
- `src/board.tsx` : câbler le lâcher sur `choisirOption`, et ouvrir
  `MenuActionsCarte` au point du lâcher quand plusieurs actions se présentent.
- `src/components/ScanCard.css` : les états visuels du glisser.

**Intouchés** : `interaction.ts`, `moteur.ts`, `ask.ts`, `zones.ts`. Le
protocole avec le moteur ne change pas d'une ligne. C'est ce qui rend le
chantier sûr : on ajoute une façon de désigner, pas une façon de jouer.

---

## 9. Ce qui ne change pas

Le clic reste exactement ce qu'il est, dans ses deux modes, simple et
détaillé. Un joueur qui ne glisse jamais ne verra aucune différence. C'est la
condition posée par l'utilisateur : « en plus de ce qu'on a ».

Aucun réglage à activer. Le glisser marche, ou il ne se déclenche pas et le
clic prend le relais.

---

## 10. Tests

- **Vitest**, 30 cas : le calcul de cibles (16) et le geste monté dans un vrai
  plateau (14). Seuil de déclenchement, clic préservé sous le seuil, clic non
  déclenché après un lâcher, cibles légales d'une source, options d'un couple
  source-cible, zones, refus.
- **Playwright** (`npm run glisser`) : le geste complet dans une VRAIE partie.
  ⚠ Les fixtures `?etat=` ne conviennent pas : ce sont des instantanés de
  `/get_world` en lecture seule, sans aucune option du moteur, donc sans rien à
  glisser. Le cas crée donc une partie par `/new`, comme `npm run lancement`,
  et vérifie que le méchant perd vraiment des points de vie.
- **Le témoin qui compte** : trois cas prouvent que le clic marche toujours.
  Sans eux, on découvrirait la régression en partie.

---

## 11. Pièges connus, déjà payés ailleurs

- **Pointer Events, jamais l'API HTML5 de glisser-déposer.** Consigné dans
  `.planning/research/PITFALLS.md`. L'ancien plateau
  (`public/js/marvel/draggable.js`) tenait sur `mousedown` seul, ce qui le
  rendait inerte au tactile.
- **`touch-action` n'existe nulle part dans les CSS actuels.** Sans lui, un
  glisser tactile deviendra un défilement. Sans objet tant qu'on reste à la
  souris, à poser le jour du tactile.
- **La couche visuelle interne d'une carte est en `pointer-events: none`**
  (`ScanCard.tsx`). La zone sensible est la carte à sa taille normale, pas son
  agrandissement au survol. Le test de survol doit s'en souvenir.
- **Les doublons de `all_legal_targets` sont significatifs** : ils portent les
  sélections réparties et les coûts variables (`ciblesParOccurrence` dans
  `interaction.ts`). Ne pas les écraser en construisant la liste des cibles.
- **Une cible peut être légale sans être dessinée** (enfouie dans une pile).
  `interaction.ts` la renvoie alors vers `SelecteurCibles`. Le glisser ne peut
  pas viser ce qu'on ne voit pas : ces cibles restent au clic.

---

## 12. Hors périmètre

- **Le tactile.** Décision de l'utilisateur : l'ordinateur d'abord. Le plateau
  portrait du téléphone est en cours de refonte, sa spec v2 attend dans
  `.planning/todos/2026-09-07-parcours-solo-mobile-portrait.md`. Coder le
  geste tactile sur une disposition qui va changer serait à refaire.
- **Défendre avec un allié** au glisser. Écarté.
- **Réorganiser le plateau** en déplaçant des cartes pour le confort, sans
  effet de jeu. Jamais demandé, et cela brouillerait le sens du geste.
