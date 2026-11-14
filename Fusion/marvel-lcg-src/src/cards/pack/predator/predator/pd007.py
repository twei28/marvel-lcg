from . import *

# Savage Skewer — EVENEMENT, cout 2, [physical]. ATTACK. TACTIC. x2.
# Hero Action (attack): Deal 5 damage to an enemy. You may discard a cloaked status card to either stun and confuse that
#   enemy or discard an attachment on that enemy with the text "Hero Action" or "Hero Response".
#
# Cartes de reference :
#  - `core/01053` Relentless Assault : degats d'attaque d'un evenement ; `rainy/rescue_rainy/90116` Magnetic Restraints :
#    « stun » / « discard an attachment with Hero Action or Hero Response » (`Players.DiscardHeroActionAttachment`) ;
#  - `Player.MayChooseOneAbility(effect, A, B)` : les deux branches + « Cancel » (« you MAY »).
#
# ⚠ Mots-pieges :
#  - « discard A cloaked status card » : DECISION UTILISATEUR (25/10/2026) = celle de PREDATOR seulement. Pas de carte Cloaked
#    sur Predator : l'option n'est pas offerte et seuls les 5 degats partent.
#  - « to EITHER stun and confuse OR discard an attachment » : une seule des deux branches ; « stun AND confuse » = les deux statuts.
#  - « that enemy » : celui qui vient de recevoir les degats ; il peut etre mort (aucune option alors).
#  - « an attachment on that enemy with the text Hero Action or Hero Response » : attachement de RENCONTRE (type Attachment),
#    pas une amelioration (Infralocked est une Upgrade) ; branche non offerte sans cible valide.


def GetAbilities() -> Sequence['Ability']:

    def embrocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not effect.targets:
            return
        cible = effect.targets[0]
        joueur.GetHero().DealDamage(effect.targets, 5, effect, property=AttackProperty())
        heros = HerosDuJoueur(joueur)
        if heros is None or not heros.IsCloaked() or not cible.card.IsOnField():
            return

        def payer() -> None:
            heros.DiscardCloaked(effect, rule=1)

        def etourdir_et_desorienter(cibles: Sequence['CardFace']) -> None:
            payer()
            Faces.GiveStatus(list(cibles), "Stunned", effect)
            Faces.GiveStatus(list(cibles), "Confused", effect)

        def defausser_attachement(cibles: Sequence['CardFace']) -> None:
            payer()
            Players.DiscardHeroActionAttachment(joueur, list(cibles), effect, may=False)

        options = [
            AbilityFactory.ForChoiceAbility("Discard a cloaked status card: stun and confuse that enemy",
                                            etourdir_et_desorienter).SetTarget([cible], range=(1, 1), not_move=True),
        ]
        if cible.GetInventoryDeck().FindCard(with_texts=["Hero Action", "Hero Response"]) is not None:
            options.append(
                AbilityFactory.ForChoiceAbility('Discard a cloaked status card: discard an attachment with "Hero Action" or "Hero Response"',
                                                defausser_attachement).SetTarget([cible], range=(1, 1), not_move=True))
        joueur.MayChooseOneAbility(effect, *options)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            embrocher,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
