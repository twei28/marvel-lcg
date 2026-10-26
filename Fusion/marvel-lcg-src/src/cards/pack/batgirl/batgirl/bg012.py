from . import *

# Utility Belt — amelioration, cout 3, [mental]. « Hero Action: When you would play an event, exhaust this card → reduce the cost of that
# event by 1. Hero Interrupt: When the hero phase ends, if this card is ready, Batgirl gets +1 hand size. »
# Cartes de reference : `us009` Solid Gear (`Worlds.UpdateNextCardPlayCost`, cout d'inclinaison), `14022`/`hz003` (Hero Action d'amelioration),
# `01029a` Iron Man / `04054` (`hand_size`).
# ⚠ Lecture du texte IMPRIME (le FAQ de l'insert decrit une ancienne version). CORRIGE le 26/10/2026 (verdict RR « Action » / « Triggered
# Abilities ») : la 1re capacite est une ACTION de heros, donc FACULTATIVE et seulement en forme heros ; le joueur peut la refuser pour garder la
# ceinture PRETE (le +1 de main de la 2e capacite). Avant : reduction automatique + inclinaison forcee a chaque evenement, dans toutes les formes.
# Pourquoi une Action qui arme « le prochain evenement » : `WhenPlayerWouldPlayCard` part APRES le paiement des ressources (impossible d'y
# reduire le cout) ; la reduction doit etre posee avant le calcul du cout, comme Solid Gear le fait (`UpdateNextCardPlayCost`).


def GetAbilities() -> Sequence['Ability']:

    def prete(effect: 'Effect', message) -> bool:
        return not effect.this.IsExhaust()

    def reduire_le_prochain_evenement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « reduce the cost of that event by 1 » : l'evenement que le joueur joue ensuite pendant son tour (valeur NEGATIVE, jamais sous 0).
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(joueur, -1, effect, finder=CardFinder(card_type=Event), in_this="Turn")

    def ceinture_main(effect: 'Effect', message: 'Message.WhenPlayerEndPhase') -> None:
        # « When the hero phase ends, if this card is ready, Batgirl gets +1 hand size » : +1 juste avant la pioche de fin de phase,
        # retire apres (le calcul continu ne relit pas l'etat « prete » : vu avec GiveKeywordToAttached / ...ApplyThis).
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        identite.GainHandSize(1, effect)

        def retirer(effect2: 'Effect', message2: 'Message.AfterPhaseEnd') -> None:
            identite.GainHandSize(-1, effect2)
        identite.effect.RegisterTemp(
            AbilityFactory.AfterPhaseEnd(AbilityType.Temp2, "Player", retirer),
            unregister_after_exec=True,
            until_round_end=True,
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reduire_le_prochain_evenement,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenPlayerEndPhase(AbilityType.HeroInterrupt, ceinture_main, conditions=[prete]),
    ]
