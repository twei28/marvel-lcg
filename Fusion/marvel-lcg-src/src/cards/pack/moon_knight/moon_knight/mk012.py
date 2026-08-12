from . import *

# Seek Help — custom « DesignHacker » (obligation de Moon Knight)
# Give to the Marc Spector player. You may flip to Marc Spector. Choose:
# - Exhaust Marc Spector -> remove Seek Help from the game.
# - Take 2 indirect damage -> discard this obligation.
# (Le texte d'origine defausse Steven Grant et Jake Lockley de la pile
#  d'identités, notion que le moteur n'a pas : l'option devient un simple
#  epuisement de l'identité, écart documenté au §9.)


def GetAbilities() -> Sequence['Ability']:

    def seek_help(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        face_marc = TrouverFaceIdentite(player, "Marc Spector")
        if face_marc is not None:
            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Flip to Marc Spector",
                    lambda t: player.GetIdentity().ChangeToFace(face_marc, effect),
                ),
            )

        def degats_puis_defausse(targets: Sequence['CardFace']) -> None:
            identite = player.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(2, effect)
            Faces.DiscardAll([this], effect)

        sur_marc = player.GetIdentity() is not None and \
            player.GetIdentity().IsName("Marc Spector")

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Marc Spector → remove Seek Help from the game",
                lambda t: Faces.RemoveAllFromGame([this], effect),
                condition=sur_marc,
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Take 2 indirect damage. Discard this obligation",
                degats_puis_defausse,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            seek_help
        )
    ]
