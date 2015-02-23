/**
 * Created on Dec 30, 2013

 * Other contributers:
 */

var services = angular.module('Utils.services', ['ngResource']);

services.constant('Tags', (function () {
    return {'NA':{'name':'Nouvel arrivage', 'class':'nouvel-arrivage', 'sign':'icon-plus-sign'},
                'MR':{'name':'Meilleure réduction', 'class':'meilleure-reduction', 'sign':'icon-bolt'},
                'MA':{'name':'Meilleur avis', 'class':'meilleur-avis', 'sign':'icon-thumbs-up'},
                'MV':{'name':'Meilleure vente', 'class':'meilleure-vente', 'sign':'icon-star'},
                'TB':{'name':'Se termine bientôt', 'class':'se-termine-bientot', 'sign':'icon-time'},
                'EF':{'name':'Est dans vos favoris', 'class':'est-dans-favoris', 'sign':'icon-heart'}
    };
}()));

services.constant('SearchFilters', (function () {
    return {
                "check-beaute-bien-etre": 1,
                "check-restauration": 1,
                "check-shopping-services": 1,
                "check-voyages": 1,
                "check-sorties-loisirs": 1,
                "check-high-tech": 1,
                score: 100,
                minPrice: 10,
                maxPrice: 1000,
                reduction: 0,
                destination: 'all'
            };
}()));

services.constant('Categories', (function () {
    return ["check-beaute-bien-etre", "check-restauration", "check-shopping-services", "check-voyages", "check-sorties-loisirs", "check-high-tech"];
}()));
