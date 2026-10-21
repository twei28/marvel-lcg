# Mode manuel 100 % identique à OCTGN, et rangement des cartes posées (07/10/2026)

**Statut : FAIT le 07/10/2026 (non déployé).** Demande de l'utilisateur : « Je veux qu'en manuel ce soit 100 % identique. Par contre, il faut trouver un moyen d'aussi pouvoir déplacer les cartes après qu'elles soient posées pour changer l'ordre, que ce soit les alliés, les sbires, les manigances ou les améliorations, et pouvoir aussi choisir que ce soit à gauche ou à droite. »

Référence : `definition.xml` et `actions.py` du dépôt Ouroboros009/OCTGN-Marvel-Champions (voir la mémoire raccourcis-octgn-source). Audit du 07/10 : l'aide du manuel est fidèle au code ; écarts listés ci-dessous.

## Décidé (questions une à une)

- Portée : TOUT. Écarts existants + ciblage + surlignage + multi-sélection + le reste.
- ↑ ↓ sur allié et sbire : comme OCTGN, ↑ = +1 dégât, ↓ = −1 dégât (aujourd'hui ↑ soigne). Héros et méchant : ↑ = +1 PV (inchangé, déjà comme OCTGN).
- Réordonner en manuel : glisser SIMPLE dans la même rangée (lâchée entre deux cartes de sa rangée, elle s'y range ; ailleurs, déplacement comme aujourd'hui). Alt + glisser marche aussi.
- Amélioration glissée sans Alt tout près de son personnage : change de côté ou de rang et reste attachée ; plus loin, déplacement comme aujourd'hui.

## Lots

1. Écarts existants : carte boost FACE CACHÉE à côté du méchant (`villainBoost`) ; ↑↓ allié/sbire = dégâts ; Suppr refuse une carte Permanent et envoie une carte « Victoire X » à la pile de victoire.
2. Rangement en manuel au glisser simple (rangées et améliorations, côté compris).
3. Ciblage : Maj+clic cibler / décibler, Échap décible tout, Maj+glisser d'une carte vers une autre = flèche.
4. Surlignage de couleur au pavé numérique (1 bleu, 2 orange, 3 vert, 4 violet, 5 rouge, 6 noir, 7 blanc, 0 retire).
5. Multi-sélection : Ctrl+clic, rectangle de sélection sur une zone vide ; les gestes s'appliquent à la sélection.
6. Le reste : Ctrl+I (fiche de la carte), Ctrl+A (méchant actif), Ctrl+H (charger un héros), F8 (prendre le contrôle des cartes communes), sauvegarde / chargement d'un état de table.

Chaque lot : tests, vérification au navigateur, aide du manuel mise à jour, commit. Rien n'est déployé sans « déploie ».

## Avancement

- Lot 1 : FAIT (a6370398), vérifié en vrai sauf le chemin « Victoire » (tests seulement).
- Lot 2 : FAIT (4a15c9a8), vérifié en vrai le 07/10 (allié rangé au glisser simple dans sa rangée, amélioration passée à gauche de son héros).
- Lots 3 et 4 : FAITS (8a88b772), vérifiés en vrai.
- Lot 6, étudié le 07/10 (source OCTGN lue) :
  - À FAIRE : Ctrl+I (aperçu fixe de la carte, mots-clés) ; Ctrl+A (méchant actif = surlignage « actif », après le lot 4, repère visuel seulement) ; confirmation de « Remélanger la défausse dans le deck » si le deck n'est pas vide ; entrées directes « Sous le deck du héros » et « Sous le deck Rencontre » ; « Tout envoyer dans le deck Rencontre » (mélanger / dessus / dessous) en UNE commande (un seul Ctrl+Z) ; « Choisir un set et le mélanger dans le deck Rencontre » (set de chaque carte à vérifier dans le monde) ; vérifier que « Sauver » reste offert en manuel et qu'une sauvegarde faite en manuel se recharge.
  - SANS OBJET, à dire dans l'aide : Ctrl+H et Ctrl+V sur la table (OCTGN les refuse dès que des cartes sont chargées ; chez nous la préparation le fait), F8 (contrôle des cartes propre à OCTGN), F10 / molette / Espace (pas de caméra libre), Get Position et Toggle Debug (outils de développeur OCTGN).
- Lot 5 : FAIT, vérifié en vrai (`ui-check/tests/zz-manuel-lots56.spec.ts`, moteur d'essai) : Ctrl+clic, rectangle sur la table vide, clic vide qui vide la sélection, F7 / double-clic / menu / glisser valent pour toute la sélection en UNE commande (lignes jointes, `triche.enLot`) donc un seul Ctrl+Z, vérifié. Sélection locale (comme OCTGN), cadre en pointillés jaunes distinct du ciblage et du surlignage.
- Lot 6 : FAIT, vérifié en vrai : Ctrl+I (fiche fixe, Échap ou clic ferme), Ctrl+A (méchant actif, surlignage vert `ActiveColour` #82FA58), « Sous le deck du héros / Rencontre » au menu de carte, confirmation du remélange de la défausse quand le deck n'est pas vide (défaut trouvé et corrigé : la question s'ouvrait DERRIÈRE la fenêtre de la pile), « Mis de côté : tout dans / sur / sous le deck Rencontre » au menu de la table (une commande, confirmation ; pas vu en vrai faute de carte mise de côté dans la partie d'essai), « Sauver » offert en manuel et une sauvegarde manuelle se recharge à l'identique, gestes groupés compris. Section « Sans objet ici » dans l'aide.
- NON FAIT : « Choisir un set et le mélanger dans le deck Rencontre » : le monde ne donne pas le set de chaque carte (`WorldCard` n'a ni set ni pack). Il faudrait l'exposer côté moteur.

- « Choisir un set et le mélanger dans le deck Rencontre » : FAIT le 07/10 (set lu dans le catalogue, `set_name` de cards.json, pas de changement moteur), une entrée par set dans le menu de la table, confirmation, une seule commande. Tests unitaires seulement : aucune carte mise de côté dans la partie d'essai pour le voir en vrai.

## Reste à vérifier (backlog item 4, relu le 21/10/2026 au soir)

Table éclatée et carte à deux faces (Rhino) : **OK**, `ui-check/tests/mode-manuel.spec.ts` rejoué en vrai contre un serveur local, cas vert. Le chemin « Victoire » : **OK**, même fichier, cas vert.

**Un vrai défaut trouvé en rejouant la suite** (pas lié à une modification de cette session) : le cas « mise en pause PENDANT une question ouverte (le mulligan), geste manuel, et la reprise repose cette même question » échoue de façon reproductible (2/2) — un dégât appliqué via le menu triche PENDANT la pause (mulligan en cours) n'est jamais publié à l'écran : la pastille de vie reste à sa valeur de départ (`10 / 10` au lieu de `7 / 10` attendu), timeout de 30 s sur l'attente du changement. Aucun commit récent sur `sandbox_command` ou le mécanisme de pause ne l'explique ; cause non recherchée plus loin faute de temps en fin de session.

**ABANDONNÉ le 21/10/2026 au soir** : jugé par l'utilisateur trop précis/pointu pour mériter d'être suivi. Retiré du backlog (item 4, `docs/rapports/etat-du-backlog-2026-10-21.md`). Non corrigé, non recherché davantage.
