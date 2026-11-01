from . import *

# Cassandra's Telepathic Cloak (attachement ARTIFACT ITEM, Boost 1). « Attach to Cassandra Nova. If she is not in play, find Cassandra Nova, reveal her, and then attach
# this card on her. Cassandra Nova cannot take any amount of damage. Forced Response : After Cassandra Nova attacks you, discard this card. »
# Cartes de reference : 02020 Hysteria (`AttachToFaceWhenPutIntoPlay(CardFinder(name=...))`), sk033 / wt017 (`*UnitCannotTakeDamage(...)`, liste a deballer), 21160 Loki,
# hf101a (`AfterUnitAttackYou`), pt019 (`AttachTo2`).
# ⚠ « cannot take ANY amount of damage » : `UnitCannotTakeDamage` previent tout (PreventDamage "All") tant que le manteau est EN JEU, attache ou non (elle seule porte le nom).
# ⚠ « After Cassandra Nova attacks YOU » : une attaque contre un autre joueur ne defausse pas le manteau.


def GetAbilities() -> Sequence['Ability']:
    cassandra = CardFinder(name=NOM_CASSANDRA, card_type=Minion)

    def pas_en_jeu(effect: 'Effect', joueur: 'Player') -> None:
        # « If she is not in play, find Cassandra Nova, reveal her, and then attach this card on her. »
        this = effect.this
        face = ChercherCassandra(effect)
        if face is not None and not face.IsInPlay():
            face.Reveal(joueur, effect)
        if face is not None and face.IsInPlay():
            this.AttachTo2(face, effect)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(cassandra, if_cannot_operation=pas_en_jeu),
        *AbilityFactory.UnitCannotTakeDamage(cassandra),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, cassandra, apres_attaque),
    ]
