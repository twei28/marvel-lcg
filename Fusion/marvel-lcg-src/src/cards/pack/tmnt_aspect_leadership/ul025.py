from . import *

# * Shōgun « Leo » — ALLIE Leadership (TMNT Aspects, Inkwire), cout 2, [physical]. NINJA. SAMURAI. TURTLE.
# THW 1* / ATQ 1* / PV 2.
# Response: After Shugun [sic] enters play, discard an ally from your hand -> give an ally a tough status
#   card.
#
# « Shugun » est une coquille du scan pour le titre « Shōgun » : une seule carte peut entrer en jeu et
# declencher sa propre Reponse, la lecture n'a pas d'alternative (cosmetique, notee dans le fichier des
# questions, non bloquante). Le texte du jeu la conserve telle qu'imprimee.
#
# CARTES DE REFERENCE
#  - `03013` Squirrel Girl : `AfterCardEnterPlay(Response, "This", op)`.
#  - `ar010` / `td001b` : « discard N card(s) from your hand -> » = `CostFunc.Discard("YourHandCards",
#    ..., range=(1, 1))`, ici filtre sur le type Allie (`card_type=Ally`).
#  - `49018` Noble Sacrifice / `62018` : « give X a tough status card » = `Faces.GiveStatus(..., "Tough")`.
#
# TEXTE CONTRE CODE
#  ⚠ « discard AN ALLY from YOUR HAND » est DEVANT la fleche : un COUT. Sans allie en main, la Reponse
#    n'est pas proposee.
#  ⚠ « give AN ally » : n'importe quel allie en jeu (le sien, Shōgun lui-meme, ou celui d'un autre
#    joueur), pas l'identite.
#  ⚠ Response facultative. Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def shogun(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        Faces.GiveStatus(effect.targets, "Tough", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            shogun,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", card_type=Ally, range=(1, 1)))
        .SetTarget(Ally),
    ]
