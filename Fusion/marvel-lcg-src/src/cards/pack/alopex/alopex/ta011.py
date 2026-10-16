from . import *

# Prey — AMELIORATION (16e carte du deck, jamais dans les 15) — CONDITION.
# Pas de cout. Mise de cote au Setup par ta001b, attachee par Matagi (ta001a).
# Alopex' attacks deal 1 additional damage to attached enemy.
# Alopex' thwarts remove 1 additional threat from attached scheme.
# Forced Interrupt: When this card leaves play, set this card aside.
#
# Cartes de reference :
#  - « attacks against attached X deal N additional damage » : `62009`
#    Cruisin' for a Bruisin' (`WhenUnitWouldAttackUnit(..., "AttachedMinion")`) ;
#    ici l'ATTAQUANT est `"You"` (l'identite : « Alopex' attacks ») et la cible
#    `"AttachedEnemy"`. `message.IncreaseDamage(1, effect)` (modele `exposed.py`,
#    `bl007`) couvre l'attaque de base ET l'attaque d'evenement ;
#  - « thwarts remove N additional threat » : `37013` Operative Skill,
#    `WhenUnitWouldThwart(type, "You", op)` + `message.RemoveAdditionalThreat` ;
#    cible `"AttachedScheme"` (`61014` Stakeout) ;
#  - Forced Interrupt « leaves play » : `21180b` Cosmo,
#    `WhenCardLeavePlay(ForcedInterrupt, 'This', op)` + `Faces.SetAside`.
#
# Mots-pieges :
#  - « ALOPEX' attacks » : les attaques de l'IDENTITE, pas celles d'un allie
#    (Nobody n'en profite pas) ; `"You"` = l'identite du controleur de Prey ;
#  - « to ATTACHED enemy » : seulement la cible portant Prey ; pas les autres ;
#  - « 1 ADDITIONAL » : +1, en plus des degats / menaces normaux ;
#  - « set this card ASIDE » : la carte va dans la reserve (`set_aside_deck`) et
#    NON dans la defausse : Matagi pourra la retrouver ;
#  - le texte dit « Alopex' » (sans « s ») : typo imprimee, conservee dans
#    cards.json.


def GetAbilities() -> Sequence['Ability']:

    def plus_un_degat(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.IncreaseDamage(1, effect)

    def plus_une_menace(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.RemoveAdditionalThreat(1, effect)

    def mettre_de_cote(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        # ⚠ GARDE ANTI-BOUCLE : `Faces.SetAside` fait QUITTER LE JEU a la carte, ce
        # qui renvoie `WhenCardLeavePlay` et relance cette Interruption forcee sans
        # fin (RecursionError AVALEE par le moteur : la carte finissait de cote
        # mais `AfterCardLeavePlay` n'etait jamais envoye, donc Kabuki et Kama ne
        # repondaient pas ; constate au journal du cas ta008, 16/10/2026).
        if getattr(this, "mise_de_cote_en_cours", False):
            return
        this.mise_de_cote_en_cours = True
        try:
            Faces.SetAside([this], effect)
        finally:
            this.mise_de_cote_en_cours = False

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            "You",
            "AttachedEnemy",
            plus_un_degat,
        ),
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.NonKeyword,
            "You",
            plus_une_menace,
            thwarted_scheme="AttachedScheme",
        ),
        AbilityFactory.WhenCardLeavePlay(
            AbilityType.ForcedInterrupt,
            "This",
            mettre_de_cote,
        ),
    ]
