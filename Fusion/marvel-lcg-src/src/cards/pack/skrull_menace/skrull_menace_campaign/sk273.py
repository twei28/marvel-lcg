from . import *

# * Newbie Training — COMPLOT ANNEXE DE JOUEUR (Aggression / Campaign, n° 273). Cout 0, menace de depart 3.
# Victory 0.
# When Defeated: The player who defeated this scheme may defeat a non-ELITE SKRULL minion and draw 1 card.
#
# Cartes de reference :
#  - **`hd011`** : squelette « Victory 0 » + `WhenSchemeBeDefeated(WhenDefeated, "This", op,
#    has_defeating_player=True)` + `MayChooseOneAbility`.
#  - **`dz009`** : « defeat a non-ELITE minion » = `SetTarget(Minion, non_trait="ELITE")` puis
#    `Faces.DefeatUnits(cibles, this, effect)`.
#
# ⚠ Mots-pieges :
#  - « a non-ELITE SKRULL minion » : un sbire SKRULL ET non Elite, engage avec N'IMPORTE QUEL joueur
#    (le texte ne dit pas « engaged with you ») ;
#  - « defeat ... AND draw 1 card » : un seul bloc facultatif ; la carte est piochee par le vainqueur du
#    complot ; sans cible legale, le bloc n'est pas offert (voir defs/campagne_cartes_questions.md, Q3) ;
#  - « defeat » = vaincre (« When Defeated » du sbire, Victory...), pas defausser.


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        vainqueur = message.GetDefeatingPlayer()
        if vainqueur is None:
            return

        def vaincre_et_piocher(cibles: Sequence['CardFace']) -> None:
            Faces.DefeatUnits(list(cibles), this, effect)
            vainqueur.DrawUp(1, effect)

        vainqueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Defeat a non-ELITE SKRULL minion and draw 1 card",
                vaincre_et_piocher,
            ).SetTarget(Minion, trait="SKRULL", non_trait="ELITE"),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            recompense,
            has_defeating_player=True,
        ),
    ]
