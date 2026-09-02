from . import *

# Nihilistic Vision — COMPLOT ANNEXE. Seuil 2 par joueur, 2 icones de boost.
#
# When Revealed: Discard cards from the top of the encounter deck until an
#   attachment is discarded. Reveal that card.
# All NECROVERSE enemies (including Gorr the God Butcher) get +1 ATK.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Discard from the top of the encounter deck until ... Reveal that card » :
#   meme brique qu'en gb016, `Worlds.DiscardEncounterCardsUntil` puis
#   `Reveal`. La difference est le filtre : ici N'IMPORTE QUEL attachement.
# - Bonus continu donne par un complot annexe en jeu : 50090b (Alert Level),
#   `GiveKeywordToInPlayWhenApplyThis(CardFinder(...), attack=1)`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « until AN ATTACHMENT is discarded » -> tout attachement, PAS seulement les
#   NECROVERSE : c'est la difference avec Brutal Cunning (gb016), qui exige le
#   trait. Les attachements d'un modulaire etranger comptent donc ici.
# « ALL NECROVERSE ENEMIES (INCLUDING Gorr the God Butcher) » -> la
#   parenthese ne fait que lever un doute : Gorr porte le trait, il est deja
#   dans le lot.
# « get +1 ATK » -> effet CONTINU tant que ce complot est en jeu, il disparait
#   quand il est contre. Il se cumule avec le palier 6 de l'environnement.


def GetAbilities() -> Sequence['Ability']:

    def vision_nihiliste(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        Unused(this)

        joueur = message.GetToPlayer()
        trouve = Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)
        if trouve is not None and joueur:
            trouve.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, vision_nihiliste),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="NECROVERSE", card_type=Enemy),
            attack=1,
        ),
    ]
