# Scène centrale de la phase du méchant (mode Détaillé)

Décidé avec l'utilisateur le 7 septembre 2026, après une phase jouée en vrai
(Taskmaster contre Ant-Man) qui a montré trois défauts du cartouche actuel :
la table est en avance sur le récit, la carte révélée n'est jamais montrée
(un dos de carte est agrandi pendant que le texte la nomme), et les tailles
n'obéissent à aucune règle lisible (agrandissement sur place, selon les
cartes, en 200 ms).

## Décisions

1. **Scène centrale.** Pendant la phase du méchant, un panneau centré prend le
   milieu de l'écran. La table derrière est assombrie et n'est plus une
   source d'information : elle peut être en avance sur le récit (une trame
   retenue peut porter deux étapes). La scène porte ses propres chiffres,
   avant → après, tirés des faits du moteur.
2. **Une seule taille de carte** dans la scène, environ 2,5 fois une carte de
   la table, face visible. Plus aucune carte n'est agrandie sur place dans la
   table, plus de trait, plus de cartouche collé à la main. La chronologie
   des cinq temps passe en haut de la scène.
3. **Un clic par étape.** Rien n'avance sans le joueur (Suivant, Espace,
   Entrée ; Échap déroule tout). L'avance automatique n'est plus proposée.
4. **Distribution puis révélation, deux étapes**, comme les règles : le dos
   de la carte avec le héros, puis la carte face visible, lisible, qui reste
   tant que le joueur n'a pas cliqué.
5. **Les questions du moteur dans la scène** : la scène reste (auteur face à
   cible, boosts visibles) et les boutons du choix prennent la place de
   Suivant. Pour un choix de cible ou d'ordre, les cartes candidates
   s'affichent dans la scène et se cliquent là.
6. **Une seule vue par activation** : l'annonce (« va attaquer ») et la
   résolution partagent la même scène et la même clé ; la résolution
   complète le texte et pose les boosts sans rien déplacer.

## Storyboard (Taskmaster contre Ant-Man)

- Menace : la manigance principale seule. « Hunting Down Heroes gagne
  1 menace · 1 → 2 / 12 ».
- Méchant : Taskmaster à gauche, flèche, cible à droite. Boosts en cartes à
  côté de Taskmaster. « Taskmaster complote contre Hunting Down Heroes ·
  1 imprimé + 2 (Photographic Reflexes) = 3 menaces · 2 → 5 / 12 ». Pour une
  attaque : « 4 dégâts · Scott Lang 12 → 8 PV ».
- Sbires : même dessin, un sbire à la fois. Sans sbire, temps barré.
- Distribution : dos de carte rencontre, héros à droite. « Scott Lang reçoit
  sa carte rencontre ». Le fait ne dit pas laquelle : c'est juste.
- Révélation : la carte grande, face visible. « Scott Lang révèle Captured
  by Hydra ». Limite connue : le moteur ne raconte pas encore l'effet
  produit ; le joueur le voit sur la table au clic suivant.
- Bilan : dernière étape, inchangé.

## Ce qui ne change pas

Précédent relit sans rejouer ; le bouton « la règle » ; le filet de 90 s
d'inactivité ; le contrat avec le moteur : l'accusé de réception part du même
effet qu'aujourd'hui (`DeroulePhase.tsx`, garde sur `trameRetenue`), rien
n'est modifié côté Python.

## Contraintes techniques relevées

- La table affiche le dernier monde reçu ; la scène ne doit rien lire sur la
  table. Les images viennent de l'index du monde (`cartesMondeParId`) par
  `pic_id`, avec visibilité forcée pour la carte révélée et les boosts,
  comme `ciblesHorsTable` le fait déjà. La carte distribuée n'a pas d'id :
  un dos.
- Le fait de révélation est journalisé AVANT le retournement : le monde de
  cette trame montre encore un dos dans `dealt_encounter_cards`.
- Les faits peuvent être dégradés (champs optionnels, `faits_mechant`
  absent) : la scène tient sans image (nom seul) et sans chiffres.
- Une question de ciblage porte `all_legal_targets` (ids) : de quoi montrer
  les candidats dans la scène.

## Livraison, une étape à la fois, avec capture à chaque fois

A. La scène : disposition, cartes de l'étape, textes, boutons ; retrait de
   la mise en scène sur place et du trait.
B. Les chiffres avant → après et le détail des boosts dans le texte.
C. Les questions simples (Défendre / Passer, options sans cible) dans la
   scène.
D. Les questions de ciblage et d'ordre dans la scène.
