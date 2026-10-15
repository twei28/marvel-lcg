from . import *

# * Cloning Faux Pas — COMPLOT ANNEXE DE JOUEUR ('Pool / Campaign, n° 271). Cout 0, menace de depart 3.
# Icone ACCELERATION (decision utilisateur du 15/10/2026). Titre d'origine sous le scotch : « Cloning Program ».
# Victory 0.
# When Defeated: The player who defeated this scheme may deal up to 3 damage to each SKRULL minion engaged
#   with them.
#
# Cartes de reference :
#  - **`hd011`** / **`hd012`** : complot annexe JOUEUR « Victory 0 » + `WhenSchemeBeDefeated(WhenDefeated,
#    "This", op, has_defeating_player=True)` + `MayChooseOneAbility`.
#  - **`ss004`** Precise Force : « deal UP TO 3 damage » = `joueur.DeclareNumber(0, 3)` puis `DealDamage`.
#  - **`56086`** S.H.I.E.L.D. Helicarrier : « deals 1 damage to each character they control and each minion
#    engaged with them » (When Defeated d'un complot annexe) = les sbires du joueur, `player.engaged_minions`.
#  - **`mots-cles/acceleration.md`** : l'icone vient du `desc` (« Acceleration »: 1), aucun script.
#
# ⚠ Mots-pieges :
#  - « up to 3 damage to EACH » : le joueur declare UN montant (0 a 3), applique a CHAQUE sbire SKRULL engage
#    avec LUI (le vainqueur, pas les sbires des autres joueurs) ;
#  - « SKRULL minion » (elite ou non), pas les autres sbires engages ;
#  - « MAY » : facultatif ; l'icone Acceleration agit tant que le complot est en jeu (phase du mechant).


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        vainqueur = message.GetDefeatingPlayer()
        if vainqueur is None:
            return

        def frapper(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            sbires = [m for m in vainqueur.engaged_minions.Get() if m.HasTrait("SKRULL")]
            if not sbires:
                return
            montant = vainqueur.DeclareNumber(0, 3)
            if montant > 0:
                this.DealDamage(sbires, montant, effect)

        vainqueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal up to 3 damage to each SKRULL minion engaged with you",
                frapper,
            ),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            recompense,
            has_defeating_player=True,
        ),
    ]
