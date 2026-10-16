from . import *

# Clan of Shadows (1A) — COMPLOT PRINCIPAL, face A.
# Content: Shredder (I) and Shredder (II). (Shredder (II) and Shredder (III) for
#   expert mode.) Shredder, Shadow of the Foot, and Standard sets. Two modular
#   encounter sets (Chunin and Foot Goon Squad).   <- texte de mise en place, vit
#   dans data/scenarios/shredder*.json
# Setup: Each player searches the encounter deck for a FOOT CLAN minion and
#   reveals it.
#
# Cartes de reference : `sp001a` (Heightened Threat : `WhenCardSetup("This", op)`
# sur une face A, puis `Find.FindAndReveal` pour « searches ... and reveals it »),
# `fne 60161a` (« Each player ... » a la mise en place), `Players.ForEachPlayer`
# (kang's wrath 11013b) pour « each player ».
#
# Mots-pieges : « EACH player » (pas seulement le premier) ; « searches the
# encounter deck » SEULEMENT (pas la defausse : a la mise en place elle est
# vide de toute facon) ; « FOOT CLAN minion » = type sbire ET trait.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        def chercher(joueur: 'Player') -> None:
            face = Search.EncounterCard(
                effect, joueur,
                include_discard_pile=False,
                card_type=Minion,
                trait="FOOT CLAN",
            )
            if face:
                face.Reveal(joueur, effect)

        Players.ForEachPlayer(effect, chercher)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
