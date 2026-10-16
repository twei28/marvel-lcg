from . import *

# * Ninja He-Man « Prince Adam » — ALLIE 4 [physical], 2**/2*, 3 PV, aspect Basic (TMNT Aspects). NINJA. WARRIOR.
# Play only if you control a [[NINJA]] or [[WARRIOR]] card.
# Toughness.
# Response: After Ninja He-Man enters play, cloak him.
#
# NOUVELLE. Cartes de reference :
#  - « Play only if you control a <trait> card » : 27048 Ghost-Spider, `CanPlayThisAllyCard().SetPlay(...)`.
#    Deux traits (OU) : helper `JouableSiVousControlez` (__init__.py du pack) ; ⚠ PAS
#    `only_if_you_control_face`, qui lit l'inventaire (attachements) de l'identite et refusait la carte.
#  - Toughness : `desc.Toughness`, lu par le moteur (fiche toughness.md) : zero code.
#  - « cloak him » : fiche mots-cles/cloak.md, `Faces.GiveStatus([lui], "Cloaked")` ; declencheur
#    `AfterCardEnterPlay(Response, "This")` (45048).
# TEXTE CONTRE CODE : « a NINJA or WARRIOR CARD » (toute carte controlee : identite, allie, soutien,
#   amelioration) ; « cloak HIM » (lui-meme).


def GetAbilities() -> Sequence['Ability']:

    def ninja_he_man(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Cloaked", effect)

    return [
        JouableSiVousControlez(AbilityFactory.CanPlayThisAllyCard().SetPlay(), ["NINJA", "WARRIOR"]),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            ninja_he_man
        ),
    ]
