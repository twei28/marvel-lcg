# Une « façon de jouer » : Automatique ou Manuel (gestes OCTGN) : décisions du 05/10/2026

Demande de l'utilisateur : proposer le jeu comme une autre manière de jouer, au même titre que les
styles (sombre, etc.), façon OCTGN. Le mode manuel (déployé le 22/09) et la pause existent déjà ;
la pause est jugée « pas une bonne version ».

## Décisions (questions une à une)

- La pause disparaît comme idée : elle devient un INTERRUPTEUR « Auto / Manuel » toujours visible
  dans la barre (nom et emplacement jugés mauvais).
- Partie commencée en auto : Manuel s'allume, on joue ; Auto recalcule toute la table et le moteur
  continue exactement à sa question.
- Partie commencée en manuel : la mise en place est faite par le moteur (comme aujourd'hui, puis il se
  tait). Au premier clic sur Auto, une fenêtre demande « On en est où ? » (phase héros, phase méchant,
  nouveau tour) ; le moteur recalcule la table et reprend là.
- Choix au départ : dans le lanceur (par partie) ET dans les Réglages (valeur par défaut).
- Gestes : ceux d'OCTGN S'AJOUTENT aux nôtres (Q, F, R, chiffres), pas de remplacement.
  *06/10/2026 : non tenu, `5b88d9a2` a retiré F, Q, R et les chiffres sur une carte sans décision
  tracée. Question 10 de `2026-10-06-mode-manuel-comme-octgn.md`.*
- Gestes OCTGN à reprendre (source : marvelchampionsmonthly.podbean.com) : double-clic sur une carte
  joueur = incliner ; double-clic sur le méchant = carte d'amplification ; flèches haut/bas = +/-1 dégât ;
  flèches droite/gauche = +/-1 jeton générique ; Suppr = défausse appropriée ; F12 = change de phase
  (simple repère, rien n'est joué) ; clic droit sur la table = charger héros / méchant, vaincre le stade
  (charge le suivant), manigance terminée (charge la suivante).
  *06/10/2026 : source à jour = plugin Ouroboros009 0.0.3.97. Haut/Bas agissent sur les PV d'une
  identité ou d'un méchant et sur la menace d'une manigance ; F12 redresse et pioche
  (`CoucheTriche.tsx:569-603`), ce n'est plus un simple repère.*
- Multijoueur : tout joueur peut passer la table en manuel, pour tout le monde, avec un bandeau qui dit
  qui l'a fait ; chacun peut remettre Auto.
  *06/10/2026 : le bandeau a été retiré par `329daedc` ; `pause_par` est publié mais plus affiché
  (`ui-app/src/board/world.ts:597`).*
- Onglet d'aide (demande du même jour) : en passant en manuel, un onglet s'ouvre à droite, comme celui du
  journal, et liste les raccourcis (OCTGN et nôtres). Choix pris sans question : il s'ouvre tout seul au
  passage en manuel, se ferme à la main, et se rouvre par un bouton tant qu'on est en manuel.

## À trancher en cours de route

- La spec du manuel disait « aucun repère de phase » : F12 en ajoute un. Mettre à jour la spec.
- Recalcul de la table au retour en Auto : à étudier côté moteur (modificateurs perdus en manuel,
  `manuel_actif`, déclencheurs fermés).
- Charger un deck par URL MarvelCDB (OCTGN le fait) : non demandé, non cadré.

## Avancement (05/10/2026, soir)

FAIT et commité (branche `mode-manuel`, non déployé) :
- Interrupteur Auto / Manuel, fenêtre « On en est où ? », bandeau, onglet d'aide à droite.
- Choix au lanceur (`facon-de-jouer.js`) et défaut dans les Réglages.
- Gestes OCTGN : flèches, Suppr, double-clic, recherche dans tout le catalogue (C).
- Côté méchant : clic droit sur la table = « Vaincre ce stade » (`Puzzle.AdvanceVillain`, cas A5 manuel)
  et « Manigance terminée » (`Puzzle.AdvanceMainScheme`).

VOLONTAIREMENT NON FAIT :
- F12 (repère de phase) : rien n'est joué, aucune valeur pour le joueur ; la spec « aucun repère de
  phase » reste donc exacte.
  *06/10/2026 : dépassé, F12 a été fait la nuit du 05/10 (`5b88d9a2`).*
- « Charger héros / méchant » : déjà couvert par « Faire apparaître une carte » (catalogue complet).

RESTE : reprise en Auto côté moteur (`POST /manuel_reprise`, travail d'un agent séparé en cours), preuve
que l'Auto tient compte des modifs manuelles, table éclatée en vraie partie, entrée « nouveautés »,
déploiement seulement sur « déploie ».

## Avancement (05/10/2026, nuit) et suite (06/10/2026)

- Nuit du 05/10 (`5b88d9a2`, déployé) : F7, Ctrl+F, F3/F4/F5, Alt+S/C/T et Ctrl+Alt, flèches par type
  de carte, Suppr, Ctrl+Q, F12, double-clic OCTGN, remélange de la défausse, aide réécrite. F, Q, R et
  les chiffres sur une carte retirés.
- 06/10 : l'utilisateur ne peut pas poser une carte de sa main par glisser. Audit, spec, plan et
  14 questions ouvertes : `.planning/todos/2026-10-06-mode-manuel-comme-octgn.md`.
