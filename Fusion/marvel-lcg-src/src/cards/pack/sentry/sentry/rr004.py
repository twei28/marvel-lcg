from . import *

# * Cornelius Worth : SOUTIEN, cout 1, [mental]. PERSONA. THERAPIST.
# Action: Exhaust this card → choose: • Generate a [mental] resource. • Remove 1 balance counter from Duality Aspect.
#
# CARTES DE REFERENCE
#  - « Exhaust this card → » : `CostFunc.Exhaust("This")` (ca003, mf005).
#  - « Generate a [mental] resource » : `CanGenerateResources(AbilityType.Resource, Resources("B"))` + `CostFunc.Exhaust("This")` (modele `im005` Stark Tower, `ca009`).
#  - « remove 1 balance counter from Duality Aspect » : `Faces.RemoveCountersOn([dualite], 1, 'balance', effect)`.
#
# TEXTE CONTRE CODE
#  « choose » : le moteur n'a pas d'« Action qui genere une ressource dans la reserve » : une ressource n'existe qu'AU PAIEMENT. Les deux options deviennent DEUX capacites qui partagent le
#  meme cout (epuiser la carte) : une `Resource` (generer [mental]) et une `Action` (retirer 1 compteur) ; elles s'excluent donc l'une l'autre, comme le « choose ». Lecture notee au compte rendu.
#  « from DUALITY ASPECT » : seulement cette carte (pas The Watchtower). Sans compteur sur Duality Aspect, l'Action est sans effet.
#  Chiffres : cout 1.


def GetAbilities() -> Sequence['Ability']:

    def retirer_un(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        dualite = Dualite(effect)
        if dualite is not None and dualite.CastTo(CanPlaceCounter).GetCounters(NOM_EQUILIBRE) > 0:
            Faces.RemoveCountersOn([dualite], 1, NOM_EQUILIBRE, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            retirer_un,
        ).SetName("Therapy").SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
