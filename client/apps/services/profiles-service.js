/**
 * Created on Nov 18, 2013
 * Other contributers:
 */

getdeal.factory('ProfileService', function ($http, $q) {
    var api_url = "/users/";
    var api_profile = "p/";
    var api_followers_url = "/followers/";
    var api_following_url = "/following/";
    var api_follow_url = "/follow/";
    var api_rated_url = "/rated/";
    var api_shared_url = "/shared/";
    var api_viewed_url = "/viewed/";
    var api_wished_url = "/wished/";
    var api_claimed_url = "/claimed/";
    var api_wallet_url = "/wallet/";
    var api_buried_url = "/buried/";
    var api_categories_url = "/categories/";
    var api_cities_url = "/cities/";
    var api_dsites_url = "/dsites/";
    var api_suppliers_url = "/suppliers/";

    return {
        get: function(username, profile){
            var url = api_url;
            if (profile === true){
               url = url + api_profile;
            }
            url = url + username + "/";
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
        list: function(profile){
            var url = api_url;
            if (profile === true){
               url = url + api_profile;
            }
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
        query: function(text, profile, eq){
            var url = api_url;
            if (profile === true){
               url = url + api_profile;
            }
            url = url + '?q=' + text;
            if (eq === true){
                url = url + '&eq=' + 1;
            }
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
        update: function(object, profile, username){
            var url = api_url;
            var objectUpdate = object.user;
            if (profile === true){
               url = url + api_profile;
                objectUpdate = object;
            }
            url = url + username + "/";
            var defer = $q.defer();
            $http({method: 'PUT',
                    url: url,
                    data: objectUpdate}).
                success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).
                error(function(data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        followers: function(username){
            var url = api_url + username+ api_followers_url;
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
        following: function(username){
            var url = api_url + username+ api_following_url;
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
        follow: function(username, action){
            var url = api_url + username+ api_follow_url;
            var defer = $q.defer();
            $http({method: 'POST',
                    url: url,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    data: 'action='+action}).
                success(function(data, status, headers, config) {
                    defer.resolve(data);
                }).
                error(function(data, status, headers, config) {
                    defer.reject("status");
                });
            return defer.promise;
        },
        rated: function(username){
            var url = api_url + username + api_rated_url;
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
        shared: function(username){
            var url = api_url + username + api_shared_url;
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
        viewed: function(username){
            var url = api_url + username + api_viewed_url;
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
        wished: function(username){
            var url = api_url + username + api_wished_url;
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
        claimed: function(username){
            var url = api_url + username + api_claimed_url;
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
        wallet: function(username){
            var url = api_url + username + api_wallet_url;
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
        buried: function(username){
            var url = api_url + username + api_buried_url;
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
        categories: function(username){
            var url = api_url + username + api_categories_url;
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
        cities: function(username){
            var url = api_url + username + api_cities_url;
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
        dsites: function(username){
            var url = api_url + username + api_dsites_url;
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
        suppliers: function(username){
            var url = api_url + username + api_suppliers_url;
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

