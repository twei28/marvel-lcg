from . import *

# Forces Combined — custom « DesignHacker »
# Immutable. Permanent. Setup.
# Interrupt: When you would spend resources on a card or ability, exhaust
#   Forces Combined → you may spend resources from both of your hands for that
#   card or ability.
#
# Depuis la refonte du 5/8/2026, les DEUX mains existent vraiment (Cloak et
# Dagger sont deux identités liées, donc deux joueurs). La carte se rend donc
# au texte, en deux morceaux :
#
#   1. l'AUTORISATION est portée par le moteur, dans
#      `CheckAnyPlayerMayHelpPay` (game/ability/factory/resources.py), le
#      crochet par lequel il laisse déjà un autre joueur financer un coût
#      (mot-clé Alliance, Coordinated Effort 58032). Elle exige que Forces
#      Combined soit en jeu et PRÊTE ;
#   2. l'INCLINAISON est ici : dès qu'une carte venue de l'autre main est
#      réellement dépensée, Forces Combined s'incline, ce qui ferme le robinet
#      jusqu'au prochain redressement.
#
# L'ancienne adaptation (« Resource : exhaust → 1 [wild] ») est supprimée : la
# carte imprimée ne génère aucune ressource, elle ne fait qu'autoriser.


def GetAbilities() -> Sequence['Ability']:

    def incliner(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.ExhaustAll([this], effect)

    def paye_depuis_l_autre_main(effect: 'Effect',
                                 message: 'Message.WhenCardBeSpendAsResource') -> bool:
        from game.player import Player
        this = effect.this
        if this.IsExhaust():
            return False
        payeur = message.GetToPlayer()
        proprietaire = message.trigger.GetOwner()
        if payeur is None or not isinstance(proprietaire, Player):
            return False
        # Seule une carte venue d'une AUTRE main déclenche l'inclinaison : payer
        # avec sa propre main n'a jamais eu besoin de Forces Combined.
        return proprietaire != payeur

    return [
        AbilityFactory.AfterGenerateResources(
            AbilityType.Rule,
            "AnyPlayer",
            incliner,
            conditions=[paye_depuis_l_autre_main],
        ).SetName("Forces Combined"),
    ]
