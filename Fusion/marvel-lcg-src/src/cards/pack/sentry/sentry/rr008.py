from . import *

# Pacifying Presence : AMELIORATION (CONDITION. SPLIT. SUPERPOWER.), cout 1, [physical]. Classe Hero.
# Hero Interrupt: When a friendly character would be dealt any amount of damage, discard this card → prevent all of that damage. Then, heal damage from among characters equal to that damage.
# Special: Heal 2 [per_hero] from Void. Other enemies cannot activate this round.
#
# CARTES DE REFERENCE
#  - « When X would be dealt damage ... prevent all » : `WhenUnitWouldTakeDamage(HeroInterrupt, None, op, conditions=[..])` + `message.PreventDamage("All", effect)` (sender_damage.py:665) ; coût `CostFunc.Discard("This")`.
#  - Soin : `this.HealthUnits([cible], 1, effect)` ; dégâts d'une carte : `carte.sustained`.
#  - « cannot activate this round » : `this.effect.RegisterTemp(WhenEnemyWouldActivate(Temp0, ..), unregister_after_exec=False, until_round_end=True)` + `message.SetBeInstead(effect)` (RECETTES §26 Specials / `rz018`).
#
# TEXTE CONTRE CODE
#  « friendly character » : identite et allies des joueurs. « Then, heal damage FROM AMONG characters EQUAL TO THAT DAMAGE » : autant de points de soin que de degats empeches, repartis un par un entre les personnages blesses au choix
#  du joueur. « Heal 2 PER HERO from Void » : 2 x nombre de joueurs. « Other enemies cannot activate THIS ROUND » : tous les ennemis sauf le Void, jusqu'a la fin du round. Chiffres : cout 1.


def GetAbilities() -> Sequence['Ability']:

    def amie(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        cible = message.trigger
        return message.will_take_damage > 0 and (Hero.IsType(cible) or AlterEgo.IsType(cible) or Ally.IsType(cible))

    def proteger_et_soigner(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        degats = message.will_take_damage
        message.PreventDamage("All", effect)
        if joueur is None:
            return
        for _ in range(degats):
            blesses = [f for f in PersonnagesDuJoueur(joueur) if f.sustained > 0]
            if not blesses:
                break
            choisi = joueur.AskChooseFace(blesses, effect, not_move=True)
            if choisi is None:
                break
            this.HealthUnits([choisi], 1, effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        this = effect.this
        void = VoidEnJeu(effect)
        if void is not None:
            this.HealthUnits([void], 2 * len(effect.world.const_players), effect)

        def pas_d_activation(e: 'Effect', m: 'Message.WhenEnemyWouldActivate') -> None:
            m.SetBeInstead(e)

        this.effect.RegisterTemp(
            AbilityFactory.WhenEnemyWouldActivate(
                AbilityType.Temp0,
                CardFinder(card_type=Enemy),
                pas_d_activation,
                conditions=[lambda e, m: m.trigger.paper.name.lstrip("* ") != NOM_VOID],
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            proteger_et_soigner,
            conditions=[amie],
        ).SetCostFunc(CostFunc.Discard("This")),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
