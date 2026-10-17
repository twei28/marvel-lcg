from . import *

# * Sōhei (Leo) — ALLIE double aspect Justice/Protection (Inkwire, TMNT Aspects).
# Cout 4, PV 2, THW 1 / ATK 1 (1 degat consecutif chacun), ressource [mental].
#
# Toughness.
# Interrupt: When Sōhei is defeated by consequential damage ([consequential]), your hero gets +2
#   hand size until the end of the round.
#
# Cartes de reference :
#  - Toughness : lu par le moteur dans `desc.Toughness` (fiche mots-cles/toughness.md), aucun code ;
#  - « defeated by consequential damage » : 30021 SP//dr (`WhenUnitBeDefeated(...,
#    by_consequential=True)`) ;
#  - « gets +N hand size until the end of the ... » : 12033 Assess the Situation / wd122
#    (`GetIdentity().GainUntilPhaseEnd(effect, hand_size=N)`) ; ici « until the end of the ROUND » :
#    `GainUntilRoundEnd(effect, hand_size=2)` (meme parametre, `face_action.py`).
#
# Q-UD4 TRANCHEE (17/10/2026) : « your hero gets +2 hand size » vaut AUSSI quand le joueur est en
#   ALTER EGO : l'identite du joueur, quelle que soit sa forme, gagne +2 de taille de main.
#
# Mots-pieges : « defeated » (pas « damaged ») ; « by consequential damage » ; « YOUR hero » (le
# joueur qui controle Sōhei) ; « until the end of the ROUND » (pas de la phase : le bonus vaut
# encore a la pioche de fin de phase joueur).


def GetAbilities() -> Sequence['Ability']:

    def main_elargie(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.GetIdentity().GainUntilRoundEnd(effect, hand_size=2)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            main_elargie,
            by_consequential=True,
        ),
    ]
