# TMNT Shinobi : réponses de l'utilisateur (17/10/2026)

Réponses données une à une (choix multiple, scan montré avant). « À APPLIQUER » = pas encore reporté dans le code.

## Socle et Paths
- Q-S1 Kagemusha : **« Shadow Stride » (scan)**. Rien à changer (provisoire = scan). A appliquer : lever « NON terminée » de se001.
- Q-S2 Shihan Recenter : **Taijutsu + Dual Kuji-Kiri/Ninjutsu** (PAS la lecture provisoire). A APPLIQUER : se004 (cartes Taijutsu, dont les Dual Taijutsu, plus la Dual KN).
- Q-S3 Paths pour qui : **héros TMNT seulement** (PAS la lecture provisoire). A APPLIQUER : ajouter les six sets « TMNT Shinobi * » à `sets_exclusifs` de `data/arts_alternatifs.json` (+ régénérer les tables), et vérifier le deck-builder / la préparation.
- Q-S4 Last Ronin / aspects : **le Path gagne seulement pour Last Ronin** (provisoire confirmée). Rien à changer.
- Q-S5 Jennika + Path : **un seul Path** (provisoire confirmée). Rien à changer.
- Q-S6 trait NINJA/MYSTIC : **littéral** (« your hero » = forme héros, « you » = les deux formes) (provisoire confirmée). Rien à changer.

## Bushido
- Q-B1 sb006 Mercy : **(a) PV restants passent à 1, la défaite n'a pas lieu, on pioche 3** (provisoire confirmée). Lever « NON terminée ».
- Q-B2 sb013 Santōryū Ōgi : **(a) identité puis arme** (provisoire confirmée). Lever « NON terminée ». (Écart moteur Restricted signalé par l'agent, non réalisé.)
- sb018 Musha Shugyō : **seule l'identité du propriétaire (et ce qu'elle joue)** retire de la menace (lecture littérale confirmée).

## Kuji-Kiri
- Q-K1 sj020 Æthreal Shift : **Hero Interrupt** (provisoire confirmée ; le texte affiché garde « Hero Action » imprimé). Lever « NON terminée ».

## Ninjutsu
- Q-N1 sa001 Assassinate : **coquille, c'est « Hero Action »** (PAS la lecture provisoire « Action » littérale). A APPLIQUER : libellé / type « Hero Action » (texte affiché, cards.json, FR) ; comportement en jeu identique (forme héros camouflé).
- Q-N2 sa012 Black Ops : **Hero Response** (provisoire confirmée). Lever « NON terminée ».
- Q-N3 sa009 Twilight Sentry : **ordre du moteur conservé** (PAS la recommandation) : la carte ne sert qu'à camoufler l'allié à la pose ; l'Interruption n'est en pratique jamais proposée (statut Cloaked avant Interruption). Aucune extension moteur. Lever « NON terminée » (cas provisoire devient le comportement retenu).

## Taijutsu
- Q-T1 sh003 Stiff Jab : crédit « MC Custom Content By: Inkwire » **laissé tel quel** (provisoire confirmée). Lever « NON terminée ».
- Q-T2 sh017 Odyn : citation **corrigée en « behind »** (PAS la lecture provisoire) dans cards.json (le FR l'est déjà). A APPLIQUER.
- Q-T3 sh005 Double Kick : **événement DEFENSE+THWART : les deux puces, pioche 2** (provisoire confirmée). Lever « NON terminée ».
- Q-T4 sh016 Jō : **identité + cartes jouées** (provisoire confirmée). Lever « NON terminée ».

## Dual
- Q-D1 sc004 Kuragari : **Action des deux formes ; en alter-ego « your hero » = l'identité camouflée et redressée** (provisoire confirmée). Lever « NON terminée ».
- Q-D2 sc012 Hitodama : **Hero Action (attack)** (provisoire confirmée, précédent bt005). Lever « NON terminée » ; le libellé affiché « Hero Response » imprimé reste ou devient « Hero Action » : voir consigne de l'agent d'application (garder le texte imprimé dans cards.json, comme pour Æthreal Shift).

## Coquilles cosmétiques gardées telles quelles (non posées, par convention)
- sb016 Wakizashi « dashido », sj015 « wierdest », sj006 « textbox » : texte transcrit comme imprimé.
- Odyn (sh017) : le moteur résout la Réponse avant les dégâts consécutifs (la carte Tough absorbe ces dégâts) : à confirmer en partie réelle.
