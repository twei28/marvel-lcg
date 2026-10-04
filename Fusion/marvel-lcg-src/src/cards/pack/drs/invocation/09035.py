from . import *

# Vapors of Valtorr

def GetAbilities() -> Sequence['Ability']:

    def vapors_of_valtorr(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        for target in effect.targets:
            face = target.GetBindFace().CastTo(Unit2)
            status_card = target.CastTo(StatusCard)
            status_target = status_card.GetBindFace()

            select_status = initiator.DeclareStatusCard(
                confused=face.CanbeConfused(),
                tough=face.CanGainTough(),
                stunned=face.CanbeStunned()
            )

            if select_status:
                if Faces.GiveStatus([status_target], select_status, effect):
                    Faces.DiscardAll([status_card], effect)

        PlaceThisCardInInvocationDeckDiscardPile(this, effect)


    return [
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            vapors_of_valtorr
        # « Choose a status card in play » : une cible OBLIGATOIRE des qu'un statut
        # existe. `range=(0, 1)` laissait valider a 0 cible, et le sort partait a
        # la defausse sans rien remplacer (meme piege que 09032, signalement n°51).
        # Sans aucun statut en jeu le sort reste lancable a vide : il peut encore
        # partir a la defausse de l'Invocation, ce qui change l'etat du jeu (ruling
        # FFG de Images of Ikonn, voir 09033), donc le minimum retombe a 0.
        ).SetTarget(StatusCard, range=(lambda effect: min(1, len(effect.context.all_legal_targets)), 1))
        .NoOutOfPlayLimit()
    ]

