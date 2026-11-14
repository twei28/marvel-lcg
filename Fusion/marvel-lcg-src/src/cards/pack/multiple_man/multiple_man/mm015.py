from . import *

# Kinetic Absorption Suit : AMELIORATION, cout 1, [mental]. ARMOR. TECH. (sans « Attach to » : extension de l'identite, RRG « Upgrade »)
# Hero Interrupt: When Multiple Man is dealt damage from an attack, exhaust this card → choose 1:
#  • Reduce the amount of damage taken by 1.
#  • Search your hand, deck, and discard pile for a Dupe ally and put it into play. (Shuffle.)
#
# CARTES DE REFERENCE : `nt007` / `05005` (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", ..., is_from_attack=True)` + `message.PreventDamage(n, effect)`), `ca014` (`ForChoiceAbility` + `joueur.ChooseAbilities`).
# TEXTE CONTRE CODE : « dealt damage FROM AN ATTACK » -> `is_from_attack=True`. « exhaust this card → » : cout. « choose 1 » : deux branches exclusives ; la 2e n'a pas besoin que le degat soit reduit
#  (l'attaque frappe quand meme). « (Shuffle.) » : rappel, la recherche melange le deck (RRG). Chiffres : cout 1, -1 degat.


def GetAbilities() -> Sequence['Ability']:

    def combinaison(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        reduire = AbilityFactory.ForChoiceAbility(
            "Reduce the amount of damage taken by 1",
            lambda cibles: message.PreventDamage(1, effect),
        ).SetHasNoTargetEffect()
        chercher = AbilityFactory.ForChoiceAbility(
            "Search your hand, deck, and discard pile for a Dupe ally and put it into play",
            lambda cibles: ChercherEtMettreUnDupe(effect, joueur),
        ).SetHasNoTargetEffect()
        joueur.ChooseAbilities(effect, reduire, chercher)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            combinaison,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
