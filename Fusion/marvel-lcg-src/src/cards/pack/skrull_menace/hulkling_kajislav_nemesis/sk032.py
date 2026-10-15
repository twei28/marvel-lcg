from . import *

# * Empress R'Klll — SBIRE NEMESIS de Hulkling (n° 32, 1/5). ELITE. SKRULL.
# SCH 2, ATK 1★, 4 PV, 2 icones boost.
# Villainous.
# ★ Empress R'Klll's attacks gain piercing.
# When Revealed: Empress R'Klll attacks each player in hero form.
#
# Cartes de reference :
#  - **`39014b`** * Spiral : « When Revealed: Spiral attacks each player » =
#    `WhenThisRevealed(None, op)` + `Players.ForEachPlayer(effect, lambda p:
#    this.DoAttackYou(p, effect))`.
#  - **`41002b`** Psi-Katana / `13008` : `UnitAttackGainKeyword(<qui>,
#    piercing=True)`, ici "This" et TOUTES ses attaques (pas seulement basic).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « each player **in hero form** » : un joueur en civil n'est pas attaque
#    par la revelation (il le sera a l'activation normale).
#  - « Villainous » : base automatique, desc.Villainous (fiche villainous.md).
#  - ATK « 1★ » : valeur 1, l'etoile renvoie au texte ★ (convention validee le
#    15/10/2026) ; desc « 1* » comme st015.
#  - ⚠ FAQ du livret (p. 20) : si le vilain Empress R'Klll (scenario Skrull
#    Empire) est revele alors que CE sbire est en jeu, le sbire est defausse
#    (unicite) et le vilain active. Regle d'unicite du moteur, rien a coder ici.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        def attaque(joueur: 'Player') -> None:
            if Hero.IsType(joueur.GetIdentity()) and this.IsInPlay():
                this.DoAttackYou(joueur, effect)

        Players.ForEachPlayer(effect, attaque)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
    ]
