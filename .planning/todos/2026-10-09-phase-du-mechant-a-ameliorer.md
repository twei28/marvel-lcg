> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « MAQUETTE À FAIRE, pas codé » »). Preuve : Dépassée : refonte déployée le 05/10 (`397331a5`), essai « Étape par étape » retiré le 11/10 (`940a01ba` annulé par `7eb795d6`), schéma du 12/10, puis trois choix (« Guidée », « Plateau animé », « Accéléré ») déployés le 19/10 d'après `2026-10-19-restes-apres-deploiement.md` (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°19).

# Phase du méchant : refonte (50 questions le 09/10/2026, MAQUETTE À FAIRE, pas codé)

Origine : rapports 60, 61, 71 et 72 de Yarro. Les trois problèmes pèsent autant : enchaînement illisible (Surge,
annulations, remplacements), dégâts subis peu clairs, rythme trop rapide.

Préalable : le correctif des n°71/72 (cartes révélées en remplacement inscrites au journal, chaîne visible dans le
panneau) est livré AVANT la refonte, qui réutilise ses données moteur.

## Décisions
Rythme
- Pause sur CHAQUE carte, boosts compris (un par un, puis calcul final), avec un gros bouton Continuer en bas à droite
  (pleine largeur sur téléphone), Espace / Entrée sur PC. Pas de bouton pour accélérer.
- Pause aussi sur l'étape Menace (avant / après).
- En multijoueur, le joueur visé avance ; les autres voient la carte. Un fil par joueur, avec son nom.

Panneau
- On garde le panneau actuel, centré et déplaçable, avec ses onglets d'étapes ; on refait son contenu.
- Bouton « Réduire » qui garde une barre avec la carte en cours.
- Téléphone : feuille basse ~70 % de hauteur, réductible.
- Mode sobre : couleurs ternies du plateau, sans pulsation.
- Sons discrets : révélation, annulation, dégâts (réutiliser les sons existants si possible).

Fil (chaîne)
- PC : fil horizontal de vignettes avec flèches ; téléphone : fil vertical.
- Carte en cours en grand (~250 px) avec la traduction posée ; les précédentes en petites vignettes.
- Flèche = mot-clé traduit + source : « Renfort (Weapons Runner) », « révélée par Stepford Cuckoos ».
- Carte annulée : grisée, tampon « ANNULÉE », vignette de la carte qui annule.
- Perte d'une de tes cartes : ligne sous la carte qui la cause (« Stepford Cuckoos : dernier psi, défaussée »).
- Distribution : cartes face cachée avec le compte ; compteur « 2/3 » qui se met à jour avec la raison (+1 Surge).
- When Revealed : carte en grand + phrase qui résume l'effet, puis les choix.
- Résultat de chaque carte : ligne dans le fil (avant / après) ET bulles sur le plateau (-1 PV, +1 menace).
- Obligation : étiquette « Ton obligation ». Némésis : étape dédiée qui montre chaque carte du set.
- Nouvelle manigance annexe : mise en avant avec menace et icônes (Accélération, Crise...).
- Sbire qui entre en jeu : courte animation vers sa place + surbrillance (coupée en sobre).
- Péril : étiquette « Péril : décide seul », visible par tous.
- Deck rencontre remélangé : étape avec pause, « +1 accélération ».
- Effets simultanés : affichés côte à côte avec « Choisis l'ordre » quand la règle le permet.
- Danger : PV ou menace critiques en rouge pulsant dans le panneau.

Attaques
- Ordre actuel gardé (choix de défense comme aujourd'hui).
- Calcul posé avec les vignettes : attaque + chaque boost (icônes) − défense = dégâts ; effet ★ des boosts mis en avant ;
  ligne « Riposte » (Retaliate, Electrostatic Armor) dans le calcul.
- Sbires : même traitement que le méchant.

Interruptions
- Boutons texte actuels gardés, mais les jetons « [[energy]][[mental]][[physical]] » remplacés par les vraies icônes de
  ressources, texte traduit (défaut visible sur la capture du n°72).

Résumé de fin de phase
- Récap chiffré en haut + fil complet de la phase. Pas d'historique des phases précédentes.

Hors périmètre : la phase du joueur.

## Validation et livraison
- Maquette image d'abord : le cas de Yarro (Weapons Runner → Klaw's Vengeance annulée par Stepford → Sonic Boom) + une
  attaque de Klaw avec 2 boosts, PC et téléphone, normal et sobre.
- Essai réservé : interrupteur « Nouvelle phase du méchant (essai) » sur le compte de Yarro, posé depuis l'admin, retour à
  l'ancienne version possible. Ses retours passent par « Signaler un bug ».
- Puis déploiement pour tous après ta validation.
