# Galactic Storm, lot GS-8 (Supreme Intelligence, Starforce, Seeds of Corruption, Nega-Bomb) : questions (20/10/2026)

Une question par carte, recommandation en premier, ce que chaque option change EN JEU. Rien n'est tranché :
la lecture recommandée est codée en attendant la réponse (pour que le scénario soit jouable), et le code
indique où changer. Scans : `docs/packs/galactic-storm/sources/<zN>/...` (chemins dans
`.planning/galactic-storm/defs/copier_images_supreme_intelligence.py`).

## Décisions déjà prises, appliquées dans ce lot (questions du lot GS-0, réponses du 20/10/2026) — CLOSES

- GS-0 Q4 (coquilles) : « completes » (gs199b The Endless Mind 2B) traité comme « completed » : la défaite des
  joueurs à l'achèvement du stade 2B est active (cas `[gs8] gs199b`). « highes » (gs214 Ronan) : citation, sans effet.
- GS-0 Q5 (nom imprimé) : sans objet dans ce lot (aucun écart de nom de fichier).
- GS-0 Q6 (conventions) : « ★ » devant Forced Interrupt (gs198b) / Boost = renvoi au texte ; ★ accolée à un nombre
  (PV 3 de Supremor, ATK 1 d'Ultimus et Shatterax, objectif 6 de gs198b) = renvoi au texte, sans valeur ; pastille
  orange = points de vie ; Y rouge = icône de boost.
- GS-0 Q7 (livret 1.2 partout) : au scénario 5 en campagne, chaque bonne carte intruse donne un allié et les deux
  Green Interference sont toujours mélangées. Hors campagne (ce lot), le set Nega-Bomb est un modulaire comme un
  autre ; la menace « X par joueur, X = Time Pressure » de la Nega-Bomb et les alliés des cartes intruses relèvent du
  lot GS-9 (campagne), NON codés ici.
- GS-0 Q10 : rien d'inventé là où le livret est vide (FAQ du scénario 5 « Q. to be added... ») ; les doutes sont
  ci-dessous.

## Q1. gs198a Protectors of the Kree Empire (1A) : Supremor est-il mis de côté avec les sbires Starforce ?

Image : `z1/Scenario Packs/Supreme Intelligence.../Setup cards/04 protectors of the kree empire IA.png` et
`.../Encounter cards/14 Supremor.png`. « Set each STARFORCE minion aside and put 1 of them at random into play ».
Supremor (gs204, x2, set Supreme Intelligence) porte les traits ELITE. KREE. STARFORCE.
1. **(Recommandé, codé) À la lettre : oui, les deux Supremor sont mis de côté.** 10 sbires STARFORCE : 9 de côté
   après la mise en place ; 1B avance quand il en reste 5 ou moins, soit après la 4e complétion de 1B ; Summon
   Reinforcements fait manigancer le méchant tant qu'il en reste un. Supremor n'arrive en jeu que par 1B ou 2A.
2. Seulement les 8 sbires du set Starforce : Supremor reste dans le deck rencontre. 7 de côté après la mise en
   place, 2A atteint après la 2e complétion de 1B : partie plus courte, Supremor révélé normalement.
3. Autre (précisez).

## Q2. gs221 Whisper in the Mind : où « Find a copy of your obligation » cherche-t-il ?

Image : `z1/Modular Sets/Seeds of Corruption.../07 Whisper in the Mind.png`. Livret p.4 : « Find : search each area
where the card could be found (play area, set-aside area, player deck, discard pile, encounter deck, etc.) ». Le
★ Boost de la même carte rend au deck l'obligation de la pile de victoire ou retirée de la partie.
1. **(Recommandé, codé) Deck rencontre, défausse rencontre et zone mise de côté.** Une obligation en pile de victoire
   ou retirée de la partie n'est pas trouvée (c'est le Boost qui la rend) : la carte gagne Renfort.
2. Toutes les zones, pile de victoire et zone retirée comprises : l'obligation revient plus souvent, Renfort plus rare.
3. Autre (précisez).

## Q3. gs223 Green Interference : quels « all-purpose counters » ?

Image : `z2/Modular Sets/Nega Bomb.../03 Green Interference.png`. FAQ officielle (fiche
`mots-cles/all-purpose-counter.md`) : la carte qui porte le compteur en définit le type.
1. **(Recommandé, codé) Tout compteur nommé sur une carte en jeu, cartes joueur comprises** (pions « time » de la
   Nega-Bomb, « integrity » de Holding Tank, Utilisations des soutiens et améliorations des joueurs). Une carte qui
   porte deux sortes de compteurs en perd un de la première sorte (choix automatique). Les jetons de dégâts et de
   menace ne sont pas des compteurs.
2. Seulement les cartes de RENCONTRE : les Utilisations des joueurs sont épargnées.
3. Comme 1, mais le joueur choisit quelle sorte de compteur retirer sur une carte qui en porte deux.
4. Autre (précisez).

## Q4. gs200 Holding Tank : « Victory 0 » quand le dernier pion intégrité part ?

Image : `z1/Scenario Packs/Supreme Intelligence.../Setup cards/06 holding tank.png`. Le mot-clé Uses DÉFAUSSE la
carte au dernier pion ; le moteur défausse une carte « Victory 0 » au lieu de la placer en pile de victoire (piège
connu de `mots-cles/uses.md`, cinq cartes livrées dans le même cas).
1. **(Recommandé, codé) Laisser le moteur : défaussée.** Aucun effet en jeu aujourd'hui (Holding Tank n'est pas un
   sbire KREE et rien ne compte la pile de victoire hors sbires) ; à rouvrir si la campagne (GS-9) lit la pile.
2. Pile de victoire (correction moteur `has_uses.py`, `Victory 0` reconnu) : touche aussi 51031, 53029, 59004,
   br012, tg011 ; batterie complète à relancer.

## Q5. gs220 Mental Torture : une ressource JOKER défaussée compte-t-elle comme « a [mental] resource » ?

Image : `z2/Modular Sets/Seeds of Corruption.../04 Mental Torture.png`.
1. **(Recommandé, codé) Non : seule une icône [mental] IMPRIMÉE étourdit** (même lecture que Psychic Shackles
   « printed [mental] resource »).
2. Oui : une carte à icône joker défaussée étourdit aussi l'identité.

## Q6. gs218 Manipulated Memories : un événement à coût 0 doit-il payer une ressource [mental] ?

Image : `z2/Modular Sets/Seeds of Corruption.../01 Manipulated Memories.png`. « Each event card in your hand gains
requirement ([mental]) » ; la fiche `requirement.md` : la contrainte de couleur est INCLUSE dans le coût.
1. **(Recommandé, codé) Oui : un événement à 0 exige de dépenser 1 ressource [mental]** (sans quoi le Requirement
   n'aurait aucun effet sur lui). Un événement qui exige déjà une [mental] est inchangé ; un événement à 2 se paie
   « 2 dont au moins 1 [mental] ».
2. Non : un événement à 0 se joue librement.

## Q7. gs198b Protectors of the Kree Empire (1B) : l'icône de Crise empêche-t-elle « remove all threat from here instead » ?

Image : `z3/Scenario Packs/Supreme Intelligence.../Setup cards/04 protectors of the kree empire IB.png`.
1. **(Recommandé, codé) Non : c'est un effet de remplacement du scénario, la Crise ne bloque que les joueurs.** La
   menace part toujours, le complot n'est jamais achevé en 1B.
2. Oui : avec une Crise en jeu la menace reste et le complot est quand même « remplacé » (sbire en jeu) puis
   s'achèverait au prochain contrôle.

## Lectures sur scan, pas des questions (consignées pour mémoire)

- gs198b : objectif 6 et escalade +2 imprimés SANS silhouette « par joueur » (fixes, quel que soit le nombre de
  joueurs) ; gs199b : départ 1, escalade +1, objectif 11, les trois PAR JOUEUR (la transcription oubliait l'objectif).
- Icônes au centre de la boîte de texte : Acceleration (gs203, gs205, dessin de sk229), Hazard (gs207, dessin de
  sk234), Amplify (gs206). Icône de ressource des Seeds : mentale (comparée à sk003 Wiccan, RES=B).

## Réponses de l'utilisateur (20/10/2026)

Principe rappelé par l'utilisateur : toujours suivre à 100 % les règles du jeu, sauf si la carte ou la campagne dit le contraire. Aucun changement de code n'est nécessaire : toutes les lectures retenues étaient déjà codées.
- Q1 : les deux Supremor sont mis de côté avec les sbires STARFORCE (à la lettre).
- Q2 : « Find » fouille deck et défausse rencontre et zone mise de côté, pas la pile de victoire ni la zone retirée (conforme au Rules Reference 1.6 : « find » ne cherche pas dans la pile de victoire).
- Q3 : tout compteur nommé sur une carte en jeu, cartes joueur comprises ; choix automatique de la sorte.
- Q4 : Holding Tank est défaussée, pas mise en pile de victoire. Règle officielle : « When a card with the victory X keyword is defeated, place it in the victory display » (Hall of Heroes, liste des mots-clés). Un attachement ne peut pas être vaincu : Uses le défausse, il ne va donc pas en pile de victoire. Le moteur est conforme, `has_uses.py` reste intact. (À rouvrir seulement si une carte de campagne dit autre chose.)
- Q5 : seule une icône [mental] imprimée étourdit (un joker défaussé n'étourdit pas).
- Q6 : décidée par cohérence avec Entropy Ascendant (Quasar Q-GS2-3) : un événement à 0 exige 1 ressource [mental].
- Q7 : la Crise ne bloque pas le remplacement de 1B (la Crise n'empêche que le retrait de menace par contre ; 1B remplace l'achèvement).
