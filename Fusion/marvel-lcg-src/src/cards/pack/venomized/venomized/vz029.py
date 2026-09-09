from . import *

# * Doctor Steven — SOUTIEN, cout 1, RES [mental]. PERSONA.
# Alter-Ego Action: Exhaust Doctor Steven -> reduce the cost of the next
#   Venomized (black) or SYMBIOTE card played this phase by 1.
#
# CARTE DE REFERENCE
#  - `05008` * Nakia Bahadir (pack msm) : « Alter-Ego Action: Exhaust ->
#    reduce the cost of the next card you play this phase by 1. » Meme
#    montage, `Worlds.UpdateNextCardPlayCost(..., in_this="Phase")` ; elle ne
#    filtre rien, celle-ci filtre.
#
# TEXTE CONTRE CODE
#  ⚠ « Venomized (black) OR SYMBIOTE » : un OU entre une CLASSE et un TRAIT.
#    `CardFinder` combine ses champs en ET — `card_class=...` plus
#    `trait=...` exigerait les deux. On passe donc par `check_face_fn`, le
#    point d'entree prevu pour un predicat maison (`finder.py`).
#  ⚠ « the NEXT card played this phase » : `in_this="Phase"`, pas "Turn". En
#    multijoueur la phase couvre les tours de tout le monde, et le texte ne
#    dit pas « that you play ».
def GetAbilities() -> Sequence['Ability']:

    def venomized_ou_symbiote(face: 'CardFace') -> bool:
        return EstUneCarteVenomized(face) or PorteLeTraitSymbiote(face)

    def doctor_steven(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        Worlds.UpdateNextCardPlayCost(
            effect.GetInitiator(),
            -1,
            effect,
            finder=CardFinder(check_face_fn=venomized_ou_symbiote),
            in_this="Phase",
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            doctor_steven
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
