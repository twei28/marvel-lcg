from . import *

# * Leonardo « Leo » — ALLIE 3 [physical], 1*/2*, 3 PV, aspect Basic (TMNT Aspects). NINJA. TURTLE.
# [star] Response: After Leonardo uses a basic power, ready another [[NINJA]] ally you control.
#
# NOUVELLE. Cartes de reference : 04032 Captain Marvel (allie) « After Captain Marvel uses a basic power » =
# `AfterUnitUseBasicPower(Response, "This")` ; 33020 Utopia (redresser un personnage cible :
# `Faces.ReadyAll(effect.targets)`, `canbe_ready=True`). « another ... you control » : le filtre exclut
# Leonardo lui-meme et ne garde que les allies du joueur (modele `check_face_fn=... != effect.this`, 27010).
# [star] = icone etoile (fiche special.md) : zero code.
# TEXTE CONTRE CODE : « ANOTHER » (pas lui) ; « NINJA ALLY » (pas l'identite) ; « YOU CONTROL ».


def GetAbilities() -> Sequence['Ability']:

    def leonardo(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            leonardo
        ).SetTarget(Ally, trait="NINJA", canbe_ready=True, another=True,
                    check_fn=lambda effect, face: face.GetControlByPlayer() == effect.GetInitiator()),
    ]
