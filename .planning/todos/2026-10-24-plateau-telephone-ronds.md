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
21. **Qui attaque qui** : **flèche du méchant à sa cible + halos** (jaune acteur, rouge cible). 22. **Ordre des sbires** : **on touche les sbires dans l'ordre voulu**, des numéros apparaissent (réponse donnée à la 2e demande ; la 1re avait dit « ordre auto + Changer »).
Noms français des états lus sur les cartes : Sonné, Désorienté, Tenace.

## Questions 23 à 39 (suite de la même séance)
23. **Carte rencontre révélée** : grande carte + feuille de résolution (texte + « Résoudre »). 24. **Traîtrise** résolue : la carte **reste au centre jusqu'à « Fermer »**.
25. **Renfort** (mot officiel français de Surge, pas « Surcroît ») : pastille rouge « RENFORT » sur la carte **+** le compteur « 1/2 » dans le titre de la feuille.
26. **Bilan** : trois lignes de résumé (menace, PV du héros, cartes arrivées) puis Terminer. 27. **Nouveau round** : écran « ROUND 3 » en grand, 1 seconde.
28. **Actions du héros** (Attaquer, Déjouer, Récupérer, Changer de forme) : dans la **feuille de la carte du héros**. 29. **Cible d'une attaque** : cibles en jaune, un toucher.
30. **Garde** : méchant assombri + étiquette « Garde » sur le sbire + bandeau. 31. **Crise** : même traitement que la Garde.
32. **Main** : une rangée qui défile de côté (grandes cartes), **posée SOUS les zones** (jamais par-dessus). 33. Si les zones grandissent, **la main rapetisse**.
34. **Ressources** : montrées **seulement au moment de payer**. 35. Au paiement, les **cartes de la table qui génèrent des ressources** s'allument en bleu avec « +1 ».
36. **Changement de forme** : le rond se retourne comme une pièce. 37. **Multijoueur** : onglets de joueurs en haut (J1, J2), une zone Héros à la fois.
38. **Sbire engagé** : pastille J1 / J2 sur chaque sbire. 39. **Nouveau stade du méchant** : le rond se retourne **et** la carte du nouveau stade s'affiche au centre (bouton Continuer).
Cartes de statut françaises : Sonné, Désorienté, Tenace. Mots-clés : Renfort (Surge), Garde (Guard), Crise (Crisis).

## Questions 40 à 48
40. **Fin de partie** : bannière explosive (celle de l'utilisateur, « Defeat ! » / équivalent victoire) + feuille de statistiques avec Rejouer / Menu. 41. **Journal** : liste chronologique, pastille de round.
42. **Piles** : quatre dos de cartes avec compteurs (deck, défausse, deck et défausse rencontre), un toucher ouvre la pile. 43. **Environnement** : rond à contour violet dans la zone Manigances, étiquette « ENV. ».
44. **Sbire ou allié vaincu** : rond grisé + étiquette rouge « VAINCU » une seconde, puis il quitte la table. 45. **Annuler** : flèche ↶ permanente dans la barre du haut (sans limite de 5 s).
46. **Mise en place** : une carte par écran, grande, **les manigances en paysage**. 47. **Menu « … »** : liste d'actions avec pictogrammes. 48. **Paysage** : les mêmes zones en largeur, la main dans un panneau à droite (réponse à la 2e demande ; la 1re avait dit « verrou portrait »).

## Questions 49 à 58
49. **Fin du tour** avec des cartes prêtes : une confirmation qui dit ce qu'il reste (cartes prêtes, ressources) ; sinon le tour se termine directement.
50. **Tour d'un autre joueur** : bandeau « En attente de J2 » ; **toucher Storm montre sa table** (ses zones).
51. **Appui long sur un rond** : aperçu de la carte en grand tant qu'on appuie, sans boutons (réponse à la 2e demande ; un simple toucher ouvre la feuille).
52. **Mode manuel** : barre d'outils en bas (PV, jeton, épuiser, défausser) qui agit sur le rond choisi.
53. **Danger (menace proche du maximum)** : aucune alerte, seule la pastille orange donne la valeur.
54. **Cartes rencontre face cachée du héros** : petit dos rouge avec le nombre à côté du rond du héros.
55. **Jetons** : une pastille par type de jeton, avec son icône.
56. **Connexion perdue** : bandeau rouge, la partie reste visible et conservée.
57. **Aide** : visite guidée de 5 étapes à la première partie.
58. **Taille des ronds** : automatique selon la largeur de l'écran (pas de réglage), 320 à 430 px.

## Synthèse pour le codage
- Toute la table est en ronds ; la main est une rangée posée sous les zones (elle rapetisse si les zones grandissent) ; piles, journal et aide restent dans les onglets sur le côté.
- Feuille en bas = carte en grand + boutons d'action (toucher), aperçu seul (appui long).
- Phase du méchant : barre de phase en bas, plus haute, 5 petits onglets, mode « Étape par étape » par défaut, interruption = la main s'allume, réponse = fenêtre avec la carte, effet obligatoire = bouton Appliquer.
- Sélection de cibles : ronds jaunes + bandeau, bouton « Ne pas défendre » ; flèche + halos pour « qui attaque qui » ; Garde et Crise : assombri + étiquette + bandeau.
- À tester sur un vrai téléphone avant tout remplacement : réglage « Cartes / Ronds ».

## Cas particuliers demandés ensuite (59 à 67)
59. **Overkill** : flèche jaune du sbire vers le méchant + « -2 » jaune sur le méchant + bandeau « Overkill : 2 dégâts en trop passent au méchant ».
60. **Riposte** : étiquette « Riposte 1 » en permanence sur le sbire ; après l'attaque, flèche rouge vers le héros + « -1 » + bandeau.
61. **Attacher une amélioration** : les cartes possibles s'allument en jaune + bandeau, on touche l'hôte. 62. **Choisir un défenseur** : seulement les halos jaunes (pas d'aperçu des PV), plus « Ne pas défendre ».
63. **Némésis / Obligation** : grande carte à résoudre à l'arrivée (comme les autres cartes rencontre), puis un rond.
64. **Embuscade** : pastille « EMBUSCADE » sur la grande carte (comme Renfort) **puis** la flèche rouge de l'attaque sur le rond. « Péril » : à traiter avec le texte de la carte.
65. **Héros K.O. (0 PV)** : le héros est **éliminé de la partie**, il ne repasse PAS en alter ego (erreur de ma première maquette, corrigée par l'utilisateur). Écran rouge plein « K.O. ! » à valider ; en solo il mène à la défaite.
66. **Main trop grande** : feuille avec toute la main en grille, on touche la carte à défausser. 67. **Carte jouée** : événement = grande carte + feuille de résolution puis défausse ; soutien = rond posé avec un halo.

## Questions 68 à 70
68. **Péril (multijoueur)** : bandeau « Péril : seul J1 peut réagir » + onglet de l'autre joueur verrouillé 🔒 pendant la carte.
69. **Plusieurs états sur une carte** : étiquettes complètes jusqu'à 2 états, **initiales colorées** (So, Dé, Te, Hé…) dès qu'il y en a plus de 2. Cinq états : Sonné (vert), Désorienté (violet), Tenace (orange), Hébété (rouge, carte TMNT Dazed), Intensifié (rose, carte TMNT).
70. **Valeur modifiée** (attaque, menace) : la valeur change de couleur (vert = augmentée, rouge = réduite).
