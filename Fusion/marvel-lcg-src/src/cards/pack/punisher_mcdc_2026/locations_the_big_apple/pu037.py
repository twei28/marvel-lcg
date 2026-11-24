from . import *

# Financial District (8) — LIEU (environnement LOCATION).
# Hero Action: The villain attacks you. If you take less than 2 damage from this attack, draw 1 card for each printed ★ and [boost]
# on the attack's boost card(s). (Limit once per round.)
#
# Cartes de reference : 15030 (Bait and Switch : `Worlds.FindVillain(effect).DoAttackYou(joueur, effect)`), 27151 (Spiked Gauntlet : mesurer
# les degats de l'attaque), 53003 / 53036 (`FacesCounter.CountTotalBoostStarAndBoost(cartes)` = icones imprimees + etoiles), pu031 (limite globale + AuLieu).
# ⚠ « The villain » = le CAPO de la rangee du joueur (`Worlds.FindVillain(effect)`, par zone) ; « you take » = l'IDENTITE du joueur : un allie qui
# defend n'est pas « vous » (0 degat pour vous), une Tough sur l'identite empeche tout (0).
# ⚠ « less than 2 damage » : les icones de boost AJOUTENT de la force a l'attaque, donc plus la carte rapporte, moins on a de chances de tirer.
# ⚠ « Hero Action » : sous-type dedie (`AbilityType.HeroAction`), pas l'Action nue.

def GetAbilities() -> Sequence['Ability']:

    def attaque_puis_pioche(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        villain = Worlds.FindVillain(effect)
        if villain is None:
            return
        fin = villain.DoAttackYou(joueur, effect)
        if fin is None:
            return
        subis = 0
        cartes_boost: List['CardFace'] = []
        for atk in fin.atk_messages:
            attaque = atk.attacked
            cible = getattr(atk, 'defender', None) or (attaque[0] if isinstance(attaque, (list, tuple)) else attaque)
            if cible is identite:
                subis += getattr(atk, 'taken_damage', 0)
            cartes_boost += list(getattr(atk, 'boost_faces', []))
        if subis < 2:
            joueur.DrawUp(FacesCounter.CountTotalBoostStarAndBoost(cartes_boost), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, attaque_puis_pioche, conditions=[Ville.AuLieu])
        .LimitOncePerRound(),
    ]
