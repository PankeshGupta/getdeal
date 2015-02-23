/**
 * Created on Nov 18, 2013
 * Other contributers:
 */

getdeal.factory('SupplierService', function ($http, $q) {
    var api_url = "/suppliers/";
    var api_deals_url = "/deals/";
    return {
        get: function(supplier){
            var url = api_url + supplier.id+ "/";
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
        deals: function(supplier){
            var url = api_url + supplier.id + api_deals_url;
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
