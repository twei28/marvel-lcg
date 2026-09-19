from . import *

# Energy Gatling Gun
# Attach to Hammerhead. (+1 ATK : cle desc "ATK+", base automatique.)
# Forced Response: After Hammerhead attacks, if the attacked character was not
#   defeated, discard this card -> Hammerhead attacks that character again.
#
# La fleche fait de la defausse un COUT (al014, 42030 : CostFunc.Discard("This")).
# « that character » : l'unite qui a subi l'attaque (defenseur ou identite).
# Un allie se re-attaque par BasicAttack([allie]) (modele 50096 Leaping Kick),
# une identite par DoAttackYou. La carte etant defaussee en cout, la seconde
# attaque ne peut pas relancer la reponse : pas de boucle.

def GetAbilities() -> Sequence['Ability']:

    def personnage_attaque(message: 'Message.AfterUnitAttackEnd') -> 'Unit2|None':
        cibles = [u for u in message.attacked_targets if u.IsInPlay() and not u.IsDefeated()]
        return cibles[0] if cibles else None

    def survivant(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return personnage_attaque(message) is not None

    def re_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)
        hammerhead = TrouverHammerhead(effect)
        cible = personnage_attaque(message)
        if hammerhead is None or cible is None:
            return
        if Identity.IsType(cible):
            joueur = cible.GetControlByPlayer()
            hammerhead.DoAttackYou(joueur, effect)
        else:
            hammerhead.BasicAttack([cible], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Hammerhead")
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Hammerhead"),
            re_attaque,
            conditions=[survivant],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
