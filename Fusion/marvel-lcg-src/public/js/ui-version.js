/* Sélecteur d'interface partagé par les écrans V2.

   Le serveur pose `ui_version=v2` uniquement après validation de la clé du
   siège hôte du compte d'essai. Ce script ne donne aucun droit : il expose
   seulement la préférence à CSS et aux futurs points d'entrée V2.

   Chargé sans `defer` dans <head> pour que l'attribut existe avant le premier
   calcul de style et éviter un éclair de V1. */
(function () {
    "use strict";

    var v2 = document.cookie.split(";").some(function (morceau) {
        return morceau.trim() === "ui_version=v2";
    });
    if (!v2) return;

    document.documentElement.dataset.uiVersion = "v2";

    // Les trois écrans historiques n'ont volontairement jamais eu de viewport
    // mobile. L'ajouter dans leur HTML changerait aussi la V1. En V2 seulement,
    // on le crée avant les feuilles de style : le navigateur calcule donc
    // directement la bonne largeur, sans mise en page PC intermédiaire.
    if (!document.querySelector('meta[name="viewport"]')) {
        var viewport = document.createElement("meta");
        viewport.name = "viewport";
        viewport.content = "width=device-width, initial-scale=1, viewport-fit=cover";
        document.head.appendChild(viewport);
    }
})();
