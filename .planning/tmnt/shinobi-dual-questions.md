# TMNT Shinobi, cartes DUAL (`sc001`-`sc012`) : questions ouvertes pour l'utilisateur (17/10/2026)

> Réponses rendues le 17/10/2026, voir shinobi-reponses.md (les mentions « NON terminée » / « provisoire » ci-dessous sont historiques : cartes levées).

Sources : zip « TMNT Shinobi », dossier `Dual Shinobi Cards/` (12 scans, 1500x2150). Scans : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/zip-shinobi/TMNT Shinobi/Dual Shinobi Cards/`.
Une question à la fois, scan à l'appui (consigne : montrer l'image avant chaque question). Lecture PROVISOIRE retenue entre parenthèses ;
chaque question dit ce qu'elle change EN JEU. Deux cartes sur douze sont concernées : elles sont scriptées dans la lecture provisoire
(le comportement est prouvé par cas) mais restent **NON terminées** jusqu'à la réponse.

## Q-D1 : sc004 Kuragari : « Action » (et non « Hero Action ») qui vise « your hero » : que fait-elle en forme alter-ego ?
- Scan : `Dual Shinobi Cards/BN2 Kuragari.png`. Texte imprimé : « *OATH.* Uses (3 samurai counters). **Action**: Exhaust this card and
  remove 3 samurai counters from it → cloak and ready your hero. »
- Pourquoi c'est ambigu : une « Action » (sans « Hero ») se joue dans les DEUX formes de l'identité, mais « your hero » n'existe qu'en forme
  héros. Aucune carte officielle du dépôt n'imprime « Action » avec « your hero » (relevé fait sur `data/cards.json` : 0 occurrence) ; les
  cartes soeurs de la même série qui redressent « your hero » disent toutes « Hero Action » (`jennika/tj006` Fearless Resolve, `se003` Samurai).
- Options :
  - (a) **le scan à la lettre : Action jouable dans les deux formes ; en forme alter-ego, « your hero » = l'identité du joueur (la carte
    d'identité, face alter-ego), qui est camouflée ET redressée** (recommandée : lecture littérale du texte imprimé ; c'est ce qui est codé) ;
  - (b) coquille probable : c'est une **Hero Action** (forme héros seulement), comme les autres cartes qui redressent « your hero » ;
  - (c) Action proposée dans les deux formes, mais en alter-ego elle ne fait RIEN (le coût de 3 compteurs est payé en vain, aucun héros à
    camoufler ni redresser).
- Effet en jeu : (a) en alter-ego on peut dépenser la carte pour redresser Peter Parker (par exemple pour réutiliser une capacité
  d'alter-ego ou « Recover ») et le camoufler ; (b) la carte n'est jouable qu'en forme héros, jamais en alter-ego ; (c) piège : on perd la carte
  (une seule utilisation) sans bénéfice si on l'utilise en alter-ego.
- Provisoire : (a). Cas : `[sc] sc004 Kuragari (PROVISOIRE Q-D1)` (alter-ego : identité camouflée et redressée). `sc004` : **NON terminée** (attend Q-D1).

## Q-D2 : sc012 Hitodama : une « Hero Response » SANS déclencheur (pas de « After... »)
- Scan : `Dual Shinobi Cards/NT2 Hitodama.png`. Texte imprimé : « *ATTACK.* **Hero Response** *(attack)*: Deal 3 damage to an enemy. If you
  paid for this card with a **THWART** event, cloak your hero. »
- Pourquoi c'est ambigu : une Réponse part « après » un événement (« After you... »), une Interruption « quand » un événement va se produire.
  Ici aucun événement n'est cité : la capacité n'a aucune fenêtre où partir. Même situation que `beast/bt005` Fighting With Friends (« Hero
  Response: Ready your hero... » sans déclencheur), que l'utilisateur a tranchée en **Hero Action** (`.planning/todos/2026-09-01-beast-gabarits-
  processus-carte.md`, bt005). Les deux cartes soeurs `sc001` Nendō et `sc011` Kenbu, de même forme « Hero Action (attack): ... deal damage », sont des
  Hero Action.
- Options :
  - (a) **Hero Action (attack)** (recommandée : précédent bt005 tranché par l'utilisateur ; même famille que Nendō et Kenbu ; c'est ce qui est codé) ;
  - (b) une vraie Réponse de héros dont le déclencheur a été perdu : donne-moi le déclencheur voulu (par exemple « After an enemy attacks you » ou
    « After you play a THWART event ») ;
  - (c) autre.
- Effet en jeu : (a) Hitodama se joue pendant ton tour comme n'importe quelle attaque d'événement (3 dégâts, camouflage si payée avec un
  événement THWART) ; (b) elle se jouerait hors de ton tour, en réaction à l'événement choisi (par exemple pendant la phase du méchant).
- Provisoire : (a). Cas : `[sc] sc012 Hitodama (PROVISOIRE Q-D2)` (6 cas). `sc012` : **NON terminée** (attend Q-D2).

## Notes sans question (relevées, aucune décision en jeu)
- **sc008 Naito Dansā** : « Discard cards from the top of the encounter deck until you discard an attachment or side scheme. Reveal that card →
  cloak up to 2 friendly characters. Daze up to 2 enemies. » reproduit **exactement** la structure de deux cartes déjà portées :
  `sm/27015` Return the Favor (« until you discard a treachery. Reveal that treachery → deal 5 damage », la révélation est le COÛT de la suite) et
  `alopex/ta006` Sniff Out Trouble (« until you discard a minion or side scheme. Reveal that card → draw 2 cards... »). Pas de question
  (consigne : texte sans ambiguïté qui reproduit une officielle). Seule différence : le type cherché est une UNION (attachement OU manigance annexe).
- **sc011 Kenbu** : « Daze each enemy damaged this way » : un ennemi dont la carte Tenace absorbe le dégât n'est pas « damaged » (règle habituelle) ;
  lecture du moteur : seuls les ennemis qui ont réellement perdu des PV sont hébétés (cas `Rhino TENACE`).
- **Crédit imprimé** : les 12 scans impriment « TMNT Shinobi By: Inkwire » (aucune coquille « MC Custom Content », contrairement à `T3 Stiff Jab`).
- **Résolution des ressources** (non une question de texte, une limite moteur) : voir le rapport, « Nendō / Omawari et une arme qui produit aussi
  une ressource ».
