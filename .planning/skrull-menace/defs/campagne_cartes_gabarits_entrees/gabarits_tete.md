# Cartes de campagne (sk263-sk289b) — gabarits PROCESSUS-CARTE

Un gabarit par card_id (26 cartes numerotees + le rappel sans numero sk289a / sk289b), rempli avec les resultats REELS du
15/10/2026 : cas `tools/cas/campagne_cartes.py` (110), substitution du bloc (module remplace par `GetAbilities -> []`, empreinte
du dossier identique avant/apres), autoplay du deck `campagne` (26 cartes) et d'un temoin, cas plateau, passes statiques.
Fichier genere par `defs/generer_gabarits_campagne_cartes.py` ; ne pas editer a la main.

## Rappel commun

- **Lecture de la substitution** : « rouges N/M » = N cas sur M tombent sans le module. Les M-N verts restants sont tous soit
  des TEMOINS d'ABSENCE d'effet (restent verts par construction, assume ici), soit des valeurs NATIVES lues dans `desc`
  (Toughness de sk265, icone Acceleration de sk271, Temporary de sk284/sk285), soit le TEMOIN POSITIF d'une restriction (sk275 :
  l'allie SKRULL a le droit de deplacer la menace ; sk281 : jouable avec un allie SKRULL) dont la restriction est prouvee rouge
  par les autres cas. Aucun cas NOMINAL de capacite ne reste vert sans module (liste complete dans la ligne « Substitution »).
- **Alliance de sk280** : le cas est vert sans module (le cout y vaut 0) ; la preuve est une MUTATION (la ligne
  `jouer.cout_en_groupe = True` retiree : le cas passe au ROUGE, remise : VERT), consignee ici et dans `RECETTES-MOTEUR §7octodecies`.
- **Autoplay** (deck `campagne` : Spider-Man + les 26 cartes, 8 parties par scenario, scenarios `rhino`, `sk_paibok`,
  `sk_super_skrull`, `sk_skrull_empire`, temoin `spider_man` de depart) : voir le resume en fin de fichier ; 0 trace
  `Traceback`/`NameError`/`AttributeError`/`TypeError`/`KeyError`/`AssertionError` apres le correctif de `player_action.py`
  (un plantage reel trouve par l'autoplay : sk288, voir `defs/campagne_cartes_moteur.md`). La phase du mechant SAUTEE par sk280
  s'est vue dans 6 parties (journal « --- Phase : Villain (skipped) ---»).
- **Passes statiques** : `verifier_appels_modules` OK (calibre : il a attrape `Message.AfterPlayerEngageMinion n'existe pas`
  dans sk286 avant correction), `verifier_api_cartes` : aucune faute dans skrull_menace.
- **Ce que ces blocs ne voient pas** : une vraie partie jouee par un humain dans le navigateur n'a pas ete faite (aucun outil
  de ce depot ne pilote un navigateur ici). A faire en partie reelle : le texte des cartes a l'ecran (X du cout de Buddy Training
  et de Princess Anelle affiche), les invites de reponse optionnelle, le choix de cible de Xavin (premiere cible legale),
  et la Cooperation Area (autre bloc) qui n'existe pas encore.
