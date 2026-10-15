from . import *

# Majime — evenement signature, x2 (7/15 et 8/15). ATTACK. THWART.
# Cout 0, ressource [mental].
# Hero Action (attack/thwart): Take X damage (to a maximum of 3) -> remove X
#   threat from a scheme and deal X damage to an enemy.
#
# Cartes de reference :
#  - `determination/dt028` Pay It Forward : « Take up to 3 damage -> deal X
#    damage ... remove X threat ... », meme squelette
#    (`DeclareNumber(0, 3)`, `hero.TakeDamage(this, n, effect)`,
#    `SetLabel('attack', 'thwart')`) ;
#  - retrait de menace : `this.RemoveThreatFromSchemes([manigance], X, effect)` ;
#  - degats : `this.DealDamage([ennemi], X, effect)`.
#
# ⚠ Mots-pieges :
#  - X est le nombre DECLARE par le joueur (0 a 3), PAS les degats reellement
#    encaisses : le texte dit « Take X damage », et un cout de degats est
#    considere paye meme si les degats sont prevenus (commentaire de
#    CostFunc.DealDamage). dt028, lui, mesure les PV perdus : c'est le point
#    de divergence. # TODO-QUESTION (question 2).
#  - « remove X threat from A scheme » : UNE manigance au choix (principale ou
#    annexe), pas de repartition. « deal X damage to AN enemy » : un seul
#    ennemi.
#  - Les deux effets sont independants : s'il n'y a aucune manigance avec de la
#    menace (ou aucun ennemi), l'autre moitie s'applique quand meme.
#  - Le libelle `(attack/thwart)` alimente Sonne ET Desoriente.

def GetAbilities() -> Sequence['Ability']:

    def majime(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None or not initiator.IsHero():
            return
        heros = initiator.GetHero()

        x = initiator.DeclareNumber(0, 3)
        heros.TakeDamage(this, x, effect)
        if x <= 0:
            return

        manigances = [s for s in Worlds.GetOnAllFieldScheme(effect) if s.threat > 0]
        if manigances:
            manigance = initiator.AskChooseFace(
                manigances, effect, prompt=f"Remove {x} threat from a scheme")
            this.RemoveThreatFromSchemes([manigance or manigances[0]], x, effect)

        ennemis = [e for e in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not e.IsDefeated()]
        if ennemis:
            ennemi = initiator.AskChooseFace(
                ennemis, effect, prompt=f"Deal {x} damage to an enemy")
            this.DealDamage([ennemi or ennemis[0]], x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            majime,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
