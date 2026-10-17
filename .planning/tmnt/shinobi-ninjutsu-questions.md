# TMNT Shinobi Ninjutsu (`sa001`-`sa020`) : questions ouvertes pour l'utilisateur (17/10/2026)

> Réponses rendues le 17/10/2026, voir shinobi-reponses.md (les mentions « NON terminée » / « provisoire » ci-dessous sont historiques : cartes levées).

Scans : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/zip-shinobi/TMNT Shinobi/Ninjutsu/`.
Une question à la fois, scan à l'appui (consigne : montrer l'image avant chaque question). Lecture PROVISOIRE retenue
entre parenthèses ; chaque question dit ce qu'elle change EN JEU. Les cartes concernées sont **NON terminées** ; leur
comportement provisoire est prouvé par des cas, le point en suspens est signalé dans les cas eux-mêmes.

## Q-N1 : sa001 Assassinate : « Action (attack) » ou « Hero Action (attack) » ? et « your hero is cloaked » en alter-ego ?
- Scan : `N1 Assassinate.png`. Imprime : « Play only if your hero is cloaked. **Action** *(attack)*: Deal 7 damage to a minion.
  This attack gains piercing. » Les autres cartes à condition « your hero is cloaked » de la même extension
  (`sa004` Scale the Wall, `sa005` Run the Rooftops) impriment « **Hero Action** », et `sa006` Cut-and-Run
  « **Hero Action** *(attack)* ».
- Deux lectures du même défaut possible : (1) coquille « Action » pour « Hero Action » ; (2) l'Action est voulue pour les
  deux formes, et alors il faut dire ce que « your hero is cloaked » vaut quand le joueur est en forme ALTER-EGO (la carte
  Cloaked est posée sur la carte d'identité, qui change de face avec la forme).
- Options : (a) **« Action » telle quelle ; « your hero is cloaked » = l'identité est en forme HÉROS et porte une carte Cloaked**
  (recommandée : lecture littérale, c'est ce qui est codé ; en pratique la carte n'est jouable qu'en forme héros, comme si
  c'était « Hero Action ») ; (b) coquille : c'est « Hero Action » (même comportement en jeu que (a), seul le libellé
  change) ; (c) « Action » voulue pour l'alter-ego : l'identité porte une carte Cloaked quelle que soit la forme, et
  l'alter-ego peut infliger les 7 dégâts perçants (le moteur n'a pas de « héros » à créditer de l'attaque : extension à écrire) ;
  (d) autre.
- Effet en jeu : (a) et (b) : jouable seulement en forme héros ; (c) jouable aussi en alter-ego tant que l'identité est
  camouflée.
- Provisoire : (a) (cas `[sa] sa001`, dont « forme ALTER-EGO camouflée : injouable »). `sa001` : **NON terminée** (attend Q-N1).
  Même point pour `sa004`, `sa005`, `sa018`... : leur texte est sans ambiguïté (« Hero Action », « identity »).

## Q-N2 : sa012 Black Ops : « Hero Action: After your hero defeats... » est contradictoire
- Scan : `N12 Black Ops.png`. Imprime : « **Hero Action**: **After** your hero defeats a minion or side scheme, discard
  Black Ops → ready your hero. » Une Action se joue à volonté, « After ... » est le déclencheur d'une RÉPONSE (même coquille
  que The Made Men, `ud004` Stealth Fighter ; `se008` Onigari imprime correctement « Hero Response: After you defeat a minion
  or side scheme »).
- Options : (a) **Hero Response : « After your hero defeats a minion or side scheme, discard Black Ops → ready your hero »**
  (recommandée : seule lecture qui donne un sens à « After », même forme que Onigari) ; (b) Hero Action : « discard Black Ops →
  ready your hero » SANS déclencheur (jouable quand on veut, après avoir vaincu ou non) ; (c) Hero Action à la lettre :
  jouable à tout moment, mais seulement si le héros vient de vaincre un sbire ou un complot annexe pendant ce tour ; (d) autre.
- Effet en jeu : (a) le redressement part juste après la défaite (y compris pendant la phase du vilain) et peut se refuser ;
  (b) un redressement gratuit une fois, à tout moment ; (c) comme (a) mais en action.
- Provisoire : (a) (cas `[sa] sa012`). `sa012` : **NON terminée** (attend Q-N2).

## Q-N3 : sa009 Twilight Sentry : l'Interruption face au statut Cloaked qui résout avant
- Scan : `N9 Twilight Sentry.png`. Imprime : « Attach to an ally you control and cloak them. Max 1 TRAINING upgrade per ally.
  **Interrupt**: When attached ally would take any amount of damage, discard a cloaked status card from them **instead**. »
- Règle de priorité du jeu (déjà codée : `TimingPriority`, Statut avant Interruption) : une carte d'état résout AVANT toute
  Interruption. Un allié camouflé qui va subir des dégâts voit donc d'abord sa carte Cloaked prévenir 2 dégâts et partir ;
  quand l'Interruption peut répondre, il n'a plus de carte Cloaked à défausser. La carte, qui camoufle l'allié à la pose
  (un seul Cloaked par personnage), ne peut donc JAMAIS servir à un allié porteur d'une seule carte Cloaked.
- Mesure (cas `[sa] sa009 ... Interrupt [LECTURE PROVISOIRE Q-N3]`) : allié camouflé + Sentry, 3 dégâts -> le statut préviendra 2, 1 dégât
  subi, Sentry jamais proposée.
- Options : (a) **la carte REMPLACE la résolution du statut (« instead ») : le joueur peut choisir Sentry AVANT que le statut
  résolve ; tous les dégâts sont évités et la carte Cloaked part** (recommandée : c'est la seule lecture où la carte sert ; extension
  du moteur : une Interruption optionnelle qui passe avant les cartes d'état) ; (b) ordre du moteur conservé (la carte ne sert que si
  le Cloaked n'a pas résolu avant : en pratique jamais, sauf Shredder avec plusieurs cartes Cloaked) ; (c) la carte remplace la
  prévention de 2 du statut mais LAISSE le statut agir en premier si le joueur ne la déclenche pas ; (d) autre.
- Effet en jeu : (a) un allié camouflé protégé par Sentry ne subit aucun dégât une fois (-2 puis -2 sinon) ; (b) la carte n'apporte que
  le Cloaked à la pose.
- Provisoire : (b) (rien changé au moteur ; le script est écrit pour (a) dès que l'ordre le permet). `sa009` : **NON terminée** (attend Q-N3).
