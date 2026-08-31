from . import *

# * Green Goblin (face heros)
# EARTH-6160. GOBLIN.  THW 2 / ATK 1 / DEF 2 — HS 5 / PV 9
# Response: After you attack an enemy, remove 1 status card from that enemy
#   -> deal 2 damage to an enemy and remove 2 threat from a scheme.
#
# Cartes de reference :
#  - declencheur : iw001a * Invisible Woman (« Boo! »), meme phrase « After
#    you attack an enemy » rendue par `AfterUnitAttackEnd(..., "You", ...,
#    against_who=Enemy)` ;
#  - cout « remove 1 status card from that enemy » : wd005 Vibro-Shock
#    Gauntlets, qui retire un statut du vilain en COUT avec choix du joueur
#    quand plusieurs statuts sont poses (DiscardStunned/DiscardConfused,
#    rule=1) — etendu ici a Tough, « 1 status card » ne restreint pas ;
#  - effet a deux cibles de types differents : 08013 Stealth Strike, choix de
#    la manigance via `ChooseAbilities` + `ForChoiceAbility(...).SetTarget()`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « from THAT enemy » (cout) contre « to AN enemy » (degats) : le contraste
#    est imprime. Le statut part de l'ennemi ATTAQUE, les 2 degats vont a
#    N'IMPORTE quel ennemi, au choix du joueur.
#  - Le retrait du statut est un COUT (avant la fleche) : la Response ne se
#    propose que si l'ennemi attaque a au moins un statut, et retirer un
#    Tough est un cout parfaitement legal (et souvent rentable).

def GetAbilities() -> Sequence['Ability']:

    def ennemi_a_statut(message: 'Message.AfterUnitAttackEnd') -> 'CardFace|None':
        # ⚠ le champ s'appelle `attacked_targets` (propriete de
        # AttackerMessageInternal, message_type.py:140), PAS `attacked` :
        # le parametre du __init__ ne devient pas un attribut du meme nom.
        for unit in message.attacked_targets:
            if unit is not None and unit.IsInPlay() and (
                    unit.HasStatus("Stunned") or unit.HasStatus("Confused")
                    or unit.HasStatus("Tough")):
                return unit
        return None

    def a_un_statut(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return ennemi_a_statut(message) is not None

    def response(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        initiator = effect.GetInitiator()

        cible = ennemi_a_statut(message)
        if cible is None:
            return

        def effet_apres_cout(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            # « deal 2 damage to an enemy and remove 2 threat from a scheme »
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy",
                    lambda cibles: this.DealDamage(cibles, 2, effect),
                ).SetTarget(Enemy),
            )
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    lambda cibles:
                        this.RemoveThreatFromSchemes(cibles, 2, effect),
                ).SetTarget(Scheme2),
            )

        # COUT : retirer 1 carte de statut de l'ennemi attaque. Quand
        # plusieurs types de statut sont poses, le choix revient au joueur
        # (meme montage que wd005).
        def retirer_sonne(targets: Sequence['CardFace']) -> None:
            cible.DiscardStunned(effect, rule=1)
            effet_apres_cout(targets)

        def retirer_desoriente(targets: Sequence['CardFace']) -> None:
            cible.DiscardConfused(effect, rule=1)
            effet_apres_cout(targets)

        def retirer_robuste(targets: Sequence['CardFace']) -> None:
            cible.DiscardTough(effect, rule=1)
            effet_apres_cout(targets)

        choix = []
        if cible.HasStatus("Stunned"):
            choix.append(AbilityFactory.ForChoiceAbility(
                "Remove the stunned status card", retirer_sonne))
        if cible.HasStatus("Confused"):
            choix.append(AbilityFactory.ForChoiceAbility(
                "Remove the confused status card", retirer_desoriente))
        if cible.HasStatus("Tough"):
            choix.append(AbilityFactory.ForChoiceAbility(
                "Remove the tough status card", retirer_robuste))
        if not choix:
            return
        initiator.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "You",
            response,
            against_who=Enemy,
            conditions=[a_un_statut],
        ),
    ]
