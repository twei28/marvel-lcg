from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_scheme(effect: 'Effect', last_value: int):
        best = 0
        for face in Worlds.FindCardsOnField(effect, card_type=Unit2):
            if face == effect.this:
                continue
            if HasScheme.IsType(face):
                best = max(best, face.scheme or 0)
            if HasThwart.IsType(face):
                best = max(best, face.thwart or 0)
        return best
    def process_scheme(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Minion).GainScheme(diff, effect)
    def check_attack(effect: 'Effect', last_value: int):
        best = 0
        for face in Worlds.FindCardsOnField(effect, card_type=Unit2):
            if face == effect.this:
                continue
            if HasAttack.IsType(face):
                best = max(best, face.attack or 0)
        return best
    def process_attack(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Minion).GainAttack(diff, effect)
    return [
        # Le SCH/ATK de Purple Man suit le plateau : il doit etre recalcule quand
        # un personnage entre ou sort du jeu, MAIS aussi quand l'ATK/THW/SCH d'un
        # personnage deja en jeu bouge (buff, flip, upgrade). D'ou les deux
        # evenements : sans le second, un heros qui gagne +2 ATK laissait Purple
        # Man sur son ancienne valeur.
        AbilityFactory.WhileValid(
            [OnEvent.CardInPlay(Unit2), OnEvent.CardKeyword("Character")],
            lambda e, m: True, check_scheme, process_scheme),
        AbilityFactory.WhileValid(
            [OnEvent.CardInPlay(Unit2), OnEvent.CardKeyword("Character")],
            lambda e, m: True, check_attack, process_attack),
    ]
