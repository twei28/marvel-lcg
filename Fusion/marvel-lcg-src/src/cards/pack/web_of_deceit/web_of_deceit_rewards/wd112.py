from . import *

# Great Web Strand

def GetAbilities() -> Sequence['Ability']:

    def changement(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        # « Hero Response: After you change form, discard Great Web Strand →
        # search your deck and discard pile for a WEB-WARRIOR ally or an ally
        # with “Spider” in its title and add it to your hand. »
        #
        # Deux familles, une seule recherche : `check_face_fn` sait dire l'une OU
        # l'autre la ou `trait=` seul ne saurait dire que la premiere.
        this = effect.this.CastTo(Support)
        joueur = effect.GetInitiator()
        Faces.DiscardAll([this], effect)

        def convient(face: 'CardFace') -> bool:
            return face.HasTrait("WEB-WARRIOR") or "Spider" in face.paper.name

        ChercherEtPrendreEnMain(
            effect, joueur, card_type=Ally, check_face_fn=convient)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "YourIdentity",
            changement
        ),
    ]
