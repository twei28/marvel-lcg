from core import *
from build import Build

from game.card.face import *
from game.deck import *
from game.card import *
from game.world.game_area import *

from game.effect import *
from game.buff import *
from game.message import *
from game.player import *
from cards.paper import Paper

from game.card.face.model.trait import ModelTrait
from game.card.face.model.damage import ModelDamage
from game.card.face.model.form import ModelForm
from game.card.face.model.consider_as import ModelConsider
from game.card.face.model.treat_blank import ModelTreatBlank
from game.card.face.model.face_action import ModelAction
from game.card.face.model.face_on_event import ModelOnEvent
from game.card.face.model.face_gain import ModelGain
from game.card.face.model.face_name import ModelName

from game.element.damage_property import DamageProperty

class CardFace(ModelName, ModelTrait, ModelAction, ModelOnEvent, ModelGain, ModelDamage, ModelForm, ModelConsider, ModelTreatBlank, metaclass=ClassNameMeta):

    is_final = False

    # EXTENSION (01/09/2026, pack custom alligator_loki) : types FINALS qu'une
    # sous-classe revendique aussi. `IsType` d'un type final n'accepte que le
    # type EXACT (`type(face) is cls`) : `Minion.IsType(<PlayerMinion>)`
    # rendait donc False, et le sbire de joueur n'etait un sbire pour personne
    # (Guard, engagement, attaque... `has_guard.py:32` assertait des l'entree
    # en jeu). La sous-classe declare ici les types finals dont elle EST un
    # cas : `PlayerMinion.also_final_types = (Minion,)`.
    also_final_types: 'Tuple[Type[CardFace], ...]' = ()

    # def __enter__(self):
    #     return self

    # def __exit__(self, *obj: object):
    #     pass

    def __lt__(self, other: 'CardFace'):
        return self.card.__lt__(other.card)

    KEY = Literal[
        "Cost", "UnitCost", "HP", "ATK", "THW", "DEF", "REC", "HS", "SCH",
        "RES", "Boost", "Uses",
        "Toughness", "Guard", "Quickstrike", "Retaliate", "Surge", "Assault",
        "ATK+", "SCH+", "THW+", "DEF+",
        "Hazard", "Crisis", "Acceleration", "Amplify",
        "StartingThreat", "TargetThreat", "EscalationThreat",
        "GiveTo", "Nemesis", "Restricted",
        "MaxPerUnit", "MaxPerDeck", "TeamUp",
        "Class", "Permanent", "Steady", "Incite", "Villainous", "Patrol", "Hinder", "Stalwart",
        "ThreatLevel",
        "Requirement", "Victory", "Alliance",
        "Setup", "Peril", "Stage",
        "Linked", "Form", "CorrespondingCard",
        "Temporary", "Teamwork", "Vulnerable",
        "Subtype", 
    ]

    IGNORE_KEY = Literal[
        "Acceleration", "Amplify", "Hazard", "Crisis",
    ]

    ABILITY_IGNORE_KEY = Literal["Guard", "Patrol", "Crisis"]

    TRAITS = Literal[
        "AVENGER", "MUTANT", "X-MEN", "GENIUS", "HERO FOR HIRE", "DEFENSE",
        "SKILL", "SUPERPOWER", "AERIAL", "ATTACK", "SUPERPOWER", "PERSONA",
        "ITEM", "TECH", "CONDITION", "CRIMINAL", "SOLDIER", "S.H.I.E.L.D",
        "LOCATION", "ARMOR", "HYDRA", "ELITE", "ARROW", "WEAPON", "GOBLIN",
        "BUSINESSMAN", "MERCENARY", "ASSASSIN", "ELITE", "MERCENARY",
        "MASTERS OF EVIL", "DRONE", "ANDROID", "BRUTE", "CHAMPION", "PSIONIC",
        "THWART", "SPY", "ASGARD", "GAMMA", "VEHICLE", "BLACK PANTHER", "GIANT",
        "TINY", "SPELL", "MYSTIC", "SYMBIOTE", "GUARDIAN", "WEB-WARRIOR",
        # CORRECTIF : traits du pack sentinel (T-Wrecks, set 173, 12/09/2026).
        # COMPONENT / INTACT / DESTROYED portent les quatre ameliorations
        # recto-verso du heros ; HACKED est donne aux ameliorations par la
        # manigance nemesis Rogue Asset ; SENTINEL est le trait du sbire.
        "COMPONENT", "INTACT", "DESTROYED", "HACKED", "SENTINEL",
        # CORRECTIF (13/09/2026) : trait du set modulaire custom `muse` (Rainy).
        # Muse est un ARTIST, et c'est le seul du catalogue.
        "ARTIST",
        "QUIET", "CIVILIAN",
        "ICE", "STONE", "METAL", "WOOD",
        # CORRECTIF : traits du pack custom superior_iron_man (Merlin).
        "EXTREMIS", "INDIVIDUAL",
        # CORRECTIF : trait du pack custom harry_osborn (Dipsome).
        "EARTH-6160",
        # CORRECTIF : trait du pack custom agatha_harkness (Ripper3).
        "COSMIC ENTITY",
        # CORRECTIF : traits du pack custom iron_patriot (Neptune).
        # `REGISTERED` est le coeur du pack : le trait que Norman Osborn donne
        # aux sbires qu'il recrute depuis son deck secondaire, et que sept
        # cartes du pack interrogent. `H.A.M.M.E.R.` est son organisation,
        # `CABAL` celle de son set nemesis (Doctor Doom).
        # ⚠ La face alter-ego imprime « BUISNESSMAN », coquille de l'auteur
        # pour BUSINESSMAN, qui existe deja plus haut. On garde le trait
        # CORRECT : un trait est une CLE MECANIQUE, pas du texte d'affichage,
        # et « BUISNESSMAN » ne s'apparierait a aucun effet du jeu. C'est le
        # seul endroit du pack ou l'on s'ecarte de ce qui est imprime.
        "REGISTERED", "H.A.M.M.E.R.", "CABAL",
        # CORRECTIF : trait du pack custom spider_woman (Kajislav). `sw012`
        # * Century est un ALIEN, trait qui n'existait nulle part alors qu'il
        # est courant dans le jeu officiel. Purement declaratif, comme les
        # autres : `TRAITS` n'est qu'un `Literal` de typage.
        "ALIEN",
        # CORRECTIF : trait du pack custom beast. Le sbire nemesis bt020
        # « Lizard-Fied Mutants » porte « LIZARD. MUTANT. ». Purement
        # declaratif : TRAITS n'est qu'un `Literal` de typage, aucun controle
        # ne le lit a l'execution (cf. l'unique usage, cards/paper.py:13).
        "LIZARD",
        # CORRECTIF (15/10/2026) : trait du pack custom skrull_menace
        # (Kajislav). sk001b * Teddy Altman, l'alter-ego de Hulkling, porte
        # « HYBRID. » (mi-Kree, mi-Skrull). Purement declaratif, comme LIZARD.
        "HYBRID",
        # (15/10/2026) Les 9 environnements du paquet PLANET du scenario
        # Skrull Empire portent « LOCATION. PLANET. » ; cinq cartes du
        # scenario les comptent ou les visent par ce trait.
        "PLANET",
        # (15/10/2026) Lyja (Kajislav) : huit evenements joueur portent « TREACHERY. »
        # (Faking Death...) : ils se melangent dans le deck rencontre et se
        # resolvent comme des traitrises. Purement declaratif cote enum ;
        # les capacites de Lyja, Mole, Untrustworthiness et Paibok le lisent.
        "TREACHERY",
        # (15/10/2026) Paibok / New Revengers (Kajislav) : « POWER SKRULL » (les quatre
        # attachements de pouvoir de Paibok), « REVENGER » (les sbires du set
        # modulaire, l'environnement O.M.N.I.T.R.O.N.I.C.U.S.) et « COMPUTER ».
        # Purement declaratif cote enum, les capacites de Paibok et du set les lisent.
        "POWER SKRULL", "REVENGER", "COMPUTER",
        # (15/10/2026) Secret Invasion (Kajislav) : les deux etats d'un Skrull infiltre
        # (CAMOUFLAGED = allie / Spider-Woman, REVEALED = sbire / Queen Veranke) et le
        # trait IMPOSTOR des 20 cartes double face du paquet Impostor. Purement declaratif.
        "CAMOUFLAGED", "REVEALED", "IMPOSTOR",
        # (15/10/2026) Skrull Pantheon (Kajislav) : « GOD » (Kly'bn / Sl'gur't), purement declaratif.
        "GOD",
        "TRAINING", "TEAM", "SPECIALIZATION", "TECHNIQUE",
        "ACTIVATION ORDER 1", "ACTIVATION ORDER 2", "ACTIVATION ORDER 3", "ACTIVATION ORDER 4", "ACTIVATION ORDER 5", "ACTIVATION ORDER 6",
        "TRAP!",
        "CROSSFIRE'S CREW", "SETTING", "ILLUSION", "INFINITE", "CAPTIVE", "WOUNDED", "UNDEAD",
        "PREPARATION", "WEATHER",
        "CHEERING CROWD", "BOOING CROWD", "STRONGHOLD",
        "BLACK ORDER", "INFINITY STONE", "SHOW", "CORNERED", "ESCAPED", "SPINNING", "X-FORCE", "X-FACTOR",
        "CREATURE", "TEMPORAL", "THIEF", "POSSE", "PSI-ENERGY", "TACTIC", "LIMBO", 
        "SHAPESHIFTER", "BROTHERHOOD OF MUTANTS", "SENTINEL", 
        "ACOLYTE", "MAGNETIC", "MARAUDER", "MUTANT LIBERATION FRONT", "NASTY BOY", "MORLOCK",
        "VERSION 1", "VERSION 2", "VERSION 3",
        "DARK RIDERS", "CELESTIAL", "HORSEMEN", "PRELATE", "IMPERIAL GUARD", "BIOMORPH", "CYBERPATH", "NEW", "ACOLYTE", 
        "REAVER", "INTERFACE", "INACTIVE", "ACTIVE", 
        "RESTRAINED", "UNLEASHED", "GENOSHA", "CONTROLLED", "DEADPOOL CORPS", "MISSION", "TRAP!", 
        "HELLFIRE", "HENCHMAN", "INFERNAL", "LEVIATHAN", "A.I.M", "LOW", "HIGH", "ADAPTOID", "RESCUED", "INHUMAN", "WAKANDA", "DORA MILAJE",
        "THUNDERBOLT", "BOARD MEMBER", "UNMASKED", "INHERITOR", "BIRD", "SERPENT SOCIETY", 
        "ENHANCED", 
        "ENCHANTMENT", "SHAPESHIFT", "ENTHRALLED", "DEFIANT", "UNREGISTERED", "ATLANTIS", 
        "DEFENDER",
        "ENHANCEMENT", "WOLVERINE", "ZOMBIE",  # CORRECTIF : traits du pack custom albert (Kajislav)
        "VARIANT",  # CORRECTIF : trait du pack custom gwenpool (ekAugust)
        "FANTASTIC FOUR", "FIRE", "MUTATE", "WATER",  # CORRECTIF : traits du pack custom human_torch (DesignHacker)
        "SCIENTIST", "ROBOT",  # CORRECTIF : traits du pack custom mister_fantastic (DesignHacker)
        "INVISIBLE", "TRAANIAN",  # CORRECTIF : traits du pack custom invisible_woman (DesignHacker)
        "PILOT", "GANG",  # CORRECTIF : traits du pack custom the_thing (DesignHacker)
        "OLYMPUS", "QUEEN", "MONSTER",  # CORRECTIF : traits du pack custom totally_awesome_hulk (DesignHacker)
        "SKRULL",  # CORRECTIF : trait du pack custom madame_web (Kajislav)
        "DARKFORCE", "LIGHTFORCE", "RUNAWAY",  # CORRECTIF : traits du pack custom cloak_dagger (DesignHacker)
        "IDENTITY", "ARTIFACT",  # CORRECTIF : traits du pack custom moon_knight (DesignHacker)
        "PET AVENGER", "GOOD BOY", "TELEPORT", "KING", "ARTHROSIAN", "HAMSTER", "SAVAGE LAND", "X-MAN",  # CORRECTIF : traits du pack custom lockjaw (Nugget)
        "MIDNIGHT SON", "WEB", "JOURNALIST", "TITLE",  # CORRECTIF : traits des packs custom spider_man_rainy / venom_rainy (Rainy)
        "SQUIRREL", "STUDENT", "SUIT", "NETWORK", "ASGARDIAN",  # CORRECTIF : traits du pack custom squirrel_girl
        "PSYCHIATRIST",  # CORRECTIF : trait du pack custom agent_13 (Rainy)
        "REPTILIAN", "A.I.M. SCIENTIST", "MULTIVERSE", "CORRUPT", "TRAP!", "UNDERLING",  # CORRECTIF : traits du pack custom web_of_deceit (Ripper3)
        "CLONE",  # CORRECTIF : trait du pack custom scarlet_spider (CptScorp)
        "DUCK", "ELDER", "VAMPIRE",  # CORRECTIF : traits du pack custom howard_the_duck (RyCoRan)
        "YOUNG AVENGER", "KREE", "FAMILY", "WIZARD",  # CORRECTIF : traits du pack custom wiccan (CptScorp)
        "ANTI HERO", "ART",  # CORRECTIF : traits du pack custom speed (CptScorp)
        "MAGGIA", "POLICE",  # CORRECTIF : traits du pack officiel Fear No Evil (Hammerhead, Cops), 18/09/2026
        "INFLUENCED", "HAND", "NINJA",  # CORRECTIF : Fear No Evil bloc 2 (Purple Man, Lady Bullseye, Hand Lookout), 18/09/2026
        "DECEIVED", "DISASTER", "DAILY BUGLE", "TRACKSUIT", "PRISONER", "BADOON", "MARTIAL ARTIST",  # CORRECTIF : Fear No Evil blocs 3-4 (Baron Zemo, Disasters, Stop the Presses!, Tracksuit Mafia, The Raft Breakout, Drang, Kingpin), 18/09/2026
        "COMPLETED", "FAILED",  # CORRECTIF : Fear No Evil bloc 5, environnements de campagne (60205-60209), 18/09/2026
        "STARLING",  # CORRECTIF : trait du pack custom ms_america (jakxin)
        "NECROVERSE",  # CORRECTIF : trait du pack custom gorr (BLUEHG)
        "TEMPTATION",  # CORRECTIF : trait du pack custom lady_sif (Rainy)
        "OPERATIONAL", "DESTROYED",  # CORRECTIF : les deux faces de Spider Armor, pack custom armored_spidey (Kajislav)
        "PORTAL",  # CORRECTIF : trait du pack custom blink (Kajislav), porte par les 5 ameliorations qui font tout le pack
        # CORRECTIF : traits du pack custom texas_twister (Kajislav).
        # ⚠ ROTATION n'est pas decoratif : tt008 et tt009 se defaussent
        # mutuellement des qu'une carte ROTATION entre en jeu.
        "RANGER", "ROTATION", "DEMON",
        "CYBORG",  # CORRECTIF : trait du pack custom beta_ray_bill (Rainy)
        # AJOUT (25/09/2026) : traits des packs custom conan et red_sonja (RyCoRan).
        # THIEF, KING et TITLE existaient deja. Lus par cn002 Belit, cn009 et la
        # remise « Discount 1 (KING) ».
        "ADVENTURER", "CIMMERIA", "PIRATE", "BARBARIAN",
        # (15/10/2026) Cartes de campagne de Skrull Menace (Kajislav, sk263-sk288) : traits imprimes sur les allies
        # et soutiens (Crusader « INITIATIVE », Paibok « S.W.O.R.D. », Skymax « SQUADRON SUPREME », Xavin
        # « RUNAWAYS », Skrull Kill Krew « CREW »). Purement declaratif, comme les autres.
        "INITIATIVE", "S.W.O.R.D.", "SQUADRON SUPREME", "RUNAWAYS", "CREW",
        # CORRECTIF : traits du pack custom leonardo (Inkwire, TMNT Heroes).
        # ⚠ KATANA n'est PAS decoratif : tl001b/tl004/tl005/tl008/tl009/tl010
        # cherchent les ameliorations par ce trait.
        "NINJA", "TURTLE", "TEENAGER", "RAT", "SENSEI", "KATANA", "STANCE",
        "FOOT CLAN", "NYC", "SKYLINE",
        # CORRECTIF : traits du pack custom donatello (Inkwire, TMNT Heroes).
        # MOUSERS / FLYBORGS ne sont pas decoratifs : td014 et td015 les lisent.
        "BO", "SEWERS",
        "MOUSERS", "FLYBORGS", "SWARM",
        # CORRECTIF : traits du pack custom venus (Inkwire, TMNT Heroes). ELEMENT n'est PAS
        # decoratif : tv001a/tv001b comptent et cherchent les ameliorations par ce trait.
        "SHARK", "ELEMENT", "QUANTA", "SONG", "CONSTRUCT", "BULL", "MOLE",
    ]

    TRAITS_LIST: List[TRAITS] = Types.LiteralToList(TRAITS)

    TOKEN = Literal[
        'acceleration_token',
        'first_player_token',
        'threat',
        'damage',  # CORRECTIF : Fear No Evil, jetons damage de Disturbed Psyche (60112), 18/09/2026
    ]

    COUNTER = Literal[
        'counter',

        'attack', 'web', 'glory', 'damage', 'infamy', 'madness', 'arrow',
        'snoop', 'medical', 'pym', 'size', 'mystic', 'psionic', 'warrior',
        'time', 'test', 'active', 'energy', 'glider', 'bomb', 'mental',
        'vengeance', 'physical', 'ammo', 'charge', 'toon', 'training', 'chime',
        'rage', 'delay',
        # AJOUT (10/09/2026, pack custom spider_woman) : le compteur du pack,
        # celui que 12 de ses 29 cartes lisent, posent ou depensent.
        # ⚠ `psionic` existe deja juste au-dessus, et il est PRIS : `mw002`
        # (pack madame_web) et `35013` (Wolverine) s'en servent. Or Madame Web
        # est justement une ALLIEE de ce pack-ci : les deux stocks peuvent se
        # retrouver sur la meme table, et porter le meme nom les melangerait
        # sous les yeux du joueur. D'ou une entree a part, au nom imprime.
        'psionic web',
        'steel', 'reflection', 'command', 'growth', 'poison', 'barrage', 'evasion',
        'fury', 'sand',
        'drain',         # CORRECTIF : Fear No Evil, Drained of Power (60080), Uses (3 drain counters), 18/09/2026
        'civilian', 'stamina', 'grip', 'spot', 'stilt', 'support',  # CORRECTIF : Fear No Evil blocs 3-4 (Disasters, Daily Bugle, Bear Hug, Spot, Stilt-Man, Public Support), 18/09/2026
        'threat',        # CORRECTIF : compteur du pack custom superior_spider_man
                         # (Rainy). Le mot-cle maison `track` DEPLACE de la menace
                         # d'une manigance vers un SBIRE ; la menace posee sur un
                         # sbire n'a aucune existence native, c'est donc un
                         # compteur nomme.
        'surveillance',  # CORRECTIF : idem, les pions de su011 Spider-Bot
        'klyntar',       # CORRECTIF : compteur de l'aspect custom venomized
                         # (ekAugust) : vz030 Durable Physiology (2) et vz032
                         # Klyntar Tendrils (3) l'impriment en toutes lettres.
        'flame',  # CORRECTIF : compteur du pack custom human_torch (DesignHacker)
        'flare',  # CORRECTIF : compteur du pack custom mister_fantastic (DesignHacker)
        'calm',  # CORRECTIF : compteur du pack custom lockjaw (Nugget)
        'illusion', 'menace',  # CORRECTIF : compteurs des packs custom spider_man_rainy / venom_rainy (Rainy)
        'evidence',  # CORRECTIF : compteur du pack custom jessica_jones (ekAugust)
        'aegis',  # CORRECTIF (11/09/2026) : compteur de ze007 The Aegis, pack custom zeus (Mozilla)\n
        'fire',   # 11/09/2026 : compteur de hc018 Firestar, pack custom hellcat (jakxin)
        'adrenaline',  # CORRECTIF : compteur du pack custom venompool (CptScorp)
        'reactor',  # CORRECTIF : compteur du pack custom iron_man_model_42 (Rainy)
        'metal', 'sense', 'article',  # CORRECTIF : compteurs du pack custom armored_spidey (Kajislav)
        'wound',  # CORRECTIF : compteur du pack custom yondu (BLUEHG + DESIGNHACKER)
        'hate',  # CORRECTIF : compteur du pack custom doctor_druid (Kajislav), max 5 sur Nekra
        'shell',  # CORRECTIF : compteur du pack custom texas_twister (Kajislav), 2 sur Armadillo
        'unworthy',  # CORRECTIF : compteur du pack custom beta_ray_bill (Rainy), 2 sur l'obligation
        'graffiti',  # CORRECTIF (13/09/2026) : compteur de mu004 Graffitied Streets,
                     # set modulaire custom muse (Rainy). 3 par heros a l'entree en
                     # jeu ; l'environnement se defausse quand le dernier part.
        # CORRECTIF : compteurs des packs officiels Jessica Jones (61xxx) et
        # Luke Cage (62xxx). Sans eux, `IsCounter` refuse le nom et toute carte
        # portant « Uses (N x counters) » tombe des la creation de la partie.
        'pheromone',  # Suggestion 61033a/b/c
        'limb',       # Spider-Woman 61016
        'squirrel',   # Squirrel Girl 61017
        'block',      # Defensive Formation 62018
        # CORRECTIF : compteurs du pack custom determination (DesignHacker). Les dix
        # sont releves dans .planning/donnees/determination-cartes.json ; sans eux,
        # la carte qui les porte tombe a la construction.
        'tactic', 'adrenaline', 'diversion', 'stimulant', 'spider', 'replay',
        'ball', 'LMD', 'configuration', 'deploy',
        'labor',  # CORRECTIF : compteur du pack custom hercules (59004)
        "blackout_y", "blackout_b", "blackout_r",
        "tic_tac_toe_1_1", "tic_tac_toe_2_1", "tic_tac_toe_3_1",
        "tic_tac_toe_1_2", "tic_tac_toe_2_2", "tic_tac_toe_3_2",
        "tic_tac_toe_1_3", "tic_tac_toe_2_3", "tic_tac_toe_3_3",

        'shift', 'pursuit', 'chi', 'ratings', 'clue', 'stake',
        'blood', 'thirst', # CORRECTIF : compteurs du pack custom blade (Rainy), 07/09/2026. 'blood' sur l'identite, 'thirst' sur l'obligation (Uses). 'stake' existait deja (Mojo 39048).
        'invocation', 'teleport', 'sword', 'mangetic',
        'power', 'backup', 'soul', 'fatigue', 'research', 'psi', 'leadership', 'boom',
        'freeze', 'operative', 'judo', 'magnet', 'knock', 'momentum',

        'progress', 'sym', 'luck', 'deploy', 'supply', 'missile', 'operation', 'speed', 
        'staff', 'mission', 'leap', 'lock', 'parley', 'bystander', 'doubt', 'target', 
        'secret', 'bird', 'recon', 'emergency', 'alert', 'notoriety', 'dart', 

        'charm', 
        'fuel', 'stronghold', 'skill',

        'rebirth', 
        # CORRECTIF : compteurs du pack custom web_of_deceit (Ripper3). The Lizard
        # gagne +1 ATK par compteur « formula », et Curt Connors ne revient au
        # Lizard que quand le dernier compteur « sanity » quitte Lizard Brain.
        # Les « pigeon » vivent sur le complot principal du scenario Vulture :
        # ils remplacent la menace qu'on voudrait retirer, trois pour trois.
        'formula', 'sanity', 'pigeon',
        'shame',  # CORRECTIF : compteur du pack custom hunting_season (Nugget), Reptilian Rage hs060, max 3
        'rat',  # CORRECTIF : compteur du pack custom hunting_season (Nugget), Vermin hs200 (allie) et hs204 (sbire)
        # Les Spider-Bots de l'arbre Web-Spinner portent leurs propres compteurs.
        'bot',
        # CORRECTIF : compteur du pack custom iron_lad (CptScorp). Ion
        # Amplifiers (il011/il012) entre en jeu avec un compteur « ion » par
        # carte TECH controlee (pose a la main, desc.Uses ne sait pas porter
        # un compte dynamique) et le depense en Hero Resource.
        'ion',
        # CORRECTIF : compteur du pack custom donatello (Inkwire). Les sbires
        # td016 / td017 (SWARM) entrent en jeu avec 2 / 4 « swarm » ; leur
        # ATQ, MNG et PV valent ce nombre.
        'swarm',
        # CORRECTIF : compteur du pack custom venus (Inkwire). Les compteurs de dragage vivent
        # sur la carte d'IDENTITE (Venus / Bonnie, meme stock) ; tv001a les pose (max 6) et
        # les ameliorations / evenements du pack les retirent en cout.
        'dredge',
        # CORRECTIF : compteurs du pack custom dazzler (Lord Havok). Le « sound »
        # marque un SONG de la Setlist deja repete (« Rehearsal » n'accepte qu'un
        # SONG SANS compteur) ; le « knife » alimente les interruptions de
        # Longshot, qui entre en jeu avec deux.
        'sound', 'knife',
        # CORRECTIF : compteurs du pack custom superior_iron_man (Merlin). Le
        # "cash" (Flouze sur la carte imprimee) alimente Daniel Hall/Claire
        # Mooney/Mason Thomas ; l'"observation" alimente Iron Sight.
        'cash', 'observation',
        # CORRECTIF : compteur du pack custom kate_bishop (CptScorp). Kate's
        # Aviators (kb011) entre en jeu avec "Uses (2 style counters)" ; sans
        # cette entree, `IsCounter('style')` echoue et la carte fait planter
        # TOUT chargement du hero_deck de Kate Bishop des la mise en place.
        'style',
        # CORRECTIF : compteur du pack custom okoye (CptScorp). Close Ranks
        # (ok010) place des compteurs "phalanx" (max 3) et les depense en
        # ressources [physical] via son pouvoir de ressource.
        'phalanx',
        # CORRECTIF (15/10/2026) : compteur du pack custom skrull_menace
        # (Kajislav). sk010 Ancestors entre en jeu avec « Uses (2 individual
        # counters) » : sans cette entree, `IsCounter('individual')` echoue et
        # la carte tombe a la mise en place, comme 'style' ci-dessus.
        'individual',
        # CORRECTIF (15/10/2026) : compteur du pack custom skrull_menace, heros
        # Lyja (Kajislav). sk056 Invisible Woman pose 1 compteur « revelation »
        # sur la cible de chacun de ses pouvoirs de base et subit +1 degat
        # consecutif par compteur deja present sur la cible suivante.
        'revelation',
        # CORRECTIF : compteur du pack custom speed (CptScorp). L'insert du pack
        # decrit les « explosive counters » : la capacite du heros en pose un sur
        # un ennemi ou une manigance (max 1 par carte), ils sont retires en fin de
        # phase des joueurs et, en partant, infligent 1 degat a l'ennemi ou
        # retirent 1 menace a la manigance.
        'explosive',
        # CORRECTIF : compteur du pack custom beast. bt012 Civilian Disguise
        # entre en jeu avec « Uses (3 disguise counters) » : sans cette
        # entree, `IsCounter('disguise')` refuse le nom et la carte tombe des
        # la construction du deck (meme panne que 'style' pour kate_bishop).
        'disguise',
        # CORRECTIF : compteur du pack custom ms_america (jakxin). Hyper-Cosmic
        # Awareness (ma007) accumule 1 compteur « star » par carte SUPERPOWER
        # jouee, et en depense 4 d'un coup pour annuler une carte rencontre.
        'star',
        # CORRECTIF : compteurs du pack custom gorr (BLUEHG). Les trois
        # horloges du scenario : `plan` s'accumule sur le complot principal
        # 1B et le fait avancer a 3, `timer` s'accumule sur l'environnement
        # Godbomb et fait perdre a 12 par joueur, `necro` sur sa face
        # All-Black Necroverse et renforce les ennemis par paliers avant de
        # faire perdre a 12 par joueur. Sans ces entrees, `IsCounter` refuse
        # le nom et la partie tombe des la pose du premier compteur.
        'plan',
        'timer',
        'necro',
        # CORRECTIF : compteur du set modulaire custom intergalactic_hazards
        # (BLUEHG). Asteroid Belt entre en jeu avec « Uses (2 asteroid
        # counters) » : sans cette entree, `IsCounter('asteroid')` refuse le
        # nom et la carte tombe des la construction du deck.
        'asteroid',
        # CORRECTIF : compteur du pack custom throg (Rainy). tg011 Trouble in
        # Central Park entre en jeu avec « Uses (3 foe counters) » : sans cette
        # entree, `IsCounter('foe')` refuse le nom et l'obligation tombe des la
        # construction du deck (meme panne que 'style' pour kate_bishop et
        # 'disguise' pour beast). Fiche du mot-cle : docs/reference/mots-cles/uses.md
        'foe',
        # CORRECTIF : compteurs du pack custom red_sonja (RyCoRan). rs011
        # Crimson Shadow entre en jeu avec « Uses (2 stealth counters) »,
        # rs018 She-Devil Shackled! avec « Uses (3 fetter counters) » : sans
        # ces entrees, `IsCounter` refuse le nom et la carte tombe des sa
        # construction (meme panne que 'foe' pour throg).
        'stealth', 'fetter',
        # AJOUT (25/09/2026) : pack custom conan (RyCoRan). 'crom' sur The Cimmerian
        # (cn012a/b), 'serpent' sur l'obligation cn013 The Coils of Doom (Uses).
        'crom', 'serpent',
        # AJOUT (15/10/2026) : pack custom skrull_menace, scenario Paibok (Kajislav).
        # 'mastery' : jetons de MAITRISE poses sur Paibok (compteur maison, insert p.12) ;
        # 'absorption' : Asti the All-Seeing (sk163). Sans ces entrees `IsCounter`
        # refuse le nom et la pose du compteur echoue.
        'mastery', 'absorption',
        # AJOUT (15/10/2026) : scenario Secret Invasion (Kajislav). 'suspicion' : jetons de
        # SOUPCON de l'environnement « Who Do You Trust? ».
        'suspicion',
        # AJOUT (15/10/2026) : scenario Skrull Pantheon (Kajislav). 'faith' : jetons de FOI
        # poses sur le mechant Kly'bn / Sl'gur't (insert p.14). Sans cette entree `IsCounter`
        # refuse le nom et la pose du jeton echoue.
        'faith',
    ]

    COUNTER_LIST: List[COUNTER] = Types.LiteralToList(COUNTER)

    FORM = Literal[
        "Energy", "Mass", "Suit"
    ]

    STATUS = Literal[
        # CORRECTIF : « Exposed », quatrieme carte d'etat, ajoutee pour le pack
        # sentinel (12/09/2026, fiche docs/reference/mots-cles/exposed.md).
        # Contrairement aux trois autres, sa regle n'est pas dans le moteur :
        # elle est scriptee sur la carte (cards/pack/status/exposed.py).
        "Confused", "Stunned", "Tough", "Exposed", "Cloaked"
    ]

    ATTACK_KEYWORD = Literal[
        'overkill', 'piercing', 'ranged'
    ]

    SETNAMES = Literal[
        "", "Absorbing Man", "Ant-Man Nemesis", "Ant-Man", "Armies of Titan", "Band Of Badoon", "Beasty Boys", "Black Order", "Black Panther Nemesis", "Black Panther", "Black Widow", "Bomb Scare", "Brotherhood Of Badoon", "Brothers Grimm", "Bulldozer", "Captain America Nemesis", "Captain America", "Captain Marvel Nemesis", "Captain Marvel", "Children of Thanos", "City in Chaos", "Collector 1", "Collector 2", "Colossus Nemesis", "Colossus", "Crime", "Crossbones", "Crossfire's Crew", "Deadpool Nemesis", "Deadpool", "Doctor Strange Nemesis", "Doctor Strange", "Down to Earth", "Drax Nemesis", "Drax", "Dystopian Nightmare", "Ebony Maw", "Enchantress", "Experimental Weapons", "Expert II", "Expert Kang", "Expert", "Fantasy", "Frost Giants", "Galactic Artifacts", "Ghost-Spider", "Goblin Gear", "Goblin Gimmicks", "Guerrilla Tactics", "Hawkeye Nemesis", "Hawkeye", "Hela", "Horror", "Hulk Nemesis", "Hulk", "Hydra Assault", "Hydra Patrol", "Infinites", "Infinity Gauntlet", "Invocation", "Iron Man Nemesis", "Iron Man", "Kang", "Klaw", "Kree Militants", "Legions of Hel", "Legions of Hydra", "Loki", "Magog", "Masters of Evil", "Menagerie Medley", "Mister Hyde", "Mojo", "Ms. Marvel", "Mutagen Formula", "Mysterio", "Nebula", "Personal Nightmare", "Piledriver", "Power Stone", "Quicksilver Nemesis", "Quicksilver", "Ransacked Armory", "Red Skull", "Rhino", "Risky Business", "Rocket Raccoon Nemesis", "Rocket Raccoon", "Ronan", "Sandman", "Scarlet Witch Nemesis", "Scarlet Witch", "Sci-Fi", "Ship Command", "Sinister Six", "Sinister Syndicate", "Sitcom", "Space Pirates", "Spectrum Nemesis", "Spectrum", "Spider-Ham Nemesis", "Spider-Ham", "Spider-Man Nemesis", "Spider-Man", "Spider-Woman Nemesis", "Spiral", "Standard II", "Standard III", "Standard", "Star-Lord Nemesis", "Star-Lord", "State of Emergency", "Storm Nemesis", "Storm", "Streets of Mayhem", "Symbiotic Strength", "Taskmaster", "Temporal", "Thanos", "The Hood", "The Tower Defense", "Thor", "Thunderball", "Ultron", "Under Attack", "Unus", "Valkyrie Nemesis", "Valkyrie", "Venom Goblin", "Venom Nemesis", "Venom", "Weapon Master", "Weather", "Western", "Whispers of Paranoia", "Wolverine Nemesis", "Wolverine", "Wrecker", "Wrecking Crew", "Zola",
        "Cyclops", "Flight", "Super Strength", "Telepathy", "Four Horsemen", 
        "Blue Moon", "Genosha", "Savage Land", "Magneto", "Shadow King", "Dreadpool", "Kree Fanatic", 
        "Thunderbolts", "Executive Board Evidence", "Frostbite", "Iceman", "Spider-Man - Miles Morales",
        "The Spot",
        # CORRECTIF : set_names du pack custom superior_iron_man (Merlin).
        # Distincts de "Iron Man"/"Iron Man Nemesis" (officiels) : IsDeckBuildingClass
        # compare les set_name litteralement (meme piege que wolverine_x23).
        "Superior Iron Man", "Superior Iron Man Nemesis",
        # CORRECTIF : set_names du pack custom gorr (BLUEHG). Deux sets
        # d'encartage : le principal et son modulaire, mis de cote au setup et
        # melange au deck de rencontre a l'etape 3A.
        "Gorr the God Butcher", "Necroverse",
    ]

    BASIC_POWER = Literal["ATK", "THW", "REC", "SCH", "DEF"]

    def __init__(self, paper: 'Paper') -> None:
        self.paper = paper
        self.card: Card

        if paper.pic_id:
            pic_id = paper.pic_id
        else:
            pic_id = paper.card_id
        self.pic_id: str = pic_id

        from game.card.face.effect.face_ability import FaceAbility
        from game.card.face.effect.face_effect import FaceEffect
        self.ability = FaceAbility(self)
        self.effect = FaceEffect(self)

        self.keywords: Dict["CardFace.KEY", Dict['CardFace', int]] = {}
        self.ignore_keywords: Dict["CardFace.IGNORE_KEY", Dict['CardFace', int]] = {}

        self.SetName(paper.name)
        self.SetSubtitle(paper.subtitle)

        self.crc: Dict[str, int] = {}
        super().__init__()

    @property
    def crc_value(self) -> int:
        return sum(self.crc.values())

    @property
    def crc_dict(self):
        return self.crc

    @final
    def Initialize(self, player_num: int):
        # self.ResetKeywords()
        self.OnInitModel()
        # self.ResetConsiderAs()

        from game.card.face.attribute.has_attribute import HasAttribute
        if HasAttribute.IsType(self):
            self.SetPlayerNum(player_num)
            for key in self.paper.desc:
                self.InitPrintedValue(key, self.paper.desc[key])

            from build import Build
            if not Build.release:
                self.CheckPrintedValue()

    ################################################################################
    # Ability
    def GetAbilities(self) -> List['Ability']:
        return []

    @property
    def effects(self) -> Sequence['Effect']:
        return self.effect.GetAll()

    ################################################################################
    # Keyword
    @final
    def SetKeywords(self, value: int, keyword: "CardFace.KEY", by_effect: 'Effect'):
        assert keyword == "Boost"
        self.keywords[keyword] = {}
        self.GainKeyword(value, keyword, by_effect)

    @final
    def GainKeyword(self, diff: int, keyword: "CardFace.KEY", by_effect: 'Effect', *, render_ui: bool=False):
        if diff == 0:
            return
        # When `OnResetKeywords`, the unit still not in play
        # assert self.IsInPlay()
        Message.WhenCardWouldUpdateKeyword_Text(self, diff, keyword, by_effect, render_ui=render_ui)

        face = by_effect.this
        if keyword in self.keywords:
            if face in self.keywords[keyword]:
                self.keywords[keyword][face] += diff
            else:
                self.keywords[keyword][face] = diff
        else:
            self.keywords[keyword] = {}
            self.keywords[keyword][face] = diff

        # Fix "19018"
        # if keyword not in ['ATK']:
        #     assert self.keywords[keyword][face] >= 0

        if self.keywords[keyword][face] == 0:
            del self.keywords[keyword][face]
            if self.keywords[keyword] == {}:
                del self.keywords[keyword]

        message = Message.WhenCardKeywordUpdated(self, diff, keyword, by_effect)
        message.Send()

    @final
    def SetIgnoreKeyword(self, diff: int, keyword: "CardFace.IGNORE_KEY", by_effect: 'Effect'):
        if diff == 0:
            return

        face = by_effect.this
        if keyword in self.ignore_keywords:
            if face in self.ignore_keywords[keyword]:
                self.ignore_keywords[keyword][face] += diff
            else:
                self.ignore_keywords[keyword][face] = diff
        else:
            self.ignore_keywords[keyword] = {}
            self.ignore_keywords[keyword][face] = diff

        if self.ignore_keywords[keyword][face] == 0:
            del self.ignore_keywords[keyword][face]
            if self.ignore_keywords[keyword] == {}:
                del self.ignore_keywords[keyword]

        # Send.WhenCardKeywordUpdated(self, diff, keyword, by_effect)

    @final
    def GetKeyword(self, keyword: "CardFace.KEY") -> int:
        """Vivian would treat any icons on the attachment or side scheme as blank until the end of the round."""
        if keyword in self.ignore_keywords:
            value = 0
            for face in self.ignore_keywords[keyword]:
                value += self.ignore_keywords[keyword][face]
            if value > 0:
                return 0
        as_blank = False
        if self.is_treat_as_if_blank and keyword in [
            "Toughness", "Guard", "Quickstrike", "Retaliate", "Surge",
            "Hazard", "Crisis", "Acceleration", "Amplify",
            "Restricted",
            "MaxPerUnit", "MaxPerDeck", "TeamUp",
            "Permanent", "Steady", "Incite", "Villainous", "Patrol", "Hinder",
            "Requirement", "Victory",
        ]:
            as_blank = True
        if keyword in self.keywords:
            value = 0
            for face in self.keywords[keyword]:
                if not as_blank or \
                    as_blank and face != self:
                    value += self.keywords[keyword][face]
            return value
        else:
            return 0

    def BonusParSource(self) -> 'Dict[str, List[List[Any]]]':
        """Les bonus d'ATK et de DEF, chacun avec la carte qui le donne
        (`[nom, object_id, valeur]`). La carte elle-meme (sa valeur de base,
        posee par `OnResetKeywords`) n'en est pas un. Sous garde : un rendu
        n'a pas a pouvoir tomber pour un affichage."""
        resultat: 'Dict[str, List[List[Any]]]' = {}
        try:
            for cle in ('ATK', 'DEF'):
                lignes = [[face.name, face.card.object_id, valeur]
                          for face, valeur in self.keywords.get(cle, {}).items()
                          if face is not self and face.card is not self.card and valeur != 0]
                if lignes:
                    resultat[cle] = lignes
        except Exception:
            return {}
        return resultat

    @final
    def ResetKeywords(self):
        self.keywords = {}
        self.ignore_keywords = {}
        from game.effect.rule import ResetKeyword
        self.OnResetKeywords(ResetKeyword(self))

    ################################################################################
    #
    @final
    def GetRenderInfo(self) -> Dict[str, int]:
        info = self.GetInfoDict()
        self.crc = {
            'is_exhaust': int(not self.card.state.is_ready),
            'traits': self.GetTraitsTotalCount(),
        } | info
        self.crc = {key: value for key, value in self.crc.items() if value != 0 and key != 'curr_ally_limit' and key != 'curr_restricted_limit'}

        if not self.IsFaceUp():
            return {}
        elif self.IsInPlay() or self.card.area.flags.is_boost_area:
            return info
        else:
            return {}

    def GetInfoDict(self) -> Dict[str, int]:
        info: Dict[str, int] = {}
        if self.is_treat_as_if_blank:
            info |= {'treat_as_if_blank': 1}
        if str(self.consider_as):
            info |= {'consider_as': 1}
        if self.card.area.GetOwner().IsPlayer():
            info |= {'with_player': self.card.area.GetOwnerPlayer().player_id + 1}
        return info

    @final
    def __repr__(self) -> str:
        return self.GetDisplayName()

    @final
    def GetReplayText(self) -> str:
        return f"c{self.card.object_id} {self.paper.card_id}"

    ################################################################################
    #
    # Notice: Call `.card.CastTo` if card face has been change
    @final
    def CastTo(self, face_type: Type[TF]) -> TF:
        face = self
        if not Build.release:
            if str(face_type) == "Villain" and face.paper.card_id == "53038":
                return self # type: ignore
            else:
                assert face.IsTypeOld(face_type), f"{self=} {face_type=}"
        return Cast(face_type, face)

    @classmethod
    def IsType(cls: Type[TF], face: 'CardFace|Effect|None', check_consider: bool=True) -> TypeGuard['TF']:
        if isinstance(face, CardFace):
            if cls.is_final:
                if type(face) is cls or cls in type(face).also_final_types:
                    return True
            else:
                if isinstance(face, cls):
                    return True
            if check_consider:
                if face.IsConsiderAs(card_type=cls):
                    return True
        if isinstance(face, Effect):
            return cls.IsType(face.this.card.face)
        return False

    @classmethod
    def IsReallyType(cls: Type[TF], face: 'CardFace|Effect|None') -> TypeGuard['TF']:
        return cls.IsType(face, check_consider=False)

    def IsTypeOld(self, face_type: Type[TF]) -> bool:
        card_types = Types.UnionTypeExtract(face_type)
        def is_list_of_types(x: List[Any]) -> TypeGuard[List[Type[CardFace]]]:
            return all(isinstance(item, type) for item in x)
        assert is_list_of_types(card_types)
        return any(x.IsType(self) for x in card_types)

    ################################################################################
    # Action
    # Do NOT overwrite those function, over write `OnXXXX` instead
    @final
    def ReadyInternal(self, by_effect: 'Effect', *, ui_group: bool=False) -> bool:
        return self.card.Ready(by_effect, ui_group=ui_group)

    @final
    def ExhaustInternal(self, by_effect: 'Effect', *, ui_group: bool=False) -> bool:
        assert self.IsInPlay()
        return self.card.Exhaust(by_effect, ui_group=ui_group)

    def OnRemoveFromGame(self, message: 'Message.AfterCardRemoveFromGame') -> None:
        from game.effect.rule import GameRule
        rule = GameRule(self)
        self.card.components.OnRemove(rule)
        message.Send()

    @final
    def SetAsideInternal(self, effect: 'Effect', *, ui_group: bool=False) -> bool:
        return self.card.SetAside(effect, ui_group=ui_group)

    @final
    def DiscardInternal(self, by_effect: 'Effect', *, into_area: 'Literal["Owner"]|Deck|None'=None, ui_group: bool=False, ignore_identity: bool=False) -> bool:
        from game.card.face.card_type import Identity
        from game.card.face.card_type import Minion
        from game.card.face.attribute.has_permanent import HasPermanent

        if self.card.state.is_discarding:
            return False

        self.card.state.is_discarding = True

        def do_discard():
            area = self.card.area
            if not ignore_identity:
                assert not Identity.IsType(self)
            if HasPermanent.IsType(self):
                if self.permanent:
                    bind_face = self.bind_face
                    if bind_face:
                        # Fix "46002" and "51036"
                        if not Minion.IsType(bind_face):
                            controller = bind_face.GetControlBy()
                            if Player.IsType(controller):
                                assert controller.is_eliminated
                    else:
                        return False
            if self.card.Discard(by_effect, into_area=into_area, ui_group=ui_group, up_face=self):
                if not ui_group and \
                    area.flags.is_deck and \
                    area.GetSize() == 0 and \
                    not area.GetOwner().is_eliminated:
                    assert False
                return True
            return False

        result = do_discard()
        self.card.state.is_discarding = False
        return result

    @final
    # Call `SpecialAttack` if the damage is from an event card
    def DealIndirectDamage(self, unit: 'Unit2', damage: int, by_effect: 'Effect'):
        return unit.TakeIndirectDamage(self, damage, by_effect)

    @final
    def DealDamageTotal(self, units: Sequence['TC'], value: int, by_effect: 'Effect') -> int|None:
        return self.DealDamage(units[:value], 1, by_effect)

    @final
    def AttackDamage(self, units: Sequence['TC'], damage: 'int|DamageProperty', by_effect: 'Effect', *, property: 'AttackProperty|None'=None,
            if_this_attack_defeats: Callable[['Unit2'], None]|None=None,
            if_this_attack_deal_excess_damage: Callable[[int], None]|None=None) -> int|None:

        return self.DealDamage(
            units,
            damage,
            by_effect,
            property=property,
            attack_in_event=True,
            if_this_attack_defeats=if_this_attack_defeats,
            if_this_attack_deal_excess_damage=if_this_attack_deal_excess_damage
        )

    @final
    def DealDamage(self, units: Sequence['TC'], damage: 'int|Literal["5*"]|DamageProperty', by_effect: 'Effect', *, property: 'AttackProperty|None'=None,
            attack_in_event: bool=False,
            if_this_attack_defeats: Callable[['Unit2'], None]|None=None,
            if_this_attack_deal_excess_damage: Callable[[int], None]|None=None,
            # choose_order: bool=False
            ) -> int|None:
        from game.card.face.base import Unit2
        from game.card.face.base import EncounterCard
        from game.card.face.base import Villain
        from game.ability.factory import AbilityFactory
        from game.ability import AbilityType
        from game.operate.filter import Filter
        from game.operate.effects import Effects
        from game.operate.worlds import Worlds

        temp_effects: List[Effect] = []
        if if_this_attack_defeats:
            ability = AbilityFactory.AfterUnitDefeatedUnit(
                AbilityType.Temp0,
                None, # self is this card, not the hero
                units,
                lambda defeated_effect, defeated_message:
                    if_this_attack_defeats(defeated_message.target)
            )

            temp_effects += self.effect.RegisterTemp(
                ability,
                unregister_after_exec=False,
            )
        if if_this_attack_deal_excess_damage:
            ability = AbilityFactory.AfterUnitDealExcessDamage(
                AbilityType.Temp0,
                None,
                lambda effect, message:
                    if_this_attack_deal_excess_damage(message.excess_damage),
                by_effect=by_effect
            )

            temp_effects += self.effect.RegisterTemp(
                ability,
                unregister_after_exec=False,
            )

        units2 = Filter.ByType(units, Unit2)
        if isinstance(by_effect.this, EncounterCard|Villain) and units2:
            player = Worlds.GetFirstPlayer(by_effect)
            if Player.IsType(units2[0].GetControlBy()):
                check_player = units2[0].GetControlByPlayer()
                if all(x.GetControlBy() == check_player for x in units2):
                    player = check_player
            units2 = player.ChooseOrder(units2, prompt="Take Damage")

        if isinstance(damage, str):
            damage = Worlds.ConvertPerPlayerIconToInt(damage, by_effect)
        total_damage = self.OnDealDamage(units2, damage, by_effect, property=property, attack_in_event=attack_in_event)

        Effects.UnRegister(temp_effects)
        return total_damage

    @final
    def PlaceThreatOnSchemes(self, schemes: Sequence['TC']|Literal["MainScheme", "EachMainScheme", "EachSideScheme", "EachScheme"], value: int|Literal["1*", "2*", "3*"], by_effect: 'Effect', *, if_not_trigger_forced_response: Callable[..., None]|None=None) -> int|None:
        from game.card.face.base import Scheme2
        from game.operate.faces import Faces
        from game.operate.filter import Filter
        from game.operate.worlds import Worlds
        from game.ability.factory import AbilityFactory
        from game.operate.effects import Effects

        total = None
        rest_faces: List['CardFace'] = []

        target_schemes: List['CardFace']

        if schemes == "EachSideScheme":
            target_schemes = list(Worlds.GetSideSchemes(by_effect))
        elif schemes == "MainScheme":
            scheme = Worlds.FindMainScheme(by_effect)
            if scheme:
                target_schemes = [scheme]
            else:
                return None
        elif schemes == "EachMainScheme":
            target_schemes = list(Worlds.GetAllMainSchemes(by_effect))
        elif schemes == "EachScheme":
            target_schemes = list(Worlds.GetOnFieldSchemes(by_effect))
        else:
            target_schemes = list(schemes)

        filtered_schemes = Filter.ByType(target_schemes, Scheme2, return_rest_faces=rest_faces)
        value = Worlds.ConvertPerPlayerIconToInt(value, by_effect)

        check_effects: List['Effect'] = []
        trigger_forced_response = False
        if if_not_trigger_forced_response:
            def set_trigger_forced_response():
                nonlocal trigger_forced_response
                trigger_forced_response = True
            check_effects = self.effect.Registers(
                AbilityFactory.WhenCardWouldResolveAbility(
                    AbilityType.Temp0,
                    ["ForcedResponse"],
                    None,
                    lambda effect, message:
                        set_trigger_forced_response(),
                    conditions=[
                        lambda effect, message:
                            message.trigger in target_schemes
                    ]
                )
            )

        for scheme in filtered_schemes:
            message = scheme.PlaceThreatInternal(value, by_effect)
            if message:
                if total == None:
                    total = 0
                total += message.value
        if rest_faces:
            assert False
            Faces.PlaceTokensOn(rest_faces, value, 'threat', by_effect)

        if if_not_trigger_forced_response:
            if not trigger_forced_response:
                if_not_trigger_forced_response()

        Effects.UnRegister(check_effects)

        return total

    @final
    def RemoveThreatFromSchemesTotal(self, schemes: Sequence['TC'], value: int, by_effect: 'Effect') -> int|None:
        return self.RemoveThreatFromSchemes(schemes[:value], 1, by_effect)

    @final
    def RemoveThreatFromSchemes(self, schemes: Sequence['TC']|Literal["MainScheme", "EachScheme", "YourLeaderMainScheme"], value: int|Literal["All", "1*", "3*", "5*"], by_effect: 'Effect', *, if_this_remove_last_threat: Callable[[], None]|None=None, ignore_crisis: bool=False) -> int|None:
        from game.card.face.base import Scheme2
        from game.ability.factory import AbilityFactory
        from game.ability import AbilityType
        from game.operate.faces import Faces
        from game.operate.filter import Filter
        from game.operate.effects import Effects
        from game.operate.worlds import Worlds
        remove_counter = 0

        target_schemes: List['CardFace']

        if schemes == "YourLeaderMainScheme":
            # Le complot principal de VOTRE leader est sur la table d'en face :
            # les equipes echangent leurs scenarios (mc56 p.14, etape 4).
            # En cooperatif il n'existe pas, et le livret p.6 tranche : « a card
            # ability that refers to your leader cannot be resolved ». D'ou la
            # liste vide, qui est le comportement d'avant.
            target_schemes = []
            world = by_effect.world
            if world.rule.mode_competitive:
                team = Worlds.GetTeamOfEffect(by_effect)
                other_area = world.GetTeamGameArea(world.GetOtherTeam(team))
                target_schemes = list(Worlds.GetMainSchemes(other_area))
        elif schemes == "MainScheme":
            scheme = Worlds.FindMainScheme(by_effect)
            if scheme:
                target_schemes = [scheme]
            else:
                return None
        elif schemes == "EachScheme":
            target_schemes = list(Worlds.GetOnFieldSchemes(by_effect))
        else:
            target_schemes = list(schemes)

        rest_faces: List['CardFace'] = []
        schemes2 = Filter.ByType(target_schemes, Scheme2, return_rest_faces=rest_faces)
        if schemes2:
            temp_effects: List[Effect] = []
            if if_this_remove_last_threat:

                ability = AbilityFactory.AfterSchemeRemoveThreat(
                    AbilityType.Temp0,
                    schemes2,
                    lambda defeated_effect, defeated_message:
                        if_this_remove_last_threat(),
                    last_threat=True,
                )

                temp_effects += self.effect.RegisterTemp(
                    ability,
                    unregister_after_exec=False,
                )


            if ignore_crisis:
                temp_effects += self.effect.RegisterTemp(
                    AbilityFactory.UnitIgnoreKeywordIcons(
                        by_effect.initiator.GetRoleCharacter(),
                        crisis=True
                    ),
                    unregister_after_exec=False
                )
                temp_effects += self.effect.RegisterTemp(
                    AbilityFactory.UnitIgnoreKeywordIcons(
                        by_effect.this,
                        crisis=True
                    ),
                    unregister_after_exec=False
                )

            if value == "All":
                remove_counter = self.DefaultRemoveSchemeThreat(self, schemes2, value, by_effect)
            else:
                from game.operate.worlds import Worlds
                value = Worlds.ConvertPerPlayerIconToInt(value, by_effect)
                remove_counter = self.OnRemoveSchemeThreat(schemes2, value, by_effect)

            Effects.UnRegister(temp_effects)

        if rest_faces:
            assert False
            remove_counter = Faces.RemoveTokensOn(rest_faces, value, 'threat', by_effect, forced=True)

        return remove_counter

    @final
    def HealthUnits(self, units: Sequence['CardFace']|Literal["EnemyLeader"], value: int|Literal["All", "Printed", "1*", "2*", "5*"], by_effect: 'Effect') -> int:
        from game.card.face.base import Unit2
        from game.operate.faces_helper import FacesHelper
        from game.operate.worlds import Worlds

        if units == "EnemyLeader":
            leader = Worlds.GetEnemyLeader(by_effect)
            if leader:
                units = [leader]
            else:
                return 0

        total = 0
        units_dict = FacesHelper.ListToDict(units)

        for unit in units_dict:
            unit = unit.CastTo(Unit2)
            if value == "All" or value == "Printed":
                message =  unit.HealHealth(value, by_effect)
            else:
                value = Worlds.ConvertPerPlayerIconToInt(value, by_effect)
                heal_value = value * units_dict[unit]
                message =  unit.HealHealth(heal_value, by_effect)
            if message:
                total += message.value
        return total

    ################################################################################
    #
    @final
    def ResolveSpecialAbility(self, player: 'Player|None', by_effect: 'Effect',
                              *,
                              name: str="",
                              sequence: Sequence['CardFace']=[]) -> bool:
        if self.is_treat_as_if_blank:
            return False
        if sequence == []:
            sequence = [self]
        from game.message import Message
        found_effects = self.effect.Find(type=AbilityType.Special)
        if found_effects:
            message = Message.WhenResolveSpecialAbility(self, name, sequence, player, by_effect)
            message.Send()
        return True

    @final
    def ResolvePreparationAbility(self, player: 'Player|None', by_effect: 'Effect'):
        from game.message import Message
        if self.is_treat_as_if_blank:
            return False
        found_effects = self.effect.Find(type=AbilityType.Preparation)
        if found_effects:
            message = Message.WhenResolvePreparationAbility(self, player, by_effect)
            message.Send()
        return True

    @final
    def ResolveAbility(self, player: 'Player', ability_type: 'AbilityType', by_effect: 'Effect', ref_message: 'Message2|None'=None) -> bool:
        if self.is_treat_as_if_blank:
            return False
        found_effects = self.effect.Find(type=ability_type)
        for found_effect in found_effects:
            # Fix "58014" with "01104"
            found_effect.checker.UpdateLegalTargets()
            min_target_num = found_effect.context.target_range[0]
            found_effect.context.targets_internal = found_effect.context.all_legal_targets[:min_target_num]
            # Fix "45158"
            found_effect.context.initiator = self.GetControlByOrOwner()
            return found_effect.ResolveToPlayer(player, by_effect, ref_message)
        return False

    ################################################################################
    #
    @final
    def GetOwner(self) -> 'Player|Scenario':
        owner = self.card.GetOwner()
        return owner
    @final
    def GetOwnerPlayer(self) -> 'Player':
        owner = self.GetOwner()
        assert isinstance(owner, Player)
        return owner
    @final
    def GetControlBy(self) -> 'Player|Scenario|None':
        return self.card.GetController()
    @final
    def GetControlByOrOwner(self) -> 'Player|Scenario|User':
        # Hack: "01084" "36038" "36037"
        if self.card.state.is_swapping_end:
            return self.GetOwner()

        controller = self.card.GetController()
        if controller == None:
            return self.GetOwner()
        else:
            return controller
    @final
    def GetControlByPlayer(self) -> 'Player':
        # player side schemes are controlled by the player that played them.
        from game.card.face.card_type import PlayerSideScheme
        if PlayerSideScheme.IsType(self):
            return self.GetOwnerPlayer()

        owner = None
        if self.IsInPlay():
            owner = self.GetControlByOrOwner()
        if owner == None:
            owner = self.GetOwner()
        assert isinstance(owner, Player)
        return owner
    @final
    def IsLikeInHand(self) -> bool:
        return self.card.IsInHand() or self.card.IsLikeInHand()
    @final
    def IsInPlay(self, *, is_same_face: bool=False) -> bool:
        from game.card.face.card_type import Identity

        def check_is_same_face():
            if not is_same_face:
                if self.card.face.IsName(self.name):
                    return True
                if Identity.IsType(self.card.face) and \
                    Identity.IsType(self):
                    return True
            return self.IsThisFaceUp()
        return self.card.IsOnField() and \
            check_is_same_face() and \
            self.IsFaceUp()
    @final
    def IsInProcessingArea(self) -> bool:
        return self.card.IsOnProcessingArea() and self.IsThisFaceUp()
    @final
    def IsInDeck(self) -> bool:
        return self.card.IsInDeck()
    @final
    def IsReady(self) -> bool:
        return self.card.IsReady()
    @final
    def IsExhaust(self) -> bool:
        return self.card.IsExhaust()
    @final
    def IsFaceUp(self) -> bool:
        return self.card.IsFaceUp()
    @final
    def IsThisFaceUp(self) -> bool:
        # (\w+).card.face == \1
        return self.card.face == self
    @final
    def CanExhaust(self) -> bool:
        return self.IsInPlay() and self.IsReady() # Maybe? self.limit_exhaust = []
    @final
    def CanReady(self) -> bool:
        return not self.card.IsReady()
    @final
    def IsCanReadyBy(self, by_effect: 'Effect') -> bool:
        if not self.CanReady():
            return False
        return self.card.IsCanReadyBy(by_effect)
    @final
    def Copy(self) -> 'CardFace':
        from copy import copy
        return copy(self)

    def IsDefeated(self) -> bool:
        return not self.IsInPlay()

    ################################################################################
    #
    @final
    @property
    def components(self):
        return self.card.components

    # GetAreaPlaced
    @final
    def GetPlacedCardArea(self) -> 'Deck':
        return self.components.placed_card.GetDeck()

    @final
    def TuckCardUnderHere(self, faces: 'CardFace'|Sequence['CardFace'], by_effect: 'Effect', *, peek: bool=False) -> bool:
        if peek:
            face_up = "Peek"
        else:
            face_up = False
        return self.PlaceCardHere(faces, face_up, by_effect)

    # PlaceCardUnder / StackCardHere
    @final
    def PlaceCardHere(self, faces: 'CardFace'|Sequence['CardFace'], face_up: bool|Literal["Peek"], by_effect: 'Effect', *, still_in_play: bool=False) -> bool:
        from game.operate.faces import Faces

        if not self.card.IsOnField() and not self.card.area.flags.is_main_scheme_deck:
            return False
        if isinstance(faces, CardFace):
            faces = [faces]

        # Fix "44050" "44009"
        if face_up == False:
            for face in faces:
                face.card.visible.Update()
        # Fix "50100"
        if face_up == "Peek":
            for face in faces:
                face.card.visible.Set(True)
            face_up = False

        # Flip first fix "03002"
        Faces.FlipAllTo(faces, face_up, by_effect)
        # if still_in_play:
        #     moved_faces = Faces.MoveAllTo(faces, self.card.area, by_effect)
        moved_faces = Faces.MoveAllTo(faces, self.GetPlacedCardArea(), by_effect)
        return moved_faces == faces

    @final
    def GetInventoryDeck(self) -> Deck2['Asset2']:
        return self.components.inventory.GetDeck()

    @final
    def GetAttachedUpgrades(self) -> List['Upgrade']:
        from game.card.face.card_type import Upgrade
        faces = self.components.inventory.GetDeck().FindCards(card_type=Upgrade)
        return faces

    @final
    def GetAttachedAttachments(self) -> List['Attachment']:
        from game.card.face.card_type import Attachment
        faces = self.components.inventory.GetDeck().FindCards(card_type=Attachment)
        return faces

    @property
    def bind_face(self) -> 'CardFace|None':
        return None
        # assert False, f"You need to override this function, {self=}"

    # @final
    def GetBindFace(self) -> 'CardFace':
        face = self.bind_face
        assert face
        return face

    @final
    def FlipTo(self, by_effect: 'Effect',
               *,
               face_up: bool|None=None,
               trait: "CardFace.TRAITS|None"=None,
               card_face: 'CardFace|None'=None, # to_face
               card_type: 'Type[TC]|None'=None, # to_type
               name: str|None=None, # to_name
               ui_group: bool=False,
               ui_look_at: bool=False,
               by_swapping: bool=False) -> bool:
        if self.card.state.is_face_up != face_up and self.card.back_faces == []:
            self.card.Flip(by_effect, ui_group=ui_group, ui_look_at=ui_look_at)
            return True
        if card_face != None:
            if self.card.back_faces[0] != card_face:
                self.card.back_faces.remove(card_face)
                self.card.back_faces = [card_face] + self.card.back_faces
            self.card.Flip(by_effect, ui_group=ui_group, ui_look_at=ui_look_at, by_swapping=by_swapping)
            return True

        if card_type != None:
            for face in self.card.back_faces:
                if card_type.IsType(face):
                    return self.FlipTo(by_effect, card_face=face, ui_group=ui_group, ui_look_at=ui_look_at, by_swapping=by_swapping)
        if trait != None:
            for face in self.card.back_faces:
                if face.HasTrait(trait):
                    return self.FlipTo(by_effect, card_face=face, ui_group=ui_group, ui_look_at=ui_look_at, by_swapping=by_swapping)
        if name != None:
            for face in self.card.back_faces:
                if face.IsName(name):
                    return self.FlipTo(by_effect, card_face=face, ui_group=ui_group, ui_look_at=ui_look_at, by_swapping=by_swapping)
        return False

    def CanPlayBy(self, player: 'Player') -> bool:
        return False

    ################################################################################
    #
    @final
    def CanResolveWhenRevealed(self) -> bool:
        if not self.IsFaceUp():
            return False

        return self.card.state.is_revealing

    ################################################################################
    #
    TB = TypeVar("TB", bound=Buff)
    @final
    def GetBuff(self, type: Type['TB']) -> 'TB':
        return self.card.components.buffs.GetBuff(type)

    @final
    def GetBuffsText(self) -> Dict['str', 'str']:
        texts: Dict[str, str] = {}
        for buff in self.card.components.buffs.GetBuffs():
            if buff:
                texts[buff.name] = buff.GetText()
        return texts

