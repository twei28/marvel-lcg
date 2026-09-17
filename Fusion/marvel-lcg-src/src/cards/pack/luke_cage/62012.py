from . import *
def GetAbilities() -> Sequence['Ability']:
    def iron_fist(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Ally)
        # ⚠ UN BUDGET POUR L'ATTAQUE ENTIERE, PAS PAR PAQUET DE DEGATS
        # (17/09/2026). La carte dit « prevent damage from that attack equal to
        # Iron Fist's ATK » : deux degats en tout, une fois.
        #
        # Signale en partie par un joueur face a l'Homme-Sable, dont l'attaque
        # inflige des degats INDIRECTS : le joueur les repartit, donc le moteur
        # envoie PLUSIEURS paquets pour une meme attaque. La prevention se
        # rejouait a chacun. Son journal, round 2 : attaque a 2 plus un boost a
        # 2, donc quatre degats, et « Prevented 2 » DEUX FOIS — sur Iron Fist
        # puis sur l'identite. Les quatre etaient absorbes au lieu de deux.
        #
        # On retient donc ce qui reste a prevenir, et on ne demande jamais plus
        # que ce que le paquet vaut : sans ce plafond, un paquet de 1 mangerait
        # les deux points du budget.
        restant = [this.attack]
        def prevent(inner_effect: 'Effect', damage_message: 'Message.WhenUnitWouldTakeDamage') -> None:
            if restant[0] <= 0:
                return
            a_prevenir = min(restant[0], damage_message.will_take_damage)
            if a_prevenir <= 0:
                return
            restant[0] -= damage_message.PreventDamage(a_prevenir, effect)
        effect.this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                None,
                prevent,
                is_from_attack=message.would_atk_message,
            ),
            unregister_after_exec=False,
            until_event_end=message.would_atk_message,
        )
    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(AbilityType.Interrupt, "This", iron_fist),
    ]
