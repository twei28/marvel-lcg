# Connexion et inscription du site : refonte (décidée le 09/10/2026, PAS ENCORE CODÉE)

Constat (captures réelles FR/EN, desktop et mobile) : petit formulaire seul au centre d'un fond noir uni, sans en-tête fin,
sans scène ni grille. Seuls le titre Marvel et le bouton rouge rappellent le reste. Pied de page de la connexion : trois
phrases empilées dans un petit bloc gris peu lisible. Mobile correct mais formulaire perdu dans le vide.

Décision de l'utilisateur : refaire dans le style de l'assistant de préparation.
- En-tête fin, scène avec illustration à gauche (~30 %), formulaire à droite.
- Mobile : scène réduite en bandeau, formulaire dessous.
- Respecter le mode sobre (voir fiche mode-sobre-des-menus).

Corrections à faire en même temps :
- « Le site est complet (0 comptes). » non traduit en anglais (`site/orchestrateur.py` ~l.1731, pas passé par `lang.t`).
- Français sans accents (« Deja un compte », « reinitialisation ») : remettre les accents.
- Pied de page de la connexion : simplifier, lisible.

Ordre : après le mode sobre et le salon invité (mêmes styles).
