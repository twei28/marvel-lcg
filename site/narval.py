"""Le narval du moment : la mascotte change toutes les trois heures.

Demande de l'utilisateur, 17/09/2026 : « c'est possible de changer d'image
toutes les 2-3 heures, que ça change et dans l'onglet et sur le site ? ».

⚠ LA MEME FORMULE VIT EN DEUX ENDROITS, ET C'EST VOULU. Le SITE la calcule ici
(page d'attente, favicon), le JEU la calcule en JavaScript
(`public/js/prepare/narval.js`) parce qu'il est servi par un autre processus,
sur un autre sous-domaine, sans rien partager avec celui-ci. Les deux doivent
donner le MEME narval au meme instant, sinon l'onglet et la page se
contrediraient. `site/test_narval.py` compare les deux listes et les deux
formules, et refuse qu'elles divergent.

⚠ ET ELLE EST CALCULEE EN UTC. Sur l'heure locale, deux joueurs dans deux
fuseaux verraient deux mascottes differentes au meme moment.
"""
import time

#: Les mascottes, dans l'ordre de passage. Ajouter un nom ici suppose d'avoir
#: depose `narwhal-<nom>.png` dans `site/static/` ET dans
#: `Fusion/marvel-lcg-src/assets/textures/`, puis de completer la liste jumelle
#: de `narval.js`.
NARVALS = ("cap", "magneto", "cyclope", "wolverine", "thor")

#: Duree d'un passage, en heures.
HEURES = 3


def tranche(maintenant: float | None = None) -> int:
    """Le numero de la tranche horaire en cours, depuis l'epoque UTC.

    On compte les heures ECOULEES plutot que l'heure du jour : une liste de
    cinq mascottes sur des tranches de trois heures ne tombe pas juste sur 24,
    et l'heure du jour ferait sauter une mascotte chaque minuit.
    """
    secondes = time.time() if maintenant is None else maintenant
    return int(secondes // (HEURES * 3600))


def narval(maintenant: float | None = None) -> str:
    """Le nom du narval a servir. Toujours un nom de la liste."""
    return NARVALS[tranche(maintenant) % len(NARVALS)]


def fichier(maintenant: float | None = None) -> str:
    """Le nom de fichier correspondant, tel qu'il est range dans `static/`."""
    return "narwhal-%s.png" % narval(maintenant)
