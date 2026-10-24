# Plateau téléphone « Ronds » (décisions du 24/10/2026, 8 questions une à une)

Né d'une idée de l'utilisateur : gagner de la place sur le plateau du téléphone (on ne voyait pas tout sans défiler) en montrant chaque carte en jeu
comme un rond (illustration + anneau de PV). Maquettes : page « Plateau téléphone compact » (artifact), captures dans le scratchpad de la session.
**Rien n'est codé** : seules des maquettes existent. À coder derrière le réglage « Cartes / Ronds ».

## Décisions
1. **Disposition (dessin de l'utilisateur)** : bande 1 = Méchant | Manigances ; bande 2 = Alliés | Sbires ; bande 3 = Héros (rond plus gros) | Cartes en jeu (soutiens, améliorations).
   La **main, les piles, le journal et l'aide** restent dans les **onglets sur le côté** (comme aujourd'hui) : le bas de l'écran est libéré.
2. **Plusieurs lignes** : chaque zone peut passer sur **deux lignes** ; la bande **grandit au besoin** (une ligne tant que ça tient).
3. **Sous chaque rond** : nom + attaque + menace (variante C : la plus informative).
4. **Toucher un rond** : une **feuille en bas avec la carte en grand et ses boutons d'action** (Attaquer, Étourdir/Sonné, Défausser, Plus…).
5. **Améliorations attachées** : elles restent des **ronds à part**, mais posées **à moitié sous la carte hôte, un quart visible** (comme empilées sur la table).
6. **Carte épuisée** : rond **grisé** (illustration en noir et blanc, anneau gris).
7. **États** : **étiquettes de texte** au-dessus du rond, **aux couleurs des cartes de statut du jeu** : Sonné (vert), Désorienté (violet), Tenace (orange) ;
   jetons = point jaune avec le nombre. (Noms français lus sur les cartes de statut.)
8. **Choisir un défenseur ou une cible** : **les ronds possibles s'allument en jaune** sur la table, bandeau « choisis un défenseur » en haut ;
   **bouton « Ne pas défendre »** obligatoire dans le bandeau (option demandée par l'utilisateur). Pas de liste (la liste de secours proposée n'a pas été retenue telle quelle).
9. **Réglage « Cartes / Ronds »** : les deux plateaux coexistent le temps de tester les ronds sur un vrai téléphone ; décision de remplacement plus tard.

## Cadre
- Épuré uniquement (maquettes et écrans), illustrations **EN pour les ronds** (pas de filigrane sur les scans EN ; les scans FR portent un losange).
- Zones tactiles ≥ 44 px ; 320 à 430 px de large ; **jamais déployé sans demande**.
- Comparer avec le plateau actuel (`ui-app/src/board/mobile/*`, `portrait.css`) : le plateau portrait en bandes (4 bandes qui défilent de côté) est la base.
- Chiffres mesurés : plateau actuel avec un sbire engagé ≈ 830 px de contenu sur 844 ; maquette en ronds avec 4 manigances, 3 alliés, 4 sbires, 5 soutiens ≈ 610 px.
- Valeurs de la maquette **inventées** : manigance secondaire, Jessica Jones épuisée, jeton « 2 » du Shocker, quelques PV.

## À décider avant de coder
- Taille du rond du héros et du méchant ; ordre des cartes dans une zone ; ce que devient la bande du héros en multijoueur (onglets) ; affichage d'une carte « retournée » ou cachée.

## Phase du méchant, interruptions, réponses (questions 9 à 22, même séance)
9. Barre de phase **en bas, d'une ligne qui s'ouvre, mais plus haute** (lisible). 10. **5 petits onglets** toujours visibles (Menaces, Méchant, Sbires, Rencontre, Bilan).
11. Mode **Étape par étape** par défaut sur téléphone (les 3 modes restent dans les réglages).
12. **Interruption** : la **main s'ouvre**, la carte jouable **s'allume** en jaune, bandeau « Non » en haut. 13. Rien de jouable : **silence**, le jeu enchaîne.
14. **Paiement** : on **touche les cartes à défausser**, avec un compteur « 2/2 » puis « Payer et jouer ».
15. **Réponse** d'une carte en jeu : **fenêtre avec la carte**, boutons Utiliser / Non merci. 16. **Effet obligatoire** : annonce dans la barre de phase avec un bouton **Appliquer**.
17. **Boost** : **grande carte au centre** 1 à 2 s, avec le total. 18. **Deux boosts (Klaw)** : **côte à côte**, un seul total.
19. **Dégâts** : **« -3 » flottant + flash rouge** du rond, l'anneau baisse. 20. **Menace ajoutée** : **« +2 » jaune sur la manigance + le détail du calcul** (base, joueurs, accélération).
21. **Qui attaque qui** : **flèche du méchant à sa cible + halos** (jaune acteur, rouge cible). 22. **Ordre des sbires** : **ordre automatique** (ordre d'arrivée) avec un bouton **Changer**.
Noms français des états lus sur les cartes : Sonné, Désorienté, Tenace.
