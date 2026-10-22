from . import *

# Redirection Mastery — AMELIORATION 2 [physical], aspect Protection (TMNT Aspects, Inkwire). SKILL.
# Play under any player's control. Max 1 per player.
# Hero Response: After you exactly defend an attack, deal damage to the attacker equal to your DEF for
#   that attack.
#
# NOUVELLE. LECTURE CHOISIE PAR L'UTILISATEUR (17/10/2026, Q-UP1) : « DEFENSE EXACTE ». La Reponse ne part
# que si la valeur de l'attaque (boosts compris) est EXACTEMENT egale a la DEF de votre heros pour cette
# attaque (coup pare pile, 0 degat) ; l'attaquant subit alors des degats egaux a cette DEF.
#
# EXTENSION MOTEUR : `Message.AfterUnitDefendEnd` porte maintenant `damage_before_defense` (valeur de
# l'attaque avant le retrait de la DEF, boosts et bonus de `WhenCalculatingAttackDamage` compris) et
# `defense_value` (DEF retenue pour ce coup) ; `dealt_damage` est plafonne a 0 et ne distingue pas la
# parade pile d'une attaque inferieure a la DEF.
#
# CARTES DE REFERENCE
#  - `09020` Unflappable : « Play under any player's control » = `CanPlayThisUpgradeCard("Players")` ;
#    « After you defend against an attack » = `AfterUnitDefendAgainstAttack(Response, "You", ...)`.
#  - `62015` Take a Stand : « Hero Response: After your hero defends » = `AfterUnitDefendEnd(HeroResponse,
#    "YourHero", ...)`.
#  - `40165` Stryfe : « deal damage to the attacker » = `attacker.TakeDamage(this, value, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « you EXACTLY defend » : attaque == DEF (egalite stricte, sans plafond) ; attaque > DEF : degats
#    subis, pas exact ; attaque < DEF : parade « trop large », pas exact non plus.
#  ⚠ « YOUR DEF FOR THAT ATTACK » : la DEF retenue pour ce coup (bonus d'Interruption compris), pas la
#    DEF imprimee. « the attacker » : l'attaquant de CETTE attaque, s'il est encore en jeu.
#  ⚠ « Hero Response » : forme heros (le defenseur est votre HEROS, pas un allie).
#  « Max 1 per player » : `desc.MaxPerUnit` (lu par le moteur). Aucune limite par tour.


def GetAbilities() -> Sequence['Ability']:

    def defense_exacte(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> bool:
        Unused(effect)
        return message.damage_before_defense is not None and \
            message.damage_before_defense == message.defense_value

    def redirection(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        attaquant = message.attacker
        valeur = message.defense_value
        if attaquant is None or valeur is None or valeur <= 0 or attaquant.IsDefeated():
            return
        attaquant.TakeDamage(this, valeur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "YourHero",
            redirection,
            conditions=[defense_exacte],
        ),
    ]
