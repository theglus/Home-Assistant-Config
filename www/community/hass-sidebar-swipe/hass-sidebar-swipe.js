!function(){var t=function(r,e){return t=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,r){t.__proto__=r}||function(t,r){for(var e in r)Object.prototype.hasOwnProperty.call(r,e)&&(t[e]=r[e])},t(r,e)};function r(r,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function n(){this.constructor=r}t(r,e),r.prototype=null===e?Object.create(e):(n.prototype=e.prototype,new n)}function e(t,r,e,n){return new(e||(e=Promise))((function(o,i){function u(t){try{s(n.next(t))}catch(t){i(t)}}function c(t){try{s(n.throw(t))}catch(t){i(t)}}function s(t){var r;t.done?o(t.value):(r=t.value,r instanceof e?r:new e((function(t){t(r)}))).then(u,c)}s((n=n.apply(t,r||[])).next())}))}function n(t,r){var e,n,o,i,u={label:0,sent:function(){if(1&o[0])throw o[1];return o[1]},trys:[],ops:[]};return i={next:c(0),throw:c(1),return:c(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function c(c){return function(s){return function(c){if(e)throw new TypeError("Generator is already executing.");for(;i&&(i=0,c[0]&&(u=0)),u;)try{if(e=1,n&&(o=2&c[0]?n.return:c[0]?n.throw||((o=n.return)&&o.call(n),0):n.next)&&!(o=o.call(n,c[1])).done)return o;switch(n=0,o&&(c=[2&c[0],o.value]),c[0]){case 0:case 1:o=c;break;case 4:return u.label++,{value:c[1],done:!1};case 5:u.label++,n=c[1],c=[0];continue;case 7:c=u.ops.pop(),u.trys.pop();continue;default:if(!(o=u.trys,(o=o.length>0&&o[o.length-1])||6!==c[0]&&2!==c[0])){u=0;continue}if(3===c[0]&&(!o||c[1]>o[0]&&c[1]<o[3])){u.label=c[1];break}if(6===c[0]&&u.label<o[1]){u.label=o[1],o=c;break}if(o&&u.label<o[2]){u.label=o[2],u.ops.push(c);break}o[2]&&u.ops.pop(),u.trys.pop();continue}c=r.call(t,u)}catch(t){c=[6,t],n=0}finally{e=o=0}if(5&c[0])throw c[1];return{value:c[0]?c[1]:void 0,done:!0}}([c,s])}}}Object.create;function o(t){var r="function"==typeof Symbol&&Symbol.iterator,e=r&&t[r],n=0;if(e)return e.call(t);if(t&&"number"==typeof t.length)return{next:function(){return t&&n>=t.length&&(t=void 0),{value:t&&t[n++],done:!t}}};throw new TypeError(r?"Object is not iterable.":"Symbol.iterator is not defined.")}function i(t,r){var e="function"==typeof Symbol&&t[Symbol.iterator];if(!e)return t;var n,o,i=e.call(t),u=[];try{for(;(void 0===r||r-- >0)&&!(n=i.next()).done;)u.push(n.value)}catch(t){o={error:t}}finally{try{n&&!n.done&&(e=i.return)&&e.call(i)}finally{if(o)throw o.error}}return u}function u(t,r,e){if(e||2===arguments.length)for(var n,o=0,i=r.length;o<i;o++)!n&&o in r||(n||(n=Array.prototype.slice.call(r,0,o)),n[o]=r[o]);return t.concat(n||Array.prototype.slice.call(r))}function c(t){return this instanceof c?(this.v=t,this):new c(t)}function s(t,r,e){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var n,o=e.apply(t,r||[]),i=[];return n={},u("next"),u("throw"),u("return"),n[Symbol.asyncIterator]=function(){return this},n;function u(t){o[t]&&(n[t]=function(r){return new Promise((function(e,n){i.push([t,r,e,n])>1||s(t,r)}))})}function s(t,r){try{(e=o[t](r)).value instanceof c?Promise.resolve(e.value.v).then(a,l):f(i[0][2],e)}catch(t){f(i[0][3],t)}var e}function a(t){s("next",t)}function l(t){s("throw",t)}function f(t,r){t(r),i.shift(),i.length&&s(i[0][0],i[0][1])}}function a(t){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var r,e=t[Symbol.asyncIterator];return e?e.call(t):(t=o(t),r={},n("next"),n("throw"),n("return"),r[Symbol.asyncIterator]=function(){return this},r);function n(e){r[e]=t[e]&&function(r){return new Promise((function(n,o){(function(t,r,e,n){Promise.resolve(n).then((function(r){t({value:r,done:e})}),r)})(n,o,(r=t[e](r)).done,r.value)}))}}}Object.create;function l(t){return"function"==typeof t}function f(t){var r=t((function(t){Error.call(t),t.stack=(new Error).stack}));return r.prototype=Object.create(Error.prototype),r.prototype.constructor=r,r}var p=f((function(t){return function(r){t(this),this.message=r?r.length+" errors occurred during unsubscription:\n"+r.map((function(t,r){return r+1+") "+t.toString()})).join("\n  "):"",this.name="UnsubscriptionError",this.errors=r}}));function h(t,r){if(t){var e=t.indexOf(r);0<=e&&t.splice(e,1)}}var v=function(){function t(t){this.initialTeardown=t,this.closed=!1,this._parentage=null,this._finalizers=null}var r;return t.prototype.unsubscribe=function(){var t,r,e,n,c;if(!this.closed){this.closed=!0;var s=this._parentage;if(s)if(this._parentage=null,Array.isArray(s))try{for(var a=o(s),f=a.next();!f.done;f=a.next()){f.value.remove(this)}}catch(r){t={error:r}}finally{try{f&&!f.done&&(r=a.return)&&r.call(a)}finally{if(t)throw t.error}}else s.remove(this);var h=this.initialTeardown;if(l(h))try{h()}catch(t){c=t instanceof p?t.errors:[t]}var v=this._finalizers;if(v){this._finalizers=null;try{for(var d=o(v),b=d.next();!b.done;b=d.next()){var m=b.value;try{y(m)}catch(t){c=null!=c?c:[],t instanceof p?c=u(u([],i(c)),i(t.errors)):c.push(t)}}}catch(t){e={error:t}}finally{try{b&&!b.done&&(n=d.return)&&n.call(d)}finally{if(e)throw e.error}}}if(c)throw new p(c)}},t.prototype.add=function(r){var e;if(r&&r!==this)if(this.closed)y(r);else{if(r instanceof t){if(r.closed||r._hasParent(this))return;r._addParent(this)}(this._finalizers=null!==(e=this._finalizers)&&void 0!==e?e:[]).push(r)}},t.prototype._hasParent=function(t){var r=this._parentage;return r===t||Array.isArray(r)&&r.includes(t)},t.prototype._addParent=function(t){var r=this._parentage;this._parentage=Array.isArray(r)?(r.push(t),r):r?[r,t]:t},t.prototype._removeParent=function(t){var r=this._parentage;r===t?this._parentage=null:Array.isArray(r)&&h(r,t)},t.prototype.remove=function(r){var e=this._finalizers;e&&h(e,r),r instanceof t&&r._removeParent(this)},t.EMPTY=((r=new t).closed=!0,r),t}(),d=v.EMPTY;function b(t){return t instanceof v||t&&"closed"in t&&l(t.remove)&&l(t.add)&&l(t.unsubscribe)}function y(t){l(t)?t():t.unsubscribe()}var m={onUnhandledError:null,onStoppedNotification:null,Promise:void 0,useDeprecatedSynchronousErrorHandling:!1,useDeprecatedNextContext:!1},w={setTimeout:function(t,r){for(var e=[],n=2;n<arguments.length;n++)e[n-2]=arguments[n];var o=w.delegate;return(null==o?void 0:o.setTimeout)?o.setTimeout.apply(o,u([t,r],i(e))):setTimeout.apply(void 0,u([t,r],i(e)))},clearTimeout:function(t){var r=w.delegate;return((null==r?void 0:r.clearTimeout)||clearTimeout)(t)},delegate:void 0};function _(t){w.setTimeout((function(){var r=m.onUnhandledError;if(!r)throw t;r(t)}))}function x(){}var g=E("C",void 0,void 0);function S(t){return E("N",t,void 0)}function E(t,r,e){return{kind:t,value:r,error:e}}var O=null;function T(t){if(m.useDeprecatedSynchronousErrorHandling){var r=!O;if(r&&(O={errorThrown:!1,error:null}),t(),r){var e=O,n=e.errorThrown,o=e.error;if(O=null,n)throw o}}else t()}var P=function(t){function e(r){var e=t.call(this)||this;return e.isStopped=!1,r?(e.destination=r,b(r)&&r.add(e)):e.destination=L,e}return r(e,t),e.create=function(t,r,e){return new A(t,r,e)},e.prototype.next=function(t){this.isStopped?z(S(t),this):this._next(t)},e.prototype.error=function(t){this.isStopped?z(E("E",void 0,t),this):(this.isStopped=!0,this._error(t))},e.prototype.complete=function(){this.isStopped?z(g,this):(this.isStopped=!0,this._complete())},e.prototype.unsubscribe=function(){this.closed||(this.isStopped=!0,t.prototype.unsubscribe.call(this),this.destination=null)},e.prototype._next=function(t){this.destination.next(t)},e.prototype._error=function(t){try{this.destination.error(t)}finally{this.unsubscribe()}},e.prototype._complete=function(){try{this.destination.complete()}finally{this.unsubscribe()}},e}(v),j=Function.prototype.bind;function I(t,r){return j.call(t,r)}var k=function(){function t(t){this.partialObserver=t}return t.prototype.next=function(t){var r=this.partialObserver;if(r.next)try{r.next(t)}catch(t){C(t)}},t.prototype.error=function(t){var r=this.partialObserver;if(r.error)try{r.error(t)}catch(t){C(t)}else C(t)},t.prototype.complete=function(){var t=this.partialObserver;if(t.complete)try{t.complete()}catch(t){C(t)}},t}(),A=function(t){function e(r,e,n){var o,i,u=t.call(this)||this;l(r)||!r?o={next:null!=r?r:void 0,error:null!=e?e:void 0,complete:null!=n?n:void 0}:u&&m.useDeprecatedNextContext?((i=Object.create(r)).unsubscribe=function(){return u.unsubscribe()},o={next:r.next&&I(r.next,i),error:r.error&&I(r.error,i),complete:r.complete&&I(r.complete,i)}):o=r;return u.destination=new k(o),u}return r(e,t),e}(P);function C(t){var r;m.useDeprecatedSynchronousErrorHandling?(r=t,m.useDeprecatedSynchronousErrorHandling&&O&&(O.errorThrown=!0,O.error=r)):_(t)}function z(t,r){var e=m.onStoppedNotification;e&&w.setTimeout((function(){return e(t,r)}))}var L={closed:!0,next:x,error:function(t){throw t},complete:x},U="function"==typeof Symbol&&Symbol.observable||"@@observable";function D(t){return t}function F(t){return 0===t.length?D:1===t.length?t[0]:function(r){return t.reduce((function(t,r){return r(t)}),r)}}var V=function(){function t(t){t&&(this._subscribe=t)}return t.prototype.lift=function(r){var e=new t;return e.source=this,e.operator=r,e},t.prototype.subscribe=function(t,r,e){var n,o=this,i=(n=t)&&n instanceof P||function(t){return t&&l(t.next)&&l(t.error)&&l(t.complete)}(n)&&b(n)?t:new A(t,r,e);return T((function(){var t=o,r=t.operator,e=t.source;i.add(r?r.call(i,e):e?o._subscribe(i):o._trySubscribe(i))})),i},t.prototype._trySubscribe=function(t){try{return this._subscribe(t)}catch(r){t.error(r)}},t.prototype.forEach=function(t,r){var e=this;return new(r=Y(r))((function(r,n){var o=new A({next:function(r){try{t(r)}catch(t){n(t),o.unsubscribe()}},error:n,complete:r});e.subscribe(o)}))},t.prototype._subscribe=function(t){var r;return null===(r=this.source)||void 0===r?void 0:r.subscribe(t)},t.prototype[U]=function(){return this},t.prototype.pipe=function(){for(var t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];return F(t)(this)},t.prototype.toPromise=function(t){var r=this;return new(t=Y(t))((function(t,e){var n;r.subscribe((function(t){return n=t}),(function(t){return e(t)}),(function(){return t(n)}))}))},t.create=function(r){return new t(r)},t}();function Y(t){var r;return null!==(r=null!=t?t:m.Promise)&&void 0!==r?r:Promise}var M=f((function(t){return function(){t(this),this.name="ObjectUnsubscribedError",this.message="object unsubscribed"}})),N=function(t){function e(){var r=t.call(this)||this;return r.closed=!1,r.currentObservers=null,r.observers=[],r.isStopped=!1,r.hasError=!1,r.thrownError=null,r}return r(e,t),e.prototype.lift=function(t){var r=new H(this,this);return r.operator=t,r},e.prototype._throwIfClosed=function(){if(this.closed)throw new M},e.prototype.next=function(t){var r=this;T((function(){var e,n;if(r._throwIfClosed(),!r.isStopped){r.currentObservers||(r.currentObservers=Array.from(r.observers));try{for(var i=o(r.currentObservers),u=i.next();!u.done;u=i.next()){u.value.next(t)}}catch(t){e={error:t}}finally{try{u&&!u.done&&(n=i.return)&&n.call(i)}finally{if(e)throw e.error}}}}))},e.prototype.error=function(t){var r=this;T((function(){if(r._throwIfClosed(),!r.isStopped){r.hasError=r.isStopped=!0,r.thrownError=t;for(var e=r.observers;e.length;)e.shift().error(t)}}))},e.prototype.complete=function(){var t=this;T((function(){if(t._throwIfClosed(),!t.isStopped){t.isStopped=!0;for(var r=t.observers;r.length;)r.shift().complete()}}))},e.prototype.unsubscribe=function(){this.isStopped=this.closed=!0,this.observers=this.currentObservers=null},Object.defineProperty(e.prototype,"observed",{get:function(){var t;return(null===(t=this.observers)||void 0===t?void 0:t.length)>0},enumerable:!1,configurable:!0}),e.prototype._trySubscribe=function(r){return this._throwIfClosed(),t.prototype._trySubscribe.call(this,r)},e.prototype._subscribe=function(t){return this._throwIfClosed(),this._checkFinalizedStatuses(t),this._innerSubscribe(t)},e.prototype._innerSubscribe=function(t){var r=this,e=this,n=e.hasError,o=e.isStopped,i=e.observers;return n||o?d:(this.currentObservers=null,i.push(t),new v((function(){r.currentObservers=null,h(i,t)})))},e.prototype._checkFinalizedStatuses=function(t){var r=this,e=r.hasError,n=r.thrownError,o=r.isStopped;e?t.error(n):o&&t.complete()},e.prototype.asObservable=function(){var t=new V;return t.source=this,t},e.create=function(t,r){return new H(t,r)},e}(V),H=function(t){function e(r,e){var n=t.call(this)||this;return n.destination=r,n.source=e,n}return r(e,t),e.prototype.next=function(t){var r,e;null===(e=null===(r=this.destination)||void 0===r?void 0:r.next)||void 0===e||e.call(r,t)},e.prototype.error=function(t){var r,e;null===(e=null===(r=this.destination)||void 0===r?void 0:r.error)||void 0===e||e.call(r,t)},e.prototype.complete=function(){var t,r;null===(r=null===(t=this.destination)||void 0===t?void 0:t.complete)||void 0===r||r.call(t)},e.prototype._subscribe=function(t){var r,e;return null!==(e=null===(r=this.source)||void 0===r?void 0:r.subscribe(t))&&void 0!==e?e:d},e}(N),R=function(t){function e(r){var e=t.call(this)||this;return e._value=r,e}return r(e,t),Object.defineProperty(e.prototype,"value",{get:function(){return this.getValue()},enumerable:!1,configurable:!0}),e.prototype._subscribe=function(r){var e=t.prototype._subscribe.call(this,r);return!e.closed&&r.next(this._value),e},e.prototype.getValue=function(){var t=this,r=t.hasError,e=t.thrownError,n=t._value;if(r)throw e;return this._throwIfClosed(),n},e.prototype.next=function(r){t.prototype.next.call(this,this._value=r)},e}(N),X=function(t){return t&&"number"==typeof t.length&&"function"!=typeof t};function q(t){return l(t[U])}function G(t){return Symbol.asyncIterator&&l(null==t?void 0:t[Symbol.asyncIterator])}function W(t){return new TypeError("You provided "+(null!==t&&"object"==typeof t?"an invalid object":"'"+t+"'")+" where a stream was expected. You can provide an Observable, Promise, ReadableStream, Array, AsyncIterable, or Iterable.")}var $="function"==typeof Symbol&&Symbol.iterator?Symbol.iterator:"@@iterator";function B(t){return l(null==t?void 0:t[$])}function J(t){return l(null==t?void 0:t.getReader)}function K(t){if(t instanceof V)return t;if(null!=t){if(q(t))return a=t,new V((function(t){var r=a[U]();if(l(r.subscribe))return r.subscribe(t);throw new TypeError("Provided object does not correctly implement Symbol.observable")}));if(X(t))return u=t,new V((function(t){for(var r=0;r<u.length&&!t.closed;r++)t.next(u[r]);t.complete()}));if(l(null==(i=t)?void 0:i.then))return e=t,new V((function(t){e.then((function(r){t.closed||(t.next(r),t.complete())}),(function(r){return t.error(r)})).then(null,_)}));if(G(t))return Q(t);if(B(t))return r=t,new V((function(t){var e,n;try{for(var i=o(r),u=i.next();!u.done;u=i.next()){var c=u.value;if(t.next(c),t.closed)return}}catch(t){e={error:t}}finally{try{u&&!u.done&&(n=i.return)&&n.call(i)}finally{if(e)throw e.error}}t.complete()}));if(J(t))return Q(function(t){return s(this,arguments,(function(){var r,e,o;return n(this,(function(n){switch(n.label){case 0:r=t.getReader(),n.label=1;case 1:n.trys.push([1,,9,10]),n.label=2;case 2:return[4,c(r.read())];case 3:return e=n.sent(),o=e.value,e.done?[4,c(void 0)]:[3,5];case 4:return[2,n.sent()];case 5:return[4,c(o)];case 6:return[4,n.sent()];case 7:return n.sent(),[3,2];case 8:return[3,10];case 9:return r.releaseLock(),[7];case 10:return[2]}}))}))}(t))}var r,e,i,u,a;throw W(t)}function Q(t){return new V((function(r){(function(t,r){var o,i,u,c;return e(this,void 0,void 0,(function(){var e,s;return n(this,(function(n){switch(n.label){case 0:n.trys.push([0,5,6,11]),o=a(t),n.label=1;case 1:return[4,o.next()];case 2:if((i=n.sent()).done)return[3,4];if(e=i.value,r.next(e),r.closed)return[2];n.label=3;case 3:return[3,1];case 4:return[3,11];case 5:return s=n.sent(),u={error:s},[3,11];case 6:return n.trys.push([6,,9,10]),i&&!i.done&&(c=o.return)?[4,c.call(o)]:[3,8];case 7:n.sent(),n.label=8;case 8:return[3,10];case 9:if(u)throw u.error;return[7];case 10:return[7];case 11:return r.complete(),[2]}}))}))})(t,r).catch((function(t){return r.error(t)}))}))}function Z(t){return function(r){if(function(t){return l(null==t?void 0:t.lift)}(r))return r.lift((function(r){try{return t(r,this)}catch(t){this.error(t)}}));throw new TypeError("Unable to lift unknown Observable type")}}function tt(t,r,e,n,o){return new rt(t,r,e,n,o)}var rt=function(t){function e(r,e,n,o,i,u){var c=t.call(this,r)||this;return c.onFinalize=i,c.shouldUnsubscribe=u,c._next=e?function(t){try{e(t)}catch(t){r.error(t)}}:t.prototype._next,c._error=o?function(t){try{o(t)}catch(t){r.error(t)}finally{this.unsubscribe()}}:t.prototype._error,c._complete=n?function(){try{n()}catch(t){r.error(t)}finally{this.unsubscribe()}}:t.prototype._complete,c}return r(e,t),e.prototype.unsubscribe=function(){var r;if(!this.shouldUnsubscribe||this.shouldUnsubscribe()){var e=this.closed;t.prototype.unsubscribe.call(this),!e&&(null===(r=this.onFinalize)||void 0===r||r.call(this))}},e}(P);function et(t,r){return Z((function(e,n){var o=null,i=0,u=!1,c=function(){return u&&!o&&n.complete()};e.subscribe(tt(n,(function(e){null==o||o.unsubscribe();var u=0,s=i++;K(t(e,s)).subscribe(o=tt(n,(function(t){return n.next(r?r(e,t,s,u++):t)}),(function(){o=null,c()})))}),(function(){u=!0,c()})))}))}function nt(t,r,e){var n=l(t)||r||e?{next:t,error:r,complete:e}:t;return n?Z((function(t,r){var e;null===(e=n.subscribe)||void 0===e||e.call(n);var o=!0;t.subscribe(tt(r,(function(t){var e;null===(e=n.next)||void 0===e||e.call(n,t),r.next(t)}),(function(){var t;o=!1,null===(t=n.complete)||void 0===t||t.call(n),r.complete()}),(function(t){var e;o=!1,null===(e=n.error)||void 0===e||e.call(n,t),r.error(t)}),(function(){var t,r;o&&(null===(t=n.unsubscribe)||void 0===t||t.call(n)),null===(r=n.finalize)||void 0===r||r.call(n)})))})):D}function ot(t,r){return Z((function(e,n){var o=0;e.subscribe(tt(n,(function(e){return t.call(r,e,o++)&&n.next(e)})))}))}function it(t,r){return Z((function(e,n){var o=0;e.subscribe(tt(n,(function(e){n.next(t.call(r,e,o++))})))}))}function ut(t,r,e,n,o){void 0===n&&(n=0),void 0===o&&(o=!1);var i=r.schedule((function(){e(),o?t.add(this.schedule(null,n)):this.unsubscribe()}),n);if(t.add(i),!o)return i}function ct(t,r,e,n,o,i,u,c){var s=[],a=0,l=0,f=!1,p=function(){!f||s.length||a||r.complete()},h=function(t){return a<n?v(t):s.push(t)},v=function(t){i&&r.next(t),a++;var c=!1;K(e(t,l++)).subscribe(tt(r,(function(t){null==o||o(t),i?h(t):r.next(t)}),(function(){c=!0}),void 0,(function(){if(c)try{a--;for(var t=function(){var t=s.shift();u?ut(r,u,(function(){return v(t)})):v(t)};s.length&&a<n;)t();p()}catch(t){r.error(t)}})))};return t.subscribe(tt(r,h,(function(){f=!0,p()}))),function(){null==c||c()}}function st(t,r,e){return void 0===e&&(e=1/0),l(r)?st((function(e,n){return it((function(t,o){return r(e,t,n,o)}))(K(t(e,n)))}),e):("number"==typeof r&&(e=r),Z((function(r,n){return ct(r,n,t,e)})))}var at=Array.isArray;function lt(t){return it((function(r){return function(t,r){return at(r)?t.apply(void 0,u([],i(r))):t(r)}(t,r)}))}var ft=["addListener","removeListener"],pt=["addEventListener","removeEventListener"],ht=["on","off"];function vt(t,r,e,n){if(l(e)&&(n=e,e=void 0),n)return vt(t,r,e).pipe(lt(n));var o=i(function(t){return l(t.addEventListener)&&l(t.removeEventListener)}(t)?pt.map((function(n){return function(o){return t[n](r,o,e)}})):function(t){return l(t.addListener)&&l(t.removeListener)}(t)?ft.map(dt(t,r)):function(t){return l(t.on)&&l(t.off)}(t)?ht.map(dt(t,r)):[],2),u=o[0],c=o[1];if(!u&&X(t))return st((function(t){return vt(t,r,e)}))(K(t));if(!u)throw new TypeError("Invalid event target");return new V((function(t){var r=function(){for(var r=[],e=0;e<arguments.length;e++)r[e]=arguments[e];return t.next(1<r.length?r:r[0])};return u(r),function(){return c(r)}}))}function dt(t,r){return function(e){return function(n){return t[e](r,n)}}}var bt=new V((function(t){return t.complete()}));function yt(t){return t<=0?function(){return bt}:Z((function(r,e){var n=0;r.subscribe(tt(e,(function(r){++n<=t&&(e.next(r),t<=n&&e.complete())})))}))}function mt(t,r=document){if(null===r)return null;const e=String(t).split(">>>");let n=r;return e.find(((t,o)=>(0===o?n=r.querySelector(e[o]):n instanceof Element&&(n=n?.shadowRoot?.querySelector(e[o])),null===n))),n===r?null:n}function wt(t){return t>1?t:window.innerWidth*t}const _t={haPanelEnergy:{onLock:()=>{const t=mt("home-assistant >>> home-assistant-main >>> ha-drawer ha-panel-energy >>> ha-top-app-bar-fixed >>> header");t&&(t.style.top="0px")}}};function xt(){const t=Math.abs(parseInt(document.body.style.top))||document.documentElement.scrollTop;Object.assign(document.body.style,{position:"",inset:""}),window.scrollTo({top:t,left:0,behavior:"auto"}),Object.values(_t).forEach((({onUnlock:t})=>t?.()))}const gt=({startThreshold:t,endThreshold:r,preventOthers:e,lockVerticalScroll:n})=>vt(document,"touchstart",{capture:e}).pipe(ot((({touches:[{clientX:r}]})=>r<wt(t))),nt((t=>{n&&(Object.assign(document.body.style,{position:"fixed",inset:0,top:`-${document.documentElement.scrollTop}px`}),Object.values(_t).forEach((({onLock:t})=>t?.()))),e&&t.stopPropagation()})),et((({touches:[{clientY:t}]})=>vt(document,"touchend").pipe(yt(1),ot((({changedTouches:[{clientX:e,clientY:o}]})=>{const i=e>Math.abs(o-t)&&e>wt(r);return n&&!i&&xt(),i})),it((t=>({open:!0,event:t}))))))),St=({preventOthers:t,threshold:r})=>vt(document,"touchstart").pipe(nt((r=>t&&r.stopPropagation())),et((({touches:[{clientX:t}]})=>vt(document,"touchend").pipe(yt(1),ot((({changedTouches:[{clientX:e}]})=>t-e>wt(r))),it((t=>({open:!1,event:t}))))))),Et=mt("home-assistant >>> home-assistant-main >>> ha-drawer"),Ot=mt("ha-sidebar",Et),Tt=mt("ha-panel-lovelace",Et),{start_threshold:Pt=.1,end_threshold:jt=.13,back_threshold:It=50,prevent_others:kt=!0,lock_vertical_scroll:At=!0,check_visibility:Ct=!0}=Tt?.lovelace?.config?.sidebar_swipe||{};if(!Ct||Ot&&"none"!==getComputedStyle(Ot).display){const t=new R(!1),r=St({threshold:It,preventOthers:kt}),e=gt({startThreshold:Pt,endThreshold:jt,preventOthers:kt,lockVerticalScroll:At});Et&&new MutationObserver((r=>{t.next(null===r[0].oldValue)})).observe(Et,{attributes:!0,attributeOldValue:!0,attributeFilter:["open"]}),t.pipe(nt((t=>At&&!t&&xt())),et((t=>t?r:e))).subscribe((({open:t})=>{mt("home-assistant >>> home-assistant-main")?.dispatchEvent(new CustomEvent("hass-toggle-menu",{detail:{open:t}}))}))}}();