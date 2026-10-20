# Galactic Storm, lot GS-0 : questions pour l'utilisateur (20/10/2026)

Une question par point douteux, recommandation en premier. Rien n'est tranché. Contexte : `docs/packs/galactic-storm/INVENTAIRE.md`,
`REGLES.md`, `transcriptions/`.

## Q1. Numérotation des cartes (card_id)

Les numéros imprimés ne forment pas une suite unique : plage 1 à 240 (jamais 305), 21 trous (31, 33-35, 40-48, 50-51, 71-75, 238),
et des collisions : les 17 cartes de Quasar portent toutes « 4 » (sauf Quantum Bubble, 49), Binary a « Pursued by the Flame » et
« Forgotten Life » en 4, et les némésis des deux héros partagent 237, 239, 240.
1. **(Recommandé) `gs` + numéro imprimé sur 3 chiffres (+ a/b), avec exceptions** : Quasar numéroté d'après le pied « n/16 » décalé
   de 300 (gs301 à gs316, gs349 pour Quantum Bubble), les trois némésis en collision suffixés `q`, les reskins Standard/Expert sans
   numéro sur 241-250. Change en jeu : rien ; un `card_id` stable et lisible comme `sk###`.
2. Ordre de lecture du livret (une suite 1 à N recalculée par nous) : propre, mais le numéro ne correspond plus au pied de carte, et
   les « solutions » des cartes intruses (81, 130, 139, 181/182) devraient être traduites.
3. Demander à l'auteur la liste officielle des 305 numéros : exact, mais bloque GS-1 et GS-2.

## Q2. 305 annoncées contre 319 trouvées

Le livret annonce 305 (109 joueur, 24 méchant, 172 rencontre) ; il y a 319 images de cartes (323 images au format carte moins 2 listes de
deck et 2 inserts). Le livret ne compte sans doute pas les 13 cartes de campagne (306) ni une carte ; non tranché.
1. **(Recommandé) Porter les 319 images, une par card_id distinct (259 cartes distinctes), et ne pas chercher à retrouver 305.** Change
   en jeu : rien, les cartes en trop sont des exemplaires.
2. Demander à l'auteur ce qu'il compte dans 305 : sûr, mais retarde.

## Q3. Exemplaires multiples au même numéro

Plusieurs cartes différentes de scénario portent le même numéro et le même texte (« Induced Mutation » 3/6 et 4/6 = 183 ; Doctor
Minerva 181 et 182 ; Threat on the Horizon 5/6 et 6/6 = 165 ; Kree Infantry 202 x4 ; Jailor of Chandilar 131 x4, etc.). Dans Skrull Menace :
un script, plusieurs copies dans le deck.
1. **(Recommandé) Un card_id par numéro imprimé, avec le nombre d'exemplaires du paquet** (comme Skrull Menace). Change en jeu : rien.
2. Un card_id par image : plus fidèle au fichier, mais des scripts dupliqués.

Cas particuliers à confirmer : « Doctor Minerva » 181 et 182 portent-ils le même texte ? « Kree Leader » 138A, 139A, 140A sont trois
stades distincts (OK). « Supreme Intelligence » 195, 196, 197 sont trois stades distincts (OK).

## Q4. « Forces Response » (Doctor Minerva 181/182, Captain Atlas 184)

Imprimé « Forces Response » au lieu de « Forced Response » (coquille probable). Même type de coquille : « completes » (Self-Destruct
Sequence 80B, The Endless Mind IIB), « highes » (Ronan 214).
1. **(Recommandé) Traiter comme « Forced Response » (la forme officielle), conserver la coquille dans la transcription.** Change en jeu :
   la capacité se déclenche et est obligatoire, comme sur toute carte officielle.
2. Reproduire la coquille à l'écran : pas de sens en jeu.

## Q5. Deux cartes dont le nom de fichier diffère du nom imprimé

« 21 War Academies of Hala » (z1) et « 20 War Academies of Hala » (z2) sont la carte « Mobilizing the Empire » (151) ; « Grip of
Annihilation » = « Death Grip » (85) ; « lair collapse protocol » = « Outpost Collapse Protocol » (87) ; « caught in their sights » =
« Caught in Its Sights » (89).1. **(Recommandé) Le nom imprimé fait foi, le nom de fichier est ignoré.** Change en jeu : rien.
2. Vérifier avec l'auteur : inutile, les images sont explicites.

## Q6. Lectures `[?]` qui changent une règle

Toutes les icônes de ressource sont marquées `[?]` (jamais nommées à vue). Trois cas changent le texte de jeu et doivent être tranchés
au début de chaque lot en regardant l'image carte par carte :
- **Étoile noire pleine `★` devant « Forced Response » / « Boost »** (Kree Sentry I, Araki, Supremor, Tanalth, etc.) : renvoi au
   texte du livret ou icône d'étoile (convention de Skrull Menace : renvoi au texte). 1. **(Recommandé) Convention Skrull Menace
   validée.** 2. Icône d'étoile de boost.
- **Étoile blanche à contour sous THW/ATK des alliés de campagne** (Rick Jones : deux étoiles à contour vide sous ATK ; Lauri-Ell : une
   étoile pleine près du 2) : dégâts consécutifs (convention de PROCESSUS-CARTE : `*` après un nombre = dégâts consécutifs). 1.
   **(Recommandé) Dégâts consécutifs.** 2. Autre sens.
- **Pastille orange à chiffre** (Rick Jones 5, Araki 4, Supremor 3 avec étoile, Doctor Pym 2, etc.) : valeur de menace d'une carte
   minion / points de vie ; non imprimée avec un libellé. 1. **(Recommandé) PV (points de vie) pour les alliés et sbires.** 2. Autre.
- **Icône rouge en Y en bas à droite** : icône de boost ordinaire (déjà validée dans Skrull Menace). Aucune question.
- Silhouette de personne noire après « HIT POINTS N » : « par joueur » (convention de PROCESSUS-CARTE). Aucune question.
- Quasar : « Quantum Bands » génère-t-elle une ressource de la couleur du choix de l'étoile noire quadrilobée ? Le livret FAQ p.22
  parle de « P » et « M » : ressource au choix du joueur parmi tous les types ? 1. **(Recommandé) Ressource « jocker » au choix de
  celui qui paie** (cohérent avec la FAQ). 2. Ressource fixe.

## Q7. Écarts livret 1.1 / 1.2 : lequel appliquer

Détail dans REGLES.md §16. Quatre écarts de règle : (a) Honorary suit l'identité et reste dans toutes les zones ; (b) Odd cards :
texte réécrit, carte d'exemple Ronan 214 disparue ; (c) Earth Under Siege : l'excès de dégâts va au méchant CHOISI par l'attaquant
(1.1 : le plus à gauche) ; (d) Scénario 5 : 1.2 donne des alliés par bonne Odd card et mélange toujours les deux Green Interference
(1.1 : retire de la menace de la Nega-Bomb, une seule Green Interference si deux bonnes réponses).
1. **(Recommandé) Appliquer le 1.2 partout** (version la plus récente, alignée sur les inserts de scénario). Change en jeu : voir (a)-(d).
2. Offrir les deux règles de la Nega-Bomb et des Odd cards en option : plus de code et de tests.
3. Appliquer le 1.1 : déconseillé.

## Q8. Les 10 « reskins Standard-Expert » d'Earth Under Siege

Advance (x2), Assault (x2), Caught Off Guard, Masterplan, Gang-Up, Under Fire, Shadow of the Past, Exhaustion sont des cartes de
l'ensemble Standard/Expert redessinées sans numéro imprimé. 1. **(Recommandé) Cartes de l'ensemble de rencontre propre à ce
scénario, nouveaux card_id (plage 241-250), même texte que les officielles Standard/Expert si identique.** Change en jeu : un
paquet Standard propre au scénario 4 plutôt que celui du moteur. 2. Réutiliser les officielles du moteur (recette reskin §11).

## Q9. Imperial Guard : retrait des cartes après victoire

Livret : « Remove each non-treachery card from the Imperial Guard set used in this scenario from the campaign » (scénarios 1 et 2,
absent aux scénarios 3 et 4 de l'insert). 1. **(Recommandé) Implémenter comme écrit : retrait aux scénarios 1 et 2 seulement.**
2. Retrait aussi au scénario 4 (Imperial Guard y figure dans l'encounter deck). Change en jeu : le nombre de cartes disponibles.

## Q10. Livrets 1.2 : « Q. to be added... »

Les FAQ des scénarios 3 et 5 sont vides dans le 1.2. 1. **(Recommandé) Ne rien inventer, noter les ambiguïtés (Hidden : cartes à
cibles multiples) dans des questions de lot.** 2. Demander à l'auteur.

## Q11. Rangement des quatre zips

Le cadrage propose de ranger les 4 zips dans `~/Desktop/Marvel LCG-contenu/kajislav/`. 1. **(Recommandé) Oui, déplacement par
l'utilisateur.** 2. Laisser à la racine du dépôt. Aucun effet en jeu.

---
## DÉCISIONS DE L'UTILISATEUR (20/10/2026)
- Q1 : `gs` + numéro imprimé sur 3 chiffres (+ a/b), avec exceptions : Quasar décalé de 300 d'après le pied « n/16 » (gs301 à gs316, gs349 pour Quantum Bubble), némésis en collision de Quasar suffixés `q`, reskins Standard/Expert sans numéro en gs241 à gs250.
- Q2 : porter les 319 images, sans chercher à retrouver 305.
- Q3 : un identifiant par numéro imprimé avec le nombre d'exemplaires du paquet (comme Skrull Menace).
- Q4 : « Forces Response » traité comme « Forced Response » (idem « completes », « highes » : coquilles).
- Q5 : le nom imprimé fait foi.
- Q6 : « ★ » = convention Skrull Menace ; étoile blanche à contour = dégâts consécutifs ; pastille orange = points de vie ; Quantum Bands = ressource joker au choix de celui qui paie.
- Q7 : livret 1.2 partout.
- Q8 : les 10 reskins Standard-Expert d'Earth Under Siege = cartes propres au scénario 4, identifiants gs241 à gs250.
- Q9 : Imperial Guard : retrait des cartes non-traîtrises aux scénarios 1 et 2 seulement, comme écrit.
- Q10 : ne rien inventer là où le livret est vide ; noter les ambiguïtés en questions de lot.
- Q11 : rangement des zips : laissé à l'utilisateur (sans effet en jeu).
