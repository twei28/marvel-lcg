from . import *

# * Sif's Chambers — soutien signature, x1 (n/15 = 11).
# ASGARD. LOCATION. Cout 1, ressource [mental].
# Alter-Ego Action: Exhaust Sif's Chambers -> heal 1 damage from Lady Sif.
#   Heal 1 damage from Thor or Odinson. Choose a Lady Sif card in your discard
#   pile and shuffle it into your deck.
#
# Cartes de reference :
#  - `aa003` * Ebony pour le squelette « soutien + Alter-Ego Action payee par
#    `CostFunc.Exhaust("This")` » ;
#  - `38007` Energy Transfer pour `this.HealthUnits(cibles, 1, effect)` ;
#  - `aa009` * The Witches' Road pour le remelange depuis la defausse :
#    `AskChooseFaces` sur `discard_pile.Get(True)` puis
#    `Faces.ShuffleAllTo([face], joueur.player_deck, effect)`.
#
# ⚠ ARBITRAGE DE L'UTILISATEUR (03/09/2026) — « Heal 1 damage from THOR OR
# ODINSON ». « Odinson » n'est le nom d'AUCUNE carte du pack : c'est le
# SOUS-TITRE de l'allie ls002 (* Thor — Odinson). Trois lectures etaient
# possibles ; l'utilisateur a tranche pour **la plus large** : n'importe quel
# personnage amical EN JEU nomme « Thor » ou « Odinson », y compris chez un
# AUTRE joueur. Le texte ne dit en effet pas « you control ».
# Consequences assumees, a garder en tete en multijoueur :
#  - les Thor OFFICIELS (`13011`, `25013`, `59020`) et `ra002` * Odinson
#    (allie de Thor Jane Foster) sont des cibles legales ;
#  - la face heros officielle `06001a` * Thor l'est aussi si elle est en jeu.
# En solo avec le deck de depart livre, la seule cible possible reste ls002.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Le `->` ne couvre QUE le premier soin. Les deux phrases suivantes ne sont
#    pas des couts et ne sont pas conditionnelles : elles tombent meme si
#    aucun degat n'a ete soigne.
#  - « heal 1 damage from LADY SIF » : l'IDENTITE. Les deux faces portent le
#    meme nom, et l'Action est une Action d'ALTER-EGO : c'est donc la face
#    civile qui est en jeu, et c'est elle qu'on soigne. On passe par
#    `GetIdentity()`, pas par un `CardFinder(name="Lady Sif")` — l'allie
#    officiel `06002` * Lady Sif porte le meme nom.
#  - « a LADY SIF card » : une carte du SET « Lady Sif », pas une carte qui
#    porte ce nom. D'ou `CardFinder(set_name="Lady Sif")`, qui compare
#    `face.paper.set_name` (checker.py:88). L'obligation ls012 en fait partie,
#    mais elle ne va jamais dans la defausse du JOUEUR.
#  - « in YOUR discard pile » : celle du joueur, pas la defausse rencontre.
#  - Les trois effets sont sequentiels et tous facultatifs dans leur cible :
#    aucun ne bloque les suivants s'il n'a rien a faire.


NOMS_THOR = ("Thor", "Odinson")


def GetAbilities() -> Sequence['Ability']:

    def thors_en_jeu(effect: 'Effect') -> List['CardFace']:
        # Lecture LARGE arbitree le 03/09/2026 : tous les joueurs, pas
        # seulement le controleur du soutien.
        return [face for face in Worlds.GetOnFieldFriendlyCharacters(effect)
                if face is not None and any(face.IsName(n) for n in NOMS_THOR)]

    def sifs_chambers(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        # 1. « heal 1 damage from Lady Sif » — l'identite du joueur.
        identite = joueur.GetIdentity()
        if identite is not None:
            this.HealthUnits([identite], 1, effect)

        # 2. « heal 1 damage from Thor or Odinson » — au choix s'il y en a
        #    plusieurs en jeu.
        cibles = thors_en_jeu(effect)
        if cibles:
            choisie = joueur.AskChooseFace(cibles, effect,
                                           prompt="Heal 1 damage from Thor or Odinson")
            this.HealthUnits([choisie or cibles[0]], 1, effect)

        # 3. « Choose a Lady Sif card in your discard pile and shuffle it into
        #    your deck » — une carte du SET, pas une carte de ce NOM.
        defausse = CardFinder(set_name="Lady Sif").Checks(
            joueur.discard_pile.Get(True))
        if defausse:
            choisie = joueur.AskChooseFace(list(defausse), effect,
                                           prompt="Shuffle a Lady Sif card into your deck")
            Faces.ShuffleAllTo([choisie or defausse[0]], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            sifs_chambers,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
