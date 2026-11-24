from . import *

# * Valeria Richards — ALLIE (Survivor deck, carte 3/5). Cout 0. THW 3[star]. ATK 0. PV 2. RES wild.
#   SURVIVOR. FANTASTIC.
# Action: Exhaust Valeria Richards -> choose one:
# - Change form.
# - Deal 3* damage to The Hunger Core.
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - Charpente « Action: Exhaust <nom> -> choose one: ... » : meme modele que `hg072` Franklin Richards
#   (`09002` Wong) : `SetCostFunc(CostFunc.Exhaust("This"))` puis `initiator.ChooseAbilities(effect,
#   ForChoiceAbility(...), ForChoiceAbility(...))`. Les DEUX branches de Valeria n'ont toutefois besoin
#   d'AUCUN `SetTarget` (aucune des deux ne demande au joueur de designer une carte) -- modele d'une branche
#   SANS cible dans un `ChooseAbilities` : `nt012` Practice (pack `night_thrasher`), dont les trois
#   `ForChoiceAbility` prennent un callback `(cibles: Sequence['CardFace']) -> None` qui ignore `cibles`
#   (`Unused(cibles)`), sans jamais appeler `.SetTarget(...)`.
# - « Change form » (sans sujet explicite autre que « vous ») : terme de regle de base (PAS un mot-cle en
#   gras imprime, voir plus bas), deja scripte par plusieurs cartes officielles -- `40002` Bodyslide
#   (`initiator.GetIdentity().ChangeToOtherIdentityForm(effect)`, retenu ici : un flip simple Heros<->
#   Alter-Ego) et `42005` Metamorphosis (qui, elle, utilise `ChangeToOtherForm` -- reserve aux heros a PLUS
#   de deux formes imprimees, via un choix de texte ; Valeria elle-meme n'a que deux formes, donc
#   `ChangeToOtherIdentityForm` est le bon choix, voir texte-contre-code).
# - « Deal 3* damage to THE HUNGER CORE » (cible FIXE, nommee, pas un choix du joueur parmi « an enemy ») :
#   modele `hg029`/`hg038`/`hg042` de ce meme scenario, qui ciblent un Metazombie NOMME par
#   `CardFinder(name=..., card_type=Villain)` plutot que par un `SetTarget` laissant le joueur choisir. Ici
#   la cible est UNIQUE dans toute la partie (il n'y a jamais deux « The Hunger Core » en jeu) : le helper
#   DEJA EXISTANT `commun.LeCoeur(effect)` (`cards/pack/the_hunger_core/commun.py:73`) la retrouve directement
#   (quel que soit son stade I/II/III), sans avoir besoin d'un `CardFinder` ni d'un `SetTarget`.
# - « Deal X damage to <cible fixe> » (methode d'application) : `this.DealDamage([cible], X, effect)`, meme
#   methode que `lj024`/`hg073` de ce lot, juste appliquee a une cible fixe plutot qu'a `effect.targets`.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « Change form » : PAS un mot-cle en gras imprime sur cette carte (`cards_custom.json` : `"• Change
#   form."`, prose nue, sans balise `<b>`) -- meme constat que les cartes officielles citees en etape 2
#   (`12016` Moxie : « After you CHANGE FORM », `13014` Surprise Attack : idem, jamais en gras). C'est un
#   terme de regle de BASE (flip Heros<->Alter-Ego), deja implemente nativement par le moteur
#   (`Identity.ChangeToOtherIdentityForm`) : rien a ficher, meme categorie que « Stunned » deja tranchee par
#   `hg037` de ce scenario.
# - « Action » : type de capacite, pas un mot-cle (meme note que `hg072`/`hg073`).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# - « choose one » -> DEUX branches `ForChoiceAbility`, comme `hg072`.
# - « Change form » (SUJET IMPLICITE « you », c'est-a-dire le JOUEUR qui active Valeria, pas Valeria
#   elle-meme -- une alliee n'a pas de forme Heros/Alter-Ego) -> `effect.GetInitiator().GetIdentity().
#   ChangeToOtherIdentityForm(effect)`. Piege a eviter : ne jamais cibler `this` (la face de Valeria) avec
#   `ChangeToForm` -- seule L'IDENTITE DU JOUEUR peut changer de forme.
# - « Deal 3* damage to THE HUNGER CORE » (nom PROPRE, pas « the villain » generique) -> `LeCoeur(effect)`,
#   qui filtre par `v.IsName(CORE)` (`CORE = "The Hunger Core"`), identique quel que soit le stade courant du
#   Coeur. Si `LeCoeur` rend `None` (Coeur deja retire du jeu, scenario termine) : aucun degat n'est applique
#   -- garde defensive, jamais observee en partie normale (le Coeur est toujours en jeu tant que le scenario
#   tourne) mais necessaire pour ne pas planter sur `None`.
# - Le « 3* » DE L'OPTION (« Deal 3* damage ») N'EST PAS LE MEME CHAMP que `desc.THW = "3*"` (le THW imprime
#   de Valeria elle-meme) : coincidence de VALEUR (3 dans les deux cas), pas de MECANISME. `desc.THW` est lu
#   NATIVEMENT par le moteur comme etoile de degats consequents (voir note generale posee dans `hg072.py`) ;
#   le « 3* » de CETTE phrase est en PROSE, absent de `desc` (aucune cle `cards_custom.json` ne porte cette
#   valeur), et son etoile designe donc le symbole GENERIQUE « par heros » documente par le guide (ex. `wd`
#   « 2* » menace, `hg001` « 12* » PV) -- PAS une etoile de degats consequents (qui n'a de sens que pour
#   ATK/THW d'un Allie/Heros, jamais pour un degat infligATOIRE a une cible exterieure). Code retenu :
#   `3 * NombreDeJoueurs(effect)` (helper deja existant, `commun.py:303`), exactement le calcul que fait
#   `FormatPlayerNumValue` pour les attributs `desc` qui en beneficient nativement.
# - Pas de `unless`/`otherwise`/`instead`/limite imprimee : rien d'autre a coder.
#
# ---------------------------------------------------------------------------
# ETAPE 6 : BLOC NOMBRES, TEXTE <-> CODE
#
# - « Deal 3* damage » -> `3 * NombreDeJoueurs(effect)` (3 en partie a 1 joueur, 6 a 2, 9 a 3, 12 a 4 --
#   coherent avec les PV du Coeur lui-meme, qui scalent de la meme facon).
# - `desc.THW = "3*"` : LU NATIVEMENT (etoile de degats consequents d'Allie), aucun script requis (voir note
#   generale `hg072.py`).
#
# A CONFIRMER EN PARTIE REELLE : meme reserve que `hg072`/`hg073`. Si le Coeur a deja ete vaincu par un
# autre moyen au moment ou cette branche est choisie (situation qui ne devrait jamais survenir en cours de
# scenario normal), l'option « Deal 3* damage » ne ferait simplement rien (garde `if coeur is not None`),
# comportement defensif jamais prouve en jeu reel par ce lot.


def GetAbilities() -> Sequence['Ability']:

    def valeria(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()

        def changer_de_forme(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            initiator.GetIdentity().ChangeToOtherIdentityForm(effect)

        def frapper_le_coeur(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            coeur = LeCoeur(effect)
            if coeur is None:
                return
            this.DealDamage([coeur], 3 * NombreDeJoueurs(effect), effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Change form",
                changer_de_forme,
            ),
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage per hero to The Hunger Core",
                frapper_le_coeur,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            valeria,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
