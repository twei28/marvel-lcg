from . import *
# Armed to the Teeth (x2). Evenement CONDITION, cout 0.
#
# Hero Action: Choose one: - Ready each WEAPON you control. - Search your deck and discard pile for a WEAPON and add it to your hand.
# Special: Place 1 all-purpose counter on a WEAPON you control.
#
# Cartes de reference : 45051 Basic Spell (`ChooseAbilities` + `ForChoiceAbility`, UNE seule capacite de jeu : pas de liste blanche
# `factory.py`), ok001b (`Search.PlayerCard`, `include_discard_pile=True`), 50011 (`Faces.PlaceCountersOn(.., 'all-purpose', ..)`).
def GetAbilities() -> Sequence['Ability']:
    def armed(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        def redresser(cibles) -> None:
            Faces.ReadyAll(ArmesSousControle(joueur), effect)
        def chercher(cibles) -> None:
            face = Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=True, trait="WEAPON")
            if face:
                joueur.GainCard(face, effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Ready each WEAPON you control", redresser),
            AbilityFactory.ForChoiceAbility("Search your deck and discard pile for a WEAPON and add it to your hand", chercher),
        )
    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = JoueurDuSpecial(effect, message)
        armes = ArmesSousControle(joueur) if joueur is not None else []
        if not armes:
            return
        cible = armes[0] if len(armes) == 1 else joueur.AskChooseFace(armes, effect, prompt="Place 1 all-purpose counter")
        if cible:
            Faces.PlaceCountersOn([cible], 1, 'all-purpose', effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            armed,
        ).SetPlay().SetLabel(),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
