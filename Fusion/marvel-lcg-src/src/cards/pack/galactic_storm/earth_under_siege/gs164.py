from . import *

# Observe the Perimeter — OBLIGATION (Earth Under Siege).
# You cannot attack.
# Alter-Ego Action: Exhaust your identity → look at the top card of the villain deck and discard this card.
# [star] Boost: After this activation, shuffle this card into the encounter deck.
#
# Cartes de reference :
#  - « You cannot attack » (non qualifie, tout ennemi) : `AbilityFactory.PlayersCannotAttackWhile("You",
#    Enemy)` (modele tl013 Brainwashed Betrayal, qui restreint « the villain » seulement — ici `Enemy`
#    generique, texte sans qualificatif).
#  - « Exhaust your identity -> look at the top card of the villain deck and discard this card » :
#    `AbilityFactory.PlayerActionToDiscardThis(AlterEgoAction, ex_operation=...)` (modele gs083 Optic Blast
#    Cannon) ; « look at » : `Player.LookAtDeck` (modele lj020 Redwing), deck = le deck de mechants
#    (`Villains._VillainDeck`, brique du 20/10/2026 — PAS `Scenario.villain_deck`, jamais utilise sur ce
#    scenario, voir earth_under_siege/gs161a.py).
#  - « [star] Boost: After this activation, shuffle this card into the encounter deck » : `WhenCardBecomeBoost`
#    + `RunAt.AfterEnemyActivationEnd` (modele sk196) + `Faces.ShuffleAllTo([this], "EncounterDeck", effect)`.
#
# ⚠ Mots-pieges : « You cannot attack » vise le joueur qui PORTE l'obligation (« You »), pas tous les
# joueurs ; « the villain deck » = le deck de MECHANTS multiples de ce scenario (6 cartes melangees), pas
# le deck de stades normal (toujours vide ici) ; « look at » ne retire ni ne revele la carte publiquement,
# seul le joueur la voit (`Faces.LookAt`, prive).


def GetAbilities() -> Sequence['Ability']:

    def regarder_le_dessus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        deck = Villains._VillainDeck(effect)
        joueur.LookAtDeck(deck, 1, effect)

    def recycler_au_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        RunAt.AfterEnemyActivationEnd(
            effect, message.would_message,
            lambda: Faces.ShuffleAllTo([this], "EncounterDeck", effect),
        )

    return [
        AbilityFactory.PlayersCannotAttackWhile("You", CardFinder(card_type=Enemy)),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
            ex_operation=regarder_le_dessus,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
        AbilityFactory.WhenCardBecomeBoost("This", recycler_au_boost),
    ]
