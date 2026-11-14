# Captive (trait CAPTIVE, scénario Black King de Hellfire Hunt)

**Texte imprimé / définition** (livret p. 10, « Captive Mutants ») : « The Hellfire Club has imprisoned several mutants, and it's your mission to liberate them. When you successfully rescue a CAPTIVE mutant, their player card is added to your hand ... If the CAPTIVE mutant ally is later discarded, it goes to your discard pile ». Victoire de campagne : « Shuffle each CAPTIVE and RECRUITED ally in each player's deck and discard pile into the Recruited Mutants deck. Record the name of each CAPTIVE ally ... as "Recruited" » : ces alliés « can be used for the rest of the campaign as have the RECRUITED trait ».

**Mécanisme moteur** : `CAPTIVE` est dans la liste blanche `CardFace.TRAITS`. Les 4 captifs (`hf208` Dust, `hf209` Mercury, `hf210` Surge, `hf211` Prodigy) sont des **alliés** : générés dans la zone mise de côté du scénario par le Setup de `hf204a` (`MiseEnPlaceDuScenario`), puis cachés sous `hf206` Captured by Hellfire! (`PlaceCardHere(face, False, effect)`, `GetPlacedCardArea()`).
- **Libération** : `hf206` « When Defeated » : `joueur.GainCard(carte_au_hasard, effect)` (main).
- **Trait RECRUITED** : `CaptifRecrute()` (`__init__.py`) = `ThisGainKeyword(note, trait="RECRUITED")`, vrai seulement si le carnet (`Recruited Allies`) note déjà la carte : pas dans le scénario où il est libéré.
- **Carnet** : `cards/pack/hellfire_hunt/campaign.py` : `CAPTIFS`, `_allies_recrutes` (un captif noté rejoint le deck Recruited Mutants), `Releve` (`_captif_libere` : un captif noté s'il n'est ni de côté ni caché sous la manigance).

**Carte exemple** : `hf208` Dust (son attaque touche aussi le vilain et chaque sbire engagé).

**Pièges connus** : « random » = `Rand.RandomChoice` (non déterministe en test : mesurer des COMPTES, pas l'identité) ; Xavier's Institute est en jeu dès le scénario 2 mais ne redirige que les alliés RECRUITED : un captif défaussé pendant sa propre libération va dans la défausse du joueur, comme le dit le livret.

**Variantes maison** : aucune.
