from . import *

# H.A.M.M.E.R. Operatives — SBIRE du deck REGISTERED (7/20), x3. 3 PV, ATQ 1,
# MNG 2, boost 2. AERIAL. H.A.M.M.E.R.
# Patrol.
# When Revealed: If this is the first card revealed from the REGISTERED deck
#   this round, put this card under your control as a REGISTERED ally.
# Counter Intelligence — Special: Exhaust this ally -> for each H.A.M.M.E.R.
#   character in play, remove 1 threat from a scheme.
#
# ⚠ LA JUMELLE DE `ip021` H.A.M.M.E.R. Commandos : voir son en-tete pour la
# lecture commune. Ici Patrol au lieu de Guard, et le contre au lieu du degat.
#
# TEXTE CONTRE CODE
#  ⚠ « remove 1 threat FROM A SCHEME » : une seule manigance, qui perd le
#    total. Principale ou secondaire, au choix du joueur.
#  ⚠ Patrol est une BASE NATIVE de sbire : elle disparait avec la conversion en
#    allie, comme Guard sur `ip021`.
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.


def GetAbilities() -> Sequence['Ability']:

    def contre_espionnage(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        valeur = PersonnagesHammerEnJeu(effect)
        manigances = Worlds.GetOnFieldSchemes(effect)
        if joueur is None or valeur <= 0 or not manigances:
            return
        cibles = joueur.AskChooseFaces(manigances, (1, 1), effect,
                                       prompt="Remove threat from a scheme")
        if cibles:
            this.RemoveThreatFromSchemes(cibles, valeur, effect)

    return [
        SiPremiereReveleeAlorsAllie(),
        SpecialRegistered("Counter Intelligence", contre_espionnage)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
