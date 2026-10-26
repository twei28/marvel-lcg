from cards.pack import *
from game.selector import Select
from cards.pack.fne import PeutCouvrirLeCout

# ===========================================================================
# SPIDER-PUNISHER (T-Wrecks, Terre-71928, prefixe `sq`, set 221) — helpers partages du pack.
#
# LE MOTEUR DU PACK : des ameliorations WEB-SHOOTER (TECH, WEAPON) qu'on inclinera pour payer / declencher
# des effets, et que Web-Sling redresse a la fin de la phase joueur.
#
# TRAIT AERIAL (corrige le 26/10/2026) : « You gain the AERIAL trait when 2 or more upgrades you control are exhausted »
# (sq005 Neighborhood Watch) est un VRAI trait pose sur l'identite (`GiveKeywordToAttached("You", trait="AERIAL",
# get_new_value=..., ex_change_on_event=...)`, recalcule a chaque inclinaison / redressement). `EstAerien` (sq005, sq012) lit ce
# trait ; une carte d'un AUTRE pack qui teste AERIAL sur l'identite le voit aussi.
# ===========================================================================
WEB_SHOOTER = "WEB-SHOOTER"


def AmeliorationsDe(joueur: 'Player') -> List['CardFace']:
    """Les ameliorations que ce joueur controle (attachees a son identite, ses allies, ses soutiens)."""
    vues: List['CardFace'] = []
    for face in joueur.GetControlCards():
        for f in [face, *face.GetInventoryDeck().Get()]:
            if Upgrade.IsType(f) and f not in vues:
                vues.append(f)
    return vues


def EstWebShooter(face: 'CardFace|None') -> bool:
    return face is not None and Upgrade.IsType(face) and face.HasTrait(WEB_SHOOTER)


def EstArmeOuTech(face: 'CardFace|None') -> bool:
    return face is not None and Upgrade.IsType(face) and (face.HasTrait("WEAPON") or face.HasTrait("TECH"))


def ArmesOuTechPretes(joueur: 'Player') -> List['CardFace']:
    return [f for f in AmeliorationsDe(joueur) if EstArmeOuTech(f) and f.IsReady()]


# Redevient vrai a chaque inclinaison ou redressement de carte : l'evenement qui recalcule le trait AERIAL de sq005.
SurInclinaisonOuRedressement = OnEvent.TemplateTrigger(Message.AfterCardExhausted | Message.AfterCardReady)


def deux_ameliorations_inclinees(effect: 'Effect', attach: Any, ui: List['CardFace']) -> int:
    """« 2 or more upgrades you control are exhausted » : 1 si le joueur de la carte en a au moins 2 d'inclinees (Watch comprise)."""
    joueur = effect.this.GetControlByOrOwner()
    if not Player.IsType(joueur):
        return 0
    return 1 if sum(1 for f in AmeliorationsDe(joueur) if not f.IsReady()) >= 2 else 0


def EstAerien(joueur: 'Player|None') -> bool:
    """« If you have the AERIAL trait » : le VRAI trait de l'identite (pose par sq005 Neighborhood Watch, ou par une carte d'un
    autre pack). Plus de raccourci : toute carte qui teste AERIAL voit la meme chose."""
    return joueur is not None and joueur.GetIdentity().HasTrait("AERIAL")


def SourceDeLAttaque(message: 'Any') -> 'CardFace|None':
    """La carte dont l'effet porte l'attaque (l'amelioration d'une Hero Action (attack)). Sur le message
    `CheckIfAttackMessageHasKeyword`, `would_atk_message` est None : l'attaque se lit sur `check_attack.by_effect`."""
    attaque = getattr(message, "check_attack", None)
    return getattr(getattr(attaque, "by_effect", None), "this", None)


def AttaqueDeCetteCarte(effect: 'Effect', message: 'Any') -> bool:
    return SourceDeLAttaque(message) is effect.this


def DegatOuMenace(effect: 'Effect', this: 'CardFace', joueur: 'Player', *, facultatif: bool=False) -> None:
    """« deal 1 damage to an enemy or remove 1 threat from a scheme » (Web-Sling, Enhanced Combat Sense)."""
    def frapper(cibles: Sequence['CardFace']) -> None:
        this.DealDamage(cibles, 1, effect)

    def retirer(cibles: Sequence['CardFace']) -> None:
        this.RemoveThreatFromSchemes(cibles, 1, effect)

    options = [
        AbilityFactory.ForChoiceAbility("Deal 1 damage to an enemy", frapper).SetTarget(Enemy),
        AbilityFactory.ForChoiceAbility("Remove 1 threat from a scheme", retirer).SetTarget(Scheme2),
    ]
    if facultatif:
        joueur.MayChooseOneAbility(effect, *options)
    else:
        joueur.ChooseAbilities(effect, *options)


def RessourceEnhancedCombatSense(cout: 'Any') -> 'Ability':
    """« You can exhaust any number of WEAPON or TECH upgrades you control to generate that many [wild] resources while
    paying for this card » (sq002). UNE capacite de ressource par amelioration (le paiement n'emploie chaque source
    qu'UNE fois) : les quatre ameliorations du pack (sq008-sq011) la portent, et l'identite (sq001a) la porte pour une
    autre arme/tech d'un autre pack. Chaque emploi consigne +1 sur l'effet de la carte PAYEE (`sq_ameliorations_epuisees`),
    relu par sq002 (« for each upgrade you exhausted to pay for this card »)."""
    def noter(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        payee = message.for_effect
        for c in message.cost_check_effect.cost_func.GetAll():
            for face in getattr(c, "return_exhausted_cards", None) or []:
                payee.sq_ameliorations_epuisees = getattr(payee, "sq_ameliorations_epuisees", 0) + 1

    return AbilityFactory.CanGenerateResources(
        AbilityType.HeroResource,
        Resources("G"),
        for_card=CardFinder(name="Enhanced Combat Sense"),
        ex_operation=noter,
    ).SetName("Enhanced Combat Sense").SetCostFunc(cout)


def ActionPayable(cout: str, *, avec_firepower: bool=True) -> 'Callable[[Effect, Any], bool]':
    """Condition d'OFFRE d'une Hero Action a cout en ressource (« Spend a [x] resource and exhaust this card »).

    Le moteur OFFRE une telle action meme quand la main ne peut rien payer ; le paiement echoue alors
    (« WhenPlayerInTurn failed ») et le pilote d'autoplay repetait la meme action sans fin (4 parties sur 8
    bloquees, sq011). On ne l'offre que si les icones IMPRIMEES de la main et de la reserve couvrent le cout, ou si
    With Great Firepower (sq006, « generate a [wild] resource for an upgrade ability ») est prete. Ecart assume :
    les autres generateurs en jeu (supports d'autres packs) ne sont pas comptes."""
    def condition(effect: 'Effect', message: 'Any') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        if PeutCouvrirLeCout(joueur, effect, Cost(cout)):
            return True
        return avec_firepower and any(f.IsName("With Great Firepower") and f.IsReady() for f in AmeliorationsDe(joueur))
    return condition
