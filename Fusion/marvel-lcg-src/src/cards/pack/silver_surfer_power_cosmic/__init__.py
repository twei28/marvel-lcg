from cards.pack import *

# ===========================================================================
# Pack SILVER SURFER « Power Cosmic » (planet deck) : contenu fan-made recu
# par images (marvelchampionslivingtierlist.streamlit.app), auteur Daring
# Lime (identifie le 05/11/2026 ; longtemps note "inconnu" dans ce fichier
# et data/cards.json, corrige partout le meme jour), 04-05/11/2026. Prefixe
# `pc` (tools/prefixes_fanmade.json), set 253.
#
# ⚠ `desc.custom`/`"custom"` (cards.json) NE DOIT CONTENIR QUE LE NOM DU
# CREATEUR, jamais l'URL de la source : `public/js/prepare/auteur.js`
# (`nomAvecAuteur`) colle TOUT le contenu de ce champ entre parentheses a
# cote du nom du heros deja suffixe de son set_name (homonyme avec
# `silver_surfer` de DesignHacker, present dans le meme depot -- ce
# suffixe-la, lui, est automatique et necessaire, pas une erreur).
# "Daring Lime (url)" dans `custom` a donc produit un triple parenthesage
# a l'ecran, corrige le 05/11/2026 (garder la source en commentaire ici
# seulement, jamais dans `custom`).
# 3e Silver Surfer du depot : distinct du `sv` officiel ET du « Silver
# Surfer (Neptune) » (zip Galactus/Thanos, non commence).
#
# MECANIQUE MAISON « PLANET » / « PLAYER ENVIRONMENT » : fiche complete
# docs/reference/mots-cles/environnement-joueur.md. Resume apres plusieurs
# revirements (journal dans la fiche) :
#  - AUCUNE carte ne change jamais de zone (ni le Heros, ni un allie, ni un
#    ennemi) : decision utilisateur du 04/11/2026.
#  - « etre a une planete » = un simple MARQUEUR pose sur la carte du
#    personnage (attribut Python `pc_planete_actuelle` sur l'objet `Card`),
#    pas une carte d'etat generique du moteur (une premiere version avec
#    une carte d'etat maison a ete ecrite puis RETIREE le 05/11/2026 :
#    l'utilisateur a fait remarquer que ce n'est pas une regle du jeu mais
#    le texte IMPRIME de Silver Surfer lui-meme, voir pc001a.py).
#  - questions ouvertes pour l'auteur : `A creer/import-silver-surfer-power-
#    cosmic/QUESTIONS-AUTEUR.md`.
################################################################################


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en
    premier : il leve un assert quand l'initiateur n'est pas un joueur, et le
    moteur l'avale). Modele repris de batman/elektra/iron_fist (pas de helper
    partage entre packs dans ce depot)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    try:
        return effect.GetInitiator()
    except Exception:
        return None


def PlanetDeck(joueur: 'Player') -> 'Deck2':
    """Le « planet deck » personnel de `joueur » : mélangé et mis de côté au
    Setup (desc.Setup de la carte alter-ego), révélé par Cosmic Surfboard
    (pc001b) et pc002.

    ⚠ REVIREMENT (05/11/2026, rapport de partie reelle) : la version
    d'origine fabriquait un `Deck2(DeckType.AdditionalDeck, ...)` MAISON,
    distinct de `joueur.additional_deck`, par excès de prudence (« le slot
    natif est réservé à un autre usage éventuel »). Resultat concret :
    AUCUN affichage plateau ne connait cet attribut Python ad hoc
    (`joueur.pc_planet_deck`) — `ui-app/src/board/zones.ts` ne lit QUE
    `notre?.additional_deck` pour dessiner un « deck spécial » façon
    Doctor Strange/Daredevil (badge, zone, titre). Le planet deck restait
    donc fonctionnel mais INVISIBLE, le piège même que PROCESSUS-CARTE §8
    bis decrit pour `su001b` Master Planner. Aucun autre mecanisme de ce
    pack ne touche `additional_deck` : reutiliser le slot natif (deja cree
    par `Player.__init__`, deja relie a `additional_discard_pile`) est
    sans risque de collision ET rend le deck visible gratuitement, sans
    code plateau specifique a ecrire."""
    return joueur.additional_deck


def EstSilverSurfer(personnage: 'CardFace|None') -> bool:
    """`personnage` est-il l'identite Silver Surfer (face Heros pc001a OU
    Alter-Ego pc001b) ? Utilise par les cartes reactives « After Silver
    Surfer departs a PLANET » (Cosmic Blast, Lightspeed Entrance, Tactical
    Navigation), qui ne doivent reagir qu'a LUI, jamais a un allie ni a
    Nova Frankie Raye (qui dit « I arrive... then depart », pas Silver
    Surfer)."""
    if personnage is None:
        return False
    return getattr(personnage.paper, "card_id", None) in ("pc001a", "pc001b")


def PersonnagesÀLaPlanète(effect: 'Effect', planete: 'CardFace') -> List['CardFace']:
    """Toutes les cartes actuellement marquees « a la planete » `planete`
    (lecture inverse de `EstÀUnePlanète` : balaie `effect.world.object_
    manager.card_dict`, le seul registre complet de toutes les cartes de la
    partie -- aucune autre zone ne les liste toutes a la fois). Necessaire
    pour une carte comme `pc018` Ego The Living Planet dont le texte agit
    sur TOUS les personnages ici a la fois (« each character here »), sans
    liste captee a l'arrivee (contrairement a `pc016` Black Hole, qui agit
    une seule fois a une arrivee connue)."""
    resultats: List['CardFace'] = []
    for carte in effect.world.object_manager.card_dict.values():
        if getattr(carte, 'pc_planete_actuelle', None) is planete:
            resultats.append(carte.face)
    return resultats


def EstÀUnePlanète(personnage: 'CardFace') -> 'CardFace|None':
    """Rend la carte PLANET sur laquelle `personnage` se trouve, ou None.

    Lit uniquement le marqueur pose par `ArriverA`/retire par `Departir` :
    ne regarde PAS la zone de la carte (qui ne bouge jamais, voir ci-dessus).
    """
    return getattr(personnage.card, 'pc_planete_actuelle', None)


def NePeutPasAllerÀUnePlanète(personnage: 'CardFace') -> None:
    """Marque `personnage` comme IMMUNISE au mot-cle maison PLANET : ni
    `ArriverA` ni `Departir` n'agissent plus jamais sur lui (no-op complet).

    AJOUTE pour `pc019` Terrax (« Terrax cannot arrive at or depart a
    PLANET »), seule carte du pack dont le texte imprime l'exige. Necessaire
    parce que `ArriverA`/`Departir` sont des FONCTIONS directes, pas des
    messages WOULD interceptables (`WhenUnitWouldArrivePlanet` n'existe pas
    dans ce mot-cle maison) : une carte comme `pc016` Black Hole pourrait
    sinon y envoyer Terrax (« the villain ... arrive here ») sans que son
    immunite imprimee ne s'applique. Appele UNE FOIS, a la mise en jeu de
    Terrax (`WhenCardEnterPlay`) : le marqueur vit sur `personnage.card`,
    pas sur la face, pour survivre a un changement de forme eventuel."""
    personnage.card.pc_immunise_planete = True


def ArriverA(effect: 'Effect', personnage: 'CardFace', planete: 'CardFace') -> None:
    """`personnage` ARRIVE a la carte PLANET `planete`.

    Pose le marqueur, puis previent les cartes qui reagissent a une arrivee
    (ex. futures pc00X). `player` du message est le joueur de `personnage`
    s'il en a un (un ennemi envoye a une planete n'a pas de joueur propre).

    No-op si `NePeutPasAllerÀUnePlanète` a ete pose sur ce personnage
    (pc019 Terrax : « cannot arrive at or depart a PLANET »).
    """
    from game.message import Message
    from game.card.face.base import Unit2

    if getattr(personnage.card, 'pc_immunise_planete', False):
        return

    personnage.card.pc_planete_actuelle = planete
    # Affichage plateau (etape 8 bis PROCESSUS-CARTE) : infobulle au survol du
    # personnage marque, nom + image de la carte PLANET (decision utilisateur
    # du 04/11/2026). `ui_marker_object_id` est le canal GENERIQUE du moteur
    # (card.py), pas un champ invente pour ce pack.
    personnage.card.ui_marker_object_id = planete.card.object_id

    joueur = None
    if Unit2.IsType(personnage):
        controleur = personnage.CastTo(Unit2).GetControlByOrOwner()
        if isinstance(controleur, Player):
            joueur = controleur

    Message.AfterCharacterArrivePlanet(joueur, personnage, planete).Send()


def Departir(effect: 'Effect', personnage: 'CardFace') -> None:
    """`personnage` PART de la planete ou il se trouve (no-op s'il n'y est pas)."""
    from game.message import Message
    from game.card.face.base import Unit2

    planete = EstÀUnePlanète(personnage)
    if planete is None:
        return

    personnage.card.pc_planete_actuelle = None
    personnage.card.ui_marker_object_id = None

    joueur = None
    if Unit2.IsType(personnage):
        controleur = personnage.CastTo(Unit2).GetControlByOrOwner()
        if isinstance(controleur, Player):
            joueur = controleur

    Message.AfterCharacterDepartPlanet(joueur, personnage, planete).Send()


def AbilitésBlocagePlanet() -> List['Ability']:
    """« Characters at a PLANET cannot attack or scheme... » : texte imprime
    IDENTIQUE sur les deux faces de pc001 (Heros et Alter-Ego), chacune
    l'implemente separement via cette fabrique partagee (pc001a.py, pc001b.py).
    Decision utilisateur du 05/11/2026 : attaque + manigance seulement, pas la
    defense (voir A creer/import-silver-surfer-power-cosmic/QUESTIONS-AUTEUR.md).
    """

    def bloque_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.SetBeInstead(effect)

    def bloque_manigance(effect: 'Effect', message: 'Message.WhenUnitWouldScheme|Message.WhenUnitWouldThwart') -> None:
        message.SetBeInstead(effect)

    def a_une_planete_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return EstÀUnePlanète(message.attacker) is not None

    def a_une_planete_manigance(effect: 'Effect', message: 'Message.WhenUnitWouldScheme|Message.WhenUnitWouldThwart') -> bool:
        return EstÀUnePlanète(message.trigger) is not None

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(),
            bloque_attaque,
            conditions=[a_une_planete_attaque],
        ),
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            CardFinder(),
            bloque_manigance,
            conditions=[a_une_planete_manigance],
        ),
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.ForcedInterrupt,
            CardFinder(),
            bloque_manigance,
            is_basic_thwart=True,
            conditions=[a_une_planete_manigance],
        ),
    ]
