from . import *

# Tarnax IV — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# While a side scheme is in play, this card gains the amplify icon ([amplify]).
#
# Carte de reference : **`40109`** Pure Force
# (`ThisGainKeywordWhileFaceIsInPlay(CardFinder(...), amplify=1)`), MAIS cette
# fabrique refuse un ENVIRONNEMENT : `ThisGainKeywordInternal` affirme que la
# carte est un personnage, un complot, un soutien, une amelioration ou un
# attachement, et l'icone n'etait jamais posee (constate le 15/10/2026, cas
# [sk-e] sk095 rouge). Meme brique en dessous, `AbilityFactory.WhileValid`
# (on_while.py), ecrite ici pour l'environnement : `check` rend 1 tant qu'un
# complot annexe est en jeu, `process` pose la difference avec GainAmplify.
#
# ⚠ « **a** side scheme » : n'importe lequel (`SchemeSide2`) ; « this card » : la planete elle-meme.
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    annexe = CardFinder(card_type=SchemeSide2)

    def un_complot_annexe(effect: 'Effect', last_value: int) -> int:
        Unused(last_value)
        return 1 if Worlds.FindCardOnField(effect, annexe, game_area=effect.this.card.game_area) else 0

    def amplifier(effect: 'Effect', diff: int, curr: int) -> None:
        Unused(curr)
        this = effect.this.CastTo(Environment)
        this.GainAmplify(diff, effect)
        Message.AfterCardApply_Text([this], effect, diff)

    return [
        AbilityFactory.WhileValid(OnEvent.CardInPlay(annexe), lambda effect, message: True,
                                  un_complot_annexe, amplifier),
    ]
