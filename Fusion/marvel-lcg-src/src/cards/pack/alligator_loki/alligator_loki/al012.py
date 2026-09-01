from . import *

# Gator Aid — amelioration signature. SKILL. Cout 2, [energy].
# Interrupt: When attached character uses a basic power, exhaust Gator Aid →
#   that character gets +1 to that power for this use. After this use, you
#   may attach this to another friendly character.
#
# Cartes de reference :
#  - bw003 Ironheart : « uses a basic power » = les TROIS pouvoirs de base,
#    couverts par `WhenUnitWouldAttackOrThwart(..., is_basic_power=True)` plus
#    `WhenUnitDefendAgainstAttack(..., is_basic_defense=True)` ;
#  - bt008 : « +N to that power for this use » -> `message.GainATKForThisAttack`,
#    et ses jumeaux `GainTHWForThisThwart` (sender_friend.py:69) et
#    `GainDEFForThisAttack` (sender_unit.py:141) ;
#  - « attached character » -> le litteral `"AttachedCharacter"` de
#    `CheckWhichCard` (condition/card_type.py) ;
#  - « after this use » -> une capacite temporaire sur `message.end_event`,
#    filtree sur `pre_message` : c'est exactement ce que `Effect
#    .SetDestroyedAfter(until_after_event=)` fait en interne (effect.py:368).
#
# ---------------------------------------------------------------------------
# AUCUNE CAPACITE « PLAY » : la carte ne dit pas a quoi elle s'attache, donc
# `Upgrade.GetAbilities` la pose sur l'identite du joueur (ma006, meme cas).
# C'est ensuite « attach this to ANOTHER friendly character » qui la fait
# voyager : identite ou allie de n'importe quel joueur
# (`Worlds.GetOnFieldFriendlyCharacters`), sauf son porteur actuel.
#
# ⚠ « you MAY attach » -> `MayChooseFace` (forced=False), le joueur peut la
# laisser ou elle est.
# ⚠ Gator Aid inclinee ne se declenche plus : la fleche est un COUT
# (`CostFunc.Exhaust("This")`), le moteur ne la propose pas si elle est deja
# inclinee. Le passage a un autre personnage ne la redresse PAS.
# ⚠ Sur un allie, « that character gets +1 » : l'allie frappe plus fort, mais
# les degats consequents restent les siens. Rien a coder pour ca.

def GetAbilities() -> Sequence['Ability']:

    def apres_usage(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = this.GetControlByPlayer()
        if not isinstance(joueur, Player) or not this.IsInPlay():
            return
        porteur = this.bind_face
        candidats = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect)
                     if f is not None and f is not porteur and f.card.IsOnField()]
        if not candidats:
            return
        cible = joueur.MayChooseFace(candidats, effect)
        if cible is not None:
            this.AttachTo2(cible, effect)

    def programmer_apres_usage(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart|Message.WhenUnitWouldDefend') -> None:
        # « After this use » : les trois fins d'usage que le moteur emet, et
        # le filtre par lequel il retrouve LUI-MEME l'usage d'origine
        # (`Effect.SetDestroyedAfter`, effect.py:283-335) :
        #   attaque -> AfterUnitAttackEnd, `would_atk_messages` ;
        #   contre  -> AfterUnitThwartEnd, `would_thw_messages` ;
        #   defense -> AfterUnitAttackEnd aussi, via `would_atk_message`.
        this = effect.this.CastTo(Upgrade)
        if isinstance(message, Message.WhenUnitWouldThwart):
            fin = AbilityFactory.AfterUnitThwartEnd(
                AbilityType.Temp0,
                None,
                apres_usage,
                conditions=[
                    lambda effect2, message2:
                        message in message2.would_thw_messages,
                ],
            )
        else:
            attaque = message if isinstance(message, Message.WhenUnitWouldAttack) else message.would_atk_message
            fin = AbilityFactory.AfterUnitAttackEnd(
                AbilityType.Temp0,
                None,
                apres_usage,
                conditions=[
                    lambda effect2, message2:
                        attaque in message2.would_atk_messages,
                ],
            )
        this.effect.RegisterTemp(
            fin,
            unregister_after_exec=True,
            until_phase_end=True,
        )

    def gator_aid_attaque_ou_contre(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        if isinstance(message, Message.WhenUnitWouldAttack):
            message.GainATKForThisAttack(1, effect)
        else:
            message.GainTHWForThisThwart(1, effect)
        programmer_apres_usage(effect, message)

    def gator_aid_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        message.GainDEFForThisAttack(1, effect)
        programmer_apres_usage(effect, message)

    return [
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.Interrupt,
            "AttachedCharacter",
            gator_aid_attaque_ou_contre,
            is_basic_power=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "AttachedCharacter",
            gator_aid_defense,
            is_basic_defense=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
