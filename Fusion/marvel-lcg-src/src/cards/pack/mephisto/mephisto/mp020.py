from . import *

# Alter the Deal — TRAITRISE. Boost 2.
# When Revealed : Shuffle each BARGAIN attachment you control into the encounter deck. For each BARGAIN attachment shuffled this way, resolve the
# "Hidden Clause" ability on the main scheme. Then, discard cards from the top of the encounter deck until a BARGAIN attachment is discarded.
# Attach that card to your identity. Otherwise, shuffle this card into the encounter deck.
#
# Cartes de reference : `Faces.ShuffleAllTo(.., "EncounterDeck", ..)` (mp005a), `ResoudreLaClauseCachee`, `Faces.DiscardAll`, `AttachTo2`.
# ⚠ Mots-pieges : « EACH BARGAIN YOU control » (ceux de l'identite de CE joueur) ; « FOR EACH ... shuffled » : une Hidden Clause par pacte remelange,
# resolue POUR LUI ; la carte attachee n'a PAS de When Revealed (elle est defaussee puis attachee : pas de choix, pas d'activation) ;
# « Otherwise » = aucun BARGAIN trouve avant d'epuiser le deck : cette traitrise est remelangee au lieu d'etre defaussee.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        pacts = PactsDuJoueur(joueur)
        if pacts:
            Faces.ShuffleAllTo(pacts, "EncounterDeck", effect)
            for _ in pacts:
                ResoudreLaClauseCachee(effect, joueur)
        # ⚠ Une copie des cartes du deck, dessus d'abord : le moteur remelange la defausse quand le deck de rencontre est vide, une boucle sur
        # `GetSize() > 0` ne s'arreterait jamais s'il n'y a aucun BARGAIN (c'est le cas « Otherwise » imprime).
        for carte in list(Worlds.GetEncounterDeck(effect).GetAll()):
            Faces.DiscardAll([carte], effect)
            if carte.HasTrait("BARGAIN"):
                carte.CastTo(Attachment).AttachTo2(joueur.GetIdentity(), effect)
                return
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
