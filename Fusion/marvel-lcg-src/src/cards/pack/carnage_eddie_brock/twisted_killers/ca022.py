from . import *

# * Murderous Nature : ATTACHEMENT (CONDITION.), boost 3. Set modulaire « Twisted Killers » (x2).
# Attach to a non-ELITE minion without a copy of Murderous Nature attached. Otherwise, this card gains surge.
# Attached enemy gains the KILLER trait and villainous keyword.
# [star] Forced Interrupt: When attached enemy attacks, it attacks the friendly character or other enemy with the fewest remaining hit points. That attack gains overkill.
#
# CARTES DE REFERENCE
#  - « Attach to a minion ... Otherwise surge » : `AttachToFaceWhenPutIntoPlay(CardFinder(..), without_another_copy=True, if_cannot_gain_surge=True)` (attachment.py:47, comme ca017) ; « gains trait / villainous » : `GiveKeywordToAttached(Minion, trait=.., villainous=1)` (asset.py:6).
#  - « it attacks X instead » : `41028` (Psionic Illusion) : `WhenUnitWouldAttackUnit(ForcedInterrupt, .., op)` + `message.ChangeTarget(unit, effect)` ; mot-cle : `message.GainOverKill(effect)` (sender_damage.py:388).
#
# TEXTE CONTRE CODE
#  « non-ELITE MINION WITHOUT A COPY of Murderous Nature » : `CardFinder(non_trait="ELITE", card_type=Minion)` + `without_another_copy=True` ; aucun sbire valable -> surge. « gains KILLER AND villainous » : les deux, par l'attache. « [star] Forced Interrupt: When ATTACHED enemy attacks » : l'ennemi porteur (`"AttachedEnemy"`).
#  « the FRIENDLY character OR OTHER ENEMY with the FEWEST REMAINING hit points » : PV RESTANTS (`health`), parmi les personnages amis (identite, allies) ET les AUTRES ennemis en jeu (jamais lui-meme) ; ex aequo : le joueur choisit. « That attack gains OVERKILL ». Chiffres : boost 3.
#  ⚠ LIMITE DU MOTEUR (03/11) : la branche « OR OTHER ENEMY » est codee (les autres ennemis sont candidats, `ChangeTarget`) mais le moteur ne redirige pas une attaque d'ennemi vers un AUTRE ennemi : `ChangeTarget(<ennemi>)` laisse l'attaque frapper l'identite
#    (cas ecrit puis retire le 03/11 : Carnage prenait 2 degats, Hydra Bomber 0). A verifier en partie reelle. Le test « sans copie deja attachee » n'est pas montable non plus : `Puzzle.Reveal('ca022')` retrouve la copie DEJA en jeu (meme card_id).


def GetAbilities() -> Sequence['Ability']:

    def nature_meurtriere(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        attaquant = message.attacker
        joueur = message.attacker.GetControlByPlayer() if hasattr(message.attacker, "GetControlByPlayer") else None
        amis = PersonnagesAmisEnJeu(effect)
        autres_ennemis = [f for f in Worlds.GetOnFieldEnemies(effect) if f is not attaquant and f.IsInPlay()]
        plus_faibles = PlusFaibleEnPV(amis + autres_ennemis)
        if not plus_faibles:
            return
        cible = plus_faibles[0]
        if len(plus_faibles) > 1:
            decideur = effect.world.GetCurrentPlayer() or joueur
            choisie = decideur.AskChooseFace(plus_faibles, effect, forced=True) if decideur is not None else None
            if choisie is not None:
                cible = choisie
        if cible is not message.target:
            message.ChangeTarget(cible, effect)
        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Minion, non_trait="ELITE"),
            without_another_copy=True,
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            trait="KILLER",
            villainous=1,
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            Unit2,
            nature_meurtriere,
        ),
    ]
