from . import *

# Illusory Attacks (TREACHERY ILLUSION PSIONIC, x2 : hf374, hf375). Boost 1 + etoile. « When Revealed : You are confused. Deal 1 damage to each
# confused character in play. [star] Boost : You are confused. »
# Cartes de reference : mt011 Psychic Tremor (`IsConfused` sur personnages amis et ennemis), hf124 (boost : `GiveStatus ... "Confused"`).
# ⚠ « each confused character in play » : alliés, identites de TOUS les joueurs ET ennemis (vilain, sbires) ; « You are confused » AVANT les degats :
# l'identite fraichement desorientee en prend 1.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)
        confus = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f.IsConfused()]
        confus += [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsConfused()]
        for face in confus:
            if face.IsInPlay():
                face.TakeDamage(this, 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
