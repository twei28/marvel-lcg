from . import *

# Meddlesome Heroes! — complot annexe nemesis (1/4). Menace 4. Boost 3.
# Hazard 1.
# When Defeated: Take 4 indirect damage or place 4 threat among any schemes
#   in play.
#
# Cartes de reference :
#  - « When Defeated » sur un complot annexe : jj013 « Chase Down a Lead »,
#    `WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", op)` — et NON
#    `AfterSchemeBeDefeated`, qui existe aussi (scheme.py:277) mais se declenche
#    APRES : le When Defeated imprime doit passer par la fabrique qui teste
#    `is_when_defeated` (defeated.py:444), sans quoi un effet qui l'ignore ne
#    serait pas respecte ;
#  - degats INDIRECTS : kb019 Golden Shot / aa014,
#    `identite.TakeIndirectDamage(this, n, effect)` ;
#  - pose de menace : le litteral `"EachScheme"` n'irait pas ici (« AMONG any
#    schemes » = repartition au choix), on passe par un choix de manigance
#    puis `PlaceThreatOnSchemes` (recette moteur §2) ;
#  - choix entre deux branches : aa014, `ChooseAbilities`.
#
# ⚠ « OR » : le joueur CHOISIT. Le pilote des tests prend toujours la premiere
# branche (RECETTES §2), d'ou deux cas distincts pour couvrir les deux.
#
# ⚠ Hazard est une base automatique lue dans `desc` : aucun module.
#
# ⚠ L'image livree par l'auteur etait en PORTRAIT ; elle a ete pivotee pour
# respecter la convention du moteur (complot annexe = paysage droit, reference
# 01107). Meme correctif que bt023.

def GetAbilities() -> Sequence['Ability']:

    def meddlesome_heroes(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)

        # ⚠ NE PAS utiliser `effect.GetInitiator()` : sur une carte de
        # RENCONTRE, l'initiateur est le VILAIN, et la methode leve
        # `AssertionError: self.initiator=Rhino`. Constate le 01/09/2026, alors
        # que le piege etait deja documente dans an011 et bt021. Le message
        # expose `defeating_player` (sender_scheme.py:206), qui peut etre None
        # si la manigance tombe sans qu'un joueur en soit la cause : on retombe
        # alors sur le premier joueur, seul choix sense pour un « take » et un
        # « place ».
        initiator = message.defeating_player or Worlds.GetFirstPlayer(effect)
        if initiator is None:
            return
        identite = initiator.GetIdentity()

        def subir(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            if identite is not None:
                identite.TakeIndirectDamage(this, 4, effect)

        def poser_menace(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            schemes = Worlds.FindCardsOnField(effect, card_type=Scheme2)
            if not schemes:
                return
            cible = initiator.AskChooseFace(schemes, effect)
            if cible:
                this.PlaceThreatOnSchemes([cible], 4, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Take 4 indirect damage", subir),
            AbilityFactory.ForChoiceAbility(
                "Place 4 threat among any schemes in play", poser_menace),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            meddlesome_heroes,
        ),
    ]
