from . import *

# Symbiotic Drop Kick — EVENEMENT, cout 3, RES [physical]. ATTACK. SYMBIOTE.
# Hero Action (attack): Deal 4 damage to an enemy. If you paid for this card
#   using only [physical] resources, stun that enemy and draw 1 card.
#
# CARTE DE REFERENCE
#  - `10014` Drop Kick (Agression, pack hlk) : MEME TEXTE MOT POUR MOT, meme
#    cout, meme ressource. L'insert le dit — les huit « Symbiotic » sont les
#    versions symbiote de cartes deja au catalogue, elles ne changent que de
#    titre et gagnent le trait SYMBIOTE, ce qui les rend cumulables avec
#    l'original dans un deck a deux aspects. Le corps est donc celui de
#    `10014`, repris SANS RIEN Y CHANGER : toute divergence serait un bug.
#
# TEXTE CONTRE CODE
#  ⚠ « using ONLY [physical] resources » -> `OnlyHasColor("R")`, pas
#    `HasColor` : payer avec un [physical] et un [wild] ne doit RIEN donner.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_drop_kick(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        this.DealDamage(effect.targets, 4, effect)

        if effect.GetPaidResources().OnlyHasColor("R"):
            Faces.GiveStatus(effect.targets, "Stunned", effect)
            initiator = effect.GetInitiator()
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            symbiotic_drop_kick
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
    ]
