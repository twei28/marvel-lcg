from . import *

# Enemies Aligned — COMPLOT ANNEXE (HELLMOUTH). Menace 4, Hinder 3[per_hero], Victory 0.
# When Defeated: Put the set-aside Slayer Scythe into play.
#
# CARTES DE REFERENCE : `43021` (mise en jeu d'une carte mise de cote, `under_control=True`). La Scythe y est liee (`desc.Linked`).
# TEXTE CONTRE CODE : « the set-aside Slayer Scythe » -> zone de mise de cote seule ; mise en jeu sous le controle du joueur qui a vaincu.


def GetAbilities() -> Sequence['Ability']:

    def enemies_aligned(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurDeLaDefaite(effect, message)
        scythe = Search.SearchForCard(effect, joueur, include_set_aside=True, name=NOM_SCYTHE, card_type=Upgrade)
        if scythe:
            scythe.PutIntoPlay(joueur, effect, under_control=True)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            enemies_aligned,
        ),
    ]
