from . import *

# Fisk Tower

def GetAbilities() -> Sequence['Ability']:

    def menace_de_depart(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        # « Each facedown CORRUPT side scheme has starting threat equal to the
        # villain's stage number. »
        #
        # Le patron `wd106` entre en jeu a zero : c'est la tour qui le charge, et
        # c'est fidele — sans elle, la regle n'existerait pas.
        manigance = message.trigger.CastTo(EncounterSideScheme)
        stade = Worlds.GetVillainStage(effect)
        if stade > 0:
            manigance.PlaceThreatOnSchemes([manigance], stade, effect)

    def soigner(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        # « Forced Response: After step one of the villain phase, heal 1 damage
        # from Kingpin and Kingpin's Suit for each CORRUPT side scheme in play. »
        this = effect.this.CastTo(Environment)
        combien = len(Worlds.FindCardsOnField(effect, trait="CORRUPT", card_type=Scheme2))
        if combien <= 0:
            return

        villain = Worlds.FindVillain(effect)
        if villain:
            this.HealthUnits([villain], combien, effect)

        # Le costume n'est pas une unite : ses degats sont des JETONS poses
        # dessus par sa propre interruption. On les lui retire donc un a un.
        costume = Worlds.FindCardOnField(
            effect, name="Kingpin's Suit", card_type=Attachment)
        if costume:
            Faces.RemoveCountersOn([costume], combien, 'damage', effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            CardFinder(card_ids=["wd106"]),
            menace_de_depart
        ),
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            soigner
        ),
    ]
