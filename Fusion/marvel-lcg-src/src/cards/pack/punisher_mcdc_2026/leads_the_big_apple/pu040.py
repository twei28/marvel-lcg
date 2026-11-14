from . import *

# Art Heals the Soul (2) — PISTE. Response : While in The Theater District, after you heal a friendly character, place 1 culture counter here.
#   Then, if there are 3 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : venomized/vz035.py (`Message.AfterUnitHealHealth`, aucune fabrique), fiche piste-lead.md.
# ⚠ « friendly character » : l'identite ou un allie que le joueur controle (jamais un ennemi) ; « you heal » : ici tout soin dans son camp
# (pas de notion de source pour les soins d'allies : le soin lui-meme est celui du joueur qui l'a joue).

def GetAbilities() -> Sequence['Ability']:

    def est_concerne(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> bool:
        joueur = Joueur(effect)
        if joueur is None or not EnLieu("pu031")(effect, message):
            return False
        soigne = message.trigger
        return (Identity.IsType(soigne) or Ally.IsType(soigne)) and ControlePar(soigne, joueur)

    def apres(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'culture', 3)

    return [Ability(AbilityType.Response, Message.AfterUnitHealHealth, [est_concerne], apres)]
