from . import *

# Bar Fight at Josie's (1) — PISTE. Response : While in Hell's Kitchen, after a minion or ally you control is defeated, place 1 bouncer counter
#   here. Then, if there are 3 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : venomized/vz035.py (`Ability(Response, Message.X, [conditions], op)` pour un evenement sans fabrique), fiche piste-lead.md.
# ⚠ « a minion OR ally you control » : lu « un sbire (de mon territoire : les interactions sont cloisonnees) ou un allie que je controle » ;
# decision prise le 22/10/2026 sans texte de la RR : a confirmer en partie reelle si une lecture « sbire que je controle » est voulue.
# ⚠ « While in » = au declenchement ; le compteur 'bouncer' est un ajout a CardFace.COUNTER.

def GetAbilities() -> Sequence['Ability']:

    def est_concerne(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        joueur = Joueur(effect)
        if joueur is None or not EnLieu("pu030")(effect, message):
            return False
        victime = message.trigger
        return Minion.IsType(victime) or (Ally.IsType(victime) and ControlePar(victime, joueur))

    def apres(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'bouncer', 3)

    return [Ability(AbilityType.Response, Message.AfterUnitBeDefeated, [est_concerne], apres)]
