# Mode campagne — questions ouvertes

Source : le livret `rulebook 1.5.pdf`, pages relues image par image (p.5-7, 9, 11, 13, 15, 17, 21-24).
Une entree par doute : la phrase, les lectures possibles, celle retenue, ou la changer.

## Regles

### Q1. Quelle carte de la pile de victoire coche quelle case du tableau ? (p.6, p.21 FAQ)
- Texte : « Each card in the victory display can be used to check off only one requirement » ; FAQ : « Each card in the victory
  display can be used to check off only one requirement in the Cooperation Progress section ».
- Lectures : (a) le JOUEUR choisit la case de chaque carte ; (b) le jeu choisit.
- Retenu : (b), par `AssignerLaProgression` : d'abord le plus grand nombre de LIGNES completes (une ligne = une carte de campagne
  gagnee), puis, avec les cartes qui restent, le plus de cases cochees, chaque carte sur sa case la plus RAIRE (un titre avant une
  categorie large) ; a egalite, l'ordre du tableau imprime. Le joueur peut corriger le carnet a la main (champ « Tableau de
  coopération » du panneau, une case par « Carte: exigence »).
- A trancher : veut-on un ecran de choix (une carte -> une case) ? Un joueur qui prefere gagner Antalya avant Cadre K ne le peut pas.

### Q2. Un sbire d'Elite en pile de victoire coche-t-il aussi le tableau ? (p.9, p.24)
- Les cartes en pile de victoire sont TOUTES des « minions and side schemes in the victory display ». Un sbire Elite (Victory 1) y est
  donc compte pour le tableau (« ELITE minion », « Jazinda », « ELITE SKRULL minion »...) EN PLUS d'ajouter son allie et son complot
  de joueur. Retenu : oui, sans exception.

### Q3. « one OTHER random Skrull Elite » : parmi quoi ? (p.10, 12, 15)
- Lectures : parmi les ensembles jamais tires (retenu), ou parmi tous sauf ceux deja en jeu.
- Retenu : parmi ceux dont le carnet n'a encore aucune zone (`Skrull Elite: <nom>` vide) ; un ensemble retire de la campagne ou
  laisse « ailleurs » compte comme DEJA TIRE. Au scenario 5, « the remaining » : TOUS ceux qui n'ont jamais ete tires (un seul dans une
  campagne jouee en entier ; cinq si on commence directement au 5).
- Defaite : le carnet n'est pas touche (« If the players lost, they may reset the scenario ») : au nouvel essai, l'Elite est TIREE DE NOUVEAU.

### Q4. Que devient une Elite qui n'est NI en pile de victoire NI en jeu ? (p.9)
- Le carnet n'a que deux cases par Elite et par scenario : « In the victory display » et « In another game area ». Retenu : tout ce qui
  n'est pas en pile de victoire (en jeu, deck rencontre, defausse, deck d'un joueur, retire du jeu) est « In another game area ».

### Q5. Combien de fragments de cote au scenario 1 ? Lesquels ? (p.7 vs p.9)
- p.7 (insert du set) : « set the Shaper minion and ALL FOUR Cosmic Cube Fragment aside » ; p.9 (campagne) : « ONE copy of the Cosmic Cube
  Fragment resource PER PLAYER aside ». Retenu : p.9 (c'est l'instruction de campagne). Quels exemplaires : au hasard parmi les quatre
  (moteur, graine de la partie), tous les quatre a quatre joueurs. En solo, le joueur n'a donc qu'un fragment au hasard au lieu de toujours
  le jaune.

### Q6. Campagne experte : un joueur elimine qui NE revient PAS (p.6)
- Texte : « the defeated player can rejoin the teammates for the next scenario by placing an acceleration token... ». Si le joueur
  refuse : le texte ne dit pas ce qu'il fait. Retenu : il ne joue pas ce scenario (le moteur l'ELIMINE a la mise en place,
  `Player.Eliminate`). Un joueur elimine qui revient repart a PV complets (« to restore their identity to full hit points »).
- Les PV d'un joueur elimine ne sont pas relevables : le panneau ignore ses champs (« Un héros éliminé ne participe à AUCUNE étape de
  victoire »), d'ou la cle `Eliminated Players` (numeros de siege) qui porte l'information.

### Q7. Les PV restants sont PLAFONNES aux PV de base : base de quelle face ? (p.6)
- Retenu : `identity.printed_health` de la face courante a la fin de la partie (PV imprimes de l'identite), jamais les PV augmentes par une
  carte (Sy-Torak Gem : « You get +3 hit points »). Prouve par `expert — PV restants PLAFONNES`.

### Q8. Le sbire « Revealed » du scenario 5 et la regle de cooperation (p.21 FAQ)
- Retenu a la lettre : aucune proposition pour un sbire portant le trait REVEALED (il va dans la defausse Impostor). Les ALLIES CAMOUFLAGED ne sont pas des
  sbires : ils ne sont pas concernes.

### Q9. « the player who defeated it » (p.6)
- Retenu : le joueur qui controle le personnage vainqueur (identite ou allie), comme `WhenUnitBeDefeated.defeating_player` ; rien n'est
  propose quand le sbire tombe de la main d'une carte rencontre, d'un degat sans source ni, bien sur, quand le deck du joueur est vide
  (« discard the top card of their deck » : on ne peut pas). Une carte a Victory X va deja en pile de victoire : aucune question, rien
  n'est defausse.
- Les complots annexes concernes : tous (de rencontre, de nemesis, de joueur). Pas le complot principal.

### Q10. Cartes de campagne et limite de deck (p.5)
- Retenu : ces cartes sont generees A LA MISE EN PLACE (apres la composition du deck), jamais ecrites dans le deck enregistre ; elles
  ne comptent donc ni dans le minimum ni dans le maximum, et « retournent a la zone » toutes seules (le carnet ne les en retire jamais). Une carte
  unique choisie par un joueur n'est plus proposee au suivant (une seule copie dans la zone).
- A faire cote deck-builder / catalogue (hors de ma portee) : « These cards cannot be included in any deck unless playing the Skrull
  Menace campaign » : les cartes 263-288 devraient etre ABSENTES du constructeur de decks.

### Q11. La carte « Cooperation Progress Reminder » (RESOLUE : creee, sk289a / sk289b) (p.6, images `cooperation progress reminder*.png`)
- C'est une aide de jeu physique (« each player MAY take » une carte). La REGLE qu'elle rappelle est implementee pour tous les
  joueurs ; la carte elle-meme n'est pas creee (pas de card_id dans la plage 263-288 : elle n'est pas numerotee). Si on la veut dans le
  jeu (une carte inerte au dos « Do not flip this unless you intend to build cooperation »), c'est une carte de plus pour l'agent des cartes.

### Q12. Graphie du tableau : « Skrull Kill Crew » (tableau) contre « Skrull Kill Krew » (carte sk282)
- Le tableau imprime p.24 ecrit « Crew », la carte « Krew » (et sa citation « Skull Kill Krew »). Retenu : « Skrull Kill Crew » dans le carnet (ce
  que le joueur lit dans son tableau) ; l'identifiant interne est `sk282`. Meme remarque pour « Pool-o-Vision » (tableau) contre « Pool-O-Vision » (carte) et
  « Nullifier » (tableau) contre « Ultimate Nullifier » (carte).

### Q13. Le journal par scenario (p.22-23)
- Le carnet imprime a une colonne par scenario 1-4 (zone du Shaper, du Cube, de chaque Elite). Le jeu ne garde que la DERNIERE valeur : c'est la seule
  que les instructions de mise en place relisent. L'historique des cases cochees par scenario n'est pas conserve.

## Interface (plateau et ecran de campagne) — FAITE le 16/10/2026 sauf 5 et 6 (voir CAMPAGNE-MODE.md)

Ce qui existe et suffit pour jouer : le panneau de fin de partie montre la zone de cooperation (les 30 cartes en vignettes cliquables, celles
de la zone sont cochees, corrigeables), le tableau (champ texte) et les zones du Shaper, du Cube et de chaque Elite (champs texte) ; les
deux sets alternatifs sont des reglages de campagne (Oui / Non) ; le livret (15 pages) est branche a l'ecran de campagne.

Ce qui manquerait pour un vrai confort (a decrire a l'agent de l'interface) :
1. **Un onglet « Zone de coopération » sur l'ecran de campagne** : cinq colonnes (Allies / Complots annexes de joueur / Ressources / Soutiens / Ameliorations)
   comme la planche du carnet p.22, les cartes presentes en couleur, les autres en grise.
2. **Un onglet « Tableau de coopération »** : le tableau de la p.24 (13 lignes, 34 cases), cases cochees en vert, calcule depuis `Cooperation Progress`.
3. **Le choix des cartes de la zone AVANT la partie**, par vignettes (une par type, par joueur), au lieu des fenetres de question de la mise
   en place (qui n'affichent que le nom de la carte). Le moteur lit deja ses choix dans les questions ; une cle `Player N Cooperation Deck` pourrait
   les pre-remplir.
4. **Choisir quelle carte coche quelle case** (Q1), avec la proposition du jeu pour valeur par defaut.
5. **L'Elite du scenario a venir**, affichee avant le lancement (« Cette fois : Xavin »), au lieu de la decouvrir a la mise en place.
6. En jeu : la proposition « defausser le dessus du deck pour placer le sbire en pile de victoire » est un `Cancel/accepter` standard ;
   un bouton a cote de la carte vaincue serait plus lisible.
