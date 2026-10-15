from . import *

# Laser Tag — EVENEMENT BASIC, cout 2 [energie]. Aucun trait.
# Team-Up (Human Torch and Lyja). Max 1 per deck.
# Hero Action: Ready Human Torch, Lyja, and each SUPERPOWER upgrade you control.
#
# Cartes de reference :
#  - **`dz038`** Love from Beyond the Stars / **`dz037`** (dazzler) : un evenement Team-Up =
#    `.SetTarget("TeamUp")` en PREMIER selecteur (database.py:222) ; TeamUp et
#    MaxPerDeck sont lus dans `desc` (« Human Torch;Lyja », « 1 »).
#  - **`31009`** / **`an001a`** : `Faces.ReadyAll(faces, effect)`.
#  - **`joueur.GetControlAllies()` / `GetControlUpgrade()`** (modele **`taskmaster 08026`**,
#    `GetControlUpgrade`) pour « each SUPERPOWER upgrade you control ».
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
