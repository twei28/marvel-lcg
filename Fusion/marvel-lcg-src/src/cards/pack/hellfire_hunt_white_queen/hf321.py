from . import *

# Echoes of Enmity. Attachement ILLUSION PSIONIC, +1 SCH / +1 ATK (desc). « When Revealed : Search the encounter deck, discard pile, and set-aside area for
# your nemesis minion, then reveal that minion. Attach Echoes of Enmity to it. (Shuffle.) [star] Boost : Exhaust your identity. »
# Cartes de reference : 01190 Shadow of the Past (nemesis mis de cote : `SetupCards.Reveal(..., only_set_aside=True)`), Search.EncounterCard
# (`is_nemesis=joueur`, `include_set_aside=True`), `this.AttachTo2(face, effect)`.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, card_type=Minion, is_nemesis=joueur)
        if sbire is not None:
            sbire.Reveal(joueur, effect)
            this.AttachTo2(sbire, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.ExhaustAll([message.GetToPlayer().GetIdentity()], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
