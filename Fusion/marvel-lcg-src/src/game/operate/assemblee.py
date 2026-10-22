# Module AUTONOME (stdlib seule) : testable sans demarrer le moteur (tools/test_assemblee.py).
from typing import Any, Dict, Tuple

import json
import os
import re
import sqlite3
import time

################################################################################
# L'ASSEMBLEE (« pod ») de « La Chute du Roi » : plusieurs TABLES (parties du serveur) qui jouent Kingsfall ensemble.
#
# Livret FR p.10 : « Pour jouer La Chute du Roi en mode multijoueur epique, divisez-vous en assemblees de 2 a 4 groupes de joueurs. » Chaque groupe est
# une table ; les tables sont des PROCESSUS differents (un moteur par table, voir site/orchestrateur.py) : l'etat commun de l'assemblee vit donc
# dans un petit fichier SQLite partage (WAL), lu et ecrit par transactions courtes. Rien ne depend de l'orchestrateur.
#
# Decisions de l'utilisateur (22/10/2026, .planning/mcdc-punisher/decisions-multi-tables.md) :
#   1. les groupes se retrouvent par un CODE d'assemblee partage ; la 1re table qui lance Kingsfall epique est l'organisatrice ;
#   2. une table qui ferme ou abandonne compte comme une DEFAITE de son groupe (1 menace par joueur) ;
#   3. Longue vie et Le Roi sont en jeu chez TOUS, en miroir du total commun.
#
# Le monde porte `world.rule.assemblee = (code, table)` (regle `assemblee_<code>_<table>` de la liste `rules`). Sans elle, RIEN n'existe : aucune
# partie ordinaire n'est touchee, et les cartes retombent sur leur comportement d'un seul groupe.
################################################################################

SQL = """
CREATE TABLE IF NOT EXISTS assemblees (
    code TEXT PRIMARY KEY, cree REAL NOT NULL, organisateur TEXT NOT NULL,
    total_jetons INTEGER NOT NULL DEFAULT 0, retournee INTEGER NOT NULL DEFAULT 0,
    degats INTEGER NOT NULL DEFAULT 0, menace INTEGER NOT NULL DEFAULT 0,
    version INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS groupes (
    code TEXT NOT NULL, tab TEXT NOT NULL, joueurs INTEGER NOT NULL, noms TEXT NOT NULL DEFAULT '',
    etat INTEGER NOT NULL DEFAULT 0,          -- 0 en cours, 1 victoire, 2 defaite, 3 abandon
    recus INTEGER NOT NULL DEFAULT 0,         -- jetons envoyes par d'autres groupes, pas encore poses sur Power to the People
    PRIMARY KEY (code, tab));
"""
EN_COURS, VICTOIRE, DEFAITE, ABANDON = 0, 1, 2, 3
GROUPES_MAX = 4


class ErreurAssemblee(Exception):
    """Une demande refusee : code inconnu, assemblee pleine, table deja inscrite."""


def _chemin() -> str:
    return os.environ.get('MCLCG_ASSEMBLEES') or os.path.join(os.getcwd(), 'assemblees.db')


def _connexion() -> sqlite3.Connection:
    base = sqlite3.connect(_chemin(), timeout=10, isolation_level=None)
    base.row_factory = sqlite3.Row
    try:
        base.execute('PRAGMA journal_mode=WAL')
    except sqlite3.DatabaseError:
        pass
    base.executescript(SQL)
    return base


class _Transaction:
    """`with _Transaction() as base:` : une transaction ecrivante, ou un refus propre apres `timeout`."""

    def __enter__(self) -> sqlite3.Connection:
        self.base = _connexion()
        self.base.execute('BEGIN IMMEDIATE')
        return self.base

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.base.execute('ROLLBACK' if exc_type else 'COMMIT')
        finally:
            self.base.close()


def _code_aleatoire() -> str:
    import secrets
    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'      # sans I, O, 0, 1 : on le recopie a la main
    return 'KING-' + ''.join(secrets.choice(alphabet) for _ in range(4))


CODE = re.compile(r'^[A-Z0-9-]{4,16}$')


class Assemblee:

    ############################################################################
    # Inscription
    @staticmethod
    def Creer(table: str, joueurs: int, noms: str = '', code: 'str|None' = None) -> str:
        """La 1re table cree l'assemblee et en est l'organisatrice. Rend le code a donner aux autres."""
        with _Transaction() as base:
            if code is not None:        # code impose (tests) : refuse s'il existe deja
                if base.execute('SELECT 1 FROM assemblees WHERE code=?', (code,)).fetchone() is not None:
                    raise ErreurAssemblee(f'Assemblee deja creee : {code}')
            else:
                for _ in range(20):
                    code = _code_aleatoire()
                    if base.execute('SELECT 1 FROM assemblees WHERE code=?', (code,)).fetchone() is None:
                        break
            base.execute('INSERT INTO assemblees (code, cree, organisateur) VALUES (?,?,?)', (code, time.time(), table))
            base.execute('INSERT INTO groupes (code, tab, joueurs, noms) VALUES (?,?,?,?)', (code, table, joueurs, noms))
        return code

    @staticmethod
    def Rejoindre(code: str, table: str, joueurs: int, noms: str = '') -> None:
        """Une autre table entre dans l'assemblee. Refus : code inconnu, 4 groupes deja, table deja inscrite."""
        code = (code or '').strip().upper()
        with _Transaction() as base:
            if not CODE.match(code) or base.execute('SELECT 1 FROM assemblees WHERE code=?', (code,)).fetchone() is None:
                raise ErreurAssemblee(f"Assemblee inconnue : {code or '(vide)'}")
            if base.execute('SELECT 1 FROM groupes WHERE code=? AND tab=?', (code, table)).fetchone() is not None:
                raise ErreurAssemblee(f'La table {table} est deja dans cette assemblee')
            if base.execute('SELECT COUNT(*) FROM groupes WHERE code=?', (code,)).fetchone()[0] >= GROUPES_MAX:
                raise ErreurAssemblee(f'Assemblee complete : {GROUPES_MAX} groupes au plus')
            base.execute('INSERT INTO groupes (code, tab, joueurs, noms) VALUES (?,?,?,?)', (code, table, joueurs, noms))
            base.execute('UPDATE assemblees SET version = version + 1 WHERE code=?', (code,))

    ############################################################################
    # Lecture
    @staticmethod
    def Etat(code: str) -> 'Dict[str, Any]|None':
        """L'etat complet, pour l'affichage et les cartes miroirs. None si le code est inconnu."""
        with closing_connexion() as base:
            a = base.execute('SELECT * FROM assemblees WHERE code=?', (code,)).fetchone()
            if a is None:
                return None
            g = [dict(r) for r in base.execute('SELECT * FROM groupes WHERE code=? ORDER BY rowid', (code,))]
        joueurs = sum(x['joueurs'] for x in g)
        return {
            'code': code, 'organisateur': a['organisateur'], 'total_jetons': a['total_jetons'], 'retournee': bool(a['retournee']),
            'degats': a['degats'], 'menace': a['menace'], 'version': a['version'], 'groupes': g,
            'joueurs': joueurs,
            # « 2 par joueur + 2 par groupe » (Long Live, 2A)
            'seuil': 2 * joueurs + 2 * len(g),
            'terminee': bool(g) and all(x['etat'] != EN_COURS for x in g),
            'gagnee': bool(g) and all(x['etat'] != EN_COURS for x in g) and a['degats'] >= a['menace'],
        }

    ############################################################################
    # Longue vie : le total commun
    @staticmethod
    def VerserJetons(code: str, n: int) -> 'Dict[str, Any]':
        """« Move each support counter from your Public Support to here » : ajoute `n` au total commun. Passe `retournee` a 1 des que le seuil
        (2 par joueur + 2 par groupe) est atteint, UNE seule fois, pour toute l'assemblee."""
        with _Transaction() as base:
            if n > 0:
                base.execute('UPDATE assemblees SET total_jetons = total_jetons + ?, version = version + 1 WHERE code=?', (n, code))
            a = base.execute('SELECT total_jetons, retournee FROM assemblees WHERE code=?', (code,)).fetchone()
            joueurs, groupes = base.execute('SELECT COALESCE(SUM(joueurs),0), COUNT(*) FROM groupes WHERE code=?', (code,)).fetchone()
            if not a['retournee'] and a['total_jetons'] >= 2 * joueurs + 2 * groupes:
                base.execute('UPDATE assemblees SET retournee = 1, version = version + 1 WHERE code=?', (code,))
        etat = Assemblee.Etat(code)
        assert etat is not None
        return etat

    ############################################################################
    # Action d'assemblee : un jeton vers Power to the People d'un autre groupe
    @staticmethod
    def EnvoyerJeton(code: str, table_cible: str) -> bool:
        with _Transaction() as base:
            cur = base.execute('UPDATE groupes SET recus = recus + 1 WHERE code=? AND tab=? AND etat=0', (code, table_cible))
            if cur.rowcount != 1:
                return False
            base.execute('UPDATE assemblees SET version = version + 1 WHERE code=?', (code,))
            return True

    @staticmethod
    def PrendreLesJetonsRecus(code: str, table: str) -> int:
        """Pose-les sur Power to the People de CETTE table : rend le nombre de jetons arrives depuis le dernier appel, et le remet a zero."""
        with _Transaction() as base:
            ligne = base.execute('SELECT recus FROM groupes WHERE code=? AND tab=?', (code, table)).fetchone()
            n = 0 if ligne is None else ligne['recus']
            if n:
                base.execute('UPDATE groupes SET recus = 0 WHERE code=? AND tab=?', (code, table))
            return n

    ############################################################################
    # Le Roi : degats (victoires) et menace (defaites)
    @staticmethod
    def Terminer(code: str, table: str, victoire: bool, abandon: bool = False) -> 'Dict[str, Any]':
        """Cette table a fini. Victoire : 1 degat par joueur du groupe sur Le Roi ; defaite ou abandon : 1 menace par joueur. IDEMPOTENT : une table
        deja finie ne compte pas deux fois (fermeture apres la fin, double envoi)."""
        with _Transaction() as base:
            g = base.execute('SELECT joueurs, etat FROM groupes WHERE code=? AND tab=?', (code, table)).fetchone()
            if g is not None and g['etat'] == EN_COURS:
                etat = ABANDON if abandon else (VICTOIRE if victoire else DEFAITE)
                base.execute('UPDATE groupes SET etat=? WHERE code=? AND tab=?', (etat, code, table))
                colonne = 'degats' if (victoire and not abandon) else 'menace'
                base.execute(f'UPDATE assemblees SET {colonne} = {colonne} + ?, version = version + 1 WHERE code=?', (g['joueurs'], code))
        etat_final = Assemblee.Etat(code)
        assert etat_final is not None
        return etat_final

    ############################################################################
    # Cote monde : la table courante
    @staticmethod
    def Courante(effect_or_world: 'Effect|World') -> 'Tuple[str, str]|None':
        """(code, table) de la partie en cours, ou None hors assemblee."""
        from game.operate.worlds import Worlds
        return getattr(Worlds.CastWorld(effect_or_world).rule, 'assemblee', None)

    @staticmethod
    def EstOrganisatrice(effect_or_world: 'Effect|World') -> bool:
        courante = Assemblee.Courante(effect_or_world)
        if courante is None:
            return False
        etat = Assemblee.Etat(courante[0])
        return etat is not None and etat['organisateur'] == courante[1]


from contextlib import contextmanager


@contextmanager
def closing_connexion():
    base = _connexion()
    try:
        yield base
    finally:
        base.close()
