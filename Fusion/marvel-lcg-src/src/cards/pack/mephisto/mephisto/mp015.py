from . import *

# * Unquenchable Envy — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte`.
# « Each resource you generate is considered a wild resource instead of its current resource. »
#
# Cartes de reference : batgirl/bg006 (`CheckEffectGeneratedResources` + `message.SetResources(Resources("G") * res.val, effect)`),
# batgirl/__init__ `VersWild`, ah001a Hypermind.
# ⚠ Mots-pieges : « EACH resource YOU generate » : seulement celles du porteur (`GetToPlayer`), toutes, sans limite de tour (capacite constante,
# pas la conversion temporaire de Nightwing) ; « INSTEAD of its current resource » : la quantite reste, seule la couleur change.


def GetAbilities() -> Sequence['Ability']:
    def pour_le_porteur(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> bool:
        porteur = effect.this.CastTo(Attachment).GetBindFace()
        return porteur is not None and message.GetToPlayer() == porteur.GetControlByPlayer()

    def en_wild(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> None:
        res = message.res
        if res.val > 0:
            message.SetResources(Resources("G") * res.val, effect)

    return [
        *AbilitesDuPacte(),
        Ability(AbilityType.NonKeyword, Message.CheckEffectGeneratedResources, [pour_le_porteur], en_wild),
    ]
