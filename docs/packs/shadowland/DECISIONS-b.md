# Shadowland, scenario 2 « Shadow Labyrinth » : decisions de l'agent b

Portee : sets SHADOW LABYRINTH (sl037-sl045) et DEADLY CONTRAPTIONS (sl046-sl056), scenarios `shadow_labyrinth` et `shadow_labyrinth_expert`.
Le livret officiel (p. 12 : « Create the trap deck ») est introuvable : tout ce qui suit est DEDUIT des 20 cartes, de la Rules Reference habituelle et du moteur.
Chaque decision cite ce qui la justifie ; aucune n'a pu etre posee a l'utilisateur. A relire des que le livret est disponible.

## 1. Le paquet piege (« trap deck »)

| Point | Decision | Raison |
|---|---|---|
| Contenu a la mise en place | les 8 cartes de trait `TRAP!` : Whisper in the Dark (sl040) + les 7 pieges de Deadly Contraptions (sl050-sl056), melangees, faces cachees | sl038a « Create the trap deck » ; seules ces 8 cartes portent `TRAP!` (le trait est cite par sl046-sl049). Whisper est « TRAP! » ET se revele quand le Corridors n'est plus la (« otherwise, set this card aside ») : elle vient donc du paquet piege, pas du deck de rencontre (il n'y a qu'un exemplaire) |
| Les 7 pieges ne sont PAS dans le deck de rencontre | oui, uniquement dans le paquet piege | « Deadly Contraptions » compte 11 cartes numerotees ; les 4 autres (sl046-sl049) sont des cartes de rencontre ordinaires, les 7 pieges n'ont d'effet que « When Revealed : Choose » et n'ont aucun sens hors d'un tirage controle |
| Defausse piege (« trap discard pile ») | une pile a part ; les cartes `TRAP!` revelees y vont | sl045 « Shuffle the trap discard pile » |
| Carte NON-piege revelee depuis le paquet (sl041 et sl045 y melangent des cartes du deck de rencontre) | elle suit sa regle normale (sbire/manigance en jeu, traitrise a la defausse de RENCONTRE) | la pile « trap discard » ne recoit que les `TRAP!` : sinon une carte de rencontre y resterait piegee |
| « Reveal the top card of the trap deck » | revelee au joueur concerne (celui qui active, qui contre, qui revele) ; ses `When Revealed` partent | formule des cartes sl037, sl039b, sl041, sl045 |
| Paquet vide | on remelange la defausse piege dans le paquet puis on revele ; rien si les deux sont vides | regle habituelle d'un deck qui s'epuise (Rules Reference) |
| Melange d'une carte de rencontre | « shuffle the top N cards of the encounter deck into the trap deck » = les N cartes quittent le deck de rencontre ; sl045 melange AUSSI la defausse piege (un seul melange) | texte imprime |

Code : `shadow_labyrinth/__init__.py` (`CreerPaquetPiege`, `MelangerDansPaquetPiege`, `ReveleDuPaquetPiege`). Moteur : le `SetAsideDeck` « TrapDeck » (deja declare pour Hunting Season) + sa defausse.

## 2. Les trois choix « Avoid / Disarm / Trip »

Mecanique deduite des 7 cartes :
- chaque piege est une traitrise `TRAP!` dont le seul `When Revealed` est « Choose » entre trois options nommees ;
- **Avoid** = payer pour esquiver (defausser une carte d'un type de la main, ou depenser deux ressources) ; **Disarm** = payer plus, puis recevoir une recompense ; **Trip** = subir (degats, statut, defausse du deck) ; **Trip n'a pas de condition** : c'est le repli quand on ne peut payer ni l'un ni l'autre.

| Point | Decision | Raison |
|---|---|---|
| Une option dont l'exigence est impossible | n'est PAS offerte (Avoid sans carte du bon type en main, Disarm sans l'allie / l'amelioration / le soutien a defausser, option a ressources impayable) | sinon Avoid serait gratuit : c'est tout le sens du choix. Meme regle que sl004a (scenario 1) : le moteur reduirait une option payante impayable au plus gros morceau payable (`player_action.py` `_PayerAutantQuePossible`) |
| Blinding Powder, Disarm « discard 2 cards at random » | offerte seulement avec 2 cartes en main au moins | l'exigence est « 2 cartes » entieres (comme un cout) |
| Les defausses « at random » | au hasard (`DiscardRandomHandCards`) ; « 1 card from your hand » (Oil Slick Trip, Caltrops Disarm) = au CHOIX du joueur | texte imprime |
| « a character you control », « an enemy », « a scheme » | au choix du joueur parmi les cibles legales | texte imprime |
| « identity-specific card » (Caltrops) | une carte de classe `IdentitySpecific` (paquet du heros) | vocabulaire de la Rules Reference ; le moteur la porte deja (`card_player.py`) |
| Quel instant pour « When you choose the "X" effect » (sl046, sl048, sl049) | message maison `QuandOnChoisitUnEffetDePiege`, envoye APRES le choix et le paiement, AVANT la resolution de l'effet | le moteur n'envoie aucun message apres le choix d'une option nommee (`WhenPlayerChooseAbility` part avant). Le cout etant l'effet lui-meme (Avoid), l'ecart d'ordre est sans consequence |
| « you cannot choose the "Avoid" effect » (sl047) | message maison `PeutChoisirUnEffetDePiege` pose avant d'offrir l'option ; Iron Monk y repond (engage avec CE joueur) | meme raison ; un autre joueur peut encore choisir Avoid |
| « When YOU choose » des cartes en jeu (sl048, sl049) | le joueur qui choisit, qu'il possede ou non la carte ; sl046 (attachee) : le porteur seulement | texte imprime (sl046 « Attach to your identity ») |

## 3. Shifting Corridors, compteurs `passage`, complots 1 et 2

- **PV infinis** (sl037, « HIT POINTS ∞ ») : `desc.HP = "INF"` (le moteur le lit deja, `can_health.py`, comme sk228). Stalwart, SCH 0★, ATK 0★ : natif / valeurs 0.
- **Menace cible infinie de sl038b** : `desc` sans `TargetThreat` (« pas de menace cible », le moteur ne l'accomplit jamais, precedent 11008b / 40139b). Le « ∞ » reste sur l'image.
- **sl038b, degats -> menace** : tout le montant que Shifting Corridors AURAIT subi (apres Tough, reductions) est retire du complot ; aucun compteur de degats ne s'accumule. Plus de degats que de menace = toute la menace part.
- **Derniere menace retiree = avance** au stade 2 (`this.Advance`) ; « the players win by advancing » : l'avance est le but du stade 1, rien a coder de plus.
- **Compteurs passage** : 10 par joueur (7 en expert) a la revelation de sl038b. Retirer le dernier fait perdre les joueurs, quelle que soit la carte qui le retire (activation de Corridors, Dead End).
- **Activation de Corridors** : `WhenEnemyWouldActivate` (Forced Interrupt) + `SetBeInstead` : l'activation n'a pas lieu (ni attaque, ni manigance, ni carte de boost), un passage est retire, le piege du dessus est revele au joueur vise ; quelle que soit la forme (heros ou alter-ego).
- **Dead End** : « If Shifting Corridors is in play » = Corridors est le vilain en jeu (stade 1) ; sa menace de depart (2 par joueur) n'augmente pas dans ce cas.
- **sl039a** : « Set Shifting Corridors aside » = zone de mise de cote du scenario (pas la defausse). « Find the chosen villain » : le vilain tire a la mise en place est MEMORISE (`world.sl_vilain_choisi`, ex. `sl014`) ; il reste de cote jusqu'au stade 2. Face B en expert : on retourne la carte puis on revele LA NOUVELLE FACE (reveler l'ancienne face laisse la B sans deck de rencontre : plantage constate).
- **sl039b** : en expert le vilain active contre chaque joueur a la revelation. « After you or an ally you control thwarts this scheme » : un contre d'un personnage d'un joueur (identite ou allie), menace retiree > 0 ; limite « une fois par round et par joueur » par le helper de Hunting Season (`LimiteParJoueurEtParRound`).
- **Victoire** (NON imprimee) : le vilain Dark Protege choisi vaincu, quelle que soit sa face = victoire des joueurs. Le moteur ne la declare pas seul tant que d'autres vilains sont de cote (`scenario.py`) : comme sl001b, ecrit dans sl039b (`WhenUnitBeDefeated` -> `SetGameOver`). Le stade 2B est donc le seul combat contre le vilain ; il n'y a pas de retournement du vilain (c'est une mecanique du scenario 1).
- **Pas de menace cible pour 2B ?** Si : 9 par joueur, accomplie = defaite (natif, texte « If this stage is completed »).

## 4. Whisper in the Dark (sl040) : le vilain traite comme un sbire ELITE

Le moteur ne sait « traiter comme un sbire » que des allies et des heros (`treat.py`). Technique de pu139 (Capo of the Past, deja dans le depot) : un SOSIE sbire (gabarit « Minion ») qui reprend nom, devise, visuel, ATQ, SCH et capacites imprimees de la face A du vilain choisi, avec **6 PV imprimes**, le trait ELITE, Guard et Villainous ; Whisper lui est attache.

- La vraie carte du vilain RESTE de cote, intacte : « put the set-aside chosen villain into play » est rendu par le sosie, et sl039a la revelera au stade 2 sans avoir a nettoyer degats ni statuts.
- « When Defeated : set this minion aside » : le sosie quitte la partie (jamais defausse : une carte generique « Minion » ne doit pas finir dans le deck de rencontre) ; Whisper, attachement lie au paquet piege, est defausse dans la defausse piege.
- Si le complot avance alors que le sosie est encore la : sl039a le retire AVEC ses attachements (Whisper en defausse piege), puis revele le vrai vilain (« Discard each status card, token, and attached card »).
- « otherwise, set this card aside » (Corridors absent) : un attachement non pose est defausse par le moteur a la fin de sa revelation ; on redirige sa defausse liee vers la zone de mise de cote (`card.bind_discard_pile`). Le vilain manigance contre le joueur.
- Les capacites du vilain (scripts Dark Protege, codes par un autre agent) s'appliquent au sosie (decision deja prise pour pu139 : il garde ses capacites) : a RE-VERIFIER a l'integration, aucun script Dark Protege n'existe dans cette branche.

## 5. Autres cartes

- **sl041 Lord Deathstrike** : Patrol natif ; Boost = `PutThisIntoPlay` (entre en jeu engage, SANS When Revealed).
- **sl043 Hall of Hidden Doors** : « the defeating player » (a defaut le premier joueur) retire 5 menaces du complot principal PUIS defausse jusqu'au premier sbire OU manigance annexe et le revele. `Worlds.DiscardEncounterCardsUntil(check_face_fn=...)`.
- **sl044 No Time to Think!** : Peril natif ; « the villain activates against you » = `DoActivate` (attaque en forme heros, manigance en alter-ego) ; le Boost ne vaut qu'en ATTAQUE (`during_attack`) : +2 icones de boost et overkill.
- **sl046 Nervous Jitters** : types nommables = ceux d'un deck de rencontre (sbire, traitrise, attachement, manigance annexe, environnement, obligation). Deck de rencontre vide au moment de defausser : rien n'est defausse, donc pas de degats (« the card discarded this way » n'existe pas).
- **sl048 / sl049 Boost** : « each character you control » = identite + allies du joueur contre qui l'activation a lieu.
- **Icones** : relues sur les scans le 22/10 ; corrections de `cards.json` : sl044 Boost 1 (etait absent), sl045 Boost 2 (absent), trait `TRAP!` sur sl040 et sl050-sl056 (etait `TRAP`, la decision du 22/10 etait de l'ecrire avec « ! »), ligne « TRAP! » retiree du texte de sl040, sl037 `HP INF`, sl038b sans TargetThreat.

## 6. Scenarios

`shadow_labyrinth` / `shadow_labyrinth_expert` (modele : shadows_in_the_night) : vilain `sl037` ; complots `sl038a,sl038b` puis `sl039a,sl039b` ; mises de cote : les 8 `TRAP!`, les 6 vilains Dark Protege (`sl012a,b`...`sl017a,b`) et leurs 10 cartes liees (`sl018`-`sl027`) ; deck de rencontre : Shadow Labyrinth (sl041-sl045, sl044 et sl045 en double), Deadly Contraptions (sl046-sl049), Ninja Swarm (sl028-sl036, x1) + set `standard` (+ `expert`). Les sets Dark Protege et Ninja Swarm sont codes dans d'autres branches : l'integration complete se fait apres fusion (en attendant les cartes liees / Ninja n'ont que leurs valeurs imprimees).

## 7. Points a surveiller

- **Moteur** : `Deck.DiscardUntil` rend « rien » quand la carte cherchee est la DERNIERE du deck (`deck.py`, `if self.GetSize() == 0: return None`). Le sbire / la manigance est pourtant defausse(e). Cas rares (sl043, sl055, sl056), non modifie (fichier partage) : les cas `[slb]` mettent une carte de plus sous la cible.
- Un deck de rencontre epuise pendant « discard until » est remelange avec sa defausse + 1 jeton d'acceleration (regle standard, observee).
- Aucune partie reelle jouee par un humain : le plateau (`ui-app`) n'a pas ete regarde pour le paquet piege ni le sosie de Whisper (etape 8 bis non faite faute d'outil de capture dans cette session).
