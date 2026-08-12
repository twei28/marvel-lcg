from . import *

# Hallucination — custom « Rainy » (nemesis d'Agent 13 / Sharon Carter)
# When Revealed: Discard cards from the encounter deck until a minion is
#   discarded. Reveal that minion and attach this card to it. If you cannot,
#   this card gains surge.
# Forced Interrupt: When attached minion would take any amount of damage,
#   discard it and place 3 threat on the main scheme.
#
# Modele pour le When Revealed : Drafted (cw/the_initiative/56080.py) et
# Cruel Experiment (aoa/dark_beast/45124.py), qui font deja exactement
# `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` puis
# `minion.Reveal(player, effect)` + `this.AttachTo2(minion, effect)`
# (can_attach.py:49). `DiscardEncounterCardsUntil` -> `Deck.DiscardUntil`
# (game/deck/deck.py:431) parcourt UNE SEULE FOIS l'etat courant du deck
# (`self.Get()[::-1]`, un instantane) : si aucun sbire n'y figure, la boucle
# se termine d'elle-meme sur `found_face = None`, sans jamais repiocher la
# defausse. Pas de risque de boucle infinie -- exactement le cas « deck sans
# sbire » signale par le brief. Le repli suit l'idiome global
# `ThisCardGainSurge`.
#
# Modele pour l'interruption forcee : Jessica's Jacket (jessica_jones/
# jessica_jones/jj010.py) pour la forme du declencheur (« would take any
# amount of damage »), et Mysterio (spider_man_rainy/spider_man_rainy_
# nemesis/sr015.py) pour le remplacement complet des degats par un autre
# effet via `message.PreventDamage("All", effect)`
# (sender_damage.py:808, la classe `WhenUnitWouldTakeDamage`). La cible
# generique `"AttachedMinion"` (ability/condition/card_type.py) est deja
# utilisee comme cible de premiere classe par Biomechanical Upgrades
# (core/the_doomsday_chair/01185.py) sur une autre famille de message :
# `message.trigger` est alors directement le sbire attache.

def GetAbilities() -> Sequence['Ability']:

    def hallucination_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        player = message.GetToPlayer()

        minion = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=Minion,
        )
        if minion:
            minion.Reveal(player, effect)
            this.AttachTo2(minion, effect)
        else:
            ThisCardGainSurge(effect)

    def hallucination_interrupt(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        minion = message.trigger.CastTo(Minion)

        message.PreventDamage("All", effect)
        Faces.DiscardAll([minion], effect)
        this.PlaceThreatOnSchemes("MainScheme", 3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hallucination_revealed,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "AttachedMinion",
            hallucination_interrupt,
        ),
    ]
