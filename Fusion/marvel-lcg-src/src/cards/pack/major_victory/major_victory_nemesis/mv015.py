from . import *

# Judgment of Korvac — TRAHISON nemesis. Boost 1 + [star].
# When Revealed: Take 3 indirect damage or place 2 threat on Korvac's Future and this card gains surge.
# [star] Boost: Choose to place 2 threat on Korvac's Future or this card gets +2 boost icons.
#
# CARTES DE REFERENCE
#  - `mw013` Spider-Woman : `player.ChooseAbilities(effect, ForChoiceAbility(..), ForChoiceAbility(..))` pour « choose to
#    either A or B » ; `identite.TakeIndirectDamage(this, n, effect)` pour les degats indirects.
#  - `mf017` : `ThisCardGainSurge(effect)`. `sk113` : `message.GainBoostIcon(n, effect)` pour « gets +N boost icons ».
#
# ARBITRAGE UTILISATEUR (30/10/2026) : le « gains surge » ne s'applique QU'AU CHOIX « menace » (pas aux degats indirects).
#
# TEXTE CONTRE CODE
#  « or » -> le joueur CHOISIT. Si Korvac's Future n'est pas en jeu (elle commence mise de cote), « place 2 threat on it »
#    est impossible : seule la branche degats est proposee (regle « si on ne peut pas, on choisit l'autre »).
#  « and this card gains surge » -> dans la branche menace seulement (arbitrage ci-dessus).
#  Boost : le joueur est le DEFENSEUR (`message.against_player`, repli : premier joueur). Chiffres : 3 degats, 2 menaces, +2 icones.


def GetAbilities() -> Sequence['Ability']:

    def judgment_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        future = FutureEnJeu(effect)

        def subir(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 3, effect)

        def poser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            cible = FutureEnJeu(effect)
            if cible is not None:
                this.PlaceThreatOnSchemes([cible], 2, effect)
            ThisCardGainSurge(effect)

        if future is None:
            subir([])
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Take 3 indirect damage", subir),
            AbilityFactory.ForChoiceAbility("Place 2 threat on Korvac's Future (this card gains surge)", poser),
        )

    def judgment_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.against_player or Worlds.GetFirstPlayer(effect)
        future = FutureEnJeu(effect)

        def menace(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            cible = FutureEnJeu(effect)
            if cible is not None:
                this.PlaceThreatOnSchemes([cible], 2, effect)

        def icones(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            message.GainBoostIcon(2, effect)

        if joueur is None:
            icones([])
            return
        if future is None:
            icones([])
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 2 threat on Korvac's Future", menace),
            AbilityFactory.ForChoiceAbility("This card gets +2 boost icons", icones),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            judgment_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            judgment_boost,
        ),
    ]
