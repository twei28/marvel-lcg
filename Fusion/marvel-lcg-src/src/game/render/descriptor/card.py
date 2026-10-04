from core import *

# world_descriptor.ts
@dataclass
class CardDescriptor:
    id                  : int               # game object id
    is_ready            : bool
    is_face_up          : bool
    visible_for_players : List[int]         # which player can visit this card
    bind_object_id      : int               # is attach or inventory
    effect_by_cards     : List[int]
    effect_to_cards     : List[int]
    game_area           : int
    name                : str               # face up name
    info                : Dict[str, int]
    traits              : Dict[str, int]    # the `int` param should not be use
    buffs               : Dict[str, str]
    card_id             : str               # current face card_id
    pic_id              : str
    down_card_ids       : List[str]         # down face card_id
    effects             : List[int]         # link `EffectState.id`, only non-force
    resources           : List[int]         # link `EffectState.id`, only resources
    card_type           : str
    cost                : int
    crc                 : int
    is_new              : bool
    is_action           : bool
    # Les BONUS d'ATQ et de DEF, chacun avec la carte qui le donne :
    # {"ATK": [[nom, id, valeur], ...], "DEF": [...]} (04/10/2026, boutons de
    # defense « Ne pas défendre (ATQ 2 + 1 Charge + 1 carte boost) »). La valeur
    # imprimee de la carte elle-meme n'y figure pas.
    bonus               : Dict[str, List[List[Any]]] = field(default_factory=dict)
