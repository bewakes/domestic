define(['angular', 'ngRoute', 'ngCookies'], function(angular) {
    var app = angular.module('expenses', ['ngRoute', 'ngCookies']);

    var appState = {
        error: '',
        identity: null,
        username: 'bibek',
    };

    app.value('appState', appState);

    config.$inject = ['$routeProvider', '$controllerProvider', '$provide', '$compileProvider', '$httpProvider', '$locationProvider'];
    app.config(config);

    function config($routeProvider, $controllerProvider, $provide, $compileProvider, $locationProvider) {

        app.register = {
            controller: $controllerProvider.register,
            factory: $provide.factory,
            directive: $compileProvider.directive
        };

        $routeProvider
            .when('/', resolve('home', 'home'))
            .when('/_=_', resolve('home', 'home')) // for social login redirect
            .when('/items', resolve('items', 'items')) // for social login redirect
//            .when('/login/', resolve('login', 'login'))
    }

    function resolve(controllername, templatename) {
        return {
            templateUrl: 'static/templates/'+templatename+'.html',
            controller: controllername+'Controller',
            resolve: {
                load: function($q, $rootScope) {
                    var deferred = $q.defer();
                    require(['controllers/'+controllername+'.controller'], function() {
                        $rootScope.$apply(deferred.resolve);
                    });
                    return deferred.promise;
                }
            }
        }
    }

    return app;
});
