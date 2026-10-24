from . import *

# Special Delivery — EVENEMENT, cout 2, impression 5/15 : ressource(s) imprimee(s) wild. ATTACK. (card_id ch007)
# Hero Action (attack): Deal 3 damage to an enemy. If this is the first event you have played this phase, confuse an enemy.
# Flow: [mental] → if this attack defeats an enemy, play the next ATTACK event from your hand at no cost.
#
# ⚠ IMPRESSIONS : Special Delivery existe en DEUX cartes (ch008) qui ne different que par l'ICONE DE RESSOURCE du coin ;
#   `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).
#
# Cartes de reference :
#  - `nt005` Kickflip : « la carte jouee est DEJA dans `stat.this_*_played_cards` quand son effet se resout » (a exclure).
#  - `mf012` / `05015` : `Faces.GiveStatus(cibles, "Confused", effect)`.
#  - cout differe : `Worlds.UpdateNextCardPlayCost(joueur, 0, effect, update_to=True, finder=..., in_this="Turn")`
#    (`dz003`, `01092`), recette RECETTES-MOTEUR §0 ligne « la prochaine carte que tu joues ».
#
# ⚠ Mots-pieges :
#  - « the FIRST event you have played this phase » : les evenements deja joues cette phase par CE joueur, hors cette carte.
#  - « confuse AN enemy » : un ennemi au choix (autre cible que l'attaque possible), seulement si c'est le premier evenement.
#  - Flow [mental] : exige un mental imprime sur la carte du dessus ; « if this attack DEFEATS an enemy » : la cible de l'attaque
#    doit avoir ete VAINCUE (plus en jeu) apres les 3 degats ; sinon rien (le Flow est tout de meme resolu : Chi Mastery).
#  - DECISION UTILISATEUR (24/10/2026) : « play the next ATTACK event » = COUT DIFFERE : le prochain evenement ATTACK que le
#    joueur JOUE ce tour coute 0 ; il garde le choix et l'ordre. Fenetre « ce tour ».


def GetAbilities() -> Sequence['Ability']:

    def special_delivery(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        cible = effect.targets[0] if effect.targets else None
        this.DealDamage([t for t in effect.targets if t is not None], 3, effect)
        if joueur is None:
            return

        deja_jouees = [f for f in joueur.stat.this_phase_played_cards if Event.IsType(f) and f is not this]
        if not deja_jouees:
            def desorienter(cibles: Sequence['CardFace']) -> None:
                Faces.GiveStatus([c for c in cibles if c is not None], "Confused", effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Confuse an enemy", desorienter).SetTarget(Enemy, canbe_confused=True),
            )

        if AccepterFlow(effect, joueur, "B"):
            if cible is not None and not cible.IsInPlay():
                Worlds.UpdateNextCardPlayCost(
                    joueur, 0, effect,
                    update_to=True,
                    finder=CardFinder(card_type=Event, traits=["ATTACK"]),
                    in_this="Turn",
                )
            FlowResolu(joueur, this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            special_delivery,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
