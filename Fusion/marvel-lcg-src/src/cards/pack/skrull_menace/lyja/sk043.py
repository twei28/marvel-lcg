from . import *

# New York Bookstore — SOUTIEN, cout 1 [mental]. LOCATION.
# Laura Green gets +2 REC.
# Alter-Ego Response: After you make a basic recovery, draw 1 card.
#
# Cartes de reference :
#  - **`60016`** Sister Maggie : « Matt Murdock gets +3 REC » =
#    `GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Matt Murdock'), recover=3)` ;
#    un NOM propre ne designe que la face qui le porte (RECETTES §3).
#  - **`tg007`** Foreverglade : `AfterUnitMakeRecovery(AlterEgoResponse, "You", op,
#    is_basic_recovery=True)` + `CanPlayThisSupportCard()`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « LAURA GREEN gets +2 REC » : nom propre, donc l'alter ego SEULEMENT : en forme
#    heros (Lyja) aucun bonus (contre-cas dans l'autre forme exige, RECETTES §3).
#  - « ALTER-EGO Response » : AlterEgoResponse, pas Response.
#  - « after you make a BASIC recovery » : `is_basic_recovery=True`.


def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        effect.GetInitiator().DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Laura Green"), recover=2),
        AbilityFactory.AfterUnitMakeRecovery(
            AbilityType.AlterEgoResponse,
            "You",
            piocher,
            is_basic_recovery=True,
        ),
    ]
