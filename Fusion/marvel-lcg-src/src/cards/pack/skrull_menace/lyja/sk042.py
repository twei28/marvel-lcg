from . import *

# Posing as a Civilian (x2) — EVENEMENT TREACHERY, cout 1 [mental]. Etoile rouge de boost.
# Hero Action: Shuffle this card into the encounter deck.
# When Revealed: The Lyja player removes 3 threat from among schemes in play.
# ★ Boost: The Lyja player removes 2 threat from a scheme.
#
# Cartes de reference :
#  - **`32187`** Surprise (« Remove 3 threat from among schemes ») :
#    `ChooseAbilities(ForChoiceAbility(...).SetTarget(Scheme2, has_threat=True))` puis
#    `RemoveThreatFromSchemes`. Surprise retire les 3 d'UNE manigance ; ici la
#    repartition est a volonte : repeat_rules="Threat" (une manigance peut etre
#    choisie autant de fois qu'elle porte de menace, selector_rule.py:105).
#  - **`event.py:79`** `Event.OnRemoveSchemeThreat` : meme remarque que sk041, le
#    retrait est fait par l'IDENTITE du proprietaire.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « 3 threat FROM AMONG schemes » : 3 au total, repartis ; s'il y a moins de 3
#    menaces en jeu, on retire tout ce qu'il y a.
#  - « schemes in play » : complot principal ET annexes.
#  - Boost « from A scheme » : une seule manigance, 2 menaces.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        lyja = ProprietaireLyja(this, effect)
        identite = lyja.GetIdentity()

        def a_retirer(eff: 'Effect') -> int:
            return min(3, sum(s.threat for s in Worlds.GetOnFieldSchemes(eff)))

        def retirer(cibles: Sequence['CardFace']) -> None:
            # Un choix = 1 menace ; les cibles se repetent selon la repartition voulue.
            for cible in cibles:
                identite.RemoveThreatFromSchemes([cible], 1, effect)

        lyja.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 3 threat from among schemes",
                retirer,
            ).SetTarget(Scheme2, has_threat=True, range=(a_retirer, 3), repeat_rules="Threat"),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        lyja = ProprietaireLyja(this, effect)
        identite = lyja.GetIdentity()
        lyja.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                lambda cibles: identite.RemoveThreatFromSchemes(cibles, 2, effect),
            ).SetTarget(Scheme2, has_threat=True),
        )

    return [
        MelangerDansLeDeckRencontre(),
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
