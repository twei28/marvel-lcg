from . import *

# * Belit — alliee signature (1/16). ADVENTURER. PIRATE. Cout 3 [wild].
# THW 1* / ATK 1* (degats consequents), 3 PV.
# While you have the THIEF or KING trait, Belit gets +1 THW.
# While you have the BARBARIAN or KING trait, Belit gets +1 ATK.
# Response: After Belit enters play, if you have the KING trait, ready your identity.
#
# CARTES DE REFERENCE
#  - bonus selon le trait de l'identite : `ThisGainKeyword(fn, thwart=1,
#    change_on_event=...)` (26001b Vision, recette §3 « +X par etat
#    dynamique »). `OnEvent.Form` couvre le changement de forme ET l'entree
#    en jeu de Belit ; `OnEvent.Faceup` couvre le couronnement, qui retourne
#    l'identite SANS changement de forme.
#  - « After X enters play » : `AfterCardEnterPlay(Response, "This", op)`
#    (44043 Bob, Agent of Hydra).
#
# TEXTE CONTRE CODE
#  « you have the ... trait » : le trait de l'IDENTITE en jeu (CIMMERIA. THIEF.
#    sur l'alter-ego de depart : +1 THW aussi en alter-ego, comme imprime).
#  « ready your identity » : `Faces.ReadyAll([identite])`.

RECALCUL = [OnEvent.Form("YourIdentity"), OnEvent.Faceup("YourIdentity")]


def _identite_a(effect: 'Effect', *traits: str) -> bool:
    joueur = JoueurDe(effect)
    if joueur is None:
        joueur = effect.this.GetControlByOrOwner()
    if not isinstance(joueur, Player):
        return False
    identite = joueur.GetIdentity()
    return identite is not None and any(identite.HasTrait(t) for t in traits)  # type: ignore


def GetAbilities() -> Sequence['Ability']:

    def pret(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        joueur = JoueurDe(effect)
        if joueur is not None:
            Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if _identite_a(effect, "THIEF", "KING") else 0,
            thwart=1,
            change_on_event=RECALCUL,
        ),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if _identite_a(effect, "BARBARIAN", "KING") else 0,
            attack=1,
            change_on_event=RECALCUL,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            pret,
            conditions=[lambda effect, message: _identite_a(effect, "KING")],
        ),
    ]
