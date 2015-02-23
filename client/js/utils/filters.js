/**
 * Created on Dec 24, 2013
 * Other contributers:
 */

angular.module('Utils.filters', []).
    filter('dateParse', ['$filter', function ($filter) {
        return function (date) {
            var parts = date.split('-');
            return new Date(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]);
        };
    }])
    .filter('FromNow', ['$filter', function ($filter) {
        return function (date) {
            var now = moment(Date());
            var diff = moment(date).diff(now, 'days');
            if (diff > 0) {
                return {'value': diff, 'unit': 'D'};
            }
            diff = moment(date).diff(now, 'hours');
            if (diff > 0) {
                return {'value': diff, 'unit': 'H'};
            }
            return {'value': moment(date).diff(now, 'minutes'), 'unit': 'M'};
        };
    }])
    .filter('partition', function ($cacheFactory) {
        var arrayCache = $cacheFactory('partition');
        return function (arr, size) {
            if (arr != undefined){
                var parts = [], cachedParts,
                    jsonArr = JSON.stringify(arr);
                for (var i = 0; i < arr.length; i += size) {
                    parts.push(arr.slice(i, i + size));
                }
                cachedParts = arrayCache.get(jsonArr);
                if (JSON.stringify(cachedParts) === JSON.stringify(parts)) {
                    return cachedParts;
                }
                arrayCache.put(jsonArr, parts);

                return parts;
            }
        };
    })
    .filter('truncate', function () {
        return function (text, length, end) {
            if (isNaN(length))
                length = 10;

            if (end === undefined)
                end = "...";

            if (text.length <= length || text.length - end.length <= length) {
                return text;
            }
            else {
                return String(text).substring(0, length-end.length) + end;
            }

        };
    });
