from . import *

# Shockwave (2e exemplaire) — custom « Rainy » (cout X)
# Hero Action: Discard the top X cards of your deck (to a maximum of 5). For
#   each [physical] resource discarded this way, deal 2 damage to each enemy.
#   For each [mental] resource discarded this way, remove 2 threat from each
#   scheme.
#
# On compte les ressources IMPRIMEES des cartes defaussees, pas les ressources
# depensees : ce sont deux notions differentes, et c'est bien la premiere
# qu'imprime la carte (« each [physical] resource discarded this way »). Une
# carte a double icone compte donc deux fois.
#
# Une icone [wild] compte pour CHAQUE couleur, comme le fait Hulk 01050 (carte
# officielle, meme montage : defausse du dessus du deck puis lecture de l'icone
# imprimee), ou `resource.g > 0` declenche tous les effets de couleur.

def GetAbilities() -> Sequence['Ability']:

    def shockwave(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        joueur = effect.GetInitiator()

        x = min(effect.GetCostX(), 5)
        if x <= 0:
            return

        defaussees = joueur.PopPlayerDeckCards(
            x,
            lambda face: Faces.DiscardAll([face], effect),
            effect,
        )
        if not defaussees:
            return

        icones = FacesCounter.GetPrintedResources(defaussees)
        physiques = icones.r + icones.g
        mentales = icones.b + icones.g

        if physiques > 0:
            ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))
            if ennemis:
                this.DealDamage(ennemis, 2 * physiques, effect)

        if mentales > 0:
            plans = list(Worlds.FindCardsOnField(effect, card_type=Scheme2))
            if plans:
                this.RemoveThreatFromSchemes(plans, 2 * mentales, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shockwave,
        ).SetPlay(hero_form_only=True),
    ]
