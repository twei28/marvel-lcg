# Verdicts Ch'od (docs/packs/chod/GABARITS.md, « Questions en attente »)

Sources : RR v1.8 (scratchpad/rr_v18.txt). Scans : Fusion/marvel-lcg-src/assets/pics/<code>.jpg. Aucune notice d'auteur pour ce pack.

## Q1 co001a — A confirmé
Texte : « Interrupt: When you play a card with the requirement keyword, Ch'od gets +1 hand size until the end of the player phase (limit once per phase). » « a card » = tout type de carte jouée (événement ou amélioration). Requirement est imprimé sur co003/co004 (événements) et co006/co007 (améliorations).

## Q2 co001b — A confirmé
Texte : « Action: Discard a card from your hand → search your deck and discard pile for Cr'reee and add it to your hand (limit once per phase). » Deck ET défausse sont imprimés. RR Cost : la seule interdiction de payer concerne un effet qui exige une CIBLE sans cible valide ; une recherche n'est pas une cible → la défausse se paie même si Cr'reee est introuvable.

## Q3 co002 Cr'reee — A confirmé
Scan : THW 1, ATK 1, chacun avec une icône de dégâts consécutifs ; « While Cr'reee is exhausted, Ch'od gets +1 hand size. »

## Q4 co003 / co004 — A confirmé
Texte : « Hero Action: Deal damage to an enemy equal to your hand size. » (sans « (attack) »). RR Attack : « If a triggered ability is labeled as an attack—such as "Hero Action (attack)"—resolving that ability is considered to attack ». Le trait ATTACK seul n'en fait pas une attaque (les traits n'ont pas d'effet propre). « hand size » = la valeur de taille de main (stat), pas le nombre de cartes tenues.

## Q5 co005 Polymath — B (corrigé) : le code doit changer
Texte : « If you paid for this card with a: [physical] - … [energy] - … [mental] - … ». RR Wild Resource : « When a player generates a wild resource, they may specify which resource type (energy, mental, physical, or wild) it is being used as. » Un wild compte pour UN type, choisi par le joueur au paiement : ni les trois lignes (A codé), ni un type imposé par le moteur (B tel qu'écrit).

## Q6 co006 Saurian Physique — A confirmé
Texte : « Ch'od's attacks gain overkill. Hero Response: After you defeat a minion, exhaust Saurian Physique → … » RR You, Your : « if it triggers "after you attack and defeat a minion," it triggers after the controlling player's identity attacks and defeats a minion but not when an ally under that player's control » ; événements, ressources et améliorations du joueur comptent comme son identité ; alliés et soutiens non.

## Q8 co008-co010 — B : le code doit changer
Texte (Engineer) : « While you have a card with a printed [energy] resource in your hand, Ch'od gets +1 hand size. » RR Wild Resource : « When resources are not being generated for a cost, a wild resource does not have any characteristic other than "wild resource." In such contexts, wild resources cannot be interpreted as any of the other resource types. » Un wild imprimé en main ne compte pour AUCUNE des trois.

## Q9 co011 Cr'reee Captured — A confirmé
RR Tuck : « Tucked cards are not in play … When a card leaves play, each card tucked under it is discarded. » Cr'reee va à la défausse de son propriétaire.

## Q10 co012 Mentor — 2 points
(a) « your deck » : DOUTE RÉEL (multijoueur seulement), voir plus bas.
(b) Wild : B : le code doit changer. Texte : « number of different printed resources discarded this way ». Hors paiement, un wild n'est QUE « wild » (RR Wild Resource, citation Q8) : il compte comme UN type différent de plus (le 4e), pas comme trois.

## Q11 co013 Duel of Wits — B partiel : le code doit changer pour le wild
Texte : « Threat cannot be removed from here by cards with a printed resource that matches the printed resource on the card tucked under here. When Revealed: Tuck a card from your hand under here. » « au moins une couleur commune » : correct. Wild : hors paiement, il ne correspond qu'à un autre wild (RR Wild Resource). « your hand » : le joueur qui révèle (RR You) : correct.

## Q12 co014 Plutonia — A confirmé
RR Star Icon : « In and of itself, the star icon has no effect; it is merely a reminder to check the card's text box ». L'aptitude est permanente.

## Q13 co015 Strike and Phase — A confirmé pour la carte sans ressource ; B pour le wild
Texte : « discard each card from your hand with a resource symbol that matches that card. » Carte du dessus sans icône : rien ne correspond (A). Wild hors paiement = « wild » seulement (RR Wild Resource) : un wild défaussé ne correspond qu'aux cartes de la main qui ont une icône wild, et inversement.

## Q14 co016 Utter Contempt — A confirmé
Texte : « Place threat … equal to the number of printed resources discarded this way. » Sans « different » (contrairement à Mentor) : on compte les icônes (YY = 2). « boost icons » : RR Boost Icon ; l'étoile n'en est pas une (RR Star Icon).

## Q15 co017-co019 — B : le code doit changer (règle de l'utilisateur du 17/10/2026)
Scans : Energy YY / Genius BB / Strength RR, « Max 1 per deck. », Basic = 01088 / 01089 / 01090. GUIDE-CREATION-CONTENU.md §12 bis : seule l'image change → art alternatif.

## Icônes de ressource (point « à vérifier » du gabarit) — conformes
scratchpad/icones_wt_co.jpg : co002 BY, co003 Y, co004 R, co005 B, co006 R, co007 B, co008 Y, co009 B, co010 R, co017 YY, co018 BB, co019 RR = cards.json.

## DOUTE RÉEL

### Mentor (co012), « When Defeated: Discard the top 2 cards of your deck » — image : Fusion/marvel-lcg-src/assets/pics/co012.jpg
Pourquoi c'est un doute : en multijoueur, « your » sur un « When Defeated » de carte rencontre n'est pas fixé par le RR. FFG a dû le préciser par errata sur Mystique's Manipulations (« When Defeated: The defeating player searches… », RR v1.8 errata : « Specified who should resolve the ability »). La phrase d'avant sur Mentor (« While Mentor is engaged with you ») vise le joueur engagé. Codé : le joueur engagé. Identique en solo.
Question : « Mentor, "Discard the top 2 cards of your deck" : en multijoueur, de quel deck s'agit-il ? »
- A (recommandé, déjà codé) : le deck du joueur engagé avec Mentor (même « you » que la phrase d'avant).
- B : le deck du joueur qui a vaincu Mentor (précédent de l'errata FFG sur Mystique's Manipulations).
- C : le premier joueur.
