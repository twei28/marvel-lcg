# Casey Jones v3 (`tc`) : questions en attente

Source : zip `TMNT Heroes-20261014T200300Z-1-001.zip`, dossier `TMNT Heroes/Casey Jones v3/`.
Scans versionnes : `.planning/tmnt/pics-casey/<card_id>.jpg` (chemin d'origine indique ci-dessous).
Chaque lecture ci-dessous est IMPLEMENTEE PROVISOIREMENT (la recommandee, en premier) et marquee
`TODO-QUESTION` dans le script. Aucune n'est un blocage : le cas de test qui la couvre est nomme.

---

## Q1 : « Casey Jones WEAPON upgrade » (tc002 Clap Back, tc006 Anything Goes)

- card_id : `tc002` (scan `Casey Jones Deck/1 Clap Back.png`) et `tc006` (scan `Casey Jones Deck/9 Anything Goes.png`).
- Texte anglais exact :
  - tc002 : « If a Casey Jones **WEAPON** upgrade was discarded to pay for this card, confuse an enemy. »
  - tc006 : « Exhaust Anything Goes -> swap a Casey Jones **WEAPON** upgrade you control with a Casey Jones **WEAPON** upgrade tucked under Casey's Bag. »
- Lectures possibles :
  1. **(retenue)** une arme du SET « Casey Jones » (tc007, tc009, tc010, tc011, tc012 : les cinq WEAPON du pack).
     Precedent du depot : `hd013` « a Howard the Duck card » = `set_name`. C'est la seule lecture qui donne une
     fonction au mot « Casey Jones » : Overswing (tc001a) dit deja « a WEAPON upgrade you control », sans nom.
  2. toute amelioration WEAPON que Casey controle (le nom « Casey Jones » ne serait qu'un rappel).
  3. une amelioration WEAPON dont le NOM contient « Casey Jones » (aucune n'existe : la carte serait morte).
- Ce que ca change en jeu : avec la lecture 1, defausser par Overswing le Sai de Raphael (WEAPON, Restricted)
  paie Clap Back mais ne confond PAS l'ennemi ; avec la 2, il confondrait. Anything Goes ne voit que les 5 armes de Casey.
- Cas qui la figent : `[casey] tc002 ... une arme d'un AUTRE heros (Raphael's Sai)` et `[casey] tc006 ... aucune arme de Casey EN JEU`.

## Q2 : Setup du Sac quand il est dans la MAIN de depart (tc001b)

- card_id : `tc001b` (scan `0 Casey Jones alter-ego.png`) ; la carte concernee est `tc013` Casey's Bag.
- Texte anglais exact : « **Setup**: Search your deck and discard pile for the Casey's Bag upgrade and put it into play. (Shuffle.) »
- Contexte moteur : `World.Setup` resout les capacites de Setup des personnages a l'etape 16, APRES la pioche
  de depart et le mulligan. Le deck de heros fait 16 cartes, la main de depart 6 : le Sac a environ 37 % de chances
  de se trouver DEJA dans la main, donc ni dans le deck ni dans la defausse.
- Lectures possibles :
  1. **(retenue)** lecture litterale : on fouille le deck ET la defausse, rien d'autre. Si le Sac est en main, il y reste
     (il n'a pas de cout imprime : il ne se joue pas, il ne sert que de ressource [mental]).
  2. fouiller aussi la MAIN (c'est ce que fait `tm001b` de Michelangelo pour tm009, par arbitrage de l'utilisateur).
  3. resoudre ce Setup AVANT la pioche de depart (ordre different de celui du moteur ; changerait tous les heros).
- Rappel : le Sac n'imprime AUCUN cout (une barre « - » a la place du chiffre) : il est donc injouable depuis la main
  et ne sert que de ressource [mental] (lecture retenue ; si c'etait un cout 0 il pourrait se jouer depuis la main).
- Ce que ca change en jeu : avec 1, environ une partie sur trois commence SANS Sac (Casey n'a alors ni tuck,
  ni Anything Goes utile, ni retour d'arme par le Sac).
- Cas qui la fige : `[casey] tc001b Setup : le Sac dans la MAIN de depart n'est PAS cherche`.

## Q3 : Cricket Willow, Reponse offerte quand l'ennemi attaque est vaincu (tc009)

- card_id : `tc009` (scan `Casey Jones Deck/12 Cricket Willow.png`).
- Texte anglais exact : « **Hero Response**: After you attack an enemy, discard Cricket Willow -> stun that enemy. »
- Lectures possibles :
  1. **(retenue)** la Reponse n'est PAS offerte quand plus aucun ennemi attaque ne peut etre etourdi (vaincu par
     l'attaque) : on ne defausse pas le Willow (cout) pour un effet impossible.
  2. elle reste offerte, le Willow est defausse pour rien.
- Cas qui la fige : `[casey] tc009 Cricket Willow : l'ennemi VAINCU par l'attaque ... n'est pas etourdi : le Willow reste en jeu`.

## Q4 : Anything Goes, l'arme qui entre en jeu par l'echange (tc006)

- card_id : `tc006` (scan `Casey Jones Deck/9 Anything Goes.png`).
- Texte anglais exact : « **Hero Action**: Exhaust Anything Goes -> swap a Casey Jones **WEAPON** upgrade you control with a Casey Jones **WEAPON** upgrade tucked under Casey's Bag. »
- Lectures possibles :
  1. **(retenue)** echange de places : l'arme en jeu va SOUS le Sac (rangee, face cachee), l'arme rangee entre en jeu PRETE,
     attachee a Casey ; on range d'abord, donc la limite Restricted n'est jamais depassee.
  2. meme echange, mais l'arme entrante arrive INCLINEE (comme les armes mises en jeu par Mikey / Leo / Raph).
  3. l'arme sortante est DEFAUSSEE et non rangee (contredit « swap » : elle ne serait plus echangeable).
- Ce que ca change en jeu : avec 2, une arme a Hero Interrupt echangee ne servirait pas ce tour-ci.
- Cas qui la fige : `[casey] tc006 Anything Goes : ECHANGE la Baseball Bat (en jeu) et le Cricket Willow (range sous le Sac)`.

## REPONSES DE L'UTILISATEUR (16/10/2026)

- **Q1** : armes du SET « Casey Jones » (lecture retenue, confirmee).
- **Q2** : fouiller AUSSI la main (PAS la lecture retenue) : tc001b met le Sac en jeu meme s'il est dans la main de depart. Corrige, cas « le Sac dans la MAIN de depart est AUSSI trouve » vu rouge puis vert.
- **Q3** : Cricket Willow, Reponse NON offerte quand l'ennemi attaque est vaincu (confirmee).
- **Q4** : Anything Goes, arme entrante PRETE, l'ancienne RANGEE sous le Sac (confirmee).
