from . import *

# Hostile Override — TRAITRISE NEMESIS, boost ETOILE.
# When Revealed: If you control at least one [[HACKED]] upgrade, deal damage to
#   a friendly character equal to your ATK value, or place threat on the main
#   scheme equal to your THW value. If you control no [[HACKED]] upgrades, you
#   are confused.
# [star] Boost: You are confused.
#
# Cartes de reference :
#  - `01077` / `50022` : `hero.attack` et `hero.thwart` pour lire les valeurs
#    COURANTES (modificateurs compris), jamais les valeurs imprimees.
#  - `aa005` / `dz037` : `ChooseAbilities` pour un « ou » obligatoire.
#  - `wd014` pour le statut Desoriente et le boost etoile.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **your** ATK value » : celle de l'identite du joueur qui revele. En
#    forme ALTER-EGO, Juston n'a ni ATQ ni CTR : les deux branches valent zero,
#    ce qui est bien ce que dit la carte (rien n'exige la forme heros).
#  - « deal damage to **a friendly character** » : l'identite ou un allie, au
#    choix — donc `"YouControlUnit"` et pas seulement les allies.
#  - Le choix entre les deux branches appartient au JOUEUR : le texte dit
#    « ou », sans designer qui tranche, et la regle generale confie ce choix
#    au joueur qui resout la carte.
#  - Le boost est ETOILE : aucune valeur numerique dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def desorienter(joueur: 'Player', effect: 'Effect') -> None:
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    def hostile_override(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        piratees = [f for f in joueur.GetControlUpgrade()
                    if f.HasTrait(TRAIT_HACKED)]
        if not piratees:
            desorienter(joueur, effect)
            return

        identite = joueur.GetIdentity()

        def frapper(cibles: Sequence['CardFace']) -> None:
            this.DealDamage(cibles, identite.attack, effect)

        def comploter(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.PlaceThreatOnSchemes("MainScheme", identite.thwart, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal damage to a friendly character equal to your ATK", frapper)
            .SetTarget("YouControlUnit"),
            AbilityFactory.ForChoiceAbility(
                "Place threat on the main scheme equal to your THW", comploter),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            desorienter(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hostile_override,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
