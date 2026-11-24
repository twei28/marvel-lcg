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
- Etape 8 bis (plateau) : `ui-app/src/board/tmnt-raphael-plateau.test.ts`, 20 cas verts (`cd ui-app && npx vitest run src/board/tmnt-raphael-plateau.test.ts`).
  Rage dessinee sur l'identite en forme heros ET en alter-ego (jusqu'a 4, rien a 0), timer de tr014, Sai de tr001b couchees sur l'identite,
  statut Stunned/Confused sur l'ennemi (tr004), attachement de rencontre qui quitte l'ennemi (tr003), obligation tr013, et la rage depensee
  comme ressource : l'identite devient une source de paiement cliquable (`useInteraction`). Sensibilite prouvee en CASSANT temporairement
  puis restaurant : (E) `counters` de `card-model.ts` -> 8 cas rouges ; (F) `peutPayer` de `interaction.ts` -> 2 rouges ; (G) `attachees` de
  `zones.ts` -> 4 rouges. Aucun vrai trou d'affichage : l'UI etait deja correcte. Pas de panorama des paires jumelles 14/15.
  Sans cas plateau (chiffrent seulement) : tr005, tr006, tr008 (soutien incline, couvert par tr009), tr015, tr016, tr017.

## Cartes terminees : OUI

tr001b (2 Sai couchees : cas plateau), tr003 et tr004 (attachement / statut : cas plateau), tr005, tr006, tr008, tr012, tr015 (natif : Toughness/Quickstrike/Nemesis, pas de module, donc pas de substitution),
tr016, tr017. Chacune : cas sujet, substitution rouge, autoplay, aucun nouvel objet dessine (statuts, defausses, inclinaison, pioche standards).
Details notables : tr003 refus du « may » (`choisir_option Cancel`) ; tr006 temoin d'epuisement (2e exemplaire refuse, ATQ +2 et non +4)
et fin de round (ATQ retombe) ; tr012 une/deux Sai, ennemi vaincu par attaque, evenement, Sai, allie (pas de pioche), Sai inclinee (pas de pioche).

## Cartes terminees : OUI aussi, apres etape 8 bis (cas plateau du 16/10/2026)

- tr001a, tr002, tr007, tr009, tr010, tr011, tr013, tr014 : etape 8 bis prouvee par `tmnt-raphael-plateau.test.ts` (voir ci-dessus), tout le reste deja prouve : OUI. Detail d'origine : tr001a (rage depensable, Yaban Hito plafonnee a 3 : cas verts, rouge sans module 4/7), tr002 (rage sans plafond, identite en civil), tr007, tr009,
  tr010, tr011, tr013, tr014 (compteur timer, Amplify prouve par +1 degat de boost : 5 contre 4).
- tr013 : « vous » = identite seulement prouve (l'identite ne contre ni ne defend, un allie oui, temoin sans obligation) ; manque seulement l'etape 8 bis.

## Decisions du 15/10/2026 appliquees et prouvees

- « Raphael » en civil = l'identite : tr002 (degat + rage sur Raph), tr007 (soin + rage), cas dans les deux formes.
- Rage : plafond 3 PARTOUT (decision du 16/10/2026, remplace celle du 15/10) : Yaban Hito, Seething Rage, Sai (4 attaques : 3), Casey 3 -> reste 3, Gekido 3 -> reste 3.
- Sai : 1 degat a l'identite, 1 a l'ennemi, +1 rage (plafond 3), action d'attaque (heros etourdi la consomme).
- tr003 : attachement de rencontre seulement (Gekido pose sur Rhino reste, Armored Rhino Suit reste).
- tr014 : Amplify 1 effectif.

## Non prouve / limites

- Aucune partie jouee par un humain dans le navigateur ; textes FR non deployes.

**Biographie verifiee le 21/10/2026** (serveur local, recherche Fan-made > Raphael (Inkwire) > Biographie) :
texte, identite civile (« Raph »), base, equipes, ennemis s'affichent tous correctement. Item 13 du backlog
desormais entierement clos (voir `docs/rapports/etat-du-backlog-2026-10-21.md`).
- `verifier_tous_les_decks.py` (toutes les decks, tres long) et `verifier_appels_modules.py` non relances.
- tr014 : le 2e passage par deux `RunVillainPhase` successifs ne rejoue pas la reponse ; la regle est prouvee par les messages d'etape 1 envoyes
  directement (cles `etape1_vilain`), pas par une phase du vilain complete.
- « Raphael » en civil pour tr010 : Gekido est une Hero Action, donc jamais utilisable en civil (cible identite par construction, non mesurable).
- Texte imprime de tr008 « payed » (faute du scan) non reproduit.
