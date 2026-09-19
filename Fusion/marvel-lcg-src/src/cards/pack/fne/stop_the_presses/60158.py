from . import *

# Breaking News
# When Revealed: Choose: • Exhaust a DAILY BUGLE support (under any player's
#   control) and remove 1 stamina counter from it. • Place 2 threat on the
#   main scheme.
# [star] Boost: Exhaust a DAILY BUGLE support (under any player's control).

def ChoisirUnSoutien(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    soutiens = SoutiensDailyBugle(effect)
    if not soutiens:
        return None
    return soutiens[0] if len(soutiens) == 1 else joueur.AskChooseFace(soutiens, effect)


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def epuiser(targets: Sequence['CardFace']) -> None:
            cible = ChoisirUnSoutien(effect, joueur)
            if cible is not None:
                Faces.ExhaustAll([cible], effect)
                RetirerUneEndurance(cible, effect)

        # ⚠ ForChoiceAbility n'a pas de `conditions` : booleen a la construction.
        existe = bool(SoutiensDailyBugle(effect))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust a Daily Bugle support and remove 1 stamina counter from it", epuiser, condition=existe),
            AbilityFactory.ForChoiceAbility("Place 2 threat on the main scheme", lambda targets: this.PlaceThreatOnSchemes("MainScheme", 2, effect)),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        cible = ChoisirUnSoutien(effect, message.GetToPlayer())
        if cible is not None:
            Faces.ExhaustAll([cible], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
