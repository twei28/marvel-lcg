from . import *

# * The Mangog

def GetAbilities() -> Sequence['Ability']:

    # CORRECTIF : la carte ne faisait RIEN. Elle declarait un WhenThisRevealed
    # et un WhenCardBecomeBoost au corps entierement commente, et son
    # « When Defeated » n'etait pas declare du tout. Le texte imprime n'a ni
    # capacite de revelation ni capacite de boost : les deux stubs sont retires.
    # « Any player in your pod can attack The Mangog » est sans effet dans
    # l'adaptation a 1 groupe de ce scenario (voir __init__.py du set).

    def the_mangog_defeated(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # Les 3 compteurs shatter sont poses par le helper ; ici le compteur
        # de synergie, sur le premier environnement SYNERGY pas encore plein
        # (meme parcours que 55046, qui porte le meme texte).
        for name in ('Unified Front', 'Mounting Resistance', 'Domineering Force', 'Feigned Retreat'):
            face = Worlds.FindCardOnField(effect, name=name, card_type=Environment)
            if face and (face.CastTo(CanPlaceCounter).GetCounters('synergy') < Worlds.GetPlayerNumIcon(effect)):
                PlaceSynergyCounters(name, 1, effect)
                break

    return [
        WhenDefeatedPlaceShatterCountersOnTheAvatarOfLokivillain(3, the_mangog_defeated),
    ]
