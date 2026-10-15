from . import *

# Strength in Otherness — evenement d'aspect BASIC (n° 25). ATTACK. THWART.
# Cout 2 [wild]. Team-Up (Hulkling and Wiccan). Max 1 per deck.
# Hero Action (attack/thwart): Remove 1 threat from the main scheme and deal 1
#   damage to the villain for each different card type in your discard pile.
#
# Cartes de reference :
#  - **`22022`** Daughters of Thanos / `12020` Swarm Tactics : evenement
#    Team-Up = `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetTarget("TeamUp")`.
#    ⚠ La premiere cible DOIT etre "TeamUp" (assert de database.py en mode dev
#    sur tout Event qui declare desc.TeamUp).
#  - `18020` Hit and Run pour l'etiquette double `SetLabel('attack', 'thwart')`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **for each** different card type » : decision de l'utilisateur
#    (15/10/2026), s'applique AUX DEUX : X menaces ET X degats, X = nombre de
#    TYPES distincts (allie, evenement, amelioration, soutien, ressource...)
#    dans TA defausse. Defausse vide : X = 0, rien.
#  - « **the main** scheme » / « **the villain** » : cibles fixes, pas de choix.
#  - « Team-Up (Hulkling **and** Wiccan) » : desc.TeamUp « Hulkling;Wiccan »,
#    les DEUX doivent etre en jeu (identite ou allie), regle moteur.
#  - « Max 1 per deck » : desc.MaxPerDeck, contrôle du deck-builder.
#  - Compte a la RESOLUTION : l'evenement lui-meme n'est pas encore dans la
#    defausse pendant qu'il resout.


def GetAbilities() -> Sequence['Ability']:

    def force(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        types = {f.paper.type for f in joueur.discard_pile.Get() if f.paper.type}
        x = len(types)
        if x <= 0:
            return
        this.RemoveThreatFromSchemes("MainScheme", x, effect)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            this.DealDamage([mechant], x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            force,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget("TeamUp"),
    ]
