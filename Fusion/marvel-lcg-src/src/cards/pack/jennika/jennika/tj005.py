from . import *

# Moonlighting — evenement signature, x2. TACTIC. Cout 0, [mental].
# Classe : Jennika ET Ninjutsu (desc.Class = « Hero;Ninjutsu »).
# Hero Action: Cloak Jennika.
#
# Mot-cle maison : Cloak (fiches mots-cles/cloak.md et cloaked.md) : « Cloak X » =
# poser la carte d'etat Cloaked sur X (decision utilisateur du 15/10/2026).
#
# Cartes de reference :
#  - `tl016` / `tl015` : `Faces.GiveStatus([face], "Cloaked", effect)` ;
#  - `td005` Improvised Tactics : Cloaked pose sur un personnage ami.
#
# ⚠ Mots-pieges :
#  - « Cloak JENNIKA » : le HEROS (face heros, seule forme ou la Hero Action est
#    jouable), pas un allie ni le vilain ;
#  - « Hero Action » : forme heros obligatoire ;
#  - Cloaked s'empile (aucun plafond, cloaked.md) : deux Moonlighting = deux cartes.


def GetAbilities() -> Sequence['Ability']:

    def moonlighting(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        Cloak(effect, joueur.GetHero())

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            moonlighting,
        ).SetPlay().SetLabel(),
    ]
