from . import *

# * Ghost Rider (Zero Cochrane) — ALLIE, cout 2 [energy], THW 1 / ATK 2
#   (1 degat consequent chacun), 2 PV. ANDROID. INFERNAL.
# Response: After Ghost Rider is discarded by your Acceleration ability, deal
#   1 damage to an enemy.
# Interrupt: When Ghost Rider is defeated, place him on the bottom of his
#   owner's deck.
#
# CARTES DE REFERENCE
#  - `40057` * White Fox: Ami Han : LE modele. Un ALLIE qui reagit APRES avoir
#    ete defausse depuis le dessus du deck, donc DEPUIS LA DEFAUSSE, ou ses
#    capacites sont normalement muettes. La fabrique est
#    `AfterCardDiscardInternal(Response, "This", op, from_where="PlayerDeckTop")`,
#    et c'est elle qui autorise la carte a agir hors du jeu
#    (`ignore.out_of_play`, ability.py:132). Sans cette fabrique precise, la
#    Reponse serait construite, verte a la construction, et **muette en
#    partie** : la condition de zone (`is_in_play_or_hand_or_temp_or_delay`)
#    la refuserait en silence.
#  - `bt011` : `Faces.MoveAllToDeck([face], player.player_deck, ..., effect)`.
#    ⚠ La position est un argument POSITIONNEL (RECETTES §2), et c'est
#    « Bottom » ici, pas « Top ».
#  - `ag006`, `th009` : `this.DealDamage(cibles, n, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « discarded BY YOUR ACCELERATION ABILITY » : la portee compte. Le
#    declencheur du moteur ne sait dire que « defausse depuis le dessus du
#    deck » — or `sm015` Electro, `sm016` Power Surge et `sm017` Charged
#    defaussent EUX AUSSI depuis le dessus du deck, et Ghost Rider ne doit PAS
#    partir sur ceux-la. D'ou la condition `par_acceleration`, qui lit le
#    marqueur du pack. **Sans elle, la carte se declencherait sur toute la
#    nemesis**, ce qui est l'inverse de ce que la carte promet.
#  ⚠ Le filtre va dans `conditions`, PAS dans le corps (RECETTES §1) : une
#    Response est PROPOSEE au joueur des que le message part. `AfterCardDiscard`
#    est frequent, c'est exactement le cas `bc010` (250 questions en 8 parties).
#  ⚠ « deal 1 damage to AN ENEMY » : une cible choisie, `SetTarget(Enemy)`.
#  ⚠ « place him on the bottom of HIS OWNER'S deck » : le deck du PROPRIETAIRE,
#    pas celui du joueur qui l'a vaincu — `GetControlByOrOwner` via
#    `JoueurDeCetteCarte`.
#  ⚠ « When ... is defeated » = INTERRUPTION : `WhenUnitBeDefeated`, qui part
#    AVANT que la carte ne parte a la defausse. C'est ce qui permet de la
#    detourner vers le deck (`WhenUnitBeDefeated` vs `AfterUnitBeDefeated` :
#    l'un resout avant l'evenement, l'autre apres — PROCESSUS-CARTE §5).
#  ⚠ Les losanges imprimes SOUS « THW » et « ATK » sont les degats
#    consequents, et ils se declarent dans la VALEUR : `"THW": "1*"`,
#    `"ATK": "2*"` (RECETTES §5, `can_attack.py:47-52`). Aucun script.


def GetAbilities() -> Sequence['Ability']:

    def par_acceleration(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        """« BY YOUR ACCELERATION ABILITY » — et pas par la nemesis."""
        Unused(message)
        return AccelerationEnCours(effect)

    def degats(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    def sous_le_deck(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        proprietaire = JoueurDeCetteCarte(effect)
        if proprietaire is None:
            return
        deck = getattr(proprietaire, "player_deck", None)
        if deck is None:
            return
        Faces.MoveAllToDeck([this], deck, "Bottom", effect)

    return [
        AbilityFactory.AfterCardDiscardInternal(
            AbilityType.Response,
            "This",
            degats,
            from_where="PlayerDeckTop",
            conditions=[par_acceleration],
        ).SetTarget(Enemy),

        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            sous_le_deck,
        ),
    ]
