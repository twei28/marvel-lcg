from . import *

# Biopathy (x2) : RESSOURCE [wild]. Hero Class.
# Response: After you spend this card, heal 1 damage from a friendly character. You may confuse a character you control to draw 1 card.
#
# CARTES DE REFERENCE
#  - `tm007` Optimism / `29009` Stroke of Genius : `AfterYouSpendThisCard(AbilityType.Response, op)` (la fabrique filtre « THIS card »), soin par `HealthUnits`, pioche par `DrawUp`.
#  - `27110` Robotic Enhancements : `SetTarget("YouControlUnit", canbe_confused=True)` + `Faces.GiveStatus(cibles, "Confused", effect)`.
#
# TEXTE CONTRE CODE
#  « Response » (PAS « Hero Response ») : jouable aussi en alter-ego. « heal 1 damage from A FRIENDLY character » : au choix, ami de n'importe quel joueur. « You MAY confuse a character
#    YOU control TO draw 1 card » : facultatif ; FAQ imprimee (« to ») : la carte n'est piochee que si le statut a ete REELLEMENT pose (un personnage deja confus ou Stoique ne compte pas).
#  Chiffres : 1 soin, 1 carte. La ressource [wild] vient de `desc.RES = G`.


def GetAbilities() -> Sequence['Ability']:

    def biopathy(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        SoignerUnAmi(effect, joueur, this, 1)

        def confondre_et_piocher(cibles: Sequence['CardFace']) -> None:
            if Faces.GiveStatus(cibles, "Confused", effect) > 0:
                joueur.DrawUp(1, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Confuse a character you control to draw 1 card",
                confondre_et_piocher,
            ).SetTarget("YouControlUnit", canbe_confused=True),
        )

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            biopathy,
        ),
    ]
