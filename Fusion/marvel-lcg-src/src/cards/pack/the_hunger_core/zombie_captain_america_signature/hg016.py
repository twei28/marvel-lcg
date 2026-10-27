from . import *

# Thrown Shield — TREACHERY (set signature Zombie Captain America, carte 1/3). Trait ATTACK.
# When Revealed: Deal 2 damage to each hero and each ally in play.
#
# Carte de reference :
#  - « When Revealed: Deal N damage to each hero and ally in play » : texte IDENTIQUE (seule la valeur change)
#    a `24035` * Mister Hyde (pack hood, minion) : `this.DealDamage(Worlds.GetOnFieldHeroes(effect) +
#    Worlds.GetOnFieldAllies(effect), 1, effect)`. `Worlds.GetOnFieldHeroes` (worlds.py:246) ne retient que les
#    identites EN FORME HEROS (`Hero.IsType`), `Worlds.GetOnFieldAllies` (worlds.py:250) prend TOUS les allies
#    de TOUS les joueurs : exactement la portee de « each hero » / « each ally in play », sans restriction a
#    « that player » ni a « you » (contrairement a `hg012` Zombie Thor qui vise un seul joueur). Variante vue
#    sur `ch020` The Life Stealer (shang_chi_nemesis) qui emploie `Worlds.GetOnFieldFriendlyCharacters` (inclut
#    aussi les Alter-Ego) pour un texte « indirect damage to each hero AND ALLY » : ecarte ici parce que
#    `GetOnFieldFriendlyCharacters` ramasse les identites quelle que soit leur FORME, alors que le texte de
#    cette carte dit « hero », pas « player »/« identity » -- modele de `24035` retenu au mot pres.
#  - Fabrique `AbilityFactory.WhenThisRevealed(None, op)` + `Message.WhenCardRevealed`, modele `wd014` Get
#    Shocked! (meme fabrique sur une Treachery, `this = effect.this.CastTo(Treachery)`).
#
# ⚠ Mots-pieges :
#  - « each hero » (pas « each player »/« your hero ») : une identite en forme ALTER-EGO n'encaisse PAS ce
#    degat -- c'est tout l'interet de `GetOnFieldHeroes` plutot que `GetPlayersIdentities` ou
#    `GetOnFieldFriendlyCharacters` (ces deux dernieres ramassent l'identite quelle que soit sa forme).
#  - « each ally IN PLAY » : tous les allies de la table, de TOUS les joueurs (pas seulement ceux du joueur a
#    qui la carte est revelee) -- aucun filtre par joueur, contrairement a `hg012` (« each ally THAT PLAYER
#    controls », filtre explicitement sur le joueur de l'activation).
#  - Degats DIRECTS hors attaque (`this.DealDamage(..., effect)`, pas une attaque de `this`) : la Treachery n'a
#    ni ATK ni cible choisie, comme `wd014`/`24035`/`ch020`.
#  - Trait imprime « ATTACK » : trait DE SAVEUR du jeu officiel sur les Treachery de ce type (ex. `01106`
#    Taking Punches), pas un mot-cle moteur, rien a coder pour lui (confirme par grep sur
#    `docs/reference/mots-cles/README.md` : absent).
#  - Pas de surge, pas de choix de cible, pas de restriction « unless »/« otherwise » dans le texte imprime :
#    rien d'autre a coder.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)

        this.DealDamage(Worlds.GetOnFieldHeroes(effect) + Worlds.GetOnFieldAllies(effect), 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
