from . import *

# H.A.M.M.E.R. Commandos — SBIRE du deck REGISTERED (4/20), x3. 3 PV, ATQ 2,
# MNG 1, boost 2. H.A.M.M.E.R. SOLDIER.
# Guard.
# When Revealed: If this is the first card revealed from the REGISTERED deck
#   this round, put this card under your control as a REGISTERED ally.
# Suppressive Fire — Special: Exhaust this ally -> for each H.A.M.M.E.R.
#   character in play, deal 1 damage to an enemy.
#
# ⚠ LA JUMELLE DE `ip022` H.A.M.M.E.R. Operatives, a un mot pres :
#     ip021  Guard   degat a un ENNEMI
#     ip022  Patrol  menace retiree d'une MANIGANCE
# Meme compte, meme cout, meme « When Revealed ».
#
# CARTE DE REFERENCE
#  - `__init__.py` du pack : `SiPremiereReveleeAlorsAllie()` et
#    `PersonnagesHammerEnJeu()`.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust THIS ALLY -> » : COUT, avant la fleche. Un allie deja incline ne
#    peut pas resoudre son « Special ». C'est ce qui empeche `ip001b` Norman
#    Osborn de rejouer la meme carte deux fois dans le tour.
#  ⚠ « for each H.A.M.M.E.R. character IN PLAY » : voir `PersonnagesHammerEnJeu`
#    — en jeu, pas « you control », et Iron Patriot lui-meme compte.
#  ⚠ « deal 1 damage TO AN ENEMY » : un seul ennemi, qui encaisse le total.
#    Pas « 1 damage a chacun ».
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.
#  ⚠ Guard est une BASE NATIVE lue dans `desc`, et elle ne vaut que tant que la
#    carte est un SBIRE : `Faces.TreatAsAlly` echange la face contre le gabarit
#    d'allie, qui ne la porte pas.


def GetAbilities() -> Sequence['Ability']:

    def tir_de_couverture(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        degats = PersonnagesHammerEnJeu(effect)
        ennemis = Worlds.GetOnFieldEnemies(effect)
        if joueur is None or degats <= 0 or not ennemis:
            return
        cibles = joueur.AskChooseFaces(ennemis, (1, 1), effect,
                                       prompt="Deal damage to an enemy")
        if cibles:
            this.DealDamage(cibles, degats, effect)

    return [
        SiPremiereReveleeAlorsAllie(),
        SpecialRegistered("Suppressive Fire", tir_de_couverture)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
