from . import *

# Trample

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        joueur.DiscardHandCards((1, 1), effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilains = VilainsEnJeu(effect)
        if not vilains:
            return
        v = vilains[0] if len(vilains) == 1 else joueur.AskChooseFace(
            vilains, effect, prompt="Choose a villain")
        amis = Worlds.GetOnFieldFriendlyCharacters(effect)
        if v is None or not amis:
            return
        # « the friendly character with the fewest remaining hit points » : entre
        # ex aequo, le joueur choisit.
        mini = min(a.health for a in amis)
        egaux = [a for a in amis if a.health == mini]
        cible = egaux[0] if len(egaux) == 1 else joueur.AskChooseFace(
            egaux, effect, prompt="Choose the character with the fewest remaining hit points")
        if cible is not None:
            v.BasicAttack([cible], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an ally you control",
                lambda targets: this.DealDamage(targets, 1, effect)
            ).SetTarget(Ally, check_fn=lambda e, f: f.GetControlByPlayer() == joueur),
        )

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
