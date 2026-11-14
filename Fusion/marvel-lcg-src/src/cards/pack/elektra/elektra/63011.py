from . import *

# * White Tiger — SOUTIEN, cout 1, [mental]. PERSONA. Unique. x1 (Elektra 11/15).
# Response: After you change to hero form, shuffle the top card of the NINJA deck into the encounter deck. Otherwise, give Elektra 1
# facedown boost card.
#
# CARTES DE REFERENCE
#  - « After you change to hero form » : `AfterUnitChangeForm(Response, "You", op, to_form=Hero)` (form.py:81 ; RECETTES « After you change to this form »).
#  - melange de la carte du dessus du paquet Ninja : `MelangerDessusNinja` du set (63001b).
#  - « give Elektra 1 facedown boost card » : `Faces.GiveFacedownBoostCards([identite], 1, effect)` (faces.py:473) ; la carte boost du heros est
#    resolue par `can_attack.py` (attaque) et, apres l'extension moteur du 13/11/2026, par le deplacement/defense (voir PLAN.md).
#
# TEXTE CONTRE CODE
#  ⚠ « Otherwise » : DECISION UTILISATEUR du 13/11/2026 : « sinon » = le paquet NINJA est VIDE. Un seul des deux effets par passage en forme heros :
#    paquet non vide -> melange de la carte du dessus ; paquet vide -> Elektra recoit 1 carte boost face cachee.
#  ⚠ « After you change TO HERO form » : seulement le passage alter-ego -> heros (`to_form=Hero`), jamais l'inverse.
#  ⚠ « 1 facedown boost card » : prise sur le dessus du paquet de rencontre, posee face cachee sur Elektra (pile de boost de l'identite).
#  Chiffres : cout 1, une carte melangee OU une carte boost.


def GetAbilities() -> Sequence['Ability']:

    def white_tiger(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        if MelangerDessusNinja(joueur, effect):
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.GiveFacedownBoostCards([identite], 1, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            white_tiger,
            to_form=Hero,
        ),
    ]
