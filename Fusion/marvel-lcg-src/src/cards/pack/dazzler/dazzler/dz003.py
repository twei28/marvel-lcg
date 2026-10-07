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
# « This ROUND » : `in_this="Round"` (ajoute au moteur le 06/10/2026). La
# reduction survit donc a la fin de la phase des joueurs et couvre aussi une
# carte jouee en reaction pendant la phase du vilain. Avant, seul « Phase »
# existait et la reduction tombait a la fin de la phase des joueurs.


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
            in_this="Round",
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
