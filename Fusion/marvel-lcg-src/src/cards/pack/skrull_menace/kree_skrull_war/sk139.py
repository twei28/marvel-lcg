from . import *

# Imperial Kree Army — TRAITRISE (Kree-Skrull War). ★ + 1 icone Y.
# When Revealed: Discard the top card of the encounter deck. Deal 1 damage to each
#   character you control for each boost icon discarded this way.
# ★ Boost: Place 2 threat on Earth Involvement.
#
# Cartes de reference :
#  - **`sk106`** Wrath of the Empire (scenario 1) : `Worlds.DiscardEncounterCards(n,
#    effect)` rend les cartes defaussees, lues ensuite (icones) ;
#    `FacesCounter.CountTotalBoostIcons(cartes)` compte les icones Y (hors ★).
#  - **`46028`** Burn / `sk114` : `WhenCardBecomeBoost("This", op)` ; **`next_evol/40110`**
#    + `hood/24017` : `player.GetControlCharacters()` pour « each character you control ».
#
# ⚠ Mots-pieges : « the top card » (UNE carte) ; « each boost icon (Y) » = les icones
# Y imprimees sur la carte defaussee, pas le ★ ; « 1 damage to EACH character you
# control FOR EACH icon » (N degats a chacun, pas N repartis) ; « you control »
# (heros et allies du joueur qui revele) ; Boost : la menace va sur Earth
# Involvement, absente = rien.


def GetAbilities() -> Sequence['Ability']:

    def armee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        defaussees = Worlds.DiscardEncounterCards(1, effect)
        icones = FacesCounter.CountTotalBoostIcons(defaussees)
        if icones <= 0:
            return
        for personnage in list(joueur.GetControlCharacters()):
            personnage.CastTo(Unit2).TakeDamage(this, icones, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        PlacerMenaceSurEarthInvolvement(effect, effect.this, 2)

    return [
        AbilityFactory.WhenThisRevealed(None, armee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
