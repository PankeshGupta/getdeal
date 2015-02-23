/**
 * Created on Nov 18, 2013
 * Other contributers:
 */
'use strict';

var getdeal = angular.module("Getdeal", ["ui.bootstrap", "ngCookies"], function ($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);

getdeal.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

getdeal.config(function ($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "static/js/app/views/feed.html",
            controller: "FeedController",
            resolve: {
                deals: function (DealService) {
                    return DealService.list();
                }
            }
        })
        .when("/deal/:id", {
            templateUrl: "static/js/app/views/view.html",
            controller: "DealController",
            resolve: {
                deal: function ($route, DealService) {
                    var dealId = $route.current.params.id;
                    return DealService.get(dealId);
                }
            }
        })
        .otherwise({
            redirectTo: '/'
        });
});
