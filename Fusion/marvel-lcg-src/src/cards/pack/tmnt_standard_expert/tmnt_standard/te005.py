from . import *

# Shadow of the Past (TMNT Standard 5/7) — TRAITRISE. 2 icones de boost.
# Texte IDENTIQUE au core 01190 : le script est celui de `01190`
# (`cards/pack/core/standard/01190.py`), recopie ici parce que la carte vit dans
# un autre pack et n'a pas d'`ability_link` (le texte imprime est le meme, mot
# pour mot : verifie sur le scan TMNT Standard 5/7).
#
# When Revealed: Reveal your set-aside nemesis minion and put it into play
#   engaged with you. Reveal your set-aside nemesis side scheme and put it into
#   play. Shuffle the rest of your set-aside nemesis encounter set into the
#   encounter deck. If your nemesis minion does not enter the game this way,
#   this card gains surge.


def GetAbilities() -> Sequence['Ability']:

    def shadow_of_the_past(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        faces = player.set_aside_nemesis_sets.Get()

        minions = Filter.ByType(faces, Minion, CardFinder(is_nemesis=player))
        faces = [x for x in faces if x not in minions]
        schemes = Filter.ByType(faces, SchemeSide2)
        faces = [x for x in faces if x not in schemes]

        entered = False

        def action():
            nonlocal entered
            entered = True

        for minion in minions:
            minion.Reveal(message.to_player, effect, if_entered_play=action)

        for scheme in schemes:
            scheme.Reveal(message.to_player, effect)

        rest_faces: List[CardFace] = [x for x in faces if x.card.area == player.set_aside_nemesis_sets]
        encounter_deck = Worlds.GetEncounterDeck(effect)
        Faces.ShuffleAllTo(rest_faces, encounter_deck, effect, ui_group=False)

        if not entered:
            this.GainSurge(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, shadow_of_the_past),
    ]
