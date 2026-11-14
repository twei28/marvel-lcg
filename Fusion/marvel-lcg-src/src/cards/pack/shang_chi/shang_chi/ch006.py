from . import *

# Roundhouse Kick — EVENEMENT, cout 0, impression 4/15 : ressource(s) imprimee(s) physique + energie. ATTACK. (card_id ch006)
# Hero Action (attack): Deal 1 damage to an enemy.
# Flow (attack): [physical] → deal 2 damage to an enemy.
#
# ⚠ IMPRESSIONS : Roundhouse Kick existe en DEUX cartes (ch005) qui ne different que par l'ICONE DE RESSOURCE du coin ;
#   `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).
#
# Cartes de reference :
#  - `64004` Fists of Fury : deux phrases « Deal N damage to an enemy » = deux choix de cible INDEPENDANTS
#    (`SetTarget(Enemy)` pour le premier, `ChooseAbilities(ForChoiceAbility(...).SetTarget(Enemy))` pour le suivant).
#
# ⚠ Mots-pieges :
#  - « an enemy » deux fois : la 2e cible se choisit a part (peut etre la meme si elle survit).
#  - Flow [physical] : la carte du dessus doit IMPRIMER un poing ; « (attack) » : ses 2 degats sont une attaque (`DealDamage`
#    depuis l'evenement, label deja pose sur le Hero Action).
#  - les 2 degats s'AJOUTENT au 1 : jamais 2 a la place de 1.


def GetAbilities() -> Sequence['Ability']:

    def roundhouse_kick(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)
        if joueur is None or not AccepterFlow(effect, joueur, "R"):
            return

        def frapper(cibles: Sequence['CardFace']) -> None:
            this.DealDamage([c for c in cibles if c is not None], 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 2 damage to an enemy", frapper).SetTarget(Enemy),
        )
        FlowResolu(joueur, this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            roundhouse_kick,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
