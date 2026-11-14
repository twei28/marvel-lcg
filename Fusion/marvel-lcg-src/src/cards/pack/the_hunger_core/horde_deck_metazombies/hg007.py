from . import *

# Zombie Captain America — METAZOMBIE (Horde deck). AVENGER. SOLDIER. SCH 1. ATK 2. PV 12[per_hero].
# Leader of the Horde. Each other Metazombie gets +1 ATK.
# Shield — Forced Interrupt: The first time each phase Zombie Captain America would take damage, reduce that
# damage by 2.
#
# Cartes de reference :
#  - « Leader of the Horde. Each other Metazombie gets +1 ATK » : `GiveKeywordToInPlayWhenApplyThis(
#    CardFinder(traits=["METAZOMBIE"], card_type=Villain), attack=1, not_include_this=True)`, modele `sk099`
#    Intelligentsia (« Each other SKRULL enemy gets +1 SCH »).
#  - « Shield — Forced Interrupt: The first time each phase ... would take damage, reduce ... by 2 » :
#    `WhenUnitWouldTakeDamage` + `message.ReduceDamage`, modele `ag002` Captain America (Rainy) ; limite
#    « the first time each phase » -> `.LimitOncePerPhase()`, modele `ar007` God of War / `sm010` Hyper-Agility.
#
# ⚠ Mots-pieges :
#  - « EACH OTHER Metazombie » : pas elle-meme (`not_include_this=True`) ; « Metazombie », pas « enemy » : ne
#    buffe PAS Le Coeur (hg001-hg003), qui n'a pas le trait METAZOMBIE (`CapacitesDuCoeur` le confirme).
#  - « Shield » et « Leader of the Horde » sont des NOMS D'AMBIANCE propres a cette carte, pas des mots-cles
#    officiels (absents de `docs/reference/mots-cles/README.md`, aucune autre carte du moteur ne les reprend) :
#    rien a ouvrir avant de coder, le texte qui suit EST la regle complete.
#  - « would take damage » SANS restriction a l'attaque ni a la defense : toute source de degats (attaque,
#    indirect, Rupture...) compte, contrairement a `ag002` qui ne couvre que la defense. Aucun `is_from_attack`
#    ni `while_defending` ici.
#  - « reduce that damage by 2 » SANS minimum imprime (contrairement a `ag002`, « to a minimum of 1 ») : la
#    reduction peut ramener les degats a 0.
#
# ⚠⚠ PIEGE DE REPERTOIRE (mesure le 27/10/2026, PREMIER Metazombie code) : `data/cards_custom.json`, champ
# `set_name`, vaut « Horde deck (Metazombies) » pour hg007-hg015 -- PAS « The Hunger Core » comme hg001-hg006.
# Nettoye (`FileManager.CleanName`) ca donne `horde_deck_metazombies`, le dossier ou vit CE fichier, PAS
# `the_hunger_core/the_hunger_core/`. Un script pose au mauvais endroit ne leve AUCUNE erreur : `database.py`
# (`CardsDB.FindAbilities`, `try_load_module`) avale l'`ImportError`/`ModuleNotFoundError` en silence et renvoie
# `GetAbilities() -> []` -- la carte se comporte EXACTEMENT comme si son texte etait vide, sans trace dans le
# rapport de test (ni rouge franc, ni message d'erreur : juste des assertions qui echouent une a une). Avant
# de chercher un bug dans la logique d'une capacite qui "ne part jamais", verifier D'ABORD le `set_name` de la
# carte dans `cards_custom.json` et le dossier ou le fichier a ete pose. Memes dossiers deja prepares pour les
# 8 autres Metazombies : `zombie_<nom>_signature/` pour chaque deck signature.


def GetAbilities() -> Sequence['Ability']:

    def shield(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        valeur = min(2, message.will_take_damage)
        if valeur > 0:
            message.ReduceDamage(valeur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(traits=["METAZOMBIE"], card_type=Villain), attack=1, not_include_this=True,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt, "This", shield,
        ).LimitOncePerPhase(),
    ]
