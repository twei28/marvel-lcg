from . import *

# Surprising Alliance — COMPLOT ANNEXE (Skrull Elite - Skymax). Menace 2[per_hero], 1 icone de boost.
# Forced Response: When a player discards an ally from their hand, they put that ally into play
#   engaged with them instead. Treat that ally as a minion with a blank text box. Its SCH is equal to its
#   printed THW and it does not take consequential damage.
#
# Cartes de reference :
#  - « Treat the ally as a minion with a blank text box. SCH = printed THW, no consequential damage » :
#    **`sw023`** Bad Inspiration / **`27171`** Manipulated Mind (`TreatAsMinion(allie, "Minion", joueur, effect,
#    process=...)`, treat.py : SCH = THW imprime, gabarit sans etoile donc pas de degats consequents, retour a la
#    face d'allie quand le sbire quitte le jeu).
#  - « would discard ... instead » : **`sk141`** (`WhenCardWouldDiscard` + `message.SetBeInstead(effect)`).
#
# ⚠ Mots-pieges : « a player discards an ALLY FROM THEIR HAND » (pas un allie en jeu, pas une carte du deck) ;
# « put THAT ally into play ENGAGED WITH THEM » (le joueur qui defaussait, pas le premier joueur) ;
# « INSTEAD » : l'allie ne va PAS dans la defausse (la defausse est remplacee) ; texte imprime blanc : aucune de
# ses capacites ne s'applique, sauf les traits imprimes ; le texte dit « Forced Response » mais decrit un
# remplacement (« instead ») : lecture retenue = remplacement d'une defausse, voir defs/modulaires_questions.md.


def GetAbilities() -> Sequence['Ability']:

    def allie_de_la_main(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> bool:
        Unused(effect)
        face = message.trigger
        joueur = face.GetControlByOrOwner()
        return Ally.IsType(face) and Player.IsType(joueur) and face.card.area.flags.is_in_hand

    def reprendre_l_allie(minion: 'Any', allie: 'Any', effect: 'Effect') -> None:
        Unused(effect)
        minion.SetName(allie.printed_name)
        minion.SetSubtitle(allie.printed_subtitle)

    def trahir(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        allie = message.trigger
        joueur = allie.GetControlByOrOwner()
        message.SetBeInstead(effect)
        TreatAsMinion(allie, GABARIT_SBIRE, joueur, effect, process=reprendre_l_allie)

    return [
        AbilityFactory.WhenCardWouldDiscard(AbilityType.NonKeyword, Ally, trahir, conditions=[allie_de_la_main]),
    ]
