from . import *

# "A Little Girl's Dream"
# SONG.
# Hero Action: Reduce the resource cost of the next ally or event you play this
#   round by 3.
# Showtime!: Confuse a non-ELITE enemy.
#
# `Worlds.UpdateNextCardPlayCost` est le crochet du moteur pour « la prochaine
# carte que tu joues » (modele Evaluate Threat 59028, Recruitment Drive 59023).
#
# ECART ASSUME, minime : la carte dit « this ROUND », le moteur ne connait que
# `in_this="Phase"` ou `"Turn"`. On prend « Phase », la plus large des deux :
# elle couvre toute la phase des joueurs, donc tout le temps ou l'on joue
# normalement un allie ou un evenement. Une carte jouee en reaction PENDANT la
# phase du vilain ne beneficierait pas de la reduction.


def GetAbilities() -> Sequence['Ability']:

    def reve(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur, -3, effect,
            finder=CardFinder(card_type=Ally | Event),
            in_this="Phase",
        )

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        Faces.GiveStatus(CiblesShowtime(effect), "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reve,
        ).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget(Enemy, non_trait="ELITE",
                                    canbe_confused=True, range=(0, 1)),
    ]
