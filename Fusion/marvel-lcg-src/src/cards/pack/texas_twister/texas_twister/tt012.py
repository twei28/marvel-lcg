from . import *

# * Armadillo (Antonio Rodriguez) — ALLIE PROTECTION, cout 4, PV 3,
#   CTR 0* / ATQ 3**. RANGER. [physical].
# Armadillo enters play with 2 shell counters on him.
# Response: After a minion enters play, remove 1 shell counter from Armadillo
#   -> give Armadillo a tough status card.
#
# CARTES DE REFERENCE
#  - `sr014` (pack spider_man_rainy) : `ThisEnterPlayWithCounters(n, 'nom')`,
#    et la leçon qui va avec — un compteur maison doit d'abord etre declare
#    dans `CardFace.COUNTER` (card_face.py:152), sinon `IsCounter` le refuse
#    et la PARTIE tombe des sa creation.
#  - `bk016` Tallus : `AfterCardEnterPlay` en Reponse.
#
# TEXTE CONTRE CODE
#  « remove 1 shell counter » est un COUT (fleche) -> `CostFunc.Counter`, et
#    non un effet : plus de compteur, plus de Reponse. C'est la limite de la
#    carte, et il ne faut donc PAS ajouter de `LimitOncePerRound`.
#  « After A MINION enters play » -> n'importe quel sbire, y compris ceux des
#    autres joueurs et ceux poses par le vilain. Pas de filtre de controle.
#  « give ARMADILLO a tough status card » -> a LUI, pas au heros : c'est un
#    mur qui encaisse, pas un soutien.
#  ⚠ ATQ `3**` = DEUX degats consequents, contre `0*` (un seul) au contre.
#    C'est la lecture de `21012` Power Man, ou `0**` existe deja.


def GetAbilities() -> Sequence['Ability']:

    def rentrer_la_carapace(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.ThisEnterPlayWithCounters(2, 'shell'),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Minion,
            rentrer_la_carapace,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'shell')),
    ]
