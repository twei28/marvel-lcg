from . import *
# * Hepzibah. Allie, 3 PV, cout 3, ATQ 2* / THW 0* (l'etoile = valeur modifiee par sa propre capacite).
#
# [star] Interrupt: When Hepzibah uses a basic power, discard a card tucked under Corsair → Hepzibah gets +3 to that
#   power for this use.
#
# Cartes de reference : 47012 Husk (`WhenUnitUseBasicPower(Interrupt, "This")` + `message.GainValue`) ; la defausse d'une
# carte glissee SOUS UN AUTRE HOTE (Corsair) ne passe pas par `CostFunc.Discard` (« ThisPlaceCards » vise la carte qui
# porte l'effet, ici Hepzibah) : le choix et la defausse sont faits dans l'operation, la condition (au moins une
# carte glissee) gardant la capacite hors de portee sinon.
# ⚠ « → » est un cout : la defausse est faite AVANT le bonus, et le bonus n'est donne que si la carte est partie.
def GetAbilities() -> Sequence['Ability']:
    def avec_une_glissee(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return bool(Glissees(IdentiteDe(effect)))
    def hepzibah(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        joueur = JoueurDe(effect)
        glissees = Glissees(IdentiteDe(effect))
        if joueur is None or not glissees:
            return
        choisie = glissees[0] if len(glissees) == 1 else joueur.AskChooseFace(
            glissees, effect, prompt="Discard a card tucked under Corsair", forced=True)
        if choisie is None:
            return
        if Faces.DiscardAll([choisie], effect):
            message.GainValue(+3, effect)
    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            hepzibah,
            conditions=[avec_une_glissee],
        ),
    ]
