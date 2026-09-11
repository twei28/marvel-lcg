# `sp_dr` ne monte aucune partie : CORRIGÉ le 11/09/2026

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


## ✅ Corrigé le 11/09/2026

**Ce n'était pas préexistant, c'était à moi.** La trace complète
(`/tmp/deck_sp_dr.log`) montre que le setup passe : c'est le **rendu du
premier ennemi** qui meurt. `Enemy.GetInfoDict` → `GetHoldingHeroPlayerNumber`
(ajouté par `6feb16d9`, Alligator Loki, le **01/09 à 23:47**, la veille du
premier constat) appelait `GetHeroFace()` sur l'identité de chaque joueur.
Peni Parker (`31002a`) n'a pas de face héros sur sa carte : l'armure SP//dr
Suit (`31001a`) est une carte à part. `GetHeroFace` pose un assert.

**Correctif** : `Identity.FindHeroFace()` (rend `None` au lieu de planter) et
`GetHoldingHeroPlayerNumber` passe par lui. Sans face héros, ce joueur ne
tient rien.

**Preuves** : cas « sp_dr : la partie monte et un sbire se rend » vu rouge
puis vert ; 13/13 cas Alligator Loki (le champ qui a introduit la régression
reste juste) ; gate de deck `sp_dr` OK (identité 31001a, main 4, deck 36).

**Leçon** : une identité n'a PAS forcément son héros au dos. Tout code qui se
demande « ce joueur a-t-il un héros qui... » doit passer par `FindHeroFace`.
