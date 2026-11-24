from . import *

# Demons of Limbo — TRAITRISE (deck signature de Zombie Magik, carte 3/3, derniere du set).
# Surge. (desc)
# When Revealed: Put the minion with the most hit points in the encounter discard pile
#   into play engaged with you.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[surge]] (mots-cles/surge.md) : mot-cle imprime en tete de texte, lu NATIVEMENT par le
#   moteur depuis `desc.Surge` (deja renseigne dans data/cards_custom.json : `"Surge": "1"`).
#   Aucun script requis pour lui (fiche : « aucune carte du pack n'a de script pour ce seul
#   mot-cle » ; le script de cette carte ne porte QUE la capacite « When Revealed » annexe,
#   exactement la regle enoncee sur la fiche pour toute carte qui cumule Surge avec un effet
#   imprime distinct).
# - « activates »/« DoActivate » : NON APPLICABLE ici, cette carte ne fait ni attaquer ni
#   manigancer personne ; elle met seulement un sbire EN JEU. Pas de consigne
#   « passer_sur_option: Defense » (reservee aux activations reelles, bug hg017) a appliquer
#   pour ce cas de test.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Put <le sbire choisi> into play engaged with you » (depuis la defausse rencontre) :
#   `next_evol/on_the_run/40111.py` Tag Team, option 2 du choix du joueur : « Discard 7 cards
#   from the top of the encounter deck. Put the topmost MARAUDER minion in the encounter
#   discard pile into play engaged with you » -> `face.PutIntoPlay(player, effect)`. Le
#   commentaire du helper `MettreEnJeuEngage` (`cards/pack/skrull_menace/communs_modulaires.py:52`)
#   confirme que mettre un SBIRE en jeu via `PutIntoPlay(joueur, effect)` l'engage directement
#   avec ce joueur et ne declenche AUCUN « When Revealed » supplementaire : exactement le
#   comportement vise par « into play engaged with you », sans action separate a coder.
# - « the <X> with the MOST hit points » (selection par tri) : `web_of_deceit/the_lizard/wd059.py`
#   Reptilian Regeneration : « Attach to the REPTILIAN enemy with the highest printed hit
#   points » -> `sorted(candidats, key=lambda x: x.printed_health)[-1]`. Meme logique reprise
#   ici : les candidats sont hors jeu (defausse rencontre), donc on trie sur `printed_health`
#   (PV IMPRIMES, scales par `*` s'il y a lieu) et jamais sur `.health` (PV COURANTS) — voir
#   TEXTE CONTRE CODE plus bas pour la raison technique.
# - « ALL/the minion(s) ... in the encounter DISCARD PILE » : `skrull_menace/skrull_elite_skymax/
#   sk241.py` et `shadowland/ninja_swarm/sl036.py` lisent tous deux la defausse rencontre via
#   `Worlds.GetEncounterDiscardPileCards(effect)` puis filtrent sur `Minion.IsType(f)` (sk241 :
#   « tous les sbires de la defausse, Skrull ou non »). Meme filtre repris ici, SANS trait
#   particulier (le texte imprime ne restreint a aucun trait, contrairement a sk241/sl036).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE
#   carte (`Condition2.ThisIsTrigger` deja integre a la fabrique).
# « the MINION with the most hit points » -> filtre `Minion.IsType(f)`, jamais `Enemy` generique
#   (qui engloberait aussi un Vilain — en pratique aucun Vilain ne finit dans la defausse
#   rencontre, mais le texte dit bien « minion », pas « enemy »).
# « the minion with the MOST hit points » -> tri par PV IMPRIMES (`printed_health`), PAS par PV
#   restants (`.health`). Raison technique verifiee dans le moteur : `Health.OnParentReset`
#   (`src/game/card/face/component/health.py`) remet `self.health = 0` quand une carte SORT de
#   jeu (donc toute carte dans la defausse rencontre, qui n'est PAS en jeu, a `.health == 0`,
#   quel que soit son etat avant d'etre defaussee) ; seul `printed_health` (PV imprimes, formate
#   par joueur si la carte porte un `*`) reste significatif hors jeu. Meme choix que wd059.
# « in the ENCOUNTER DISCARD PILE » -> `Worlds.GetEncounterDiscardPileCards(effect)`, jamais la
#   pioche rencontre (`GetEncounterDeckCards`) ni la defausse JOUEUR.
# « PUT ... into play ENGAGED WITH YOU » -> `cible.PutIntoPlay(message.GetToPlayer(), effect)` :
#   le joueur qui a revele la carte (celui vise par « you »), pas le joueur actif ni un autre.
# Defausse rencontre sans AUCUN sbire -> rien ne se passe (pas de « if you cannot » imprime sur
#   cette carte, et aucune clause de repli n'est donnee : silence volontaire, cf. §5 du
#   processus).
# Plusieurs sbires a egalite de PV imprimes -> AUCUNE regle de bris d'egalite n'est imprimee sur
#   la carte ; `sorted(...)[-1]` prend alors le DERNIER de l'ordre de retour de
#   `GetEncounterDiscardPileCards` (ordre d'empilement de la defausse) parmi les egalites. A
#   CONFIRMER EN PARTIE REELLE si ce cas se presente (deux sbires distincts a PV imprimes
#   identiques simultanement dans la defausse) : aucune regle officielle Marvel Champions ne
#   tranche ce cas non plus (meme angle mort que wd059, qui ne le traite pas davantage).


def GetAbilities() -> Sequence['Ability']:

    def demons(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        sbires = [f for f in Worlds.GetEncounterDiscardPileCards(effect) if Minion.IsType(f)]
        if not sbires:
            return
        cible = sorted(sbires, key=lambda f: f.printed_health)[-1]
        cible.PutIntoPlay(message.GetToPlayer(), effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            demons,
        ),
    ]
