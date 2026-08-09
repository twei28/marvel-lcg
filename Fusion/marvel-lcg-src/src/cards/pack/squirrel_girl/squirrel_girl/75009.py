from . import *

# * Squirrel Girl's Costume
# Squirrel Girl gets +1 ATK.
# Hero Response: After a minion is defeated, call 1 Squirrel. Limit once per round.
#
# Ecart assume au materiel d'origine, arbitre avec l'utilisateur : le
# declencheur est « un vilain est vaincu », par n'importe quelle source, et non
# « vaincu par l'attaque de base de Squirrel Girl ». Squirrel Girl a ATK 1 :
# adosser son moteur a son attaque de base ne demarrait jamais.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            AppelerEcureuil(joueur, effect)

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
        )
            .LimitOncePerRound()),
    ]
