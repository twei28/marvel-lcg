from . import *

# Sense of Dread — AMELIORATION Leadership (TMNT Aspects, Inkwire), cout 1, [mental]. CONDITION. FERAL.
# Attach to a minion that your hero attacked this turn. If attached to a non-[[ELITE]] minion, it gains
#   vulnerable.
# Interrupt: When attached minion leaves play, draw 1 card.
#
# MOT-CLE (fiche lue AVANT le code) : Vulnerable — docs/reference/mots-cles/vulnerable.md : compteur
#   `Vulnerable` lu par le moteur (`HasVulnerable.GainVulnerable`), aucune regle a coder ici, seulement le
#   GAIN du mot-cle.
#
# CARTES DE REFERENCE
#  - `43012` Puncture Wound : « Attach to an enemy that X attacked this turn » =
#    `CanPlayThisUpgradeCard(CardFinder(card_type=..., check_effect_fn=...))` sur
#    `world.stat.this_turn_made_attack` (attaquant, effet, cibles).
#  - `sk093` / `st016` : un mot-cle sans parametre dedie dans la fabrique d'attachement =
#    `GiveKeywordToAttached(finder, apply=...)` ; le filtre rend 0 pour un porteur qui ne remplit pas
#    la condition (ici : ELITE).
#  - `sk213a` : « When X leaves play » (Interruption) = `WhenCardWouldLeavePlay(<type>, ..., op)` : AVANT
#    la sortie, quand l'amelioration est encore attachee (`WhenCardLeavePlay` arrive apres son detachement :
#    mesure en jeu, l'Interruption ne partait pas).
#
# TEXTE CONTRE CODE
#  ⚠ « a MINION » : pas le vilain.
#  ⚠ « that YOUR HERO attacked THIS TURN » : l'identite du joueur qui joue la carte, en forme heros, a
#    attaque ce sbire pendant ce tour (pas un allie, pas un autre joueur).
#  ⚠ « non-ELITE » : un sbire ELITE porte la carte mais ne gagne PAS vulnerable.
#  ⚠ « Interrupt » (pas Hero) : facultative ; « draw 1 card » = le joueur qui controle Sense of Dread.
#  ⚠ « leaves play » : vaincu, defausse, retourne au deck... toute sortie.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def attaque_par_votre_heros(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        for attaquant, _, cibles in effect.world.stat.this_turn_made_attack:
            if Hero.IsType(attaquant) and attaquant.GetControlByPlayer() == joueur and face in cibles:
                return True
        return False

    def gagner_vulnerable(effect: 'Effect', face: 'CardFace', diff: int) -> None:
        face.GainVulnerable(diff, effect)

    def le_porteur(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> bool:
        this = effect.this.CastTo(Upgrade)
        return this.bind_face is not None and message.trigger is this.bind_face

    def piocher(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = this.GetControlByOrOwner()
        if Player.IsType(joueur):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(
                card_type=Minion,
                check_effect_fn=attaque_par_votre_heros,
            )
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(card_type=Minion, non_trait="ELITE"),
            apply=gagner_vulnerable,
        ),
        AbilityFactory.WhenCardWouldLeavePlay(
            AbilityType.Interrupt,
            Minion,
            piocher,
            conditions=[le_porteur],
        ),
    ]
