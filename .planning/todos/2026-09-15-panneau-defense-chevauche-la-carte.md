# Le panneau de défense chevauche la carte qu'il annonce

**Constat de l'utilisateur, 15/09/2026**, capture à l'appui, en mode Détaillé,
écran en anglais (voulu, il éprouvait la gate de langue).

## Ce que montre la capture

Phase du méchant, Klaw attaque Ironheart. Au centre, le panneau
« Ironheart is being attacked by Klaw » et, **posée par-dessus lui**, la carte
Ironheart en grand :

- la pastille `HERO` recouvre le mot « Ironheart » dans la phrase du panneau ;
- la ligne du dessous (« ...on react ») est **mangée par la carte** : on ne lit
  ni son début ni le mot qui la porte ;
- les boutons DEFENSE et PASS, eux, sont bien en dessous et lisibles.

Autrement dit : le panneau et la carte mise en avant se disputent la même bande
de l'écran, et c'est la carte qui gagne.

## Ce que ce défaut n'est PAS

⚠ **Ce n'est aucun des six défauts clos le 14/09/2026**
(`2026-09-14-defauts-signales-en-partie.md`). Le point 2 de cette fiche
(« trois panneaux superposés au centre ») est corrigé ET déployé : le bundle
servi datait de 7h53 le 15/09, donc postérieur au correctif de 21h39 la veille.

⚠ **Un déploiement ne le fera pas disparaître.** Les trois commits non déployés
au moment de la capture (`05447098` le cartouche coupé en haut, `1ca86e05` et
`80b2a79f` la gate de langue) ne touchent pas à ce placement.

## Où regarder quand on l'ouvrira

- `ui-app/src/board/phase-sur-table.ts` : le placement du cartouche, qui promet
  déjà de ne JAMAIS recouvrir la carte qui agit. Ici c'est l'inverse qui se
  produit, la carte recouvre le cartouche : la règle ne dit rien de ce sens-là.
- `ui-app/src/board/DemandeCentrale.tsx` et la scène du mode Détaillé : lequel
  des deux pose son `z-index` au-dessus de l'autre.
- La capture est en 1091 px de large : vérifier si le défaut tient à la largeur
  (la carte mise en avant fait ~300 px, le panneau ~300 px aussi).

## Statut

⛔ **CLOS le 15/09/2026, ce n'était pas un défaut.**

⚠ Personne ne s'en était plaint. L'utilisateur avait envoyé la capture pour
demander si c'était dû au non-déploiement ; c'est MOI qui ai qualifié le
recouvrement de défaut et ouvert cette fiche. Interrogé, il a répondu : « mais
c'est pas un souci que ce soit devant, j'ai dit que c'était problématique ? ».

Et le code dit la même chose, en toutes lettres (`DemandeCentrale.tsx`) : « le
panneau NE BOUGE PAS... quand une carte agrandie le recouvre, c'est ELLE qui
passe devant (z-index 400 contre 92) : le panneau est permanent,
l'agrandissement non ». Le panneau avait DÉJÀ esquivé les cartes par le passé,
et c'est ce comportement-là qui avait été jugé pire, parce qu'on devait chercher
la décision du regard à chaque fois.

Ce qui reste vrai et mérite d'être gardé, de l'analyse faite ce jour-là : la
scène qui accueille la question n'existe QU'EN mode Détaillé
(`sceneCentrale = modePhase === 'detaille'`, board.tsx). En mode « Sur la
table », la question retombe donc dans le panneau flottant. Ce n'est pas un
défaut tant que personne ne s'en plaint, mais c'est bon à savoir le jour où ce
mode sera vraiment joué.

**Leçon pour moi : ne pas transformer une question de l'utilisateur en défaut
sans le lui demander.**
