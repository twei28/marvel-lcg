from . import *

# Hero Appearance (x2) — EVENEMENT TREACHERY, cout 1 [physique]. Etoile rouge de boost.
# Hero Action: Shuffle this card into the encounter deck.
# When Revealed: The Lyja player deals 4 damage among enemies in play.
# ★ Boost: The Lyja player deals 3 damage to an enemy.
#
# Cartes de reference :
#  - **`16152`** Contingency Plan : « deal N damage among enemies » =
#    `ChooseAbilities(ForChoiceAbility(...).SetTarget(Enemy, range=(1, N), repeat_rules=...))`
#    puis `DealDamageTotal(cibles, N, effect)` (1 degat par choix ; un meme ennemi peut
#    etre choisi plusieurs fois).
#  - **`event.py:61`** `Event.OnDealDamage` : les degats d'un evenement sont ceux de
#    l'IDENTITE de `effect.GetInitiator()`. Ici l'initiateur est le joueur a qui la
#    carte est revelee, pas forcement Lyja : on frappe donc par l'identite du
#    PROPRIETAIRE (« the Lyja player », decision du 15/10/2026).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « 4 damage AMONG enemies » : 4 degats repartis a volonte (1 ennemi 4 fois, ou 2+2...),
#    PAS 4 degats a chacun ; « enemies in play » : vilain compris.
#  - Boost « 3 damage to AN enemy » : un seul ennemi, au choix de Lyja.
#  - « The Lyja player deals » : degats infliges par le joueur proprietaire.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        lyja = ProprietaireLyja(this, effect)
        identite = lyja.GetIdentity()
        lyja.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 4 damage among enemies",
                lambda cibles: identite.DealDamageTotal(cibles, 4, effect),
            ).SetTarget(Enemy, range=(4, 4), repeat_rules="Any"),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        lyja = ProprietaireLyja(this, effect)
        identite = lyja.GetIdentity()
        lyja.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage to an enemy",
                lambda cibles: identite.DealDamage(cibles, 3, effect),
            ).SetTarget(Enemy),
        )

    return [
        MelangerDansLeDeckRencontre(),
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
