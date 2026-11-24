from . import *

# Sleeper Agent — TRAITRISE (deck signature de Zombie Black Widow, carte 3/3, derniere carte du set). Trait
# ATTACK.
# When Revealed: If you are in alter-ego form, change to hero form. Zombie Black Widow activates against you.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Carte-modele PRESQUE au mot pres (meme pack) : `hg024` Hulk Hungry! (set signature de Zombie Hulk), texte
#   imprime strictement identique a un nom de Metazombie pres (« If you are in alter-ego form, change to hero
#   form. <Metazombie nomme> activates against you. »). Repris tel quel ici, seul le nom change :
#   `Worlds.FindVillain(effect, name="Zombie Black Widow")` au lieu de "Zombie Hulk".
# - « If you are in alter-ego form, change to hero form. <Villain> attacks/activates you » : modele d'origine
#   `50076` Attacrobatics (pack officiel black_widow) : `player.IsAlterEgo()` -> `player.GetIdentity(
#   ).ChangeToForm(Hero, effect)`, puis `Worlds.FindVillain(effect, name="Black Widow")` et l'activation.
#   Ecart assume, deja documente par hg024 : 50076 dit « attacks » (DoAttackYou) ; cette carte dit « activates »
#   (couvre aussi la manigance en forme Alter-Ego) -- sans consequence pratique ici non plus, voir plus bas.
# - « <Villain> activates against you » (et non « attacks you ») : modele `hg017` Avengers, Feast! (meme pack) :
#   `metazombie.DoActivate(joueur, effect, ...)` plutot que `DoAttackYou` -- meme piege deja documente par ce
#   pack : « activates » couvre Attaque ET Manigance selon la FORME du joueur vise au moment de l'appel.
# - Trouver LE Metazombie nomme (pas « chaque Metazombie en jeu ») : `Worlds.FindVillain(effect,
#   name="Zombie Black Widow")`, exactement le modele de 50076/hg024, a distinguer du helper `Metazombies(
#   effect)` de `commun.py` qui, lui, sert aux textes « EACH Metazombie ».
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « activates » : pas une fiche mots-cles dediee (absente de `docs/reference/mots-cles/README.md`), c'est
#   la mecanique de base d'activation d'ennemi (`Enemy.DoActivate`), deja traitee ainsi par hg012/hg017/hg024
#   de ce meme pack.
# - « change to hero form » : regle de base (changement de forme hero/alter-ego), aucune fiche mots-cles/
#   dediee (grep README.md : absent) ; rendu par `Identity.ChangeToForm`, idiome deja employe par des cartes
#   officielles (`50076`, `30331`, `60386`) et par `hg024` de ce meme pack.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte.
# « If YOU are in alter-ego form » -> `message.GetToPlayer()` (le joueur a qui CETTE carte est revelee, pas un
#   autre joueur de la partie), `.IsAlterEgo()` natif (modele 50076/hg024 au mot pres).
# « change to hero form » -> `joueur.GetIdentity().ChangeToForm(Hero, effect)`, SEULEMENT dans la branche
#   « if » : un joueur deja en forme Heros ne change pas de forme (le texte conditionne le changement par
#   « if you are in alter-ego form », il ne dit pas « change to hero form » nu).
# « Zombie Black Widow activates against you » -> `Worlds.FindVillain(effect, name="Zombie Black Widow")` (le
#   Metazombie NOMME, pas « chaque Metazombie » ni « le Metazombie actif ») ; `villain.DoActivate(joueur,
#   effect)` -- puisque le joueur vient d'etre force en forme Heros par la branche precedente (quand elle
#   s'applique), Zombie Black Widow ATTAQUE en pratique toujours sur cette carte precise (`DoActivate` lit la
#   forme REELLE du joueur au moment de l'appel, qui est deja Heros a ce stade de la resolution, que le joueur
#   l'ait ete depuis le debut ou qu'il vienne juste de changer). La branche Manigance de `DoActivate` n'est
#   donc, pour CETTE carte, jamais empruntee en pratique -- consequence du texte lui-meme (le changement de
#   forme est OBLIGATOIRE et precede l'activation), pas une restriction codee en dur : on appelle bien
#   `DoActivate` (jamais `DoAttackYou` seul), pour rester fidele au mot « activates » et robuste si un effet
#   hors de ce module empechait un jour le changement de forme.
# « IF Zombie Black Widow n'est plus en jeu » (NON IMPRIME, mais le moteur doit rester silencieux si ce
#   Metazombie nomme a deja ete vaincu avant la resolution de cette carte de SON PROPRE deck signature) ->
#   garde `if villain:` avant l'appel, modele 50076/hg024.
#
# ⚠ Pas de surge, pas de boost supplementaire impose, pas de restriction « unless »/« otherwise » dans le
# texte imprime : rien d'autre a coder.
#
# A CONFIRMER en jeu reel (aucun outil de ce lot ne le verifie) : le livret du scenario (recupere en TTS) ne
# precise pas explicitement le cas « Zombie Black Widow deja vaincu quand sa propre carte signature se revele » ;
# le garde `if villain:` est defensif (modele 50076/hg024), pas la transcription d'une regle imprimee pour ce
# cas.


def GetAbilities() -> Sequence['Ability']:

    def sleeper_agent(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        if joueur.IsAlterEgo():
            joueur.GetIdentity().ChangeToForm(Hero, effect)

        villain = Worlds.FindVillain(effect, name="Zombie Black Widow")
        if villain:
            villain.DoActivate(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            sleeper_agent,
        ),
    ]
