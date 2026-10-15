from . import *

# Laser Tag — EVENEMENT BASIC, cout 2 [energie]. Aucun trait.
# Team-Up (Human Torch and Lyja). Max 1 per deck.
# Hero Action: Ready Human Torch, Lyja, and each SUPERPOWER upgrade you control.
#
# Cartes de reference :
#  - **`dz...`** Coolest Team-Up Ever! (dazzler/dz038) : un evenement Team-Up =
#    `.SetTarget("TeamUp")` en PREMIER selecteur (database.py:222) ; TeamUp et
#    MaxPerDeck sont lus dans `desc` (« Human Torch;Lyja », « 1 »).
#  - **`31001a`** / **`an001a`** : `Faces.ReadyAll(faces, effect)`.
#  - **`Worlds.FindCardsOnField`/`controller.GetControlCards2(CardFinder2(...))`** pour
#    « each SUPERPOWER upgrade you control ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Team-Up (Human Torch AND Lyja) » : les DEUX en jeu (Human Torch = allie, Lyja =
#    le heros) ; sinon l'evenement n'est pas jouable.
#  - « ready Human Torch, Lyja, AND EACH SUPERPOWER upgrade YOU CONTROL » : trois groupes,
#    les ameliorations SUPERPOWER du joueur seulement.
#  - « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def laser_tag(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        a_redresser: List['CardFace'] = []
        torche = [f for f in joueur.GetControlAllies() if f.IsName("Human Torch")]
        a_redresser += torche
        a_redresser.append(joueur.GetIdentity())
        a_redresser += [f for f in joueur.GetControlUpgrade() if f.HasTrait("SUPERPOWER")]
        Faces.ReadyAll(a_redresser, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            laser_tag,
        ).SetPlay()
        .SetTarget("TeamUp"),
    ]
