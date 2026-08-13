from . import *

# Heightened Threat (1A)

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        player = Worlds.GetFirstPlayer(effect)

        # « Find the What Goes Around... environment and put side A into play
        # (side B instead for expert mode). » Les deux faces sont mises de cote
        # par le scenario ; on prend celle du mode joue.
        face_voulue = "sp006b" if Worlds.IsExpert(effect) else "sp006a"
        environnement = Worlds.AsideDeck(effect).FindCard(card_ids=[face_voulue])
        if environnement:
            environnement.PutIntoPlay(player, effect)

        # « The first player seeks a Spot card with the Threat Level keyword
        # and reveals it. »
        Find.FindAndReveal(
            effect,
            player,
            finder=CardFinder(card_ids=CARTES_A_NIVEAU)
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place
        ),
    ]
