from cards.pack import *

# Helpers partages du set « Lyja » (Kajislav, Skrull Menace).
#
# Tout le kit tourne autour des cartes « TREACHERY » : huit evenements joueur
# portent le trait TREACHERY, se melangent dans le deck RENCONTRE (« Hero
# Action: Shuffle this card into the encounter deck ») et s'y comportent comme
# des traitrises (When Revealed, Boost). Decisions de l'utilisateur
# (15/10/2026) :
#  - « TREACHERY card » = une carte de TYPE Treachery (traitrise de rencontre)
#    OU portant le trait TREACHERY (les evenements de Lyja) ;
#  - « The Lyja player » = le PROPRIETAIRE de la carte ;
#  - une carte joueur defaussee depuis le deck rencontre va dans la defausse de
#    son proprietaire (Event.OnWhenCardRevealed, event.py).


def EstTraitrise(face: 'CardFace') -> bool:
    """« a TREACHERY card » : type Treachery OU trait TREACHERY."""
    return Treachery.IsType(face) or face.HasTrait("TREACHERY")


def FinderTraitrise() -> 'CardFinder':
    return CardFinder(check_face_fn=EstTraitrise)


def TraitrisesDuDeckRencontre(effect: 'Effect') -> List['CardFace']:
    """Les traitrises que contient le deck rencontre (face cachee comprise)."""
    return list(FinderTraitrise().Checks(Worlds.GetEncounterDeckCards(effect)))


def ChercherTraitrisesRencontre(effect: 'Effect', joueur: 'Player', nombre: int) -> List['CardFace']:
    """« Search the encounter deck for N TREACHERY card(s) ».

    Le joueur designe les cartes ; s'il y en a moins que `nombre`, il prend
    toutes celles qui existent. Les cartes trouvees sortent du deck (zone de
    traitement) et le deck est melange par la recherche elle-meme
    (`SelectorEnd.DoShuffle`). Rien trouve : on melange quand meme, la
    recherche a eu lieu. L'appelant CONSOMME les cartes (defausse ou dessus du
    deck) : une carte laissee en zone de traitement serait perdue.
    """
    candidates = TraitrisesDuDeckRencontre(effect)
    n = min(nombre, len(candidates))
    if n <= 0:
        Worlds.GetEncounterDeck(effect).Shuffle(effect)
        return []
    return list(Search.EncounterCards(
        effect, joueur,
        include_discard_pile=False,
        finder=FinderTraitrise(),
        total=n,
    ))


def PoserSurLeDeckRencontre(effect: 'Effect', joueur: 'Player', faces: Sequence['CardFace']) -> None:
    """« Place those cards on the top of the encounter deck (in any order) »."""
    if not faces:
        return
    faces = list(faces)
    Faces.MoveAllToDeck(faces, Worlds.GetEncounterDeck(effect), "Top", effect)
    if len(faces) > 1:
        joueur.PlaceOnTopInAnyOrder(faces, effect)


def ProprietaireLyja(face: 'CardFace', effect: 'Effect') -> 'Player':
    """« The Lyja player » = le proprietaire de la carte (decision du 15/10/2026).

    Repli (carte fabriquee par le scenario, sans proprietaire joueur : cela
    n'arrive qu'aux montages de test) : le joueur dont l'identite est Lyja,
    sinon le premier joueur.
    """
    proprietaire = face.GetOwner()
    if Player.IsType(proprietaire):
        return proprietaire
    for joueur in Worlds.GetPlayers(effect):
        if joueur.GetIdentity().paper.card_id in ("sk037a", "sk037b"):
            return joueur
    return Worlds.GetFirstPlayer(effect)


def MelangerDansLeDeckRencontre() -> 'Ability':
    """« Hero Action: Shuffle this card into the encounter deck. » (les 4 evenements TREACHERY).

    L'evenement se joue (cout 1) puis part dans le deck rencontre : il n'est plus
    en zone de traitement a la fin de sa resolution, `Event.OnAfterPlay` ne le
    defausse donc pas.
    """
    def melanger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, melanger).SetPlay()


def ADesUsagesOuUnTexteDeHeros(face: 'CardFace') -> bool:
    """« an attachment with the uses keyword or the text "Hero Action" or "Hero Response" »."""
    if not Attachment.IsType(face):
        return False
    if getattr(face, "uses_counters", 0):
        return True
    for capacite in face.ability.abilities:
        if capacite.flags.is_hero_action or capacite.flags.is_hero_response:
            return True
    return False
