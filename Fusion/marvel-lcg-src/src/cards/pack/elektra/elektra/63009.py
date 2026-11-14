from . import *

# Sai Strike — EVENEMENT, cout 1, [physical]. ATTACK. x2 (Elektra 8-9/15).
# Hero Action (attack): Deal 3 damage to an enemy. For each Elektra's Sai you control, shuffle the top card of the NINJA deck
# into the encounter deck.
#
# CARTES DE REFERENCE
#  - « Deal N damage to an enemy » (evenement d'attaque) : `16005` Root Stomp (`this.DealDamage(effect.targets, n, effect)`).
#  - compter des cartes nommees que l'on controle : `Worlds.FindCardsOnField(effect, CardFinder(...))` filtre par
#    `GetControlByPlayer()` (meme lecture que `DiscountAbility` de fne : `face.GetControlBy() == player`).
#
# TEXTE CONTRE CODE
#  ⚠ « For each Elektra's Sai YOU CONTROL » : seulement les Sai du joueur (pas ceux d'un autre joueur), ATTACHES ou non : la carte est
#    une amelioration, elle est comptee des qu'elle est en jeu sous son controle. Zero Sai = aucun melange.
#  ⚠ L'ordre imprime : les degats d'abord, puis les melanges (un melange par Sai, une carte du dessus a chaque fois).
#  Chiffres : cout 1, 3 degats fixes.


def GetAbilities() -> Sequence['Ability']:

    def sai_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.DealDamage(effect.targets, 3, effect)
        sai = [f for f in Worlds.FindCardsOnField(effect, CardFinder(name=NOM_SAI))
               if f is not None and f.GetControlBy() == joueur]
        for _ in sai:
            if not MelangerDessusNinja(joueur, effect):
                break

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sai_strike,
        ).SetPlay().SetLabel('attack').SetTarget(Enemy),
    ]
