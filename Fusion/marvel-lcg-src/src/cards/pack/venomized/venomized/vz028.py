from . import *

# * Alchemax — SOUTIEN, cout 2, RES [energy]. LOCATION.
# Alter-Ego Action: Exhaust Alchemax -> add the topmost aspect card from your
#   discard pile to your hand.
#
# CARTE DE REFERENCE
#  - `01034` * Stark Tower : « Alter-Ego Action: Exhaust Stark Tower -> ...
#    returns the TOPMOST [[Tech]] upgrade in their discard pile to their
#    hand. » Meme montage : `discard_pile.FindTopmost(<filtre>)` puis
#    `Faces.ReturnToHand`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR discard pile », pas « a player's » : `01034` fait choisir un
#    joueur et vise sa defausse ; ici la defausse est celle du joueur actif,
#    donc aucune cible a choisir et pas de `SetTarget`.
#  ⚠ « an ASPECT card » : la classe `"Aspect"` existe dans `CARD_CLASS` et
#    designe exactement « carte non-heros non-basique » (voir `04033`
#    Finesse, qui genere une ressource « for an aspect card »). Ce n'est PAS
#    `card_class="Venomized"` — Alchemax remonte n'importe quel aspect.
#  ⚠ « add ... to your hand » depuis la DEFAUSSE : `Faces.ReturnToHand`, le
#    meme verbe que `01034`.
def GetAbilities() -> Sequence['Ability']:

    def alchemax(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        trouvee = joueur.discard_pile.FindTopmost(CardFinder(card_class="Aspect"))
        if trouvee:
            Faces.ReturnToHand([trouvee], joueur, effect)

    def une_carte_aspect_en_defausse(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        return joueur.discard_pile.FindTopmost(CardFinder(card_class="Aspect")) is not None

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            alchemax,
            conditions=[une_carte_aspect_en_defausse],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
