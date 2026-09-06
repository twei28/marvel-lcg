from . import *

# Chomped — ATTACHEMENT nemesis (N 5/5). CONDITION.
#   Aucune icone de boost chiffree, une icone [star].
# Attach to your identity.
# Forced Interrupt: When the round ends, take 1 damage.
# Forced Interrupt: When you would use a basic power, discard Chomped and take
#   1 damage instead.
# [star] Boost: Reveal this card.
#
# ⚠ CETTE CARTE A EXIGE UN CORRECTIF MOTEUR (05/09/2026). Voir l'encadre plus
# bas : la defense de base etait le SEUL des quatre pouvoirs de base qu'on ne
# pouvait pas remplacer.
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `boost` (mots-cles/boost.md) : l'etoile n'est PAS une icone chiffree.
#    `desc.Boost = "0"` — la carte n'ajoute rien a la puissance de
#    l'activation — et l'etoile n'existe que parce qu'une capacite
#    `WhenCardBecomeBoost` est ecrite. Le moteur ne lit pas le texte.
#
# CARTES DE REFERENCE
#  - `ls017` Love Concoction (pack lady_sif) et `55014` (officielle) :
#    `AttachToFaceWhenPutIntoPlay("YourIdentity")` +
#    `WhenCardBecomeBoost("This", RevealThisCard)`. Meme squelette exact.
#  - `al012` Gator Aid (pack alligator_loki) : les trois fabriques qui
#    couvrent « un pouvoir de base » a la source —
#    `WhenUnitWouldAttackOrThwart(..., is_basic_power=True)`,
#    `WhenUnitDefendAgainstAttack(..., is_basic_defense=True)` — et le
#    litteral `"AttachedCharacter"`.
#  - `40069` Superpower Feedback : `identity.TakeDamage(this, 1, effect)`,
#    l'idiome des degats infliges par un attachement a son porteur.
#  - `aa010` / `ag012` / `av002` : `message.SetBeInstead(effect)`, la primitive
#    « instead » du moteur.
#
# TEXTE CONTRE CODE
#  ⚠ « When YOU WOULD USE a basic power » -> il faut se brancher sur les
#    messages `WhenUnitWould...`, PAS sur `WhenUnitUseBasicPower`. Ce dernier
#    est envoye APRES le test de remplacement (can_attack.py:151,
#    can_thwart.py:105, can_defense.py:57) : un `SetBeInstead` pose depuis lui
#    arriverait toujours trop tard, et le pouvoir passerait quand meme. Piege
#    paye a la lecture, pas en jeu.
#  ⚠ « a BASIC POWER » -> LES QUATRE. ATQ et CTR en forme heros
#    (`WhenUnitWouldAttackOrThwart`), DEF en forme heros
#    (`WhenUnitDefendAgainstAttack`), et REC en forme alter-ego
#    (`WhenUnitMakeRecovery`). Oublier la recuperation laisserait le joueur
#    passer en civil pour se soigner sans jamais payer la morsure.
#  ⚠ « INSTEAD » -> le pouvoir n'a PAS lieu. Le cout d'inclinaison, lui, a
#    deja ete paye : c'est le modele uniforme du moteur pour les quatre
#    pouvoirs (`ThisCanAttack` et `ThisCanDefense` posent tous deux
#    `CostFunc.Exhaust("This")` AVANT d'appeler la resolution). Le
#    personnage est donc incline et n'a rien fait, ce qui est bien la
#    punition imprimee.
#  « discard Chomped » -> la carte part, donc la seconde Interruption forcee
#    ne mord QU'UNE FOIS. Celle de fin de round, elle, se repete tant que la
#    carte est la : ce sont deux capacites distinctes, pas deux moities.
#  « take 1 damage » (les deux fois) -> l'IDENTITE, porteuse de
#    l'attachement — pas un allie, pas le heros au choix.
#  ⚠ « [star] Boost: Reveal this card » -> la carte SORT du paquet de boost
#    pour entrer en jeu attachee, au lieu d'etre defaussee. C'est ce qui la
#    met en jeu sans revelation normale (montage `ho017` / `27078` / `ls017`).
#
# ---------------------------------------------------------------------------
# ⚠ CORRECTIF MOTEUR DU 05/09/2026 : LA DEFENSE DE BASE DEVIENT REMPLACABLE
#
# `Message.WhenUnitWouldDefend` portait le commentaire « No `CanBeInstead` »
# (sender_unit.py) et n'heritait donc PAS de la classe. Ses trois soeurs —
# `WhenUnitWouldAttack`, `WhenUnitWouldThwart`, `WhenUnitWouldRecovery` —
# l'ont toutes. Consequence : aucune carte du jeu ne pouvait remplacer une
# DEFENSE de base, et cette carte-ci laissait donc passer un pouvoir sur
# quatre, en silence.
#
# Deux lignes ont suffi, calquees sur `can_attack.py:151` :
#   - `CanBeInstead` ajoute aux bases de `WhenUnitWouldDefend` ;
#   - `if would_defense_message.is_be_instead: return None` dans
#     `CanDefense.DefenseInternal`, AVANT `SetDefender`.
# Sans `SetDefender`, `being_atk_message.defense_messages` reste vide : la DEF
# ne reduit donc rien (can_attack.py:231) et aucun `AfterUnitDefendEnd` n'est
# envoye. Le defenseur reste declare, mais c'est deja la cible de l'attaque —
# le resultat est identique a « il n'a pas defendu ».
#
# `can_defense.py` et `sender_unit.py` sont des fichiers PARTAGES : la regle
# de portee du GUIDE (§6bis) impose la batterie complete, pas seulement les
# cas du pack.
# ---------------------------------------------------------------------------


def GetAbilities() -> Sequence['Ability']:

    def porteur(effect: 'Effect') -> 'CardFace|None':
        this = effect.this.CastTo(Attachment)
        return getattr(this, "bind_face", None)

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        identite = porteur(effect)
        if identite is not None:
            identite.TakeDamage(this, 1, effect)

    def morsure(effect: 'Effect',
                message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart|Message.WhenUnitWouldDefend|Message.WhenUnitWouldRecovery') -> None:
        this = effect.this.CastTo(Attachment)

        # L'identite est relue AVANT la defausse : une fois Chomped hors jeu,
        # `bind_face` ne vaut plus rien.
        identite = porteur(effect)

        # « ... instead » : le pouvoir n'a pas lieu.
        message.SetBeInstead(effect)

        # « discard Chomped and take 1 damage »
        Faces.DiscardAll([this], effect)
        if identite is not None:
            identite.TakeDamage(this, 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity"
        ),
        AbilityFactory.WhenRoundEnd(
            AbilityType.ForcedInterrupt,
            None,
            fin_de_round,
        ),
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.ForcedInterrupt,
            "AttachedCharacter",
            morsure,
            is_basic_power=True,
        ),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.ForcedInterrupt,
            "AttachedCharacter",
            morsure,
            is_basic_defense=True,
        ),
        AbilityFactory.WhenUnitMakeRecovery(
            AbilityType.ForcedInterrupt,
            "AttachedCharacter",
            morsure,
            is_basic_recovery=True,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
