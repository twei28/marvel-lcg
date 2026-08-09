from . import *

# * Enchantress

def GetAbilities() -> Sequence['Ability']:

    def enchantress_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        face = SetupCards.PutIntoPlay(
            effect,
            name="Future of Despair",
            from_where=["SetAside"],
        )

        if face:
            # CORRECTIF : le stade III imprime 4 menaces PAR HEROS. Le « 3* »
            # est la valeur du stade II (55002), recopiee par erreur.
            this.PlaceThreatOnSchemes([face], "4*", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            enchantress_revealed
        ),
        # CORRECTIF : la Reponse Forcee « After Enchantress attacks you, place
        # 1 charm counter » manquait sur CE stade seulement (les stades I et II
        # appellent bien le helper partage).
        AfterEnchantressAttacksYouPlaceCharmCounter(),
    ]

