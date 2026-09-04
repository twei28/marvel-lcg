from . import *

# * Nocturne (Talia Wagner) — ALLIE d'AGRESSIVITE, cout 3, PV 2. X-MEN.
# Response: After Nocturne enters play, deal 1 damage to a minion for each
#   upgrade you control.
#
# ⚠ CARTE D'ASPECT MAISON : elle entre dans le vivier general de
# l'Agressivite, donc devient jouable par TOUS les heros du jeu, pas seulement
# par Blink (arbitrage de l'utilisateur du 04/09/2026).
#
# TEXTE CONTRE CODE
#  « for each UPGRADE you control » -> TOUTES les ameliorations, pas seulement
#    les PORTAL : la carte recompense n'importe quel heros a ameliorations.
#  « to A MINION » -> une seule cible, et un SBIRE, pas un ennemi quelconque.


def GetAbilities() -> Sequence['Ability']:

    def nocturne(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        montant = len(joueur.GetControlUpgrade(CardFinder(card_type=Upgrade)))
        if montant > 0 and effect.targets:
            this.DealDamage(effect.targets, montant, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            nocturne,
        ).SetTarget(Minion),
    ]
