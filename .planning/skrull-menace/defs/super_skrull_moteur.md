# Super-Skrull / Kree-Skrull War — modifications du moteur PARTAGE

Une seule, additive (une ligne de donnees) :

| Fichier | Quoi | Pourquoi | Cas qui la prouve |
|---|---|---|---|
| `Fusion/marvel-lcg-src/src/game/operate/worlds.py` (`Worlds.ASIDE_DECK_NAME`) | ajout du nom `"SuperpowerDeck"` (avec un commentaire date) | Le moteur cree un `SetAsideDeck` par nom liste dans ce Literal (`world.py:131`). Le paquet SUPERPOWER du scenario en a besoin, comme `"PlanetDeck"` pour Skrull Empire et `"TrapDeck"` pour Hunting Season | `[super_skrull] sk120a Setup : paquet SUPERPOWER cree…` (sans la ligne : `KeyError`) |

Aucune autre modification de `src/game/**`, de `src/cards/pack/__init__.py` ni des enums de traits (les traits SUPERPOWER, KREE, MYSTIC, ROBOT,
GENIUS, ELITE, TITLE existaient deja). Fusion avec les autres agents : une ligne par agent dans le meme Literal, a concilier a la main au merge.

Ce qui N'A PAS demande de moteur (mesure) : `Permanent` + `Setup` (cles desc natives, precedent 60113a), l'icone de crise conditionnelle d'Earth
Involvement (`ThisGainKeyword(change_on_event=OnEvent.Threat("This"))`), le cout additionnel d'Invisibility (`WhenUnitWouldBeAttacked` +
`CostFunction`), la defausse du paquet (`Faces.BindDiscardPile`, comme les pieges de Kraven).

Limite constatee du harnais : `Puzzle.PutIntoPlay('sk123')` sur une carte DEJA dans le paquet SUPERPOWER ne declenche pas son `AttachToFaceWhenPutIntoPlay`
(la carte entre en jeu sans s'attacher) alors que `Reveal` (chemin reel : complots, Reponse obligatoire, Power Multiplying) fonctionne. Les cas utilisent donc
`Puzzle.Reveal`. Aucune capacite du scenario ne met un pouvoir en jeu autrement que par revelation.
