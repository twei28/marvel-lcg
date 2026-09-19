from . import *

# Imprisoned (obligation de rencontre)
# You cannot thwart, attack, or change to alter-ego form.
# Hero Action: Spend 3 resources of any type or exhaust characters you control
#   with a total THW of 3 or more -> discard this card.
# [star] Boost: Reveal this card.
# Modeles : 27133 (PlayersCannotThwartWhile), 11049 (PlayersCannotAttackWhile),
# PlayersCannotChangeForms(to_form=AlterEgo) ; la seconde branche de cout est
# un CostFunc.Custom qui fait choisir des personnages prets jusqu'a 3 THW.

def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.DiscardAll([effect.this], effect)

    def incliner_pour_trois_thw(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        joueur = effect.GetInitiator()
        prets = [c for c in joueur.GetControlCharacters() if c.IsReady()]
        if sum(c.thwart for c in prets) < 3:
            return False
        choisis: List['CardFace'] = []
        while sum(c.thwart for c in choisis) < 3:
            restants = [c for c in prets if c not in choisis]
            if not restants:
                return False
            c = restants[0] if len(restants) == 1 else joueur.AskChooseFace(restants, effect)
            if c is None:
                return False
            choisis.append(c)
        Faces.ExhaustAll(choisis, effect)
        return True

    def revele(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is not None:
            this.Reveal(joueur, effect)

    return [
        AbilityFactory.PlayersCannotThwartWhile("You", None),
        AbilityFactory.PlayersCannotAttackWhile("You", None),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "You", to_form=AlterEgo),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, defausser)
            .SetName("Spend 3 resources of any type: discard Imprisoned")
            .SetCost(Cost("3")),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, defausser)
            .SetName("Exhaust characters with a total THW of 3 or more: discard Imprisoned")
            .SetCostFunc(CostFunc.Custom(None, incliner_pour_trois_thw)),
        AbilityFactory.WhenCardBecomeBoost("This", revele),
    ]
