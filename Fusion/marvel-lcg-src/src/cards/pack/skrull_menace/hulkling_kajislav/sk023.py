from . import *

# * Talos — allie d'aspect BASIC (n° 23). SKRULL. Cout 3 [physical].
# THW 1* / ATK 3** (1 et 2 degats consecutifs), 3 PV.
# Interrupt: When Talos would take any amount of consequential damage, deal
#   that damage to another character you control.
#
# Cartes de reference :
#  - **`dt043`** * The Thing : « When your hero would take any amount of
#    damage, deal that damage to The Thing instead » = `WhenUnitWouldTakeDamage`
#    + `message.SetBeInstead(effect)` + `TakeDamage(..., message.will_take_damage)`.
#  - **`53024`** Wingman : `is_consequential_damage=True` pour viser les seuls
#    degats consecutifs.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **consequential** damage » seulement : une attaque ennemie sur Talos
#    le blesse normalement.
#  - « **another** character **you control** » : ton identite ou un autre de
#    tes allies, jamais Talos lui-meme, jamais un personnage d'un autre joueur.
#    Aucun autre personnage (impossible : l'identite est toujours la) => rien.
#  - « deal **that** damage » : le meme montant, 1 apres une contre, 2 apres
#    une attaque. Il est INFLIGE (pas « place ») : une carte Tough l'absorbe.
#  - « Interrupt » nu, pas de cout, pas de limite : optionnel a chaque fois
#    (le joueur peut aussi laisser Talos encaisser).


def GetAbilities() -> Sequence['Ability']:

    def detourner(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)

        joueur = this.GetControlByPlayer()
        if joueur is None:
            return
        montant = message.will_take_damage
        autres = [joueur.GetIdentity()] + [a for a in joueur.GetControlAllies() if a != this]
        cible = joueur.AskChooseFace(
            autres, effect,
            prompt="Choose another character you control to take Talos's consequential damage",
        )
        if cible is None:
            return
        message.SetBeInstead(effect)
        cible.CastTo(Unit2).TakeDamage(this, montant, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "This",
            detourner,
            is_consequential_damage=True,
        ),
    ]
