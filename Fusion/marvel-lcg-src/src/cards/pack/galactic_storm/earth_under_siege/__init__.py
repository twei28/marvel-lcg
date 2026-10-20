from cards.pack import *

# ===========================================================================
# Scenario EARTH UNDER SIEGE (Galactic Storm, Kajislav) — helpers partages
# (gs161-gs194, gsr01-gsr10). Livret 1.2 p.16, « Scenario 4 : Earth Under
# Siege », encart « Multiple Villains » / « Villains Activation ».
#
# Regle propre : JUSQU'A 6 MECHANTS EN JEU SIMULTANEMENT (Annihilus, Attuma,
# Destroyer, Doctor Minerva, Mole Man, Veranke), brique commune du 20/10/2026
# (`src/game/operate/villains.py`, fiche `mots-cles/mechants-multiples.md`) :
# PREMIERE carte de campagne a la cabler. Regle posee a la mise en place
# (gs161a) : `the_villain="Leftmost"`, `player_cards="PlayerChooses"`.
#
#  - « deck de mechants » (Villains.BuildVillainDeck / RevealNextVillain) :
#    DISTINCT du deck de STADES normal (`Scenario.villain_deck`, jamais
#    utilise ici — la composition du scenario (`data/scenarios/
#    gs_earth_under_siege*.json`) laisse `"villain": []`, donc la mise en
#    place automatique du moteur (placer scenario.villain_deck[0]) ne fait
#    rien : gs161a construit et revele le deck de mechants lui-meme).
#  - Les 6 cartes de stade (une par mechant selon la difficulte) ET leurs
#    ensembles de rencontre (ex. Annihilus : gs166/167 + gs168/169) naissent
#    MIS DE COTE (`data/scenarios/gs_earth_under_siege*.json`, cle
#    `set_aside`), `desc.set_name` = nom du mechant (« Annihilus », pas
#    « Earth Under Siege ») pour pouvoir retrouver « le reste » de son
#    ensemble (`CardFinder(set_name=...)`) une fois le mechant revele.
#  - Compteur maison 'safety' (CardFace.COUNTER) : jetons de SECURITE
#    d'Earthfall (gs161a/b), retires Apres chaque phase du mechant ; sous le
#    nombre de cartes du deck de mechants, un nouveau mechant est revele
#    (gs161b). Enemies at Large (gs162a/b) en REPOSE 1 des qu'elle est
#    videe de sa menace, et gere la revelation finale/victoire quand le
#    DERNIER mechant en jeu est vaincu.
# ===========================================================================

NOMS_MECHANTS = ("Annihilus", "Attuma", "Destroyer", "Doctor Minerva", "Mole Man", "Veranke")


def RevelerProchainMechantEtMelangerLeReste(effect: 'Effect', player: 'Player') -> 'Villain|None':
    """« Reveal the top card of the villain deck and shuffle the rest of its
    encounter set into the encounter deck. » Partage par la mise en place
    (gs161a) et par le tic de securite (gs161b) et Enemies at Large
    (gs162a/b). Rend le mechant revele, ou None si le deck de mechants est
    vide."""
    mechant = Villains.RevealNextVillain(player, effect)
    if mechant is not None:
        reste = Worlds.GetSetAsideAreaCards(effect, CardFinder(set_name=mechant.name))
        if reste:
            Faces.ShuffleAllTo(reste, "EncounterDeck", effect)
    return mechant


def DefausserJusquaCarteIdentitaire(effect: 'Effect', joueur: 'Player') -> 'Tuple[CardFace|None, Sequence[CardFace]]':
    """« Discard cards from the top of your deck until you discard an
    identity-specific card. » Partage par gs166/gs167 Annihilus (Forced
    Response) et gs169 Annihilation Wave (When Revealed). Rend (carte
    identitaire trouvee ou None si le deck s'est vide avant, autres cartes
    defaussees au passage). Modele `Worlds.DiscardEncounterCardsUntil`
    (`deck.DiscardUntil`, deja generique : fonctionne sur N'IMPORTE QUEL
    deck, pas seulement le deck de rencontre)."""
    return joueur.player_deck.DiscardUntil(
        effect, name=None, trait=None, card_type=CardFace, card_class="IdentitySpecific")


def CapacitesAnnihilus() -> List['Ability']:
    """Stades I et II (gs166/gs167), texte identique hors Toughness (native, desc.Toughness, stade II
    seulement) : « Forced Response: After Annihilus activates against you, discard cards from the top of
    your deck until you discard an identity-specific card. »"""
    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        Unused(message)
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            DefausserJusquaCarteIdentitaire(effect, joueur)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(AbilityType.ForcedResponse, "This", apres_activation),
    ]
