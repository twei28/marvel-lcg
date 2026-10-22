# Shadowland (MC65) : inventaire des cartes

Transcription du 22/10/2026 depuis les 93 scans de play.marvelsimulator.com (`.planning/shadowland/scans-marvelsimulator/`), faite par lecture d'image : **aucun texte n'est encore valide contre le livret ni contre MarvelCDB**. Sources brutes : `.planning/shadowland/transcriptions/part1-5.json` (fusion : `toutes.json`).

Identifiants du jeu : `65NNN[A|B]` officiel -> `slNNN[a|b]` (prefixe `sl`, voir `PLAN.md`).

## Verifie

- **93 images, 78 numeros, 90 exemplaires** : la somme des totaux imprimes par set (13+16+9+11+11+17+13) fait 90, comme l'annonce du produit ; les « trous » dans la numerotation « n/m » d'un set sont les exemplaires multiples d'une meme carte (quantite = ecart avec le numero suivant). La quantite est donc DEDUITE, pas lue.
- L'icone rouge en forme de **Y** est l'icone **Boost** (compare a Sandman 01102 Boost 2, Breakin' & Takin' 01107 Boost 2 et Armored Guard 01120 Boost 1) ; l'icone « carte avec un +, noire » est **Hazard** (01107 : « Hazard Icon: Deal +1 encounter card »).

## Icones resolues par comparaison (22/10/2026)

Comparees au zoom a des cartes OFFICIELLES du depot (01107 Hazard, 01108 Crisis, 01109 Acceleration, 16054 et 16069 Amplify), jamais a vue :

| Icone | Cartes Shadowland |
|---|---|
| **Boost** (Y rouge, nombre = nombre de Y) | lues sur chaque carte ; icone verifiee sur 01102, 01107, 01120 |
| **Crisis** (« !! » dans un eclat) | sl007, sl009, sl025, sl042, sl048, sl075 |
| **Hazard** (carte inclinee avec « + ») | sl024, sl070 |
| **Acceleration** (maison/toit avec « + » et barre) | sl043, sl076 (x2) |
| **Amplify** (avion avec « + ») | aucune carte du pack |
| **Aucune icone imprimee** (le texte accorde l'icone selon la position du vilain) | sl008 Strategic Positioning |

Corrections par rapport aux lectures brutes plus bas : sl025 est **Crisis** (lu « hazard »), sl048 est **Crisis** (lu « crisis/acceleration »), sl070 est **Hazard** (lu « non identifie »), sl076 est **Acceleration x2** (lu « hazard ? »), sl024 est **Hazard** (lu « crisis ou amplify »).

L'etoile rouge isolee en bas (sl043, sl048, sl076...) est l'icone de Boost « ★ » : l'effet est ecrit dans le texte (« ★ Boost: ... »). A modeliser comme les autres cartes a Boost-etoile du jeu (regarder 01123 Sonic Boom) au moment de l'entree JSON.

## Correction : roles des nombres d'un complot principal (face B)

Les agents de transcription ont inverse les deux nombres. Sur la carte officielle **01097b The Break-In!** (`desc` : StartingThreat 0, TargetThreat 7*, EscalationThreat 1*), le **rond en haut a gauche** (7 par joueur) est le **TargetThreat** et le **nombre en bas a droite** (0) est le **StartingThreat**. Les valeurs de sl001b, sl002b, sl038b, sl039b, sl060b, sl061b sont recorrigees en consequence ci-dessous (la transcription brute `toutes.json` n'est pas modifiee). Consequence : sl038b a un **TargetThreat ∞** (la menace ne peut jamais completer l'etape) et part de 25 par joueur.

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

#### sl001b (65001B) : A Barricade of Blades — MAIN SCHEME 1B, 1/13, x1
- Valeurs (CORRIGE 22/10/2026, voir plus haut) : TargetThreat=7 par_joueur (rond en haut a gauche), StartingThreat=2 par_joueur (en bas a droite), EscalationThreat=+1 par_joueur
- Texte :
  > In expert mode, the villain gets +1 SCH and +3[per_hero] hit points.
  > <b>Forced Interrupt</b>: When the villain would be defeated on side A, instead flip it to side B, reset its hit points, and change the villain's position. Deal each player 1 facedown encounter card.
  > <b>If the villain is defeated on side B, the players win the game.</b>
- A verifier : Le texte 'In expert mode...' et le premier paragraphe ne sont pas en italique; 'If the villain is defeated on side B...' est en gras complet (pas un mot-clé) | 7 = menace de depart (grand chiffre en haut a gauche) par joueur; 2 par joueur = seuil en bas a droite

#### sl002a (65002A) : Fortress Lockdown — MAIN SCHEME 2A, 2/13, x1
- Texte :
  > <i>While the forces on the outside hold the heroes back, ninjas on the inside lock every door and window.</i>
  > In expert mode, the villain gets +3[per_hero] hit points.
  > <b>When Revealed</b>: Change the villain's position. Each player searches the encounter deck and discard pile for a minion and reveals it. <i>(Shuffle.)</i>

#### sl002b (65002B) : Fortress Lockdown — MAIN SCHEME 2B, 2/13, x1
- Valeurs (CORRIGE 22/10/2026, voir plus haut) : TargetThreat=8 par_joueur, StartingThreat=2 par_joueur, EscalationThreat=+1 par_joueur
- Texte :
  > In expert mode, the villain gets +1 SCH and +3[per_hero] hit points.
  > <b>Forced Interrupt</b>: When the villain would be defeated on side A, instead flip it to side B, reset its hit points, and change the villain's position. Deal each player 1 facedown encounter card.
  > <b>If the villain is defeated on side B, the players win the game.</b>
  > <b>If this stage is completed, the players lose the game.</b>

#### sl003a (65003A) : The Streets Below — ENVIRONMENT, 3/13, x1
- Texte :
  > <b><i>VILLAIN POSITION.</i></b>
  > If both positions are the same:
  > • Each character gets +1 ATK.
  > If the positions are different:
  > • Reduce the amount of damage each character takes from each attack by 1.
  > • Threat cannot be removed from the main scheme.
- A verifier : 'VILLAIN POSITION.' est en gras italique majuscules (style de trait), pas un mot-clé gras normal; balisage <b><i> a vérifier

#### sl003b (65003B) : Atop the Tenshu — ENVIRONMENT, 3/13, x1
- Texte :
  > <b><i>VILLAIN POSITION.</i></b>
  > If both positions are the same:
  > • Each character gets +1 ATK.
  > If the positions are different:
  > • Reduce the amount of damage each character takes from each attack by 1.
  > • Threat cannot be removed from the main scheme.
- A verifier : 'VILLAIN POSITION.' en gras italique majuscules (style de trait)

#### sl004a (65004A) : The Streets Below — ENVIRONMENT, 4/13, x1
- Texte :
  > <b><i>HERO POSITION.</i></b>
  > <b>First Player Action</b>: Resolve one of the effects below, then flip this card:
  > • Place 3 threat on the main scheme and stun your identity.
  > • Spend [physical] [physical] resources.
  > • Spend 1 resource of any type and exhaust an <b><i>AERIAL</i></b> character you control.
- A verifier : Icone de ressource = poing noir (identifie comme [physical]), deux fois | AERIAL en gras italique majuscules (trait)

#### sl004b (65004B) : Atop the Tenshu — ENVIRONMENT, 4/13, x1
- Texte :
  > <b><i>HERO POSITION.</i></b>
  > <b>First Player Action</b>: Resolve one of the effects below, then flip this card:
  > • Deal 3 damage to your identity.
  > • Spend [energy] [energy] resources.
  > • Discard an ally or upgrade you control.
- A verifier : Icone de ressource = éclair noir (identifie comme [energy]), deux fois

#### sl005 (65005) : Black Tarantula ★unique — MINION, 5/13, x1
- Traits : BRUTE, HAND
- Valeurs : SCH=2, ATK=2, HP=5
- Icones (lecture brute) : {"nom": "icones rouges en forme de Y en bas a droite", "nombre": 3}
- Texte :
  > Guard.
  > <b>When Revealed</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, Black Tarantula attacks you; otherwise, give the villain and Black Tarantula each a tough status card.
- A verifier : HP=5 lu dans le cercle orange (minion); 3 icones rouges en bas a droite (probablement marqueur d'ensemble/nombre d'exemplaires), nature non certaine

#### sl006 (65006) : Ghost Maker ★unique — MINION, 6/13, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=2, HP=4
- Icones (lecture brute) : {"nom": "boost star (étoile rouge en bas a droite)", "nombre": 1}
- Texte :
  > <b>When Defeated</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, discard 1 card you control; otherwise, take 2 indirect damage.
  > <b>[star] Boost</b>: If an ally is defending against this attack, reveal this minion.
- A verifier : Il y a une ligne de séparation horizontale avant la ligne Boost | Étoile du Boost: en texte, '★' noire devant 'Boost'; mis [star]

#### sl007 (65007) : Sealed Entrances — SIDE SCHEME, 7/13, x1
- Valeurs : StartingThreat=4
- Icones (lecture brute) : {"nom": "crisis", "nombre": 1} ; {"nom": "icones rouges en forme de Y en bas a gauche", "nombre": 2}
- Texte :
  > Assault. <i>(Basic thwarts against this scheme use ATK instead of THW.)</i>
  > <b>When Defeated</b>: Change the villain's position if it has not changed this phase.
- A verifier : 'Assault.' non en gras (mot-clé en texte normal sur le scan) | 4 = menace de depart sans icone joueur | 2 icones rouges en bas a gauche, nature non certaine

#### sl008 (65008) : Strategic Positioning — SIDE SCHEME, 8/13, x1
- Valeurs : StartingThreat=3 par_joueur
- Icones (lecture brute) : {"nom": "icones rouges en forme de Y en bas a gauche", "nombre": 2}
- Texte :
  > <i>Under Shadowland, the Hand rules the streets.</i>
  > While the villain's position is The Streets Below, this scheme gains 1 acceleration icon ([acceleration]).
  > While the villain's position is Atop the Tenshu, this scheme gains 1 hazard icon ([hazard]).
- A verifier : 2 icones rouges en bas a gauche, nature non certaine | Pas d'icone crisis visible

#### sl009 (65009) : Surround the Fortress — SIDE SCHEME, 9/13, x1
- Valeurs : StartingThreat=2 par_joueur
- Icones (lecture brute) : {"nom": "crisis", "nombre": 1} ; {"nom": "icone rouge en forme de Y en bas a gauche", "nombre": 1}
- Texte :
  > <b>When Revealed</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, place 1[per_hero] threat on the main scheme; otherwise, place 1[per_hero] threat here.
- A verifier : 1 icone rouge en bas a gauche, nature non certaine

#### sl010 (65010) : Chaos in Hell's Kitchen — TREACHERY, 10/13, x2
- Icones (lecture brute) : {"nom": "boost star (étoile rouge en bas a droite)", "nombre": 1}
- Texte :
  > <b>When Revealed</b>: Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, place 2 threat on the main scheme; otherwise, take 2 damage.
  > <b>[star] Boost</b>: Resolve this card's "<b>When Revealed</b>" ability.
- A verifier : Ligne de séparation horizontale avant Boost

#### sl011 (65011) : Moonlit Silhouette — TREACHERY, 12/13, x2
- Texte :
  > <b>When Revealed (Alter-Ego)</b>: Change the villain's position if it has not changed this phase. You are confused.
  > <b>When Revealed (Hero)</b>: If the villain's position is Atop the Tenshu, the villain schemes; otherwise, the villain attacks you.
- A verifier : Numero dans le set = 12/13 alors que le numero de collection au pied = 11

### DARK PROTÉGÉ

#### sl012a (65012A) : Archpriestess ★unique — VILLAIN A, 1/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=1★, HP=15 par_joueur
- Texte :
  > <b>[star] Forced Response</b>: After Archpriestess attacks you, give a minion a tough status card. If no tough status card was placed this way, discard the top 3 cards of the encounter deck, then deal 1 minion discarded this way to yourself as a facedown encounter card.
- A verifier : ATK '1' avec une petite étoile en exposant (valeur imprimée '1★') | Le set imprime 'DARK PROTÉGÉ (1/16) / HIT POINTS 15[per_hero]'

#### sl012b (65012B) : Archpriestess ★unique — VILLAIN B, 1/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Texte :
  > Steady. Toughness.
  > <b>[star] Forced Response</b>: After Archpriestess attacks you, give a minion a tough status card. If no tough status card was placed this way, discard the top 3 cards of the encounter deck, then deal 1 minion discarded this way to yourself as a facedown encounter card.
- A verifier : ATK '2' avec petite étoile en exposant | 'Steady.' et 'Toughness.' en texte normal non gras

#### sl013a (65013A) : Daredevil ★unique — VILLAIN A, 2/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=2, HP=15 par_joueur
- Texte :
  > <b>Forced Response</b>: After you or an ally you control attacks Daredevil, choose: Either discard 1 random card from your hand, or Daredevil attacks you. (Limit once per round per player.)
- Citation : "Hell's Kitchen is now under the protection of the Hand!"
- A verifier : '(Limit once per round per player.)' non italique sur le scan

#### sl013b (65013B) : Daredevil ★unique — VILLAIN B, 2/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=2, ATK=2, HP=18 par_joueur
- Texte :
  > Steady. Toughness.
  > <b>Forced Response</b>: After you or an ally you control attacks Daredevil, choose: Either discard 1 random card from your hand, or Daredevil attacks you. (Limit once per round per player.)
- A verifier : Mots-clés Steady. et Toughness. en texte normal (non gras) sur la carte, transcrits sans <b>

#### sl014a (65014A) : Elektra ★unique — VILLAIN A, 3/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=2★, HP=15 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 2
- Texte :
  > [star] <b>Forced Interrupt</b>: When Elektra attacks you, discard the top card of your deck. If that card's printed cost is an odd number, Elektra gets +1 ATK for this attack; otherwise, this attack gains overkill and piercing.
- Citation : "The Hand guides me, and death follows."

#### sl014b (65014B) : Elektra ★unique — VILLAIN B, 3/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 2
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Interrupt</b>: When Elektra attacks you, discard the top card of your deck. If that card's printed cost is an odd number, Elektra gets +1 ATK for this attack; otherwise, this attack gains overkill and piercing.

#### sl015a (65015A) : Gorgon ★unique — VILLAIN A, 4/16, x1
- Traits : HAND
- Valeurs : SCH=1, ATK=2★, HP=15 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 2
- Texte :
  > [star] <b>Forced Interrupt</b>: When Gorgon attacks you, choose:
  > • Spend a [physical] resource.
  > • Stun your identity.
  > • Take 2 indirect damage.
- Citation : "I've died and been born again. There is nothing I fear."
- A verifier : Icône de ressource dans 'Spend a ... resource' : poing noir, nommée [physical] à vue

#### sl015b (65015B) : Gorgon ★unique — VILLAIN B, 4/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 2
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Interrupt</b>: When Gorgon attacks you, choose:
  > • Spend a [physical] resource.
  > • Stun your identity.
  > • Take 2 indirect damage.
- A verifier : Icône de ressource : poing noir, nommée [physical] à vue

#### sl016a (65016A) : Lady Bullseye ★unique — VILLAIN A, 5/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=1★, HP=15 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 1
- Texte :
  > [star] <b>Forced Response</b>: After Lady Bullseye attacks you, if that attack was undefended, take 1 indirect damage; otherwise, place 1 threat on the main scheme.
- Citation : "I plan to take my time with you."

#### sl016b (65016B) : Lady Bullseye ★unique — VILLAIN B, 5/16, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2★, HP=18 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 2
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Response</b>: After Lady Bullseye attacks you, if that attack was undefended, take 1 indirect damage; otherwise, place 1 threat on the main scheme.

#### sl017a (65017A) : White Tiger ★unique — VILLAIN A, 6/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=0★, HP=15 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 0
- Texte :
  > [star] <b>Forced Response</b>: After White Tiger attacks you, she attacks you again with +1 ATK. (Limit once per round per player.)
- Citation : "Civilization will fall into chaos and darkness, and we who walk the left-hand path will kneel before the Beast!"

#### sl017b (65017B) : White Tiger ★unique — VILLAIN B, 6/16, x1
- Traits : HAND, POSSESSED
- Valeurs : SCH=1, ATK=1★, HP=18 par_joueur
- Icones (lecture brute) : étoile (★) à côté de l'ATK 1
- Texte :
  > Steady. Toughness.
  > [star] <b>Forced Response</b>: After White Tiger attacks you, she attacks you again. (Limit once per round per player.)
- A verifier : Pied de carte coupé en bas de l'image : illustrateurs et copyright partiellement lisibles, complétés par analogie avec 17A

#### sl018 (65018) : Art of the Kill — ATTACHMENT, 7/16, x1
- Icones (lecture brute) : icône d'ensemble de rencontre (Y rouge) en bas à droite
- Texte :
  > Linked (Elektra, Lady Bullseye, or White Tiger).
  > Attach to your identity.
  > <b>Forced Interrupt</b>: When an enemy attacks you, it gets +1 ATK for that attack. If that attack defeats a character, place 1 threat on the main scheme.
  > <b>Alter-Ego Action</b>: Spend [energy] [mental] [physical] resources → discard this card.
- A verifier : Titre imprimé verticalement à gauche ; carte portrait | Trois icônes de ressources dans l'action Alter-Ego : éclair, forme ressemblant à des figures/silhouette, poing ; nommées [energy] [mental] [physical] à vue, ordre éclair/mental/poing | Pas de ligne de traits (aucun trait imprimé)

#### sl019 (65019) : Krahllak's Blessing — ATTACHMENT, 8/16, x1
- Traits : CONDITION, SPELL
- Icones (lecture brute) : icône d'ensemble de rencontre (Y rouge) en bas à droite
- Texte :
  > Linked (Archpriestess, Daredevil, or Gorgon).
  > Attach to the villain.
  > <b>Forced Interrupt</b>: When attached villain would take any amount of damage from a character, reduce that amount by 3. Attached villain attacks that character. Discard this card.
- A verifier : Titre imprimé verticalement à gauche ; carte portrait

#### sl020 (65020) : Archpriestess ★unique — MINION, 9/16, x1
- Traits : HAND, MYSTIC
- Valeurs : SCH=2, ATK=1, Boost=5
- Icones (lecture brute) : boost 5 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Gorgon, Lady Bullseye, or White Tiger).
  > Villainous.
  > <b>When Revealed</b>: Each other minion engaged with you attacks you. If no attack was made this way, discard the top 3 cards of the encounter deck.
- A verifier : Mot-clé Villainous. en texte normal (non gras)

#### sl021 (65021) : Gorgon ★unique — MINION, 10/16, x1
- Traits : BRUTE, HAND
- Valeurs : SCH=0, ATK=1, Boost=5
- Icones (lecture brute) : boost 5 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Daredevil, Elektra, or Lady Bullseye).
  > Guard. Villainous.
  > <b>Forced Response</b>: After a character attacks and damages Gorgon, stun that character.

#### sl022 (65022) : Lady Bullseye ★unique — MINION, 11/16, x1
- Traits : HAND
- Valeurs : SCH=1, ATK=1★, Boost=5
- Icones (lecture brute) : boost 5 ; étoile (★) à côté de l'ATK 1 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Archpriestess, Gorgon, or White Tiger).
  > Villainous.
  > [star] <b>Forced Interrupt</b>: When Lady Bullseye attacks you, this attack gains ranged and she attacks the ally with the highest printed cost you control, if able.

#### sl023 (65023) : White Tiger ★unique — MINION, 12/16, x1
- Traits : HAND
- Valeurs : SCH=1, ATK=2, Boost=5
- Icones (lecture brute) : boost 5 ; 2 icônes d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Archpriestess, Daredevil, or Elektra).
  > Villainous.
  > <b>When Revealed</b>: Take 2 indirect damage.

#### sl024 (65024) : Rite of Offering — SIDE SCHEME, 13/16, x1
- Valeurs : StartingThreat=1
- Icones (lecture brute) : icône de carte avec signe plus (noire) en bas du texte, probablement crisis ou amplify, non sûre
- Texte :
  > Linked (Archpriestess, Elektra, or White Tiger).
  > <b>When Defeated</b>: The defeating player removes an ally they control from the game. If no ally was removed this way, that player takes 3 damage.
- A verifier : Icône noire (carte avec +) : type non identifié avec certitude | Menace de départ '1' en bas à gauche : pas d'icône par_joueur visible | Aucun trait imprimé

#### sl025 (65025) : Shadowy Plot — SIDE SCHEME, 14/16, x1
- Valeurs : StartingThreat=2
- Icones (lecture brute) : icône hazard (point d'exclamation dans un éclat)
- Texte :
  > Linked (Daredevil, Gorgon, or Lady Bullseye).
  > <b>When Defeated</b>: The defeating player looks at the top 3 cards of the encounter deck, reveals 1 of them, and discards the rest.
- A verifier : Icône à point d'exclamation nommée hazard à vue | Menace de départ '2' : pas d'icône par_joueur visible | Aucun trait imprimé

#### sl026 (65026) : Darkness Within — TREACHERY, 15/16, x1
- Icones (lecture brute) : boost : 1 étoile rouge (★) ; 1 icône d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Archpriestess, Gorgon, or Lady Bullseye).
  > <b>When Revealed</b>: Change to hero form. The villain attacks you.
  > ---
  > [star] <b>Boost</b>: If this activation is an attack, it gains overkill.
- A verifier : Séparateur horizontal entre texte principal et boost noté --- | Étoile rouge en bas à droite = icône boost (symbole étoile) probable

#### sl027 (65027) : Embraced by Darkness — TREACHERY, 16/16, x1
- Icones (lecture brute) : boost : 1 étoile rouge (★) ; 1 icône d'ensemble de rencontre (Y rouge)
- Texte :
  > Linked (Daredevil, Elektra, or White Tiger).
  > <b>When Revealed</b>: The villain schemes. If 2 or less threat was placed on the main scheme this way, discard the top 3 cards of the encounter deck.
  > ---
  > [star] <b>Boost</b>: If this activation is an attack, place 2 threat on the main scheme.
- A verifier : Séparateur horizontal noté --- | Étoile rouge en bas à droite = icône boost probable

### NINJA SWARM

#### sl028 (65028) : Black Mountain ★unique — MINION, 1/9, x1
- Traits : BRUTE, HAND, NINJA
- Valeurs : SCH=2, ATK=2, cout=5
- Icones (lecture brute) : étoile boost (bas droite)
- Texte :
  > Guard.
  > While Black Mountain is engaged with you, each other <b>NINJA</b> minion engaged with you cannot be attacked.
  > <b>★ Boost</b>: If an ally is defending against this attack, reveal this minion.
- A verifier : Pas de PV imprimes visibles | NINJA en gras italique dans le texte

#### sl029 (65029) : Kirigi ★unique — MINION, 2/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=2, cout=3
- Icones (lecture brute) : étoile boost (bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>).
  > <b>When Defeated</b>: The defeating player either spends 2 resources of any type or shuffles Kirigi into the encounter deck.
  > <b>★ Boost</b>: If an ally is defending against this attack, this card gains [boost][boost] and this attack gains overkill.
- A verifier : Les deux icones dans 'this card gains' : deux symboles rouges en Y (boost ?), nom a confirmer | Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact

#### sl030 (65030) : Bo Staff Ninja — MINION, 3/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1, cout=2
- Icones (lecture brute) : boost x2 (deux icones Y rouges bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>). Toughness.
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact

#### sl031 (65031) : Fukiya Ninja — MINION, 4/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1★, cout=2
- Icones (lecture brute) : boost x1 (icone Y rouge bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>).
  > ★ This minion's attacks gain ranged.
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact | ATK '1' suivi d'une petite etoile (superscript)

#### sl032 (65032) : Katana Ninja — MINION, 5/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1, cout=2
- Icones (lecture brute) : boost x1 (icone Y rouge bas droite)
- Texte :
  > Guard. Teamwork (<b>NINJA</b>).
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact | Pas d'illustrateur imprime

#### sl033 (65033) : Kusarigama Ninja — MINION, 6/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1, cout=2
- Icones (lecture brute) : boost x2 (deux icones Y rouges bas droite)
- Texte :
  > Patrol. Teamwork (<b>NINJA</b>).
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact | Pas d'illustrateur imprime

#### sl034 (65034) : Shuriken Ninja — MINION, 7/9, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=1★, cout=2
- Icones (lecture brute) : boost x1 (icone Y rouge bas droite)
- Texte :
  > Teamwork (<b>NINJA</b>).
  > ★ This minion's attacks gain piercing.
  > <b>When Defeated</b>: The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact | ATK '1' suivi d'une petite etoile | Pas d'illustrateur imprime

#### sl035 (65035) : Dancing Shadows — SIDE SCHEME, 8/9, x1
- Valeurs : StartingThreat=3
- Icones (lecture brute) : étoile boost (bas gauche)
- Texte :
  > Each <b>NINJA</b> minion gets +1 hit point.
  > Threat cannot be removed from this scheme while at least 1 <b>NINJA</b> minion is in play.
  > <b>★ Boost</b>: Reveal this card.
- A verifier : Le '3' du coin bas gauche : menace de depart ; sans icone par joueur visible | Pas d'illustrateur imprime

#### sl036 (65036) : Countless Numbers — TREACHERY, 9/9, x1
- Icones (lecture brute) : étoile boost + 1 icone Y rouge (bas droite)
- Texte :
  > Surge.
  > <b>When Revealed</b>: Shuffle each <b>NINJA</b> minion in the encounter discard pile into the encounter deck.
  > <b>★ Boost</b>: Resolve this card's "<b>When Revealed</b>" ability.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact | Surge imprime en texte simple (non gras)

### SHADOW LABYRINTH

#### sl037 (65037) : Shifting Corridors — VILLAIN A, 1/11, x1
- Traits : LOCATION
- Valeurs : SCH=0★, ATK=0★, HP=∞
- Texte :
  > Stalwart.
  > <b>★ Forced Interrupt</b>: When Shifting Corridors would activate against you, instead remove 1 passage counter from here and reveal the top card of the trap deck.
  > <b>If the last passage counter is removed from here, the players lose the game.</b>
- A verifier : SCH et ATK '0' avec petite etoile | 'HIT POINTS ∞' imprime dans le pied (pas de bloc PV) | Etoile devant Forced Interrupt (★)

#### sl038a (65038A) : Into the Labyrinth — MAIN SCHEME 1A, 2/11, x1
- Texte :
  > <b>Contents</b>: Shifting Corridors (A). Shadow Labyrinth, Dark Protégé, Deadly Contraptions, and Standard encounter sets. One modular encounter set <i>(Ninja Swarm)</i>.
  > <b>Setup</b>: Create the trap deck <i>(see rulebook, p. 12)</i>. Set the Dark Protégé encounter set aside. Choose 1 random villain from that set, then shuffle each card linked to that villain into the encounter deck <i>(keep the chosen villain set aside)</i>.

#### sl038b (65038B) : Into the Labyrinth — MAIN SCHEME 1B, 2/11, x1
- Valeurs (CORRIGE 22/10/2026, voir plus haut) : TargetThreat=∞, StartingThreat=25 par_joueur, EscalationThreat=+1 par_joueur, Stage=1
- Texte :
  > <b>When Revealed:</b> Place 10[per_hero] passage counters on Shifting Corridors (7[per_hero] instead in expert mode).
  > <b>Forced Interrupt</b>: When Shifting Corridors would take any amount of damage, remove that much threat from here instead.
  > <b>Forced Interrupt</b>: When the last threat is removed from this scheme, advance to stage 2A <i>(the players win by advancing)</i>.
- A verifier : Menace de depart : symbole infini ∞ (coin haut gauche) | Dernier forced interrupt : italique partiel seulement sur la parenthese

#### sl039a (65039A) : Chamber of Vile Secrets — MAIN SCHEME 2A, 3/11, x1
- Texte :
  > <b>When Revealed</b>: Do each of the following:
  > 1. Set Shifting Corridors aside.
  > 2. Find the chosen Dark Protégé villain. Discard each status card, token, and attached card from it.
  > 3. Reveal the chosen villain's side A (side B instead in expert mode).

#### sl039b (65039B) : Chamber of Vile Secrets — MAIN SCHEME 2B, 3/11, x1
- Valeurs (CORRIGE 22/10/2026, voir plus haut) : TargetThreat=9 par_joueur, StartingThreat=1 par_joueur, EscalationThreat=+1 par_joueur, Stage=2
- Texte :
  > <b>When Revealed</b>: In expert mode, the villain activates against each player.
  > <b>Forced Response</b>: After you or an ally you control thwarts this scheme, reveal the top card of the trap deck. (Limit once per round per player.)
  > <b>If this stage is completed, the players lose the game.</b>
- A verifier : Seuil '1 par joueur' sous le +1 ; verifier que c'est bien le seuil cible | Menace de depart 9 par joueur (coin haut gauche)

#### sl040 (65040) : Whisper in the Dark — ATTACHMENT, 4/11, x1
- Texte :
  > <i>TRAP!</i>
  > Treat attached villain as an <b>ELITE</b> minion with 6 printed hit points. It gains: "Guard. Villainous. <b>When Defeated</b>: Set this minion aside."
  > <b>When Revealed</b>: If Shifting Corridors is in play, put the set-aside chosen villain into play engaged with you, side A faceup, with this card attached; otherwise, set this card aside and the villain schemes.
- A verifier : Titre imprime verticalement sur le cote gauche | 'TRAP!' en italique gras en tete du texte (traite comme trait ? a confirmer) | Pas d'illustrateur imprime

#### sl041 (65041) : Lord Deathstrike ★unique — MINION, 5/11, x1
- Traits : HAND
- Valeurs : SCH=2, ATK=2, cout=5
- Icones (lecture brute) : étoile boost (bas droite)
- Texte :
  > Patrol.
  > <b>When Revealed</b>: If Shifting Corridors is in play, shuffle the top 2 cards of the encounter deck into the trap deck; otherwise, reveal the top card of the trap deck.
  > <b>★ Boost</b>: Put this minion into play engaged with you.
- A verifier : Pas d'illustrateur imprime

#### sl042 (65042) : Dead End — SIDE SCHEME, 6/11, x1
- Valeurs : StartingThreat=2 par_joueur
- Icones (lecture brute) : boost x3 (trois icones Y rouges, bord gauche) ; icone crisis (point d'exclamation dans un eclat)
- Texte :
  > Assault. <i>(Basic thwarts against this scheme use ATK instead of THW.)</i>
  > <b>When Revealed</b>: If Shifting Corridors is in play, remove 1 passage counter from it; otherwise, place 1[per_hero] threat here.
- A verifier : Les icones rouges en forme de Y/pointe sont interpretees comme icones de boost, non certain du nom exact | Icone '!' dans un eclat noir consideree comme crisis, non certain

#### sl043 (65043) : Hall of Hidden Doors — SIDE SCHEME, 7/11, x1
- Valeurs : StartingThreat=3
- Icones (lecture brute) : étoile boost (bas gauche) ; icone acceleration (croix sur forme de toit)
- Texte :
  > <b>When Defeated</b>: The defeating player removes 5 threat from the main scheme. They discard cards from the encounter deck until a minion or side scheme is discarded, then reveal it.
  > <b>★ Boost</b>: Place 3 threat on the main scheme.
- A verifier : Icone centrale (croix sur forme de toit) interpretee comme acceleration, non certain | Menace de depart 3 sans icone par joueur visible

#### sl044 (65044) : No Time to Think! — TREACHERY, 8/11, x2
- Icones (lecture brute) : etoile rouge (coin bas droit, icone d'ecran de menace / acceleration ?) ; boost x1 (chevron rouge en Y)
- Texte :
  > Peril. <i>(While you are resolving this card, other players cannot help you.)</i>
  > <b>When Revealed</b>: The villain activates against you.
  > ★ <b>Boost</b>: If this activation is an attack, this card gains [boost][boost] and this attack gains overkill.
- A verifier : Icone etoile rouge en bas a droite : nature (acceleration/crisis/autre) non certaine | Les deux icones dans le texte 'gains [boost][boost]' lues comme icone boost (chevron en Y), non certain | Etoile du Boost lue comme ★

#### sl045 (65045) : Sudden Shift — TREACHERY, 10/11, x2
- Icones (lecture brute) : etoile rouge (coin bas droit) ; boost x2 (chevrons rouges en Y)
- Texte :
  > <b>When Revealed</b>: Shuffle the trap discard pile and the top 3 cards of the encounter deck into the trap deck. Reveal the top card of the trap deck.
  > ★ <b>Boost</b>: Shuffle the trap discard pile and the top 2 cards of the encounter deck into the trap deck.
- A verifier : Icone etoile rouge : nature non certaine

### DEADLY CONTRAPTIONS

#### sl046 (65046) : Nervous Jitters — ATTACHMENT, 1/11, x1
- Traits : CONDITION
- Icones (lecture brute) : boost x1 (chevron rouge en Y)
- Texte :
  > <i>CONDITION.</i>
  > Attach to your identity.
  > <b>Forced Interrupt</b>: When you choose the "<i>Avoid</i>" effect or the "<i>Disarm</i>" effect on a <b>TRAP!</b> card, name an encounter card type, then discard the top card of the encounter deck. If the card discarded this way was not of the named type, take 4 indirect damage and discard this attachment.
- A verifier : Mise en forme de TRAP! (police speciale) rendue par <b>

#### sl047 (65047) : Iron Monk ★unique — MINION, 2/11, x1
- Traits : HAND, MYSTIC
- Valeurs : SCH=2, ATK=1, cout_ou_PV=4 (cercle orange-rouge en bas a droite de l'image, probablement PV)
- Icones (lecture brute) : boost x2 (chevrons rouges en Y)
- Texte :
  > Patrol. Toughness.
  > While Iron Monk is engaged with you, you cannot choose the "<i>Avoid</i>" effect on <b>TRAP!</b> cards.
- Citation : "Your only path is through me. Let us begin."
- A verifier : Le 4 dans le cercle : identifie comme PV (pas de mention par joueur visible)

#### sl048 (65048) : Hall of Punishment — SIDE SCHEME, 3/11, x1
- Valeurs : StartingThreat=2 par_joueur
- Icones (lecture brute) : icone crisis/acceleration (point d'exclamation dans un eclat noir, au centre) ; etoile rouge (coin bas gauche)
- Texte :
  > <b>Forced Interrupt</b>: When you choose the "<i>Trip</i>" effect on a <b>TRAP!</b> card, discard the top 3 cards of your deck.
  > ★ <b>Boost</b>: Place 1 threat on the main scheme for each character you control.
- A verifier : Icone '!' au centre : crisis presume, non certain | Icone etoile rouge bas gauche : nature non certaine

#### sl049 (65049) : Path of a Thousand Cuts — SIDE SCHEME, 4/11, x1
- Valeurs : StartingThreat=5
- Icones (lecture brute) : etoile rouge (coin bas gauche)
- Texte :
  > <i>Every step is a test of resilience.</i>
  > <b>Forced Interrupt</b>: When you choose the "<i>Avoid</i>" effect or the "<i>Trip</i>" effect on a <b>TRAP!</b> card, take 2 indirect damage.
  > ★ <b>Boost</b>: Deal 1 damage to each character you control.
- A verifier : Menace de depart 5 sans icone par joueur visible | Icone etoile rouge : nature non certaine | Ligne en italique d'ouverture traitee comme ambiance/reglement et laissee dans texte

#### sl050 (65050) : Blinding Powder — TREACHERY, 5/11, x1
- Traits : TRAP
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard a <b>THWART</b> event from your hand.
  > • <i>Disarm</i> — Discard 2 cards at random from your hand, then give a character you control a tough status card.
  > • <i>Trip</i> — Deal 2 damage to your identity and confuse it.
- A verifier : TRAP! en ligne centree gras italique, traite comme trait | Aucune icone boost visible

#### sl051 (65051) : Caltrops — TREACHERY, 6/11, x1
- Traits : TRAP
- Icones (lecture brute) : boost x1
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard a <b>DEFENSE</b> event from your hand.
  > • <i>Disarm</i> — Discard 1 identity-specific card from your hand, then deal 2 damage to an enemy.
  > • <i>Trip</i> — Deal 2 damage to your identity and stun it.
- A verifier : TRAP! en ligne centree traite comme trait

#### sl052 (65052) : Flame Spout — TREACHERY, 7/11, x1
- Traits : TRAP
- Icones (lecture brute) : boost x3
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard an ally from your hand.
  > • <i>Disarm</i> — Discard an ally you control, then draw 2 cards.
  > • <i>Trip</i> — Deal 3 damage to your identity. Discard the top 3 cards of your deck.
- A verifier : TRAP! en ligne centree traite comme trait

#### sl053 (65053) : Oil Slick — TREACHERY, 8/11, x1
- Traits : TRAP
- Icones (lecture brute) : boost x1
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard an upgrade from your hand.
  > • <i>Disarm</i> — Discard an upgrade you control, then remove 4 threat from the main scheme.
  > • <i>Trip</i> — Discard 1 card from your hand. Discard the top 8 cards of your deck.
- A verifier : TRAP! en ligne centree traite comme trait

#### sl054 (65054) : Poison Darts — TREACHERY, 9/11, x1
- Traits : TRAP
- Icones (lecture brute) : boost x2
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Spend [energy] [energy] resources.
  > • <i>Disarm</i> — Spend [mental] [mental] [physical] resources, then deal 3 damage to the villain.
  > • <i>Trip</i> — Deal 3 damage to your identity and exhaust it.
- A verifier : Icones de ressources dans le texte : eclair = energy, petite icone 'silhouette' = mental, poing = physical ; nommees a vue, non 100% certain | TRAP! centree traite comme trait

#### sl055 (65055) : Pressure Plate — TREACHERY, 10/11, x1
- Traits : TRAP
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Spend [mental] [mental] resources.
  > • <i>Disarm</i> — Spend [energy] [physical] [physical] resources, then search the top 4 cards of your deck for a card and add it to your hand. <i>(Shuffle.)</i>
  > • <i>Trip</i> — Discard cards from the top of the encounter deck until a minion is discarded, then reveal it.
- A verifier : Icones de ressources nommees a vue (silhouette=mental, eclair=energy, poing=physical), non 100% certain | Aucune icone boost visible | TRAP! centree traite comme trait

#### sl056 (65056) : Tripwire — TREACHERY, 11/11, x1
- Traits : TRAP
- Icones (lecture brute) : boost x2
- Texte :
  > <b>TRAP!</b>
  > <b>When Revealed</b>: Choose:
  > • <i>Avoid</i> — Discard an <b>ATTACK</b> event from your hand.
  > • <i>Disarm</i> — Discard a support you control, then remove 3 threat from a scheme.
  > • <i>Trip</i> — Discard cards from the top of the encounter deck until a side scheme is discarded, then reveal it.
- A verifier : TRAP! centree traite comme trait

### HEART OF SHADOW

#### sl057 (65057) : Krahllak ★unique — VILLAIN, 1/17, x1
- Traits : DEMON, HAND
- Valeurs : niveau_etape=I, SCH=2, ATK=3★ (etoile en exposant), HP=18 par_joueur
- Texte :
  > Steady.
  > ★ <b>Interrupt</b>: When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
- Citation : "There is only the Beast!"
- A verifier : Etoile en exposant a cote de ATK : indique ATK avec effet de carte (consideree) | Tiret de '–3 ATK' est un tiret en (–)

#### sl058 (65058) : Krahllak ★unique — VILLAIN, 2/17, x1
- Traits : DEMON, HAND
- Valeurs : niveau_etape=II, SCH=2, ATK=4★, HP=21 par_joueur
- Texte :
  > Steady. Toughness.
  > ★ Krahllak's attacks gain overkill.
  > ★ <b>Interrupt</b>: When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
- A verifier : Etoile en exposant sur ATK

#### sl059 (65059) : Krahllak ★unique — VILLAIN, 3/17, x1
- Traits : DEMON, HAND
- Valeurs : niveau_etape=III, SCH=3, ATK=4★, HP=25 par_joueur
- Texte :
  > Retaliate 1. Steady. Toughness.
  > ★ Krahllak's attacks gain overkill and piercing.
  > ★ <b>Interrupt</b>: When Krahllak attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Krahllak gets –3 ATK for this attack.
- A verifier : Etoile en exposant sur ATK

#### sl060a (65060A) : Dark Invitation — MAIN SCHEME 1A, 4/17, x1
- Valeurs : niveau_etape=1A
- Texte :
  > <b>Contents</b>: Krahllak (I) and Krahllak (II). <i>(Krahllak (II) and Krahllak (III) instead for expert mode.)</i> Heart of Shadow, Black Flower, and Standard encounter sets. One modular encounter set <i>(Ninja Swarm)</i>.
  > <b>Setup</b>: Each player puts a Creeping Corruption upgrade into play. Set the rest aside.

#### sl060b (65060B) : Dark Invitation — MAIN SCHEME 1B, 4/17, x1
- Valeurs (CORRIGE 22/10/2026, voir plus haut) : TargetThreat=6 par_joueur, StartingThreat=2 par_joueur, EscalationThreat=+1 par_joueur, Stage=1
- Texte :
  > <b>Forced Interrupt</b>: When this stage would be completed, instead remove all threat from here and each player chooses:
  > • Place 2 corruption counters on their Creeping Corruption.
  > • Take 3 damage and deal themself 1 facedown encounter card.
  > <b>Forced Response</b>: After Krahllak is defeated, advance this scheme to stage 2A.
- A verifier : Role exact des trois nombres (6 / +1 / 2 par joueur) : 6 = menace de depart (gros chiffre a gauche), +1 = escalade, 2 = seuil ; a confirmer sur le moteur | Le 2 par joueur en bas a droite pourrait etre un seuil de menace

#### sl061a (65061A) : Beast Be Praised — MAIN SCHEME 2A, 5/17, x1
- Valeurs : niveau_etape=2A
- Texte :
  > <i>An inferno erupts in the throne room, punishing those who have yet to succumb to Krahllak's dark will.</i>
  > <b>When Revealed</b>: Each player whose Creeping Corruption has the <b>OVERPOWERING</b> trait discards 1 random card from their hand. Each other player discards a card they control from play. In expert mode, deal each player 1 facedown encounter card.

#### sl061b (65061B) : Beast Be Praised — MAIN SCHEME 2B, 5/17, x1
- Valeurs (CORRIGE 22/10/2026, voir plus haut) : TargetThreat=9 par_joueur, StartingThreat=2 par_joueur, EscalationThreat=+1★ par_joueur (etoile a confirmer), Stage=2
- Icones (lecture brute) : acceleration/escalade: +1 par_joueur étoile (encart bas droite)
- Texte :
  > [star] <b>Forced Response</b>: After resolving step one of the villain phase, each player chooses:
  > • Place 1 corruption counter on their Creeping Corruption.
  > • Place 3 threat here.
  > <b>If this stage is completed, the players lose the game.</b>
- A verifier : Le gros 9 + icône joueur en haut à gauche et le 2 + icône joueur en bas à droite : rôle exact (menace de départ / seuil) non étiqueté sur la carte | Étoile à côté de +1 [per_hero] dans l'encart d'escalade : icône acceleration avec étoile ? | Le texte de règle 'If this stage is completed...' est en gras entier (pas d'italique)

#### sl062 (65062) : Dark Shroud — ATTACHMENT, 6/17, x1
- Traits : SPELL
- Valeurs : ATK=+1
- Icones (lecture brute) : marqueur de set rouge en Y x1 (bas droite)
- Texte :
  > Attach to Krahllak.
  > <b>Interrupt</b>: When you or an ally you control would deal 4 or more damage to Krahllak with an attack, instead prevent all of that damage, place 1 corruption counter on your Creeping Corruption, and discard this card.
- A verifier : Icône rouge en Y en bas à droite : nature (boost ?) non certaine

#### sl063 (65063) : Fear Projection — ATTACHMENT, 7/17, x1
- Traits : SPELL
- Icones (lecture brute) : aucune icône de boost visible ; marqueur rouge en Y x1 (bas droite)
- Texte :
  > Attach to Krahllak.
  > Krahllak gains retaliate 1.
  > <b>Hero Action</b>: Place 2 corruption counters on your Creeping Corruption → discard this card.
  > <b>Alter-Ego Action</b>: Spend [mental] [mental] [mental] resources → discard this card. Remove 1 corruption counter from your Creeping Corruption.
- A verifier : Les trois icônes de ressource dans 'Spend ... resources' : petites icônes noires en forme de 'nœud/molécule' ; je les ai notées [mental] sans certitude (pourraient être une autre ressource) | Icône rouge en Y en bas à droite : nature incertaine

#### sl064 (65064) : Mark of the Wicked — ATTACHMENT, 8/17, x1
- Traits : SPELL
- Valeurs : ATK=+2 avec étoile
- Icones (lecture brute) : ATK +2 [star] ; marqueur rouge en Y x3 (bas droite)
- Texte :
  > <b>When Revealed</b>: You may attach this card to your identity. If you do not, take 4 damage, stun your identity, remove 1 corruption counter from your Creeping Corruption, and discard this card.
  > [star] <b>Forced Response</b>: After attached hero makes a basic attack, place 1 corruption counter on your Creeping Corruption.
- A verifier : Icônes rouges en Y (x3) : nature (boost ?) non certaine

#### sl065 (65065) : Pull of Power — ATTACHMENT, 9/17, x1
- Traits : SPELL
- Valeurs : THW=+2 avec étoile
- Icones (lecture brute) : THW +2 [star] ; marqueur rouge en Y x2 (bas droite)
- Texte :
  > <b>When Revealed</b>: You may attach this card to your identity. If you do not, take 4 damage, confuse your identity, remove 1 corruption counter from your Creeping Corruption, and discard this card.
  > [star] <b>Forced Response</b>: After attached hero makes a basic thwart, place 1 corruption counter on your Creeping Corruption.
- A verifier : Icônes rouges en Y (x2) : nature (boost ?) non certaine

#### sl066 (65066) : Fist ★unique — MINION, 10/17, x1
- Traits : HAND, UNDEAD
- Valeurs : SCH=2, ATK=2, HP=6
- Icones (lecture brute) : marqueur rouge en Y x2 (bas droite)
- Texte :
  > Patrol. Retaliate 2.
  > <b>Hero Action</b>: Place 1 corruption counter on your Creeping Corruption → deal 4 damage to Fist.
- Citation : A half-dead monstrosity brought to life by the mystical arts of the Hand, Fist won't stop until its mission is complete.
- A verifier : Icônes rouges en Y (x2) : nature (boost ?) non certaine | Le 6 dans le cercle orange est supposé être les PV

#### sl067 (65067) : Hellbride ★unique — MINION, 11/17, x1
- Traits : DEMON, HAND
- Valeurs : SCH=1, ATK=3, HP=7
- Icones (lecture brute) : marqueur rouge en Y x3 (bas droite)
- Texte :
  > <b>When Defeated</b>: The defeating player places 2 corruption counters on their Creeping Corruption, then heals 6 damage from their identity.
  > <b>Hero Action</b>: If Hellbride has 2 or fewer remaining hit points, exhaust your hero → discard Hellbride. Remove 1 corruption counter from your Creeping Corruption.
- A verifier : Icônes rouges en Y (x3) : nature incertaine | 7 dans le cercle orange supposé PV

#### sl068 (65068) : Retainer ★unique — MINION, 12/17, x1
- Traits : BRUTE, DEMON, HAND
- Valeurs : SCH=1, ATK=4 avec étoile, HP=9
- Icones (lecture brute) : ATK 4 [star] ; marqueur rouge en Y x3 (bas droite)
- Texte :
  > [star] Retainer's attacks gain overkill.
  > [star] <b>Interrupt</b>: When Retainer attacks you, you may place 1 corruption counter on your Creeping Corruption. If you do, Retainer gets –3 ATK for this attack.
- Citation : Krahllak's avatar, summoned to exact vengeance.
- A verifier : Icônes rouges en Y (x3) : nature incertaine | Le signe devant '3' dans '–3 ATK' est un tiret en (–) tel que lu

#### sl069 (65069) : Snakeroot Elders ★unique — MINION, 13/17, x1
- Traits : HAND, MYSTIC, NINJA
- Valeurs : SCH=1, ATK=2, HP=8
- Icones (lecture brute) : marqueur rouge en Y x3 (bas droite)
- Texte :
  > While there is at least 1 corruption counter here, Snakeroot Elders gains guard and patrol.
  > <b>When Revealed</b>: You may place 1 corruption counter on your Creeping Corruption. If you do not, place 1 corruption counter here.
- A verifier : Icônes rouges en Y (x3) : nature incertaine

#### sl070 (65070) : Veil of Nightmares — SIDE SCHEME, 14/17, x2
- Valeurs : menace_de_depart=5 par_joueur
- Icones (lecture brute) : marqueur rouge en Y x2 (bas gauche) ; icône noire centrale (croix dans un pentagone/maison) : voir incertitudes
- Texte :
  > <i>Krahllak's dark magic can tap into a person's deepest fears.</i>
  > <b>Hero Action</b>: Place 1 corruption counter on your Creeping Corruption → remove 5 threat from this scheme.
- A verifier : Icône centrale (croix blanche dans un pentagone noir) : probablement hazard ou similaire, non nommée avec certitude | Le 5 + icône joueur : supposé menace de départ | La ligne d'ambiance en italique est le premier paragraphe, sans attribution

#### sl071 (65071) : Submit or Suffer — TREACHERY, 16/17, x2
- Icones (lecture brute) : boost: 1 étoile rouge [star] (bas droite)
- Texte :
  > <b>When Revealed</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or remove 1 corruption counter from your Creeping Corruption and Krahllak attacks you.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or stun your identity.
- A verifier : Une ligne de séparation horizontale sépare When Revealed et Boost

### BLACK FLOWER

#### sl072a (65072A) : Creeping Corruption — UPGRADE A, 1/13, x4
- Icones (lecture brute) : petit rectangle blanc en haut à gauche (emplacement/coût vide)
- Texte :
  > Permanent. Setup. Max 1 per player.
  > If there are at least 5 corruption counters here, remove each of them from here and flip this card.
  > <b>Action</b>: Exhaust Creeping Corruption and place 1 corruption counter here → draw 1 card.
- A verifier : Le rectangle blanc en haut à gauche : probablement pas de coût (vide), nature exacte non certaine

#### sl072b (65072B) : Creeping Corruption — UPGRADE B, 1/13, x4
- Traits : OVERPOWERING
- Icones (lecture brute) : petit rectangle blanc en haut à gauche
- Texte :
  > Permanent. Max 1 per player.
  > <b>If there are at least 5 corruption counters here, you are defeated.</b>
  > <b>Action</b>: Exhaust Creeping Corruption and place 1 corruption counter here → draw 2 cards, then discard 1 card from your hand.
- A verifier : La ligne 'If there are at least 5...' est en gras complet | OVERPOWERING apparaît en ligne de traits en italique gras, comme les autres traits

#### sl073 (65073) : Aka ★unique — MINION, 5/13, x1
- Traits : HAND, NINJA
- Valeurs : SCH=1, ATK=3 avec étoile, HP=6
- Icones (lecture brute) : ATK 3 [star] ; boost: 1 étoile rouge [star] + marqueur rouge en Y x1 (bas droite)
- Texte :
  > Quickstrike. Villainous.
  > [star] <b>Interrupt</b>: When Aka would attack you, you may place 1 corruption counter on your Creeping Corruption. If you do, cancel that attack.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or discard 1 random card from your hand.
- A verifier : Icône rouge en Y : nature incertaine | Ligne de séparation entre Interrupt et Boost

#### sl074 (65074) : Tongue of the Beast ★unique — MINION, 6/13, x1
- Traits : DEMON, HAND
- Valeurs : SCH=1, ATK=2, HP=1
- Icones (lecture brute) : boost: 1 étoile rouge [star] (bas droite)
- Texte :
  > <b>When Defeated</b>: The defeating player places 2 corruption counters on their Creeping Corruption.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or this card gains [boost][boost][boost].
- A verifier : Les trois icônes noires en Y dans 'this card gains' : je les ai notées [boost] mais c'est la même forme que les marqueurs rouges des autres cartes ; nature non certaine

#### sl075 (65075) : Binding Ritual — SIDE SCHEME, 7/13, x2
- Valeurs : menace_de_depart=1 par_joueur
- Icones (lecture brute) : marqueur rouge en Y x2 (bas gauche) ; icône centrale : point d'exclamation dans un éclat (crisis probable)
- Texte :
  > <i>"He whom we serve shall reign supreme!"</i>
  > <i>—Takashi</i>
  > <b>When Revealed</b>: Each player chooses:
  > • Place 1 corruption counter on their Creeping Corruption.
  > • Place 3 threat here.
- Citation : "He whom we serve shall reign supreme!" —Takashi
- A verifier : Icône '!' dans un éclat : probablement crisis, non certain | Le 1 + icône joueur supposé menace de départ

#### sl076 (65076) : Roots of a Black Flower — SIDE SCHEME, 9/13, x1
- Valeurs : menace_de_depart=1
- Icones (lecture brute) : boost: 1 étoile rouge [star] (bas gauche) ; deux icônes noires (croix dans pentagone avec barre dessous) au centre
- Texte :
  > <b>When Defeated</b>: The defeating player places 2 corruption counters on their Creeping Corruption.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or place 4 threat on the main scheme.
- A verifier : Deux icônes noires centrales (croix dans pentagone avec barre) : nom (hazard ?) non certain | Le 1 sans icône joueur : supposé menace de départ fixe

#### sl077 (65077) : Malediction — TREACHERY, 10/13, x2
- Icones (lecture brute) : marqueur rouge en Y x1 (bas droite)
- Texte :
  > <b>When Revealed (Alter-Ego)</b>: You may place 2 corruption counters on your Creeping Corruption. If you do not, the villain schemes with +2 SCH.
  > <b>When Revealed (Hero)</b>: If your Creeping Corruption has the <b><i>OVERPOWERING</i></b> trait, the villain schemes with +1 SCH; otherwise, the villain attacks you.
- A verifier : Icône rouge en Y : nature incertaine | OVERPOWERING en petites capitales italiques grasses

#### sl078 (65078) : Invasive Thoughts — TREACHERY, 12/13, x2
- Icones (lecture brute) : boost: 1 étoile rouge [star] (bas droite)
- Texte :
  > <b>When Revealed</b>: Place 1 corruption counter on your Creeping Corruption. If it has the <b><i>OVERPOWERING</i></b> trait, place 1 threat on the main scheme; otherwise, take 1 damage.
  > [star] <b>Boost</b>: Choose: Either place 1 corruption counter on your Creeping Corruption, or take 4 indirect damage.
- A verifier : OVERPOWERING en petites capitales italiques grasses
