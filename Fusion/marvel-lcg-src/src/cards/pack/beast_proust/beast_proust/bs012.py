from . import *

# Tech Genius : RESSOURCE [wild]. x2.
# Hero Response: After you spend this card, search your deck or discard pile for a TECH upgrade and tuck it under Beast's Lab.
#
# CARTES DE REFERENCE
#  - `dz018` Sound Absorption : `AbilityFactory.AfterYouSpendThisCard(Response, op)` (la carte est deja a la defausse quand la Reponse part ; `NoOutOfPlayLimit` natif).
#  - `bs009` (meme set) : `ChercherTechEtGlisser`.
#
# TEXTE CONTRE CODE
#  « Hero RESPONSE » : sous-type dedie `HeroResponse` (forme heros). « After you SPEND this card » : depense en paiement (pas « play »). « deck OR discard pile » : les deux. « tuck it under Beast's Lab » : sous le Lab, visible
#    (rien ne se passe sans Lab en jeu : la recherche n'est pas ouverte).
#  Chiffres : aucun.


def GetAbilities() -> Sequence['Ability']:

    def lab_en_jeu(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and LabDe(joueur) is not None

    def genie_de_la_tech(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        Unused(message)
        ChercherTechEtGlisser(effect.GetInitiator(), effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            genie_de_la_tech,
            conditions=[lab_en_jeu],
        ),
    ]
