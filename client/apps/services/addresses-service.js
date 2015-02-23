/**
 * Created on Nov 18, 2013
 * Other contributers:
 */

getdeal.factory('CityService', function ($http, $q) {
    var api_url = "/cities/";
    var api_deals_url = "/deals/";
    return {
        get: function(city){
            var url = api_url + city.id+ "/";
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
        list: function(){
            var defer = $q.defer();
            $http({method: 'GET', url: api_url}).
                success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).
                error(function(data, status, headers, config) {
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
        deals: function(city){
            var url = api_url + city.id + api_deals_url;
            var defer = $q.defer();
            $http({method: 'GET', url: url}).
                success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).
                error(function(data, status, headers, config) {
                    defer.reject(status);
            });
            return defer.promise;
        }
    }
});
