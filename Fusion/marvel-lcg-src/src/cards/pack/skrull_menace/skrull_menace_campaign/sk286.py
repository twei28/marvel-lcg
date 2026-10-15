from . import *

# Reverting Device — AMELIORATION de campagne (Justice / Campaign, n° 286). Cout 0. NON unique. ITEM. TECH.
# Play under any player's control.
# Each SKRULL minion engaged with you gets -1 SCH.
#
# Cartes de reference :
#  - **`cw/56013`** Aggressive Conditioning : « Play under any player's control » =
#    `CanPlayThisUpgradeCard("Players")`.
#  - **`environment_helper.py`** : « Each X gets -1 SCH » = `GiveKeywordToInPlayWhenApplyThis(CardFinder(...),
#    scheme=-1, get_new_value=fn, change_on_event=...)` ; `get_new_value` rend 1 pour les sbires du bon joueur,
#    0 sinon (la valeur est un multiplicateur de `scheme=-1`).
#  - **`next_evol/40181`** Tempo : « while engaged with you » (relation sbire <-> joueur engage).
#
# ⚠ Mots-pieges :
#  - « SKRULL MINION » : sbires seulement (ni le mechant, ni un sbire sans le trait) ;
#  - « engaged with YOU » : les sbires engages avec le PROPRIETAIRE de la carte (le joueur sous le controle
#    duquel elle est), pas avec un autre joueur ;
#  - « -1 SCH » : jamais sous 0 (un MNG negatif est ramene a 0 par le moteur) ; recalcule a l'engagement
#    et au desengagement (`AfterMinionEngagePlayer`).


def GetAbilities() -> Sequence['Ability']:

    def sbire_engage_avec_moi(effect: 'Effect', face: 'CardFace') -> int:
        joueur = effect.this.GetBindFace()
        if joueur is None:
            return 0
        joueur = joueur.GetControlByPlayer()
        return 1 if Minion.IsType(face) and face.GetEngagedPlayer() == joueur else 0

    changement_d_engagement = OnEvent.TemplateTrigger(
        Message.AfterMinionEngagePlayer,
        lambda effect, message: True,
    )

    return [
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion, trait="SKRULL"),
            scheme=-1,
            get_new_value=sbire_engage_avec_moi,
            change_on_event=changement_d_engagement,
        ),
    ]
