from cards.pack import *

# ===========================================================================
# Pack MS. AMERICA — helpers partages du set `Ms. America`.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : MODIFIER SES STATS, ET JOUER DES CARTES SUPERPOWER
#
# L'insert de l'auteur le dit mot pour mot : « America wants to do two
# things: modify her stats and play SUPERPOWER cards. » Tout le pack tourne
# autour de Star-Gaze (ma001a), la Response de la face heros qui se declenche
# APRES avoir joue une carte [[SUPERPOWER]] et qui branche sur la RESSOURCE
# IMPRIMEE de cette carte.
#
# ⚠ FAIT MESURE (30/08/2026) : le trait SUPERPOWER n'existe QUE sur des
# cartes de heros dans tout le catalogue — 0 carte Aggression, 0 Justice,
# 0 Leadership, 2 Protection. Star-Gaze ne se declenchera donc quasiment que
# sur les cartes signature de ce pack (ma005, ma006, ma007, ma009/ma010,
# ma011/ma012, ma013/ma014, ma015/ma016), sur ma025 Power Stomp, et sur ce
# que ma006 Star Flight CONVERTIT en SUPERPOWER. Une couverture faible en
# autoplay est donc NORMALE, ce n'est pas un defaut.
#
# ---------------------------------------------------------------------------
# LA REGLE DE LA FLECHE — elle apparait sur SIX cartes de ce pack
#
# `→` separe un COUT (a gauche) d'un EFFET (a droite), et la capacite ne se
# declenche QUE si le cout est integralement payable. Regle officielle,
# appliquee sans exception, y compris a une capacite forcee (`11014`,
# `11031`, `16074`) ; quand une carte veut deux CONSEQUENCES elle les relie
# par « and » SANS fleche (`02021` Pumpkin Bombs).
#
# | Carte | Cout (gauche de la fleche) | Rendu par |
# |---|---|---|
# | ma001b | defausser une carte de ta main | `CostFunc.Discard(from_where=["YourHandCards"])` |
# | ma004  | incliner Santana Family | `CostFunc.Exhaust("This")` |
# | ma005  | incliner Star Light | `CostFunc.Exhaust("This")` |
# | ma006  | incliner Star Flight | `CostFunc.Exhaust("This")` |
# | ma007  | incliner CETTE carte **et** en retirer 4 compteurs `star` | `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 4, "star")` |
# | ma009/ma010 | choisir CTR ou ATQ **et redresser ton identite** | `CostFunc.Ready("YourIdentity")` |
# | ma013/ma014 | trouver un allie dans une defausse et le poser incline | `.SetTarget(...)` obligatoire sur la capacite |
# | ma017  | subir 2 (ou 4) degats | `CostFunc.TakeDamage(...)` |
# | ma024  | incliner Noh-Varr's Ship | `CostFunc.Exhaust("This")` |
#
# ⚠ ma009/ma010 America's Anger : l'utilisateur a EXPLICITEMENT REFUSE une
# exception le 30/08/2026. Le cout est bien « choisir CTR ou ATQ ET redresser
# ton identite ». Consequence assumee et VOULUE : identite deja prete = cout
# impayable = CARTE INJOUABLE. Il faut s'etre incline d'abord. Ne pas
# « corriger », ne pas contourner.
#
# ---------------------------------------------------------------------------
# PIEGE DE NOMMAGE — le `*` d'unicite
#
# `cards/paper.py:45-46` retire le prefixe « * » d'un nom unique. Un
# `CardFinder(name="* Star Light")` ne trouverait JAMAIS rien, EN SILENCE.
# Les constantes ci-dessous sont ecrites SANS l'etoile.
#
# PIEGE DE NOMMAGE — TROIS cartes s'appellent « Hawkeye » / Kate Bishop
#
# `04011` Hawkeye (allie officiel Leadership, pack core), le heros du pack
# `kate_bishop` (kb001a/kb001b), et `ma003` Hawkeye de ce pack. AUCUNE carte
# de ce pack ne fait de recherche par nom ou par sous-titre sur « Hawkeye »
# ou « Kate Bishop » : ma003 ne parle que d'elle-meme (`"This"`).
#
# PIEGE DE NOMMAGE — « Gwenpool »
#
# Le jeu contient DEJA un pack complet `gwenpool` (prefixe `gp`, identite
# « Gwenpool »). `ma022` est un ALLIE homonyme. Deux cartes distinctes,
# aucune collision moteur, RIEN n'est corrige cote `gp` : ma022 ne fait
# aucune recherche par nom.
#
# ---------------------------------------------------------------------------
# LA REGLE DE DECK-BUILDING (ma001b)
#
# « You may include upgrade cards that modify your basic powers from any
# aspect in your deck. » Ce n'est PAS une capacite de jeu : le moteur ne
# valide jamais un deck au chargement (GUIDE §5.2). La regle vit dans le
# DECK-BUILDER, `public/js/deckbuilder/app.js`, fonction
# `exemptDeLaLimiteAspect(hero, carte)` (GUIDE §14.1), troisieme cas apres
# Madame Web et Patriot. Rien a coder dans ma001b.py pour elle.
# ===========================================================================

# Noms ecrits SANS l'etoile d'unicite (voir le piege ci-dessus).
NOM_MS_AMERICA = "Ms. America"
NOM_AMERICA_CHAVEZ = "America Chavez"
NOM_ALLOY = "Alloy"
NOM_HAWKEYE = "Hawkeye"
NOM_SANTANA_FAMILY = "Santana Family"
NOM_STAR_LIGHT = "Star Light"
NOM_STAR_FLIGHT = "Star Flight"
NOM_HYPER_COSMIC = "Hyper-Cosmic Awareness"
NOM_CATALINA = "Catalina Chavez"

# Nom de la capacite d'identite, tel qu'il est pose par `.SetName()` sur
# ma001a. ma002 s'y accroche par `ability_name=` : c'est le seul lien.
NOM_STAR_GAZE = "Star-Gaze"

TRAIT_SUPERPOWER = "SUPERPOWER"
TRAIT_YOUNG_AVENGER = "YOUNG AVENGER"
TRAIT_AERIAL = "AERIAL"

# Compteur `star`, ajoute a l'enum COUNTER de `game/card/face/card_face.py`
# (commentaire `# CORRECTIF`). Employe par ma007.
COMPTEUR_STAR = "star"
COMPTEURS_POUR_ANNULER = 4

# ma004 : « to a maximum of 2 » evenements attaches.
MAX_EVENEMENTS_SANTANA = 2

# ma022 : « to a maximum of +2 ATK ».
BONUS_ATK_MAX_GWENPOOL = 2

# ma025 : « Play only if your hero has at least 3 ATK ».
ATK_MINIMUM_POWER_STOMP = 3


################################################################################
# ETAT MAISON PORTE PAR LE MONDE
#
# Idiome du depot (bulles de Gwenpool, `gwenpool/gwenpool/__init__.py:104`) :
# un attribut clairement nomme pose sur `effect.world`, jamais une variable
# de module (le moteur est un singleton mais les mondes ne le sont pas).

def _etat(effect: 'Effect') -> dict:
    monde = effect.world
    d = getattr(monde, '_ms_america', None)
    if d is None:
        d = {}
        setattr(monde, '_ms_america', d)
    return d


################################################################################
# DRAPEAU « STAR-GAZE A ETE RESOLUE CE TOUR »
#
# Lu par ma003 Hawkeye (« if you have resolved "Star-Gaze" this turn »). Le
# drapeau est pose par `ResoudreStarGaze` ci-dessous, donc par le SEUL chemin
# qui resout vraiment la capacite : si Star-Gaze est eteinte, ne trouve
# aucune couleur ou n'est pas declenchee, le drapeau reste baisse.
#
# Il est range PAR JOUEUR (« YOU have resolved »), et vide a la fin du
# premier tour de joueur qui suit, via `RunAt.TurnEnd` (run_at.py:32) —
# meme montage que le nettoyage des bulles de Gwenpool.

def NoterStarGazeResolue(effect: 'Effect', player: 'Player') -> None:
    d = _etat(effect)
    joueurs = d.get('star_gaze_ce_tour')
    if joueurs is None:
        joueurs = set()
        d['star_gaze_ce_tour'] = joueurs
    if not joueurs:
        RunAt.TurnEnd(effect, joueurs.clear)
    joueurs.add(id(player))


def StarGazeResolueCeTour(effect: 'Effect', player: 'Player') -> bool:
    return id(player) in _etat(effect).get('star_gaze_ce_tour', set())


################################################################################
# DRAPEAU « RESSOURCE IMPRIMEE FORCEE EN [wild] » (ma005 Star Light)
#
# « You may change the printed resource of the played card to a [wild]
# resource. » Cette phrase n'a d'effet QUE sur la lecture faite par Star-Gaze.
#
# ECART TECHNIQUE ASSUME : le moteur SAIT muter une ressource imprimee
# (`Message.WhenCountingResourcesOnCards` + `SetReturnValue`, employe par
# `29038` Haywire et `40037a` Domino), mais cette voie change AUSSI la valeur
# de la carte quand elle est DEPENSEE comme ressource, et pour toute la duree
# de vie de la capacite. Ici on ne veut changer que ce que Star-Gaze LIT, une
# fois, pour la carte qui vient d'etre payee. On passe donc par un drapeau,
# comme le guide l'autorise explicitement. Il est efface a la fin de la phase
# (`RunAt.TheEndOfThePhase`, run_at.py:8).

def ForcerRessourceImprimeeEnWild(effect: 'Effect', face: 'CardFace') -> None:
    d = _etat(effect)
    d['ressource_forcee'] = id(face)
    RunAt.TheEndOfThePhase(effect, lambda: d.pop('ressource_forcee', None))


def CouleursImprimeesDe(effect: 'Effect', face: 'CardFace') -> List[str]:
    """Les couleurs imprimees sur `face`, en tenant compte de Star Light.

    `printed_resource` (has_resources.py:15) expose un compteur par couleur
    (`r`/`b`/`y`/`g`) et passe par `Message.WhenCountingResourcesOnCards` :
    c'est la lecture officielle, celle d'`av007` et de `53018` Redwing.
    """
    if _etat(effect).get('ressource_forcee') == id(face):
        return ['g']
    res = getattr(face, 'printed_resource', None)
    if res is None:
        return []
    return [lettre for lettre in ('r', 'b', 'y', 'g')
            if getattr(res, lettre, 0) > 0]


################################################################################
# STAR-GAZE, LA CAPACITE D'IDENTITE (ma001a)
#
# « Response: After you play a [[SUPERPOWER]] card, if that card's printed
#   resource was:
#     [physical] – Deal 1 damage to an enemy.
#     [energy]   – Heal 1 damage from Ms. America.
#     [mental]   – Remove 1 threat from a scheme.
#     [wild]     – Ready Ms. America. »
#
# Le corps est ici et non dans ma001a.py parce que ma008 Energy Infusion doit
# pouvoir le rejouer « an additional time », en FORCANT la couleur.
#
# ECART DOCUMENTE — une carte a PLUSIEURS icones imprimees. Le texte dit
# « was » (singulier) et aucune carte SUPERPOWER du catalogue n'imprime deux
# couleurs DIFFERENTES ; le cas est donc theorique. Quand il se presente, on
# resout UNE FOIS CHAQUE COULEUR PRESENTE, ce qui est l'idiome deja etabli du
# depot pour cette lecture (`av007` Unlikely Allies et `wd154`, tous deux
# « printed resource area includes »). Deux icones de la MEME couleur
# (ma008 « GG ») ne declenchent qu'une fois : on lit des couleurs, pas des
# icones.

def ResoudreStarGaze(effect: 'Effect', player: 'Player',
                     couleurs: Sequence[str]) -> None:
    if not couleurs:
        return

    identite = player.GetIdentity()
    if identite is None:
        return
    # La SOURCE des effets est l'IDENTITE, pas `effect.this` : Star-Gaze est
    # la capacite de Ms. America, et ma008 Energy Infusion la rejoue depuis
    # une carte DEJA DEFAUSSEE (elle vient d'etre depensee comme ressource).
    # Prendre `effect.this` ferait porter les degats par une face hors jeu.
    source = identite

    def branche_physique(targets: Sequence['CardFace']):
        source.DealDamage(list(targets), 1, effect)

    def branche_energie(targets: Sequence['CardFace']):
        Unused(targets)
        source.HealthUnits([identite], 1, effect)

    def branche_mental(targets: Sequence['CardFace']):
        source.RemoveThreatFromSchemes(list(targets), 1, effect)

    def branche_wild(targets: Sequence['CardFace']):
        Unused(targets)
        Faces.ReadyAll([identite], effect)

    fabriques = {
        'r': lambda: AbilityFactory.ForChoiceAbility(
            "Star-Gaze: deal 1 damage to an enemy",
            branche_physique,
        ).SetTarget(Enemy),
        'y': lambda: AbilityFactory.ForChoiceAbility(
            "Star-Gaze: heal 1 damage from Ms. America",
            branche_energie,
        ).SetHasNoTargetEffect(),
        'b': lambda: AbilityFactory.ForChoiceAbility(
            "Star-Gaze: remove 1 threat from a scheme",
            branche_mental,
        ).SetTarget(Scheme2),
        'g': lambda: AbilityFactory.ForChoiceAbility(
            "Star-Gaze: ready Ms. America",
            branche_wild,
        ).SetHasNoTargetEffect(),
    }

    resolue = False
    for lettre in ('r', 'b', 'y', 'g'):
        if lettre in couleurs:
            player.ChooseAbilities(effect, fabriques[lettre]())
            resolue = True

    if resolue:
        NoterStarGazeResolue(effect, player)


################################################################################
# SOMME DES MODIFICATEURS DE STATS DANS LA ZONE DE JEU D'UN JOUEUR (ma018)
#
# « [star] Catalina Chavez gets each stat modifier in your play area
#   (replacing THW with SCH). »
#
# ARBITRAGE DE L'UTILISATEUR (30/08/2026) : lecture LITTERALE, TOUT ce qui
# est dans la zone de jeu du joueur, y compris les ameliorations posees sur
# ses ALLIES (Inspired, Laser Blaster, Danger Room Training...), pas
# seulement celles attachees a l'identite. C'est la lecture la plus punitive,
# et c'est celle qui est demandee.
#
# ECART TECHNIQUE ASSUME — comment on MESURE ces modificateurs. Le moteur
# n'expose nulle part « la liste des modificateurs poses par une carte » :
# les ameliorations d'aspect n'ecrivent PAS leur bonus dans `desc` (mesure
# le 30/08/2026 : les cles `ATK+`/`THW+`/`SCH+` n'existent que sur des
# ATTACHEMENTS de rencontre, jamais sur Combat Training, Heroic Intuition ou
# Inspired, qui l'expriment en CODE via `GiveKeywordToAttached`). On lit donc
# le resultat la ou il est visible : sur les PERSONNAGES AMIS du joueur,
# `face.attack - face.printed_attack` et `face.thwart - face.printed_thwart`
# (attributs officiels, can_attack.py:39 et can_thwart.py:17). Tout
# modificateur pose par une carte de la zone de jeu s'y retrouve, sur
# l'identite comme sur les allies. C'est ce que le texte decrit, mesure a
# l'endroit ou le moteur le rend lisible.

def SommeDesModificateurs(player: 'Player|None', attribut: str) -> int:
    """Somme des modificateurs de `attribut` sur les personnages du joueur.

    `attribut` vaut 'attack' ou 'thwart'. Rend 0 si le joueur est absent.
    """
    if player is None:
        return 0
    total = 0
    faces: List['CardFace'] = []
    identite = player.GetIdentity()
    if identite is not None:
        faces.append(identite)
    faces.extend(player.allies.Get())
    for face in faces:
        if not face.IsInPlay():
            continue
        courant = getattr(face, attribut, None)
        imprime = getattr(face, 'printed_' + attribut, None)
        if courant is None or imprime is None:
            continue
        total += courant - imprime
    return total
