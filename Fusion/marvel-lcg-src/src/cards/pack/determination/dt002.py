from . import *

# * Moon Knight

def GetAbilities() -> Sequence['Ability']:

    def moon_knight(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        faces = initiator.DiscardHandCards((1, 1), effect)
        if not faces:
            return

        res = FacesCounter.GetPrintedResources(faces)

        ability_y = AbilityFactory.ForChoiceAbility(
            "Draw a card",
            lambda targets:
                initiator.DrawUp(1, effect)
        ).SetHasNoTargetEffect()

        ability_b = AbilityFactory.ForChoiceAbility(
            "Confuse an enemy",
            lambda targets:
                Faces.GiveStatus(targets, "Confused", effect)
        ).SetTarget(Enemy)

        ability_r = AbilityFactory.ForChoiceAbility(
            "Stun an enemy",
            lambda targets:
                Faces.GiveStatus(targets, "Stunned", effect)
        ).SetTarget(Enemy)

        # « includes » et non « is » : une carte a plusieurs icones declenche
        # plusieurs lignes, d'ou des `if` separes (c'est ce que fait 17011).
        # Le joker demande DEUX des trois lignes, et le moteur sait le dire :
        # `choose_x_different_options` retire l'option deja prise.
        if res.g:
            initiator.ChooseAbilities(
                effect,
                ability_y,
                ability_b,
                ability_r,
                choose_x_different_options=2,
            )
        if res.y:
            initiator.ChooseAbilities(effect, ability_y)
        if res.b:
            initiator.ChooseAbilities(effect, ability_b)
        if res.r:
            initiator.ChooseAbilities(effect, ability_r)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            moon_knight
        ),
    ]
