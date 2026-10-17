from . import *

# Kuragari — AMELIORATION DUALE Bushido/Ninjutsu, cout 2, [energy]. OATH.
# Classe : « Bushido;Ninjutsu ».
# Uses (3 samurai counters).
# Action: Exhaust this card and remove 3 samurai counters from it -> cloak and ready your hero.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md) ; samurai counter / OATH (samurai-counter.md) ; Cloak (cloak.md,
# cloaked.md).
#
# Cartes de reference :
#  - `jennika/tj006` Fearless Resolve : `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", n, 'samurai')`,
#    `Faces.ReadyAll([heros], effect)` (« ready your hero ») ;
#  - `jennika/tj005` Moonlighting / `tmnt_shinobi_paths/se001` : `ShinobiCloak(effect, face)`.
#
# TEXTE CONTRE CODE
#  ⚠ « remove 3 samurai counters FROM IT » : les TROIS d'un coup (cout), donc UNE SEULE utilisation par exemplaire, puis la
#    carte quitte le jeu (Uses, dernier compteur retire).
#  ⚠ « Exhaust this card AND remove 3 counters » : deux couts obligatoires.
#  ⚠ « cloak AND ready your hero » : les deux effets sur LE HEROS, sans condition (le heros peut deja etre pret ou deja
#    camoufle : pas de seconde carte Cloaked).
#  ⚠ « Action » (et non « Hero Action ») avec « your hero » : QUESTION OUVERTE (.planning/tmnt/shinobi-dual-questions.md,
#    Q-D1). LECTURE PROVISOIRE : Action utilisable dans les deux formes ; en forme alter-ego « your hero » designe l'identite
#    du joueur (la carte d'identite, face alter-ego). NON TERMINEE tant que la reponse n'est pas donnee.


def GetAbilities() -> Sequence['Ability']:

    def kuragari(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # Q-D1 (provisoire) : le heros en forme heros, l'identite (alter-ego) sinon.
        cible = joueur.GetHero() if joueur.IsHero() else joueur.GetIdentity()
        ShinobiCloak(effect, cible)
        Faces.ReadyAll([cible], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kuragari,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 3, 'samurai')),
    ]
