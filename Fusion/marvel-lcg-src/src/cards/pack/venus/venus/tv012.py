from . import *

# * Dream Weaver — AMELIORATION, cout 2, [wild]. ELEMENT. SONG. x1.
# Hero Action: Exhaust this card and remove 2 dredge counters from Venus -> discard cards
#   from the top of your deck until you discard an ally or upgrade. Add that card to your
#   hand.
#
# CARTES DE REFERENCE : `tv010` (meme pack, meme montage) ; `br009` / `seek.md`.
#
# TEXTE CONTRE CODE
#  ⚠ « an ALLY OR UPGRADE » -> la premiere carte qui est un allie OU une amelioration (pas
#    les deux types a la fois), `DefausserJusquA(verifier=...)`.
#  ⚠ Deux couts (inclinaison + 2 compteurs). Action de HEROS.


def GetAbilities() -> Sequence['Ability']:

    def tisseur(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = DefausserJusquA(
            effect, joueur,
            verifier=lambda f: Ally.IsType(f) or Upgrade.IsType(f))
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tisseur,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("YourIdentity", 2, DREDGE)),
    ]
