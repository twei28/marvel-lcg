# Le déroulé détaillé, condensé : douze décisions

Suite de `2026-09-06-phase-mechant-deroule-detaille-design.md`, écrite après le
premier contrôle en partie réelle.

## Le constat qui a déclenché cette passe

Mot pour mot : « je vois des fois que c'est un peu trop détaillé parce qu'il y a
marqué truc va s'activer, puis il va mettre autant et puis il les met. C'est un
petit peu trop quoi, deux ou trois explications pour dire une seule chose. »

Et la forme attendue, elle aussi mot pour mot : « je veux vraiment qu'il y ait
genre tour du vilain et puis après on voit bien pose de x manigances sur la
manigance principale. Après l'activation du méchant, après l'activation des
sbires et puis donner la carte de rencontre. »

Ce document ne vaut que pour le mode **Détaillé**. Le mode Instantané ne change
pas.

---

## 1. La forme d'une étape : titre concret, règle repliée

Le cartouche affichait trois lignes pour un seul fait : un titre générique, le
détail, puis la règle du jeu.

    Menace sur la manigance principale
    • L'Effraction ! gagne 2 menaces
    Point 1 : chaque joueur ajoute 1 menace à la manigance principale.

Il n'en affiche plus qu'une, qui dit directement ce qui se passe, avec le
compteur de la carte visée :

    L'Effraction ! gagne 2 menaces                    5/8
    › la règle

Le titre générique disparaît. La règle du jeu reste écrite, mais repliée.

## 2. La règle repliée se retient comme un réglage

Une fois dépliée, elle le reste sur toutes les étapes et toutes les parties,
jusqu'à ce qu'on la replie. C'est un choix qu'on ne fait qu'une fois : celui qui
apprend la garde ouverte, celui qui connaît ne la revoit jamais.

Conséquence technique : c'est un réglage personnel, donc `localStorage`, comme
le mode et l'avance auto.

## 3. La narration technique du moteur disparaît du cartouche

Une phase observée en partie réelle a produit **douze étapes, dont huit de
narration technique**, en anglais et illisibles :

    Rage of Ultron were discarded
    Warlock's Cape was discarded to Adam Warlock's DiscardPile<3>
    Fin de l'activation de Ultron
    Ultron n'appliquent plus Shadow of the Past

Elles ne sont plus des étapes du tout. **Rien n'est perdu** : elles restent
entières dans le journal à droite et dans le Log.

Cela renverse l'arbitrage du 06/09 au matin (« tout garder, mais sans clic »),
qui les faisait défiler seules une demi-seconde chacune. Voir passer huit lignes
illisibles reste du bruit, même sans clic.

## 4. Cinq temps dans la chronologie, méchant et sbires séparés

    MENACE · MÉCHANT · SBIRES · DISTRIBUTION · RÉVÉLATION

Au lieu des quatre actuels, qui fondaient le méchant et ses sbires sous un seul
« ACTIVATIONS ». La carte de référence officielle n'en fait qu'un point, mais le
méchant s'active avant ses sbires et ce sont deux moments distincts du tour :
les voir séparés dit où on en est.

## 5. Un temps vide est barré, il ne coûte aucun clic

    MENACE · MÉCHANT · ~~SBIRES~~ · DISTRIBUTION · RÉVÉLATION
       ✓        ✓       (aucun)         ●            ○

Le temps reste visible mais grisé et barré : on voit qu'il a été passé et
pourquoi, sans valider une étape qui ne dit rien.

## 6. Le chiffre : le résultat, une fois

Une activation dit qui agit et ce que ça a coûté, en une phrase. Les cartes de
boost restent affichées, c'est le moment de tension du jeu.

    [MÉCHANT]
    Klaw attaque Colossus
    → 4 dégâts

    boost : Hydra Bomber  +1
    › la règle

On ne lit plus l'annonce du montant PUIS son application.

## 7. Deux temps SEULEMENT quand on peut vraiment agir

Arbitrage de l'utilisateur, et c'est une règle du jeu qu'il a raison de
rappeler : entre la déclaration d'une attaque et sa résolution, on peut
défendre ou jouer une interruption.

L'étape se dédouble donc en « intention » puis « résultat » **uniquement quand
le moteur ouvre réellement une fenêtre**. Quand rien n'est jouable, elle reste
en un seul temps.

    Cas où l'on peut défendre :
      Klaw va attaquer Colossus
      boost : Hydra Bomber  +1
      → tu peux défendre ou répondre        [ Suivant ]
      Klaw attaque Colossus → 4 dégâts      [ Suivant ]

    Cas où rien n'est jouable :
      Klaw attaque Colossus → 4 dégâts      [ Suivant ]

On ne clique deux fois que là où ça compte.

**Implémenté le 06/09/2026 (tâche A3), avec une nuance sur le nombre de clics.**
Le moteur inscrit désormais deux faits par activation : une intention à la
déclaration (`etat: 'annonce'`, avant `WhenUnitWouldAttack`, donc avant les
boosts et avant les questions au joueur), puis la résolution (`etat: 'resolu'`),
qui remplace la première sous le même `activation_id`. L'étape du cartouche ne
change donc pas de clé : elle se complète sur place.

La nuance : dans le cas où l'on peut agir, l'intention ne porte PAS de bouton
« Suivant ». Le moteur n'attend pas un accusé de réception à ce moment-là, il
attend une réponse à sa question, posée ailleurs (le panneau central). Un
« Suivant » y aurait été un bouton sans effet. Le cartouche affiche donc
l'intention et la mention « tu peux défendre ou répondre », puis se complète
tout seul une fois la question résolue ; le joueur clique une fois, sur l'étape
complète. Dans le cas où rien n'est jouable, l'accusé part immédiatement sur
l'intention et l'étape n'est vue qu'une fois, complète, exactement ce que
cette décision demande.

Une activation annoncée qui n'a finalement pas lieu (un « ... instead » qui la
remplace, une cible qui quitte la table) se clôt par un fait `etat: 'annule'`,
et l'étape dit « L'attaque n'a pas lieu. » : une intention sans suite laisserait
le cartouche sur « va attaquer » jusqu'à la fin de la phase.

## 8. Une étape par sbire, avec un compteur

    SBIRES                                          1 sur 3
    Trafiquant d'armes attaque Colossus
    → 2 dégâts

Chacun a son moment, sa carte mise en avant et son trait vers sa cible. Le
regroupement était tentant, mais il casserait dès qu'un sbire ouvre une fenêtre
pour défendre (décision 7).

## 9. L'ouverture : le bandeau suffit

Pas d'étape « Tour du vilain » à valider. L'annonce plein écran dit déjà « phase
du méchant, round X », et la chronologie à cinq temps montre immédiatement où
l'on va. Un premier clic qui ne dirait rien de plus coûterait un geste par round.

## 10. La fermeture : un bilan court, à valider

    MENACE · MÉCHANT · SBIRES · DISTRIBUTION · RÉVÉLATION
       ✓        ✓        ✓          ✓            ✓

    FIN DE LA PHASE DU MÉCHANT
    Colossus a pris 6 dégâts                     8/14 PV
    L'Effraction ! a gagné 3 menaces                6/8

                                        [ À toi de jouer ]

C'est le moment où l'on décide de son tour : l'avoir en deux lignes évite de
remonter le journal.

## 11. Le multijoueur suit les règles officielles

Chaque joueur révèle et résout sa carte rencontre **dans l'ordre du tour, en
commençant par le premier joueur**. Toutes les cartes sont montrées à tous : le
jeu est coopératif et à information ouverte, seules les mains sont privées.

Une étape par joueur, avec son compteur, comme pour les sbires.

## 12. Chacun valide chez soi, et l'on attend tout le monde

Le déroulé avance quand tous les joueurs ont validé. Personne ne rate d'étape.

Le filet anti-blocage reste indispensable et relâche la table au bout d'un long
moment si quelqu'un s'est absenté : un onglet oublié ne doit pas geler une
partie. Il ne doit pas être court, sous peine de doubler un joueur attentif.

## 13. Un héros vaincu arrête le déroulé net

    MÉCHANT
    Klaw attaque Colossus → 6 dégâts

    ☠ COLOSSUS EST VAINCU

    La phase s'arrête ici.                    [ Continuer ]

C'est le moment le plus important d'une partie : il ne doit pas défiler comme
les autres.

---

## Ce que ce document ne tranche pas

- La version mobile.
- Le déroulé des effets pendant le tour d'un joueur.
- Le récapitulatif de fin de partie, qui garde son rôle pour le mode Instantané.
