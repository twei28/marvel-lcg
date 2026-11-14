from . import *
# Slave Pits of Chandilar. Manigance annexe, 2[per_hero] menace de depart, 1 icone Acceleration, boost 3.
#
# When Revealed: Each player places an ally or PERSONA support they control facedown under here. Each player who cannot
#   discards 1 card from their hand.
# When Defeated: Return each facedown card here to play under its owner's control.
#
# Cartes de reference : gs119 Imprisoned on Chandilar (glisser des allies sous une manigance, les remettre en jeu a la
# defaite : `WhenLastThreatRemoveFromThisScheme`, `Reset(False)` avant `PutIntoPlay`), 50081 Abduct Superhumans
# (`TuckCardUnderHere` = FACE CACHEE, ce que dit « facedown »), 58027 (defausse choisie d'une carte de la main).
# ⚠ « Each player who CANNOT » : sans allie ni soutien PERSONA controle. Un joueur a main vide ne defausse rien.
# ⚠ « under its OWNER's control » (pas celui qui les a posees) : `GetOwnerPlayer()` de chaque carte.
def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        for joueur in JoueursEnOrdre(effect):
            candidates = AlliesEtPersonasDe(joueur)
            if candidates:
                choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(
                    candidates, effect, prompt="Place under Slave Pits of Chandilar", forced=True)
                if choisie is not None:
                    this.TuckCardUnderHere(choisie, effect)
                    continue
            main = list(joueur.hand_cards.Get())
            if main:
                def action(chosen: Sequence['CardFace']):
                    Faces.DiscardAll(list(chosen), effect)
                joueur.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(
                    'Discard 1 card from your hand', action).SetTarget(main, range=(1, 1), not_move=True))
    def liberer(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        this = effect.this.CastTo(SchemeSide2)
        for face in list(this.GetPlacedCardArea().GetAll()):
            proprietaire = face.GetOwnerPlayer()
            face.Reset(False)
            if Ally.IsType(face) or Support.IsType(face):
                face.PutIntoPlay(proprietaire, effect, under_control=True)
    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedInterrupt, liberer),
    ]
