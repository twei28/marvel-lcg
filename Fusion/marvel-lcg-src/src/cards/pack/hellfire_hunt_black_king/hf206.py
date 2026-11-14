from . import *

# Captured by Hellfire! (side scheme 5, Permanent, Victory 1). « When Revealed : Place 1[per player] random set-aside CAPTIVE allies facedown
# beneath this scheme. When Defeated : The player who defeated this scheme takes a random card from beneath here, and add it to their hand. After
# that, if there still has card under this scheme, place 5 threat here. Otherwise, advance to main scheme 2A and add this card to the victory
# display. »
# Cartes de reference : sk265 / sk267 (cartes glissees sous une carte : `PlaceCardHere(face, False, effect)`, `GetPlacedCardArea()`), 60113a
# (side scheme PERMANENT : le moteur envoie « When Defeated » sans la defausser : `EncounterSideScheme.OnBeDefeated`), 04141 (`WhenSchemeBeDefeated`,
# `message.defeating_player`), `Faces.AddToVictoryDisplay`.
# ⚠ Mots-pieges : « beneath » = face cachee SOUS la carte ; « random » = `Rand.RandomChoice` (deterministe en test) ; « the player who DEFEATED »
# (pas le premier joueur) ; « After that, if there STILL has card » : on relit la pile APRES la prise ; la carte est Permanent : elle ne quitte le
# jeu que par l'effet « add this card to the victory display » (meme set « Black King » : has_permanent.py l'autorise).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        candidats = list(Worlds.GetSetAsideAreaCards(effect, CardFinder(trait=CAPTIF, card_type=Ally)))
        for _ in range(Worlds.GetPlayerNum(effect)):
            if not candidats:
                break
            face = Rand.RandomChoice(candidats, effect)
            candidats.remove(face)
            this.PlaceCardHere(face, False, effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.defeating_player or Worlds.GetCurrentPlayer(effect)
        dessous = list(this.GetPlacedCardArea().Get(True))
        if dessous:
            libere = Rand.RandomChoice(dessous, effect)
            joueur.GainCard(libere, effect)
        if this.GetPlacedCardArea().Get(True):
            this.PlaceThreatOnSchemes([this], 5, effect)
        else:
            principal = Worlds.FindMainScheme(effect)
            if principal is not None:
                principal.CastTo(MainScheme).Advance("2A", effect)
            Faces.AddToVictoryDisplay([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
