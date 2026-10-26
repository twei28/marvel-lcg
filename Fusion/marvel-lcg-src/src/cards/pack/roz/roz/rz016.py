from . import *

# Weighed Down — OBLIGATION (« Give to the Rosalind Solomon player »), boost 2.
# Forced Response: After you resolve the "Special" ability on a card you control, take 1 damage.
# Alter-Ego Action: Take 1 damage for each card you control with a "Special" ability (to a maximum of 5 damage).
#   If you take: • 2 or fewer damage → discard this card. • 3 or more damage → remove this card from the game.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Forced Response + degats a l'identite d'une obligation PERSISTANTE : `11018` Weakened
#    (`AfterUnitUseBasicPower(ForcedResponse, ...)` + `this.DealDamage(...)`), `04166` Anti-Hero Propaganda.
#  - « After you resolve a Special » : `storm/36007` (`AfterPlayerResolveAbility(..., which_abilities=["Special"],
#    control_by_you=True)`).
#  - Alter-Ego Action qui se defausse : `AbilityFactory.PlayerActionToDiscardThis` (`attachment.py`) ;
#    `Faces.RemoveAllFromGame([this], effect)` : `01160` Legal Work.
#  - « If you take N damage » : `DealDamage` rend le total reellement inflige (card_face.py:930).
#
# MOTS-PIEGES
#  - Forced Response : « AFTER you resolve ... ON A CARD YOU CONTROL » : le Special resolu sur une carte de ce
#    joueur (y compris celui de Roz elle-meme), UNE FOIS par Special resolu.
#  - « for each CARD YOU CONTROL WITH a Special ability » : les cartes qui IMPRIMENT un Special (`ADesSpecial`),
#    pas le nombre de Specials resolus ; plafond 5.
#  - « If you TAKE » : les degats REELLEMENT subis (apres prevention / Tough), pas le nombre annonce.
#  - « 2 OR FEWER » (0, 1 ou 2) → defausse ; « 3 OR MORE » → RETIREE de la partie. Zero carte a Special = 0 degat
#    = defausse.
def GetAbilities() -> Sequence['Ability']:

    def apres_special(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Obligation)
        # Le joueur qui resout le Special : une obligation en jeu n'a pas de controleur joueur evident, on lit le message.
        joueur = message.GetToPlayer() or JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.DealDamage([joueur.GetIdentity()], 1, effect)

    def en_civil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        porteuses = [f for f in joueur.GetControlCards() if f is not None and f.ability.Find(type=AbilityType.Special)]
        subis = this.DealDamage([joueur.GetIdentity()], min(5, len(porteuses)), effect) or 0
        if subis <= 2:
            Faces.DiscardAll([this], effect)
        else:
            Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.ForcedResponse,
            "You",
            None,
            apres_special,
            which_abilities=["Special"],
            control_by_you=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            en_civil,
        ),
    ]
