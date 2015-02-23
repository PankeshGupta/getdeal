/**
 * Created on Nov 18, 2013
 * Other contributers:
 */

getdeal.factory('DealService', function ($http, $q) {
    var api_url = "/deals/";
    return {
        get: function (deal) {
            var url = api_url + deal.id + "/";
            var defer = $q.defer();
            $http({method: 'GET', url: url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                })
                .error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        list: function () {
            var defer = $q.defer();
            $http({method: 'GET', url: api_url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        query: function(text){
            var url = api_url + '?q=' + text;
            var defer = $q.defer();
            $http({method: 'GET', url: url}).
                success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).
                error(function(data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        rate: function (deal, action) {
            var url = api_url + deal.id + "/rate/";
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: 'action='+action}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        share: function (deal, action) {
            var url = api_url + deal.id + "/share/";
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: 'action='+action}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        wish: function (deal, action) {
            var url = api_url + deal.id + "/wish/";
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: 'action='+action}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        wallet: function (deal, action) {
            var url = api_url + deal.id + "/wallet/";
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: 'action='+action}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        claim: function (deal, action) {
            var url = api_url + deal.id + "/claim/";
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: 'action='+action}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        bury: function (deal, action) {
            var url = api_url + deal.id + "/bury/";
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: 'action='+action}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        }
    }
});
