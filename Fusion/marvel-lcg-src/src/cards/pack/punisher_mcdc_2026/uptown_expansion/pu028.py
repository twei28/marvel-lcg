from . import *

# Bronx Bombered (U3) — PISTE Uptown. Response : While in The Bronx, after you deal damage to the villain, place an equal amount of damage here. Then, if there is damage here
#   equal to or greater than the villain's printed hit points, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : `AbilityFactory.AfterFaceDealDamage` (game/ability/factory/damage.py, `message.dealt_damage`), leads_the_big_apple/pu044 (jetons `damage`,
# `Faces.PlaceTokensOn`, `PisteTerminee`), the_big_apple `LeVilain` (« the villain » d'un joueur = le CAPO de SA zone).
# ⚠ Mots-pieges :
#  - « AFTER you deal damage » (contrairement a pu044, « instead ») : le vilain SUBIT les degats ET la piste en recoit autant (`dealt_damage` = degats reellement infliges,
#    apres boucliers) ; « you » = identite ou allie du joueur (comme les autres pistes) ;
#  - « THE villain » = le CAPO de la zone du joueur (`LeVilain`), pas un autre CAPO d'une autre rangee ;
#  - « equal to or GREATER than the villain's PRINTED hit points » : PV IMPRIMES du CAPO (`printed_health_numeral`, non multiplies par joueur), pas ses PV restants ;
#  - jetons de DEGATS (`damage`), pas un compteur.

def GetAbilities() -> Sequence['Ability']:

    def mon_personnage_sur_le_vilain(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> bool:
        joueur = Joueur(effect)
        vilain = LeVilain(effect, joueur) if joueur is not None else None
        touches = message.who_took_damage if isinstance(message.who_took_damage, (list, tuple)) else [message.who_took_damage]   # `who_took_damage` : une LISTE de faces
        return (joueur is not None and vilain is not None and any(f is vilain for f in touches)
                and message.trigger is not None and ControlePar(message.trigger, joueur))

    def apres(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> None:
        this = effect.this
        joueur = Joueur(effect)
        Faces.PlaceTokensOn([this], message.dealt_damage, 'damage', effect)
        vilain = LeVilain(effect, joueur)
        if vilain is not None and this.GetTokens('damage') >= vilain.printed_health_numeral:
            PisteTerminee(effect, joueur)

    return [
        AbilityFactory.AfterFaceDealDamage(AbilityType.Response, Friend, Villain, apres, conditions=[EnLieu(LIEU_U3), mon_personnage_sur_le_vilain]),
    ]
