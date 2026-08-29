from . import *

# Sudden Plan Change — BASIC, Team-Up (Stature and Iron Lad). Max 1 per deck.
# Hero Action: Change to another form. You get +1 hand size until the end
#   of the phase.
#
# TeamUp inapplicable tel quel : Stature n'est pas une identite heros
# separee dans ce moteur (c'est l'alliee signature il002, deja dans le deck
# d'Iron Lad). Tranche par l'utilisateur le 29/08/2026 : condition rendue
# comme "l'alliee Stature en jeu". "Change to another form" :
# `identity.ChangeToOtherForm(effect)` (game/card/face/base/identity.py).
#
# CORRECTIF (trouve par test_capacites.py) : `SetPlay(only_if_you_control_
# face=...)` cherche dans `GetInventoryDeck()` (les upgrades/objets
# equipes), PAS les allies en jeu -- la condition ne voyait donc jamais
# Stature. Remplace par un `conditions=[...]` sur `WhenInYourPlayTurn`
# testant `Worlds.FindCardsOnField(effect, name="Stature", card_type=Ally)`.
# Deuxieme correctif : `identity.ChangeToOtherForm(effect)` sert au choix
# PARMI PLUSIEURS faces (identites a 3+ faces, `AskChooseOneText` sur les
# noms de `back_faces`) -- pas au simple aller-retour Hero/AlterEgo, qui ne
# changeait donc rien ici. La bonne methode est
# `identity.ChangeToOtherIdentityForm(effect)` (game/card/face/card_type/
# identity.py), le vrai bascule binaire.

def GetAbilities() -> Sequence['Ability']:

    def stature_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return Worlds.FindCardsOnField(effect, name="Stature", card_type=Ally) != []

    def sudden_plan_change(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        identity.ChangeToOtherIdentityForm(effect)
        initiator.GetIdentity().GainUntilPhaseEnd(effect, hand_size=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sudden_plan_change,
            conditions=[stature_en_jeu],
        ).SetPlay(),
    ]
