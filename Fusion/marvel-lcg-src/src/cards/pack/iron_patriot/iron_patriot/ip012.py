from . import *

# Repulsor Bombard — EVENEMENT, cout 1, RES [energy]. ATTACK. x2.
# Hero Action (attack): Deal 2 damage to an enemy and discard the top card from
#   the REGISTERED deck. For each boost icon discarded this way, deal 1 damage
#   to an enemy.
#
# CARTE DE REFERENCE
#  - `vz032` / `01080` pour la forme generale ; ici l'originalite est de lire
#    les ICONES DE BOOST d'une carte DEFAUSSEE, ce que `IconesDeBoostDe` fait
#    deja pour le recrutement.
#
# TEXTE CONTRE CODE
#  ⚠ Les degats supplementaires visent « AN enemy », pas « that enemy » : la
#    seconde salve peut aller ailleurs, et se repartir. On rouvre donc un
#    choix par icone.
#  ⚠ Le prix se lit AVANT la defausse : une fois la carte partie, sa face n'est
#    plus interrogeable de la meme facon.
#  ⚠ Deck REGISTERED vide : rien n'est defausse, aucun degat supplementaire.
#    Les 2 degats de base tombent quand meme.


def GetAbilities() -> Sequence['Ability']:

    def bombardement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect)
        if joueur is None:
            return

        deck = DeckRegistered(joueur)
        dessus = deck.GetTop()
        if dessus is None:
            return
        icones = IconesDeBoostDe(dessus)
        # ⚠ `Faces.DiscardAll` et NON `joueur.DiscardDeckTopCards` : cette
        # derniere ne connait que le deck du JOUEUR. Ici la carte part du deck
        # REGISTERED, et sa defausse propre est celle que `ip001b` a branchee.
        Faces.DiscardAll([dessus], effect)

        for _ in range(icones):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 1 damage to an enemy",
                    lambda cibles: this.DealDamage(cibles, 1, effect),
                ).SetLabel('attack').SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            bombardement,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
