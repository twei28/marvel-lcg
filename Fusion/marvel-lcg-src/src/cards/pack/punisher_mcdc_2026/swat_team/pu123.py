from . import *

# Tactical Sniper — SBIRE x2. POLICE. SCH 1★, ATQ 3★, 4 PV, Boost 2, Vulnerable.
# Vulnerable.
# ★ When Tactical Sniper schemes, place that threat on SWAT, if able.
# ★ Forced Interrupt : When Tactical Sniper would attack, if there are fewer than 3 wanted counters on SWAT, it attacks
#   the enemy with the fewest remaining hit points without the POLICE trait instead.
#
# Cartes de reference : `MenaceSurSwat()`, jigsaw/pu059.py (`SetBeInstead`), `Enemy.AttackCharacter` (brique commune).
# ⚠ « the ENEMY with the fewest HP WITHOUT POLICE » : sbires ET vilain, jamais un POLICE ni lui-meme ; a egalite le
# premier joueur choisit ; aucune cible = il attaque normalement (le « instead » n'a rien a remplacer). Vulnerable : natif.

def GetAbilities() -> Sequence['Ability']:
    en_cours = {'oui': False}   # ⚠ l'attaque de remplacement repasse par `WhenUnitWouldAttack` : sans ce garde, boucle infinie

    def au_lieu_d_attaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        if en_cours['oui']:
            return
        this = effect.this.CastTo(Enemy)
        cibles = [e for e in Worlds.GetOnFieldEnemies(effect) if e is not this and not e.HasTrait("POLICE")]
        if not cibles:
            return
        mini = min(e.health for e in cibles)
        ex_aequo = [e for e in cibles if e.health == mini]
        premier = Worlds.GetFirstPlayer(effect)
        cible = ex_aequo[0] if len(ex_aequo) == 1 else premier.AskChooseFace(ex_aequo, effect)
        if cible is None:
            return
        message.SetBeInstead(effect)
        en_cours['oui'] = True
        try:
            this.AttackCharacter(cible, effect)
        finally:
            en_cours['oui'] = False

    return [
        MenaceSurSwat(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt, "This", au_lieu_d_attaquer,
            conditions=[lambda effect, message: CompteursRecherche(effect) < 3],
        ),
    ]
