# `sp_dr` ne monte aucune partie : à traiter après Zeus

**Demande de l'utilisateur le 11/09/2026** : « après Zeus on va voir le
problème avec sp_dr ».

## Ce qu'on sait

- `tools/verifier_tous_les_decks.py` : `sp_dr` est le SEUL deck sur 132 qui
  échoue, au setup : `AssertionError: self=[(01,31002a) Peni Parker]`.
- Préexistant : même message consigné le 02/09/2026
  (`2026-09-02-portage-viv-vision.md`, « préexistant ») et le 05/09/2026
  (`2026-09-05-throg-gabarits-processus-carte.md`). Aucun rapport avec la
  cinquième couleur (11/09) : le message est identique avant et après.
- Le pack s'appelle `spdr` dans `src/cards/pack/`, le deck `sp_dr`.
- `31002a` est Peni Parker, l'alter ego de SP//dr, et l'assertion porte sur une
  liste d'UNE face : c'est un `assert` de construction (`factory.py` en pose,
  voir la gate finale de `PROCESSUS-HEROS.md`) ou un setup qui attend une
  autre face (SP//dr a une carte « SP//dr » de côté au montage).

## Par où commencer

1. `DECK_NOM=sp_dr $PY tools/verifier_tous_les_decks.py "$W/.game-src" 27000`
   avec la trace complète (`/tmp/deck_sp_dr.json` ne garde que le message).
2. Lire `src/cards/pack/spdr/spdr/31002a.py` et `31001a.py` : le setup de SP//dr
   met une carte de côté ; vérifier `BeginGameWithSetAside`.
3. Comparer avec un héros à setup similaire qui monte (Storm et son deck
   météo, `36001b`).
