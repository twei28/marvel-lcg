# Shadowland (MC65) : etat au 23/10/2026

**Les 93 faces (sl001-sl078) et les 3 scenarios sont codes** sur la branche `shadowland` (fusionnee dans la branche principale le 23/10 ; non poussee, non deployee) : Shadows in the Night, Shadow Labyrinth, Heart of Shadow, chacun en standard et expert, avec Ninja Swarm en modulaire recommande (`modular_sets`). Entree `209. Shadowland` dans `data/sets_info.json`.

## Preuves
- 431 cas `[sl]`, `[sla]`, `[slb]`, `[slc]`, `[sld]` verts (`tools/cas/shadowland*.py`), chaque carte avec au moins un cas qui passe au rouge quand on vide son module.
- `tools/test_cards.py` : 7269 ok / 0 erreur. `verifier_prefixes.py` OK.
- Autoplay (Spider-Man, 3 profils, normal + expert, 4 parties par combinaison, 72 parties) : 0 traceback, 0 blocage, 0 victoire (le pilote ne gagne pas avec le deck de depart, meme contre Rhino) ; la victoire face B est couverte par les cas.
- Cartes verifiees une a une sur les scans par chaque agent ; corrections de `cards.json` listees dans les DECISIONS.

## Decisions (aucun livret officiel en ligne : regle muette = Rules Reference habituelle)
Une par lot : `DECISIONS-a.md` (Dark Protege), `DECISIONS-b.md` (Shadow Labyrinth, paquet de pieges deduit des cartes puisque le livret p.12 manque), `DECISIONS-c.md` (Heart of Shadow), `DECISIONS-d.md` (Ninja Swarm, Black Flower). A confirmer par le livret quand il sera disponible : la mecanique du paquet piege (b), les quantites par carte de sl075/sl077/sl078 (d).

## Mini-campagne (23/10/2026, livret FR)
Codee : voir `CAMPAGNE.md` (`campaign.py`, `data/campagnes/shadowland.json`, 62 cas `[slcamp]`, 496 cas `[sl*]` verts). Deck Piege conforme au livret (`DECISIONS-b.md` §8).

## Pas fait
- Aucune partie jouee par un humain dans le navigateur ; pas de cas plateau (ui-app) pour les compteurs `corruption` / `passage` et le paquet piege.
- Defaut moteur connu non corrige : la recherche dans un paquet ne trouve pas la carte quand elle est la derniere (`Deck.DiscardUntil`), rare (sl043, sl055, sl056).
- Le pilote d'autoplay ne prend jamais l'Action « HERO POSITION » (sl004) : elle se re-propose a l'infini, defaite au round 1 ; ses 6 branches sont couvertes par les cas `[sl]`.
- Fusion avec la branche principale : FAITE le 23/10/2026 (`gs7-earth-under-siege`). Conflits resolus a la main dans `data/sets_info.json` (entree 209) et `data/cards.json` (bloc `shadowland`), sommes de controle recalculees. Apres fusion : `test_cards` 7290 ok / 0 erreur, `verifier_prefixes` OK, 431/431 cas `[sl*]`, et pas de regression sur `[el_aspect]` 44, `[if_aspect]` 78, `[ville]` 15, `[big]` 55, `[gang]` 27.
