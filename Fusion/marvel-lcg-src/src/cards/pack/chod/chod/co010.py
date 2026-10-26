from . import *

def GetAbilities() -> Sequence['Ability']:
    def une_carte_physique_en_main(effect: 'Effect', tc: 'CardFace', ui: List['CardFace']) -> int:
        """« While you have a card with a printed [x] resource in your hand » : 1 si une carte de la main imprime la couleur."""
        Unused(tc, ui)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return 0
        return 1 if any("R" in Types(f) for f in joueur.hand_cards.Get()) else 0

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Ch'od"),
            hand_size=1,
            get_new_value=une_carte_physique_en_main,
            ex_change_on_event=OnEvent.HandCards("EngagedPlayer"),
        ),
    ]
