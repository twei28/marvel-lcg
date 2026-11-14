# Piste (LEAD)

**Texte imprimé / définition** : trait imprimé en italique *« Lead. »* sur 9 obligations (p077-p093, set « Leads —
The Big Apple », ID 6039-6047), une par lieu (même numéro entre parenthèses dans le titre que le lieu correspondant,
voir `lieu.md`), plus 3 de plus avec Uptown (p051-p055, U1-U3). Forme commune des 9 cartes :
- Une condition de position : « While in <lieu> » (la plupart) ou une condition sans position (p081 *A Walk in the
  Park*, p087 *Kings of Yancy Street* teste « when you attack the villain »).
- Un déclencheur qui pose un ou plusieurs compteurs NOMMÉS sur la piste elle-même (bouncer, culture, curse, rent…),
  ou empile des cartes dessus (tuck, p085 *Midtown Memories*), ou accumule des dégâts (p087).
- Une clause finale commune aux 9 cartes : « Then, if there are **N** or more <compteurs/cartes/dégâts> here, add
  this card to the victory display, reveal the top LEAD card, and draw 1 card. » (N varie : 3, 3, —, 4, 3, 8, 3…,
  à vérifier carte par carte au portage).
- p001 *Gang War (1B)*, manigance principale : « After a LEAD card is added to the victory display, if there are
  2👤 LEAD cards there, advance to stage 2A (the players win by advancing). »

**Mécanisme moteur** : **à créer**, aucun équivalent exact. Éléments disponibles dans le dépôt :
- Un deck annexe par joueur existe déjà pour un autre pack : `player.additional_deck` / `additional_discard_pile`
  (`src/game/player/player.py:97-99`, modèle Iron Patriot `ip`, deck secondaire de sbires REGISTERED) — mais c'est
  un deck PAR JOUEUR, alors que le deck LEADS de 9 cartes est **commun à toute la table** (une pioche partagée, une
  carte revient dessus à chaque fois qu'une piste part en victoire). `Worlds.AsideDeck` (si confirmé dans le code)
  est la piste la plus proche pour un deck de côté commun.
- La pile de victoire et « tant que X est dans la pile de victoire » : `RECETTES-MOTEUR.md` §3bis (déjà fait,
  réutilisable tel quel pour « add this card to the victory display »).
- Les compteurs nommés arbitraires (bouncer, culture, curse, rent, etc.) suivent la règle déjà fichée dans
  `all-purpose-counter.md` : le TYPE du compteur est celui de la carte qui le porte, aucun ajout d'enum nécessaire
  pour un nom de compteur inédit tant qu'il reste sur SA carte.
- Dépend de `lieu.md` (position du joueur) pour lire « while in <lieu> ».

**Carte exemple** : aucune carte portée à ce jour (lot PU-6 du cadrage, après PU-5 qui pose `lieu.md`/`territoire.md`).

**Pièges connus** :
- Révéler « la piste du dessus du deck LEADS » (p077 etc.) : une seule piste est révélée par joueur à la mise en
  place (p001, Setup), puis une nouvelle piste est révélée à chaque fois qu'une piste part en victoire — il faut
  donc distinguer « ma piste active » (par joueur, modifiable) du deck LEADS commun (par table).
- La condition de position se lit au moment du déclencheur (ex. « after a minion or ally you control is defeated,
  **while in Hell's Kitchen** »), pas en continu : un joueur qui quitte le lieu après coup ne perd pas les
  compteurs déjà posés.
- Mode campagne (combat 2, p003) : « record the location where the final LEAD card was added to the victory
  display » — le CARNET DE CAMPAGNE doit mémoriser un numéro de lieu (1 à 9), lu par le tableau de p265
  (`docs/packs/mcdc-2026-punisher/cartes.md`, ligne ~1077) pour choisir la manigance principale du combat 2.
- Ne pas confondre avec le mot « lead » générique de l'anglais MC (« the lead player ») : ici c'est un TYPE de carte
  (Obligation, trait Lead), toujours en MAJUSCULES dans le texte des cartes qui le citent (« reveal the top LEAD
  card »).

**Variantes maison** : aucune à ce jour ; brique neuve du lot Punisher MC×DC 2026 (cadrage §1.2, mécanique M3).
