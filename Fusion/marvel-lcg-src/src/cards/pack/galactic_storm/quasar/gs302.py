from . import *

# * Epoch — allie signature (QUASAR 2/16). COSMIC ENTITY. Cout 4, [wild].
# CTR 1 (1 degat consecutif), ATQ 3 (3 degats consecutifs), 4 PV.
# ★ Response: After Epoch uses one of her basic powers, ready Quantum Bands.
#
# Cartes de reference :
#  - **`14001a`** / `04032` / `tt001a` : « After you use a basic power » =
#    `AfterUnitUseBasicPower(type, "This", op, powers=[...])` (RECETTES §1) ;
#    ici l'allie lui-meme (`"This"`).
#  - `gs300a` pour « ready Quantum Bands » (helper `RedresserLesBandes`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « one of HER basic powers » : un allie n'a que deux pouvoirs de base,
#    ATTAQUER et CONTRER (pas de DEF : un allie qui defend n'utilise pas de
#    pouvoir de base) -> `powers=["ATK", "THW"]`.
#  - « ★ » devant « Response » et a cote de CTR/ATQ : renvoi au texte
#    (convention de l'auteur, validee pour Skrull Menace), pas un mot-cle.
#    Les etoiles CREUSES sous les chiffres sont les degats consecutifs
#    (1 sous CTR, 3 sous ATQ) : `desc` « 1* » et « 3*** ».
#  - « **Response** » : facultative, aucune limite imprimee.
#  - « ready Quantum Bands » : sans effet si elles sont deja pretes ou
#    absentes (condition, comme gs300a).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        RedresserLesBandes(effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            redresser,
            powers=["ATK", "THW"],
            conditions=[lambda effect, message: BandesInclinees(effect)],
        ),
    ]
