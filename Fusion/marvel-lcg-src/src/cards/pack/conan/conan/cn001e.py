from . import *

# * Conan — alter-ego roi (mis de cote au Setup). KING. REC 3, 11 PV, main 6.
# Battle-Forged — Response: After you change to this form, choose:
#   • Give King Conan a tough status card.
#   • Remove all crom counters from The Cimmerian -> heal 1 damage from King
#     Conan for each crom counter removed this way.
#
# CARTES DE REFERENCE
#  - `AfterUnitChangeForm(type, "You", op, to_this_form=True)` (12001b Scott
#    Lang, officiel).
#  - choix a deux branches : `ChooseAbilities(ForChoiceAbility(...), ...)`
#    (44043 Bob, Agent of Hydra).
#
# TEXTE CONTRE CODE
#  « After you change to this form » : un vrai changement de forme. Le
#    couronnement (The Cimmerian) n'en est PAS un (arbitrage du 25/09/2026) :
#    il retourne la carte sans message de changement de forme.
#  « heal 1 damage from King Conan » : l'identite (un seul cadran de PV pour
#    toutes les faces), meme si l'on est sur l'alter-ego a ce moment.


def GetAbilities() -> Sequence['Ability']:

    def battle_forged(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        this = effect.this
        joueur = JoueurDe(effect)
        if joueur is None:
            return

        def tenace(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.GiveStatus([joueur.GetIdentity()], "Tough", effect)

        def soigner(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            cim = TrouverCimmerian(joueur, effect)
            if cim is None:
                return
            n = cim.CastTo(CanPlaceCounter).GetCounters('crom')
            if n <= 0:
                return
            Faces.RemoveCountersOn([cim], "All", 'crom', effect)
            this.HealthUnits([joueur.GetIdentity()], n, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Give King Conan a tough status card", tenace),
            AbilityFactory.ForChoiceAbility(
                "Remove all Crom counters from The Cimmerian -> heal 1 damage per counter",
                soigner,
            ),
        )

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            battle_forged,
            to_this_form=True,
        ).SetName("Battle-Forged"),
    ]
