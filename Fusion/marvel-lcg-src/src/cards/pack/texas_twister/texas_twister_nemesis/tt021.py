from . import *

# * Master Pandemonium — SBIRE NEMESIS. PV 5, COMPL 1, ATQ 2, 2 boost.
# [star] Forced Interrupt: When Master Pandemonium would activate against you,
#   choose to either spend an [energy] resource or exhaust your identity.
# (Texas Twister's nemesis minion.)
#
# CARTES DE REFERENCE
#  - `dr011` Nekra : structure d'un sbire nemesis a Reponse forcee.
#  - `bk018` Timebroker : `AfterEnemyActivatesAgainstYou`. ⚠ ICI C'EST
#    L'INTERRUPTION qu'il faut (`WhenEnemyActivateAgainstYou`, activate.py:44) :
#    la taxe se paie AVANT l'activation, pas apres.
#
# TEXTE CONTRE CODE
#  « CHOOSE TO EITHER ... OR ... » -> un vrai choix offert au joueur, donc
#    `ChooseAbilities` avec deux `ForChoiceAbility`. ⚠ Les deux branches
#    doivent rester possibles : un joueur sans ressource energie doit pouvoir
#    incliner son identite, et un joueur deja incline doit pouvoir payer.
#  « SPEND an [energy] resource » -> une depense de RESSOURCE, pas une
#    defausse de carte : `CostFunc.Spend(Cost("Y"))` sur la branche.
#  « EXHAUST YOUR IDENTITY » -> et l'obligation tt020 interdit justement de la
#    redresser : les deux cartes du set nemesis se repondent.
#  ⚠ PAS d'etoile a l'ATQ ni au COMPL sur le scan : les valeurs sont fixes,
#    ce ne sont pas des « par joueur ». Un sbire NEMESIS n'a de toute façon
#    jamais de multiplicateur par joueur (leçon Nekra, pack doctor_druid).


def GetAbilities() -> Sequence['Ability']:

    def payer_le_demon(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer() if hasattr(message, "GetToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return

        def incliner_l_identite(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ExhaustAll([identite], effect)

        joueur.ChooseAbilities(
            effect,
            # ⚠ `ForChoiceAbility(...).SetCost(...)` LEVE UN ASSERT :
            # « Call `ForChoiceAbilityWithCost` instead » (ability.py:342). Une
            # branche de choix qui coute quelque chose a sa propre fabrique
            # (for_choice.py:110), qui prend le cout EN PREMIER argument.
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("Y"),
                "Spend an energy resource",
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity",
                incliner_l_identite,
            ),
        )

    return [
        AbilityFactory.WhenEnemyActivateAgainstYou(
            AbilityType.ForcedInterrupt,
            "This",
            payer_le_demon,
        ),
    ]
