from . import *

# * The Witches' Road — soutien signature. LOCATION. Cout 1.
# Response: After a MYSTIC alter-ego changes into hero form, exhaust The
#   Witches' Road -> reduce the resource cost of the next SPELL card that
#   hero plays this phase by 1. Shuffle 2 cards from that hero's discard
#   pile into their deck.
#
# Cartes de reference (RECETTES) :
#  - le declencheur : `AfterUnitChangeForm(..., to_form=Hero)` (form.py),
#    filtre MYSTIC sur l'unite qui bascule ;
#  - la reduction « next SPELL this phase » : 16024 Deft Focus, MEME effet
#    (`Worlds.UpdateNextCardPlayCost(joueur, -1, ..., finder=
#    CardFinder2("SPELL"), in_this="Phase")`) ;
#  - le remelange : an014 (`Faces.ShuffleAllTo`) + choix wd005
#    (`AskChooseFaces` dans la defausse de CE heros).
#
# ⚠ « a MYSTIC alter-ego » : N'IMPORTE quel joueur MYSTIC de la table (Wanda
# officielle, Wiccan, Doctor Strange...), pas seulement Agatha — et les
# effets visent « THAT hero », le joueur qui vient de basculer.

def GetAbilities() -> Sequence['Ability']:

    def witches_road(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        joueur = message.trigger.GetControlByPlayer()
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur,
            -1,
            effect,
            finder=CardFinder2("SPELL"),
            in_this="Phase",
        )
        defausse = joueur.discard_pile.Get(True)
        if defausse:
            choisies = joueur.AskChooseFaces(list(defausse), (0, 2), effect)
            if choisies:
                Faces.ShuffleAllTo(list(choisies), joueur.player_deck, effect)

    def est_mystic(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> bool:
        return message.trigger.HasTrait("MYSTIC")

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            Identity,
            witches_road,
            to_form=Hero,
            conditions=[est_mystic],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
