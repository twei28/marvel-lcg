from . import *

# To Battle! — EVENEMENT, cout 2, [mental]. TACTIC. x3.
# Hero Action: Choose two of the following:
#   • Search your deck and discard pile for a TACTIC or WEAPON upgrade and add
#     it to your hand.
#   • Ready a hero-specific upgrade you control.
#   • Ready Ares.
#
# CARTES DE REFERENCE
#  - `br005` Star Jump (pack beta_ray_bill) : « Choose X of the following »,
#    trois branches dans un `ChooseAbilities` repose X fois.
#  - `an001b` / `ho007` : `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, finder=CardFinder(...))` + `GainCard`.
#  - `an001a` / `ho011` : `Faces.ReadyAll`.
#
# TEXTE CONTRE CODE
#  ⚠ « Choose TWO of the following » -> ARBITRAGE UTILISATEUR DU 07/09/2026 :
#    deux options DIFFERENTES. `br005` autorisait la repetition parce que son
#    texte disait « Choose X » sans « different » ; ici la lecture habituelle
#    de « two of the following » est deux lignes distinctes. La branche deja
#    prise est retiree du second choix.
#  ⚠ « a TACTIC OR WEAPON upgrade » -> `CardFinder(card_type=Upgrade,
#    traits=[TACTIC, WEAPON])` : `traits` est un OU (finder.py:133). Ares' Axe
#    (WEAPON) et Feint/Reeling/Sundered/God of War... (TACTIC) sont eligibles ;
#    Ares' Battle Helm (ARMOR) ne l'est pas.
#  ⚠ « deck AND discard pile » -> les deux zones, `include_discard_pile=True`.
#  ⚠ « a HERO-SPECIFIC upgrade YOU CONTROL » -> classe `IdentitySpecific`
#    (desc Class « Hero », card_player.py:69) ET sous votre controle. Une
#    amelioration d'aspect ne compte pas ; Feint pose sur un ennemi reste
#    « you control » (le controleur d'une amelioration est son joueur), mais
#    elle n'a rien a redresser : `canbe_ready=True` ne propose que l'incline.
#  ⚠ « Ready ARES » -> l'identite en jeu, par le TYPE (les deux faces portent
#    ce nom). En forme heros, puisque c'est une Hero Action.


def GetAbilities() -> Sequence['Ability']:

    def au_combat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        prises: set = set()

        def chercher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            prises.add("chercher")
            face = Search.PlayerCard(
                effect, joueur,
                include_player_deck=True,
                include_discard_pile=True,
                finder=CardFinder(card_type=Upgrade, traits=[TRAIT_TACTIC, TRAIT_WEAPON]),
            )
            if face is not None:
                joueur.GainCard([face], effect)

        def redresser_amelioration(cibles: Sequence['CardFace']) -> None:
            prises.add("amelioration")
            faces = [c for c in cibles if c is not None]
            if faces:
                Faces.ReadyAll(faces, effect)

        def redresser_ares(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            prises.add("ares")
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

        def branches() -> list:
            choix = []
            if "chercher" not in prises:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Search your deck and discard pile for a TACTIC or WEAPON upgrade",
                    chercher))
            if "amelioration" not in prises:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Ready a hero-specific upgrade you control",
                    redresser_amelioration,
                ).SetTarget(
                    CardFinder(card_type=Upgrade, card_class="IdentitySpecific"),
                    from_where=["YouControlCards"],
                    canbe_ready=True,
                ))
            if "ares" not in prises:
                choix.append(AbilityFactory.ForChoiceAbility("Ready Ares", redresser_ares))
            return choix

        for _ in range(2):
            choix = branches()
            if not choix:
                break
            joueur.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            au_combat,
        ).SetPlay(),
    ]
