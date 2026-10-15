from . import *

# Tarnax II — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Decrease the target threat value of the main scheme by 1[per_hero].
#
# Carte de reference : **`hs224`** Cold Blooded, MEME montage :
# `GiveKeywordToInPlayWhenApplyThis(MainScheme, target_threat=-1,
# get_new_value=par_heros)`. ⚠ `get_new_value` rend la GRANDEUR (positive) ;
# le signe vient de `target_threat=-1`. Une valeur negative est lue par
# environment_helper2.py comme un RETRAIT et rien n'etait applique (constate
# le 15/10/2026 : cible restee a 6, cas [sk-e] sk094 rouge).
#
# ⚠ « by 1[per_hero] » : -1 PAR JOUEUR ; « the main scheme » : le stade courant, et le suivant quand il arrive.
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            MainScheme,
            target_threat=-1,
            get_new_value=lambda effect, face: Worlds.GetPlayerNumIcon(effect),
        ),
    ]
