/**
 * Created on Nov 23, 2013
 * Other contributers:
 */

getdeal.filter('ago', function() {
  return function(input) {
    return moment(input).fromNow();
  };
});
