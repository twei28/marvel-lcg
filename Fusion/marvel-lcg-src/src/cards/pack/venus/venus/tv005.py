from . import *

# Eldritch Lance — EVENEMENT, cout 4, [wild]. ATTACK. SUPERPOWER. x1.
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains overkill. Draw 1 card
#   for each [wild] resource used to pay for this card.
#
# CARTES DE REFERENCE
#  - `td006` Singularity : `heros.DealDamage(cibles, N, effect, property=AttackProperty(overkill=True))`.
#  - `tr006` Unbridled Fury : `effect.GetPaidResources()` lu apres paiement.
#  - docs/reference/mots-cles/overkill.md.
#
# TEXTE CONTRE CODE
#  ⚠ « for each [WILD] resource used to PAY for this card » -> `GetPaidResources().g` : les
#    ressources JOKER depensees (une ressource physique/mentale/energie d'une carte
#    imprimee [wild] compte ; une carte [physical] non). Compte, pas simple presence.
#    DECISION UTILISATEUR (16/10/2026) : seulement les wild NECESSAIRES au cout :
#    min(wild payees, cout paye `context.paid_this_cost.true_val`), jamais le surplus.
#  ⚠ « This attack gains OVERKILL » -> `AttackProperty(overkill=True)` : l'excedent passe au
#    vilain, jamais d'un ennemi au sien.
#  Icone [wild] du texte verifiee par decoupe (docs/packs/venus_cartes.md).


def GetAbilities() -> Sequence['Ability']:

    def lance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur) or IdentiteDuJoueur(effect, joueur)
        cibles = [t for t in effect.targets if t is not None]
        if heros is not None and cibles:
            heros.DealDamage(cibles, 5, effect, property=AttackProperty(overkill=True))
        if joueur is not None:
            # DECISION UTILISATEUR (16/10/2026, Q3) : seulement les ressources [wild]
            # NECESSAIRES au cout ; le surplus (ressources payees au-dela du cout)
            # ne compte pas, la pioche ne depasse donc jamais le cout de la carte.
            jokers = min(int(effect.GetPaidResources().g),
                         int(effect.context.paid_this_cost.true_val))
            if jokers > 0:
                joueur.DrawUp(jokers, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lance,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
