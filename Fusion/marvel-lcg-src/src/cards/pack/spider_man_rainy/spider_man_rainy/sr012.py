from . import *

# Impact Webbing — custom « Rainy » (carte de regles, Permanent. Setup.)
# Forced Interrupt: When a webbed enemy activates, remove all web counters
#   from that enemy -> that enemy gets -1 SCH and -1 ATK for each web counter
#   removed this way for that activation.
#
# Une activation etant soit une attaque soit une intrigue, on intercepte les
# deux messages et on n'applique que la statistique concernee ; le retrait des
# compteurs est integral dans les deux cas. Le plafond de 3 compteurs par
# ennemi (regle du livret) est egalement porte ici : la carte est Permanent et
# en jeu des le setup, la regle vaut donc pour toute la partie.

def GetAbilities() -> Sequence['Ability']:

    def attaque_entoilee(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        cible = message.attacker
        n = cible.GetCounters('web')
        if n <= 0:
            return
        Faces.RemoveCountersOn([cible], "All", 'web', effect)
        message.GainATKForThisAttack(-n, effect)

    def intrigue_entoilee(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        cible = message.trigger
        n = cible.GetCounters('web')
        if n <= 0:
            return
        Faces.RemoveCountersOn([cible], "All", 'web', effect)
        message.GainSCHForThisScheme(-n, effect)

    def attaquant_toile(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return message.attacker.GetCounters('web') > 0

    def intrigant_toile(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> bool:
        return message.trigger.GetCounters('web') > 0

    def maximum_3(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> None:
        message.maximum = 3

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            Enemy,
            attaque_entoilee,
            conditions=[attaquant_toile],
        ).SetName("Impact Webbing"),

        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            Enemy,
            intrigue_entoilee,
            conditions=[intrigant_toile],
        ).SetName("Impact Webbing"),

        AbilityFactory.WhenCardWouldBePlacedCounter(
            AbilityType.Rule,
            CardFinder(card_type=Enemy),
            'web',
            maximum_3,
        ),
    ]
