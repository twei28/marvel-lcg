from . import *

# Mr. Hyde's Lab — MANIGANCE ANNEXE nemesis, custom « CptScorp »
# `StartingThreat "2*"` (2 PAR JOUEUR), 2 icones de bonus, `Crisis "1"`.
#
# When Defeated: Mr. Hyde attacks you. If no attack was made this way, search
#   the encounter deck and encounter discard pile for Mr. Hyde and put him
#   into play.
#
# ---------------------------------------------------------------------------
# ⚠ L'ICONE CRISIS A ETE VERIFIEE PAR DECOUPE D'IMAGE, NE PAS RE-LITIGER
#
# Contre la carte-temoin `ag011`, dont le `desc` declare `Crisis` ET
# `Acceleration`, avec `hd022` (Hazard) et `hd026` (Acceleration) en
# controles : c'est bien un BURST NOIR AVEC « ! », donc Crisis, et il n'y a
# AUCUNE autre icone. `Crisis` est lu NATIVEMENT dans `desc` (`CanCrisis`) :
# aucun module a ecrire pour lui, et coder une capacite fantome serait une
# faute. Fiche : docs/reference/mots-cles/crisis.md.
#
# `StartingThreat "2*"` : l'etoile est le marqueur « par joueur » du moteur,
# lu nativement lui aussi. Deux menaces par joueur a l'entree en jeu.
#
# ---------------------------------------------------------------------------
# TYPE : `SideScheme` EN JSON = CLASSE `EncounterSideScheme` DANS LE SCRIPT
# (piege connu, GUIDE §10).
#
# ---------------------------------------------------------------------------
# LE DECLENCHEUR
#
# `AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", ...)`
# — modele `jj012` Always a Bigger Conspiracy, meme fabrique pour un
# « When Defeated » de manigance annexe.
#
# « ATTACKS **YOU** » : le joueur qui vient de battre la manigance,
# `message.defeating_player` (sender_scheme.py:175-184). La fabrique le
# calcule a partir du tueur ou de l'initiateur de l'effet ; s'il est absent
# (une manigance peut tomber par un effet du scenario), on retombe sur le
# premier joueur, ce que fait deja `jj012`.
#
# ---------------------------------------------------------------------------
# « IF NO ATTACK WAS MADE THIS WAY »
#
# `enemy.DoAttackYou(player, effect, if_no_attack_was_made=action)` : brique
# exacte du moteur, modeles `02040` Tail Sweep et `22031` Old Rivals. Le
# repli part quand l'attaque n'a pas eu lieu (joueur en identite civile,
# attaque annulee...).
#
# ET AUSSI quand Mr. Hyde n'est PAS EN JEU DU TOUT : c'est le cas nominal de
# cette carte, et `02040` traite deja ce cas par un `else: action()`. C'est
# la lecture qui donne son sens a la carte — la manigance FAIT VENIR le
# sbire, ou le laisse frapper s'il est deja la.
#
# « search the encounter deck AND encounter discard pile » -> `Search
# .EncounterCard(effect, joueur, include_discard_pile=True, ...)`. DEUX zones
# seulement : la carte ne dit PAS « and set aside cards » (contrairement a
# pt019, qui en cite trois — mot-piege du PROCESSUS-CARTE §5, on ne recopie
# pas une carte sur l'autre).
#
# Modeles du couple recherche + mise en jeu : `60060` (pack fne, Echo) et
# `bw021` Namor (pack brawn), tous deux en
# `Search.EncounterCard(...)` puis `face.PutIntoPlay(joueur, effect)`.


def GetAbilities() -> Sequence['Ability']:

    def mr_hydes_lab(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        joueur = message.defeating_player
        if joueur is None:
            joueur = Worlds.GetFirstPlayer(effect)
        if joueur is None:
            return

        def faire_venir_mr_hyde():
            face = Search.EncounterCard(
                effect,
                joueur,
                include_discard_pile=True,
                name=NOM_MR_HYDE,
                card_type=Minion,
            )
            if face:
                face.PutIntoPlay(joueur, effect)

        hyde = Worlds.FindCardOnField(effect, name=NOM_MR_HYDE, card_type=Enemy)
        if hyde:
            hyde.DoAttackYou(joueur, effect,
                             if_no_attack_was_made=faire_venir_mr_hyde)
        else:
            faire_venir_mr_hyde()

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            mr_hydes_lab,
        ),
    ]
