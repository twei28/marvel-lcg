from . import *

# * Red Wolf (William Talltrees) — ALLIE BASIC, cout 4, PV 4,
#   CTR 2** / ATQ 2**. RANGER. [physical].
# Response: After an ally enters play under your control, reduce all
#   consequential damage Red Wolf takes by 1 until the end of the phase.
#
# CARTES DE REFERENCE
#  - `bk016` Tallus : `AfterCardEnterPlay(..., under_your_control=True)`.
#  - `dt035` Gladiator et `33016` Coordinated Attack : les degats consequents.
#
# TEXTE CONTRE CODE
#  ⚠ « UNDER YOUR CONTROL » -> `under_your_control=True` : l'allie d'un autre
#    joueur ne declenche rien. Le parametre existe sur la fabrique
#    (card_move.py:117), l'oublier rendrait la carte deux fois trop bonne en
#    multijoueur.
#  « until the end of the PHASE » -> il n'existe PAS de `GainUntilPhaseEnd`
#    acceptant les degats consequents (face_action.py:481 ne prend que
#    trait/main/ATQ/DEF/complot/CTR/riposte). On passe donc par `TemporaryGain`
#    directement, avec `Message.WhenPhaseEnd` comme evenement de fin — c'est
#    exactement ce que `GainUntilPhaseEnd` fait sous le capot.
#  « an ALLY enters play » -> Red Wolf LUI-MEME compte quand il arrive : rien
#    dans le texte ne l'exclut, et le moteur declenche bien sur sa propre
#    entree. C'est un bonus gratuit au tour ou on le pose.
#  ⚠ CTR et ATQ a `2**` : DEUX degats consequents chacun. La carte rend donc
#    ses pouvoirs de base soutenables, et c'est tout son interet.


def GetAbilities() -> Sequence['Ability']:

    def meute(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.TemporaryGain(
            effect,
            None,
            Message.WhenPhaseEnd,
            attack_consequential_damage=-1,
            thwart_consequential_damage=-1,
        )

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Ally,
            meute,
            under_your_control=True,
        ),
    ]
