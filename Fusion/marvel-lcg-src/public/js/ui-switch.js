/*
 * ui-switch.js — la sortie de secours entre la nouvelle et l'ancienne version d'un ecran.
 *
 * A QUOI CA SERT
 * Pendant la refonte, chaque ecran existe un moment en deux exemplaires : la
 * nouvelle version et l'ancienne, qui continue de fonctionner. Ce script pose
 * le va-et-vient entre les deux, dans les deux sens, et retient le choix.
 *
 * COMMENT ON S'EN SERT
 * Une seule balise a poser en fin de <body>, avec deux ou trois attributs :
 *
 *   sur la NOUVELLE page (ajoute un lien discret « Revenir a l'ancienne version ») :
 *     <script src="/public/js/ui-switch.js" data-role="nouvelle"
 *             data-ancienne="/scene.html" defer></script>
 *
 *   sur l'ANCIENNE page (affiche un bandeau « Revenir a la nouvelle version »,
 *   UNIQUEMENT si l'utilisateur a demande l'ancienne version) :
 *     <script src="/public/js/ui-switch.js" data-role="ancienne"
 *             data-nouvelle="/prepare.html" defer></script>
 *
 * La NOUVELLE page doit en plus porter, en TOUT PREMIER dans son <head>, le
 * petit aiguillage qui lit `?ui=old` / `?ui=new` et redirige avant tout
 * affichage (voir prepare.html). Sans lui, la nouvelle version s'afficherait
 * une fraction de seconde avant de basculer : l'ecran clignoterait.
 *
 * OU EST RANGE LE CHOIX
 * Dans `localStorage`, cle « ui », valeur 'old' ou 'new'. Pas dans un cookie :
 * le serveur en pose deja (session_token, app_version) et on ne s'en approche
 * pas. Pas dans l'adresse non plus : le parametre `?ui=old` est perdu des le
 * lancement d'une partie (launcher.js fait `location.href = "/?hot_seat"`).
 * Il faut donc que le choix survive a une navigation : d'ou localStorage.
 * Tous les acces sont sous try/catch (navigation privee, stockage refuse).
 *
 * CONVENTION POUR LES PAGES MIGREES ENSUITE
 * Tant que l'ancienne version existe sous son propre nom de fichier
 * (scene.html face a prepare.html), `data-ancienne` pointe simplement dessus.
 * Quand la nouvelle version PREND le nom de l'ancienne — cas prevu pour
 * marvel.html en phase 5 — on depose d'abord une copie VERBATIM de l'ancienne
 * page dans `public/legacy/<page>.html`, qu'on ne retouche plus JAMAIS
 * ensuite, et `data-ancienne` pointe sur cette copie :
 *
 *     data-ancienne="/public/legacy/marvel.html"
 *
 * Une copie figee est la seule facon de garantir que la sortie de secours mene
 * a quelque chose qui marche encore dans six mois.
 *
 * REGLE ABSOLUE
 * Quand la preference est vide ou vaut 'new', ce script ne doit RIEN changer a
 * l'ancienne page : pas un pixel. Sinon les images de reference du filet de
 * securite (npm run captures) bougeraient sans raison.
 */
(function () {
    'use strict';

    var CLE = 'ui';
    var ANCIENNE = 'old';
    var NOUVELLE = 'new';

    function lirePreference() {
        try {
            return localStorage.getItem(CLE);
        } catch (e) {
            return null;
        }
    }

    function ecrirePreference(valeur) {
        try {
            localStorage.setItem(CLE, valeur);
        } catch (e) {
            /* navigation privee : on bascule quand meme, sans memoriser */
        }
    }

    // La balise qui a charge ce script porte la configuration.
    var balise = document.currentScript;
    if (!balise) {
        var candidates = document.querySelectorAll('script[src*="ui-switch.js"]');
        balise = candidates[candidates.length - 1] || null;
    }
    if (!balise) {
        return;
    }

    var role = balise.getAttribute('data-role');
    var urlAncienne = balise.getAttribute('data-ancienne') || '';
    var urlNouvelle = balise.getAttribute('data-nouvelle') || '';

    // Les styles ne sont poses que si l'on affiche quelque chose : une page qui
    // ne montre ni bandeau ni lien reste strictement identique a avant.
    function poserStyles(css) {
        if (document.getElementById('ui-switch-styles')) {
            return;
        }
        var style = document.createElement('style');
        style.id = 'ui-switch-styles';
        style.textContent = css;
        (document.head || document.documentElement).appendChild(style);
    }

    function basculerVers(valeur, url) {
        ecrirePreference(valeur);
        if (url) {
            window.location.href = url;
        }
    }

    /* ---------- ancienne version : le bandeau de retour ---------- */

    function afficherBandeau() {
        // Le bandeau n'a de sens que si l'utilisateur a DEMANDE l'ancienne
        // version. Sans preference, la page ne bouge pas d'un pixel.
        if (lirePreference() !== ANCIENNE) {
            return;
        }

        poserStyles(
            '#ui-switch-bandeau{display:flex;align-items:center;justify-content:center;' +
            'flex-wrap:wrap;gap:8px 16px;padding:10px 16px;' +
            'background:#2b2114;border-bottom:1px solid #6b5426;' +
            'color:#f3e3c3;font-family:"Inter","Segoe UI",system-ui,sans-serif;' +
            'font-size:14px;line-height:1.4;text-align:center}' +
            '#ui-switch-bandeau strong{color:#ffd88a;font-weight:700}' +
            '#ui-switch-bandeau button{font:inherit;font-weight:600;cursor:pointer;' +
            'padding:7px 16px;border-radius:8px;border:1px solid #8a6d2f;' +
            'background:#f0c463;color:#2b2114}' +
            '#ui-switch-bandeau button:hover{background:#ffd88a}'
        );

        var bandeau = document.createElement('div');
        bandeau.id = 'ui-switch-bandeau';
        bandeau.setAttribute('role', 'region');
        bandeau.setAttribute('aria-label', "Version de l'interface");

        var texte = document.createElement('span');
        var fort = document.createElement('strong');
        fort.textContent = "Vous utilisez l'ancienne version.";
        texte.appendChild(fort);
        bandeau.appendChild(texte);

        var bouton = document.createElement('button');
        bouton.type = 'button';
        bouton.id = 'ui-switch-retour';
        bouton.textContent = 'Revenir à la nouvelle version';
        bouton.addEventListener('click', function () {
            basculerVers(NOUVELLE, urlNouvelle);
        });
        bandeau.appendChild(bouton);

        // En tete du flux de la page : le bandeau pousse le contenu vers le
        // bas au lieu de le recouvrir.
        document.body.insertBefore(bandeau, document.body.firstChild);
    }

    /* ---------- nouvelle version : le lien discret ---------- */

    function afficherLien() {
        // Le lien est place EN TETE DU FLUX, comme le bandeau de l'ancienne
        // version : c'est la seule position qui ne recouvre aucun bouton.
        // Mesure faite sur prepare.html dans les 3 gabarits : en flottant en
        // haut a droite il masquait les 2 dernieres etapes de l'assistant, en
        // bas il tombait sur la barre de boutons fixe. Bonus : « la bascule est
        // toujours en haut de la page » se retient sans mode d'emploi.
        poserStyles(
            '#ui-switch-barre{display:flex;justify-content:flex-end;align-items:center;' +
            'padding:5px 16px;background:rgba(0,0,0,.3);' +
            'border-bottom:1px solid rgba(255,255,255,.07);' +
            'font-family:"Inter","Segoe UI",system-ui,sans-serif;font-size:12px;line-height:1.5}' +
            '#ui-switch-lien{color:rgba(255,255,255,.55);text-decoration:none;' +
            'padding:2px 7px;border-radius:6px}' +
            '#ui-switch-lien:hover{color:#fff;background:rgba(255,255,255,.09)}'
        );

        var barre = document.createElement('div');
        barre.id = 'ui-switch-barre';

        var lien = document.createElement('a');
        lien.id = 'ui-switch-lien';
        lien.href = urlAncienne || '#';
        lien.textContent = "Revenir à l'ancienne version";
        lien.addEventListener('click', function (evenement) {
            evenement.preventDefault();
            basculerVers(ANCIENNE, urlAncienne);
        });
        barre.appendChild(lien);

        document.body.insertBefore(barre, document.body.firstChild);
    }

    function demarrer() {
        if (role === 'ancienne') {
            afficherBandeau();
        } else if (role === 'nouvelle') {
            afficherLien();
        }
    }

    // `defer` garantit deja que le DOM est parse ; la garde couvre le cas d'une
    // balise posee sans `defer` par erreur.
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', demarrer);
    } else {
        demarrer();
    }
})();
