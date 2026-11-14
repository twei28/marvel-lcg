from . import *

# * Blade — ALLIE (Survivor deck, carte 4/5). Cout 0. THW 1[star]. ATK 2[star]. PV 3. RES wild.
#   SURVIVOR. HUNTER.
# Undead Hunter. While Blade attacks a Zombie or Metazombie enemy, he gets +2 ATK. If he defeats it, Blade
# takes no consequential damage.
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - « While <this> attacks a <trait> character, it gets +X ATK » (bonus conditionnel pendant UNE attaque,
#   pas permanent) : modele officiel `42025` Harpoon (pack `angel`) : `*AbilityFactory.
#   UnitGetATKWhileAttacking(AbilityType.NonKeywordStar, "This", CardFinder2("AERIAL", Unit2), 1)`. Repris
#   ici avec un bonus de `2` (imprime) et une cible filtree par DEUX traits en OU (« Zombie or Metazombie »)
#   plutot qu'un seul (« Aerial ») -- `CardFinder2` n'accepte qu'UN `trait` (singulier,
#   `card_finder/finder.py:391`), donc le `CardFinder` DE BASE est utilise directement a la place
#   (`traits=[...]`, parametre OR natif, deja employe par `hg001`/`hg073` de ce meme scenario).
# - « If he defeats it, <nom> takes no consequential damage » (negation CONDITIONNELLE, apres coup, liee a
#   la DEFAITE de la cible par CETTE attaque) : modele `mut_gen/32091` Cannonball (« Cannonball takes -1
#   consequential damage after he attacks and defeats a minion »), charpente
#   `AbilityFactory.AfterUnitAttackAndDefeatUnit(AbilityType.NonKeywordStar, "This", <cible>, op)` qui
#   recupere le message d'attaque EN COURS via `message.GetWouldAtkMessage()` (le degat consequent n'est
#   calcule qu'APRES cette etape, voir `card_type/ally.py:34-58`). Cannonball ne fait que REDUIRE (`-1`,
#   `GainForThisActive(attack_consequential_damage=-1)`) ; Blade annule ENTIEREMENT -- la primitive exacte
#   pour « takes NO consequential damage » (negation totale, pas une reduction chiffree) est `message.
#   DoesNotTakeConsequentialDamage(effect)`, deja employee par trois cartes officielles sur le message
#   d'attaque (`wonder_man/58020`, `stld/17020` Cosmo, `tmnt_aspect_leadership/ul038`) et documentee dans le
#   commentaire de `skrull_menace/sk283` (« lu par `Ally.GetAbilities`, ally.py:49 »). Blade combine donc les
#   DEUX modeles : le DECLENCHEUR post-defaite de Cannonball, la PRIMITIVE de negation de 58020/17020.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « Undead Hunter » : NOM D'AMBIANCE propre a cette carte (titre en gras d'une capacite unique, pas un
#   mot-cle reutilisable) -- meme traitement que « Absorption » sur `hg011` Zombie Captain Marvel de ce MEME
#   scenario (commentaire de ce fichier : « NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel »).
#   Grep `data/cards.json` et `data/cards_custom.json` sur `"Undead Hunter"` : UNE SEULE occurrence, celle de
#   `hg075` lui-meme -- confirme qu'aucune autre carte du depot ne le reprend comme mecanique partagee.
#   Absent du README des mots-cles, rien a ouvrir, rien a creer.
# - « consequential damage » : terme de REGLE DE BASE (pas un mot-cle en gras imprime sur cette carte -- le
#   texte dit « Blade takes no consequential damage », prose nue), deja implemente nativement par
#   `card_type/ally.py` ; seule la NEGATION ponctuelle est scriptee ici (comme `58020`/`17020`), jamais le
#   mecanisme de base lui-meme.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# - « a Zombie or Metazombie ENEMY » (et non « minion ») -> `CardFinder(card_type=Enemy, traits=["ZOMBIE",
#   "METAZOMBIE"])`, exactement le MEME filtre que `hg073` Chewie, mais ici le mot imprime est bien « enemy »
#   (englobe nativement `Minion` ET `Villain`, aucune ambiguite de lecture contrairement a `hg073` -- ce
#   point n'a donc PAS besoin d'un « A CONFIRMER »).
# - « WHILE Blade attacks » (bonus actif PENDANT l'attaque, pas une Reponse/Interrupt separee) ->
#   `UnitGetATKWhileAttacking`, qui modifie l'attaque EN COURS (`WhenRecalculateAttackDamage`), pas un
#   message distinct.
# - « gets +2 ATK » : bonus FIXE de 2, jamais lie au nombre de joueurs (pas de `*` sur cette phrase en
#   prose) -- a ne pas confondre avec le `*` NATIF de `desc.ATK = "2*"` (etoile de degats consequents, note
#   generale posee dans `hg072.py`) : les DEUX valent « 2 » par coincidence, mais l'un est un bonus
#   D'ATTAQUE conditionnel (code ici), l'autre une etoile de DEGAT CONSEQUENT lue nativement (jamais codee).
# - « IF HE DEFEATS IT » (condition : la cible doit etre VAINCUE par CETTE attaque, pas juste attaquee) ->
#   `AfterUnitAttackAndDefeatUnit` (et non `WhenUnitWouldAttack`, qui se declencherait AVANT de savoir si la
#   cible est vaincue -- piege deja signale sur `sk283`, qui lui NE CONDITIONNE PAS a la defaite et utilise
#   donc `WhenUnitWouldAttack`, modele a NE PAS copier tel quel ici).
# - « Blade TAKES NO consequential damage » (negation TOTALE, pas une reduction) -> `message.
#   DoesNotTakeConsequentialDamage(effect)`, jamais `GainForThisActive(attack_consequential_damage=-N)` (qui
#   ne ferait que REDUIRE, laissant un reste si N < degat consequent reel -- ici N serait de toute facon
#   `1` puisque `desc.ATK = "2*"` ne porte QU'UNE etoile, donc `-1` aurait accidentellement donne le MEME
#   resultat visible que la negation totale sur CETTE carte precise ; retenu malgre tout la primitive de
#   negation, exacte vis-a-vis du texte imprime et robuste si la carte etait un jour reequilibree avec plus
#   d'une etoile).
# - Meme cible (`Enemy` + traits ZOMBIE/METAZOMBIE) utilisee par les DEUX capacites : une seule variable
#   `cible` partagee, pas deux `CardFinder` divergents qui pourraient un jour desynchroniser.
# - Pas de `unless`/`otherwise`/`instead`/limite imprimee : rien d'autre a coder.
#
# ---------------------------------------------------------------------------
# ETAPE 6 : BLOC NOMBRES, TEXTE <-> CODE
#
# - « gets +2 ATK » -> `2` explicite passe a `UnitGetATKWhileAttacking`.
# - `desc.ATK = "2*"` / `desc.THW = "1*"` : LUS NATIVEMENT (etoiles de degats consequents d'Allie), aucun
#   script requis (note generale `hg072.py`).
#
# A CONFIRMER EN PARTIE REELLE : meme reserve que `hg072`/`hg073`/`hg074` -- aucun cas n'a ete EXECUTE par
# moi (consigne explicite de la tache : ne pas lancer `test_capacites.py`). Point MOTEUR non verifiable
# sans execution : confirmer que `message.GetWouldAtkMessage()` renvoie bien, au moment de
# `AfterUnitDefeatedUnit`, le MEME objet message sur lequel `DoesNotTakeConsequentialDamage` doit agir avant
# que `card_type/ally.py` ne lise `end_message.would_atk_messages` (ordre deja exploite par `32091`
# Cannonball, mais jamais rejoue PAR MOI sur CETTE carte).


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(card_type=Enemy, traits=["ZOMBIE", "METAZOMBIE"])

    def pas_de_degats_consequents(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        message.GetWouldAtkMessage().DoesNotTakeConsequentialDamage(effect)

    return [
        *AbilityFactory.UnitGetATKWhileAttacking(
            AbilityType.NonKeywordStar,
            "This",
            cible,
            2,
        ),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.NonKeywordStar,
            "This",
            cible,
            pas_de_degats_consequents,
        ),
    ]
