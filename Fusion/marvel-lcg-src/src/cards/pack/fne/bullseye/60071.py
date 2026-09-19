from . import *

# Incessant Pursuit (CONDITION)
# Attach to an ally without Incessant Pursuit attached. Otherwise, surge.
# Forced Interrupt: When the villain would attack you, it attacks attached
#   ally instead and the attack gains overkill. If this attack defeats
#   attached ally, remove them from the game.
# Modeles : 21178 Beguiled (finder not_with_attach), 50096 Leaping Kick
# (BasicAttack([allie], overkill)), RECETTES §2 « instead ».
# « you » = le joueur qui controle l'allie attache.

def GetAbilities() -> Sequence['Ability']:

    def contre_moi(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Attachment)
        allie = this.GetBindFace()
        joueur = message.GetAgainstPlayer()
        # ⚠ L'attaque de remplacement (BasicAttack sur l'allie) repasse ici :
        # sans ce garde, recursion infinie (constate au harnais).
        cibles = list(getattr(message, 'targets', None) or getattr(message, 'attacked_targets', None) or [])
        if allie is None or allie in cibles:
            return False
        return joueur is not None and allie.GetControlByPlayer() is joueur

    def poursuite(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        allie = this.GetBindFace()
        vilain = message.trigger.CastTo(Villain)
        if allie is None:
            return
        message.SetBeInstead(effect)
        vilain.BasicAttack(
            [allie], effect,
            property=AttackProperty(overkill=True),
            if_this_defeat_unit=lambda unite: Faces.RemoveAllFromGame([unite], effect),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Ally, not_with_attach=CardFinder(name="Incessant Pursuit")),
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            Villain,
            poursuite,
            conditions=[contre_moi],
        ),
    ]
