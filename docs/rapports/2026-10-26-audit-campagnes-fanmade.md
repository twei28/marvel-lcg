# Audit des campagnes fan-made fournies en zip (26/10/2026)

Lecture seule : aucun code ni donnée du jeu n'a été touché. Source : les 19 zips datés des 24 et 25/10/2026 à la racine du dépôt. Les livrets ont été lus à l'écran (ce sont des images ou des PDF sans texte).

## 1. Combien de campagnes ?

**Trois**, et seulement trois. Les 16 autres zips sont des packs de héros ou de scénario isolé : Alien vs Predator, Batgirl, Batman, Lady Deathstrike, New Ultimate Winter Soldier, Predator, Roz, Shang-Chi, She-Hulk (EN et FR), Silver Surfer, Spider-Punisher, The Vault, The Warriors Three, U.S. Agent, Wasp. Aucun ne contient de livret de campagne, de carnet ou de scénarios en chaîne (j'ai vérifié les listes de fichiers de chacun).

| | Hellfire Hunt | Hydra Unleashed | Schemes of the Shi'ar |
|---|---|---|---|
| Où | zip « Hellfire Hunt Campaign » | zip « Hydra Unleashed » | dossier « Schemes of the Shi'ar Campaign (WIP) » **dans** le zip Starjammers |
| Fichiers | 294 | 421 | 192 |
| Auteur | Dipsome | Lord Havok | Phenexian et Mysteltainn (équipe Starjammers) |
| Statut | **complète** | **complète**, mais FAQ vide (modèle non rempli) | **WIP** (« work in progress » dans le nom) |
| Livret de règles | oui, PDF de 24 pages | oui, 27 pages en images | **non** |
| Carnet de campagne | oui (pages 18-19) | oui (page 24) | **non** |
| Scénarios | 5 (White Queen, Black Queen, Cassandra Nova, Torn, Black King) | 5 + 3 interludes « .5 » = 8 | 3 (Erik the Red, Gladiator, Deathbird) |
| Cartes (selon le livret / le décompte des fichiers) | 371 : 113 cartes joueur, 24 vilains, 234 rencontre | 385 | environ 189 cartes de rencontre |
| Enchaînement | linéaire : il faut gagner 1 à 5 dans l'ordre ; en cas de défaite on rejoue sans pénalité | **à embranchements** : une défaite mène à un scénario « .5 », deux défaites de suite = fin de partie ; seul le n°5 clôt la campagne | inconnu : aucun livret |

## 2. Hellfire Hunt (Dipsome)

**Contenu.** 5 scénarios, 9 modules (Darkhold, Hellfire Conclave, Immensity, Mind Control, Mutant Extinction Agenda, Negasonic Teenager Warhead, Perfection, Psionic Delusion, Sebastian Shaw), 16 alliés de campagne, 12 side schemes d'alliés potentiels, 8 cartes de campagne, 15 cartes d'aspect de campagne (cartes 263-288 dans le livret : « Basic / Campaign »), et les héros **Sunspot** et **Marvel Girl (Rachel Summers)**, avec leurs decklists page 18.

**Héros requis : déjà portés.** `sunspot-hellfire` (so) et `rachel_summers` (rm) existent dans le jeu. À revérifier : le pack de héros du zip Hellfire Hunt a ses propres cartes d'aspect (15), distinctes de celles qu'on a déjà.

**Mécaniques.**
- **Déjà connues du moteur** (fiches dans `docs/reference/mots-cles/`) : Guard, Hinder, Incite, Patrol, Permanent, Piercing, Ranged, Setup, Stalwart, Steady, Team-Up, Temporary, Victory, Villainous, Armored, Amplify. Le livret cite aussi la campagne **Skrull Menace**, déjà dans le jeu (`data/campagnes/skrull_menace.json`).
- **Inédites** :
  1. **Vilain à deux faces qui change de forme** (White Queen : PSIONIC / DIAMOND) sans remise à zéro de ses PV ; « incite 1 » à chaque retour en forme PSIONIC.
  2. **Deck « Potential Ally »** : 12 side schemes mélangés au deck de rencontre ; en gagner un recrute l'allié.
  3. **Deck « Recruited Mutants »** à côté de l'environnement *Xavier's Institute*, qui se vide et se remélange tout seul, et dont l'allié se joue par une Action de l'environnement.
  4. **Carnet** : identités, alliés « Recruited » notés entre scénarios, et en mode expert **PV restants persistants** d'un scénario au suivant (avec possibilité de les restaurer en posant un jeton d'accélération).
  5. Cartes **de campagne** réservées (ne comptent pas dans la taille du deck).
- Les cinq pages de scénario n'ont pas toutes été lues en détail (j'ai lu la page 8, White Queen) : il peut y avoir 1 ou 2 mécaniques propres à chaque vilain en plus.

**Effort estimé.** 5 scénarios (+ version expert), 1 fichier de campagne dans `data/campagnes/`, et environ **300 cartes à porter** via `PROCESSUS-CARTE.md` (234 de rencontre + 24 vilains + une cinquantaine de cartes joueur nouvelles : 15 aspects, 26 de campagne, alliés). Le moteur de carnet couvre déjà le principe ; **3 extensions** probables : forme de vilain avec PV conservés, deux decks annexes (Potential Ally / Recruited), PV persistants du mode expert. Les 15 campagnes déjà présentes sont de taille comparable (7 à 16 Ko de JSON chacune).

## 3. Hydra Unleashed (Lord Havok)

**Contenu.** 8 scénarios : 1 Blitzkrieg, 1.5 Escape to the Future, 2 The Six Heads of the Hydra, 2.5 The Viper Strikes, 3 Power Vacuum, 3.5 The Enemy of my Enemy, 4 Red Reign, 5 Prophecy Fulfilled. Plus 74 cartes « Campaign Files » : 15 alliés, 8 alliés et améliorations S.H.I.E.L.D., 8 améliorations, 4 événements, 7 modulaires Standard, ressources, le côté-scheme *The Prophecy*, la pièce *Fang of the Hydra*. Le livret a 27 pages (règles, chronologie, un scénario par page ou double page, FAQ, carnet, decklists).

**Héros requis.** Deux héros précombinés : **U.S. Agent** (déjà porté, pack `us-agent`) et **Mockingbird**, qui **n'existe pas** dans le jeu (seulement l'allié `01083`/`04004`). Le zip ne contient **aucune carte** de Mockingbird (seulement sa decklist page 25) : il faut donc un autre zip ou des scans.

**Mécaniques inédites (nombreuses).**
- **Mots-clés absents du moteur** (aucune fiche) : **Civilians X** (jetons de civils sur un side scheme), **Heroic**, **Sniper X**, **Zealot**, **Mercenary** (capacité qui retourne un sbire en allié). Déjà connus : Agile, Armored, Guard, Hinder, Incite, Multiverse, Patrol, Permanent, Surge, Victory, Villainous, Vulnerable.
- **Scénario 1** : deux environnements « Rescued Civilians » et « Casualties of War » ; on gagne en ayant plus de jetons sur le premier.
- **Scénario 2** : **six vilains en jeu**, dont X = joueurs + 1 sont face visible, un jeton d'activation qui passe de vilain en vilain, schème associé qui reste actif quand le vilain se retourne. Voir la fiche `mechants-multiples.md`.
- **Scénario 3** : **le vilain est un sbire** pioché dans le deck de rencontre, avec « Wannabe Leader », PV recalculés (+10 par joueur), liste de mots-clés ignorés et de sbires incompatibles ; stades de vilain recalés.
- **Scénario 4** : un **deck de Lieutenants** avec sa propre défausse ; alliés « Captive ».
- **Scénario 5** : **Hydra God, un vilain en six cartes** (torse + 5 têtes) avec côtés ATTACKING / DECAPITATED, un **dé à 6 faces** qui désigne le vilain actif, le torse invulnérable tant qu'une tête attaque.
- **Campagne** : embranchements victoire/défaite, points d'expérience dépensés dans un « S.H.I.E.L.D. Warehouse », 4 améliorations d'entraînement gagnées ou perdues, case « The Prophecy found ».
- **Attention** : le dé à 6 faces est un hasard de plus que le moteur n'a peut-être pas (à vérifier).

**Effort estimé.** Le plus lourd des trois : 8 scénarios + versions expert, **385 cartes**, un héros à créer (Mockingbird, matériel manquant), **5 mots-clés à documenter puis coder**, et au moins **4 extensions moteur** (six vilains simultanés avec jeton d'activation, vilain issu du deck de rencontre, deck de Lieutenants, vilain à six cartes avec dé). Risque moteur élevé.

## 4. Schemes of the Shi'ar (WIP, équipe Starjammers)

**Contenu.** Trois « packs de scénario » (une image de couverture chacun, pas de livret) : Erik the Red (27 cartes de rencontre + modulaires Kin Crimson 7 cartes et Shi'ar Strike Force 8), Gladiator (17 + modulaire Imperial Guard 26 + 60 cartes de modulaires d'élite : Fang, Titan, Mentor, Smasher, Electron, Warstar, Oracle, Starbolt), Deathbird (34 + modulaire Fraternity of Raptors 10).

**Manque.** Pas de livret, pas de texte de mise en place, pas de règle de victoire, pas de carnet : tout ce qui fait la **campagne** manque. Seules les cartes existent. Les scénarios peuvent donc au mieux se jouer **isolés**, en devinant la mise en place d'après les cartes de manigance principale (« Main Scheme 1A/1B »).

**Héros requis.** Les Starjammers, déjà portés : `corsair`, `hepzibah`, `raza`, `chod`, `rachel_summers`, `smasher`. **Dépendance** : les 50 cartes d'aspect Starjammers (voir le zip Starjammers, dossier « Aspect and Basic Cards ») ne sont pas encore dans le jeu. Elles sont le pool de decks naturel pour ces scénarios. Le sbire Smasher des modulaires d'élite est le même personnage que le héros Smasher (à vérifier si le héros du jeu peut en être l'allié sans conflit).

**Mécaniques.** Non lues (aucun texte de règle). Cartes à ploys numérotés (« Ploy 1 » à « Ploy 10 ») chez Erik the Red, vilains à 3 stades à chaque scénario, côtés « Atavistic Wings grounded / aerial » chez Deathbird (le trait AERIAL est déjà couvert par le pack Spider-Punisher).

**Effort estimé.** Environ 190 cartes à porter, 3 scénarios (+ expert à préciser), pas de fichier de campagne tant que l'auteur n'a pas livré le livret. Risque moteur : faible à moyen, à confirmer carte par carte.

## 5. Ordre recommandé

1. **Les 50 cartes d'aspect Starjammers** (déjà demandées) : elles débloquent le décor de la campagne Shi'ar et complètent les héros du même zip.
2. **Hellfire Hunt** : matériel complet (livret, carnet, 5 scénarios, décklists), les deux héros sont déjà dans le jeu, la plupart des mots-clés existent, enchaînement linéaire sans embranchement. Risque moteur moyen : trois extensions bien délimitées. C'est la campagne fan-made la plus proche d'être jouable.
3. **Shi'ar, scénarios seulement** : une fois les aspects posés, les trois scénarios peuvent se porter comme des scénarios isolés (même démarche que *The Vault*), sans attendre le livret. La partie « campagne » attend l'auteur.
4. **Hydra Unleashed en dernier** : la plus grosse, la plus risquée pour le moteur (six vilains simultanés, vilain-sbire, vilain à six cartes, dé), avec un héros dont le zip ne contient pas les cartes. Elle gagne à venir après les deux autres, qui auront déjà rodé les extensions de carnet.

Raison de fond : on avance du moins risqué au plus risqué, et chaque étape prépare la suivante (decks d'aspect pour Shi'ar, carnet à embranchements pour Hydra).

## 6. Questions réelles à poser

Aucune question que les livrets ou les règles tranchent. Ne restent que les manques de matériel et un choix de périmètre :

1. **Mockingbird** (héros d'Hydra Unleashed) : avez-vous le zip du héros (scans ou cartes) ? Sans lui, Hydra Unleashed se joue avec U.S. Agent seul et le héros reste à ajouter plus tard.
2. **Schemes of the Shi'ar** : l'auteur a-t-il fourni (ou fournira-t-il) un livret, des textes de mise en place et un carnet ? Sinon, on porte les trois scénarios en parties isolées, sans mode campagne.
3. **Hydra Unleashed, FAQ** : la page 23 du livret est un gabarit vide. Faut-il écrire des arbitrages maison à mesure qu'on joue, ou attendre une version corrigée de l'auteur ?
4. **Dé à 6 faces** (Hydra God, scénario 5) : le jeu accepte-t-il une carte qui tire un résultat de dé ? Si le moteur n'a pas ce hasard, souhaitez-vous qu'on l'ajoute pour cette seule carte ?

## 7. Ce que je n'ai pas fait

- Je n'ai pas lu chaque page de scénario des 8 + 5 livrets : j'ai lu l'introduction, les mots-clés, les règles de campagne, le carnet, les decklists, et la première page d'au moins un scénario de chaque campagne (Hydra : 1, 2, 3, 4, 5 ; Hellfire : White Queen). Les autres scénarios Hellfire (Black Queen, Cassandra Nova, Torn, Black King) restent à lire avant de coder.
- Je n'ai pas ouvert chacune des ~1 000 images de cartes : les nombres de cartes viennent des listes de fichiers et des chiffres imprimés dans les livrets.
- Je n'ai rien extrait dans le dépôt ; mes notes et images de travail sont dans le dossier temporaire de la session.

## 8. Décisions de l'utilisateur (26/10/2026)

- **Schemes of the Shi'ar : abandonnée pour l'instant.** On ne fait que les campagnes COMPLÈTES (livret + carnet). Les cartes d'aspect Starjammers restent à faire (héros), pas les trois scénarios Shi'ar.
- **Un héros manquant n'est pas bloquant** : Hydra Unleashed se fait sans Mockingbird (U.S. Agent seul), le héros s'ajoutera plus tard si le zip arrive. Les questions 1 et 2 du §6 sont donc closes.
- **Ordre retenu :** 1. cartes d'aspect Starjammers (en cours), 2. Hellfire Hunt, 3. Hydra Unleashed. Restent ouvertes : FAQ vide d'Hydra (§6 n°3) et dé à 6 faces (§6 n°4).
- **Les deux campagnes (Hellfire Hunt puis Hydra Unleashed) seront faites.** Mockingbird : à chercher et à faire si le temps le permet, sans bloquer Hydra.
- **Dé à 6 faces (Hydra God, scénario 5) : décision.** Un randomizer cliquable, avec un vrai petit D6 animé (il roule un peu) qui montre le résultat. Question §6 n°4 close. À prévoir côté interface (`ui-app`) + côté moteur (tirage 1 à 6 stocké dans l'état, pour que la partie reste rejouable et multijoueur).
- **Hydra Unleashed, FAQ vide : tant pis.** Pas d'attente de l'auteur ; les doutes se tranchent par les règles et les livrets, comme pour les autres packs. Question §6 n°3 close : plus aucune question ouverte sur les campagnes.
