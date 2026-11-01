from . import *

# * Mantis (face alter-ego) : OUTLAW. PSIONIC. REC 3*, main 6, PV 9.
# [star] Empathic Leveling — Response: After you use your REC, confuse a character you control.
#
# CARTES DE REFERENCE
#  - `bf025` Normal Again : `AfterUnitUseBasicPower(.., "You"|Identity, op, powers=[..])` pour « After you use a basic power » ; `Condition.CheckBasicPower` filtre le pouvoir (`powers=["REC"]`).
#  - `27110` Robotic Enhancements : `ChooseAbilities(effect, ForChoiceAbility(.., fn).SetTarget("YouControlUnit", canbe_confused=True))` + `Faces.GiveStatus(.., "Confused", effect)`.
#
# TEXTE CONTRE CODE
#  « After YOU use your REC » : le joueur de Mantis, son pouvoir de base de RECUPERATION (pas l'attaque ni la menee). « Response » nue : face alter-ego seulement (la capacite est portee par cette face).
#  « confuse A character YOU control » : au choix du joueur parmi SES personnages (identite ou allie, Mantis elle-meme comprise) ; un personnage Stoique ou deja confus n'est pas proposable. Pas de « may » : obligatoire.
#  Chiffres : REC 3* (l'etoile renvoie a cette capacite), main 6, PV 9.


def GetAbilities() -> Sequence['Ability']:

    def empathic_leveling(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Confuse a character you control",
                lambda cibles:
                    Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget("YouControlUnit", canbe_confused=True),
        )

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            empathic_leveling,
            powers=["REC"],
        ),
    ]
