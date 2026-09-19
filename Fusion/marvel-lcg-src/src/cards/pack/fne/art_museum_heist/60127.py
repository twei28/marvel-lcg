from . import *

# Tug of War
# When Revealed: You may spend [physical] x3 resources to move an ART
#   attachment from the villain to your identity. Otherwise, move an ART
#   attachment from an identity to the villain and this card gains surge.
#
# Modele : 50134 Innocent Bystanders (ForChoiceAbilityWithCost) + Otherwise.
# La branche payante n'est offerte que si le vilain porte une oeuvre ET que
# le joueur peut payer (PeutCouvrirLeCout, helper du pack).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def branche_payante_possible(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            # Offerte seulement si le vilain porte une oeuvre ET si les trois
            # [physical] sont couvrables : sinon le moteur ne proposerait
            # qu'elle (Otherwise est masquee tant qu'une autre option existe),
            # le paiement echouerait et rien ne se passerait (constate au
            # harnais, 18/09/2026). ⚠ Le joueur vient de la CLOTURE : le message
            # de choix n'expose pas GetToPlayer (exception avalee -> condition
            # fausse, branche jamais offerte, constate le meme jour).
            vilain = Worlds.FindVillain(effet_choix)
            if vilain is None or not OeuvresSur(vilain):
                return False
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("RRR"))

        def reprendre(targets: Sequence['CardFace'], res: 'Resources') -> None:
            DeplacerUneOeuvreDuVilainVers(effect, joueur, joueur.GetIdentity())

        def sinon(targets: Sequence['CardFace']) -> None:
            DeplacerUneOeuvreVersLeVilain(effect, joueur)
            ThisCardGainSurge(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("RRR"),
                "Spend [physical][physical][physical]: move an Art attachment from the villain to your identity",
                reprendre,
                conditions=[branche_payante_possible],
            ),
            AbilityFactory.Otherwise(sinon),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
