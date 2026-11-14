from . import *

# Trained Shots — EVENEMENT, cout 2, [energy] (x2 dans le deck). SKILL.
# Hero Action: Deal 2 damage to an enemy. Resolve the "Special" ability on a [[WAKANDA]] upgrade.
#   Resolve the "Special" ability on a [[WAKANDA]] upgrade.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Hero Action d'evenement a degats : `01022` Ground Stomp (`WhenInYourPlayTurn(HeroAction, op).SetPlay()
#    .SetLabel().SetTarget(Enemy)` + `this.DealDamage(effect.targets, N, effect)`).
#  - plusieurs Specials : `51025` Heart of the Panther (`ChooseAbilities` + `ForChoiceAbility` +
#    `initiator.ResolveSpecialAbility(targets, effect)`).
#
# MOTS-PIEGES
#  - DEUX resolutions SEPAREES (« Resolve ... Resolve ... ») : deux choix independants, la MEME amelioration
#    peut etre choisie deux fois (l'insert ne l'interdit pas) ; ce n'est pas « up to 2 upgrades ».
#  - « a WAKANDA UPGRADE » : une amelioration (type Upgrade), pas le heros ni un allie.
#  - pas de `(attack)` imprime : ce n'est PAS une attaque (`SetLabel()` sans etiquette).
#  - les deux resolutions ont lieu APRES les degats (ordre du texte).
def GetAbilities() -> Sequence['Ability']:

    def tirs_precis(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage(effect.targets, 2, effect)
        ResoudreSpecialSurAmelioration(effect, joueur)
        ResoudreSpecialSurAmelioration(effect, joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tirs_precis,
        ).SetPlay().SetLabel()
        .SetTarget(Enemy),
    ]
