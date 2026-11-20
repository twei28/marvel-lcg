# Shadowland (MC65) : inventaire des cartes

Transcription du 22/10/2026 depuis les 93 scans de play.marvelsimulator.com (`.planning/shadowland/scans-marvelsimulator/`), **relue par un second regard independant** (5 relectures, une par lot, `verif1-5.json`) : 23 corrections appliquees (menaces cible/depart, icones, lignes de traits retirees du texte). **Aucun texte n'est encore valide contre le livret ni contre MarvelCDB.** Fichier genere par `.planning/shadowland/transcriptions/generer_cartes_md.py` depuis `toutes-relues.json` ; la transcription brute est `toutes.json`.

Identifiants du jeu : `65NNN[A|B]` officiel -> `slNNN[a|b]` (prefixe `sl`, voir `PLAN.md`).

## Verifie

- **93 images, 78 numeros, 90 exemplaires** : la somme des totaux imprimes par set (13+16+9+11+11+17+13) fait 90, comme l'annonce du produit ; les « trous » dans la numerotation « n/m » d'un set sont les exemplaires multiples d'une meme carte (quantite = ecart avec le numero suivant). La quantite est DEDUITE, pas lue.
- L'icone rouge en forme de **Y** est l'icone **Boost** (compare a Sandman 01102 Boost 2, Breakin' & Takin' 01107 Boost 2, Armored Guard 01120 Boost 1) ; l'etoile rouge isolee est l'icone de boost « ★ » (effet ecrit dans le texte).
- **Complot principal, face B** : le rond en haut a gauche est la menace **cible** (TargetThreat), le nombre en bas a droite est la menace de **depart** (StartingThreat), `+1` au-dessus est l'escalade (compare a 01097b The Break-In!).
- **Icones de manigance**, comparees au zoom a 01107 Hazard, 01108 Crisis, 01109 Acceleration, 16054/16069 Amplify : Crisis sl007, sl009, sl025, sl042, sl048, sl075 ; Hazard sl024, sl070 ; Acceleration sl043, sl076 (x2) ; Amplify aucune ; sl008 n'imprime aucune icone (le texte en accorde selon la position du vilain).
- **Ressources dans le texte** : poing = physique [physical], eclair = energie [energy], reseau de noeuds = mentale [mental] (comme sur Genius 01089).
- La **ligne de traits** (« TRAP! », « CONDITION. », « HAND. POSSESSED. »...) est dans `Traits`, pas dans le texte.

## Recapitulatif par set

| Set | Numeros | Faces | Exemplaires |
|---|---|---|---|
| SHADOWS IN THE NIGHT | 65001-65011 (11) | 15 | 13 |
| DARK PROTÉGÉ | 65012-65027 (16) | 22 | 16 |
| NINJA SWARM | 65028-65036 (9) | 9 | 9 |
| SHADOW LABYRINTH | 65037-65045 (9) | 11 | 11 |
| DEADLY CONTRAPTIONS | 65046-65056 (11) | 11 | 11 |
| HEART OF SHADOW | 65057-65071 (15) | 17 | 17 |
| BLACK FLOWER | 65072-65078 (7) | 8 | 13 |

## Cartes

### SHADOWS IN THE NIGHT

#### sl001a (65001A) : A Barricade of Blades — MAIN SCHEME 1A, 1/13, x1
- Texte :
  > <b>Contents</b>: Shadows in the Night, Dark Protégé, and Standard encounter sets. One modular encounter set <i>(Ninja Swarm)</i>.
  > <b>Setup</b>: Put each The Streets Below environment into play. Set the Dark Protégé encounter set aside. Choose 1 random villain from that set and reveal its side A, then shuffle each card linked to that villain into the encounter deck.
- Pied : © MARVEL © 2026 FFG [icône FFG] 1A

#### sl001b (65001B) : A Barricade of Blades — MAIN SCHEME 1B, 1/13, x1
- Valeurs : StartingThreat=2 par_joueur, escalade=+1 par_joueur, TargetThreat=7 par_joueur
- Texte :
  > In expert mode, the villain gets +1 SCH and +3[per_hero] hit points.
  > <b>Forced Interrupt</b>: When the villain would be defeated on side A, instead flip it to side B, reset its hit points, and change the villain's position. Deal each player 1 facedown encounter card.
  > <b>If the villain is defeated on side B, the players win the game.</b>
- Pied : © MARVEL © 2026 FFG [icône FFG] 1B

#### sl002a (65002A) : Fortress Lockdown — MAIN SCHEME 2A, 2/13, x1
- Texte :
  > <i>While the forces on the outside hold the heroes back, ninjas on the inside lock every door and window.</i>
  > In expert mode, the villain gets +3[per_hero] hit points.
  > <b>When Revealed</b>: Change the villain's position. Each player searches the encounter deck and discard pile for a minion and reveals it. <i>(Shuffle.)</i>
- Pied : Facundo Moyano © MARVEL © 2026 FFG [icône FFG] 2A

#### sl002b (65002B) : Fortress Lockdown — MAIN SCHEME 2B, 2/13, x1
- Valeurs : StartingThreat=2 par_joueur, escalade=+1 par_joueur, TargetThreat=8 par_joueur
- Texte :
  > In expert mode, the villain gets +1 SCH and +3[per_hero] hit points.
  > <b>Forced Interrupt</b>: When the villain would be defeated on side A, instead flip it to side B, reset its hit points, and change the villain's position. Deal each player 1 facedown encounter card.
  > <b>If the villain is defeated on side B, the players win the game.</b>
  > <b>If this stage is completed, the players lose the game.</b>
- Pied : Facundo Moyano © MARVEL © 2026 FFG [icône FFG] 2B

#### sl003a (65003A) : The Streets Below — ENVIRONMENT, 3/13, x1
- Texte :
  > <b><i>VILLAIN POSITION.</i></b>
  > If both positions are the same:
  > • Each character gets +1 ATK.
  > If the positions are different:
  > • Reduce the amount of damage each character takes from each attack by 1.
  > • Threat cannot be removed from the main scheme.
- Pied : © MARVEL © 2026 FFG [icône FFG] 3A

#### sl003b (65003B) : Atop the Tenshu — ENVIRONMENT, 3/13, x1
- Texte :
  > <b><i>VILLAIN POSITION.</i></b>
  > If both positions are the same:
  > • Each character gets +1 ATK.
  > If the positions are different:
  > • Reduce the amount of damage each character takes from each attack by 1.
  > • Threat cannot be removed from the main scheme.
- Pied : © MARVEL © 2026 FFG [icône FFG] 3B

#### sl004a (65004A) : The Streets Below — ENVIRONMENT, 4/13, x1
- Texte :
  > <b><i>HERO POSITION.</i></b>
  > <b>First Player Action</b>: Resolve one of the effects below, then flip this card:
  > • Place 3 threat on the main scheme and stun your identity.
  > • Spend [physical] [physical] resources.
  > • Spend 1 resource of any type and exhaust an <b><i>AERIAL</i></b> character you control.
- Pied : © MARVEL © 2026 FFG [icône FFG] 4A

#### sl004b (65004B) : Atop the Tenshu — ENVIRONMENT, 4/13, x1
- Texte :
  > <b><i>HERO POSITION.</i></b>
  > <b>First Player Action</b>: Resolve one of the effects below, then flip this card:
  > • Deal 3 damage to your identity.
  > • Spend [energy] [energy] resources.
  > • Discard an ally or upgrade you control.
- Pied : © MARVEL © 2026 FFG [icône FFG] 4B

#### sl005 (65005) : Black Tarantula ★unique — MINION, 5/13, x1
- Traits : BRUTE, HAND
- Valeurs : SCH=2, ATK=2, HP=5
- Icones : {"nom": "icones rouges en forme de Y en bas a droite", "nombre": 3}
- Texte :
  > Guard.
  > <b>When Revealed</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, Black Tarantula attacks you; otherwise, give the villain and Black Tarantula each a tough status card.
- Pied : © MARVEL © 2026 FFG [icône FFG] 5

#### sl006 (65006) : Ghost Maker ★unique — MINION, 6/13, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=2, HP=4
- Icones : {"nom": "boost star (étoile rouge en bas a droite)", "nombre": 1}
- Texte :
  > <b>When Defeated</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, discard 1 card you control; otherwise, take 2 indirect damage.
  > <b>[star] Boost</b>: If an ally is defending against this attack, reveal this minion.
- Pied : Kyle Petchock © MARVEL © 2026 FFG [icône FFG] 6

#### sl007 (65007) : Sealed Entrances — SIDE SCHEME, 7/13, x1
- Valeurs : StartingThreat=4
- Icones : {"nom": "crisis", "nombre": 1} ; {"nom": "icones rouges en forme de Y en bas a gauche", "nombre": 2}
- Texte :
  > Assault. <i>(Basic thwarts against this scheme use ATK instead of THW.)</i>
  > <b>When Defeated</b>: Change the villain's position if it has not changed this phase.
- Pied : Eduardo Mello © MARVEL © 2026 FFG [icône FFG] 7

#### sl008 (65008) : Strategic Positioning — SIDE SCHEME, 8/13, x1
- Valeurs : StartingThreat=3 par_joueur
- Icones : {"nom": "icones rouges en forme de Y en bas a gauche", "nombre": 2}
- Texte :
  > <i>Under Shadowland, the Hand rules the streets.</i>
  > While the villain's position is The Streets Below, this scheme gains 1 acceleration icon ([acceleration]).
  > While the villain's position is Atop the Tenshu, this scheme gains 1 hazard icon ([hazard]).
- Pied : © MARVEL © 2026 FFG [icône FFG] 8

#### sl009 (65009) : Surround the Fortress — SIDE SCHEME, 9/13, x1
- Valeurs : StartingThreat=2 par_joueur
- Icones : {"nom": "crisis", "nombre": 1} ; {"nom": "icone rouge en forme de Y en bas a gauche", "nombre": 1}
- Texte :
  > <b>When Revealed</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, place 1[per_hero] threat on the main scheme; otherwise, place 1[per_hero] threat here.
- Pied : © MARVEL © 2026 FFG [icône FFG] 9

#### sl010 (65010) : Chaos in Hell's Kitchen — TREACHERY, 10/13, x2
- Icones : {"nom": "boost star (étoile rouge en bas a droite)", "nombre": 1}
- Texte :
  > <b>When Revealed</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, place 2 threat on the main scheme; otherwise, take 2 damage.
  > <b>[star] Boost</b>: Resolve this card's "<b>When Revealed</b>" ability.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG [icône FFG] 10

#### sl011 (65011) : Moonlit Silhouette — TREACHERY, 12/13, x2
- Texte :
  > <b>When Revealed (Alter-Ego)</b>: Change the villain's position if it has not changed this phase. You are confused.
  > <b>When Revealed (Hero)</b>: If the villain's position is Atop the Tenshu, the villain schemes; otherwise, the villain attacks you.
- Pied : Sebastián Guidobono © MARVEL © 2026 FFG [icône FFG] 11

### DARK PROTÉGÉ

#### sl012a (65012A) : Archpriestess ★unique — VILLAIN A, 1/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=1★, HP=15 par_joueur
- Texte :
  > <b>[star] Forced Response</b>: After Archpriestess attacks you, give a minion a tough status card. If no tough status card was placed this way, discard the top 3 cards of the encounter deck, then deal 1 minion discarded this way to yourself as a facedown encounter card.
- Pied : Bruno Frenda © MARVEL © 2026 FFG [icône FFG] 12A ; ligne de set: DARK PROTÉGÉ (1/16) / HIT POINTS 15[per_hero]

#### sl012b (65012B) : Archpriestess ★unique — VILLAIN B, 1/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Texte :
  > Steady. Toughness.
  > <b>[star] Forced Response</b>: After Archpriestess attacks you, give a minion a tough status card. If no tough status card was placed this way, discard the top 3 cards of the encounter deck, then deal 1 minion discarded this way to yourself as a facedown encounter card.
- Pied : Bruno Frenda © MARVEL © 2026 FFG [icône FFG] 12B ; ligne de set: DARK PROTÉGÉ (1/16) / HIT POINTS 18[per_hero]

#### sl013a (65013A) : Daredevil ★unique — VILLAIN A, 2/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=2, HP=15 par_joueur
- Texte :
  > <b>Forced Response</b>: After you or an ally you control attacks Daredevil, choose: Either discard 1 random card from your hand, or Daredevil attacks you. (Limit once per round per player.)
- Citation : "Hell's Kitchen is now under the protection of the Hand!"
- Pied : Joey Vazquez © MARVEL © 2026 FFG [icône FFG] 13A ; ligne de set: DARK PROTÉGÉ (2/16) / HIT POINTS 15[per_hero]

#### sl013b (65013B) : Daredevil ★unique — VILLAIN B, 2/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=2, ATK=2, HP=18 par_joueur
- Texte :
  > Steady. Toughness.
  > <b>Forced Response</b>: After you or an ally you control attacks Daredevil, choose: Either discard 1 random card from your hand, or Daredevil attacks you. (Limit once per round per player.)
- Pied : Joey Vazquez © MARVEL © 2026 FFG 13B

#### sl014a (65014A) : Elektra ★unique — VILLAIN A, 3/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=2★, HP=15 par_joueur
- Icones : étoile (★) à côté de l'ATK 2
- Texte :
  > [star] <b>Forced Interrupt</b>: When Elektra attacks you, discard the top card of your deck. If that card's printed cost is an odd number, Elektra gets +1 ATK for this attack; otherwise, this attack gains overkill and piercing.
- Citation : "The Hand guides me, and death follows."
- Pied : Joey Vazquez © MARVEL © 2026 FFG 14A

#### sl014b (65014B) : Elektra ★unique — VILLAIN B, 3/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Icones : étoile (★) à côté de l'ATK 2
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Interrupt</b>: When Elektra attacks you, discard the top card of your deck. If that card's printed cost is an odd number, Elektra gets +1 ATK for this attack; otherwise, this attack gains overkill and piercing.
- Pied : Joey Vazquez © MARVEL © 2026 FFG 14B

#### sl015a (65015A) : Gorgon ★unique — VILLAIN A, 4/16, x1
- Traits : HAND
- Valeurs : SCH=1, ATK=2★, HP=15 par_joueur
- Icones : étoile (★) à côté de l'ATK 2
- Texte :
  > [star] <b>Forced Interrupt</b>: When Gorgon attacks you, choose:
  > • Spend a [physical] resource.
  > • Stun your identity.
  > • Take 2 indirect damage.
- Citation : "I've died and been born again. There is nothing I fear."
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 15A

#### sl015b (65015B) : Gorgon ★unique — VILLAIN B, 4/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Icones : étoile (★) à côté de l'ATK 2
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Interrupt</b>: When Gorgon attacks you, choose:
  > • Spend a [physical] resource.
  > • Stun your identity.
  > • Take 2 indirect damage.
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 15B

#### sl016a (65016A) : Lady Bullseye ★unique — VILLAIN A, 5/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=1★, HP=15 par_joueur
- Icones : étoile (★) à côté de l'ATK 1
- Texte :
  > [star] <b>Forced Response</b>: After Lady Bullseye attacks you, if that attack was undefended, take 1 indirect damage; otherwise, place 1 threat on the main scheme.
- Citation : "I plan to take my time with you."
- Pied : Joey Vazquez © MARVEL © 2026 FFG 16A

#### sl016b (65016B) : Lady Bullseye ★unique — VILLAIN B, 5/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Icones : étoile (★) à côté de l'ATK 2
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Response</b>: After Lady Bullseye attacks you, if that attack was undefended, take 1 indirect damage; otherwise, place 1 threat on the main scheme.
- Pied : Joey Vazquez © MARVEL © 2026 FFG 16B

#### sl017a (65017A) : White Tiger ★unique — VILLAIN A, 6/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=0★, HP=15 par_joueur
- Icones : étoile (★) à côté de l'ATK 0
- Texte :
  > [star] <b>Forced Response</b>: After White Tiger attacks you, she attacks you again with +1 ATK. (Limit once per round per player.)
- Citation : "Civilization will fall into chaos and darkness, and we who walk the left-hand path will kneel before the Beast!"
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 17A

#### sl017b (65017B) : White Tiger ★unique — VILLAIN B, 6/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=1★, HP=18 par_joueur
- Icones : étoile (★) à côté de l'ATK 1
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Response</b>: After White Tiger attacks you, she attacks you again. (Limit once per round per player.)
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 17B (pied partiellement coupé en bas de l'image)

#### sl018 (65018) : Art of the Kill — ATTACHMENT, 7/16, x1
- Icones : icône d'ensemble de rencontre (Y rouge) en bas à droite
- Texte :
  > Linked (Elektra, Lady Bullseye, or White Tiger).
  > Attach to your identity.
  > <b>Forced Interrupt</b>: When an enemy attacks you, it gets +1 ATK for that attack. If that attack defeats a character, place 1 threat on the main scheme.
  > <b>Alter-Ego Action</b>: Spend [energy] [mental] [physical] resources → discard this card.
- Pied : Rowel Palapar © MARVEL © 2026 FFG 18

#### sl019 (65019) : Krahllak's Blessing — ATTACHMENT, 8/16, x1
- Traits : CONDITION, SPELL
- Icones : icône d'ensemble de rencontre (Y rouge) en bas à droite
- Texte :
  > Linked (Archpriestess, Daredevil, or Gorgon).
  > Attach to the villain.
  > <b>Forced Interrupt</b>: When attached villain would take any amount of damage from a character, reduce that amount by 3. Attached villain attacks that character. Discard this card.
- Pied : © MARVEL © 2026 FFG 19

#### sl020 (65020) : Archpriestess ★unique — MINION, 9/16, x1
- Traits : HAND, MYSTIC
- Valeurs : SCH=2, ATK=1, Boost=5
- Icones : boost 5 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Gorgon, Lady Bullseye, or White Tiger).
  > Villainous.
  > <b>When Revealed</b>: Each other minion engaged with you attacks you. If no attack was made this way, discard the top 3 cards of the encounter deck.
- Pied : © MARVEL © 2026 FFG 20

#### sl021 (65021) : Gorgon ★unique — MINION, 10/16, x1
- Traits : BRUTE, HAND
- Valeurs : SCH=0, ATK=1, Boost=5
- Icones : boost 5 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Daredevil, Elektra, or Lady Bullseye).
  > Guard. Villainous.
  > <b>Forced Response</b>: After a character attacks and damages Gorgon, stun that character.
- Pied : © MARVEL © 2026 FFG 21

#### sl022 (65022) : Lady Bullseye ★unique — MINION, 11/16, x1
- Traits : HAND
- Valeurs : SCH=1, ATK=1★, Boost=5
- Icones : boost 5 ; étoile (★) à côté de l'ATK 1 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Archpriestess, Gorgon, or White Tiger).
  > Villainous.
  > [star] <b>Forced Interrupt</b>: When Lady Bullseye attacks you, this attack gains ranged and she attacks the ally with the highest printed cost you control, if able.
- Pied : © MARVEL © 2026 FFG 22

#### sl023 (65023) : White Tiger ★unique — MINION, 12/16, x1
- Traits : HAND
- Valeurs : SCH=1, ATK=2, Boost=5
- Icones : boost 5 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Archpriestess, Daredevil, or Elektra).
  > Villainous.
  > <b>When Revealed</b>: Take 2 indirect damage.
- Pied : © MARVEL © 2026 FFG 23

#### sl024 (65024) : Rite of Offering — SIDE SCHEME, 13/16, x1
- Valeurs : StartingThreat=1
- Icones : h ; a ; z ; a ; r ; d
- Texte :
  > Linked (Archpriestess, Elektra, or White Tiger).
  > <b>When Defeated</b>: The defeating player removes an ally they control from the game. If no ally was removed this way, that player takes 3 damage.
- Pied : © MARVEL © 2026 FFG 24

#### sl025 (65025) : Shadowy Plot — SIDE SCHEME, 14/16, x1
- Valeurs : StartingThreat=2
- Icones : c ; r ; i ; s ; i ; s
- Texte :
  > Linked (Daredevil, Gorgon, or Lady Bullseye).
  > <b>When Defeated</b>: The defeating player looks at the top 3 cards of the encounter deck, reveals 1 of them, and discards the rest.
- Pied : © MARVEL © 2026 FFG 25

#### sl026 (65026) : Darkness Within — TREACHERY, 15/16, x1
- Icones : boost : 1 étoile rouge (★) ; 1 icône d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Archpriestess, Gorgon, or Lady Bullseye).
  > <b>When Revealed</b>: Change to hero form. The villain attacks you.
  > ---
  > [star] <b>Boost</b>: If this activation is an attack, it gains overkill.
- Pied : © MARVEL © 2026 FFG 26

#### sl027 (65027) : Embraced by Darkness — TREACHERY, 16/16, x1
- Icones : boost : 1 étoile rouge (★) ; 1 icône d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Daredevil, Elektra, or White Tiger).
  > <b>When Revealed</b>: The villain schemes. If 2 or less threat was placed on the main scheme this way, discard the top 3 cards of the encounter deck.
  > ---
  > [star] <b>Boost</b>: If this activation is an attack, place 2 threat on the main scheme.
- Pied : Eduardo Mello © MARVEL © 2026 FFG 27

### NINJA SWARM

#### sl028 (65028) : Black Mountain ★unique — MINION, 1/9, x1
- Traits : BRUTE, HAND, NINJA
- Valeurs : SCH=2, ATK=2, cout=5
- Icones : étoile boost (bas droite)
- Texte :
  > Guard.
  > While Black Mountain is engaged with you, each other <b>NINJA</b> minion engaged with you cannot be attacked.
  > <b>★ Boost</b>: If an ally is defending against this attack, reveal this minion.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 28

#### sl029 (65029) : Kirigi ★unique — MINION, 2/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=2, cout=3
- Icones : étoile boost (bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>).
  > <b>When Defeated</b>: The defeating player either spends 2 resources of any type or shuffles Kirigi into the encounter deck.
  > <b>★ Boost</b>: If an ally is defending against this attack, this card gains [boost][boost] and this attack gains overkill.
- Pied : Sebastián Guidobono © MARVEL © 2026 FFG 29

#### sl030 (65030) : Bo Staff Ninja — MINION, 3/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1, cout=2
- Icones : boost x2 (deux icones Y rouges bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>). Toughness.
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 30

#### sl031 (65031) : Fukiya Ninja — MINION, 4/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1★, cout=2
- Icones : boost x1 (icone Y rouge bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>).
  > ★ This minion's attacks gain ranged.
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- Pied : Aitor Prieto © MARVEL © 2026 FFG 31

#### sl032 (65032) : Katana Ninja — MINION, 5/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1, cout=2
- Icones : boost x1 (icone Y rouge bas droite)
- Texte :
  > Guard. Teamwork (<b>NINJA</b>).
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- Pied : © MARVEL © 2026 FFG 32

#### sl033 (65033) : Kusarigama Ninja — MINION, 6/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1, cout=2
- Icones : boost x2 (deux icones Y rouges bas droite)
- Texte :
  > Patrol. Teamwork (<b>NINJA</b>).
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- Pied : © MARVEL © 2026 FFG 33

#### sl034 (65034) : Shuriken Ninja — MINION, 7/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1★, cout=2
- Icones : boost x1 (icone Y rouge bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>).
  > ★ This minion's attacks gain piercing.
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- Pied : © MARVEL © 2026 FFG 34

#### sl035 (65035) : Dancing Shadows — SIDE SCHEME, 8/9, x1
- Valeurs : StartingThreat=3
- Icones : étoile boost (bas gauche)
- Texte :
  > Each <b>NINJA</b> minion gets +1 hit point.
  > Threat cannot be removed from this scheme while at least 1 <b>NINJA</b> minion is in play.
  > <b>★ Boost</b>: Reveal this card.
- Pied : © MARVEL © 2026 FFG 35

#### sl036 (65036) : Countless Numbers — TREACHERY, 9/9, x1
- Icones : étoile boost + 1 icone Y rouge (bas droite)
- Texte :
  > Surge.
  > <b>When Revealed</b>: Shuffle each <b>NINJA</b> minion in the encounter discard pile into the encounter deck.
  > <b>★ Boost</b>: Resolve this card's "<b>When Revealed</b>" ability.
- Pied : © MARVEL © 2026 FFG 36

### SHADOW LABYRINTH

#### sl037 (65037) : Shifting Corridors — VILLAIN A, 1/11, x1
- Traits : LOCATION
- Valeurs : SCH=0★, ATK=0★, HP=∞
- Texte :
  > Stalwart.
  > <b>★ Forced Interrupt</b>: When Shifting Corridors would activate against you, instead remove 1 passage counter from here and reveal the top card of the trap deck.
  > <b>If the last passage counter is removed from here, the players lose the game.</b>
- Pied : HIT POINTS ∞ ; Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 37

#### sl038a (65038A) : Into the Labyrinth — MAIN SCHEME 1A, 2/11, x1
- Texte :
  > <b>Contents</b>: Shifting Corridors (A). Shadow Labyrinth, Dark Protégé, Deadly Contraptions, and Standard encounter sets. One modular encounter set <i>(Ninja Swarm)</i>.
  > <b>Setup</b>: Create the trap deck <i>(see rulebook, p. 12)</i>. Set the Dark Protégé encounter set aside. Choose 1 random villain from that set, then shuffle each card linked to that villain into the encounter deck <i>(keep the chosen villain set aside)</i>.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 38A

#### sl038b (65038B) : Into the Labyrinth — MAIN SCHEME 1B, 2/11, x1
- Valeurs : StartingThreat=25 par_joueur, escalade=+1 par_joueur, TargetThreat=∞, niveau_etape=1
- Texte :
  > <b>When Revealed:</b> Place 10[per_hero] passage counters on Shifting Corridors (7[per_hero] instead in expert mode).
  > <b>Forced Interrupt</b>: When Shifting Corridors would take any amount of damage, remove that much threat from here instead.
  > <b>Forced Interrupt</b>: When the last threat is removed from this scheme, advance to stage 2A <i>(the players win by advancing)</i>.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 38B

#### sl039a (65039A) : Chamber of Vile Secrets — MAIN SCHEME 2A, 3/11, x1
- Texte :
  > <b>When Revealed</b>: Do each of the following:
  > 1. Set Shifting Corridors aside.
  > 2. Find the chosen Dark Protégé villain. Discard each status card, token, and attached card from it.
  > 3. Reveal the chosen villain's side A (side B instead in expert mode).
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 39A

#### sl039b (65039B) : Chamber of Vile Secrets — MAIN SCHEME 2B, 3/11, x1
- Valeurs : StartingThreat=1 par_joueur, escalade=+1 par_joueur, TargetThreat=9 par_joueur, niveau_etape=2
- Texte :
  > <b>When Revealed</b>: In expert mode, the villain activates against each player.
  > <b>Forced Response</b>: After you or an ally you control thwarts this scheme, reveal the top card of the trap deck. (Limit once per round per player.)
  > <b>If this stage is completed, the players lose the game.</b>
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 39B

#### sl040 (65040) : Whisper in the Dark — ATTACHMENT, 4/11, x1
- Texte :
  > <i>TRAP!</i>
  > Treat attached villain as an <b>ELITE</b> minion with 6 printed hit points. It gains: "Guard. Villainous. <b>When Defeated</b>: Set this minion aside."
  > <b>When Revealed</b>: If Shifting Corridors is in play, put the set-aside chosen villain into play engaged with you, side A faceup, with this card attached; otherwise, set this card aside and the villain schemes.
- Pied : © MARVEL © 2026 FFG 40

#### sl041 (65041) : Lord Deathstrike ★unique — MINION, 5/11, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2, cout=5
- Icones : étoile boost (bas droite)
- Texte :
  > Patrol.
  > <b>When Revealed</b>: If Shifting Corridors is in play, shuffle the top 2 cards of the encounter deck into the trap deck; otherwise, reveal the top card of the trap deck.
  > <b>★ Boost</b>: Put this minion into play engaged with you.
- Pied : © MARVEL © 2026 FFG 41

#### sl042 (65042) : Dead End — SIDE SCHEME, 6/11, x1
- Valeurs : StartingThreat=2 par_joueur
- Icones : boost x3 (trois icones Y rouges, bord gauche) ; icone crisis (point d'exclamation dans un eclat)
- Texte :
  > Assault. <i>(Basic thwarts against this scheme use ATK instead of THW.)</i>
  > <b>When Revealed</b>: If Shifting Corridors is in play, remove 1 passage counter from it; otherwise, place 1[per_hero] threat here.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 42

#### sl043 (65043) : Hall of Hidden Doors — SIDE SCHEME, 7/11, x1
- Valeurs : StartingThreat=3
- Icones : étoile boost (bas gauche) ; icone acceleration (croix sur forme de toit)
- Texte :
  > <b>When Defeated</b>: The defeating player removes 5 threat from the main scheme. They discard cards from the encounter deck until a minion or side scheme is discarded, then reveal it.
  > <b>★ Boost</b>: Place 3 threat on the main scheme.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 43

#### sl044 (65044) : No Time to Think! — TREACHERY, 8/11, x2
- Icones : [ ; " ; b ; o ; o ; s ; t ;   ; ★ ;   ; ( ; e ; t ; o ; i ; l ; e ;   ; r ; o ; u ; g ; e ;   ; i ; s ; o ; l ; e ; e ; ) ; " ; , ;   ; " ; b ; o ; o ; s ; t ;   ; x ; 1 ;   ; ( ; c ; h ; e ; v ; r ; o ; n ;   ; r ; o ; u ; g ; e ;   ; e ; n ;   ; Y ; ) ; " ; ]
- Texte :
  > Peril. <i>(While you are resolving this card, other players cannot help you.)</i>
  > <b>When Revealed</b>: The villain activates against you.
  > ★ <b>Boost</b>: If this activation is an attack, this card gains [boost][boost] and this attack gains overkill.
- Pied : Kyle Petchock © MARVEL © 2026 FFG 44

#### sl045 (65045) : Sudden Shift — TREACHERY, 10/11, x2
- Icones : [ ; " ; b ; o ; o ; s ; t ;   ; ★ ;   ; ( ; e ; t ; o ; i ; l ; e ;   ; r ; o ; u ; g ; e ;   ; i ; s ; o ; l ; e ; e ; ) ; " ; , ;   ; " ; b ; o ; o ; s ; t ;   ; x ; 2 ;   ; ( ; c ; h ; e ; v ; r ; o ; n ; s ;   ; r ; o ; u ; g ; e ; s ;   ; e ; n ;   ; Y ; ) ; " ; ]
- Texte :
  > <b>When Revealed</b>: Shuffle the trap discard pile and the top 3 cards of the encounter deck into the trap deck. Reveal the top card of the trap deck.
  > ★ <b>Boost</b>: Shuffle the trap discard pile and the top 2 cards of the encounter deck into the trap deck.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 45

### DEADLY CONTRAPTIONS

#### sl046 (65046) : Nervous Jitters — ATTACHMENT, 1/11, x1
- Traits : CONDITION
- Icones : boost x1 (chevron rouge en Y)
- Texte :
  > Attach to your identity.
  > <b>Forced Interrupt</b>: When you choose the "<i>Avoid</i>" effect or the "<i>Disarm</i>" effect on a <b>TRAP!</b> card, name an encounter card type, then discard the top card of the encounter deck. If the card discarded this way was not of the named type, take 4 indirect damage and discard this attachment.
- Pied : Eduardo Mello © MARVEL © 2026 FFG 46

#### sl047 (65047) : Iron Monk ★unique — MINION, 2/11, x1
- Traits : HAND, MYSTIC
- Valeurs : SCH=2, ATK=1, HP=4
- Icones : boost x2 (chevrons rouges en Y)
- Texte :
  > Patrol. Toughness.
  > While Iron Monk is engaged with you, you cannot choose the "<i>Avoid</i>" effect on <b>TRAP!</b> cards.
- Citation : "Your only path is through me. Let us begin."
- Pied : Facundo Moyano © MARVEL © 2026 FFG 47

#### sl048 (65048) : Hall of Punishment — SIDE SCHEME, 3/11, x1
- Valeurs : StartingThreat=2 par_joueur
- Icones : [ ; " ; c ; r ; i ; s ; i ; s ;   ; ( ; ! ; ! ;   ; d ; a ; n ; s ;   ; u ; n ;   ; e ; c ; l ; a ; t ; ) ; " ; , ;   ; " ; b ; o ; o ; s ; t ;   ; ★ ;   ; ( ; e ; t ; o ; i ; l ; e ;   ; r ; o ; u ; g ; e ;   ; i ; s ; o ; l ; e ; e ; , ;   ; b ; a ; s ;   ; g ; a ; u ; c ; h ; e ; ) ; " ; ]
- Texte :
  > <b>Forced Interrupt</b>: When you choose the "<i>Trip</i>" effect on a <b>TRAP!</b> card, discard the top 3 cards of your deck.
  > ★ <b>Boost</b>: Place 1 threat on the main scheme for each character you control.
- Pied : Facundo Moyano © MARVEL © 2026 FFG 48

#### sl049 (65049) : Path of a Thousand Cuts — SIDE SCHEME, 4/11, x1
- Valeurs : StartingThreat=5
- Icones : [ ; " ; b ; o ; o ; s ; t ;   ; ★ ;   ; ( ; e ; t ; o ; i ; l ; e ;   ; r ; o ; u ; g ; e ;   ; i ; s ; o ; l ; e ; e ; , ;   ; b ; a ; s ;   ; g ; a ; u ; c ; h ; e ; ) ; " ; ]
- Texte :
  > <i>Every step is a test of resilience.</i>
  > <b>Forced Interrupt</b>: When you choose the "<i>Avoid</i>" effect or the "<i>Trip</i>" effect on a <b>TRAP!</b> card, take 2 indirect damage.
  > ★ <b>Boost</b>: Deal 1 damage to each character you control.
- Pied : Kyle Petchock © MARVEL © 2026 FFG 49

#### sl050 (65050) : Blinding Powder — TREACHERY, 5/11, x1
- Traits : TRAP
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard a <b>THWART</b> event from your hand.
  > • <i>Disarm</i> — Discard 2 cards at random from your hand, then give a character you control a tough status card.
  > • <i>Trip</i> — Deal 2 damage to your identity and confuse it.
- Pied : Kyle Petchock © MARVEL © 2026 FFG 50

#### sl051 (65051) : Caltrops — TREACHERY, 6/11, x1
- Traits : TRAP
- Icones : boost x1
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard a <b>DEFENSE</b> event from your hand.
  > • <i>Disarm</i> — Discard 1 identity-specific card from your hand, then deal 2 damage to an enemy.
  > • <i>Trip</i> — Deal 2 damage to your identity and stun it.
- Pied : Aitor Prieto © MARVEL © 2026 FFG 51

#### sl052 (65052) : Flame Spout — TREACHERY, 7/11, x1
- Traits : TRAP
- Icones : boost x3
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard an ally from your hand.
  > • <i>Disarm</i> — Discard an ally you control, then draw 2 cards.
  > • <i>Trip</i> — Deal 3 damage to your identity. Discard the top 3 cards of your deck.
- Pied : Facundo Moyano © MARVEL © 2026 FFG 52

#### sl053 (65053) : Oil Slick — TREACHERY, 8/11, x1
- Traits : TRAP
- Icones : boost x1
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard an upgrade from your hand.
  > • <i>Disarm</i> — Discard an upgrade you control, then remove 4 threat from the main scheme.
  > • <i>Trip</i> — Discard 1 card from your hand. Discard the top 8 cards of your deck.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 53

#### sl054 (65054) : Poison Darts — TREACHERY, 9/11, x1
- Traits : TRAP
- Icones : boost x2
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Spend [energy] [energy] resources.
  > • <i>Disarm</i> — Spend [mental] [mental] [physical] resources, then deal 3 damage to the villain.
  > • <i>Trip</i> — Deal 3 damage to your identity and exhaust it.
- Pied : Eduardo Mello © MARVEL © 2026 FFG 54

#### sl055 (65055) : Pressure Plate — TREACHERY, 10/11, x1
- Traits : TRAP
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Spend [mental] [mental] resources.
  > • <i>Disarm</i> — Spend [energy] [physical] [physical] resources, then search the top 4 cards of your deck for a card and add it to your hand. <i>(Shuffle.)</i>
  > • <i>Trip</i> — Discard cards from the top of the encounter deck until a minion is discarded, then reveal it.
- Pied : Eduardo Mello © MARVEL © 2026 FFG 55

#### sl056 (65056) : Tripwire — TREACHERY, 11/11, x1
- Traits : TRAP
- Icones : boost x2
- Texte :
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard an <b>ATTACK</b> event from your hand.
  > • <i>Disarm</i> — Discard a support you control, then remove 3 threat from a scheme.
  > • <i>Trip</i> — Discard cards from the top of the encounter deck until a side scheme is discarded, then reveal it.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 56

### HEART OF SHADOW

#### sl057 (65057) : Krahllak ★unique — VILLAIN, 1/17, x1
- Traits : DEMON, HAND
- Valeurs : niveau_etape=I, SCH=2, ATK=3★ (etoile en exposant), HP=18 par_joueur
- Texte :
  > Steady.
  > ★ <b>Interrupt</b>: When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
- Citation : "There is only the Beast!"
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 57

#### sl058 (65058) : Krahllak ★unique — VILLAIN, 2/17, x1
- Traits : DEMON, HAND
- Valeurs : niveau_etape=II, SCH=2, ATK=4★, HP=21 par_joueur
- Texte :
  > Steady. Toughness.
  > ★ Krahllak's attacks gain overkill.
  > ★ <b>Interrupt</b>: When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 58

#### sl059 (65059) : Krahllak ★unique — VILLAIN, 3/17, x1
- Traits : DEMON, HAND
- Valeurs : niveau_etape=III, SCH=3, ATK=4★, HP=25 par_joueur
- Texte :
  > Retaliate 1. Steady. Toughness.
  > ★ Krahllak's attacks gain overkill and piercing.
  > ★ <b>Interrupt</b>: When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
- Pied : Bruno Frenda & Sara Cuomo © MARVEL © 2026 FFG 59

#### sl060a (65060A) : Dark Invitation — MAIN SCHEME 1A, 4/17, x1
- Valeurs : niveau_etape=1A
- Texte :
  > <b>Contents</b>: Krahllak (I) and Krahllak (II). <i>(Krahllak (II) and Krahllak (III) instead for expert mode.)</i> Heart of Shadow, Black Flower, and Standard encounter sets. One modular encounter set <i>(Ninja Swarm)</i>.
  > <b>Setup</b>: Each player puts a Creeping Corruption upgrade into play. Set the rest aside.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 60A

#### sl060b (65060B) : Dark Invitation — MAIN SCHEME 1B, 4/17, x1
- Valeurs : StartingThreat=2 par_joueur, escalade=+1 par_joueur, TargetThreat=6 par_joueur, niveau_etape=1B
- Texte :
  > <b>Forced Interrupt</b>: When this stage would be completed, instead remove all threat from here and each player chooses:
  > • Place 2 corruption counters on their Creeping Corruption.
  > • Take 3 damage and deal themself 1 facedown encounter card.
  > <b>Forced Response</b>: After Krahllak is defeated, advance this scheme to stage 2A.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 60B

#### sl061a (65061A) : Beast Be Praised — MAIN SCHEME 2A, 5/17, x1
- Valeurs : niveau_etape=2A
- Texte :
  > <i>An inferno erupts in the throne room, punishing those who have yet to succumb to Krahllak's dark will.</i>
  > <b>When Revealed</b>: Each player whose Creeping Corruption has the <b>OVERPOWERING</b> trait discards 1 random card from their hand. Each other player discards a card they control from play. In expert mode, deal each player 1 facedown encounter card.
- Pied : © MARVEL © 2026 FFG 61A

#### sl061b (65061B) : Beast Be Praised — MAIN SCHEME 2B, 5/17, x1
- Valeurs : TargetThreat=9 par_joueur, StartingThreat=2 par_joueur, escalade=+1 par_joueur ★, niveau_etape=2
- Icones : acceleration/escalade: +1 par_joueur étoile (encart bas droite)
- Texte :
  > [star] <b>Forced Response</b>: After resolving step one of the villain phase, each player chooses:
  > • Place 1 corruption counter on their Creeping Corruption.
  > • Place 3 threat here.
  > <b>If this stage is completed, the players lose the game.</b>
- Pied : © MARVEL © 2026 FFG 61B

#### sl062 (65062) : Dark Shroud — ATTACHMENT, 6/17, x1
- Traits : SPELL
- Valeurs : ATK=+1
- Icones : marqueur de set rouge en Y x1 (bas droite)
- Texte :
  > Attach to Krahllak.
  > <b>Interrupt</b>: When you or an ally you control would deal 4 or more damage to Krahllak with an attack, instead prevent all of that damage, place 1 corruption counter on your Creeping Corruption, and discard this card.
- Pied : Eduardo Mello © MARVEL © 2026 FFG 62

#### sl063 (65063) : Fear Projection — ATTACHMENT, 7/17, x1
- Traits : SPELL
- Icones : aucune icône de boost visible ; marqueur rouge en Y x1 (bas droite)
- Texte :
  > Attach to Krahllak.
  > Krahllak gains retaliate 1.
  > <b>Hero Action</b>: Place 2 corruption counters on your Creeping Corruption → discard this card.
  > <b>Alter-Ego Action</b>: Spend [mental] [mental] [mental] resources → discard this card. Remove 1 corruption counter from your Creeping Corruption.
- Pied : © MARVEL © 2026 FFG 63

#### sl064 (65064) : Mark of the Wicked — ATTACHMENT, 8/17, x1
- Traits : SPELL
- Valeurs : ATK=+2 avec étoile
- Icones : ATK +2 [star] ; marqueur rouge en Y x3 (bas droite)
- Texte :
  > <b>When Revealed</b>: You may attach this card to your identity. If you do not, take 4 damage, stun your identity, remove 1 corruption counter from your Creeping Corruption, and discard this card.
  > [star] <b>Forced Response</b>: After attached hero makes a basic attack, place 1 corruption counter on your Creeping Corruption.
- Pied : © MARVEL © 2026 FFG 64

#### sl065 (65065) : Pull of Power — ATTACHMENT, 9/17, x1
- Traits : SPELL
- Valeurs : THW=+2 avec étoile
- Icones : THW +2 [star] ; marqueur rouge en Y x2 (bas droite)
- Texte :
  > <b>When Revealed</b>: You may attach this card to your identity. If you do not, take 4 damage, confuse your identity, remove 1 corruption counter from your Creeping Corruption, and discard this card.
  > [star] <b>Forced Response</b>: After attached hero makes a basic thwart, place 1 corruption counter on your Creeping Corruption.
- Pied : © MARVEL © 2026 FFG 65

#### sl066 (65066) : Fist ★unique — MINION, 10/17, x1
- Traits : HAND, UNDEAD
- Valeurs : SCH=2, ATK=2, HP=6
- Icones : marqueur rouge en Y x2 (bas droite)
- Texte :
  > Patrol. Retaliate 2.
  > <b>Hero Action</b>: Place 1 corruption counter on your Creeping Corruption → deal 4 damage to Fist.
- Citation : A half-dead monstrosity brought to life by the mystical arts of the Hand, Fist won't stop until its mission is complete.
- Pied : © MARVEL © 2026 FFG 66

#### sl067 (65067) : Hellbride ★unique — MINION, 11/17, x1
- Traits : DEMON, HAND
- Valeurs : SCH=1, ATK=3, HP=7
- Icones : marqueur rouge en Y x3 (bas droite)
- Texte :
  > <b>When Defeated</b>: The defeating player places 2 corruption counters on their Creeping Corruption, then heals 6 damage from their identity.
  > <b>Hero Action</b>: If Hellbride has 2 or fewer remaining hit points, exhaust your hero → discard Hellbride. Remove 1 corruption counter from your Creeping Corruption.
- Pied : © MARVEL © 2026 FFG 67

#### sl068 (65068) : Retainer ★unique — MINION, 12/17, x1
- Traits : BRUTE, DEMON, HAND
- Valeurs : SCH=1, ATK=4 avec étoile, HP=9
- Icones : ATK 4 [star] ; marqueur rouge en Y x3 (bas droite)
- Texte :
  > [star] Retainer's attacks gain overkill.
  > [star] <b>Interrupt</b>: When Retainer attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Retainer gets –3 ATK for this attack.
- Citation : Krahllak's avatar, summoned to exact vengeance.
- Pied : © MARVEL © 2026 FFG 68

#### sl069 (65069) : Snakeroot Elders ★unique — MINION, 13/17, x1
- Traits : HAND, MYSTIC, NINJA
- Valeurs : SCH=1, ATK=2, HP=8
- Icones : marqueur rouge en Y x3 (bas droite)
- Texte :
  > While there is at least 1 corruption counter here, Snakeroot Elders gains guard and patrol.
  > <b>When Revealed</b>: You may place 1 corruption counter on your Creeping Corruption. If you do not, place 1 corruption counter here.
- Pied : © MARVEL © 2026 FFG 69

#### sl070 (65070) : Veil of Nightmares — SIDE SCHEME, 14/17, x2
- Valeurs : menace_de_depart=5 par_joueur
- Icones : [ ; " ; b ; o ; o ; s ; t ;   ; x ; 2 ;   ; ( ; r ; o ; u ; g ; e ;   ; e ; n ;   ; Y ;   ; x ; 2 ; , ;   ; b ; a ; s ;   ; g ; a ; u ; c ; h ; e ; ) ; " ; , ;   ; " ; h ; a ; z ; a ; r ; d ;   ; ( ; c ; a ; r ; t ; e ;   ; a ; v ; e ; c ;   ; + ;   ; i ; n ; c ; l ; i ; n ; é ; e ; , ;   ; n ; o ; i ; r ; e ; , ;   ; c ; e ; n ; t ; r ; e ; ) ; " ; ]
- Texte :
  > <i>Krahllak's dark magic can tap into a person's deepest fears.</i>
  > <b>Hero Action</b>: Place 1 corruption counter on your Creeping Corruption → remove 5 threat from this scheme.
- Pied : Kyle Petchock © MARVEL © 2026 FFG 70

#### sl071 (65071) : Submit or Suffer — TREACHERY, 16/17, x2
- Icones : boost: 1 étoile rouge [star] (bas droite)
- Texte :
  > <b>When Revealed</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or remove 1 corruption counter from your Creeping Corruption and Krahllak attacks you.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or stun your identity.
- Pied : © MARVEL © 2026 FFG 71

### BLACK FLOWER

#### sl072a (65072A) : Creeping Corruption — UPGRADE A, 1/13, x4
- Icones : petit rectangle blanc en haut à gauche (emplacement/coût vide)
- Texte :
  > Permanent. Setup. Max 1 per player.
  > If there are at least 5 corruption counters here, remove each of them from here and flip this card.
  > <b>Action</b>: Exhaust Creeping Corruption and place 1 corruption counter here → draw 1 card.
- Pied : Sebastián Guidobono © MARVEL © 2026 FFG 72A

#### sl072b (65072B) : Creeping Corruption — UPGRADE B, 1/13, x4
- Traits : OVERPOWERING
- Icones : petit rectangle blanc en haut à gauche
- Texte :
  > Permanent. Max 1 per player.
  > <b>If there are at least 5 corruption counters here, you are defeated.</b>
  > <b>Action</b>: Exhaust Creeping Corruption and place 1 corruption counter here → draw 2 cards, then discard 1 card from your hand.
- Pied : Sebastián Guidobono © MARVEL © 2026 FFG 72B

#### sl073 (65073) : Aka ★unique — MINION, 5/13, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=3 avec étoile, HP=6
- Icones : ATK 3 [star] ; boost: 1 étoile rouge [star] + marqueur rouge en Y x1 (bas droite)
- Texte :
  > Quickstrike. Villainous.
  > [star] <b>Interrupt</b>: When Aka would attack you, you may place 1 corruption counter on your Creeping Corruption. If you do, cancel that attack.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or discard 1 random card from your hand.
- Pied : © MARVEL © 2026 FFG 73

#### sl074 (65074) : Tongue of the Beast ★unique — MINION, 6/13, x1
- Traits : DEMON, HAND
- Valeurs : SCH=1, ATK=2, HP=1
- Icones : boost: 1 étoile rouge [star] (bas droite)
- Texte :
  > <b>When Defeated</b>: The defeating player places 2 corruption counters on their Creeping Corruption.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or this card gains [boost][boost][boost].
- Pied : © MARVEL © 2026 FFG 74

#### sl075 (65075) : Binding Ritual — SIDE SCHEME, 7/13, x2
- Valeurs : menace_de_depart=1 par_joueur
- Icones : marqueur rouge en Y x2 (bas gauche) ; icône centrale : point d'exclamation dans un éclat (crisis probable)
- Texte :
  > <i>"He whom we serve shall reign supreme!"</i>
  > <i>—Takashi</i>
  > <b>When Revealed</b>: Each player chooses:
  > • Place 1 corruption counter on their Creeping Corruption.
  > • Place 3 threat here.
- Citation : "He whom we serve shall reign supreme!" —Takashi
- Pied : © MARVEL © 2026 FFG 75

#### sl076 (65076) : Roots of a Black Flower — SIDE SCHEME, 9/13, x1
- Valeurs : menace_de_depart=1
- Icones : [ ; " ; b ; o ; o ; s ; t ;   ; é ; t ; o ; i ; l ; e ;   ; [ ; s ; t ; a ; r ; ] ;   ; ( ; b ; a ; s ;   ; g ; a ; u ; c ; h ; e ; ) ; " ; , ;   ; " ; a ; c ; c ; e ; l ; e ; r ; a ; t ; i ; o ; n ;   ; x ; 2 ;   ; ( ; m ; a ; i ; s ; o ; n ; / ; t ; o ; i ; t ;   ; a ; v ; e ; c ;   ; + ;   ; e ; t ;   ; b ; a ; r ; r ; e ; , ;   ; d ; e ; u ; x ;   ; f ; o ; i ; s ; , ;   ; c ; e ; n ; t ; r ; e ; ) ; " ; ]
- Texte :
  > <b>When Defeated</b>: The defeating player places 2 corruption counters on their Creeping Corruption.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or place 4 threat on the main scheme.
- Pied : Kyle Petchock © MARVEL © 2026 FFG 76

#### sl077 (65077) : Malediction — TREACHERY, 10/13, x2
- Icones : marqueur rouge en Y x1 (bas droite)
- Texte :
  > <b>When Revealed (Alter-Ego)</b>: You may place 2 corruption counters on your Creeping Corruption. If you do not, the villain schemes with +2 SCH.
  > <b>When Revealed (Hero)</b>: If your Creeping Corruption has the <b><i>OVERPOWERING</i></b> trait, the villain schemes with +1 SCH; otherwise, the villain attacks you.
- Pied : Andrea Di Vito & Laura Villari © MARVEL © 2026 FFG 77

#### sl078 (65078) : Invasive Thoughts — TREACHERY, 12/13, x2
- Icones : boost: 1 étoile rouge [star] (bas droite)
- Texte :
  > <b>When Revealed</b>: Place 1 corruption counter on your Creeping Corruption. If it has the <b><i>OVERPOWERING</i></b> trait, place 1 threat on the main scheme; otherwise, take 1 damage.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or take 4 indirect damage.
- Pied : Facundo Moyano © MARVEL © 2026 FFG 78
