from . import *

# Conflicted Feelings — OBLIGATION du SET NEMESIS, custom « CptScorp »
# 1 icone de bonus, `GiveTo "Thomas Shepherd"`.
# While this obligation is in play, Coat of Arms cannot be damaged.
# Alter-Ego Action: Spend [energy][mental] resources -> discard this card.
#
# ⚠ C'EST UNE OBLIGATION QUI APPARTIENT AU SET NEMESIS : le scan la numerote
# « SPEED NEMESIS (5/5) » et elle porte une icone de bonus. Elle vit donc dans
# `nemesis_set` (melangee au deck rencontre avec le reste du set quand sd017
# est revelee), PAS dans la cle `obligations` du deck de depart, qui ne porte
# que sd017 No Outrunning This.
#
# ⚠ ELLE DOIT RESTER EN JEU. C'est ce qui la distingue de toutes les autres
# obligations du depot, qui se resolvent et partent. Le seul precedent est
# `28021` Weight of the World (Nova) : « While this card is in play, Supernova
# Helmet cannot ready. Alter-Ego Action: ... -> remove this obligation from the
# game. » Meme forme exactement.
#
# COMMENT ELLE RESTE : en NE DECLARANT AUCUN `WhenThisObligationGiveToYou`.
# `Obligation.OnWhenCardRevealed` (obligation.py:86-99) met la carte en jeu
# dans `obligations_area` puis envoie `WhenObligationGiveToPlayer` ; la
# defausse automatique qui suit ne concerne que le cas
# `card.area.flags.is_dealt_encounter`. Sans capacite de resolution, la carte
# demeure — exactement comme 28021.
#
# ---------------------------------------------------------------------------
# « COAT OF ARMS CANNOT BE DAMAGED » ->
# `*AbilityFactory.UnitCannotTakeDamage(CardFinder(name="Coat of Arms"))`
# (factory/damage.py:255). La fabrique agit TANT QUE CETTE CARTE-CI EST EN JEU
# (les capacites d'une carte ne sont actives qu'en jeu) : c'est le « While this
# obligation is in play », et quand l'obligation est defaussee la protection
# tombe avec elle. Meme mecanisme que le `CardCannotReady` de 28021.
#
# ⚠ CETTE FABRIQUE A ETE CORRIGEE POUR CETTE CARTE (voir le `# CORRECTIF` de
# damage.py) : elle plantait sur un `NameError` et, une fois ce plantage leve,
# ne faisait RIEN — son `BuffCannotTakeDamage` est une classe marqueur qu'aucun
# chemin de degats ne consulte. Elle rend desormais une LISTE (le buff pour
# l'affichage, plus la vraie prevention), d'ou le `*` devant l'appel.
#
# La recherche par nom est bornee au nom unique du set (« Coat of Arms »,
# ecrit SANS l'etoile d'unicite que `cards/paper.py:45` retire).
#
# ---------------------------------------------------------------------------
# « ALTER-EGO ACTION: SPEND [energy][mental] RESOURCES -> DISCARD THIS CARD »
# -> `AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction)
# .SetCost(Cost("YB"))`, la meme fabrique que 01100 / 04072 / sd020, ici en
# mode alter-ego.
#
# Le cout est **1 energie + 1 mental**, releve par DECOUPE D'IMAGE du coin de
# texte (`/tmp/claude-1000/speed_work/cf_cout.png`), jamais a vue — lecon
# Lockjaw. `Cost("YB")` est le litteral du moteur pour ce couple
# (element/cost.py:38-42).
#
# « discard this card » et non « remove from the game » (28021) : c'est le mot
# imprime, la carte retourne donc dans la defausse rencontre et peut revenir.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.UnitCannotTakeDamage(
            CardFinder(name=NOM_COAT_OF_ARMS),
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCost(Cost("YB")),
    ]
