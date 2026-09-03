from . import *

# Cosmic Connection — traitrise NEMESIS, x2 (3/5 et 4/5). Boost 1.
# When Revealed: If the Cosmic Ax attachment is in play and your hero has a
#   [[WEAPON]] card in play, take 3 indirect damage. If no damage was taken
#   this way, this card gains surge.
#
# Cartes de reference :
#  - `06030` Trickster / `as025` pour `WhenThisRevealed(None, op)` et
#    `message.GetToPlayer()`.
#  - `ag013` Hallucination (pack agent_13) pour l'idiome global
#    `ThisCardGainSurge(effect)`.
#  - `Worlds.FindCardOnField(effect, name="Cosmic Ax")` (worlds.py:451),
#    modele `aos/batroc/__init__.py:7` pour la recherche d'une carte nommee.
#  - `this.DealDamage(..., property=AttackProperty(indirect_damage=True))`
#    pour les degats INDIRECTS.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - DEUX conditions cumulatives, reliees par « **and** » : la Cosmic Ax en
#    jeu ET une carte WEAPON chez le heros. L'une sans l'autre ne fait rien.
#  - « **your hero** has a [[WEAPON]] card in play » : une carte de trait
#    WEAPON que le JOUEUR controle. Dans ce pack, deux la portent — `nt003b`
#    Battle Board cote arme et `nt009` Escrima Sticks — et c'est la moitie du
#    sel de la carte : elle punit exactement la face que le pack cherche a
#    montrer.
#    ⚠ La Cosmic Ax elle-meme porte WEAPON, mais elle est attachee a TERRAX,
#    pas au heros : elle ne satisfait donc pas la seconde condition, et le
#    filtre sur les cartes du joueur est ce qui l'exclut.
#  - « **3 indirect** damage » : indirects, donc repartissables et non
#    prevenus par une defense. Pas de simple `DealDamage` nu.
#  - « If **no** damage was taken this way » : zero, pas « moins de trois ».
#    Et c'est la condition qui rend la carte dangereuse quand elle ne mord
#    pas : Dechainement enchaine une carte rencontre de plus.


def GetAbilities() -> Sequence['Ability']:

    def cosmic_connection(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            ThisCardGainSurge(effect)
            return

        hache = Worlds.FindCardOnField(effect, name="Cosmic Ax")

        # ⚠ `GetControlCardsByType` (player_get.py:107) et pas
        # `GetControlCards()` : il faut nommer explicitement les familles
        # regardees, sans quoi les AMELIORATIONS attachees au heros — donc
        # `nt003b` Battle Board cote arme et `nt009` Escrima Sticks, les deux
        # seules cartes WEAPON que ce heros puisse controler — sont hors du
        # balayage et la condition est toujours fausse.
        # ⚠ `attachment=False` : la Cosmic Ax porte elle aussi WEAPON, mais
        # elle est attachee a TERRAX et pas au heros. La compter ici rendrait
        # la premiere condition suffisante a elle seule.
        armes = joueur.GetControlCardsByType(
            CardFinder(trait="WEAPON"),
            ally=True, upgrade=True, support=True, identity=True,
            attachment=False,
        )
        arme_du_heros = armes[0] if armes else None

        if hache is None or arme_du_heros is None:
            ThisCardGainSurge(effect)
            return

        identite = joueur.GetIdentity()
        if identite is None:
            ThisCardGainSurge(effect)
            return

        # ⚠ `AttackProperty` N'A PAS de `indirect_damage` : la premiere
        # ecriture le passait, et le moteur levait un TypeError — visible au
        # journal, mais la carte ne faisait plus RIEN. La bonne API est
        # `DealIndirectDamage` (card_face.py:583), qui redirige vers
        # `unit.TakeIndirectDamage`.
        this.DealIndirectDamage(identite, 3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            cosmic_connection,
        ),
    ]
