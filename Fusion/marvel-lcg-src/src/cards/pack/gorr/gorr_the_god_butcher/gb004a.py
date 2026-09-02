from . import *

# Deicide 1A — COMPLOT PRINCIPAL, face de mise en place.
#
# Setup: Set the Necroverse modular encounter set, the Necro-Raven Gestalt
#   minion, the double-sided Godbomb environment, and all copies of Heroes'
#   Labor and Stalking Berserker aside, out of play. Advance to stage 1B.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Setup d'un complot principal : 50087a (Batroc), `WhenCardSetup` +
#   `SetupCards.SetAsideCards`. Meme forme ici, en plusieurs passes.
# - « Advance to stage 1B » : AUCUN code. Une face A sans `TargetThreat` est
#   avancee toute seule par le moteur a la revelation
#   (scheme_main.py:65-73). Ecrire un `Advance` ici la ferait avancer DEUX
#   fois et sauterait le stade 1B.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « the Necroverse MODULAR ENCOUNTER SET » -> ⚠ un set modulaire EXTERNE au
#   pack, pas un sous-ensemble des 34 cartes (toutes portent « GORR THE GOD
#   BUTCHER (x/34) » en pied, aucune ne se reclame d'un autre set). Il s'agit
#   de « Necroverse [1.5] » du meme auteur, PAS ENCORE PORTE (02/09/2026,
#   dossier Drive fourni par l'utilisateur). La recherche par `set_name` ne
#   trouve donc rien pour l'instant et ne fait rien : le jour ou le set sera
#   porte sous ce `set_name`, le Setup et le complot 3A fonctionneront sans
#   changer une ligne.
# « the double-sided Godbomb environment » -> UNE carte a deux faces
#   (« gb007a,gb007b »), declaree dans le `set_aside` du scenario : le moteur
#   la cree deja hors jeu, il n'y a donc rien a mettre de cote. Idem pour le
#   sbire Necro-Raven Gestalt. On les cherche quand meme par securite : si un
#   flux les avait posees en jeu, elles doivent en sortir.
# « ALL COPIES of Heroes' Labor and Stalking Berserker » -> les 4+4
#   exemplaires. Ils ne sont PAS dans le deck de rencontre : ce sont des
#   cartes a dos joueur, creees dans les decks des joueurs par les complots
#   2A et 3A (voir gb005a / gb006a). Rien a mettre de cote non plus, mais la
#   meme securite s'applique.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        # Le set modulaire part du deck de rencontre vers la reserve.
        SetupCards.SetAsideCards(effect, set_name="Necroverse")

        # Ceintures et bretelles : ces trois-la vivent deja hors jeu (le
        # `set_aside` du scenario pour l'environnement et le Gestalt, les
        # decks des joueurs pour les deux cartes a dos joueur). L'appel ne
        # trouve normalement rien ; il garantit le texte si un autre flux les
        # avait fait entrer.
        SetupCards.SetAsideCards(effect, card_ids=["gb007a", "gb007b", "gb008",
                                                    "gb021", "gb022"])

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
    ]
