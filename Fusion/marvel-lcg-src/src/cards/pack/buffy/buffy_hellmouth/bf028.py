from . import *

# Becoming — COMPLOT ANNEXE (HELLMOUTH). Menace 3, Hinder 2[per_hero], Victory 0.
# When Defeated: Find Enemies Aligned and the Faith minion and reveal them. Put the set-aside Chosen upgrade into play.
#
# CARTES DE REFERENCE : `43021` (mise en jeu d'une carte mise de cote), `mv013` (find + reveal) ; meme montage que `bf027`.
#
# TEXTE CONTRE CODE
#  « Enemies Aligned AND the Faith minion » -> DEUX recherches, chacune suivie de `Reveal` ; « the Faith MINION » -> filtre `Minion` (l'allie Faith
#    porte le meme nom). « the set-aside Chosen upgrade » -> la carte « Chosen One » (liee a Becoming), zone de mise de cote seule.


def GetAbilities() -> Sequence['Ability']:

    def becoming(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurDeLaDefaite(effect, message)
        ea = Trouver(effect, joueur, NOM_ENEMIES_ALIGNED, EncounterSideScheme)
        if ea:
            ea.Reveal(joueur, effect)
        faith = Trouver(effect, joueur, NOM_FAITH, Minion)
        if faith:
            faith.Reveal(joueur, effect)
        chosen = Search.SearchForCard(effect, joueur, include_set_aside=True, name=NOM_CHOSEN_ONE, card_type=Upgrade)
        if chosen:
            chosen.PutIntoPlay(joueur, effect, under_control=True)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            becoming,
        ),
    ]
