from cards.pack import *

# ===========================================================================
# Pack VENOMPOOL — set nemesis « Venompool Nemesis » (vp012-vp016).
#
# Killer Thrill et sa bande de chasseurs de primes alien viennent reprendre le
# symbiote. Le set est construit autour d'ELLE : Coldwar (vp014) et Guzz
# (vp015) gagnent chacun +1 a une statistique tant qu'elle est en jeu, et les
# deux portent le meme [star] Boost qui les renvoie face cachee sur le joueur.
# ===========================================================================


KILLER_THRILL_NAME = "* Killer Thrill"


def RedirigerVersLeJoueur(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
    """[star] Boost : « deal this card to yourself as a facedown encounter card ».

    Repris mot pour mot de bw021 Imperius Rex! (pack brawn), qui porte le meme
    texte et documente le piege : DEPLACER la carte ici ne sert a rien, le
    moteur range une carte de boost APRES la resolution de son effet et ecrase
    le deplacement (mesure du 7/8/2026 : la carte finissait dans `AsideDeck`).
    On detourne donc le rangement A VENIR au lieu de devancer le moteur.
    """
    this = effect.this
    joueur = effect.GetInitiator()
    if not isinstance(joueur, Player):
        return

    def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
        message2.SetToArea(joueur.dealt_encounter_cards)

    this.effect.RegisterTemp(
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.Temp0,
            "This",
            rediriger,
        ),
        unregister_after_exec=False,
        until_round_end=True,
    )
