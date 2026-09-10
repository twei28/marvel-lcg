from . import *

# * Man-Bull — SBIRE de nemesis (1/5). 5 PV, ATQ 3, MNG 1, boost 2. CRIMINAL.
# When Revealed: Each player discards 1 identity-specific card from their hand.
# (Spider-Woman's nemesis minion.)
#
# CARTES DE REFERENCE
#  - `27153` Induced Panic (pack sm) : `card_class="IdentitySpecific"`, la clef
#    qui designe une carte propre a une identite. Elle y sert de COUT ; ici
#    c'est un effet.
#  - `04077` * Absorbing Man : `Players.ForEachPlayer`.
#
# TEXTE CONTRE CODE
#  ⚠ « EACH player » : toute la table, pas seulement celui qui revele.
#  ⚠ « 1 IDENTITY-SPECIFIC card » : une carte de set heros, pas une carte
#    d'aspect ni une basique. C'est exactement ce que le pack fait mal a
#    Spider-Woman, dont tout le moteur est dans son set heros.
#  ⚠ Main sans carte de ce type : ce joueur ne defausse rien, et les autres
#    defaussent quand meme.


def GetAbilities() -> Sequence['Ability']:

    def man_bull(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(effect.this, message)

        def defausser(joueur: 'Player') -> None:
            cartes = [f for f in joueur.hand_cards.GetAll()
                      if f is not None and EstSpecifiqueALIdentite(f)]
            if cartes:
                # ⚠ `AskDiscardFaces` N'A PAS de parametre `prompt` : elle pose
                # son propre libelle (« Discard », player_ask.py:325). Le lui
                # passer leve un TypeError que le moteur AVALE, et la carte
                # devenait alors totalement inerte sans un mot. Vu le
                # 10/09/2026 par le harnais, jamais par `test_cards` ni par
                # `verifier_appels_modules` (qui verifie les NOMS, pas les
                # signatures).
                joueur.AskDiscardFaces(cartes, (1, 1), effect)

        Players.ForEachPlayer(effect, defausser)

    return [
        AbilityFactory.WhenThisRevealed(None, man_bull),
    ]
