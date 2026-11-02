from . import *

# The Hate Machine (MANIGANCE ANNEXE). Menace de depart 2. « While at least 1 Cassandra Control counter on your identity, you cannot attack Cassandra
# Nova or thwart the main scheme. When Revealed : For each Cassandra Controls counter in play, place 1 threat here. [star] Boost : Reveal this card. »
# Cartes de reference : 27142 Life-Size Decoy (`PlayersCannotThwartWhile`), 27106 Take One for the Team (`PlayersCannotAttackWhile`), hf110 (boost
# `RevealThisCard`), hf620.
# ⚠ « YOU cannot » : le heros (l'identite), pas ses allies (meme regle que « You » de `CheckWhichPlayerIncludeAllies`) ; la condition se lit sur
# l'identite du joueur qui agit.


def _joueur_controle(message: 'Message.CheckIfUnitCanBeAttackBy|Message.CheckIfSchemeCanBeThwartBy') -> bool:
    agissant = message.by_effect.initiator
    if not Player.IsType(agissant) or Controles(agissant) < 1:
        return False
    par = message.by_effect.this
    if Ally.IsType(par):
        return False
    if Upgrade.IsType(par) and not Identity.IsType(par.GetBindFace()):
        return False
    return True


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        n = TotalControlesEnJeu(effect)
        if n > 0:
            this.PlaceThreatOnSchemes([this], n, effect)

    return [
        AbilityFactory.PlayersCannotAttackWhile("AnyPlayer", CardFinder(name=NOM_CN, card_type=Villain),
                                                conditions=[lambda effect, message: _joueur_controle(message)]),
        AbilityFactory.PlayersCannotThwartWhile("AnyPlayer", MainScheme,
                                                conditions=[lambda effect, message: _joueur_controle(message)]),
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
