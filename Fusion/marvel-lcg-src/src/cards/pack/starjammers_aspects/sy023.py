from . import *
# Energy Cannon (Aggression, amelioration 1 [energy]). TECH. WEAPON. Restricted.
# Action: Exhaust Energy Cannon → place 1 charge counter on it.
# Hero Action: Discard Energy Cannon → deal X damage divided among enemies as you choose, where X is equal to the number of charge counters
# on Energy Cannon.
#
# Cartes de reference : 48032 Gunboat Diplomacy (repartition LIBRE entre ennemis : `ForChoiceAbility(..).SetTarget(Enemy, range=(0, X),
# repeat_rules="Health")` + `this.DealDamage(targets, 1, effect)`) ; rl008 / us007 (compteurs `charge` : `Faces.PlaceCountersOn`) ;
# fiche restricted.md (`desc.Restricted`, base automatique).
# ⚠ « Discard Energy Cannon → deal X » : X se lit AVANT la defausse (la carte perd ses compteurs en quittant le jeu) ; la defausse est donc
# faite apres la lecture, dans l'operation. Un compteur unique « all-purpose » n'est pas en jeu ici : le compteur est `charge`.
def GetAbilities() -> Sequence['Ability']:
    def charger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, 'charge', effect)
    def tirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        x = this.GetCounters('charge')
        joueur = effect.GetInitiator()
        if x > 0:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda targets:
                        this.DealDamage(targets, 1, effect)
                ).SetTarget(Enemy, range=(0, x), repeat_rules="Health")
            )
        Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            charger,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tirer,
        ),
    ]
