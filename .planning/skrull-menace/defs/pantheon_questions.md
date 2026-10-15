# Skrull Pantheon (sk170-183) et Dard'van Sect (sk184-188) — questions ouvertes pour l'utilisateur

Format : card_id, phrase imprimee, lectures possibles, lecture RETENUE (implementee), chemin de l'image.
Images : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/` + `<SP>` = `Scenario Packs/Skrull Pantheon (Skrull Menace Expansion Content)/`
(`Setup cards/`, `Encounter cards/`, `insert.png`) et `<DS>` = `Modular Sets/Dard_van Sect (Skrull Menace Expansion Content)/`.

## 1. sk186 Dard'van Sect — l'icone noire « boite avec un plus »
- Phrase : aucune ; une icone noire (carte penchee portant une croix evidee) est imprimee au milieu de la boite de texte
  (la carte est paysage : l'icone apparait tournee de 90 degres). La transcription disait « black box-with-plus symbol ».
- Lectures : (a) HAZARD ; (b) decor.
- RETENU : (a). Verifie par la methode du glyphe (`docs/reference/mots-cles/hazard.md`, 3e methode) : le glyphe `H` de
  `public/fonts/ChampionsIcons.ttf` rendu a cote du scan decoupe est identique (carte penchee, croix, RIEN dessous ; ni la pointe + barre
  d'Acceleration, ni l'avion d'Amplify). `desc.Hazard = "1"` : tant que la carte est en jeu, la phase du mechant distribue une carte
  rencontre de plus (cas `[pantheon] sk186 ...`, cle `icones`).
- Image : `<DS>/04 dard_van sect side scheme.png`. Si c'est du decor : supprimer la cle `Hazard` de sk186 dans `defs/pantheon_cards.py`.

## 2. sk170a/b, sk171a/b, sk172a/b — « Deal the players each ... card ... in player order »
- Phrase : « Deal the players each non-treachery card discarded this way as a facedown encounter card in player order. »
- Lectures : (a) les cartes sont donnees UNE A UNE aux joueurs, en commencant par le premier joueur, puis on recommence au premier quand tous
  ont recu une carte (3 cartes, 2 joueurs : J1, J2, J1) ; (b) CHAQUE joueur recoit chaque carte (impossible : une carte physique) ;
  (c) tout au premier joueur.
- RETENU : (a). Un seul joueur : tout pour lui. Les cartes sont distribuees face cachee, revelees a l'etape 4 avec les autres.
- Image : `<SP>/Setup cards/01 kly_bn I.png`, `01 sl_gur_t I.png` (et II, III).

## 3. Jetons de foi : conserves d'un stade du mechant au suivant
- Constat moteur : le stade suivant du mechant prend la place de la MEME carte (comme Paibok), donc les compteurs (foi) restent ; les
  degats sont remis a zero (nouveaux PV). Le « When Revealed » du nouveau stade ajoute 1 jeton : foi(N+1) = foi(N) + 1.
- Le livret ne dit rien des jetons de foi a la defaite d'un stade (il dit seulement qu'ils survivent au RETOURNEMENT). Lecture retenue : ils restent.
  Alternative : les remettre a 0 a chaque nouveau stade (« tout ce qui est associe au mechant part avec lui »).
- Image : `<SP>/insert.png` (p.14, « Alternation of Gods »).

## 4. sk173b — « Advance to stage 2B » (derniere menace retiree) contre « Advance to stage 2A » (When Completed)
- Lecture retenue : « 2B » = le complot saute la face A du stade 2 et arrive directement sur la face B : le « When Revealed » de 2A
  (rechercher Strengthen the Faith et y placer 2[per_hero] menaces supplementaires) N'EST PAS resolu ; seul le « When Revealed » de 2B
  (retourner le mechant) l'est. « 2A » = chemin ordinaire : face A (recherche) puis face B. C'est la lecture du livret : detruire le Pantheon
  rend la suite plus facile (pas de Strengthen the Faith gratuite).
- Alternative : 2A resolue aussi dans les deux cas. Cas : `[pantheon] sk173b Derniere menace retiree ...` (Strengthen reste dans le deck)
  et `sk173b When Completed ...` (Strengthen revelee, menace 4).
- Image : `<SP>/Setup cards/04 protect the pantheon 1B.png`.

## 5. sk175a/b Skrull Pantheon — Action de heros non offerte sans jeton de foi
- Phrase : « Spend 2 resources ... → remove 1 faith counter from the villain. »
- Lecture retenue : l'Action n'est offerte que s'il reste au moins 1 jeton de foi sur le mechant (le cout serait paye pour rien). Alternative :
  toujours offerte (cout payable meme sans effet).
- « 2 resources of the same type » (Stronghold) : deux ressources du meme type ; un joker compte comme n'importe quel type (regle du moteur,
  `Cost('2', same_type=True)`, modele `next_evol/40090`). Destroyed : « any type ».
- Image : `<SP>/Setup cards/06 skrull partheon.png`, `06 skrull partheon damaged.png`.
- Regle du livret « faith counters cannot be removed from the villain until the main scheme advances to the second stage » : tenue PAR
  CONSTRUCTION (le seul moyen de retirer un jeton est l'environnement, mis de cote pendant tout le stade 1). Aucun garde supplementaire.

## 6. sk185 Dard'van Priest — qui choisit, et que devient l'activation
- Phrase : « When Dard'van Priest would attack, instead choose a card in play with a "When Revealed" ability and resolve that ability. »
- Lectures : (a) l'attaque est REMPLACEE (ni degats, ni cartes de boost) par la resolution ; le joueur engage avec le Priest choisit ;
  (b) le Priest attaque quand meme apres.
- RETENU : (a). Le Priest peut se choisir lui-meme (son propre « When Revealed » le fait comploter) et choisir le mechant, le complot 2B,
  un sbire, etc. ; sans carte eligible, rien. ATQ ★ = `desc.ATK "0*"` (convention de sk099 / sk109).
- Image : `<DS>/03 dardvan priest.png`.

## 7. sk188 Sectarian Practices — qui choisit
- Phrase : « Choose a card in play with a "When Revealed" ability and resolve that ability. If you cannot, this card gains surge. »
- RETENU : le joueur a qui la carte est revelee ; « a card in play » : les cartes de la table portant une capacite WhenRevealed non
  traitee comme blanche (complots principaux, mechant, sbires, complots annexes, environnements, attachements). Aucune carte : Renfort.
- Image : `<DS>/06 sectarian practices.png`.

## 8. « treachery card » (Kly'bn / Sl'gur't)
- RETENU : type Traitrise OU trait TREACHERY (decision utilisateur du 15/10/2026 pour les evenements de Lyja, qui se melangent au deck rencontre).

## 9. Retournement du mechant pendant une activation (Nogor Boost, Prayer Boost, Strengthen the Faith Boost)
- Le livret : tout ce qui est associe au mechant est defausse sauf jetons de foi et degats. Pendant une activation, les AUTRES cartes de
  boost face cachee du mechant sont donc defaussees sans etre resolues ; la carte de boost en cours de resolution suit son chemin. Le
  retournement n'annule pas l'activation en cours (le mechant attaque / manigance avec la valeur de la carte au moment du coup).
- Image : `<SP>/insert.png`.

## 10. sk187 Collective Prayers — « the top card ... for each character in play »
- RETENU : N = nombre de personnages EN JEU au moment de la revelation (identites, allies, sbires, mechant). Les cartes defaussees sont
  revelees dans l'ordre de la defausse, seulement celles du set Dard'van Sect. Si le deck s'epuise, le moteur s'arrete (pas de remelange :
  `Worlds.DiscardEncounterCards`, comme sk106 / sk139).
