# Questions de conception ouvertes — corrections « Sur la table » du 19/10/2026

Chaque point : ce que j'ai vu, les options, ma recommandation. Rien n'est tranché à ta place.

## Q1 (T3) — « l'ordre de la table » pour les sbires : gauche → droite, ou l'ordre du moteur ?
Vu : le moteur liste les sbires engagés du PLUS RÉCENT au plus ancien, ce qui donne, à l'écran, l'ordre DROITE → GAUCHE
(mesuré : 6 sbires, x = 932, 839, 746, 654, 561, 468). Le bouton « Garder l'ordre de la table » clique les sbires de GAUCHE
à DROITE (le sens de lecture de la rangée).
Options : (a) gauche → droite (actuel) ; (b) ordre du moteur (le plus récent d'abord, donc de droite à gauche) ;
(c) ordre d'engagement (le plus ancien d'abord) = ce que beaucoup de joueurs font à la main.
Recommandation : (a), c'est ce que « l'ordre de la rangée » veut dire à l'œil ; (c) si tu préfères la convention des
joueurs. Pour Bebop et Rocksteady : le moteur pose une question à choix unique (« quel méchant d'abord ? »), un seul clic
déjà, donc pas de bouton « garder l'ordre ».

## Q2 (T2) — le bandeau se pose à GAUCHE par défaut : il cache la pile Rencontre
Vu : en colonne contre le bord gauche, il ne recouvre plus l'aperçu agrandi ni les cartes lues au centre (recouvrement
mesuré 593 à 4619 px² avant, 0 après), mais il passe sur la pile du deck Rencontre (haut gauche), d'où partent les cartes
lues. Il se déplace à la poignée.
Options : (a) garder à gauche ; (b) à droite quand l'aperçu n'est pas affiché (mais l'aperçu est ancré à droite) ;
(c) à gauche mais sous la pile Rencontre (≈ 205 px du haut), au prix d'une colonne plus courte.
Recommandation : (a), la pile Rencontre n'a pas besoin d'être cliquée pendant la phase.

## Q3 (T6) — le bouton de Bodyguard (Yōjimbō, se011) s'appelle « Interruption de héros »
Vu : la défense est bien proposée et désigne le héros (DÉF 2 retranchée), mais le bouton porte le TYPE de la capacité,
pas son nom, parce que le moteur ne nomme pas l'option. Le bandeau dit « Ne pas utiliser Yōjimbō ».
Options : (a) laisser ; (b) afficher « Yōjimbō — Interruption de héros » (nom de la carte porteuse devant, comme pour les
améliorations) ; (c) lire « Bodyguard » dans le texte de la carte.
Recommandation : (b), simple et exact.

## Q4 (T6) — Draw Their Fire (53011) n'est jamais proposée dans ma reproduction
Vu : Falcon équipé de la carte ; au début de la phase du méchant le moteur n'ouvre aucune fenêtre de réponse (journal
moteur : « Phase : Villain » puis « Étape de la manigance principale » directement). Ce n'est pas le plateau.
Options : (a) la jouer à la main avant la phase pour voir si le problème vient de `PutIntoPlay` du harnais ; (b) lancer un
cas moteur dédié (`tools/test_capacites.py`) ; (c) laisser.
Recommandation : (b) dans une session moteur.

## Q5 (T11) — règles cachées : Tenace
J'ai ajouté une ligne « Tenace : défaussé à la place des dégâts » (le moteur publie `robuste`), en plus des quatre que tu
as listées. Tu veux la garder ? Options : garder / retirer.
Recommandation : garder.
