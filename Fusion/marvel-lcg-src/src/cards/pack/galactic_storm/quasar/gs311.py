from . import *

# Quantum Energy — ressource signature (QUASAR 11/16 et 12/16, x2). [wild].
# Response: After you spend this card, ready Quantum Bands.
#
# Cartes de reference :
#  - **`sh001`** / factory `AfterYouSpendThisCard(type, op, to_pay_card=...)`
#    (factory/resources.py) : « After you spend this card » ; ici sans filtre
#    sur la carte payee.
#  - `gs300a` pour « ready Quantum Bands » (helper `RedresserLesBandes`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you SPEND this card » : la carte defaussee de la main pour sa
#    ressource ([wild] imprime : case verte a etoile, verifiee par decoupe),
#    pour n'importe quel paiement.
#  - « **Response** » (pas Hero Response) : utilisable dans les deux formes,
#    mais sans effet si les Bandes ne sont pas inclinees (condition).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)
        RedresserLesBandes(effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            redresser,
            conditions=[lambda effect, message: BandesInclinees(effect)],
        ),
    ]
