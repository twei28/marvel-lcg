from . import *

# Calm Before the Storm — AMELIORATION, cout 2, [energy]. SKILL. SUPERPOWER.
# Your hero gets +1 ATK while Stormbreaker is in play and +1 THW while it is
#   not in play.
# Hero Action: Spend 1 resource of any type and exhaust this card -> resolve
#   your hero's Worthy ability (ignoring its limit).
#
# ⚠ LA CARTE EST BONNE DANS LES DEUX SENS, ET C'EST TOUT SON INTERET. Le
# marteau passe son temps a faire l'aller-retour main <-> jeu : ici, chacune
# des deux positions donne un bonus, l'une offensive, l'autre au contre.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir : `GiveKeywordToAttached`, bonus d'amelioration de heros.
#  - `as012` Night Vision (pack armored_spidey) : ⚠ LA LEÇON DU
#    `change_on_event` — une condition CONTINUE relue a chaque changement.
#    Sans lui, le bonus reste fige a sa valeur du moment ou il a ete calcule.
#
# TEXTE CONTRE CODE
#  DEUX bonus EXCLUSIFS, jamais les deux ensemble : deux `GiveKeywordToAttached`
#    a conditions opposees. `OnEvent.CardInPlay(CardFinder(name=...))` recalcule
#    les deux des que Stormbreaker entre ou sort du jeu.
#  « resolve your hero's WORTHY ability (IGNORING ITS LIMIT) » -> on rejoue le
#    corps partage `ResoudreWorthy`, et surtout PAS la capacite de br001a
#    elle-meme : celle-ci porte `.LimitOncePerRound()`, que le texte demande
#    justement d'ignorer.
#  « SPEND 1 resource AND EXHAUST this card » -> DEUX couts chaines
#    (modele `fne/60020`), pas un choix entre les deux.


def GetAbilities() -> Sequence['Ability']:

    def marteau_en_jeu(effect: 'Effect') -> bool:
        return MarteauEnJeu(effect) is not None

    def marteau_absent(effect: 'Effect') -> bool:
        return MarteauEnJeu(effect) is None

    def calme_avant_la_tempete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        ResoudreWorthy(effect, JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            attack=1,
            get_new_value=lambda effect, face, ui: 1 if marteau_en_jeu(effect) else 0,
            ex_change_on_event=OnEvent.CardInPlay(CardFinder(name=NOM_MARTEAU)),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            thwart=1,
            get_new_value=lambda effect, face, ui: 1 if marteau_absent(effect) else 0,
            ex_change_on_event=OnEvent.CardInPlay(CardFinder(name=NOM_MARTEAU)),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            calme_avant_la_tempete,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("1")),
    ]
