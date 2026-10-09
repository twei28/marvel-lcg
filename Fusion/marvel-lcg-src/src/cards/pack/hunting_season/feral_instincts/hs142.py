from . import *

# hs142 Primal Strength
# Attach to the villain. ATK+X, X = villain's stage number (ATK+ mis a 0 dans cards.json,
# valeur dynamique ci-dessous). Interrupt: When the villain attacks you, choose to either
# spend [physical][physical] or exhaust your identity -> discard Primal Strength.

def GetAbilities() -> Sequence['Ability']:

    def payer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = message.GetAgainstPlayer()
        identite = joueur.GetIdentity()

        def epuiser(cibles):
            Faces.ExhaustAll([identite], effect)
            Faces.DiscardAll([effect.this], effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("RR"), None, lambda cibles, res: Faces.DiscardAll([effect.this], effect)),
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity", epuiser,
                condition=identite is not None and identite.IsReady()),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Villain)),
        *AbilityFactory.GiveKeywordToAttached(
            attack=1,
            get_new_value=lambda effect, face, faces: face.printed_stage,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "AttachedVillain",
            payer,
            against_player="You",
        ),
    ]
