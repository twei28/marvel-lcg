from . import *

# * Emma Frost : allie RECRUITED, cout 4, PV 3, THW 2*, ATK 1*. Armored 1.
# « Armored X » : mot-cle MAISON (fiche docs/reference/mots-cles/armored.md, glossaire MC4DB) : « when a character with this keyword would take
# any amount of damage FROM AN ATTACK, prevent X of that damage ». Carte de reference : si016 / 01098 (`WhenUnitWouldTakeDamage(...,
# is_from_attack=True)` + `message.PreventDamage`). Pas de cle `desc.Armored` : elle fait planter la lecture de la carte.
# Response: After Emma Frost defends against an attack, discard 1 card from your deck, you may play it if it is an event, ignoring its
# resource cost.
#
# Cartes de reference : 15003 Chaos Magic (`initiator.PlayCardsLikeInTurn(faces, effect, ignore_resources_cost=True)`), hf013 (defense).
# ⚠ « discard 1 card from YOUR deck » : le deck du joueur qui controle Emma ; « you MAY play it » : facultatif ; seulement un EVENEMENT.
def GetAbilities() -> Sequence['Ability']:
    def emma(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        face = joueur.player_deck.GetTop()
        if face is None:
            return
        Faces.DiscardAll([face], effect)
        if Event.IsType(face):
            joueur.PlayCardsLikeInTurn([face], effect, ignore_resources_cost=True)

    def armored_1(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            armored_1,
            is_from_attack=True,
        ),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.Response,
            "This",
            emma,
        ),
    ]
