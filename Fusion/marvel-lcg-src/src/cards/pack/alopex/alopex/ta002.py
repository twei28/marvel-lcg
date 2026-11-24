from . import *

# * Nobody (Angel Bridges) — ALLIE signature, x1. NINJA. VIGILANTE.
# Cout 2, [mental]. THW 1* / ATQ 1* / PV 3.
# [star] Response: After Nobody takes consequential damage ([consequential]), if she:
#   • Attacked an enemy with Prey attached, daze that enemy.
#   • Thwarted a scheme with Prey attached, cloak her.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (fichier Inkwire du 10/11/2026, image du Drive) : avant, DEUX Reponses
# separees (« After Nobody attacks... », « After Nobody thwarts... »). LECTURE CHOISIE PAR L'UTILISATEUR
# (17/11/2026, « meme action ») : la Reponse part quand les degats consecutifs viennent de SON attaque ou
# de SON contre (ATQ 1* / CTR 1*) ; « if she attacked an enemy with Prey » = CETTE attaque-la, « if she
# thwarted a scheme with Prey » = CE contre-la (etat de la manigance AU MOMENT du contre, decision du
# 16/10/2026 conservee). Modele : `sh014` Minarai (`AfterAllyTakeConsequentialDamage`, qui porte
# `atk_message` / `thw_message`).
#
# Cartes de reference :
#  - « After X attacks » : `AfterUnitAttackEnd(Response, "This", op,
#    against_who=Enemy)` (RECETTES §1) ; « After X thwarts » :
#    `AfterUnitThwartEnd(Response, "This", op)` (thwart.py:180) ;
#  - « Daze » : fiche mots-cles/daze.md (`Faces.GiveStatus(..., "Dazed", ...)`) ;
#    « Cloak her » : fiche cloak.md (`Faces.GiveStatus(..., "Cloaked", ...)`).
#
# Mots-pieges :
#  - « [star] Response » : UNE seule Reponse (depuis le 17/11/2026), deux branches selon l'action ;
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

    def ennemis_avec_prey(attaque: 'Message.AfterUnitAttackEnd') -> List['CardFace']:
        return [f for f in attaque.attacked_targets
                if Enemy.IsType(f) and f.IsInPlay() and PreyAttachee(f) is not None]

    def prey_au_moment_du_contre(contre: 'Message.AfterUnitThwartEnd') -> bool:
        return any(getattr(m, 'prey_attachee', False) for m in contre.would_thw_messages)

    def conditions_de_la_reponse(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> bool:
        if message.atk_message is not None:
            return bool(ennemis_avec_prey(message.atk_message))
        if message.thw_message is not None:
            return prey_au_moment_du_contre(message.thw_message)
        return False

    def nobody(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        if message.atk_message is not None:
            cibles = ennemis_avec_prey(message.atk_message)
            if cibles:
                Faces.GiveStatus(cibles, "Dazed", effect)
        elif message.thw_message is not None:
            Faces.GiveStatus([this], "Cloaked", effect)

    return [
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.NonKeyword,
            "This",
            noter_prey_sur_la_manigance,
        ),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            nobody,
            conditions=[conditions_de_la_reponse],
        ),
    ]
