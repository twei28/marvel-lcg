from . import *

# hs105 * Kraven The Hunter
# When Revealed : cherche Tooth Necklace (paquet et defausse de rencontre) et le revele.
# Forced Interrupt : piege distribue et revele (limite 1 par ronde et par joueur).

def GetAbilities() -> Sequence['Ability']:

    def collier(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(
            effect, message.GetToPlayer(),
            finder=CardFinder(name="Tooth Necklace", card_type=Attachment,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )

    return [AbilityFactory.WhenThisRevealed(None, collier), PiegeSurAttaque(1, True)]
