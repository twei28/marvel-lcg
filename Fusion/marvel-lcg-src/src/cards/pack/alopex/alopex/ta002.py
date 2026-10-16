from . import *

# * Nobody (Angel Bridges) — ALLIE signature, x1. NINJA. VIGILANTE.
# Cout 2, [mental]. THW 1* / ATQ 1* / PV 3.
# [star] Response: After Nobody attacks an enemy with Prey attached, daze that
#   enemy.
# [star] Response: After Nobody thwarts a scheme with Prey attached, cloak her.
#
# Cartes de reference :
#  - « After X attacks » : `AfterUnitAttackEnd(Response, "This", op,
#    against_who=Enemy)` (RECETTES §1) ; « After X thwarts » :
#    `AfterUnitThwartEnd(Response, "This", op)` (thwart.py:180) ;
#  - « Daze » : fiche mots-cles/daze.md (`Faces.GiveStatus(..., "Dazed", ...)`) ;
#    « Cloak her » : fiche cloak.md (`Faces.GiveStatus(..., "Cloaked", ...)`).
#
# Mots-pieges :
#  - « [star] Response » : DEUX Reponses distinctes, pas de choix ;
#  - « an enemy WITH PREY ATTACHED » : l'ennemi attaque porte Prey ; si cette
#    attaque l'a vaincu, il n'y a plus d'ennemi a etourdir (rien a faire) ;
#  - « a scheme WITH PREY ATTACHED » : lu A L'INSTANT DU CONTRE : si ce contre
#    vide la manigance, Prey part (de cote) mais la Reponse part quand meme
#    (information connue au moment du contre) — DECISION UTILISATEUR (16/10/2026, Q2) ;
#  - « cloak HER » : Nobody elle-meme (pas l'identite) ;
#  - « daze THAT enemy » : l'ennemi attaque (pas un autre) ;
#  - ATQ 1* / THW 1* : les etoiles imprimees sont des degats consecutifs
#    (desc `1*`), lus par le moteur.
#
# DECISION UTILISATEUR (16/10/2026, Q2, ta002) : « thwarts a scheme with Prey attached » quand le
# contre retire la derniere menace (Prey part de cote avec la manigance) ?
# Lecture retenue : la Reponse part (etat de la manigance AU MOMENT du contre).


def GetAbilities() -> Sequence['Ability']:

    def noter_prey_sur_la_manigance(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        # Information connue AU MOMENT du contre : la manigance peut etre
        # videe (et sa Prey envoyee de cote) avant la fenetre de Reponse.
        Unused(effect)
        message.prey_attachee = any(PreyAttachee(s) is not None for s in message.schemes)

    def prey_au_moment_du_contre(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> bool:
        return any(getattr(m, 'prey_attachee', False) for m in message.would_thw_messages)

    def etourdir_l_ennemi(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        cibles = [f for f in message.attacked_targets
                  if Enemy.IsType(f) and f.IsInPlay() and PreyAttachee(f) is not None]
        if cibles:
            Faces.GiveStatus(cibles, "Dazed", effect)

    def prey_sur_l_ennemi(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return any(Enemy.IsType(f) and f.IsInPlay() and PreyAttachee(f) is not None
                   for f in message.attacked_targets)

    def se_camoufler(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.GiveStatus([this], "Cloaked", effect)

    return [
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.NonKeyword,
            "This",
            noter_prey_sur_la_manigance,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            etourdir_l_ennemi,
            against_who=Enemy,
            conditions=[prey_sur_l_ennemi],
        ),
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.Response,
            "This",
            se_camoufler,
            conditions=[prey_au_moment_du_contre],
        ),
    ]
