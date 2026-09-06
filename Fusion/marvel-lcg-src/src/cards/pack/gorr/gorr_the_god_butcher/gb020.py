from . import *

# You Are My God — COMPLOT ANNEXE. Seuil 2 (FIXE, aucune icone joueur), icone
# de CRISE, 2 icones de boost.
#
# Hinder 1[per_hero].
# Forced Response: After Gorr the God Butcher attacks, he attacks again. Deal
#   him no boost cards for this attack. (Limit once per player per phase.)
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Hinder` (mots-cles/hinder.md) : BASE AUTOMATIQUE, `desc.Hinder = "1*"`.
#   Le moteur pose la menace sur CETTE carte a son entree en jeu. Aucun script.
# - `Crisis` (mots-cles/crisis.md) : base automatique elle aussi.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « After X attacks, he attacks again » : `AfterUnitAttackEnd` puis
#   `DoAttackYou`, la forme de 07020 (Ball and Chain) pour le declencheur.
#   ⚠ Le « no boost cards » est le parametre `do_not_give_boost=True` de
#   `DoActivate` (enemy.py:203) : `DoAttackYou` (enemy.py:98) ne l'accepte
#   PAS. On passe donc par `DoActivate`, qui choisit lui-meme attaque ou
#   manigance selon la forme du joueur vise — ici toujours l'attaque, puisque
#   la carte ne se declenche qu'apres une attaque.
# - « Limit once per player per phase » : ⚠ NI `LimitOncePerPhase` (globale :
#   wd056b documente la panne, elle interdit l'effet a tous les autres joueurs
#   des qu'un seul l'a declenche), NI `LimitOncePerPhasePerPlayer`, qui
#   `assert isinstance(message, TriggerNonePlayerMessage)`
#   (condition/once_per.py:30) — or `AfterUnitAttackEnd` n'en est pas un, et
#   l'assertion, avalee par `effect_checker.py`, rendait la carte INERTE en
#   silence. Constate par le cas gb020 le 02/09/2026.
#   La condition est donc ecrite a la main sur le meme registre du moteur
#   (`world.stat.IsOncePerPhasePerPlayer`), avec le joueur pris sur le message
#   d'attaque (`GetAgainstPlayer`) au lieu de `GetToPlayer`.
#   ⚠ CORRECTIF DU 07/09/2026 (audit C, point 2) : lire le registre ne suffit
#   pas, il faut aussi l'ALIMENTER. Le moteur le fait tout seul dans
#   `Effect.SetHasSpellInPhase` (effect.py:172-177), mais UNIQUEMENT quand
#   `self.bind_message` est une `TriggerNonePlayerMessage`, ce que
#   `AfterUnitAttackEnd` n'est pas (sender_damage.py:558, herite de
#   `TriggerUnitMessage`). L'ecriture au registre est donc faite A LA MAIN,
#   ici meme, par `world.stat.RecordEffectWithPlayer(effect, joueur)`, AVANT
#   de declencher la seconde attaque : sans cet ordre, la seconde attaque
#   emet elle-meme un `AfterUnitAttackEnd`, la condition le relit alors que
#   rien n'est encore inscrit, et la Reponse Forcee se redeclenche sur
#   elle-meme sans fin (bug constate : 10 degats en une seule activation).
#   Preuve : `tools/test_capacites.py … "gb020"`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After Gorr the God Butcher ATTACKS » -> apres son attaque, y compris une
#   attaque declenchee par une autre carte, pas seulement l'activation de la
#   phase du vilain.
# « HE ATTACKS AGAIN » -> une seconde attaque contre le MEME joueur que la
#   premiere (le texte ne change pas de cible).
# « Deal him NO BOOST CARDS for this attack » -> la seconde attaque seulement.
# « (Limit ONCE PER PLAYER PER PHASE) » -> un joueur ne peut subir la seconde
#   attaque qu'une fois par phase ; a plusieurs, chacun a la sienne.
# ⚠ Sans cette limite, une attaque en declencherait une autre indefiniment.


def GetAbilities() -> Sequence['Ability']:

    def une_fois_par_joueur_par_phase(effect: 'Effect',
                                      message: 'Message.AfterUnitAttackEnd') -> bool:
        joueur = message.GetAgainstPlayer()
        if not isinstance(joueur, Player):
            return False
        return effect.world.stat.IsOncePerPhasePerPlayer(effect.ability, joueur)

    def il_frappe_encore(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this
        Unused(this)

        vilain = TrouverGorr(effect)
        joueur = message.GetAgainstPlayer()
        if vilain and isinstance(joueur, Player):
            # Inscription AVANT de declencher la seconde attaque : c'est elle
            # qui alimente le registre lu par `une_fois_par_joueur_par_phase`.
            # Faite trop tard (apres `DoActivate`), la seconde attaque
            # redeclencherait cette meme Reponse Forcee sans que rien ne
            # l'arrete (voir note ci-dessus).
            effect.world.stat.RecordEffectWithPlayer(effect, joueur)
            vilain.DoActivate(joueur, effect, do_not_give_boost=True)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name=NOM_GORR),
            il_frappe_encore,
            conditions=[une_fois_par_joueur_par_phase],
        ),
    ]
