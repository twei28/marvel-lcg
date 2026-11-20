from . import *

# * Lusting Existence — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte`.
# « Action : Exhaust an identity-specific card you control -> ready your identity. »
#
# Cartes de reference : sm/osborn_tech/27152 (`WhenInYourPlayTurn(Action, ..).SetCostFunc(CostFunc.Exhaust(..))`), sk069 (identity-specific =
# `desc.Class == "Hero"`, decision de l'auteur), mister_fantastic/mf013 (`Select.From(CardFinder(..))`).
# ⚠ Mots-pieges : « identity-SPECIFIC » (carte signature, pas une carte d'aspect) ; « you CONTROL » (en jeu, a toi) ; « Action » nue : les
# deux formes, alter-ego comme heros ; le cout est l'inclinaison d'UNE carte, pas de l'identite.


def GetAbilities() -> Sequence['Ability']:
    def specifique(face: 'CardFace') -> bool:
        return (getattr(face.paper, "desc", None) or {}).get("Class") == "Hero"

    def redresse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        *AbilitesDuPacte(),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, redresse)
        .SetCostFunc(CostFunc.Exhaust(Select.From("YouControlCards", finder=CardFinder(check_face_fn=specifique)))),
    ]
