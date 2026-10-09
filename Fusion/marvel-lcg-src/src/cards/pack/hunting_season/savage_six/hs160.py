from . import *

# hs160 * Scorpion
# [star] +1 SCH tant que l'identite engagee avec lui est etourdie. [star] Forced Response : apres qu'il attaque et blesse
# un personnage, ce personnage est etourdi. Boost : +1 icone de boost si vous etes etourdi.

def GetAbilities() -> Sequence['Ability']:

    def identite_etourdie(effect: 'Effect', ui: List['CardFace']) -> int:
        joueur = effect.this.CastTo(Minion).engaged_player
        return 1 if joueur is not None and joueur.GetIdentity().IsStunned() else 0

    def etourdi(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        return message.GetToPlayer().GetIdentity().IsStunned()

    return [
        AbilityFactory.ThisGainKeyword(identite_etourdie, scheme=1, change_on_event=OnEvent.Status(Unit2, 'Stunned')),
        MalusApresDegats("Stunned"),
        BoostPourIconeSi(etourdi),
        IconeEnPlus(),
    ]
