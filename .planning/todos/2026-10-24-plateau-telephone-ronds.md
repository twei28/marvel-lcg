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

## Feuille d'une carte (71 et 72)
71. **Contenu de la feuille** (demande : « tout voir, comme sur le PC ») : tout empilé sous la carte : étiquette de type, carte en grand, barre de PV (ou menace), **valeurs ajustées** avec leur origine (ex. « ATQ 3 (2 +1 Lance-toile) », DEF, MNG), les **vraies cartes de statut** et l'amélioration attachée en mini-cartes, les jetons, puis les boutons d'action.
72. **Autre face** (héros / alter ego, méchant à deux stades) : **les deux faces côte à côte**, comme sur le PC (cartes un peu plus petites). Les manigances restent en **paysage**.
Référence PC : l'aperçu au survol montre la carte grande, une étiquette de type au-dessus (« MÉCHANT », « ALTER EGO »), la barre de PV dessous et « AUTRE FACE » à côté.

## CODE (24/10/2026) : premier jet du plateau en ronds, derriere un reglage
Fait, non deploye : `ui-app/src/board/mobile/ronds/` (repartir-ronds.ts, etats-ronds.ts, Rond.tsx, TableRonds.tsx, ChoixPlateau.tsx, ronds.css, ronds.test.tsx) ; `PlateauPortrait.tsx` choisit entre les bandes et les ronds selon le reglage `plateau` (`reglages-telephone.ts`) ; `card-model.ts` + `ScanCard.tsx` : `statsComplets` (toutes les stats avec leur valeur imprimee, pour colorer les valeurs modifiees).
- **Choix au debut de la partie** (`ChoixPlateau`) : sur telephone, a chaque nouvelle partie (round 1), tant que le joueur n'a pas coche **« Garder ce choix pour les prochaines parties »**. Ensuite la question ne revient plus ; le choix se change dans **Reglages > Plateau** et **Reglages > Demander le plateau a chaque partie**.
- **Cadrage des illustrations** : un peu plus haut dans le rond (remarque de l'utilisateur) : positions de fond `48% 24%` (cartes), `44% 22%` (heros), `38% 20%` (mechant).
- Fait : zones en trois rangees, anneau PV / menace, pastille, nom + ATQ / MNG colores selon la modification, etats en etiquettes puis initiales au-dela de 2, jetons par type, ameliorations en petits ronds, carte epuisee grisee, manigance en paysage tournee, un toucher = feuille de la carte (ou choisit la carte si le moteur demande une cible / une ressource), appui long = apercu.
- **Pas encore fait** (decisions notees plus haut, a coder ensuite) : main posee sous les zones (aujourd'hui : l'encoche et sa feuille comme avant), barre de phase haute avec 5 onglets, grandes cartes (boost, rencontre, nouveau stade), fleches d'attaque, Garde / Crise assombries, paysage en largeur, mode manuel au doigt, ecran K.O. et bannieres de fin, ordre des sbires par numeros, feuille de la carte « tout » avec cartes de statut et autre face.
- Essai local : `npx vite --config <config avec proxy complet> --port 5199` (le proxy d'origine de vite.config.ts ne relaie pas toutes les routes du jeu).

73. **Main repliable** : posee SOUS les zones, ouverte par defaut, une fleche ▼ la replie, la languette « Main » la rouvre ; hauteur 31 vh (118 a 210 px) ; ne se range pas toute seule en ronds (seul le joueur la replie). **Code** : `ronds/MainSousLaTable.tsx`, grille a 3 rangees dans `.plateau-portrait.avec-main-dock`.

## A faire (demandes de l'utilisateur, 24/10/2026)
- **Améliorations attachées** (Q74) : l'utilisateur a refusé A/B/C et va montrer lui-même ce qu'il veut. En attendant, le code garde la décision Q4 (petits ronds à moitié sous la carte hôte, un quart visible).
- **Admin au téléphone** : revoir les pages de la version admin pour le téléphone ; surtout, **sur la page d'accueil l'admin voit beaucoup d'icônes en haut mais pas toutes** : trouver où elles sont coupées (en-tête de `prepare.html`, `lien-admin.js`, `tel-pages.js`, menu burger) et les rendre toutes accessibles. À lancer avec captures en 320 à 430 px, compte admin.
- **Phase du méchant en ronds** : barre de phase haute avec 5 onglets, la suite de la liste (voir plus haut). Captures des étapes réelles dans le scratchpad de la session (`reel/ph-*.png`).

74-76. **Ameliorations attachees** (l'utilisateur a refuse mes variantes et dessine : « comme les cartes qui se mettent l'une a cote de l'autre un peu en dessous, mais sur le cote ») : un rond de la **MEME TAILLE que la carte hote**, pose DERRIERE elle et **decale sur le cote** (a droite), **les deux tiers** du rond depassant ; plusieurs se suivent. La zone s'elargit pour les contenir (jamais par-dessus la voisine). **Pastille de PV sous le rond** (sur le nom). Code : `--nb-amelio`, `--rang`, `.rond-mini`.
77. **Carte prete / utilisee** : une carte de la table pas encore utilisee (soutien, allie, amelioration, heros) a un **anneau vert tres fin, colle au rond** (1 px, a 2 px) ; utilisee (epuisee) elle est **grisee**, sans anneau. Les sbires et le mechant n'ont pas d'anneau pret.

## Glisser au doigt (questions 78 a 82, demande de l'utilisateur)
78. **Ce qu'on glisse** : le heros sur un mechant ou un sbire = attaquer ; le heros sur une manigance = dejouer ; une carte de la main sur sa cible = la jouer ; un allie ou un soutien pret sur une cible = l'utiliser.
79. **Demarrage** : des que le doigt bouge, le rond suit ; les cibles s'allument en jaune, les autres s'assombrissent (pas d'attente, un toucher ouvre toujours la feuille).
80. **Lacher** : l'action part tout de suite ; bandeau + fleche ↶ pour annuler.
81. **Main** : glisser vers le HAUT = jouer la carte ; de cote = la main defile.
82. **Mauvais lacher** (a vide, mauvaise cible) : la carte retourne dans la main, message « ce n'est pas une cible valide ».
Faisabilite a verifier au codage : le glissement doit declencher les memes questions du moteur que le toucher (action puis cible) ; voir `interaction.ts` (`EtatInteractif`) et `board.tsx` (`onCardClick`, `glisser`).

## CODE (suite) : glisser au doigt + jetons anglais
- **Glisser** (decisions 78 a 82) : `ronds/glisser-ronds.tsx` reutilise les regles du plateau PC (`props.glisser` : `estSource`, `ciblesLegales`, `libelle`, `onDepot`) ; geste adapte : un rond se leve des 8 px, une carte de la main seulement vers le HAUT (de cote la main defile, `touch-action: pan-x`) ; fantome + etiquette (« Jouer · Peter Parker »), cibles jaunes, autres assombries, bulle de refus (« Pas ici ») ; le clic qui suit un glisser est avale. Verifie sur la vraie partie : glisser Peter Parker sur Rhino = « Pas ici » (l'alter ego n'attaque pas) ; glisser Lance-toile de la main sur le heros = le jeu ouvre « Payer 1 pour jouer ». Pas encore verifie : attaquer avec Spider-Man (forme heros), les menus a plusieurs actions au lacher.
- **Jetons anglais** : les ronds, leurs ameliorations et le fantome du glisser utilisent l'illustration ANGLAISE (retrait de `fr_` dans l'adresse), pour ne pas voir le filigrane ; la feuille de la carte en grand reste le scan FRANCAIS.

## Icones du haut / menu admin au telephone (24/10/2026)
Constat : au telephone, les outils (Reprendre, Revoir, Stats, Puzzles, Player, Administration, Releve des illustrations, Palettes, Sauvegarde du code, Signaler un bug, Documents) etaient des icones SEULES dans le burger de l'accueil et de l'assistant, en grille, sans nom, et le menu etait plafonne a 70 % de l'ecran. **Fait** : une ligne par outil (icone + nom, 46 px), menu jusqu'a `100dvh - 130px` (une bande reste en bas pour le fermer en touchant a cote). Fichier : `prepare-tel.css` (cache `?v=5` dans `prepare.html`). Les 14 tests de l'assistant passent.
**Pas encore fait** : (1) les icones ajoutees par le COMPTE du site (lien admin du site, signalements), que je ne vois pas sur un moteur local ; a verifier sur le site apres deploiement avec un compte admin ; (2) les autres pages admin au telephone.

## CODE (suite 2) : ronds
Fait : degats / menace flottants (« -3 », « +2 »), etiquette Garde, etiquette « +1 » et anneau bleu sur une ressource a depenser, retournement d'un rond (forme, stade), « VAINCU » (fantome gris 1,1 s), fleche ↶ permanente dans la barre du haut (plus de bandeau de 5 s en ronds), « ROUND N » en grand (round 2 et plus), 27+ tests dans `ronds/`.
**Reste a faire (ordre de reprise)** : (1) grandes cartes boost / rencontre / nouveau stade (Q17, Q18, Q23, Q24, Q39) a brancher sur le panneau de phase existant (`CartouchePhase.tsx`) ; (2) fleches d'attaque + halos (Q21), Overkill / Riposte (Q59, Q60) ; (3) ecran « K.O. ! » (Q65) ; (4) feuille de carte « avec tout » (Q71, Q72) : PV, valeurs ajustees, cartes de statut, autre face, dans `CarteOuverte.tsx` ; (5) appui long = apercu seul (Q51) ; (6) paysage : zones en largeur, main a droite (Q48) ; (7) mode manuel au doigt (Q52) ; (8) visite guidee (Q57) ; (9) bandeau Peril / onglet verrouille (Q68) ; (10) pages admin au telephone ; (11) essai sur vrai telephone, 320 a 430 px, et deploiement SEULEMENT sur demande.

## CODE (suite 3, 24/10/2026) : le « Reste a faire » est vide, sauf l'essai sur vrai telephone
Fait et commite (non deploye) : (1) grandes cartes boost / rencontre revelee / stade dans le panneau de phase (`ronds.css`, `body[data-plateau='ronds']`) ; les fleches de phase visent les ronds (`carteDeLaTable`, `FlechesPhase.tsx`) ; Overkill / Riposte passent par la meme chaine que le PC, etiquette « Riposte N » permanente sur le sbire ; (3) `EcranKO.tsx` ; (4) feuille « avec tout » : `FeuilleDetail.tsx` (valeurs ajustees, jetons `JetonsCarte`, mots-cles `apercu-mots-cles` : memes composants et memes mots que l'apercu du PC, a la demande de l'utilisateur), deux faces cote a cote (`CarteOuverte` prop `detail`) ; (5) appui long = apercu tenu au doigt sans boutons (`apercuSeul`, ferme au relacher) ; (6) paysage < 768 px : main en panneau a droite (2 colonnes) ; (7) mode manuel : `BarreManuelle.tsx` (PV, menace, jeton, epuiser, defausser sur le rond choisi) ; (8) `VisiteGuidee.tsx`, 5 etapes (les ronds, la main, la phase, glisser, le menu), une seule fois ; (9) Peril multijoueur : `data-peril-joueur` sur <html> (DeroulePhase) -> bandeau + onglets verrouilles ; (10) pages admin : onglets de l'admin a la ligne, page Sauvegardes (meta viewport), Releve sans debordement ; **et les pages admin / suivi / page du site passent a l'habillage Epure (bleu)**, remarque de l'utilisateur.
Reste : essai sur un vrai telephone (320 a 430 px) ; texte de la visite guidee a valider par l'utilisateur .
Corrige : mise en place en telephone couche (hauteur < 500 px) = carte a gauche, legende + bouton Continuer a droite (`mise-en-place.css`), verifie a 667x375.

## Suite 4 (24/10/2026, apres essai sur vrai telephone) : fait et commite, PAS deploye (« pas aujourd'hui »)
Deploye en ligne : jusqu'a 7316e706 (V2 garde le mode telephone, dessin des manigances annexes). Commite ensuite, en attente de deploiement :
- Heros : un toucher le choisit, « Continuer » en bas (plus de « Choisir » en haut ni d'avance auto).
- Glisser fluide (fantome par transform, une maj par image, plus de rendu du plateau a chaque cible) ; plus d'appui long sur les ronds.
- Anneaux : carte prete = dore ; carte de la rencontre chez le joueur = contour rouge ; carte du joueur chez le mechant = contour vert.
- Etiquette Crise / Garde devant le rond ; moteur : base_health comptait le max de PV en double (Drone d'Ultron 1 / 2).
- « Retour au menu » : `signalerDepart()` (retour-android.ts) avant la navigation, sinon history.back() l'annulait (a confirmer sur vrai telephone).
- Paiement : toucher une carte de la main = payer ; cartes de la table qui paient dans la rangee de la main apres « EN JEU » ; plus de bleu.
- Visite guidee : une seule fois (Passer ou Terminer), Reglages la remet. Languettes : glisser haut / bas = deplacer tout de suite.
- Interruptions simultanees (variante B) : `DemandeCentrale` au telephone, cartes cote a cote avec leur texte, « Ignorer les deux ».
- Menu de l'accueil en admin (simule) : 11 outils accessibles a 320 px ; le bouton d'affichage a maintenant son nom.
A faire : libelles anglais « Change To AVENGER GIANT / TINY » dans le menu d'actions du heros (Ant-Man) ; deploiement sur demande.
