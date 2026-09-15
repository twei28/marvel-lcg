"""Simulateur de parties : joue un deck N fois et rend victoires, defaites et rounds.

Le moteur se pilote sans navigateur : toutes ses decisions passent par
DeviceManager.DoGetInput, qu'on detourne pour y brancher une politique de jeu.
Chaque partie tourne dans SON PROPRE PROCESSUS, le moteur etant un singleton
global impossible a reinitialiser proprement entre deux parties.

Ce que l'outil mesure
---------------------
Victoires, defaites, rounds tenus, cartes jouees, cause de fin. A politique
identique et graines identiques, deux decks sont directement comparables.

Ce qu'il ne mesure pas
----------------------
Un taux de victoire depend AUSSI du niveau du pilote, qui est une heuristique
et pas une IA de recherche. D'ou les trois profils : un deck qui ne gagne
qu'avec le profil agressif ne se joue pas tout seul.

Usage
-----
    python3.10 tools/autoplay.py .game-src --deck spider_man \\
        --vilains rhino,klaw --difficultes normal,expert \\
        --profils prudent,equilibre,agressif --parties 500

`--deck` accepte un nom de deck de depart (deck/starter/<nom>.json) ou un
chemin vers un fichier de deck exporte. Viser .game-src (liens vers src/),
jamais .game qui n'est que du bytecode.

Python 3.10 obligatoire : ~/marvel-work/python/bin/python3.10
"""
import argparse
import json
import os
import subprocess
import sys
import time

os.environ.setdefault("RELEASE", "1")

# Plafond de questions par partie. Une partie normale en demande quelques
# milliers ; au-dela on considere que le moteur tourne en rond.
MAX_ASKS = 80000

# Nombre de fois qu'une meme option peut etre choisie dans une meme situation
# avant d'etre mise de cote. Sans ce garde-fou, une action que le moteur
# propose puis refuse (vu sur Enhanced Ivory Horn) bloque la partie a l'infini.
MAX_REPETITIONS = 2

# ⚠ COMBIEN DE FOIS UNE CAPACITE NOMMEE PEUT ETRE REPRISE DANS UN MEME ROUND.
#
# Un humain prend une Action repetable une ou deux fois, puis passe a autre
# chose. Le pilote, lui, la reprenait tant qu'elle gagnait au score : mesure du
# 15/09/2026 sur `iron_patriot`, l'Action « Enlistment » de `ip002a` prise
# 21 FOIS dans le seul round 1, 20 allies REGISTERED entres en jeu, partie
# perdue au round 1,0 sur 16 parties sur 16.
#
# ⚠ LA DECROISSANCE DU SCORE (20/(1+n)) N'Y SUFFIT PAS, et la trace des scores
# dit pourquoi. Vers la fin du round il ne reste que DEUX options, et la
# seconde s'effondre plus vite que la premiere :
#
#     scores r1: [('Enlistment', 6.67), ('Change_Form', 2.82)]   -> Enlistment
#     scores r1: [('Enlistment', 5.00), ('Change_Form', -2.64)]  -> Enlistment
#     scores r1: [('Enlistment', 3.33), ('Change_Form', -13.55)] -> Enlistment
#     scores r1: [('Enlistment', 2.86), ('Change_Form', -19.00)] -> Enlistment
#
# Chaque enrolement amene des sbires que le joueur ne controle pas : les degats
# entrants montent, l'urgence de survie avec eux, et passer en forme heros
# devient de plus en plus suicidaire aux yeux du scorer. Le pilote s'enterre, et
# plus il s'enterre, plus s'enterrer encore est ce qu'il trouve de mieux.
#
# On ECARTE donc l'option au-dela du plafond, au lieu de la noter plus bas.
# ⚠ Ecarter, pas annuler : noter negativement avait ete essaye le 11/09/2026 et
# REJETE, parce que le bot declinait alors et que le moteur reposait la meme
# question. Ici l'option sort de la liste et une AUTRE est choisie, donc la
# partie avance. Et si toutes sont saturees, on rend la liste entiere : mieux
# vaut rejouer la meme chose qu'etre bloque.
PLAFOND_CAPACITE_NOMMEE = 3

# Les noms que le scorer traite explicitement : ce sont les actions de BASE du
# jeu, et elles ne sont jamais plafonnees. Attaquer trois fois avec trois allies
# differents est normal ; reprendre trois fois la meme Action nommee ne l'est
# pas. Tout ce qui n'est pas dans cette liste tombe dans la branche « capacite
# nommee » du scorer (`fixe = 20.0 / (1 + deja_prise)`).
ACTES_DE_BASE = {"Thwart", "Attack", "Defense", "Recover", "Play",
                 "Change_Form", "Change Form", "End Phase", "End_Phase",
                 "Resolve Mulligans"}


def est_capacite_nommee(nom):
    """Une capacite nommee, par opposition aux actions de base du jeu."""
    nom = str(nom or "")
    if nom in ACTES_DE_BASE or nom.startswith("Change_To_"):
        return False
    # « Play:Ally », « Play:Event »... : le journal detaille le type joue.
    return not nom.startswith("Play:") and not nom.lower().startswith("exhaust")


# --------------------------------------------------------------- profils --
# Tous les seuils sont des ratios entre 0 et 1.
#   poids_*       : ponderation de chaque axe dans l'evaluation de l'etat.
#                   poids_activation est la penalite des actions qui consomment
#                   l'activation du heros, la ressource la plus disputee.
#   portee_de_finition : PV du vilain sous lesquels on cesse de temporiser.
#   seuil_repli   : PV restants sous lesquels le heros repasse en alter-ego.
#   seuil_retour  : PV restants au-dessus desquels l'alter-ego repasse heros.
#   seuil_bloc    : PV restants sous lesquels on sacrifie un allie au blocage.
#   sbire_achevable : PV en dessous desquels un sbire passe avant le vilain.
PROFILS = {
    "prudent": {
        "portee_de_finition": 6, "seuil_repli": 0.55, "seuil_retour": 0.85,
        "poids_menace": 14, "poids_survie": 12, "poids_controle": 6,
        "poids_moteur": 5, "poids_progression": 4, "poids_activation": 6,
        "seuil_bloc": 0.50, "sbire_achevable": 3,
    },
    "equilibre": {
        "portee_de_finition": 5, "seuil_repli": 0.45, "seuil_retour": 0.70,
        "poids_menace": 12, "poids_survie": 10, "poids_controle": 6,
        "poids_moteur": 5, "poids_progression": 6, "poids_activation": 5,
        "seuil_bloc": 0.35, "sbire_achevable": 2,
    },
    "agressif": {
        "portee_de_finition": 8, "seuil_repli": 0.30, "seuil_retour": 0.50,
        "poids_menace": 9, "poids_survie": 8, "poids_controle": 5,
        "poids_moteur": 4, "poids_progression": 9, "poids_activation": 4,
        "seuil_bloc": 0.20, "sbire_achevable": 1,
    },
}


# Tags semantiques deduits du texte imprime. Le bot classait les cartes par
# TYPE, ce qui ne distingue pas un generateur de ressources d'une amelioration
# inutile, ni un evenement qui desamorce d'un evenement qui frappe. Or en solo
# le heros n'a qu'une activation par round : desamorcer avec lui annule tout
# juste l'escalade, sans jamais faire baisser la menace. La seule facon de
# gagner est que les CARTES desamorcent pendant que le heros frappe, ce qui
# suppose de savoir ce que fait chaque carte.
MOTS_TAGS = {
    "DESAMORCE": ("thwart", "remove 1 threat", "remove 2 threat", "remove 3 threat",
                  "remove that much threat", "thw"),
    "DEGATS": ("damage", "atk"),
    "SOIN": ("heal",),
    "PIOCHE": ("draw",),
    "ECONOMIE": ("resource",),
    "DEFENSE": ("defense", "def)"),
    "STATUT": ("stunned", "confused", "stun ", "confuse "),
}


def tags_carte(texte, desc, type_carte):
    """Rend l'ensemble des effets qu'une carte sait produire."""
    brut = (texte or "").lower()
    tags = set()
    for tag, mots in MOTS_TAGS.items():
        if any(mot in brut for mot in mots):
            tags.add(tag)
    if type_carte == "Resource":
        tags.add("ECONOMIE")
    # Les bonus imprimes ne sont pas toujours dans le texte.
    for cle, tag in (("THW", "DESAMORCE"), ("ATK", "DEGATS"), ("DEF", "DEFENSE")):
        if (desc or {}).get(cle):
            tags.add(tag)
    return tags


def nombre(valeur, defaut=0):
    """Lit une valeur imprimee comme '14*' ou '3' sans jamais lever."""
    if valeur is None:
        return defaut
    texte = "".join(c for c in str(valeur) if c.isdigit())
    return int(texte) if texte else defaut


# ----------------------------------------------------------- une partie --
def jouer_une_partie(game_dir, port, deck, vilain, difficulte, profil, graine,
                     sortie, trace):
    """Corps execute DANS LE PROCESSUS FILS."""
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    # Mode console : aucun serveur web, donc aucun port a reserver. Sans ca,
    # deux parties lancees en parallele se disputaient le meme launch.json et
    # le meme port, et la seconde mourait sur « port indisponible ».
    sys.argv = [sys.argv[0], "-config_files", "launch.json", "-device", "key"]

    etiquette = f"{os.path.basename(deck)}_{vilain}_{difficulte}_{profil}_{graine}"
    journal = open(f"/tmp/autoplay_{etiquette}.log", "w", buffering=1)
    sys.stdout = journal
    sys.stderr = journal

    from engine.device.manager.base import DeviceManager

    # Reglages injectables : le balayage de tools/calibrer.py explore l'espace
    # des seuils sans toucher au code. Un profil nomme reste le defaut.
    reglages = dict(PROFILS[profil])
    if os.environ.get("AUTOPLAY_REGLAGES"):
        reglages.update(json.loads(os.environ["AUTOPLAY_REGLAGES"]))
    etat = {"asks": 0, "cartes_jouees": 0, "debut": time.time(),
            "historique": {}, "rounds_max": 0}

    def monde():
        from engine import Engine
        return Engine.game.world

    def rendre(verdict, message):
        resultat = {
            "deck": deck, "vilain": vilain, "difficulte": difficulte,
            "profil": profil, "graine": graine, "verdict": verdict,
            "message": message, "asks": etat["asks"],
            "cartes_jouees": etat["cartes_jouees"],
            "rounds": etat["rounds_max"],
            "secondes": round(time.time() - etat["debut"], 1),
            "journal": {str(k): v for k, v in
                        sorted(etat.get("journal", {}).items())},
        }
        try:
            w = monde()
            go = getattr(w, "game_over", None)
            gagne = getattr(go, "players_won", None)
            resultat["gagne"] = gagne
            resultat["raison"] = (getattr(go, "reason", None) or "")
            resultat["rounds"] = max(etat["rounds_max"],
                                     nombre(getattr(w, "round_id", 0)))
            # Etat du vilain en fin de partie : distingue « le bot manque de
            # degats » de « le bot manque de temps ».
            from game.card.face.base.villain import Villain
            for obj in w.object_manager.card_dict.values():
                face = getattr(obj, "face", None)
                if face is not None and isinstance(face, Villain) \
                        and hasattr(face, "IsInPlay") and face.IsInPlay():
                    resultat["vilain_pv"] = nombre(getattr(face, "health", 0))
                    resultat["vilain_pv_max"] = nombre(
                        getattr(face, "max_health", 0))
                    break
        except Exception:
            resultat["gagne"] = None
        with open(sortie, "w") as f:
            json.dump(resultat, f, ensure_ascii=False)
        print("RESULTAT:", json.dumps(resultat, ensure_ascii=False), flush=True)
        os._exit(0)

    # ------------------------------------- capture d'une phase du mechant --
    # ⚠ AUCUN EFFET SANS `AUTOPLAY_CAPTURE`. C'est un outillage, pas un
    # changement de comportement : sans la variable, cette fonction rend la main
    # au premier test et autoplay se comporte exactement comme avant.
    #
    # Pourquoi elle existe (14/09/2026) : il n'existait AUCUN moyen d'observer
    # une phase du mechant hors du navigateur. Aucune fixture ne portait de
    # `faits_mechant`, et trois tentatives de pilotage automatique du navigateur
    # ont echoue (la partie ne depassait pas le round 1). Chaque verification
    # coutait donc une partie jouee a la main.
    #
    # ⚠ ON CAPTURE LE DESCRIPTEUR, PAS L'OBJET `world`. C'est `world.render.descriptor`
    # que la route `/get_world` envoie au client (server_sync.py) : capturer autre
    # chose donnerait une fixture que le plateau ne saurait pas lire.
    capture = {"dossier": os.environ.get("AUTOPLAY_CAPTURE") or "", "faits": 0, "n": 0}

    def capturer_si_phase_mechant():
        if not capture["dossier"]:
            return
        try:
            from engine import Engine
            from engine.lib import Json
            d = Engine.game.world.render.descriptor
            faits = list(getattr(d, "faits_mechant", None) or [])
            # On n'ecrit QUE quand le journal s'est enrichi : sans ce garde-fou,
            # une phase produirait autant de fichiers que de questions posees.
            if len(faits) <= capture["faits"]:
                return
            capture["faits"] = len(faits)
            capture["n"] += 1
            nom = f"phase-mechant-{etiquette}-{capture['n']:02d}.js"
            chemin = os.path.join(capture["dossier"], nom)
            corps = Json.Dumps(d, indent=1)
            with open(chemin, "w", encoding="utf-8") as f:
                f.write("// ETAT CAPTURE par tools/autoplay.py (AUTOPLAY_CAPTURE).\n")
                f.write(f"// {len(faits)} fait(s) de phase du mechant.\n")
                f.write("export default " + corps + "\n")
        except Exception as exc:
            print("CAPTURE ECHOUEE:", exc, flush=True)

    # ------------------------------------------------- lecture de l'etat --
    def lire_etat():
        """Photographie du monde utile a la decision, tolerante aux absences."""
        from game.card.face.base.villain import Villain
        from game.card.face.card_type.minion import Minion
        from game.card.face.card_type.scheme_main import MainScheme
        from game.card.face.card_type.ally import Ally
        from game.card.face.base.scheme import Scheme2

        w = monde()
        ctx = {"faces": {}, "vilains": [], "sbires": [], "schemes": [],
               "schemes_secondaires": [], "allies": [],
               "pv_ratio": 1.0, "menace_ratio": 0.0,
               "round": nombre(getattr(w, "round_id", 0)), "forme_heros": True}

        for oid, obj in w.object_manager.card_dict.items():
            face = getattr(obj, "face", None)
            if face is None:
                continue
            ctx["faces"][str(oid)] = face
            if not (hasattr(face, "IsInPlay") and face.IsInPlay()):
                continue
            if isinstance(face, Villain):
                ctx["vilains"].append(face)
            elif isinstance(face, Minion):
                ctx["sbires"].append(face)
            elif isinstance(face, MainScheme):
                ctx["schemes"].append(face)
            elif isinstance(face, Scheme2):
                ctx["schemes_secondaires"].append(face)
            elif isinstance(face, Ally):
                ctx["allies"].append(face)

        etat["rounds_max"] = max(etat["rounds_max"], ctx["round"])

        # Chaque lecture a son propre garde : `hand_cards` est un Deck2 et non
        # une liste, et l'iterer levait une TypeError qui faisait echouer TOUTE
        # la lecture d'etat. Les PV restaient a 100 %, le bot ne se repliait
        # jamais et se faisait tuer sans jamais changer de forme.
        try:
            joueur = w.players[0]
            ctx["joueur"] = joueur
        except Exception:
            return ctx
        try:
            ctx["forme_heros"] = bool(joueur.IsInHeroForm())
        except Exception:
            pass
        try:
            ctx["taille_main"] = nombre(getattr(joueur, "hand_size", 0))
        except Exception:
            ctx["taille_main"] = 0
        # ⚠ CE QUE L'EMPREINTE DE PROGRES IGNORAIT.
        # Une action peut REUSSIR sans toucher ni les PV, ni la menace, ni la
        # main, ni le round : « un personnage ami gagne le trait AERIAL jusqu'a
        # la fin du round » (Skies Above New York) ne bouge rien de tout cela.
        # Le detecteur de boucle concluait alors a un blocage sur une action qui
        # avait marche — trois parties sur trois du scenario Underling.
        # On photographie donc aussi les TRAITS des personnages amis et la
        # taille de la defausse, qui bouge des qu'une carte est jouee ou
        # depensee. Chaque lecture a son propre garde, comme partout ici.
        try:
            amis = list(ctx["allies"])
            try:
                amis.append(joueur.GetIdentity())
            except Exception:
                pass
            traits = []
            for face in amis:
                if face is None:
                    continue
                paper = getattr(face, "paper", None)
                traits.append((str(getattr(paper, "card_id", face)),
                               tuple(sorted(str(t) for t in (getattr(face, "traits", None) or [])))))
            ctx["traits_amis"] = tuple(sorted(traits))
        except Exception:
            ctx["traits_amis"] = ()
        try:
            ctx["taille_defausse"] = len(joueur.discard_pile.Get())
        except Exception:
            ctx["taille_defausse"] = 0
        try:
            # Reperer l'identite par sa lignee et non par le nom exact de sa
            # classe : la face heros n'est pas forcement de classe « Hero »
            # selon les identites, et un test sur le nom rendait l'identite
            # introuvable en forme heros. Les PV restaient alors bloques a
            # 100 %, le bot ne se repliait jamais et mourait sur place.
            identite = None
            for face in ctx["faces"].values():
                if not (hasattr(face, "IsInPlay") and face.IsInPlay()):
                    continue
                if any(c.__name__ == "Identity" for c in type(face).__mro__):
                    identite = face
                    break
            ctx["identite_face"] = identite
            if identite is not None:
                maxi = nombre(getattr(identite, "max_health", 0), 1) or 1
                ctx["pv_ratio"] = nombre(getattr(identite, "health", 0)) / maxi
                ctx["pv_heros"] = nombre(getattr(identite, "health", 0))
                ctx["identite"] = (f"{type(identite).__name__}"
                                   f"{'/epuise' if getattr(identite, 'IsExhaust', lambda: False)() else ''}"
                                   f"{'/sonne' if getattr(identite, 'IsStunned', lambda: False)() else ''}"
                                   f"{'/confus' if getattr(identite, 'IsConfused', lambda: False)() else ''}"
                                   f":"
                                   f"{getattr(identite.paper, 'card_id', '?')}:"
                                   f"{getattr(identite, 'health', '?')}/"
                                   f"{getattr(identite, 'max_health', '?')}")
            else:
                ctx["identite"] = "INTROUVABLE"
        except Exception as exc:
            ctx["identite"] = f"ERREUR {type(exc).__name__}: {exc}"

        # Menace : rapport entre la menace posee et la cible de la manigance
        # principale. C'est le minuteur de la partie, c'est lui qui fait
        # perdre. `threat` et `target_threat` sont des attributs directs de la
        # face, pas des compteurs : GetCounters('threat') rend toujours 0.
        for scheme in ctx["schemes"]:
            try:
                pose = nombre(getattr(scheme, "threat", 0))
                cible = nombre(getattr(scheme, "target_threat", 0), 0)
                if cible:
                    ctx["menace_ratio"] = max(ctx["menace_ratio"], pose / cible)
                    ctx["menace_restante"] = min(
                        ctx.get("menace_restante", 10**6), cible - pose)
                ctx["escalade"] = max(ctx.get("escalade", 0),
                                      nombre(getattr(scheme, "escalation_threat", 0)))
            except Exception:
                pass

        # Menace attendue au prochain tour de vilain. Elle depend de la FORME :
        # en heros, les ennemis attaquent ; en alter-ego, ils manigancent tous.
        # Se replier avec deux sbires sur la table peut donc boucler la
        # manigance d'un seul coup, ce qui a coute des parties entieres.
        def sch(face):
            return nombre((getattr(getattr(face, "paper", None), "desc", {})
                           or {}).get("SCH"), 0)

        def icone(face, nom_icone):
            return nombre((getattr(getattr(face, "paper", None), "desc", {})
                           or {}).get(nom_icone), 0)

        # Une manigance secondaire a icone Crise INTERDIT de retirer de la
        # menace du plan principal : desamorcer devient un coup dans le vide
        # tant qu'elle est en jeu. Les icones Acceleration, Danger et Amplifier
        # renchérissent chaque round ou on les laisse.
        ctx["crise"] = any(icone(sc, "Crisis") for sc in ctx["schemes_secondaires"])

        # Capacite de frappe du plateau : le heros plus les allies en jeu.
        def stat(face, cle, defaut=0):
            return nombre((getattr(getattr(face, "paper", None), "desc", {})
                           or {}).get(cle), defaut)

        frappe = 0
        if ctx.get("identite_face") is not None:
            frappe += stat(ctx["identite_face"], "ATK", 0)
        frappe += sum(stat(a, "ATK", 0) for a in ctx["allies"])
        ctx["frappe_par_tour"] = max(frappe, 1)

        sch_ennemis = sum(sch(e) for e in ctx["vilains"] + ctx["sbires"])
        # L'acceleration s'ajoute a la menace posee chaque round, quelle que
        # soit la forme du heros.
        ctx["escalade"] = ctx.get("escalade", 0) + sum(
            icone(sc, "Acceleration") for sc in ctx["schemes_secondaires"])
        ctx["menace_si_heros"] = ctx.get("escalade", 0)
        ctx["menace_si_alterego"] = ctx.get("escalade", 0) + sch_ennemis
        return ctx

    def infos_carte(ctx, bind_id):
        face = ctx["faces"].get(str(bind_id))
        if face is None:
            return {}
        papier = getattr(face, "paper", None)
        desc = dict(getattr(papier, "desc", {}) or {})
        type_carte = type(face).__name__
        return {
            "face": face,
            "card_id": getattr(papier, "card_id", None),
            "nom": getattr(papier, "name", "") or "",
            "type": type_carte,
            "cout": nombre(desc.get("Cost"), 0),
            "classe": desc.get("Class", ""),
            "tags": tags_carte(getattr(papier, "text", ""), desc, type_carte),
        }

    # ------------------------------------------------------- la politique --
    def scorer(option, ctx):
        """Note une action par ce qu'elle CHANGE au plateau.

        L'ancienne version notait des noms d'actions (« Play vaut 91, Attack
        vaut 90 »). Elle ne pouvait donc pas arbitrer « cette carte defensive
        vaut plus que cette attaque parce qu'elle me garde en vie deux rounds
        de plus ». La mesure qui a impose cette refonte : en attaquant sans
        jamais se defendre le bot infligeait 2,9 degats par round, assez pour
        les 29 necessaires, mais mourait en 3,9 rounds ; en se defendant il
        tenait 10 rounds mais tombait a 1,7 degat par round. Le produit restait
        constant parce qu'attaquer et se defendre puisent dans la MEME
        activation. D'ou la penalite explicite `cout_activation`, qui rend
        visible ce que coute vraiment chaque choix.
        """
        nom = str(option.get("name") or "")
        carte = infos_carte(ctx, option.get("bind_id"))
        type_carte = carte.get("type", "")
        cout = carte.get("cout", 0)
        tags = carte.get("tags") or set()
        acteur = carte.get("face")
        pv = ctx["pv_ratio"]

        # ⚠ LA STAT VIVANTE D'ABORD, L'IMPRIMEE EN SECOURS (11/09/2026).
        #
        # On ne lisait que `paper.desc`, c'est-a-dire la valeur IMPRIMEE sur le
        # papier. Or beaucoup de cartes recoivent leurs statistiques A
        # L'EXECUTION, et leur gabarit imprime porte des zeros : le pilote les
        # voyait alors comme sans valeur et refusait de s'en servir.
        #
        # Mesure qui l'a revele, sur `iron_patriot` : les allies REGISTERED
        # (gabarit `registered_ally`, `ATK: '0*'`, `THW: '0*'`, valeurs
        # reellement posees par `Faces.TreatAsAlly`) faisaient noter Attaque et
        # Contre a MOINS CINQ. Le bot recrutait des allies puis ne s'en servait
        # jamais, et le complot principal s'accomplissait au round 1 sur 16
        # parties sur 16.
        #
        # ⚠ CE N'EST PAS UN DEFAUT PROPRE A IRON PATRIOT. Tout ce qui pose ses
        # valeurs en jeu est concerne : `TreatAsAlly`, `TreatAsMinion`, les
        # bonus continus, les ameliorations qui donnent +1 ATQ. Le pilote
        # jugeait sur le papier, jamais sur la table.
        ATTRIBUT_VIVANT = {"ATK": "attack", "THW": "thwart", "DEF": "defense",
                           "REC": "recover", "HP": "health"}

        def stat_acteur(cle, defaut=1):
            if acteur is None:
                return defaut
            vivant = ATTRIBUT_VIVANT.get(cle)
            if vivant is not None:
                valeur = getattr(acteur, vivant, None)
                if isinstance(valeur, int):
                    return valeur
            return nombre((getattr(getattr(acteur, "paper", None), "desc", {})
                           or {}).get(cle), defaut)

        # --- les deux horloges, qui donnent l'urgence de chaque axe ---------
        marge = ctx.get("menace_restante", 99)
        par_tour = max(ctx.get("menace_si_heros", 1), 1)
        pv_vilain = min((nombre(getattr(v, "health", 99))
                         for v in ctx["vilains"]), default=99)
        tours_defaite = marge / par_tour
        tours_victoire = pv_vilain / max(ctx.get("frappe_par_tour", 2), 1)

        # L'urgence croit quand l'echeance approche. Une rampe lineaire
        # (2 - tours/4) a ete essayee et retiree : elle faisait tomber le bot
        # de 6,3 a 4 rounds, en le faisant reagir a une menace lointaine au
        # detriment de tout le reste. La courbe hyperbolique ne se declenche
        # que quand l'echeance devient reelle.
        # ⚠ ESSAI 11/09/2026 : un PLANCHER. La courbe rend EXACTEMENT ZERO des
        # que l'echeance depasse 6 tours (3/6 - 0,5 = 0). Contrer ne vaut donc
        # rien tant que la defaite est lointaine, et le cout d'activation rend
        # le score NEGATIF : mesure -5,0 sur iron_patriot. N'importe quelle
        # capacite a score fixe l'emporte alors.
        def urgence(tours):
            return max(0.3, min(2.5, 3.0 / max(tours, 0.5) - 0.5))

        urgence_menace = urgence(tours_defaite)
        degats_entrants = max(sum(nombre((getattr(getattr(e, "paper", None),
                                                  "desc", {}) or {}).get("ATK"), 0)
                                  for e in ctx["vilains"] + ctx["sbires"]), 1)
        # Horloge de la survie, symetrique de celle de la menace : combien de
        # tours de vilain le heros encaisse avant de tomber. Un ratio de PV ne
        # dit rien tout seul, puisqu'il ignore ce qui arrive en face.
        tours_mort = ctx.get("pv_heros", 10) / degats_entrants
        urgence_survie = urgence(tours_mort)

        g_menace = g_survie = g_controle = g_moteur = g_progression = 0.0
        cout_activation = 0.0
        fixe = None

        if nom == "Thwart":
            g_menace = stat_acteur("THW", 1)
            cout_activation = 1.0

        elif nom == "Attack":
            g_progression = stat_acteur("ATK", 1)
            cout_activation = 1.0

        elif nom == "Defense":
            if type_carte == "Ally":
                # L'allie encaisse toute l'attaque et ne coute PAS l'activation
                # du heros. C'est la seule protection qui ne se paie pas sur la
                # meme ressource que l'offensive.
                g_survie = degats_entrants
                g_controle = -1.0
            else:
                g_survie = min(stat_acteur("DEF", 1), degats_entrants)
                cout_activation = 1.0

        elif nom == "Recover":
            g_survie = stat_acteur("REC", 2)
            cout_activation = 1.0

        elif nom == "Play":
            # Une carte ne consomme jamais l'activation : c'est ce qui permet
            # de traiter la menace ET de frapper dans le meme round.
            if "DESAMORCE" in tags:
                g_menace = 2.0
            if "DEGATS" in tags:
                g_progression = 3.0 if type_carte == "Event" else 1.0
            if "DEFENSE" in tags:
                g_survie = degats_entrants * 0.8
            if "SOIN" in tags:
                g_survie = 2.0
            if tags & {"ECONOMIE", "PIOCHE"}:
                # Le moteur rapporte proportionnellement aux rounds restants :
                # pose au round 2 il sert dix fois, pose au round 9 jamais.
                g_moteur = max(0.0, 3.0 - 0.3 * ctx["round"])
            if type_carte == "Ally":
                # Valeur d'un allie sur sa duree de vie : ses activations plus
                # le blocage qu'il offrira.
                g_controle = 2.0
                g_survie += degats_entrants * 0.5
                g_progression += 1.0
            if type_carte in ("Upgrade", "Support") and not (
                    tags & {"ECONOMIE", "PIOCHE"}):
                g_moteur += 1.0
            g_moteur -= 0.4 * cout

        elif nom in ("Change_Form", "Change Form") or nom.startswith("Change_To_"):
            if ctx["forme_heros"]:
                # Se replier fait maniganer le vilain ET tous les sbires.
                cout_menace = ctx.get("menace_si_alterego", 3)
                if pv <= 0.25 or (pv < reglages["seuil_repli"]
                                  and marge > cout_menace + 1):
                    g_survie = stat_acteur("REC", 3) + 1
                    g_menace = -cout_menace
                else:
                    fixe = 0.0
                if pv_vilain <= reglages["portee_de_finition"] \
                        and tours_defaite > 1:
                    fixe = 0.0
            else:
                if pv >= reglages["seuil_retour"] or urgence_menace >= 1.0:
                    g_progression = ctx.get("frappe_par_tour", 2)
                    g_survie = -1.0
                else:
                    fixe = 0.0

        elif nom in ("End Phase", "End_Phase"):
            fixe = 0.5

        elif nom in ("Resolve Mulligans",):
            fixe = 1000.0

        elif nom.lower().startswith("exhaust") \
                and acteur is ctx.get("identite_face"):
            # Epuiser l'identite coute une activation entiere pour un gain le
            # plus souvent mineur.
            g_controle = 1.0
            cout_activation = 1.0

        else:
            # Reponses, interruptions et capacites nommees. Une capacite
            # proposee et non forcee est presque toujours un gain.
            #
            # ⚠ MAIS ELLE S'USE DANS LE ROUND (essai 11/09/2026). Le score
            # etait FIXE : une Action repetable sans limite gardait
            # eternellement le meme attrait. Mesure sur `iron_patriot` :
            # l'Action « Enlistment » de `ip002a` prise 21 fois dans le round 1,
            # 33 sbires REGISTERED en jeu, et 16 parties sur 16 perdues au
            # round 1,0.
            #
            # ⚠ CETTE DECROISSANCE NE SERT A RIEN SANS LE PLANCHER D'URGENCE
            # pose plus haut : tant que Contre valait -5, faire tomber
            # Enlistment de 20 a 0,5 ne changeait rien, il gagnait quand meme.
            # Les deux ont ete essayes SEPAREMENT avant d'etre gardes ensemble.
            #
            # TACHE 11 (15/09/2026) : c'est ICI, sans aucun cas special, que
            # tombe `Reveal_Main_Scheme` (World.CONFIRM_MAIN_SCHEME_OPTION),
            # la question posee au premier joueur avant de retourner la face A
            # de la manigance principale quand la regle confirm_main_scheme
            # est active -- son nom ne correspond a aucune branche ci-dessus.
            # Elle est TOUJOURS seule sur la table (un seul ForChoiceAbility
            # passe a ChooseAbilities dans World.ConfirmMainSchemeReveal),
            # donc n'importe quel score positif suffit a la faire choisir des
            # le premier ask. Mesure : partie rejouee avec la regle active
            # (game_dir=.game-src-par7, hors port 2345), journal du round 0 ->
            # `"actes": {"Reveal_Main_Scheme": 1, "Resolve Mulligans": 1}`,
            # partie qui continue ensuite normalement jusqu'au round 5 sans
            # jamais rendre "bloquee". Aucun code a changer.
            deja_prise = (ctx.get("actes_du_round") or {}).get(nom, 0)
            fixe = 20.0 / (1.0 + deja_prise)

        if fixe is not None:
            return fixe

        poids = reglages
        return (poids["poids_menace"] * urgence_menace * g_menace
                + poids["poids_survie"] * urgence_survie * g_survie
                + poids["poids_controle"] * g_controle
                + poids["poids_moteur"] * g_moteur
                + poids["poids_progression"] * g_progression
                - poids["poids_activation"] * cout_activation)

    def choisir_cibles(option, ctx):
        """Designe les cibles selon leur nature, pas selon l'ordre du moteur."""
        legales = [str(x) for x in (option.get("all_legal_targets") or [])]
        mini, maxi = (option.get("target_num_range") or [0, 0])[:2]
        if not legales or not isinstance(mini, int):
            return []
        nom = str(option.get("name") or "")

        if nom == "Resolve Mulligans":
            # Rejeter ce qu'on ne pourra pas payer tot : les cartes cheres.
            chers = [t for t in legales if infos_carte(ctx, t).get("cout", 0) >= 4]
            plafond = maxi if isinstance(maxi, int) else len(chers)
            return chers[:plafond]

        def note_cible(oid):
            carte = infos_carte(ctx, oid)
            type_cible = carte.get("type", "")
            face = carte.get("face")
            pv = nombre(getattr(face, "health", 0)) if face is not None else 0
            if nom == "Attack":
                if type_cible == "Minion":
                    # Un sbire se juge sur ce qu'il produira au prochain tour,
                    # pas sur ses PV : un sbire a 1 PV et 4 ATK est un gros
                    # probleme. On ajoute son ATK et son SCH.
                    dangerosite = nombre((getattr(getattr(face, "paper", None),
                                                  "desc", {}) or {}).get("ATK"), 0) \
                        + nombre((getattr(getattr(face, "paper", None),
                                          "desc", {}) or {}).get("SCH"), 0)
                    achevable = pv <= reglages["sbire_achevable"]
                    return 100 + 15 * dangerosite + (60 if achevable else 0)
                if type_cible in ("Villain", "EncounterVillain"):
                    # Le vilain vient en dernier dans l'ordre du cadre, SAUF
                    # quand il est a portee de tomber : la premiere question
                    # reste « peut-on gagner ce tour-ci ». Sans cette bascule,
                    # un sbire quelconque passait toujours devant et le bot
                    # laissait le vilain a 1 PV pendant des rounds.
                    if pv <= reglages["portee_de_finition"]:
                        return 400
                    return 140
                return 50
            if nom == "Thwart":
                if type_cible == "MainScheme":
                    # Sous Crise, retirer de la menace du plan principal ne
                    # fait rien : tout passe apres la manigance qui l'impose.
                    return 60 if ctx.get("crise") else 200
                crise = nombre((getattr(getattr(face, "paper", None), "desc", {})
                                or {}).get("Crisis"), 0)
                autres = sum(nombre((getattr(getattr(face, "paper", None),
                                             "desc", {}) or {}).get(k), 0)
                             for k in ("Acceleration", "Hazard", "Amplify"))
                if crise:
                    return 400
                if autres:
                    return 300
                return 150
            return 100

        ordonnees = sorted(legales, key=note_cible, reverse=True)
        besoin = max(mini, 1) if mini else mini
        if besoin == 0:
            return []
        # Une plage [1, 3] ne veut pas dire « 1 suffit » : Power Drain (02041)
        # exige AUTANT de cartes que d'icones de boost defaussees, un nombre que
        # la question n'annonce pas. Le minimum echouait donc en silence, et la
        # meme question revenait indefiniment. `cibles_bonus`, monte d'un cran a
        # chaque repetition sans progres, remonte la plage jusqu'a ce que ca
        # passe.
        besoin = min(max(maxi, besoin), besoin + etat.get("cibles_bonus", 0))
        return ordonnees[:besoin]

    def payer(option, cibles, ctx):
        """Couvre le cout en depensant d'abord les cartes les plus cheres.

        `target_payment` donne, PAR CIBLE, le cout a couvrir et les cartes
        capables de le financer. Sans ce champ renseigne, le moteur considere
        le cout impaye et la carte n'est JAMAIS jouee : le simulateur croirait
        jouer des cartes sans qu'aucune ne parte.
        """
        paiements = option.get("target_payment") or {}
        if not paiements:
            return []
        cle = cibles[0] if cibles and cibles[0] in paiements else next(iter(paiements))
        infos = paiements.get(cle) or {}
        cout = str(infos.get("cost", "0"))
        besoin = int(cout) if cout.isdigit() else len(cout)
        if besoin <= 0:
            return []
        interdits = {str(option.get("bind_id"))}
        candidates = []
        for entree in infos.get("payment") or []:
            for objet_id in entree:
                if str(objet_id) not in interdits:
                    candidates.append(str(objet_id))
                break
        # Depenser d'abord ce qu'on aura le plus de mal a jouer.
        candidates.sort(key=lambda oid: infos_carte(ctx, oid).get("cout", 0),
                        reverse=True)
        choisies = candidates[:besoin]
        return choisies if len(choisies) >= besoin else []

    def executable(option, ctx):
        """Cette option peut-elle REELLEMENT se jouer, ou est-elle une coquille
        vide qui ne changera rien au plateau ?

        Vu sur Spider-Man (deck officiel) : une option peut apparaitre avec un
        vrai id, une vraie cible legale et AUCUN `failure_reason` -- donc
        "offerte" au sens strict -- tout en couttant une ressource dont
        `target_payment.payment` ne liste AUCUNE candidate (main sans la bonne
        couleur a cet instant). `payer()` rend alors `[]` non pas parce que le
        cout est nul, mais parce qu'il est IMPAYABLE ; envoyer ce paiement vide
        quand meme ne fait rien avancer -- l'action ne se joue pas, le plateau
        ne bouge pas, et la MEME question revient a l'identique. Ce n'est pas
        un choix illegal au sens du moteur (pas d'AssertionError), donc
        indiscernable d'un blocage reel sans ce filtre : d'ou l'exclure EN
        AMONT du choix plutot que de compter sur le detecteur de boucle pour
        le repecher apres coup.
        """
        mini = (option.get("target_num_range") or [0, 0])[0]
        if mini and not option.get("all_legal_targets"):
            return False
        paiements = option.get("target_payment") or {}
        if not paiements:
            return True
        cibles = choisir_cibles(option, ctx)
        cle = cibles[0] if cibles and cibles[0] in paiements else next(iter(paiements), None)
        if cle is None:
            return True
        infos = paiements.get(cle) or {}
        cout = str(infos.get("cost", "0"))
        besoin = int(cout) if cout.isdigit() else len(cout)
        if besoin <= 0:
            return True
        interdits = {str(option.get("bind_id"))}
        candidates = [str(oid) for entree in (infos.get("payment") or [])
                      for oid in list(entree)[:1] if str(oid) not in interdits]
        return len(candidates) >= besoin

    def compteurs_du_joueur(ctx):
        """Compteurs portes par l'identite et les allies du joueur.

        CORRECTIF (03/09/2026, pack iron_man_model_42). Les deux empreintes du
        pilote — celle du garde-fou anti-repetition (`empreinte`) et celle du
        desistement (`progres`) — ignoraient les compteurs. Depenser un
        compteur pour PREVENIR des degats ne bougeait donc AUCUN de leurs
        termes : les PV ne baissent pas, justement parce que la prevention a
        marche, et la capacite passait pour n'avoir rien fait.

        Constate sur `im007` Energy Shield (« remove 1 reactor counter ->
        prevent up to 2 of that damage »). Le journal montre le compteur retire
        ET les degats prevenus : la partie AVAIT progresse.

        ⚠ Le helper est PARTAGE a dessein. Les deux corrections du 03/09 ont la
        meme cause : deux signatures du meme fichier qui ne regardaient pas le
        meme monde, et qui divergent des qu'on n'en corrige qu'une. La
        premiere passe n'avait ajoute les compteurs qu'a `progres`, et le
        blocage s'est simplement deplace sur l'autre garde-fou.

        ⚠ CORRECTIF DU 03/09/2026 (soir), pack armored_spidey : on balaie
        TOUTES les faces du plateau, pas seulement l'identite et les allies.
        La premiere ecriture ne lisait que ces deux-la, et le compteur `metal`
        d'Armored Spidey vit sur une AMELIORATION (Spider Armor) : le meme
        blocage serait revenu tel quel. Anticipe a la lecture des scans, avant
        le premier autoplay du pack.
        """
        return tuple(sorted(nombre(getattr(f, "GetAllCounters", lambda: 0)())
                            for f in ctx["faces"].values()))

    def empreinte(ctx, options):
        """Signature d'une situation, pour reperer qu'on tourne en rond.

        CORRECTIF (03/09/2026, pack lady_sif) : la menace des manigances
        ANNEXES entre desormais dans la signature. `menace_ratio` ne lit que la
        manigance PRINCIPALE ; une capacite qui retire de la menace d'une
        annexe ne bougeait donc AUCUN des cinq termes, et deux declenchements
        successifs partageaient la meme cle. Le compteur `MAX_REPETITIONS`
        s'epuisait alors sur une capacite qui, elle, faisait bel et bien
        avancer la partie.

        Constate sur `ls001a` Valiant Warrior (« After Lady Sif uses a basic
        power, remove 1 threat from a scheme »), une Response SANS limite qui
        part deux a quatre fois par round : **3 parties bloquees sur 32**, la
        question fautive etant toujours la meme et toujours forcee
        (`plage=[1, 1]`, donc « 0 » illegal).

        L'empreinte de PROGRES de `desistement` (plus bas dans ce fichier)
        comptait deja les annexes : les deux signatures du meme fichier ne
        regardaient pas le meme monde. On aligne la plus grossiere sur la
        plus fine.

        Correctif strictement ADDITIF : un terme de plus ne peut que SEPARER
        des situations jusque-la confondues, jamais en confondre de nouvelles.
        Il ne peut donc pas creer de blocage la ou il n'y en avait pas.

        CORRECTIF (07/09/2026, pack ares) : les PV du vilain et des sbires
        entrent aussi dans la signature. `pv_ratio` est celui du HEROS ; une
        suite d'attaques identiques d'un meme evenement (Spray and Pray,
        `ar002` : « make the following attack 5 times », cinq fois « Deal 1
        damage to an enemy » avec les memes cibles legales) ne bougeait donc
        AUCUN terme, et `MAX_REPETITIONS` (2) tombait au TROISIEME tir alors
        que Rhino perdait bel et bien 1 PV a chaque fois : **7 parties
        bloquees sur 8**, question fautive toujours forcee (`plage=[1, 1]`).
        Burst Fire (`ag003`) et It's Clobberin' Time! (`th010`) passaient
        seulement parce que leurs DEUX attaques tiennent dans le budget.

        Meme remede que ci-dessus : `progres` comptait deja ces PV, on aligne
        `empreinte` dessus. Toujours additif.
        """
        return (ctx["round"], ctx.get("taille_main", 0),
                round(ctx["pv_ratio"], 2), round(ctx["menace_ratio"], 2),
                tuple(sorted(nombre(getattr(sc, "threat", 0))
                             for sc in ctx.get("schemes_secondaires") or [])),
                tuple(sorted(nombre(getattr(v, "health", 0))
                             for v in ctx.get("vilains") or [])),
                tuple(sorted(nombre(getattr(s, "health", 0))
                             for s in ctx.get("sbires") or [])),
                compteurs_du_joueur(ctx),
                tuple(sorted(str(o.get("id")) for o in options)))

    def clef_option(o):
        """Identite d'une option pour le compteur anti-repetition `deja`.

        L'"id" JSON d'une option est LOCAL a l'abilite qui la propose, pas
        globalement unique : une capacite en plusieurs etapes (activer,
        choisir une carte, choisir une cible) recommence souvent a 1 pour
        chacune de ses etapes. Vu sur Super Spy (ag001b) : activer la
        capacite (id=1, aucune cible), choisir la carte en defausse (id=1,
        7 cibles) et choisir la manigance a soulager (id=1, 2 cibles)
        partagent le meme id ET la meme empreinte de plateau (rien n'est
        encore joue entre ces 3 etapes) -- cle sur le seul id, ces 3
        questions DIFFERENTES epuisaient le meme compteur, forçant un "0"
        illegal sur la 3e (forcee) avant meme qu'elle soit vraiment
        redemandee. D'ou une cle qui inclut aussi la FORME de la question
        (plage de cibles et cibles legales), qui distingue ces etapes tout
        en laissant une VRAIE repetition (Burst Fire pose deux fois
        d'affilee « Deal 2 damage... » avec exactement les memes cibles)
        continuer a etre comptee normalement.
        """
        return (str(o.get("id")),
                tuple(o.get("target_num_range") or []),
                tuple(sorted(str(t) for t in (o.get("all_legal_targets") or []))))

    def pilote(self, data, player_id, check):
        self_pilote = lambda d, p, c: pilote(self, d, p, c)
        etat["asks"] += 1
        capturer_si_phase_mechant()
        if etat["asks"] > MAX_ASKS:
            rendre("bloquee", f"plafond de {MAX_ASKS} questions atteint")
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []

        brute = data.options_json or ""

        passer = json.dumps({"id": "0", "targets": [], "resources": []})
        libres = [o for o in options
                  if isinstance(o, dict) and not o.get("failure_reason")]
        if not libres:
            etat["derniere_reponse_legale"] = False
            return passer

        try:
            ctx = lire_etat()
        except Exception as exc:
            print("lecture d'etat impossible:", type(exc).__name__, exc, flush=True)
            etat["derniere_reponse_legale"] = False
            return passer

        # Detection de boucle : si la MEME question (JSON brut identique)
        # revient alors que le tour precedent lui avait deja envoye une
        # reponse legale (un choix reellement pris dans les options offertes,
        # pas un "0" de repli) ET que rien n'a bouge sur le plateau entre les
        # deux -- vu sur ag001b/Super Spy avec une carte a 0 icone de bonus,
        # cf. .superpowers/sdd/2026-08-07-agent-13/enquete-boucle.md. Sans ce
        # garde-fou le pilote tourne en silence jusqu'au minuteur, ce qui a
        # fait passer 10 parties bloquees pour de simples lenteurs.
        #
        # Le JSON identique SEUL ne suffit pas : Burst Fire (ag003) pose deux
        # fois d'affilee « Deal 2 damage to an enemy. This attack gains
        # ranged. » avec les MEMES cibles legales pour ses deux attaques
        # successives -- une repetition legitime, pas un blocage. Ce qui
        # distingue les deux, c'est que Burst Fire fait vraiment avancer la
        # partie entre les deux demandes (les PV de la cible baissent) alors
        # que le blocage de Super Spy ne change RIEN au plateau, l'exception
        # etant avalee avant tout effet. D'ou la comparaison en plus d'une
        # empreinte de progres (PV du vilain et des sbires, menace des
        # manigances, main, round) : identique => rien n'a progresse.
        progres = (
            ctx["round"], ctx.get("taille_main", 0),
            round(ctx["pv_ratio"], 3), round(ctx.get("menace_ratio", 0.0), 3),
            tuple(sorted(nombre(getattr(v, "health", 0)) for v in ctx["vilains"])),
            tuple(sorted(nombre(getattr(s, "health", 0)) for s in ctx["sbires"])),
            tuple(sorted(nombre(getattr(sc, "threat", 0))
                         for sc in ctx["schemes"] + ctx["schemes_secondaires"])),
            ctx.get("traits_amis", ()),
            ctx.get("taille_defausse", 0),
            len(ctx["allies"]) + len(ctx["sbires"]) + len(ctx["schemes_secondaires"]),
            compteurs_du_joueur(ctx),
        )
        if brute and brute == etat.get("derniere_question_brute") \
                and progres == etat.get("dernier_progres") \
                and etat.get("derniere_reponse_legale"):
            # LE DESISTEMENT. Avant ce garde-fou, le pilote rendait « bloquee »
            # des la premiere repetition sans progres : il n'avait aucun moyen
            # d'abandonner l'option fautive et de tenter les autres. Or une
            # action de heros qui ECHOUE (cout impayable, effet sans cible
            # utile) est reproposee a l'identique par le moteur, et le pilote la
            # rechoisissait sans fin.
            #
            # Mesure : Tenacity (01093), carte joueur OFFICIELLE — « Spend a
            # [physical] resource and discard this card → ready your hero » — et
            # le Hero Action de Kingpin's Cane (wd100) bloquaient chacun une
            # partie sur quatre. Ce ne sont pas des defauts de carte : le pilote
            # ne savait pas passer a autre chose.
            #
            # On ecarte donc l'option qui vient d'echouer et on laisse la
            # question etre reposee : le tour suivant la choisira autrement. Ce
            # n'est qu'apres avoir epuise TOUTES les options qu'on rend le
            # verdict — un vrai blocage moteur reste donc detecte, il l'est
            # simplement une question plus tard.
            fautive = etat.get("derniere_option")
            plage = list(fautive[1]) if fautive and len(fautive) > 1 else []
            mini_f = plage[0] if plage else 0
            maxi_f = plage[1] if len(plage) > 1 else mini_f

            # a) La question est FORCEE (elle exige au moins une cible) et sa
            #    plage laisse de la marge : on retente avec une cible de plus.
            #    Repondre « 0 » a une question forcee leve une AssertionError
            #    dans `ChoiceOne` (controller.py:274), avalee en silence, et la
            #    question revient a l'identique : le remede serait pire.
            if mini_f > 0 and etat.get("cibles_bonus", 0) < maxi_f - mini_f:
                etat["cibles_bonus"] = etat.get("cibles_bonus", 0) + 1
                etat["derniere_question_brute"] = None
                return self_pilote(data, player_id, check)

            # b) Sinon on ecarte l'option fautive et on laisse la question etre
            #    reposee : le tour suivant la choisira autrement.
            desistees = etat.setdefault("desistees", set())
            recentes = [x for x in etat.get("dernieres_options", [])
                        if x not in desistees]
            if recentes:
                desistees.update(recentes)
                etat["derniere_reponse_legale"] = False
                etat["derniere_question_brute"] = None
                etat["dernier_progres"] = progres
                if mini_f == 0:
                    return passer
                return self_pilote(data, player_id, check)
            # c) Une question FORCEE a plage fixe qui echoue toujours n'a pas
            #    de remede cote pilote : le moteur propose une action qui ne
            #    peut pas se resoudre, et aucune reponse ne la fera passer.
            #    Mesure : Tenacity (01093), carte joueur OFFICIELLE — « Spend a
            #    [physical] resource and discard this card → ready your hero » —
            #    est offerte alors que le heros est deja pret. Le verdict tombe,
            #    et il est juste : le defaut est ailleurs.
            resume = "; ".join(
                f"{o.get('name')}(id={o.get('id')}, "
                f"cibles_legales={o.get('all_legal_targets')}, "
                f"plage={o.get('target_num_range')})"
                for o in options if isinstance(o, dict)
            ) or brute[:500]
            rendre("bloquee",
                   "meme question posee a l'identique et le plateau n'a pas "
                   "bouge malgre une reponse legale au tour precedent -- "
                   f"question fautive : {resume}")
        if progres != etat.get("dernier_progres"):
            # La table a bouge : les desistements de la situation precedente
            # n'ont plus lieu d'etre, une option ecartee peut redevenir jouable.
            etat["desistees"] = set()
            etat["cibles_bonus"] = 0
            etat["dernieres_options"] = []
        etat["derniere_question_brute"] = brute
        etat["dernier_progres"] = progres

        # Les options dont on s'est desiste ne sont plus proposees -- sauf s'il
        # ne resterait rien, auquel cas le detecteur de boucle tranchera.
        sans_desistees = [o for o in libres
                          if clef_option(o) not in etat.get("desistees", set())]
        if sans_desistees:
            libres = sans_desistees

        # Ecarter ce qui a deja ete tente en vain dans la meme situation.
        cle = empreinte(ctx, libres)
        deja = etat["historique"].setdefault(cle, {})
        retenues = [o for o in libres
                    if deja.get(clef_option(o), 0) < MAX_REPETITIONS]
        if not retenues:
            # Le "0"/passer n'est une reponse LEGALE que si au moins une des
            # options ecartees acceptait 0 cible (target_num_range[0] == 0).
            # Sinon l'envoyer est garanti illegal : ChoiceOne (moteur) exige,
            # pour accepter un "0", un unique descripteur dont le minimum est
            # 0 (.game-src/engine/controller/controller.py:274) -- une
            # AssertionError avalee en silence par effect_invoke.py s'ensuit,
            # et la MEME question revient a l'identique indefiniment.
            #
            # Vu sur Super Spy (ag001b) : ses TROIS etapes (activer la
            # capacite, choisir la carte en defausse, choisir la manigance)
            # partagent le meme "id" local (1) et la meme empreinte de
            # plateau (rien n'a encore ete joue entre elles) -- le garde-fou
            # anti-repetition MAX_REPETITIONS, concu pour une option
            # refusee puis reproposee (Enhanced Ivory Horn), les confond
            # avec la MEME option redemandee et epuise son budget avant
            # meme d'atteindre le choix de manigance, forcant ce "0" illegal
            # sur un choix pourtant force. Plutot que d'envoyer une reponse
            # qu'on sait deja illegale, on rend un verdict explicite -- cf.
            # .superpowers/sdd/2026-08-07-agent-13/enquete-boucle.md.
            if any((o.get("target_num_range") or [0, 0])[0] > 0 for o in libres):
                resume = "; ".join(
                    f"{o.get('name')}(id={o.get('id')}, "
                    f"cibles_legales={o.get('all_legal_targets')}, "
                    f"plage={o.get('target_num_range')})"
                    for o in libres
                )
                rendre("bloquee",
                       "toutes les options offertes sont deja epuisees par le "
                       "garde-fou anti-repetition, mais au moins une est "
                       "forcee (minimum de cibles > 0) : y repondre 0 est "
                       "illegal et bloquerait la partie -- question fautive : "
                       f"{resume}")
            etat["derniere_reponse_legale"] = False
            return passer

        # Ne retenir une option sans cible legale ou impayable que si RIEN
        # d'autre n'agit reellement. Choisir une telle option est "legal" au
        # sens du moteur (pas d'AssertionError) mais ne change rien au
        # plateau : l'action ne se joue pas, et la MEME question revient a
        # l'identique -- un blocage indiscernable d'un vrai defaut moteur
        # sans ce filtre. Repere sur Spider-Man (deck officiel, jamais
        # bloque avant l'ajout du detecteur de boucle) : `executable()`.
        executables = [o for o in retenues if executable(o, ctx)]
        if executables:
            retenues = executables
        elif all((o.get("target_num_range") or [0, 0])[0] == 0 for o in retenues):
            # AUCUNE option restante ne peut reellement se jouer (paiement
            # insuffisant pour toutes), mais toutes acceptent 0 cible : decliner
            # est une reponse legale (pas de risque d'AssertionError ChoiceOne,
            # qui ne porte que sur le comptage de cibles). Retenter quand meme
            # la "moins pire" ne ferait que reproduire la meme question --
            # repere sur Spider-Man : Hero_Action a "RRR" de cout avec un seul
            # "R" disponible en main, reoffert a l'identique tant qu'on insiste.
            etat["derniere_reponse_legale"] = False
            return passer
        # Sinon (au moins une option forcee -- cible reelle exigee -- est
        # aussi impayable) : garder le choix du "moins pire" plutot que de
        # decliner, par prudence -- decliner un choix FORCE risquerait la
        # meme AssertionError que le "0" illegal deja documente plus haut.
        # Le detecteur de boucle (comparaison de progres) rendra "bloquee"
        # explicitement si cela ne progresse vraiment pas.

        # Journal par round : ce que le bot fait et ce que la table devient.
        # Sans cette trace, chaque reglage se juge sur le seul verdict final,
        # et on ne sait jamais lequel des deux problemes on a deplace.
        r = ctx["round"]
        ligne = etat.setdefault("journal", {}).setdefault(r, {
            "pv_vilain": min((nombre(getattr(v, "health", 0))
                              for v in ctx["vilains"]), default=None),
            "menace": round(ctx["menace_ratio"], 2), "actes": {},
        })
        ligne["pv_vilain_fin"] = min((nombre(getattr(v, "health", 0))
                                      for v in ctx["vilains"]), default=None)

        # Rythme de degats observe, qui alimente l'horloge de la victoire.
        # Le vilain peut se soigner (Rhino remonte de 10 a 14 PV via son set de
        # rencontre) : on ne compte donc que la progression nette.
        premier = etat.get("pv_vilain_depart")
        if premier is None and ligne["pv_vilain"] is not None:
            etat["pv_vilain_depart"] = premier = ligne["pv_vilain"]
        if premier and r > 0 and ligne["pv_vilain_fin"] is not None:
            etat["degats_par_tour"] = max(
                (premier - ligne["pv_vilain_fin"]) / r, 0.5)

        # Ce que le bot a DEJA fait ce round, lisible par le scorer : c'est lui
        # qui fait decroitre une capacite nommee reprise en boucle.
        ctx["actes_du_round"] = ligne["actes"]

        # ⚠ LES SCORES, ET AVANT LE CHOIX (15/09/2026).
        #
        # La trace ne montrait que `offres r1: ['Change_Form', 'Enlistment',
        # 'Play', 'Attack', 'Thwart']`. On voyait CE QUI etait offert, jamais
        # POURQUOI le pilote prenait l'un plutot que l'autre, et tout reglage du
        # scorer se faisait a l'aveugle. C'est ce qui a coute le plus cher sur
        # `iron_patriot` : il a fallu instrumenter le scorer a la main pour
        # decouvrir que Contre et Attaque valaient MOINS CINQ. Premiere demande
        # de `.planning/todos/2026-09-11-autoplay-aveugle-sur-iron-patriot.md`.
        #
        # ⚠ ET ELLE SE CALCULE ICI, PAS PLUS BAS. Pose apres le choix, elle
        # affichait les scores D'APRES : le compteur du round venait d'etre
        # incremente, et une capacite nommee s'y lisait deja decote. On lisait
        # « Enlistment 6,67 » sur une decision prise a 10,0 — de quoi conclure
        # l'inverse de ce qui s'est passe.
        if trace and etat["asks"] <= trace:
            notes = sorted(((str(o.get("name")), round(scorer(o, ctx), 2))
                            for o in retenues), key=lambda x: -x[1])
            print(f"    scores r{ctx['round']}: {notes}", flush=True)

        # ⚠ UNE CAPACITE NOMMEE NE SE REPREND PAS INDEFINIMENT DANS UN ROUND.
        # Voir `PLAFOND_CAPACITE_NOMMEE` : la decroissance du score ne suffit
        # pas quand les autres options s'effondrent plus vite qu'elle.
        saturees = {nom for nom, pris in ligne["actes"].items()
                    if pris >= PLAFOND_CAPACITE_NOMMEE and est_capacite_nommee(nom)}
        if saturees:
            libres_du_plafond = [o for o in retenues
                                 if str(o.get("name")) not in saturees]
            # Rien d'autre a faire : on rend la liste entiere plutot que de
            # bloquer la partie. Le plafond est une preference, pas une regle.
            if libres_du_plafond:
                retenues = libres_du_plafond

        meilleure = max(retenues, key=lambda o: scorer(o, ctx))
        # Une option notee a zero est jugee nuisible : passer vaut mieux que la
        # jouer faute de mieux. Sans ce garde-fou, le bot basculait en
        # alter-ego en fin de tour simplement parce que c'etait la derniere
        # option encore proposee, et gaspillait le changement de forme.
        if scorer(meilleure, ctx) <= 0:
            etat["derniere_reponse_legale"] = False
            return passer
        deja[clef_option(meilleure)] = deja.get(clef_option(meilleure), 0) + 1

        cibles = choisir_cibles(meilleure, ctx)
        nom_acte = str(meilleure.get("name"))
        if nom_acte == "Play":
            etat["cartes_jouees"] += 1
            nom_acte = "Play:" + (infos_carte(ctx, meilleure.get("bind_id"))
                                  .get("type") or "?")
        ligne["actes"][nom_acte] = ligne["actes"].get(nom_acte, 0) + 1

        if trace and etat["asks"] <= trace:
            print(f"    offres r{ctx['round']}: "
                  f"{[str(o.get('name')) for o in libres]}"
                  f" | ecartees: "
                  f"{[(str(o.get('name')), str(o.get('failure_reason'))[:40]) for o in options if isinstance(o, dict) and o.get('failure_reason')]}",
                  flush=True)
        if trace and etat["asks"] <= trace:
            print(f"ASK {etat['asks']} r{ctx['round']} pv={ctx['pv_ratio']:.2f} "
                  f"menace={ctx['menace_ratio']:.2f} id={ctx.get('identite')} "
                  f"-> {meilleure.get('name')} "
                  f"{infos_carte(ctx, meilleure.get('bind_id')).get('nom', '')}",
                  flush=True)

        etat["derniere_reponse_legale"] = True
        etat["derniere_option"] = clef_option(meilleure)
        # ⚠ LA QUESTION QUI SE REPETE N'EST PAS CELLE QU'IL FAUT ECARTER.
        # Une action de tour se joue en DEUX temps : le menu (« Hero Action »,
        # « Play ») puis le ciblage (« Select 2 cards to swap »). C'est le
        # ciblage qui boucle, mais c'est le MENU qu'il faut abandonner — desister
        # le ciblage ne fait que reproposer la meme action au tour suivant. On
        # garde donc les trois derniers choix, et le desistement les ecarte tous.
        recentes = etat.setdefault("dernieres_options", [])
        recentes.append(clef_option(meilleure))
        del recentes[:-3]
        return json.dumps({"id": str(meilleure.get("id", 0)),
                           "targets": cibles,
                           "resources": payer(meilleure, cibles, ctx)})

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    from engine.file.manager import FileManager

    # Le deck : un nom de deck de depart, ou un chemin vers un fichier exporte.
    if os.path.isfile(deck):
        texte_deck = open(deck).read()
    else:
        chemin = FileManager.FindJsonPath("Hero", deck)
        assert chemin, f"deck introuvable : {deck}"
        with FileManager.OpenFile(chemin, read=True) as fichier:
            texte_deck = fichier.Read()

    # La difficulte vit dans la campagne : on la force avant de monter la scene.
    chemin_vilain = FileManager.FindJsonPath("Campaign", vilain)
    assert chemin_vilain, f"vilain introuvable : {vilain}"
    with FileManager.OpenFile(chemin_vilain, read=True) as fichier:
        campagne = json.loads(fichier.Read())
    # Le champ `expert` de la campagne ne sert QU'A nommer le replay
    # (scene.py ligne 74) : le poser seul ne change strictement rien a la
    # partie. Le mode expert consiste a ajouter le set de rencontre « expert »
    # et a faire demarrer le vilain a son stade II. Sans cela, normal et expert
    # rendaient des resultats rigoureusement identiques.
    campagne["expert"] = (difficulte == "expert")
    if difficulte == "expert":
        sets = list(campagne.get("encounter_sets") or [])
        if "expert" not in sets:
            sets.append("expert")
        campagne["encounter_sets"] = sets
        vilains = list(campagne.get("villain") or [])
        if len(vilains) > 1:
            campagne["villain"] = vilains[1:]

    # AJOUT 13/09/2026 : les SETS MODULAIRES, par la variable
    # `AUTOPLAY_MODULAIRES` (« muse », ou « muse,necroverse »).
    #
    # Un set modulaire n'appartient a aucun scenario : sans ce levier, il
    # n'existe AUCUNE facon de le faire jouer par le pilote, et un pack comme
    # `muse` ne pouvait etre eprouve que carte par carte au harnais des
    # capacites — jamais dans une vraie partie, ou ses cartes se croisent.
    # Le champ `encounter_sets` de la campagne est celui que le moteur lit
    # deja pour le set « expert » juste au-dessus : on y ajoute, sans rien
    # retirer de ce que le scenario apporte.
    modulaires = [m.strip() for m in
                  (os.environ.get("AUTOPLAY_MODULAIRES") or "").split(",")
                  if m.strip()]
    if modulaires:
        sets = list(campagne.get("encounter_sets") or [])
        for nom in modulaires:
            if nom not in sets:
                sets.append(nom)
        campagne["encounter_sets"] = sets

    scene = SceneLoader.NewFromJson(json.dumps(campagne), None, [texte_deck],
                                    graine, [], {})
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")
    try:
        if not jeu.GameSetup():
            rendre("plantage", "GameSetup a echoue")
        jeu.GameLoop()
    except SystemExit:
        raise
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        rendre("plantage", f"{type(exc).__name__}: {exc}")
    rendre("terminee", "la boucle de jeu s'est arretee")


# ----------------------------------------------------------- campagne --
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game_dir")
    ap.add_argument("--deck", default="spider_man")
    ap.add_argument("--vilains", default="rhino")
    ap.add_argument("--difficultes", default="normal")
    ap.add_argument("--profils", default="equilibre")
    ap.add_argument("--parties", type=int, default=1)
    ap.add_argument("--graine-depart", type=int, default=1)
    ap.add_argument("--port", type=int, default=4400)
    ap.add_argument("--paralleles", type=int, default=1)
    ap.add_argument("--minuteur", type=int, default=600)
    ap.add_argument("--rapport", default="/tmp/autoplay.json")
    ap.add_argument("--trace", type=int, default=0)
    ap.add_argument("--modulaires", default="",
                    help="sets modulaires a ajouter au scenario, separes par "
                         "des virgules (ex. : muse)")
    ap.add_argument("--reglages", default="",
                    help="JSON de seuils qui surchargent le profil")
    args = ap.parse_args()

    if os.environ.get("AUTOPLAY_LOT"):
        lot = json.loads(os.environ["AUTOPLAY_LOT"])
        jouer_une_partie(args.game_dir, lot["port"], lot["deck"], lot["vilain"],
                         lot["difficulte"], lot["profil"], lot["graine"],
                         lot["sortie"], args.trace)
        return

    vilains = [v.strip() for v in args.vilains.split(",") if v.strip()]
    difficultes = [d.strip() for d in args.difficultes.split(",") if d.strip()]
    profils = [p.strip() for p in args.profils.split(",") if p.strip()]
    for p in profils:
        assert p in PROFILS, f"profil inconnu : {p} (connus : {list(PROFILS)})"

    travaux = []
    port = args.port
    for vilain in vilains:
        for difficulte in difficultes:
            for profil in profils:
                for i in range(args.parties):
                    graine = args.graine_depart + i
                    etiquette = (f"{os.path.basename(args.deck)}_{vilain}_"
                                 f"{difficulte}_{profil}_{graine}")
                    travaux.append({
                        "deck": args.deck, "vilain": vilain,
                        "difficulte": difficulte, "profil": profil,
                        "graine": graine, "port": port,
                        "sortie": f"/tmp/autoplay_{etiquette}.json",
                    })
                    port += 1

    print(f"{len(travaux)} parties a jouer "
          f"({len(vilains)} vilains x {len(difficultes)} difficultes x "
          f"{len(profils)} profils x {args.parties} graines)", flush=True)

    resultats = []
    en_cours = []
    depart = time.time()

    def recolter(proc, lot):
        if os.path.exists(lot["sortie"]):
            return json.load(open(lot["sortie"]))
        return {**{k: lot[k] for k in ("deck", "vilain", "difficulte",
                                       "profil", "graine")},
                "verdict": "minuteur", "gagne": None, "rounds": 0,
                "message": f"aucun resultat (voir le journal de {lot['sortie']})"}

    for lot in travaux:
        if os.path.exists(lot["sortie"]):
            os.remove(lot["sortie"])
        env = dict(os.environ, AUTOPLAY_LOT=json.dumps(lot))
        if args.reglages:
            env["AUTOPLAY_REGLAGES"] = args.reglages
        if args.modulaires:
            env["AUTOPLAY_MODULAIRES"] = args.modulaires
        proc = subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), args.game_dir,
             "--trace", str(args.trace)],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        en_cours.append((proc, lot, time.time()))

        while len(en_cours) >= max(1, args.paralleles):
            time.sleep(0.2)
            for entree in list(en_cours):
                p, l, t0 = entree
                if p.poll() is not None:
                    en_cours.remove(entree)
                    resultats.append(recolter(p, l))
                elif time.time() - t0 > args.minuteur:
                    p.kill()
                    en_cours.remove(entree)
                    resultats.append(recolter(p, l))
            if len(resultats) and len(resultats) % 25 == 0:
                print(f"  {len(resultats)}/{len(travaux)} parties jouees "
                      f"({round(time.time() - depart)}s)", flush=True)

    while en_cours:
        time.sleep(0.2)
        for entree in list(en_cours):
            p, l, t0 = entree
            if p.poll() is not None or time.time() - t0 > args.minuteur:
                if p.poll() is None:
                    p.kill()
                en_cours.remove(entree)
                resultats.append(recolter(p, l))

    # ------------------------------------------------------- le rapport --
    lignes = {}
    for r in resultats:
        cle = (r["vilain"], r["difficulte"], r["profil"])
        ligne = lignes.setdefault(cle, {"parties": 0, "victoires": 0,
                                        "defaites": 0, "incidents": 0,
                                        "rounds": [], "causes": {}})
        ligne["parties"] += 1
        if r.get("gagne") is True:
            ligne["victoires"] += 1
        elif r.get("gagne") is False:
            ligne["defaites"] += 1
            cause = r.get("raison") or "inconnue"
            ligne["causes"][cause] = ligne["causes"].get(cause, 0) + 1
        else:
            ligne["incidents"] += 1
            cause = r.get("verdict") or "inconnu"
            ligne["causes"][cause] = ligne["causes"].get(cause, 0) + 1
        if r.get("rounds"):
            ligne["rounds"].append(r["rounds"])

    print(f"\nDeck : {args.deck}      {len(resultats)} parties en "
          f"{round(time.time() - depart)}s\n")
    entete = f"{'vilain':<14}{'diff':<9}{'profil':<11}{'parties':>8}{'V':>6}{'D':>6}{'%V':>7}{'rounds':>9}{'!':>4}"
    print(entete)
    print("-" * len(entete))
    for (vilain, diff, profil), l in sorted(lignes.items()):
        joues = l["victoires"] + l["defaites"]
        taux = f"{100 * l['victoires'] / joues:.0f}%" if joues else "-"
        moy = f"{sum(l['rounds']) / len(l['rounds']):.1f}" if l["rounds"] else "-"
        print(f"{vilain:<14}{diff:<9}{profil:<11}{l['parties']:>8}"
              f"{l['victoires']:>6}{l['defaites']:>6}{taux:>7}{moy:>9}"
              f"{l['incidents']:>4}")
    incidents = sum(l["incidents"] for l in lignes.values())
    if incidents:
        print(f"\n! = parties sans verdict (plantage, blocage ou minuteur) : "
              f"{incidents}. Elles ne comptent pas dans le taux de victoire.")

    # Les causes de fin disent OU le deck cede : la manigance qui se remplit et
    # le heros qui tombe ne se corrigent pas avec les memes cartes.
    causes = {}
    for l in lignes.values():
        for cause, n in l["causes"].items():
            causes[cause] = causes.get(cause, 0) + n
    if causes:
        print("\nCauses de fin :")
        for cause, n in sorted(causes.items(), key=lambda x: -x[1]):
            print(f"  {n:>5}  {cause}")

    json.dump({"deck": args.deck,
               "lignes": [{"vilain": k[0], "difficulte": k[1], "profil": k[2],
                           **{c: v for c, v in l.items() if c != "rounds"},
                           "rounds_moyen": (sum(l["rounds"]) / len(l["rounds"])
                                            if l["rounds"] else None)}
                          for k, l in sorted(lignes.items())],
               "parties": resultats},
              open(args.rapport, "w"), indent=1, ensure_ascii=False)
    print(f"\nRapport detaille : {args.rapport}")
    sys.exit(0)


if __name__ == "__main__":
    main()
