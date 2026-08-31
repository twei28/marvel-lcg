from . import *

# * Kingpin — sbire nemesis. EARTH-6160. ELITE. PV 8 / SCH 1* / ATK 1*.
# [star] Kingpin gets +1 SCH and +1 ATK for each side scheme in play.
# (Green Goblin's nemesis minion.)
# [star] Boost: Place 2 threat on each side scheme.
#
# Cartes de reference :
#  - le gain par complot annexe : 04125 * Red Skull, MOT POUR MOT « gets +1
#    ATK for each side scheme in play », rendu par
#    `ThisGainKeywordForEachFaceInPlay(CardFinder(card_type=SchemeSide2),
#    attack=1)` — etendu ici avec `scheme=1` (01059 * Jessica Jones porte le
#    pendant THW du meme motif). Le moteur code l'etoile de Red Skull sans
#    verrou Expert : meme convention ici ;
#  - le boost : an013 Hel-Wolf pour `WhenCardBecomeBoost("This", ...)`, et
#    50134 Innocent Bystanders pour `PlaceThreatOnSchemes` — la cible
#    "EachSideScheme" est un litteral du moteur (card_face.py:621).
#
# ⚠ Le boost nourrit ho014/ho017 ET tout autre complot annexe du scenario :
# c'est le coeur du set, Kingpin grossit avec ce que son boost entretient.
#
# ⚠ Homonymes : vilain wd091-wd093 (campagne Web of Deceit) et sbire 60061
# (Echo Nemesis) — sets distincts, aucun partage de code.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)

        this.PlaceThreatOnSchemes("EachSideScheme", 2, effect)

    return [
        AbilityFactory.ThisGainKeywordForEachFaceInPlay(
            CardFinder(card_type=SchemeSide2),
            attack=1,
            scheme=1,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
