from . import *

# Chilly McHotpants Minion — GABARIT technique : la forme SBIRE de sk268 (voir sk268.py).
# [star] Response: After "Chilly McHotpants" attacks you, draw 1 cards. If you take no damage from that
#   attack, draw 1 card.
#
# Cartes de reference :
#  - **`sk150`** Ice Control : « After X attacks you » = `AfterUnitAttackYou(type, "This"|"AttachedEnemy", op)` ;
#    le message `AfterUnitAttackEnd` porte `damaged_targets` (les unites qui ont VRAIMENT encaisse des degats :
#    une carte Tough absorbee n'y figure pas).
#
# ⚠ Mots-pieges : « attacks YOU » (le joueur engage avec le sbire) ; « If YOU take no damage » : l'IDENTITE du
# joueur n'a pas encaisse de degats (un allie qui defend et encaisse, un statut Tough, une DEF suffisante
# donnent la seconde carte) ; « draw 1 CARDS » : faute imprimee (« draw 1 cards »), lue « 1 carte ».


def GetAbilities() -> Sequence['Ability']:

    def pioche(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)
        if joueur.GetIdentity() not in message.damaged_targets:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.Response,
            "This",
            pioche,
        ),
    ]
