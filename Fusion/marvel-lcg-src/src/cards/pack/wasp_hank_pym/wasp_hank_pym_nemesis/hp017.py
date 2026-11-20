from . import *
# Take Over Signal — attachement (HACKED). Traite l'allie porteur comme un sbire HACKED sans texte, SCH = THW imprime
# (modele 27171 Manipulated Mind : TreatAttachedCardAsMinion). When Revealed : s'attache a l'allie que tu controles au cout
# le plus ELEVE ; sinon « seek » un allie de ton deck, le met en jeu engage avec toi avec cette carte attachee.
# CORRECTIF 26/10/2026 : (1) le sbire porte le trait HACKED (« as a HACKED minion », modele st016 / sentinel) en plus des traits de
# l'allie ; (2) AUCUN surge : il n'est pas imprime ici (27171 en a un, pas cette carte) ; sans allie a prendre, la carte ne
# s'attache a rien et est defaussee (RR ATTACH TO : si la verification d'attache echoue, la carte est defaussee).
def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        face = Filter.One(joueur.GetControlAllies(), effect, highest_cost=True)
        if face:
            this.AttachTo2(face, effect)
            return
        autres: List['CardFace'] = []
        allie = joueur.DiscardDeckUntil(effect, card_type=Ally, return_other_faces=autres)
        if allie:
            allie.PutIntoPlay(joueur, effect)
            this.AttachTo2(allie, effect)
        else:
            Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.TreatAttachedCardAsMinion(
            Ally,
            "Minion",
            lambda minion, allie, effect: minion.GainTraits(+1, [*allie.traits, "HACKED"], effect),
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
