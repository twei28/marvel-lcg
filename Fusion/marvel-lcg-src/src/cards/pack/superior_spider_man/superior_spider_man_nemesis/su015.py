from . import *

# Goblin Protocol — COMPLOT ANNEXE nemesis. Boost 3. Menace 2 par joueur.
# DEUX icones ACCELERATION.
# Threat on tracked minions counts towards the main scheme's target threat.
# Threat here cannot be removed by Spider-Bots or tracking.
#
# CARTES DE REFERENCE
#  - `04125` Red Skull, `01059` : une regle CONTINUE portee par un complot
#    annexe, active tant qu'il est en jeu.
#  - `su010` Spider-Bot et le helper `Tracer` du set heros : les deux choses que
#    la seconde phrase interdit.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « THREAT ON TRACKED MINIONS COUNTS TOWARDS THE MAIN SCHEME'S TARGET
#    THREAT » : c'est LA carte qui retourne le pack contre son heros. Chaque
#    `track` rapproche le vilain de la victoire au lieu de l'en eloigner. Le
#    moteur n'a aucune notion de « menace ailleurs qui compte » : la carte
#    ajoute donc au complot principal, en continu, le total des pions `threat`
#    poses sur les sbires.
#  ⚠ « THREAT HERE cannot be removed by Spider-Bots OR TRACKING » : « here »
#    designe CE complot annexe, pas le principal. Deux interdictions distinctes,
#    et c'est le helper `Tracer` qui doit les respecter.
#  ⚠ LES DEUX ICONES SONT DES **ACCELERATION**, pas des Alea : verifie par
#    comparaison d'image le 08/09/2026 contre `ag011` (Acceleration, avec la
#    barre de soulignement) et `hd022` (Alea, sans barre). Base automatique lue
#    dans `desc` : aucun script (RECETTES §3).
#  ⚠ La menace de depart « 2 [per_hero] » s'ecrit `StartingThreat: "2*"`.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.
#
# ⚠⚠ A VERIFIER EN PARTIE REELLE : « counts towards the main scheme's TARGET
#    threat » peut se lire de deux facons — soit la menace des sbires s'ajoute
#    au compteur du complot principal, soit elle abaisse son seuil. Les deux
#    reviennent au meme pour la defaite, mais pas pour les cartes qui LISENT le
#    compteur. Montage retenu : on ajoute au compteur, ce qui est la lecture la
#    plus simple et la seule que le moteur sache rendre sans toucher au calcul
#    de seuil.


def GetAbilities() -> Sequence['Ability']:

    def menace_des_sbires(effect: 'Effect') -> int:
        total = 0
        for face in Worlds.GetOnFieldEnemies(effect):
            if face is not None and Minion.IsType(face):
                total += MenaceSurSbire(face)
        return total

    return [
        # ⚠⚠ `GiveKeywordToInPlayWhenApplyThis` et NON `ThisGainKeyword` : le
        # bonus ne va pas sur CETTE carte mais sur le COMPLOT PRINCIPAL.
        # Mesure du 08/09/2026 : avec `ThisGainKeyword`, le seuil du complot
        # principal restait a 7 (imprime 7, attendu 9) — la carte modifiait son
        # propre seuil, que personne ne regarde.
        # ⚠ Et le recalcul passe par `OnEvent.Counter` : ce qui change n'est pas
        # la presence d'une carte mais la pose d'un COMPTEUR sur un sbire deja
        # en jeu (meme lecon que `su007` le meme jour).
        # ⚠ L'ETOILE : cette fabrique rend une LISTE d'abilities, comme
        # `GiveKeywordToAttached`. Sans elle, la liste entiere est passee comme
        # UNE ability et le moteur plante au SETUP sur `AttributeError: 'list'
        # object has no attribute 'paper'` — donc deck injouable (08/09/2026).
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            MainScheme,   # ⚠ le TYPE directement : un `CardFinder` ici fait
                          # lever `AttributeError: 'list' object has no attribute
                          # 'paper'` en pleine partie (mesure du 08/09/2026).
            get_new_value=lambda effect, face: menace_des_sbires(effect),
            target_threat=1,
            change_on_event=OnEvent.Counter(Minion, COMPTEUR_MENACE),
        ),
    ]
