from . import *

# Toshokan Arcana (sj008), Kuji-Kiri, soutien LOCATION, unique (Inkwire, TMNT Shinobi).
# Action: Exhaust Toshokan Arcana → discard cards from the top of your deck until you discard a SPELL card.
# Add that card to your hand.
#
# Cartes de reference : `ant/12015` Call for Aid (« Discard cards from the top of your deck until you discard an
# [[Avenger]] ally, then add that ally to your hand » : `DiscardDeckUntil` + `GainCard`) ; cout « Exhaust this
# card » : `CostFunc.Exhaust("This")`.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » (les deux formes de l'identite) ; cout = incliner le soutien.
#  ⚠ « until you discard a SPELL card » : n'importe quel type de carte portant le trait SPELL ; les cartes
#    sautees restent defaussees ; la SPELL trouvee va en MAIN (elle est defaussee puis reprise).
#  ⚠ Aucun SPELL dans le deck : tout le deck est defausse (regles du deck vide, `DiscardDeckUntil`), rien
#    n'est ajoute a la main.


def GetAbilities() -> Sequence['Ability']:

    def toshokan_arcana(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = joueur.DiscardDeckUntil(effect, trait="SPELL")
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            toshokan_arcana,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
