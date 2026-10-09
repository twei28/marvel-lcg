from . import *

# hs086 * White Rabbit
# Forced Response : apres avoir attaque et blesse l'identite, sans AERIAL, defausse une carte au hasard de la main.
# Boost : si l'attaque vous blesse, defaussez une carte de votre main.

def GetAbilities() -> Sequence['Ability']:

    def vous_blesse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        return identite in message.damaged_targets and not identite.HasTrait("AERIAL")

    def defausser(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        message.GetAgainstPlayer().DiscardRandomHandCards(1, effect)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        SiLAttaqueVousBlesse(
            effect, message,
            lambda joueur, degats: DefausserUneCarteDeLaMain(effect, joueur))

    return [
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", defausser, conditions=[vous_blesse]),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost, during_attack=True),
    ]
