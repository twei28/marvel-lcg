# Raphael (tr) : gabarits PROCESSUS-CARTE, 16/10/2026

Preuves communes :
- Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_raphael.py`, **97 cas verts sur 97** (`test_capacites.py .game-src <port> rapport "[raphael]"`).
- Substitution (`substituer_pack.py .game-src 47000 tr0`) : **17/17 modules avec au moins un cas rouge** sans module. Les cas qui restent verts
  sont des contre-cas d'ABSENCE d'effet (autre forme, refus, temoin sans la carte), assumes.
- Autoplay : 16 parties raphael (rhino + klaw, equilibre + agressif), 0 incident, 0 traceback sur les 24 journaux
  (NameError/AttributeError/TypeError/KeyError/AssertionError). 0 % de victoire : `player_deck` est vide par regle (15 cartes seulement) ;
  temoin spider_man vs rhino, 8 parties : 0 % aussi.
- Textes, nombres et icones relus contre les 18 scans (`assets/pics/tr*.jpg`) : conformes. Icones de ressource par decoupe : poing = physique
  (`01003`), etoile = wild (`01043d`) ; tr002 = wild, toutes les autres cartes de deck = physique.
- Etape 8 bis (plateau) : AUCUN cas plateau ecrit. Les compteurs `rage`/`timer` passent par le rendu generique (`compteurs-fr.ts`).

## Cartes terminees : OUI

tr001b, tr003, tr004, tr005, tr006, tr008, tr012, tr015 (natif : Toughness/Quickstrike/Nemesis, pas de module, donc pas de substitution),
tr016, tr017. Chacune : cas sujet, substitution rouge, autoplay, aucun nouvel objet dessine (statuts, defausses, inclinaison, pioche standards).
Details notables : tr003 refus du « may » (`choisir_option Cancel`) ; tr006 temoin d'epuisement (2e exemplaire refuse, ATQ +2 et non +4)
et fin de round (ATQ retombe) ; tr012 une/deux Sai, ennemi vaincu par attaque, evenement, Sai, allie (pas de pioche), Sai inclinee (pas de pioche).

## Cartes terminees : NON (rage/timer : cas plateau absent, etape 8 bis non tenue)

- tr001a (rage depensable, Yaban Hito plafonnee a 3 : cas verts, rouge sans module 4/7), tr002 (rage sans plafond, identite en civil), tr007, tr009,
  tr010, tr011, tr013, tr014 (compteur timer, Amplify prouve par +1 degat de boost : 5 contre 4).
- tr013 : « vous » = identite seulement prouve (l'identite ne contre ni ne defend, un allie oui, temoin sans obligation) ; manque seulement l'etape 8 bis.

## Decisions du 15/10/2026 appliquees et prouvees

- « Raphael » en civil = l'identite : tr002 (degat + rage sur Raph), tr007 (soin + rage), cas dans les deux formes.
- Rage : plafond 3 seulement Yaban Hito / Seething Rage / Sai (4 attaques : 3) ; Casey 3 -> 4 et Gekido 3 -> 4 sans plafond.
- Sai : 1 degat a l'identite, 1 a l'ennemi, +1 rage (plafond 3), action d'attaque (heros etourdi la consomme).
- tr003 : attachement de rencontre seulement (Gekido pose sur Rhino reste, Armored Rhino Suit reste).
- tr014 : Amplify 1 effectif.

## Non prouve / limites

- Aucune partie jouee par un humain dans le navigateur ; biographie `heros-info.js` non verifiee au survol ; textes FR non deployes.
- `verifier_tous_les_decks.py` (toutes les decks, tres long) et `verifier_appels_modules.py` non relances.
- tr014 : le 2e passage par deux `RunVillainPhase` successifs ne rejoue pas la reponse ; la regle est prouvee par les messages d'etape 1 envoyes
  directement (cles `etape1_vilain`), pas par une phase du vilain complete.
- « Raphael » en civil pour tr010 : Gekido est une Hero Action, donc jamais utilisable en civil (cible identite par construction, non mesurable).
- Texte imprime de tr008 « payed » (faute du scan) non reproduit.
