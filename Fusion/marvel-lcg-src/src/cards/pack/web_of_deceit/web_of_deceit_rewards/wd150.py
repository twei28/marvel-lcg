from . import *

# * Get it Off!

def GetAbilities() -> Sequence['Ability']:

    def arracher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action: Exhaust this card → find a Symbiosis card and add it to
        # the victory display. Draw 1 card. »
        #
        # « Find » sans plus : on cherche partout ou une carte de l'arbre peut
        # etre, deck et defausse compris.
        joueur = effect.GetInitiator()
        trouvee = Search.SearchForCard(
            effect,
            joueur,
            include_player_deck=True,
            include_player_discard_pile=True,
            include_player_hand_cards=True,
            set_name="Web of Deceit Rewards",
            check_face_fn=lambda f: f.paper.card_id in SYMBIOSIS,
        )
        if trouvee:
            Faces.AddToVictoryDisplay([trouvee], effect)
        joueur.DrawUp(1, effect)

    def cartes_en_victoire(effect: 'Effect', ui: List['CardFace']) -> int:
        # « While there are 5 Symbiosis cards in the victory display you get +1
        # to each of your basic powers and +1 hand size. »
        combien = len([x for x in Worlds.VictoryDisplay(effect).Get()
                       if x.paper.card_id in SYMBIOSIS])
        return 1 if combien >= 5 else 0

    return [
        AbilityFactory.ThisGainKeyword(
            cartes_en_victoire,
            attack=1,
            thwart=1,
            defense=1,
            recover=1,
            hand_size=1,
            change_on_event=OnEvent.Victory(None),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            arracher
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
