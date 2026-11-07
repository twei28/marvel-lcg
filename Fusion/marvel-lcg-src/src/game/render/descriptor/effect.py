from core import *

# data.ts
@dataclass
class EffectDescriptor:

    @dataclass
    class Payment:
        cost: str
        payment: List[Dict[int, str]] # `effect_id` `res_text`
        rule: List[str]
        # AJOUT 11/09/2026. Vide, ou {"keyword": "Crisis"|"Patrol",
        # "paid_with": "B", "mode": "any"|"only"} : « paye sans cette couleur
        # (mode any : au moins une ; only : rien d'autre), ce coup ne produira
        # aucun effet » (le complot vise est verrouille et la carte ne
        # l'ignore qu'a cette condition). Le plateau affiche une confirmation
        # AVANT d'envoyer la reponse ; il ne connait ni la carte ni la regle,
        # seulement ceci.
        warning: Dict[str, str]

    id: int                         # game object id
    name: str
    bind_id: int                    # link `CardState.id`
    bind_player_id: int             # [0,1,2,3]
    all_legal_targets: List[int]    # link `CardState.id`
    target_num_range: List[int]     # target [min, max] number
    target_payment: Dict[int, Payment]

    select_rule: str
    select_rule_param: Tuple[int, int]
    target_must_include_traits: List[str] # For "26035"

    failure_reason: str             # not null if fail
    is_search: bool
    # Option de cout d'une carte rencontre reduite au plus gros morceau payable : le plateau la surligne.
    au_maximum: bool = False
    # AJOUT 07/11/2026 : cette option vient d'`AskChooseOneText`/`ForChoiceAbility` (le moteur ne
    # transporte que le NOM de la carte, `bind_id` vaut l'identite du joueur, jamais la carte choisie).
    # Signale au plateau de retrouver la vraie carte par son nom et de l'afficher en grille de vignettes
    # plutot qu'en bouton de texte brut (ui-app/src/board/option-carte.ts, DemandeCentrale.tsx).
    is_text_choice: bool = False

    # is_ex_effect check `AskOption`

