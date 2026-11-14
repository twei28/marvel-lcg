from . import *

# * Slothful Endurance — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte`.
# « Your identity cannot take damage less than its DEF from each attack. Double the DEF value of your identity. »
#
# LECTURE (provisoire, a confirmer par l'auteur) : « cannot take [damage less than its DEF] from each attack » = une attaque qui infligerait
# MOINS que la DEF de l'identite ne lui inflige RIEN (seuil d'endurance, comme les pactes voisins c'est un avantage) ; une attaque d'au moins DEF
# inflige ses degats normalement. L'autre lecture (plancher : l'identite prend AU MOINS DEF degats) serait une malediction, a contre-courant des six
# autres pactes.
# Cartes de reference : fne/typhoid_mary/60117 (`WhenUnitWouldTakeDamage` + `PreventDamage("All")`), mp012/mp013 (doublement par `get_new_value`).
# ⚠ Mots-pieges : « each ATTACK » (`IsFromAttack`, pas les degats de carte) ; « take » = degats SUBIS apres reductions (`will_take_damage`) ;
# « DOUBLE the DEF value » : +DEF imprime (x2) ; alter-ego sans DEF : rien a prevenir.


def GetAbilities() -> Sequence['Ability']:
    def l_identite_porteuse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return message.trigger is effect.this.CastTo(Attachment).GetBindFace() and message.IsFromAttack()

    def endurance(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        identite = message.trigger
        defense = getattr(identite, "defense", 0)
        if 0 < message.will_take_damage < defense:
            message.PreventDamage("All", effect)

    def valeur_imprimee(effect: 'Effect', face: Any, ui: List['CardFace']) -> int:
        return getattr(face, "printed_defense", 0)

    return [
        *AbilitesDuPacte(),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Identity, endurance, conditions=[l_identite_porteuse]),
        *AbilityFactory.GiveKeywordToAttached(Identity, get_new_value=valeur_imprimee, defense=1),
    ]
