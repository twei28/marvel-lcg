from . import *

# Midnight Veil — EVENEMENT Leadership (TMNT Aspects, Inkwire), cout 3, [energy]. NYC. SKILL.
# Hero Action: Cloak up to 2 characters you control (3 characters instead if you control a [[NYC]]
#   support).
#
# MOT-CLE (fiche lue AVANT le code) : Cloak — docs/reference/mots-cles/cloak.md : poser une carte d'etat
#   Cloaked (`Faces.GiveStatus(..., "Cloaked", ...)`). Plafond d'une carte Cloaked par personnage
#   (cloaked.md) : un personnage deja camoufle peut etre choisi, rien n'y est pose.
#
# CARTES DE REFERENCE
#  - `td005` Improvised Tactics : « Cloak two friendly characters » = choix des personnages par
#    `joueur.AskChooseFaces(candidats, (min, max), effect, not_move=True)` puis `Faces.GiveStatus`.
#  - `ua015` Demolish : « if you control a NYC support » = `joueur.IsControl(CardFinder2("NYC", Support))`,
#    lu a la resolution.
#
# TEXTE CONTRE CODE
#  ⚠ « UP TO 2 » : de 0 a 2 personnages (de 0 a 3 avec un soutien NYC), au choix du joueur.
#  ⚠ « characters YOU CONTROL » : votre identite et vos allies, pas ceux des autres joueurs.
#  ⚠ « 3 characters INSTEAD » : le plafond passe a 3, ce n'est pas 2 + 3.
#  ⚠ « a NYC SUPPORT » : un soutien, controle par ce joueur.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def midnight_veil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        plafond = 3 if joueur.IsControl(CardFinder2("NYC", Support)) else 2
        candidats = [f for f in joueur.GetControlCharacters() if f is not None and f.IsInPlay()]
        if not candidats:
            return
        choisis = joueur.AskChooseFaces(
            candidats,
            (0, min(plafond, len(candidats))),
            effect,
            prompt="Cloak up to %d characters you control" % plafond,
            not_move=True,
        )
        if choisis:
            Faces.GiveStatus(list(choisis), "Cloaked", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            midnight_veil,
        ).SetPlay().SetLabel(),
    ]
