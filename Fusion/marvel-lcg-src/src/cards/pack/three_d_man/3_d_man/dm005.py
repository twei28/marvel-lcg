from . import *

# Triple the Effectiveness — EVENEMENT. DEFENSE. SKILL. Cout 3, [energy].
# Hero Interrupt (defense): When you would take damage from an enemy attack,
#   reduce the amount taken by 3. Remove 3 threat from a scheme. Deal 3
#   damage to an enemy. If you reduced this card's cost, stun an enemy.
#
# CARTES DE REFERENCE
#  - « reduce the amount taken by X » (defense) : **`sm010`** Hyper-Agility /
#    **`as020`** Double Defense : `WhenUnitWouldTakeDamage(.., is_from_attack
#    =True)` + `message.ReduceDamage(X, effect)` (PAS `PreventDamage` :
#    « reduce » soustrait, « prevent » annule tout).
#  - « deal X damage to an enemy AND remove X threat from a scheme », deux
#    cibles de types differents dans la meme carte : **`sj011`** Unravel —
#    `.SetTarget(Enemy).SetTarget2(Scheme2)`, `effect.targets` /
#    `effect.targets2`.
#  - « carte jouee en defense » (Hero Interrupt, label 'defense') : modele
#    **`bw005`** Calculated Defense (`SetPlay().SetLabel('defense')`,
#    declenche sur l'attaque en cours).
#  - « If you reduced this card's cost, stun AN enemy » : cible libre,
#    DIFFERENTE de celle deja endommagee (« an enemy », pas « that enemy ») :
#    choix interactif `joueur.AskChooseFace(Worlds.GetOnFieldEnemies(effect),
#    effect, ..)`, modele deja use par ce pack (dm015). `CoutReduit` : helper
#    du pack.
#
# TEXTE CONTRE CODE
#  « When YOU would take damage FROM AN ENEMY ATTACK » : l'identite du
#  joueur, uniquement les degats d'attaque (`is_from_attack=True`), pas les
#  degats indirects. « reduce the amount taken by 3 » : soustraction, pas une
#  prevention totale. « a scheme »/« an enemy » : principale ou annexe, et
#  n'importe quel ennemi, cibles independantes l'une de l'autre et du
#  declencheur. « stun AN enemy » (bonus) : peut viser un ennemi different de
#  celui deja frappe, ou le meme si un seul est en jeu.


def GetAbilities() -> Sequence['Ability']:

    def triple_the_effectiveness(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        message.ReduceDamage(3, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 3, effect)
        this.DealDamage(effect.targets, 3, effect)

        if CoutReduit(effect):
            ennemis = Worlds.GetOnFieldEnemies(effect)
            if ennemis:
                cible = joueur.AskChooseFace(ennemis, effect, prompt="Stun an enemy")
                if cible is not None:
                    Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            triple_the_effectiveness,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
