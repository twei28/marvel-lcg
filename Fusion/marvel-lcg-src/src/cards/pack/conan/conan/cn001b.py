from . import *

# * Conan — alter-ego de depart. CIMMERIA. THIEF. REC 3, 11 PV, main 6.
# Savage Vitality — Setup: Set King Conan aside. Put The Cimmerian upgrade
#   into play, TITLE side faceup.
# Action: Spend 1 resource of any type -> place 1 Crom counter on The
#   Cimmerian. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `AbilityFactory.SetupPutIntoPlay(["26002a,26002b"], flip_to_name=...)`
#    (26001b * Vision, officiel) : cree l'amelioration recto/verso et la met
#    en jeu au Setup, sur la face voulue.
#  - `.SetCost(Cost("1"))` = « spend 1 resource of any type » (04001b Clint
#    Barton, 53029 Harlem's Protector).
#  - « Set King Conan aside » : drapeau `hors_pile_identite` sur cn001d/e
#    (`MarquerHorsPile`, conan/__init__.py).
#
# TEXTE CONTRE CODE
#  « Action » (pas « Alter-Ego Action ») : l'alter-ego ne la porte que sur
#    cette face, donc elle n'existe qu'en alter-ego de toute facon.
#  « Limit once per round » : `LimitOncePerRound`, temoin d'epuisement exige.


def GetAbilities() -> Sequence['Ability']:

    def savage_vitality(effect: 'Effect', faces: List['CardFace']) -> None:
        Unused(faces)
        joueur = JoueurDe(effect)
        if joueur is not None:
            MarquerHorsPile(joueur, FACES_ROI)

    def poser_un_crom(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        PoserCrom(JoueurDe(effect), 1, effect)

    return [
        AbilityFactory.SetupPutIntoPlay(
            [f"{ID_CIMMERIAN_TITRE},{ID_CIMMERIAN_ROI}"],
            flip_to_trait="TITLE",
            operation=savage_vitality,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            poser_un_crom,
            conditions=[
                lambda effect, message:
                    JoueurDe(effect) is not None and
                    TrouverCimmerian(JoueurDe(effect), effect) is not None,  # type: ignore
            ],
        ).SetName("Savage Vitality")
        .SetCost(Cost("1"))
        .LimitOncePerRound(),
    ]
