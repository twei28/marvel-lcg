from . import *

# Hammer Twirl — EVENEMENT, cout 0, [physical]. DEFENSE. x2.
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, exhaust Stormbreaker OR spend 1 resource of any type -> prevent
#   all of that damage. If you paid for this card using Stormbreaker, deal 2
#   damage to your attacker.
#
# ⚠ DEUX CAPACITES `Play` SUR LE MEME EVENEMENT, ET IL FAUT LE DECLARER.
# « exhaust Stormbreaker OR spend 1 resource » sont deux COUTS differents pour
# le meme effet, et un cout est fige a la construction : le « or » devient donc
# le choix entre DEUX capacites. `factory.py` pose alors
# `assert play_count == 2` et exige que le `card_id` figure dans sa liste
# blanche — sans quoi LE DECK NE MONTE AUCUNE PARTIE, et ni `test_cards`, ni
# `test_capacites`, ni `substituer_pack` ne le voient : seul
# `verifier_tous_les_decks` l'attrape (leçon `ls005`, pack lady_sif, dont le
# deck est reste injouable une journee entiere). br004 y a donc ete ajoutee
# AVANT d'ecrire ce fichier.
# Meme motif que `an003` Heven's Fury, `vv005` Solar Beam et `ls005` To Arms!.
#
# CARTES DE REFERENCE
#  - `ma011` Bulletproof Chica et `bk003` Assault Redirection :
#    `WhenUnitWouldTakeDamage` + `message.PreventDamage("All", effect)`.
#  - `dz036` : lire QUELLE carte a paye (helper `MarteauAPaye`).
#
# TEXTE CONTRE CODE
#  ⚠ LES DEUX MOITIES SONT INDEPENDANTES, et c'est le piege de la carte.
#    « exhaust Stormbreaker » est un COUT D'ACTIVATION ; « paid for this card
#    using Stormbreaker » parle du COUT EN RESSOURCES, paye par la capacite
#    `Hero Resource` de br010 (« discard Stormbreaker -> generate [wild][wild]
#    for an event »). On peut donc incliner le marteau SANS declencher les 2
#    degats, et les declencher SANS l'incliner.
#  « from AN ATTACK » -> `is_from_attack=True`.
#  « to YOUR ATTACKER » -> celui qui frappe, lu sur le message.


def GetAbilities() -> Sequence['Ability']:

    def moulinet(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        message.PreventDamage("All", effect)
        if not MarteauAPaye(effect):
            return
        attaquant = getattr(message, "attacker", None)
        if attaquant is not None and attaquant.IsInPlay():
            this.DealDamage([attaquant], 2, effect)

    def defense(cout: 'CostFunc.Base|None', ressources: 'Cost|None') -> 'Ability':
        ability = AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            moulinet,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense')
        if cout is not None:
            ability.SetCostFunc(cout)
        if ressources is not None:
            ability.SetCost(ressources)
        return ability

    return [
        # Branche 1 : on incline le marteau. Gratuite en ressources.
        defense(CostFunc.Exhaust(name=NOM_MARTEAU, card_type=Upgrade,
                                 from_where=["YouControlCards"]), None),
        # Branche 2 : on paie 1 ressource de n'importe quel type. C'est CELLE-CI
        # que br010 peut financer, et donc la seule ou les 2 degats tombent.
        defense(None, Cost("1")),
    ]
