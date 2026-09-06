from cards.pack import *

# ===========================================================================
# Helpers partages du set « Cameo Compliment » (BlueRiver, set 162, prefixe
# `cc`).
#
# ⚠ CE N'EST PAS UN PACK DE HEROS. Trois cartes d'ASPECT, une par aspect, sans
# identite, sans obligation, sans set nemesis. `PROCESSUS-HEROS.md` ne
# s'applique donc pas : seul `PROCESSUS-CARTE.md`, trois fois.
#
# ⚠ LES TROIS SONT DES CALQUES D'UNE CARTE OFFICIELLE : `58031` Cameo (Meneur,
# imprimee dans le pack wonder_man). Meme texte a un mot pres, meme montage,
# seul le FILTRE change :
#   `58031` officiel  : un ALLIE specifique a une identite
#   `cc001` Justice   : un soutien specifique a une identite, trait LOCATION
#   `cc002` Protection: une amelioration specifique a une identite, trait ARMOR
#   `cc003` Agression : une amelioration specifique a une identite, trait
#                       WEAPON, et NON PERMANENTE
# Le nom du zip, « Cameo compliment », dit exactement cela : le complement de
# Cameo pour les trois autres aspects.
#
# ⚠ « SEARCH YOUR COLLECTION » N'EST PAS UN ECART A ASSUMER. Le moteur sait le
# faire : `CardsDB.papers` porte le catalogue entier, `CardFactory.GenerateCard`
# fabrique une carte qui n'etait dans aucune zone, et `58031` en fait deja la
# demonstration. On recopie SON chemin plutot que la primitive
# `Search.Collection` (search.py:371), pour une raison precise : cette
# primitive appelle `AskChoosePaper`, qui rend un `card_id` sans jamais
# montrer les cartes, alors que `58031` fabrique les faces et appelle
# `AskChooseFace` — la joueuse VOIT ce qu'elle choisit. Sur 70 candidats, la
# difference n'est pas cosmetique.
# ⚠ Le journal de `wd029` Multiverse Recruit assume au contraire un ECART sur
# ce meme texte, faute d'avoir vu l'un ou l'autre de ces deux chemins.
# ===========================================================================

# « Discard 2 cards from your hand » — le nombre est imprime sur les trois.
CARTES_A_DEFAUSSER = 2


def SetsDIdentitesHorsPartie(this: 'CardFace') -> set:
    """Les `set_name` de heros dont AUCUNE identite n'est a la table.

    ⚠ « from an identity NOT IN THIS GAME » : on retire des sets de heros du
    catalogue ceux des identites presentes, TOUTES FACES CONFONDUES
    (`GetAllIdentityFace`) — une identite a trois faces comme Hulk ou
    Invisible Woman ne doit pas passer entre les mailles.

    Montage repris tel quel de `58031`.
    """
    from cards.database import CardsDB

    monde = this.card.world
    en_partie = set()
    for joueur in monde.players:
        for face in joueur.GetAllIdentityFace():
            if face.paper.set_name:
                en_partie.add(face.paper.set_name)
    sets_de_heros = {p.set_name for p in CardsDB.papers.values()
                     if p.type == 'Hero' and p.set_name}
    return sets_de_heros - en_partie


def EstSpecifiqueAUneIdentite(paper: 'Paper') -> bool:
    """« IDENTITY-SPECIFIC » — la carte est liee a UNE identite.

    ⚠⚠ ECART DELIBERE AVEC `58031`, ET C'EST LE SEUL DU PACK.
    La carte officielle ne teste QUE `paper.set_name in candidate_sets`,
    c'est-a-dire « imprimee dans le pack d'un heros ». Or un pack de heros
    contient AUSSI des cartes d'aspect et des cartes basiques, que n'importe
    quel deck peut inclure : elles ne sont PAS specifiques a une identite.

    La regle du jeu est claire : « identity-specific » designe la restriction
    de construction de deck, qui vaut `Class: "Hero"` dans les donnees. On
    ajoute donc ce test.

    Mesure sur le catalogue du 05/09/2026 : il ecarte QUATRE soutiens LOCATION
    qui seraient sinon offerts a tort — `lj030` * Central Park (Basic, pack
    lockjaw), `as019` * The Daily Bugle (Protection) et `as022` * Spider-Verse
    (Basic, pack armored_spidey), `bk015` * Earth-295 (Basic, pack blink). Il
    n'ecarte AUCUNE amelioration ARMOR ni WEAPON : sur ces deux traits, les
    deux lectures coincident.

    ⚠ L'imprecision de `58031` est donc REELLE mais SANS CONSEQUENCE chez elle
    (aucun allie du depot n'est dans ce cas). Consigne ici plutot que
    recopiee.
    """
    classes = (paper.desc.get("Class") or "").split(";")
    return "Hero" in classes


def CapaciteCameo(type_de_carte: str,
                  trait: str,
                  *,
                  non_permanent: bool = False) -> 'Ability':
    """La capacite Setup commune aux trois cartes.

    Modele integral : `58031` Cameo. Les etapes, dans l'ordre imprime :
      1. chercher dans la collection ;
      2. melanger la carte choisie dans le deck du joueur ;
      3. defausser 2 cartes de sa main ;
      4. retirer cette carte du jeu.

    ⚠ L'ORDRE COMPTE. « Discard 2 cards » est APRES le melange : la carte
    trouvee ne peut donc pas etre defaussee dans la foulee, elle est deja dans
    le deck. Et « remove this card from the game » est en dernier : la carte
    doit encore etre en jeu pendant tout le reste.

    ⚠ `if not this.IsInPlay(): return` : la capacite est branchee sur
    `AfterGameSetup`, qui part pour TOUT LE MONDE. Sans cette garde, la carte
    agirait depuis le deck d'un joueur qui ne l'a pas mise en place.
    """
    from cards.database import CardsDB

    def cameo(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        if not this.IsInPlay():
            return
        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return

        monde = this.card.world
        sets_candidats = SetsDIdentitesHorsPartie(this)

        # ⚠ DEDOUBLONNAGE PAR NOM, comme `58031` : deux packs peuvent imprimer
        # la meme carte (« * Wolverine's Claws » est a la fois `35002` et
        # `wx002`). La joueuse n'a pas a choisir entre deux exemplaires
        # identiques.
        vus = set()
        faces: List['CardFace'] = []
        for card_id, paper in sorted(CardsDB.papers.items()):
            if paper.type != type_de_carte:
                continue
            if paper.set_name not in sets_candidats:
                continue
            if trait not in (paper.traits or []):
                continue
            if not EstSpecifiqueAUneIdentite(paper):
                continue
            if non_permanent and paper.desc.get("Permanent"):
                continue
            if paper.name in vus:
                continue
            vus.add(paper.name)
            carte = CardFactory.GenerateCard(card_id, monde.area_removed, monde)
            faces.append(carte.face)

        if faces:
            choisie = joueur.AskChooseFace(faces, effect)
            if choisie:
                Faces.ShuffleAllTo([choisie], joueur.player_deck, effect)

        # « Discard 2 cards from your hand » — la joueuse choisit lesquelles.
        main = list(joueur.hand_cards.Get())
        if main:
            combien = min(CARTES_A_DEFAUSSER, len(main))

            def defausser(cibles: Sequence['CardFace']) -> None:
                Faces.DiscardAll(list(cibles), effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard 2 cards", defausser,
                ).SetTarget(main, range=(combien, combien), not_move=True),
            )

        # « and remove this card from the game. »
        Faces.RemoveAllFromGame([this], effect)

    return AbilityFactory.AfterGameSetup(cameo)
