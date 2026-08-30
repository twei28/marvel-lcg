from cards.pack import *

# ===========================================================================
# Pack SPEED — helpers partages du set `Speed`.
#
# ---------------------------------------------------------------------------
# MECANIQUE CENTRALE : LES COMPTEURS EXPLOSIFS
#
# L'insert du pack (« Speed Insert », lu par decoupe d'image le 30/08/2026)
# donne la regle complete, et elle n'appartient a AUCUNE carte :
#
#   « Through his hero ability, Speed can put explosive counters on an enemy
#     or scheme (MAX 1 COUNTER per enemy/scheme).
#     These counters are removed from play AT THE END OF THE PLAYER PHASE and
#     they have the following effects WHEN THEY ARE REMOVED FROM PLAY:
#     - If removed from an enemy, it deals 1 damage to that enemy.
#     - If removed from a scheme, it removes 1 threat from that scheme. »
#
# Ces deux regles transverses (le PLAFOND de 1 et le BALAYAGE de fin de phase
# joueur avec son effet) sont donc portees par l'IDENTITE, et sur LES DEUX
# FACES (sd001a ET sd001b) : les compteurs doivent survivre a un changement de
# forme et etre balayes meme si Speed finit la phase en alter-ego. Une seule
# des deux faces est en jeu a la fois, la regle n'est donc jamais appliquee en
# double. `ReglesDesCompteursExplosifs()` ci-dessous rend les trois capacites
# et est appelee par sd001a.py comme par sd001b.py.
#
# Briques du moteur employees, toutes verifiees avant d'ecrire une ligne :
#   - `Enemy` (game/card/face/base/enemy.py:10) et `Scheme2`
#     (game/card/face/base/scheme.py:9) heritent DEJA de `CanPlaceCounter` :
#     AUCUN correctif moteur n'est necessaire pour poser un compteur dessus ;
#   - `AbilityFactory.WhenCardWouldBePlacedCounter(..., which_face=None, ...)`
#     + `message.maximum = 1` rend le plafond GLOBAL (la fabrique toute faite
#     `MaxCounterHere` ne vise que « This », donc une seule carte) ;
#   - `AbilityFactory.WhenPlayerPhaseEnd` (factory/turn_phase.py:258) rend
#     « at the end of the player phase » ;
#   - `AbilityFactory.AfterCardRemovedCounter(..., which_card=None, ...)` rend
#     « when they are removed from play » : l'effet part quel que soit CE QUI
#     retire le compteur, pas seulement le balayage. C'est la lettre de
#     l'insert. `Condition.CheckWhichCard(None, ...)` rend toujours vrai
#     (condition/card_type.py:98), c'est l'idiome d'un ecouteur global.
#
# Le degat du retrait n'est PAS une attaque : il part de `face.DealDamage`
# depuis l'identite, sans `AttackProperty` et sans passer par
# `WhenUnitWouldAttack` — donc aucune riposte, aucun re-declenchement de
# « apres une attaque ». Meme chose pour le retrait de menace, qui n'est pas
# un contre (`RemoveThreatFromSchemes`, la meme brique que 10004 Sub-Orbital
# Leap).
#
# ---------------------------------------------------------------------------
# L'INTERRUPTEUR DE L'OBLIGATION (sd017)
#
# sd017 No Outrunning This propose « You cannot resolve Speed's Hyperkinetic
# Fuel Interrupt until the end of the next round ». C'est un interrupteur qui
# eteint la capacite du HEROS, pas une capacite de l'obligation : il vit donc
# ici, a cote du helper, exactement comme `EteindreLesBoosts` chez wiccan.
#
# Rendu : un attribut clairement nomme sur `effect.world` (guide §3.1, « Etat
# persistant maison »), leve par `EteindreHyperkineticFuel`, qui enregistre en
# meme temps sur l'IDENTITE du joueur (jamais sur l'obligation, qui part a la
# defausse aussitot apres) une capacite temporaire `WhenRoundEnd` qui le
# rabaisse. « Until the end of the NEXT round » et non « next player phase »
# comme wc018 : l'obligation est revelee pendant la phase du vilain du round
# N, la fin de round qui la leve est donc celle du round N+1, pas N — d'ou le
# compteur `_rounds_ignores` qui laisse passer la premiere.
#
# ---------------------------------------------------------------------------
# LE COUPLAGE sd005 <-> sd001a
#
# sd005 « I'm Out » imprime : « If you would resolve Speed's Hyperkinetic Fuel
# ability when playing this event, shuffle 1 event from your discard pile into
# your deck and draw 1 card INSTEAD. » Le « instead » remplace la RESOLUTION
# de Hyperkinetic Fuel (donc : pas de compteur), pas l'annulation de la carte
# rencontre. C'est la capacite du HEROS qui doit poser la question, sd005
# n'ayant aucun moyen de se voir « en train d'etre payee ». D'ou la liste
# `CARTES_QUI_REMPLACENT_HYPERKINETIC_FUEL` et l'aide partagee
# `RemonterUnEvenementEtPiocher`, elle-meme reutilisee mot pour mot par la
# face alter-ego sd001b (meme phrase imprimee).
#
# ---------------------------------------------------------------------------
# PIEGE DE NOMMAGE — le `*` d'unicite
#
# `cards/paper.py:45-46` retire le prefixe « * » d'un nom unique. Un
# `CardFinder(name="* Quicksilver")` ne trouverait JAMAIS rien, en silence.
# Les constantes ci-dessous sont donc ecrites SANS l'etoile.
#
# PIEGE DE NOMMAGE — la collision « Quicksilver »
#
# sd002 est un ALLIE nomme « Quicksilver » ; `14001a` est le HEROS OFFICIEL du
# meme nom, et CINQ de ses cartes (14003, 14008, 14009, 14010, 14011) font un
# `CardFinder(name="Quicksilver")` NON borne. La collision PREEXISTE : `15002`
# (pack scw) est deja un allie « * Quicksilver ». On ne corrige donc rien cote
# `qsv` (ecart documente dans docs/speed_cartes.md) mais AUCUNE carte de ce
# pack ne fait de recherche par nom non bornee : sd002 n'agit que sur
# `effect.this` (« This »), jamais sur un `CardFinder(name=...)`.
# Meme prudence pour « Speed » lui-meme : le catalogue contient DEJA un allie
# officiel `15010` « * Speed » (Thomas Shepherd, aspect Justice) et un sbire
# `57060` « * Speed ». Aucune carte du pack ne cherche « Speed » par nom.
# ===========================================================================

NOM_SPEED = "Speed"
NOM_THOMAS = "Thomas Shepherd"
NOM_QUICKSILVER = "Quicksilver"
NOM_COAT_OF_ARMS = "Coat of Arms"

# Nom du compteur, declare dans `CardFace.COUNTER` (card_face.py, CORRECTIF).
COMPTEUR_EXPLOSIF = 'explosive'

# « max 1 counter per enemy/scheme » (insert).
MAX_COMPTEURS_EXPLOSIFS = 1

# Nom de l'attribut pose sur le monde par l'obligation sd017.
DRAPEAU_HYPERKINETIC_ETEINT = "_speed_hyperkinetic_eteint"

# Les cartes dont le texte imprime remplace la resolution de Hyperkinetic
# Fuel. Une seule aujourd'hui : sd005 « I'm Out ».
CARTES_QUI_REMPLACENT_HYPERKINETIC_FUEL = ("sd005",)


################################################################################
# Lire les compteurs explosifs

def PorteUnCompteurExplosif(face: 'CardFace|None') -> bool:
    """Vrai si cette face porte au moins un compteur explosif."""
    if face is None:
        return False
    if not isinstance(face, CanPlaceCounter):
        return False
    return face.GetCounters(COMPTEUR_EXPLOSIF) > 0


def FacesAvecUnCompteurExplosif(effect: 'Effect') -> List['CardFace']:
    """Toutes les cartes EN JEU qui portent un compteur explosif."""
    return [face for face in Worlds.GetOnFieldCards(effect)
            if PorteUnCompteurExplosif(face)]


def IlYAUnCompteurExplosifEnJeu(effect: 'Effect') -> bool:
    """« if there is an explosive counter in play » (sd011/sd012 Top Speed).

    N'importe ou en jeu : rien n'exige que ce soit sur une cible du joueur de
    Speed, ni meme que Speed l'ait pose.
    """
    return FacesAvecUnCompteurExplosif(effect) != []


def UneCibleDeCeMessagePorteUnCompteur(message: 'Message2') -> bool:
    """Vrai si l'attaque/le contre decrit par ce message vise au moins une
    carte portant un compteur explosif.

    Accepte indifferemment `WhenUnitWouldAttack` (cibles dans
    `attacked_targets`), `WhenUnitWouldThwart` (cibles dans `schemes`), et les
    messages de pouvoir de base `WhenUnitUseBasicPower` /
    `AfterUnitUseBasicPower`, qui portent l'un des deux precedents dans
    `would_message` / `pre_message.would_message`.
    """
    would = message
    if isinstance(would, Message.AfterUnitUseBasicPower):
        would = would.pre_message
    if isinstance(would, Message.WhenUnitUseBasicPower):
        would = would.would_message

    if isinstance(would, Message.WhenUnitWouldAttack):
        cibles: Sequence['CardFace'] = would.attacked_targets
    elif isinstance(would, Message.WhenUnitWouldThwart):
        cibles = would.schemes
    else:
        return False

    for cible in cibles:
        if PorteUnCompteurExplosif(cible):
            return True
    return False


################################################################################
# Poser un compteur explosif

def PoserUnCompteurExplosif(player: 'Player|None', effect: 'Effect',
                            libelle: str="Put an explosive counter on an enemy or scheme",
                            ) -> None:
    """« put an explosive counter on an enemy or scheme ».

    La cible est demandee par un `ChooseAbilities` a UNE branche (idiome du
    depot, modele 60044 Choreography) plutot que par un `.SetTarget` pose sur
    la capacite appelante : sd001a doit pouvoir NE PAS poser de compteur
    quand sd005 remplace la resolution, et un selecteur declare sur la
    capacite poserait la question meme dans ce cas-la.

    La cible « Enemy|Scheme » est le selecteur du moteur qui rend exactement
    « un ennemi ou une manigance » (selector_target.py:36, modeles 53002
    Redwing et 52002 Smooth as Silk). Il y a toujours au moins un complot
    principal en jeu : la capacite ne reste donc jamais sans cible.
    """
    if player is None:
        return

    def poser(targets: Sequence['CardFace']) -> None:
        if not targets:
            return
        Faces.PlaceCountersOn(list(targets), 1, COMPTEUR_EXPLOSIF, effect,
                              maximum=MAX_COMPTEURS_EXPLOSIFS)

    player.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            libelle,
            poser,
        ).SetTarget("Enemy|Scheme", range=(1, 1)),
    )


################################################################################
# Les deux regles transverses de l'insert (portees par les DEUX faces)

def ReglesDesCompteursExplosifs() -> List['Ability']:
    """Les regles de l'insert, a poser sur sd001a comme sur sd001b."""

    def plafonner(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> None:
        # « max 1 counter per enemy/scheme ». On ecrit `message.maximum`, ce
        # que `PlaceCountersInternal` relit juste apres
        # (can_place_counter.py:56-60) et qui a PRIORITE sur le `maximum=`
        # passe par l'appelant : la regle vaut donc pour TOUTE source, pas
        # seulement pour Hyperkinetic Fuel.
        message.maximum = MAX_COMPTEURS_EXPLOSIFS

    def balayer(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        # « These counters are removed from play at the end of the player
        # phase. » On retire, l'effet du retrait est porte par la capacite
        # suivante (`AfterCardRemovedCounter`), pas ici : l'insert dit bien
        # « when they are REMOVED », pas « at the end of the phase ».
        Unused(message)
        for face in FacesAvecUnCompteurExplosif(effect):
            face.CastTo(CanPlaceCounter).RemoveCountersInternal(
                "All", COMPTEUR_EXPLOSIF, effect, forced=True)

    def effet_du_retrait(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        # « If removed from an enemy, it deals 1 damage to that enemy.
        #   If removed from a scheme, it removes 1 threat from that scheme. »
        # 1 par compteur retire ; le plafond garantit que c'est toujours 1,
        # mais on lit quand meme `removed_counters` plutot que de cabler la
        # valeur, pour que la regle reste juste si le plafond bouge un jour.
        nombre = message.removed_counters
        if nombre <= 0:
            return
        cible = message.trigger
        this = effect.this
        if Enemy.IsType(cible):
            this.DealDamage([cible], nombre, effect)
        elif Scheme2.IsType(cible):
            this.RemoveThreatFromSchemes([cible], nombre, effect)

    return [
        AbilityFactory.WhenCardWouldBePlacedCounter(
            AbilityType.NonKeyword,
            None,
            COMPTEUR_EXPLOSIF,
            plafonner,
        ),
        AbilityFactory.WhenPlayerPhaseEnd(
            AbilityType.NonKeyword,
            balayer,
        ),
        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.NonKeyword,
            None,
            COMPTEUR_EXPLOSIF,
            effet_du_retrait,
        ),
    ]


################################################################################
# Hyperkinetic Fuel : l'interrupteur de l'obligation sd017

def HyperkineticFuelActif(effect: 'Effect') -> bool:
    """Faux uniquement quand l'obligation sd017 a eteint la capacite."""
    return not getattr(effect.world, DRAPEAU_HYPERKINETIC_ETEINT, False)


def EteindreHyperkineticFuel(player: 'Player', effect: 'Effect') -> None:
    """Interrupteur de sd017 : Hyperkinetic Fuel ne se resout plus jusqu'a la
    fin du PROCHAIN round.

    Enregistre sur l'IDENTITE du joueur, jamais sur l'obligation (qui est
    defaussee dans la foulee, ce qui emporterait ses capacites temporaires
    avec elle). L'obligation est revelee en phase du vilain du round N : la
    premiere fin de round rencontree est celle du round N, la seconde celle du
    round N+1 — c'est elle que le texte vise (« the end of the NEXT round »).
    """
    setattr(effect.world, DRAPEAU_HYPERKINETIC_ETEINT, True)

    identite = player.GetIdentity()
    if identite is None:
        return

    class Compte:
        fins_de_round = 0

    def rallumer(eff: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        Unused(message)
        Compte.fins_de_round += 1
        if Compte.fins_de_round >= 2:
            setattr(eff.world, DRAPEAU_HYPERKINETIC_ETEINT, False)

    identite.effect.RegisterTemp(
        AbilityFactory.WhenRoundEnd(
            AbilityType.Temp2,
            None,
            rallumer,
        ),
        unregister_after_exec=False,
    )


################################################################################
# « Shuffle 1 event from your discard pile into your deck. Then, draw 1 card. »

def RemonterUnEvenementEtPiocher(player: 'Player|None', effect: 'Effect') -> None:
    """Phrase imprimee a l'identique sur sd001b (Accelerated Perception) et
    sur sd005 (« I'm Out », branche « instead »).

    Modele : ok011 Upanga et 60014 Karen Page, meme couple
    `Search.PlayerCard(include_discard_pile=True, finder=...)` puis
    `Faces.ShuffleAllTo([face], player.player_deck, effect)`.

    La pioche est INCONDITIONNELLE : le texte dit « Then, draw 1 card », pas
    « if you do ». Une defausse sans le moindre evenement pioche quand meme.
    """
    if player is None:
        return

    face = Search.PlayerCard(
        effect,
        player,
        include_player_deck=False,
        include_discard_pile=True,
        finder=CardFinder(card_type=Event),
    )
    if face:
        Faces.ShuffleAllTo([face], player.player_deck, effect)

    player.DrawUp(1, effect)
