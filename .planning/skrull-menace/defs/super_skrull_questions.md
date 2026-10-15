# Super-Skrull / Kree-Skrull War — questions ouvertes (a poser a l'utilisateur)

Chemin des images : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/` + `Scenario Packs/Super-Skrull (Skrull Menace Expansion Content)/`
(sous-dossiers `Setup Cards`, `Superpower Deck`, `Encounter Cards`, `insert.png`) ou `Modular Sets/Kree-Skrull War (…)/`.
Pour chaque point : la lecture RETENUE est implementee et testee ; une autre lecture se change en quelques lignes.

## Q1 — Que devient un attachement SUPERPOWER DEFAUSSE (par un effet de carte) ?
- Cartes : sk117/118/119 (Reponse obligatoire), sk122-125. Exemple d'effet : « Feign Loyalty » de Lyja (defausse un attachement avec Action de heros).
- Phrase : « shuffle each SUPERPOWER attachment **from play** into the SUPERPOWER deck ». Rien ne dit ou va un pouvoir defausse.
- (Fait constate : quand le mechant avance de stade, ses attachements RESTENT attaches — regle native du moteur ; cas
  `sk117 Super-Skrull I — vaincu : le stade II herite des pouvoirs`.)
- Lectures : (a) il va a la defausse Rencontre et est PERDU pour la partie ; (b) il reste dans la defausse du paquet SUPERPOWER et revient au prochain remelange.
- **Retenu : (b)** — la defausse du paquet est rendue au paquet en meme temps que les attachements en jeu (sk117-119). Cas : `[super_skrull] sk119 … la defausse du paquet revient au paquet`.

## Q2 — Une ressource WILD compte-t-elle comme « physique » / « mentale » pour Hypnotic Gaze ?
- Carte : sk133 (`Image : Encounter Cards/19 hypnotic gaze.png`). « For each [physical] resource discarded this way stun…, for each [mental] resource … confuse… ».
- Lectures : (a) seules les icones physique / mentale comptent ; (b) un wild compte comme physique ET mentale.
- **Retenu : (a)** (lecture litterale ; le moteur officiel lit les ressources IMPRIMEES sans convertir le wild, ex. fne/60084). Mt'nox, lui, donne
  explicitement « wild = tout » : l'auteur sait ecrire cette convention quand il la veut. Cas : `sk133 … CONTRE-CAS energie + wild`.

## Q3 — Invisibility : « As an additional cost to attack Super-Skrull, you must spend 1 resource »
- Carte : sk123. Le moteur n'a de cout additionnel que pour le pouvoir de BASE de l'attaquant (`AdditionalCostToAttack`), pas pour « attaquer CETTE cible ».
- **Retenu** : le cout est exige a la DECLARATION de toute attaque contre le Super-Skrull (pouvoir de base ou carte), paye par le joueur de l'attaquant ;
  s'il ne peut pas payer, l'attaque est annulee (`SetBeInstead`, precedent 58027). Limite : l'attaquant s'est deja incline pour attaquer ; la regle
  officielle voudrait que l'attaque ne soit meme pas proposee. A confirmer en partie reelle.

## Q4 — Lord Kl'rt : la fleche de « Reveal the top card of the SUPERPOWER deck → discard this card »
- Carte : sk127 (`Encounter Cards/13 lord kl_rt.png`).
- Lectures : (a) reveler est le COUT, defausser Lord Kl'rt l'EFFET (le joueur « paie » un pouvoir de plus au mechant pour se debarrasser du titre) ;
  (b) l'inverse (peu plausible : on ne « defausse » pas comme cout une carte qu'on veut garder).
- **Retenu : (a)**. Consequence : paquet SUPERPOWER vide = cout impayable = l'Action n'est pas proposee.
- L'icone au centre de la boite de texte est l'**amplification** (croix + avion, convention NOTES.md du 15/10) : la transcription disait « icone de
  heros ». Implemente : cle desc `Amplify` = 1. Boost : l'etoile rouge seule (pas d'icone Y).

## Q5 — Heir to the Throne 2A : « Shuffle the encounter deck »
- Carte : sk121a. La phrase est separee de la recherche (« Otherwise, search … and attach it to Super-Skrull. Shuffle the encounter deck. »).
- **Retenu** : le deck Rencontre est melange dans LES DEUX branches (Lord Kl'rt deja en jeu : on distribue une carte face cachee a chaque joueur,
  puis on melange). L'autre lecture (melange seulement apres la recherche) change peu en jeu.

## Q6 — Earth Involvement (Permanent + Setup, crise conditionnelle)
- Carte : sk138. A 0 menace elle reste en jeu (Permanent : aucune capacite du set ne la defausse) sans icone de crise ; le texte dit seulement
  « cannot leave play » (insert p. 10). Menace de depart « 1 par joueur » (`StartingThreat 1*`, image).
- « A card that belongs to the Kree-Skrull War encounter set is **revealed** » : une carte mise en jeu par une recherche (Raksor appele par Bel-Dann) ou
  retournee comme carte de boost n'est PAS revelee ; leur effet ★ Boost (sk139/sk140) pose lui-meme 2 menaces. Retenu tel quel.

## Q7 — Pyrokinesis : « After a friendly character thwarts the main scheme, deal 1 damage to it »
- Carte : sk124. « friendly character » = heros ou allie d'un joueur ; « thwarts » sans exiger que de la menace soit effectivement retiree ;
  « it » = le personnage qui a contre ; degats normaux (pas indirects), donc Tough / Toughness les absorbent. Retenu tel quel.

## Q8 — Invisible Forcefield
- Carte : sk126. Seuil « at least 5 » identique en expert (rien d'imprime). « Highest printed hit points » compare les PV imprimes (le Super-Skrull porte
  14/16/19 par joueur) ; une copie suivante saute un ennemi qui en a deja une (cas teste : 2e copie sur Praxagora). Degats places en compteurs `damage`
  sur la carte (modele fne/60117). Aucune icone de boost imprimee (image). Retenu.

## Q9 — Badge ATK etoile seule de Rock Mimicry (sk125)
- Decision utilisateur du 15/10/2026 (NOTES.md) : marqueur « voir le texte », sans valeur chiffree. Aucune cle `ATK+` dans desc. Applique.

## Q10 — Textes FR : le texte d'ambiance (italique) des manigances n'est pas traduit
- Comme sk111 du scenario 1 (le champ EN `text` garde l'ambiance, le FR ne la reprend pas). A reprendre si l'utilisateur veut l'ambiance en francais.

## Non fait / a noter
- Pas de fichier `data/encounter_sets/sk_super_skrull.json` : les cartes du set Super-Skrull sont dans `encounters` des deux scenarios (comme `sk_skrull_empire`).
  Le livret dit que Army of Skrulls et Kree-Skrull War « peuvent etre retires de ce scenario / ajoutes a d'autres » : le set Kree-Skrull War est un
  fichier modulaire propre ; le set Super-Skrull, lui, n'est pas modulaire.
- Aucune adaptation du plateau React (`ui-app`) : le paquet SUPERPOWER n'a pas de zone dessinee (comme le paquet PLANET du scenario 1) ; les pouvoirs
  attaches au mechant s'affichent comme tout attachement du mechant.
