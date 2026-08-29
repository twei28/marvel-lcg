from . import *

# * Squirrel Girl's Costume
# Squirrel Girl gets +1 ATK.
# Hero Response: After a minion engaged with you is defeated, call 1 Squirrel.
#   Limit once per round.
#
# Ecart assume au materiel d'origine, arbitre avec l'utilisateur : le
# declencheur n'est PAS « vaincu par l'attaque de base de Squirrel Girl »
# (elle a ATK 1 : ce moteur ne demarrait jamais). Resserre le 28/08/2026 de
# « un minion est vaincu, par n'importe qui » a « un minion ENGAGE AVEC TOI est
# vaincu » : le declencheur reste atteignable, mais ne se nourrit plus des
# minions vaincus a l'autre bout de la table en multijoueur.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            AppelerEcureuil(joueur, effect)

    def engage_avec_toi(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        vaincu = message.trigger
        if vaincu is None or not Minion.IsType(vaincu):
            return False
        return vaincu.CastTo(Minion).engaged_player == joueur

    return [
        # Pas de CanPlayThisUpgradeCard : comme Supernova Helmet (28009), une
        # amelioration signature s'attache par defaut a sa propre identite.
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            attack=1,
        ),
        (AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            Minion,
            appeler,
            conditions=[engage_avec_toi],
        )
            .LimitOncePerRound()),
    ]
