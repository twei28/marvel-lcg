from . import *

# * Major Victory (face heros) : HP 10, ATK 1, THW 2, DEF 2, main 5. GUARDIAN. PSIONIC. SOLDIER.
# Shield Toss — Action: Spend 1 resource of any type → find Captain America's Shield and add it to your hand.
#   If it leaves play this way, deal 4 damage to an enemy. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `04001b` (Clint Barton, Weapon of Choice) et `rg001b` : `SetCost(Cost("1"))` + `Search.PlayerCard` + `GainCard`.
#  - `Faces.ReturnToHand` : le meme chemin, mais valable pour une carte qui est EN JEU (« if it leaves play this way »).
#
# TEXTE CONTRE CODE
#  « find » = chercher dans le deck, la defausse ET le jeu (`include_player_area`), contrairement a Hawkeye/Red Guardian
#    qui ne cherchent que deck + defausse.
#  « if it leaves play this way » -> on lit `IsInPlay()` AVANT le retour en main. Un bouclier venant du deck ou de la
#    defausse ne declenche rien.
#  « deal 4 damage to an enemy » -> les degats viennent de CETTE capacite (nom « Shield Toss ») : c'est ce qui permet a
#    Telekinetic Throw (mv007) de se declencher.
#  « Limit once per round » -> `LimitOncePerRound`.


def GetAbilities() -> Sequence['Ability']:

    def shield_toss(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        bouclier = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            include_player_area=True,
            card_type=Upgrade,
            name=NOM_BOUCLIER,
        )
        if not bouclier:
            return
        etait_en_jeu = bouclier.IsInPlay()
        Faces.ReturnToHand([bouclier], joueur, effect)
        if etait_en_jeu:
            cible = ChoisirUne(joueur, Worlds.GetOnFieldEnemies(effect), effect, "Shield Toss : deal 4 damage to an enemy")
            if cible is not None:
                this.DealDamage([cible], 4, effect)

    return [
        (AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            shield_toss,
        )
            .SetName(NOM_SHIELD_TOSS)
            .SetCost(Cost("1"))
            .LimitOncePerRound()),
    ]
