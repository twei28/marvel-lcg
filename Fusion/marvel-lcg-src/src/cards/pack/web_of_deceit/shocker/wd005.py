from . import *

# Vibro-Shock Gauntlets

def GetAbilities() -> Sequence['Ability']:

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « After Shocker attacks and damages you, discard a card from your hand. »
        joueur = message.attacked.GetControlByPlayer()
        joueur.AskDiscardFaces(joueur.hand_cards.Get(), (1, 1), effect)

    def shocker_sonne(effect: 'Effect') -> 'CardFace|None':
        # Le vilain de ce scenario EST Shocker : la carte lui est attachee.
        villain = effect.this.CastTo(Attachment).attached_face
        if villain is None:
            return None
        return villain if villain.HasStatus("Stunned") or villain.HasStatus("Confused") else None

    def a_un_statut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # ⚠ LA MOITIE DU COUT MANQUAIT. « and remove a stunned or confused
        # status card from Shocker » n'est pas un decor : c'est une CONDITION
        # (il faut d'abord le sonner ou le desorienter) et un COUT (le statut
        # part). Sans elle, les gants se defaussaient pour deux ressources.
        return shocker_sonne(effect) is not None

    def retirer_le_statut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        villain = shocker_sonne(effect)
        if villain is None:
            return
        sonne = villain.HasStatus("Stunned")
        desoriente = villain.HasStatus("Confused")

        def enlever_sonne(cibles: 'Sequence[CardFace]') -> None:
            villain.DiscardStunned(effect, rule=1)

        def enlever_desoriente(cibles: 'Sequence[CardFace]') -> None:
            villain.DiscardConfused(effect, rule=1)

        # « a stunned OR confused status card » : quand les deux sont poses,
        # c'est au joueur de dire lequel il sacrifie — les deux ne bloquent pas
        # la meme chose.
        if sonne and desoriente:
            effect.GetInitiator().ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove the stunned status card", enlever_sonne),
                AbilityFactory.ForChoiceAbility(
                    "Remove the confused status card", enlever_desoriente),
            )
        elif sonne:
            enlever_sonne([])
        else:
            enlever_desoriente([])

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "AttachedVillain",
            "YourIdentity",
            blesse
        ),
        # « Hero Action: Spend [physical][mental] resources and remove a stunned
        # or confused status card from Shocker -> discard Vibro-Shock Gauntlets. »
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            conditions=[a_un_statut],
            ex_operation=retirer_le_statut,
        ).SetCost(Cost("RB")),
    ]
