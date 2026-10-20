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


def CapacitesAttuma() -> List['Ability']:
    """Stades I et II (gs170/gs171), texte identique hors Toughness (native, desc.Toughness, stade II
    seulement) : « [star] While another ATLANTIS card is in play, Attuma gets +1 SCH and +1 ATK. »"""
    def autre_atlantis(effect: 'Effect', ui: List['CardFace']) -> int:
        autres = [f for f in Worlds.FindCardsOnField(effect, CardFinder(trait="ATLANTIS")) if f is not effect.this]
        if autres:
            ui.append(autres[0])
            return 1
        return 0

    return [
        AbilityFactory.ThisGainKeyword(
            autre_atlantis, attack=1, scheme=1,
            change_on_event=OnEvent.CardInPlay(CardFinder(trait="ATLANTIS")),
        ),
    ]


def ExcesVersMenaceSurManigancePrincipale(effect: 'Effect', exces: int) -> None:
    """« Excess damage ... is placed as threat on the main scheme. » Partage par gs176/gs177 Destroyer
    (capacite constante) et gs179/gs180 (Boost « if this attack deals excess damage »)."""
    if exces <= 0:
        return
    complot = Worlds.FindMainScheme(effect)
    if complot is not None:
        complot.PlaceThreatOnSchemes([complot], exces, effect)


def CapacitesDestroyer() -> List['Ability']:
    """Stades I et II (gs176/gs177), texte identique hors Toughness : « [star] Excess damage dealt by
    Destroyer's attacks is placed as threat on the main scheme. »"""
    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        ExcesVersMenaceSurManigancePrincipale(effect, message.excess_damage)

    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", Unit2, apres_attaque),
    ]


def CapacitesDoctorMinerva() -> List['Ability']:
    """Stades I et II (gs181/gs182), texte identique hors Toughness. Texte imprime « Forces Response »
    (faute d'impression, sans « d » : transcrit tel quel sur les deux stades) : « After Doctor Minerva
    schemes against you, deal yourself a facedown encounter card. »"""
    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
    ]


def UneAutreCarteAtlantisEstEnJeu(effect: 'Effect', ui: 'List[CardFace]') -> int:
    """« While/for each ATLANTIS card is in play » hors This : partage par gs174 Andromeda et gs175 Rising
    Sea Levels."""
    autres = [f for f in Worlds.FindCardsOnField(effect, CardFinder(trait="ATLANTIS")) if f is not effect.this]
    if autres:
        ui.append(autres[0])
        return 1
    return 0
