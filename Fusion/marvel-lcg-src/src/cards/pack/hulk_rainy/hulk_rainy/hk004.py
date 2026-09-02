from . import *

# Hulk Smash — evenement signature, x2 (n/15 = 4 et 5).
# ATTACK. SUPERPOWER. Cout 3, ressource [physical].
# Hero Action: Make the following attacks against the same target:
# • (attack): Deal 3 damage.
# • (attack): Deal 3 damage.
# • (attack): Deal 3 damage.
#
# Cartes de reference :
#  - `th010` It's Clobberin' Time! (pack the_thing) pour la SUITE d'attaques
#    d'un meme evenement ;
#  - `08013` Stealth Strike pour `SetLabel('attack').SetTarget(Enemy)` sur
#    l'abilite elle-meme.
#
# ⚠ ECART VOLONTAIRE AVEC th010, ET C'EST LE POINT DELICAT DE LA CARTE.
# th010 imprime « 2 attacks » sans contrainte de cible, et repose donc un
# `ForChoiceAbility(...).SetTarget(Enemy)` a CHAQUE attaque : le joueur
# choisit deux fois. Hulk Smash imprime « against the SAME target » : la
# cible se choisit UNE FOIS. On la prend donc sur l'abilite
# (`.SetTarget(Enemy)`) et on frappe trois fois `effect.targets`, sans
# jamais reposer de selecteur.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the SAME target » : une seule cible, choisie une fois. Reposer un
#    selecteur serait un vrai defaut de regle, pas un detail d'ergonomie.
#  - TROIS attaques distinctes, pas une attaque de 9. La difference se voit :
#    une Riposte se declenche trois fois, une carte Tenace n'absorbe que la
#    premiere, et un sbire a 3 PV tombe des la premiere en laissant les deux
#    suivantes sans cible.
#  - « Deal 3 damage » sans « to an enemy » sur chaque puce : la cible est
#    celle annoncee en tete, d'ou la lecture ci-dessus.
#  - Aucun mot-cle imprime : ni overkill, ni piercing, ni ranged.
#  - La cible peut mourir en cours de route. `DealDamage` sur une face qui
#    n'est plus en jeu ne fait rien et ne leve pas : les attaques restantes
#    tombent dans le vide, ce qui est le comportement correct.


def GetAbilities() -> Sequence['Ability']:

    def hulk_smash(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        for _ in range(3):
            this.DealDamage(effect.targets, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hulk_smash,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
