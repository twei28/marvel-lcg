# CHAINES du MODE CAMPAGNE de HELLFIRE HUNT (Dipsome) : prefixe « [campagne_hellfire] ».
#
# Jouees par `tools/test_campagne_chaine.py` (qui charge ce fichier en plus de `campagne_mode.py`) :
#
#   RELEASE=1 CAS_PREFIX=hfm python3.10 tools/test_campagne_chaine.py "$PWD/.game-src-hfm" 11000 /tmp/rapport.json "[campagne_hellfire]"
#
# Chaque chaine ENCHAINE les cinq scenarios 1 -> 5 avec le MEME carnet qui voyage : apres chaque partie (forcee en victoire par l'API Puzzle),
# le harnais ne reporte au scenario suivant QUE les cles que le panneau de recompenses ecrit (celles de `data/campagnes/hellfire_hunt.json`),
# exactement comme `preremplissage.ts`. Une cle que le moteur lit mais que le fichier ne declare pas est donc PERDUE a la partie suivante.
#
# Ce que chaque etape verifie, a la mise en place ET au carnet sortant (livret p.8-p.16) :
#   - identite fixe : `Player N Identity` du carnet sortant = le heros choisi, a chaque scenario ;
#   - allies Recruited gagnes (scenarios 1 -> 5) : deck Recruited Mutants = exactement les allies notes, les autres de cote ;
#   - Potential Ally : 1 par joueur melangee aux scenarios 1, 3 et 4 SEULEMENT ; une manigance vaincue ne revient plus ;
#   - cases « Emma Frost's Redemption » / « Cryptic Threatening Message » : la carte revelee selon la case (scenarios 2, 3, 4) ;
#   - Xavier's Institute en jeu aux scenarios 1 a 4 ; au 5 : Rally the Survivors, Tactical Help et Enemy Of Enemy au deck de rencontre ;
#   - expert : PV restants reportes (et plafonnes), jeton d'acceleration « restaurer » (accepte, puis REFUSE), joueur elimine.
CAS = []

CHAINES = []

SCENARIOS = ["hellfire_white_queen", "hellfire_black_king", "hellfire_black_queen", "hellfire_torn", "hellfire_cassandra_nova"]
ALLIES = [f"hf{n:03d}" for n in range(13, 29)]
CAPTIFS = ["hf208", "hf209", "hf210", "hf211"]
POTENTIELS = [f"hf{n:03d}" for n in range(29, 41)]
EMMA = "hf025"
CEREBRO, REDEMPTION, CRYPTIC, MINEFIELD, RALLY, TACTICAL, ENEMY, INSTITUTE = (
    "hf041", "hf042", "hf043", "hf044", "hf045", "hf046", "hf047", "hf048")
CLE_RECRUTES, CLE_PA, CLE_EMMA, CLE_CRYPTIC = (
    "Recruited Allies", "Removed Potential Allies", "Emma Frost's Redemption: Defeated", "Cryptic Threatening Message: Defeated")
HEROS_DECKS = ["sunspot_hellfire", "rachel_summers"]
IDENTITES = [("so001b", "Sunspot", 10), ("rm001b", "Marvel Girl", 10)]


# ---------------------------------------------------------------- aides --
def _faces(monde):
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None)
        if face is not None:
            yield face


def _id(face):
    return getattr(getattr(face, "paper", None), "card_id", None)


def _liste(valeur):
    return [x for x in (valeur or "").split(";") if x]


def _deck_recrutes(monde):
    etat = getattr(monde, "hf_recruited", None)
    return sorted(_id(f) for f in etat[0].Get(True)) if etat else []


def _de_cote(monde):
    return sorted(_id(f) for f in monde.aside_deck.Get(True) if _id(f) in ALLIES)


def _potentiels_rencontre(monde):
    from game.operate.worlds import Worlds
    return sorted(_id(f) for f in Worlds.GetEncounterDeckCards(monde) if _id(f) in POTENTIELS)


def _ids_rencontre(monde):
    from game.operate.worlds import Worlds
    return [_id(f) for f in Worlds.GetEncounterDeckCards(monde)]


def _en_jeu(monde):
    return {_id(f) for f in _faces(monde) if f.IsInPlay()}


def _verif(*controles):
    soucis = [message for ok, message in controles if not ok]
    return (not soucis), (" ; ".join(soucis) if soucis else "ok")


def _jetons_acceleration(monde):
    from game.operate.worlds import Worlds
    return sum(f.GetTokens("acceleration_token") for f in Worlds.GetAllMainSchemes(monde))


# ---------------------------------------------------------- la chaine --
# Degats subis par chaque joueur a chaque scenario (campagne experte) : petits, pour que le cumul des soins REFUSES reste vivable.
DEGATS = {1: (3, 2), 2: (2, 3), 3: (1, 1), 4: (2, 2), 5: (1, 1)}


def construire(nom, joueurs=1, expert=False, emma=True, cryptic=True, refuser_soin=(), elimine=None, depart=None, perdre=()):
    """Une chaine 1 -> 5 (le meme carnet voyage, filtre comme le fait le panneau).

    `emma` : vaincre Emma Frost's Redemption au scenario 2 (sinon elle est revelee de nouveau au 3 et vaincue LA).
    `cryptic` : vaincre Cryptic Threatening Message au scenario 3 (sinon elle est revelee de nouveau au 4).
    `refuser_soin` : scenarios (2..5) ou le pilote REFUSE le soin par jeton d'acceleration (campagne experte).
    `perdre` : scenarios (1..5) d'abord JOUES ET PERDUS : le carnet ne bouge pas, on rejoue le meme scenario sans penalite.
    `elimine` : (scenario, siege) : ce joueur est ELIMINE avant la victoire de ce scenario (campagne experte).
    """
    decks = HEROS_DECKS[:joueurs]
    # M : ce que le carnet DOIT contenir (et que le PANNEAU reporte) ; mis a jour a la fin de chaque etape.
    M = {"deck": set(), "pa": [], "emma": False, "cryptic": False, "pv": {}, "elimine": set()}
    etapes = []

    def deck_de_mise_en_place(k):
        """Le deck Recruited Mutants attendu apres la mise en place du scenario k : les allies notes + Emma Frost aux regles des scenarios 3 et 5."""
        deck = set(M["deck"])
        if k == 3 and M["emma"]:
            deck.add(EMMA)
        if k == 5 and not M["emma"]:
            deck.add(EMMA)
        return sorted(deck)

    def soin_accepte(k):
        return k not in refuser_soin

    def pv_au_depart(k, i):
        """PV attendus d'un joueur juste apres la mise en place du scenario k (campagne experte, k >= 2)."""
        maxi = IDENTITES[i][2]
        reporte = M["pv"].get(i)
        if reporte is None:                       # jamais note (ou joueur elimine) : PV pleins
            return maxi
        return maxi if soin_accepte(k) and reporte < maxi else min(reporte, maxi)

    def a_payer(k, i):
        """Un pion d'acceleration est pose pour soigner ce joueur ? (PV reportes < max et soin accepte ; joueur elimine : il rejoint en payant)."""
        reporte = M["pv"].get(i)
        if i in M["elimine"]:
            return True
        return reporte is not None and reporte < IDENTITES[i][2] and soin_accepte(k)

    def verifier(k):
        def f(monde):
            deck = _deck_recrutes(monde)
            attendu = deck_de_mise_en_place(k)
            pa = _potentiels_rencontre(monde)
            en_jeu = _en_jeu(monde)
            ids = _ids_rencontre(monde)
            devant = {1: ([CEREBRO, INSTITUTE], [REDEMPTION, CRYPTIC, MINEFIELD, RALLY]),
                      2: ([REDEMPTION, INSTITUTE], [CEREBRO, CRYPTIC, MINEFIELD, RALLY]),
                      3: ([CRYPTIC, INSTITUTE], [CEREBRO, REDEMPTION, MINEFIELD, RALLY]) if M["emma"]
                      else ([REDEMPTION, INSTITUTE], [CEREBRO, CRYPTIC, MINEFIELD, RALLY]),
                      4: ([MINEFIELD, INSTITUTE], [CEREBRO, REDEMPTION, CRYPTIC, RALLY]) if M["cryptic"]
                      else ([CRYPTIC, INSTITUTE], [CEREBRO, REDEMPTION, MINEFIELD, RALLY]),
                      5: ([RALLY], [CEREBRO, REDEMPTION, CRYPTIC, MINEFIELD, INSTITUTE])}[k]
            n_pa = joueurs if k in (1, 3, 4) else 0
            controles = [
                (deck == attendu, f"deck Recruited Mutants = {deck} (attendu {attendu})"),
                (_de_cote(monde) == sorted(set(ALLIES) - set(attendu)),
                 f"allies de cote = {_de_cote(monde)} (attendus {sorted(set(ALLIES) - set(attendu))})"),
                (len(pa) == n_pa, f"{len(pa)} Potential Ally dans le deck de rencontre ({pa}), attendu {n_pa}"),
                (not set(pa) & set(M["pa"]), f"une manigance Potential Ally RETIREE est revenue : {sorted(set(pa) & set(M['pa']))}"),
                (all(c in en_jeu for c in devant[0]), f"devraient etre en jeu : {sorted(c for c in devant[0] if c not in en_jeu)}"),
                (not any(c in en_jeu for c in devant[1]), f"ne devraient PAS etre en jeu : {sorted(c for c in devant[1] if c in en_jeu)}"),
                ((TACTICAL in ids and ENEMY in ids) if k == 5 else (TACTICAL not in ids and ENEMY not in ids),
                 f"Tactical Help / Enemy Of Enemy au deck de rencontre : {TACTICAL in ids}/{ENEMY in ids} (scenario {k})"),
            ]
            if expert and k >= 2:
                for i in range(joueurs):
                    pv = monde.players[i].GetIdentity().health
                    controles.append((pv == pv_au_depart(k, i), f"joueur {i + 1} : PV au depart = {pv} (attendu {pv_au_depart(k, i)} ; "
                                      f"reportes {M['pv'].get(i)}, soin {'accepte' if soin_accepte(k) else 'refuse'})"))
                voulus = sum(1 for i in range(joueurs) if a_payer(k, i))
                controles.append((_jetons_acceleration(monde) == voulus,
                                  f"jetons d'acceleration sur la manigance principale = {_jetons_acceleration(monde)} (attendu {voulus})"))
            return _verif(*controles)
        return f

    def gagnes_du_scenario(k):
        """Les allies que la partie k fait entrer en jeu (ou, pour Emma, la manigance vaincue qui la recrute)."""
        gagnes = {1: ["hf013", "hf014", "hf019"], 2: ["hf208", "hf209"], 3: ["hf020"], 4: ["hf021"], 5: []}[k]
        if k == 2 and emma:
            gagnes = gagnes + [EMMA]
        if k == 3 and not M["emma"]:
            gagnes = gagnes + [EMMA]
        if k == 3 and M["emma"] and cryptic:
            gagnes = gagnes + ["hf026"]
        return gagnes

    def avant(k):
        """L'etat de FIN de partie ; la victoire est forcee ensuite par le harnais."""
        def f(monde):
            commandes = [f"Puzzle.PutIntoPlay('{c}', under_control=True)" for c in gagnes_du_scenario(k)]
            if k == 1:
                # Un allie recrute PUIS defait avant la fin est dans une defausse, pas en jeu : il doit quand meme etre note.
                commandes.append("Puzzle.Discard('hf019')")
            if k in (1, 3, 4):
                for card_id in _potentiels_rencontre(monde):
                    commandes.append(f"Puzzle.AddToVictoryDisplay('{card_id}')")
                    M["pa"].append(card_id)
            if (k == 2 and emma) or (k == 3 and not M["emma"]):
                commandes.append(f"Puzzle.AddToVictoryDisplay('{REDEMPTION}')")
            if k == 3 and M["emma"] and cryptic:
                commandes.append(f"Puzzle.AddToVictoryDisplay('{CRYPTIC}')")
            if expert:
                for i in range(joueurs):
                    commandes.append(f"Puzzle.Damage('{IDENTITES[i][0]}', {DEGATS[k][i]})")
                if elimine and elimine[0] == k:
                    commandes.append(f"Puzzle.Damage('{IDENTITES[elimine[1]][0]}', 99)")
            return commandes
        return f

    def carnet_verifier(k):
        def f(suggestions, entrant):
            recrutes = sorted(_liste(suggestions.get(CLE_RECRUTES)))
            voulus = sorted(set(deck_de_mise_en_place(k)) | set(gagnes_du_scenario(k)))
            # etat du carnet APRES ce scenario
            if k == 3 and M["emma"] and cryptic:
                M["cryptic"] = True           # Cryptic n'est revelee (donc vaincue) au 3 que si la case d'Emma etait deja cochee
            if (k == 2 and emma) or (k == 3 and not M["emma"]):
                M["emma"] = True
            M["deck"] = set(voulus)
            controles = [
                (recrutes == voulus, f"{CLE_RECRUTES} = {recrutes} (attendu {voulus})"),
                (sorted(_liste(suggestions.get(CLE_PA))) == sorted(M["pa"]),
                 f"{CLE_PA} = {sorted(_liste(suggestions.get(CLE_PA)))} (attendu {sorted(M['pa'])})"),
                ((suggestions.get(CLE_EMMA) == "1") == M["emma"], f"case Emma = {suggestions.get(CLE_EMMA)!r} (attendu {'1' if M['emma'] else 'absente'})"),
                ((suggestions.get(CLE_CRYPTIC) == "1") == M["cryptic"], f"case Cryptic = {suggestions.get(CLE_CRYPTIC)!r} (attendu {'1' if M['cryptic'] else 'absente'})"),
            ]
            for i in range(joueurs):
                if elimine and elimine[0] == k and elimine[1] == i:
                    continue                  # un joueur elimine ne participe pas a la victoire : le panneau ne reporte rien pour lui
                controles.append((suggestions.get(f"Player {i + 1} Identity") == IDENTITES[i][1],
                                  f"identite du joueur {i + 1} = {suggestions.get(f'Player {i + 1} Identity')!r} (attendu {IDENTITES[i][1]!r})"))
            if expert:
                for i in range(joueurs):
                    cle = f"Player {i + 1} Remaining hit points"
                    if elimine and elimine[0] == k and elimine[1] == i:
                        # Un joueur ELIMINE ne participe pas aux etapes de victoire : le panneau ne reporte pas sa cle, l'ANCIENNE valeur reste au carnet
                        # (fusion sur l'ancien carnet) ; au scenario suivant il revient avec elle et peut etre soigne par un jeton (livret p.7).
                        continue
                    depart = pv_au_depart(k, i) if k >= 2 else IDENTITES[i][2]
                    voulu = depart - DEGATS[k][i]
                    controles.append((suggestions.get(cle) == str(voulu), f"{cle} = {suggestions.get(cle)!r} (attendu {voulu} : {depart} au depart - {DEGATS[k][i]} degats)"))
                    M["pv"][i] = voulu
                    M["elimine"].discard(i)
            return _verif(*controles)
        return f

    for k in range(1, 6):
        scenario = SCENARIOS[k - 1] + ("_expert" if expert else "")
        etape = {
            "nom": f"scenario {k} {SCENARIOS[k - 1]}",
            "scenario": scenario,
            "etape": SCENARIOS[k - 1],
            "verifier": verifier(k),
            "avant": avant(k),
            "carnet_verifier": carnet_verifier(k),
            "carnet_attendu": {"gagnee": True, "scenario": SCENARIOS[k - 1], "cles_presentes": ["Player 1 Identity"]},
        }
        if expert and k in refuser_soin:
            etape["preferer"] = REFUS
        if k in perdre:
            perdue = dict(etape, nom=f"scenario {k} PERDU puis rejoue", fin="Lose", avant=[], carnet_verifier=None,
                          carnet_attendu={"gagnee": False, "scenario": SCENARIOS[k - 1]})
            etapes.append(perdue)
        etapes.append(etape)
    return {"nom": f"[campagne_hellfire] {nom}", "campagne": "hellfire_hunt", "heros": decks, "carnet": depart or {}, "etapes": etapes}


# Fragments d'option que le pilote choisit pour REFUSER le soin (a preciser d'apres les options reellement proposees).
REFUS = ["Cancel"]

CHAINES += [
    construire("STANDARD 1 joueur (Sunspot) : 1 -> 5, allies gagnes, Emma Frost's Redemption vaincue au 2, Cryptic au 3, deck Recruited reconstruit"),
    construire("STANDARD 2 joueurs (Sunspot + Marvel Girl) : 1 -> 5, deux Potential Ally par scenario, deux identites fixes", joueurs=2),
    construire("STANDARD 1 joueur, branche Emma NON vaincue au 2 : Redemption revelee de nouveau au 3 (et vaincue), Cryptic revelee au 4", emma=False),
    construire("STANDARD 1 joueur, branche Cryptic NON vaincue au 3 : Cryptic revelee de nouveau au 4, jamais Psychic Minefield", cryptic=False),
    construire("EXPERT 1 joueur (Sunspot) : 1 -> 5, PV restants reportes, soin par jeton d'acceleration accepte a chaque scenario", expert=True),
    construire("EXPERT 1 joueur : le soin est REFUSE au scenario 3 -> les PV reportes restent (pas de jeton)", expert=True, refuser_soin=(3,)),
    construire("EXPERT 2 joueurs : Marvel Girl est ELIMINEE au scenario 3 mais l'equipe gagne -> au 4 elle rejoint en payant un jeton", joueurs=2, expert=True, elimine=(3, 1)),
    construire("EXPERT 2 joueurs : soins refuses aux scenarios 2 et 4, Marvel Girl eliminee au 3", joueurs=2, expert=True, refuser_soin=(2, 4), elimine=(3, 1)),
    construire("STANDARD 1 joueur : defaites aux scenarios 2 et 4, rejouees sans penalite (le carnet ne bouge pas), puis victoire 1 -> 5", perdre=(2, 4)),
    construire("EXPERT 1 joueur : defaite au scenario 3 rejouee sans penalite (PV reportes intacts)", expert=True, perdre=(3,)),
]
