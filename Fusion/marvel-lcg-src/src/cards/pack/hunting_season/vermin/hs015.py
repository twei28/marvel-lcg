from . import *

# Vermin Clone (hs015)
# Guard (mot-cle de base). While engaged with you, characters you control cannot
# attack Regular Rats and Feral Rats. [star] Boost: Give the attacking enemy an
# additional boost card for this activation.
# Modeles : PlayersCannotAttackWhile (27106, 32080), 50145 (boost supplementaire).

def GetAbilities() -> Sequence['Ability']:

    def meme_joueur(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        joueur = effect.this.CastTo(Minion).engaged_player
        return joueur is not None and message.by_effect.GetInitiator() == joueur

    def boost_supplementaire(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GiveActivatingEnemyAdditionalBoostCard(1, effect)

    return [
        AbilityFactory.PlayersCannotAttackWhile(
            "AnyPlayer",
            CardFinder(names=["Regular Rats", "Feral Rats"], card_type=Minion),
            conditions=[meme_joueur],
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost_supplementaire),
    ]
