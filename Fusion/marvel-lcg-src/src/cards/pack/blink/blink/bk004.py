from . import *

# Everywhere at Once (x3) — EVENEMENT, cout 0, [physical]. ATTACK. THWART.
# Hero Action (attack/thwart): Deal 2 damage to each enemy with a [[PORTAL]]
#   upgrade attached. Remove 2 threat from each scheme with a [[PORTAL]]
#   upgrade attached.
#
# La carte de recompense du moteur : cout NUL, effet multiplie par le nombre
# de portails deployes. Trois exemplaires, la plus frequente du deck.
#
# TEXTE CONTRE CODE
#  « EACH enemy / EACH scheme WITH a PORTAL attached » -> aucune cible a
#    choisir, mais un FILTRE : seules les cartes qui en portent un. Sans
#    portail en jeu, la carte ne fait STRICTEMENT rien — c'est voulu.
#  « (attack/thwart) » -> DEUX libelles sur le meme `SetLabel`.


def GetAbilities() -> Sequence['Ability']:

    def partout_a_la_fois(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        ennemis = [e for e in Worlds.GetOnFieldEnemies(effect) if PorteUnPortail(effect, e)]
        if ennemis:
            this.DealDamage(ennemis, 2, effect)
        manigances = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                      if PorteUnPortail(effect, s)]
        if manigances:
            this.RemoveThreatFromSchemes(manigances, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            partout_a_la_fois,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
