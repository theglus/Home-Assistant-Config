"use strict";(self.webpackChunkhacs_frontend=self.webpackChunkhacs_frontend||[]).push([[3945],{58445:function(t,e,i){i.d(e,{H:function(){return r}});var a=i(33994),n=i(22858),r=(i(71499),i(95737),i(97741),i(39790),i(66457),i(99019),i(16891),i(96858),function(){var t=(0,n.A)((0,a.A)().mark((function t(e){var n,r,s,l;return(0,a.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(e.parentNode){t.next=2;break}throw new Error("Cannot setup Leaflet map on disconnected element");case 2:return t.next=4,Promise.all([i.e(5458),i.e(4066)]).then(i.t.bind(i,44066,23));case 4:return(n=t.sent.default).Icon.Default.imagePath="/static/images/leaflet/images/",r=n.map(e),(s=document.createElement("link")).setAttribute("href","/static/images/leaflet/leaflet.css"),s.setAttribute("rel","stylesheet"),e.parentNode.appendChild(s),r.setView([52.3731339,4.8903147],13),l=o(n).addTo(r),t.abrupt("return",[r,n,l]);case 14:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}()),o=function(t){return t.tileLayer("https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}".concat(t.Browser.retina?"@2x.png":".png"),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})}},79662:function(t,e,i){var a,n,r=i(64599),o=i(35806),s=i(71008),l=i(62193),d=i(2816),u=i(27927),c=(i(81027),i(66360)),h=i(29818);(0,u.A)([(0,h.EM)("ha-input-helper-text")],(function(t,e){var i=function(e){function i(){var e;(0,s.A)(this,i);for(var a=arguments.length,n=new Array(a),r=0;r<a;r++)n[r]=arguments[r];return e=(0,l.A)(this,i,[].concat(n)),t(e),e}return(0,d.A)(i,e),(0,o.A)(i)}(e);return{F:i,d:[{kind:"method",key:"render",value:function(){return(0,c.qy)(a||(a=(0,r.A)(["<slot></slot>"])))}},{kind:"field",static:!0,key:"styles",value:function(){return(0,c.AH)(n||(n=(0,r.A)([":host{display:block;color:var(--mdc-text-field-label-ink-color,rgba(0,0,0,.6));font-size:.75rem;padding-left:16px;padding-right:16px;padding-inline-start:16px;padding-inline-end:16px}"])))}}]}}),c.WF)},1328:function(t,e,i){var a=i(22858).A,n=i(33994).A;i.a(t,function(){var t=a(n().mark((function t(a,r){var o,s,l,d,u,c,h,f,p,v,m,k,y,g,b,_,M,A,x,w;return n().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,i.r(e),i.d(e,{HaLocationSelector:function(){return w}}),o=i(658),s=i(64599),l=i(41981),d=i(35806),u=i(71008),c=i(62193),h=i(2816),f=i(27927),p=i(81027),i.n(p),v=i(50693),i.n(v),m=i(26098),i.n(m),k=i(66360),y=i(29818),g=i(94100),b=i(50880),_=i(81656),i(88606),!(M=a([_])).then){t.next=31;break}return t.next=27,M;case 27:t.t1=t.sent,t.t0=(0,t.t1)(),t.next=32;break;case 31:t.t0=M;case 32:_=t.t0[0],w=(0,f.A)([(0,y.EM)("ha-selector-location")],(function(t,e){var i=function(e){function i(){var e;(0,u.A)(this,i);for(var a=arguments.length,n=new Array(a),r=0;r<a;r++)n[r]=arguments[r];return e=(0,c.A)(this,i,[].concat(n)),t(e),e}return(0,h.A)(i,e),(0,d.A)(i)}(e);return{F:i,d:[{kind:"field",decorators:[(0,y.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,y.MZ)({type:Object})],key:"value",value:void 0},{kind:"field",decorators:[(0,y.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,y.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:function(){return!1}},{kind:"field",key:"_schema",value:function(){return(0,g.A)((function(t,e){return[{name:"",type:"grid",schema:[{name:"latitude",required:!0,selector:{number:{step:"any"}}},{name:"longitude",required:!0,selector:{number:{step:"any"}}}]}].concat((0,l.A)(t?[{name:"radius",required:!0,default:1e3,disabled:!!e,selector:{number:{min:0,step:1,mode:"box"}}}]:[]))}))}},{kind:"method",key:"willUpdate",value:function(){var t;this.value||(this.value={latitude:this.hass.config.latitude,longitude:this.hass.config.longitude,radius:null!==(t=this.selector.location)&&void 0!==t&&t.radius?1e3:void 0})}},{kind:"method",key:"render",value:function(){var t,e;return(0,k.qy)(A||(A=(0,s.A)([" <p>",'</p> <ha-locations-editor class="flex" .hass="','" .helper="','" .locations="','" @location-updated="','" @radius-updated="','"></ha-locations-editor> <ha-form .hass="','" .schema="','" .data="','" .computeLabel="','" .disabled="','" @value-changed="','"></ha-form> '])),this.label?this.label:"",this.hass,this.helper,this._location(this.selector,this.value),this._locationChanged,this._radiusChanged,this.hass,this._schema(null===(t=this.selector.location)||void 0===t?void 0:t.radius,null===(e=this.selector.location)||void 0===e?void 0:e.radius_readonly),this.value,this._computeLabel,this.disabled,this._valueChanged)}},{kind:"field",key:"_location",value:function(){var t=this;return(0,g.A)((function(e,i){var a,n,r,o,s,l,d=getComputedStyle(t),u=null!==(a=e.location)&&void 0!==a&&a.radius?d.getPropertyValue("--zone-radius-color")||d.getPropertyValue("--accent-color"):void 0;return[{id:"location",latitude:!i||isNaN(i.latitude)?t.hass.config.latitude:i.latitude,longitude:!i||isNaN(i.longitude)?t.hass.config.longitude:i.longitude,radius:null!==(n=e.location)&&void 0!==n&&n.radius?(null==i?void 0:i.radius)||1e3:void 0,radius_color:u,icon:null!==(r=e.location)&&void 0!==r&&r.icon||null!==(o=e.location)&&void 0!==o&&o.radius?"mdi:map-marker-radius":"mdi:map-marker",location_editable:!0,radius_editable:!(null===(s=e.location)||void 0===s||!s.radius||null!==(l=e.location)&&void 0!==l&&l.radius_readonly)}]}))}},{kind:"method",key:"_locationChanged",value:function(t){var e=(0,o.A)(t.detail.location,2),i=e[0],a=e[1];(0,b.r)(this,"value-changed",{value:Object.assign(Object.assign({},this.value),{},{latitude:i,longitude:a})})}},{kind:"method",key:"_radiusChanged",value:function(t){var e=Math.round(t.detail.radius);(0,b.r)(this,"value-changed",{value:Object.assign(Object.assign({},this.value),{},{radius:e})})}},{kind:"method",key:"_valueChanged",value:function(t){var e,i;t.stopPropagation();var a=t.detail.value,n=Math.round(t.detail.value.radius);(0,b.r)(this,"value-changed",{value:Object.assign({latitude:a.latitude,longitude:a.longitude},null===(e=this.selector.location)||void 0===e||!e.radius||null!==(i=this.selector.location)&&void 0!==i&&i.radius_readonly?{}:{radius:n})})}},{kind:"field",key:"_computeLabel",value:function(){var t=this;return function(e){return t.hass.localize("ui.components.selectors.location.".concat(e.name))}}},{kind:"field",static:!0,key:"styles",value:function(){return(0,k.AH)(x||(x=(0,s.A)(["ha-locations-editor{display:block;height:400px;margin-bottom:16px}p{margin-top:0}"])))}}]}}),k.WF),r(),t.next=40;break;case 37:t.prev=37,t.t2=t.catch(0),r(t.t2);case 40:case"end":return t.stop()}}),t,null,[[0,37]])})));return function(e,i){return t.apply(this,arguments)}}())},40168:function(t,e,i){var a,n,r,o=i(64599),s=i(35806),l=i(71008),d=i(62193),u=i(2816),c=i(27927),h=(i(81027),i(66360)),f=i(29818),p=i(31225),v=i(50880),m=(0,c.A)(null,(function(t,e){var i=function(e){function i(){var e;(0,l.A)(this,i);for(var a=arguments.length,n=new Array(a),r=0;r<a;r++)n[r]=arguments[r];return e=(0,d.A)(this,i,[].concat(n)),t(e),e}return(0,u.A)(i,e),(0,s.A)(i)}(e);return{F:i,d:[{kind:"field",decorators:[(0,f.MZ)({attribute:"entity-id"})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,f.MZ)({attribute:"entity-name"})],key:"entityName",value:void 0},{kind:"field",decorators:[(0,f.MZ)({attribute:"entity-picture"})],key:"entityPicture",value:void 0},{kind:"field",decorators:[(0,f.MZ)({attribute:"entity-color"})],key:"entityColor",value:void 0},{kind:"method",key:"render",value:function(){return(0,h.qy)(a||(a=(0,o.A)([' <div class="marker ','" style="','" @click="','"> '," </div> "])),this.entityPicture?"picture":"",(0,p.W)({"border-color":this.entityColor}),this._badgeTap,this.entityPicture?(0,h.qy)(n||(n=(0,o.A)(['<div class="entity-picture" style="','"></div>'])),(0,p.W)({"background-image":"url(".concat(this.entityPicture,")")})):this.entityName)}},{kind:"method",key:"_badgeTap",value:function(t){t.stopPropagation(),this.entityId&&(0,v.r)(this,"hass-more-info",{entityId:this.entityId})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,h.AH)(r||(r=(0,o.A)([".marker{display:flex;justify-content:center;align-items:center;box-sizing:border-box;width:48px;height:48px;font-size:var(--ha-marker-font-size, 1.5em);border-radius:var(--ha-marker-border-radius,50%);border:1px solid var(--ha-marker-color,var(--primary-color));color:var(--primary-text-color);background-color:var(--card-background-color)}.marker.picture{overflow:hidden}.entity-picture{background-size:cover;height:100%;width:100%}"])))}}]}}),h.WF);customElements.define("ha-entity-marker",m)},81656:function(t,e,i){var a=i(22858).A,n=i(33994).A;i.a(t,function(){var t=a(n().mark((function t(e,a){var r,o,s,l,d,u,c,h,f,p,v,m,k,y,g,b,_,M,A,x,w,L,Z,z,P,E,O,C,I,B,F,S,N,T,j;return n().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,r=i(64599),o=i(33994),s=i(22858),l=i(35806),d=i(71008),u=i(62193),c=i(2816),h=i(27927),f=i(14562),p=i(19867),v=i(13025),i.n(v),m=i(95737),i.n(m),k=i(97741),i.n(k),y=i(89655),i.n(y),g=i(50693),i.n(g),b=i(29193),i.n(b),_=i(39790),i.n(_),M=i(9241),i.n(M),A=i(66457),i.n(A),x=i(99019),i.n(x),w=i(253),i.n(w),L=i(2075),i.n(L),Z=i(54846),i.n(Z),z=i(16891),i.n(z),P=i(66555),i.n(P),E=i(96858),i.n(E),O=i(66360),C=i(29818),I=i(94100),B=i(50880),i(79662),F=i(7437),!(S=e([F])).then){t.next=57;break}return t.next=53,S;case 53:t.t1=t.sent,t.t0=(0,t.t1)(),t.next=58;break;case 57:t.t0=S;case 58:F=t.t0[0],(0,h.A)([(0,C.EM)("ha-locations-editor")],(function(t,e){var a,n=function(e){function a(){var e;return(0,d.A)(this,a),e=(0,u.A)(this,a),t(e),e._loadPromise=Promise.all([i.e(5458),i.e(4066)]).then(i.t.bind(i,44066,23)).then((function(t){return i.e(3874).then(i.t.bind(i,3874,23)).then((function(){return e.Leaflet=t.default,e._updateMarkers(),e.updateComplete.then((function(){return e.fitMap()}))}))})),e}return(0,c.A)(a,e),(0,l.A)(a)}(e);return{F:n,d:[{kind:"field",decorators:[(0,C.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,C.MZ)({attribute:!1})],key:"locations",value:void 0},{kind:"field",decorators:[(0,C.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,C.MZ)({type:Boolean})],key:"autoFit",value:function(){return!1}},{kind:"field",decorators:[(0,C.MZ)({type:Number})],key:"zoom",value:function(){return 16}},{kind:"field",decorators:[(0,C.MZ)({attribute:"theme-mode",type:String})],key:"themeMode",value:function(){return"auto"}},{kind:"field",decorators:[(0,C.wk)()],key:"_locationMarkers",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_circles",value:function(){return{}}},{kind:"field",decorators:[(0,C.P)("ha-map",!0)],key:"map",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_loadPromise",value:void 0},{kind:"method",key:"fitMap",value:function(t){this.map.fitMap(t)}},{kind:"method",key:"fitBounds",value:function(t,e){this.map.fitBounds(t,e)}},{kind:"method",key:"fitMarker",value:(a=(0,s.A)((0,o.A)().mark((function t(e,i){var a,n;return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(this.Leaflet){t.next=3;break}return t.next=3,this._loadPromise;case 3:if(this.map.leafletMap&&this._locationMarkers){t.next=5;break}return t.abrupt("return");case 5:if(a=this._locationMarkers[e]){t.next=8;break}return t.abrupt("return");case 8:"getBounds"in a?(this.map.leafletMap.fitBounds(a.getBounds()),a.bringToFront()):(n=this._circles[e])?this.map.leafletMap.fitBounds(n.getBounds()):this.map.leafletMap.setView(a.getLatLng(),(null==i?void 0:i.zoom)||this.zoom);case 9:case"end":return t.stop()}}),t,this)}))),function(t,e){return a.apply(this,arguments)})},{kind:"method",key:"render",value:function(){return(0,O.qy)(N||(N=(0,r.A)([' <ha-map .hass="','" .layers="','" .zoom="','" .autoFit="','" .themeMode="','"></ha-map> '," "])),this.hass,this._getLayers(this._circles,this._locationMarkers),this.zoom,this.autoFit,this.themeMode,this.helper?(0,O.qy)(T||(T=(0,r.A)(["<ha-input-helper-text>","</ha-input-helper-text>"])),this.helper):"")}},{kind:"field",key:"_getLayers",value:function(){return(0,I.A)((function(t,e){var i=[];return Array.prototype.push.apply(i,Object.values(t)),e&&Array.prototype.push.apply(i,Object.values(e)),i}))}},{kind:"method",key:"willUpdate",value:function(t){(0,f.A)((0,p.A)(n.prototype),"willUpdate",this).call(this,t),this.Leaflet&&t.has("locations")&&this._updateMarkers()}},{kind:"method",key:"updated",value:function(t){var e=this;if(this.Leaflet&&t.has("locations")){var i,a,n=t.get("locations"),r=null===(i=this.locations)||void 0===i?void 0:i.filter((function(t,i){var a,r;return!n[i]||(t.latitude!==n[i].latitude||t.longitude!==n[i].longitude)&&(null===(a=e.map.leafletMap)||void 0===a?void 0:a.getBounds().contains({lat:n[i].latitude,lng:n[i].longitude}))&&!(null!==(r=e.map.leafletMap)&&void 0!==r&&r.getBounds().contains({lat:t.latitude,lng:t.longitude}))}));if(1===(null==r?void 0:r.length))null===(a=this.map.leafletMap)||void 0===a||a.panTo({lat:r[0].latitude,lng:r[0].longitude})}}},{kind:"method",key:"_updateLocation",value:function(t){var e=t.target,i=e.getLatLng(),a=i.lng;Math.abs(a)>180&&(a=(a%360+540)%360-180);var n=[i.lat,a];(0,B.r)(this,"location-updated",{id:e.id,location:n},{bubbles:!1})}},{kind:"method",key:"_updateRadius",value:function(t){var e=t.target,i=this._locationMarkers[e.id];(0,B.r)(this,"radius-updated",{id:e.id,radius:i.getRadius()},{bubbles:!1})}},{kind:"method",key:"_markerClicked",value:function(t){var e=t.target;(0,B.r)(this,"marker-clicked",{id:e.id},{bubbles:!1})}},{kind:"method",key:"_updateMarkers",value:function(){var t=this;if(!this.locations||!this.locations.length)return this._circles={},void(this._locationMarkers=void 0);var e={},i={},a=getComputedStyle(this).getPropertyValue("--accent-color");this.locations.forEach((function(n){var r;if(n.icon||n.iconPath){var o,s=document.createElement("div");s.className="named-icon",void 0!==n.name&&(s.innerText=n.name),n.icon?(o=document.createElement("ha-icon")).setAttribute("icon",n.icon):(o=document.createElement("ha-svg-icon")).setAttribute("path",n.iconPath),s.prepend(o),r=t.Leaflet.divIcon({html:s.outerHTML,iconSize:[24,24],className:"light"})}if(n.radius){var l=t.Leaflet.circle([n.latitude,n.longitude],{color:n.radius_color||a,radius:n.radius});n.radius_editable||n.location_editable?(l.editing.enable(),l.addEventListener("add",(function(){var e=l.editing._moveMarker,i=l.editing._resizeMarkers[0];r&&e.setIcon(r),i.id=e.id=n.id,e.addEventListener("dragend",(function(e){return t._updateLocation(e)})).addEventListener("click",(function(e){return t._markerClicked(e)})),n.radius_editable?i.addEventListener("dragend",(function(e){return t._updateRadius(e)})):i.remove()})),e[n.id]=l):i[n.id]=l}if(!n.radius||!n.radius_editable&&!n.location_editable){var d={title:n.name,draggable:n.location_editable};r&&(d.icon=r);var u=t.Leaflet.marker([n.latitude,n.longitude],d).addEventListener("dragend",(function(e){return t._updateLocation(e)})).addEventListener("click",(function(e){return t._markerClicked(e)}));u.id=n.id,e[n.id]=u}})),this._circles=i,this._locationMarkers=e,(0,B.r)(this,"markers-updated")}},{kind:"get",static:!0,key:"styles",value:function(){return(0,O.AH)(j||(j=(0,r.A)(["ha-map{display:block;height:100%}"])))}}]}}),O.WF),a(),t.next=66;break;case 63:t.prev=63,t.t2=t.catch(0),a(t.t2);case 66:case"end":return t.stop()}}),t,null,[[0,63]])})));return function(e,i){return t.apply(this,arguments)}}())},7437:function(t,e,i){var a=i(22858).A,n=i(33994).A;i.a(t,function(){var t=a(n().mark((function t(e,a){var r,o,s,l,d,u,c,h,f,p,v,m,k,y,g,b,_,M,A,x,w,L,Z,z,P,E,O,C,I,B,F,S,N,T,j,H,q;return n().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,r=i(64599),o=i(33994),s=i(658),l=i(22858),d=i(64782),u=i(35806),c=i(71008),h=i(62193),f=i(2816),p=i(27927),v=i(14562),m=i(19867),i(64017),k=i(34597),y=i(81027),i.n(y),g=i(79243),i.n(g),b=i(97741),i.n(b),_=i(89655),i.n(_),M=i(50693),i.n(M),A=i(29193),i.n(A),x=i(39790),i.n(x),w=i(253),i.n(w),L=i(54846),i.n(L),Z=i(16891),i.n(Z),z=i(66555),i.n(z),P=i(5343),E=i(66360),O=i(29818),C=i(25558),I=i(84345),B=i(58445),F=i(58692),S=i(81523),N=i(15789),i(58715),i(40168),!(T=e([k,C,I])).then){t.next=56;break}return t.next=52,T;case 52:t.t1=t.sent,t.t0=(0,t.t1)(),t.next=57;break;case 56:t.t0=T;case 57:j=t.t0,k=j[0],C=j[1],I=j[2],q=function(t){return"string"==typeof t?t:t.entity_id},(0,p.A)([(0,O.EM)("ha-map")],(function(t,e){var i,a,n=function(e){function i(){var e;(0,c.A)(this,i);for(var a=arguments.length,n=new Array(a),r=0;r<a;r++)n[r]=arguments[r];return e=(0,h.A)(this,i,[].concat(n)),t(e),e}return(0,f.A)(i,e),(0,u.A)(i)}(e);return{F:n,d:[{kind:"field",decorators:[(0,O.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,O.MZ)({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[(0,O.MZ)({attribute:!1})],key:"paths",value:void 0},{kind:"field",decorators:[(0,O.MZ)({attribute:!1})],key:"layers",value:void 0},{kind:"field",decorators:[(0,O.MZ)({type:Boolean})],key:"autoFit",value:function(){return!1}},{kind:"field",decorators:[(0,O.MZ)({type:Boolean})],key:"renderPassive",value:function(){return!1}},{kind:"field",decorators:[(0,O.MZ)({type:Boolean})],key:"interactiveZones",value:function(){return!1}},{kind:"field",decorators:[(0,O.MZ)({type:Boolean})],key:"fitZones",value:function(){return!1}},{kind:"field",decorators:[(0,O.MZ)({attribute:"theme-mode",type:String})],key:"themeMode",value:function(){return"auto"}},{kind:"field",decorators:[(0,O.MZ)({type:Number})],key:"zoom",value:function(){return 14}},{kind:"field",decorators:[(0,O.wk)()],key:"_loaded",value:function(){return!1}},{kind:"field",key:"leafletMap",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"field",key:"_mapItems",value:function(){return[]}},{kind:"field",key:"_mapFocusItems",value:function(){return[]}},{kind:"field",key:"_mapZones",value:function(){return[]}},{kind:"field",key:"_mapPaths",value:function(){return[]}},{kind:"method",key:"connectedCallback",value:function(){(0,v.A)((0,m.A)(n.prototype),"connectedCallback",this).call(this),this._loadMap(),this._attachObserver()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,v.A)((0,m.A)(n.prototype),"disconnectedCallback",this).call(this),this.leafletMap&&(this.leafletMap.remove(),this.leafletMap=void 0,this.Leaflet=void 0),this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}},{kind:"method",key:"update",value:function(t){var e,i;if((0,v.A)((0,m.A)(n.prototype),"update",this).call(this,t),this._loaded){var a=!1,r=t.get("hass");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),a=!0;else if(this._loaded&&r&&this.entities){var o,s=(0,d.A)(this.entities);try{for(s.s();!(o=s.n()).done;){var l=o.value;if(r.states[q(l)]!==this.hass.states[q(l)]){this._drawEntities(),a=!0;break}}}catch(u){s.e(u)}finally{s.f()}}(t.has("_loaded")||t.has("paths"))&&this._drawPaths(),(t.has("_loaded")||t.has("layers"))&&(this._drawLayers(t.get("layers")),a=!0),(t.has("_loaded")||this.autoFit&&a)&&this.fitMap(),t.has("zoom")&&this.leafletMap.setZoom(this.zoom),(t.has("themeMode")||t.has("hass")&&(!r||(null===(e=r.themes)||void 0===e?void 0:e.darkMode)!==(null===(i=this.hass.themes)||void 0===i?void 0:i.darkMode)))&&this._updateMapStyle()}}},{kind:"get",key:"_darkMode",value:function(){return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(this.hass.themes.darkMode)}},{kind:"method",key:"_updateMapStyle",value:function(){var t=this.renderRoot.querySelector("#map");t.classList.toggle("dark",this._darkMode),t.classList.toggle("forced-dark","dark"===this.themeMode),t.classList.toggle("forced-light","light"===this.themeMode)}},{kind:"field",key:"_loading",value:function(){return!1}},{kind:"method",key:"_loadMap",value:(a=(0,l.A)((0,o.A)().mark((function t(){var e,i,a;return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!this._loading){t.next=2;break}return t.abrupt("return");case 2:return(e=this.shadowRoot.getElementById("map"))||((e=document.createElement("div")).id="map",this.shadowRoot.append(e)),this._loading=!0,t.prev=5,t.next=8,(0,B.H)(e);case 8:i=t.sent,a=(0,s.A)(i,2),this.leafletMap=a[0],this.Leaflet=a[1],this._updateMapStyle(),this._loaded=!0;case 14:return t.prev=14,this._loading=!1,t.finish(14);case 17:case"end":return t.stop()}}),t,this,[[5,,14,17]])}))),function(){return a.apply(this,arguments)})},{kind:"method",key:"fitMap",value:function(t){var e,i,a;if(this.leafletMap&&this.Leaflet&&this.hass)if(this._mapFocusItems.length||null!==(e=this.layers)&&void 0!==e&&e.length){var n,r=this.Leaflet.latLngBounds(this._mapFocusItems?this._mapFocusItems.map((function(t){return t.getLatLng()})):[]);if(this.fitZones)null===(n=this._mapZones)||void 0===n||n.forEach((function(t){r.extend("getBounds"in t?t.getBounds():t.getLatLng())}));null===(i=this.layers)||void 0===i||i.forEach((function(t){r.extend("getBounds"in t?t.getBounds():t.getLatLng())})),r=r.pad(null!==(a=null==t?void 0:t.pad)&&void 0!==a?a:.5),this.leafletMap.fitBounds(r,{maxZoom:(null==t?void 0:t.zoom)||this.zoom})}else this.leafletMap.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),(null==t?void 0:t.zoom)||this.zoom)}},{kind:"method",key:"fitBounds",value:function(t,e){var i;if(this.leafletMap&&this.Leaflet&&this.hass){var a=this.Leaflet.latLngBounds(t).pad(null!==(i=null==e?void 0:e.pad)&&void 0!==i?i:.5);this.leafletMap.fitBounds(a,{maxZoom:(null==e?void 0:e.zoom)||this.zoom})}}},{kind:"method",key:"_drawLayers",value:function(t){if(t&&t.forEach((function(t){return t.remove()})),this.layers){var e=this.leafletMap;this.layers.forEach((function(t){e.addLayer(t)}))}}},{kind:"method",key:"_computePathTooltip",value:function(t,e){var i;return i=t.fullDatetime?(0,C.r6)(e.timestamp,this.hass.locale,this.hass.config):(0,P.c)(e.timestamp)?(0,I.ie)(e.timestamp,this.hass.locale,this.hass.config):(0,I.Xs)(e.timestamp,this.hass.locale,this.hass.config),"".concat(t.name,"<br>").concat(i)}},{kind:"method",key:"_drawPaths",value:function(){var t=this,e=this.hass,i=this.leafletMap,a=this.Leaflet;if(e&&i&&a&&(this._mapPaths.length&&(this._mapPaths.forEach((function(t){return t.remove()})),this._mapPaths=[]),this.paths)){var n=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach((function(e){var r,o;e.gradualOpacity&&(r=e.gradualOpacity/(e.points.length-2),o=1-e.gradualOpacity);for(var s=0;s<e.points.length-1;s++){var l=e.gradualOpacity?o+s*r:void 0;t._mapPaths.push(a.circleMarker(e.points[s].point,{radius:N.C?8:3,color:e.color||n,opacity:l,fillOpacity:l,interactive:!0}).bindTooltip(t._computePathTooltip(e,e.points[s]),{direction:"top"})),t._mapPaths.push(a.polyline([e.points[s].point,e.points[s+1].point],{color:e.color||n,opacity:l,interactive:!1}))}var d=e.points.length-1;if(d>=0){var u=e.gradualOpacity?o+d*r:void 0;t._mapPaths.push(a.circleMarker(e.points[d].point,{radius:N.C?8:3,color:e.color||n,opacity:u,fillOpacity:u,interactive:!0}).bindTooltip(t._computePathTooltip(e,e.points[d]),{direction:"top"}))}t._mapPaths.forEach((function(t){return i.addLayer(t)}))}))}}},{kind:"method",key:"_drawEntities",value:function(){var t=this.hass,e=this.leafletMap,i=this.Leaflet;if(t&&e&&i&&(this._mapItems.length&&(this._mapItems.forEach((function(t){return t.remove()})),this._mapItems=[],this._mapFocusItems=[]),this._mapZones.length&&(this._mapZones.forEach((function(t){return t.remove()})),this._mapZones=[]),this.entities)){var a,n=getComputedStyle(this),r=n.getPropertyValue("--accent-color"),o=n.getPropertyValue("--secondary-text-color"),s=n.getPropertyValue("--dark-primary-color"),l=this._darkMode?"dark":"light",u=(0,d.A)(this.entities);try{for(u.s();!(a=u.n()).done;){var c=a.value,h=t.states[q(c)];if(h){var f="string"!=typeof c?c.name:void 0,p=null!=f?f:(0,S.u)(h),v=h.attributes,m=v.latitude,k=v.longitude,y=v.passive,g=v.icon,b=v.radius,_=v.entity_picture,M=v.gps_accuracy;if(m&&k)if("zone"!==(0,F.t)(h)){var A="string"!=typeof c&&"state"===c.label_mode?this.hass.formatEntityState(h):null!=f?f:p.split(" ").map((function(t){return t[0]})).join("").substr(0,3),x=i.marker([m,k],{icon:i.divIcon({html:'\n              <ha-entity-marker\n                entity-id="'.concat(q(c),'"\n                entity-name="').concat(A,'"\n                entity-picture="').concat(_?this.hass.hassUrl(_):"",'"\n                ').concat("string"!=typeof c?'entity-color="'.concat(c.color,'"'):"","\n              ></ha-entity-marker>\n            "),iconSize:[48,48],className:""}),title:p});this._mapItems.push(x),"string"!=typeof c&&!1===c.focus||this._mapFocusItems.push(x),M&&this._mapItems.push(i.circle([m,k],{interactive:!1,color:s,radius:M}))}else{if(y&&!this.renderPassive)continue;var w="";if(g){var L=document.createElement("ha-icon");L.setAttribute("icon",g),w=L.outerHTML}else{var Z=document.createElement("span");Z.innerHTML=p,w=Z.outerHTML}this._mapZones.push(i.marker([m,k],{icon:i.divIcon({html:w,iconSize:[24,24],className:l}),interactive:this.interactiveZones,title:p})),this._mapZones.push(i.circle([m,k],{interactive:!1,color:y?o:r,radius:b}))}}}}catch(z){u.e(z)}finally{u.f()}this._mapItems.forEach((function(t){return e.addLayer(t)})),this._mapZones.forEach((function(t){return e.addLayer(t)}))}}},{kind:"method",key:"_attachObserver",value:(i=(0,l.A)((0,o.A)().mark((function t(){var e=this;return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:this._resizeObserver||(this._resizeObserver=new ResizeObserver((function(){var t;null===(t=e.leafletMap)||void 0===t||t.invalidateSize({debounceMoveend:!0})}))),this._resizeObserver.observe(this);case 2:case"end":return t.stop()}}),t,this)}))),function(){return i.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,E.AH)(H||(H=(0,r.A)([":host{display:block;height:300px}#map{height:100%}#map.dark{background:#090909}#map.forced-dark{color:#fff;--map-filter:invert(0.9) hue-rotate(170deg) brightness(1.5) contrast(1.2) saturate(0.3)}#map.forced-light{background:#fff;color:#000;--map-filter:invert(0)}#map:active{cursor:grabbing;cursor:-moz-grabbing;cursor:-webkit-grabbing}.leaflet-tile-pane{filter:var(--map-filter)}.dark .leaflet-bar a{background-color:#1c1c1c;color:#fff}.dark .leaflet-bar a:hover{background-color:#313131}.leaflet-marker-draggable{cursor:move!important}.leaflet-edit-resize{border-radius:50%;cursor:nesw-resize!important}.named-icon{display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;color:var(--primary-text-color)}.leaflet-pane{z-index:0!important}.leaflet-bottom,.leaflet-control,.leaflet-top{z-index:1!important}.leaflet-tooltip{padding:8px;font-size:90%;background:rgba(80,80,80,.9)!important;color:#fff!important;border-radius:4px;box-shadow:none!important;text-align:center}"])))}}]}}),E.mN),a(),t.next=69;break;case 66:t.prev=66,t.t2=t.catch(0),a(t.t2);case 69:case"end":return t.stop()}}),t,null,[[0,66]])})));return function(e,i){return t.apply(this,arguments)}}())},15789:function(t,e,i){i.d(e,{C:function(){return a}});var a="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0},32350:function(t,e,i){var a=i(32174),n=i(23444),r=i(33616),o=i(36565),s=i(87149),l=Math.min,d=[].lastIndexOf,u=!!d&&1/[1].lastIndexOf(1,-0)<0,c=s("lastIndexOf"),h=u||!c;t.exports=h?function(t){if(u)return a(d,this,arguments)||0;var e=n(this),i=o(e);if(0===i)return-1;var s=i-1;for(arguments.length>1&&(s=l(s,r(arguments[1]))),s<0&&(s=i+s);s>=0;s--)if(s in e&&e[s]===t)return s||0;return-1}:d},4978:function(t,e,i){var a=i(41765),n=i(49940),r=i(36565),o=i(33616),s=i(2586);a({target:"Array",proto:!0},{at:function(t){var e=n(this),i=r(e),a=o(t),s=a>=0?a:i+a;return s<0||s>=i?void 0:e[s]}}),s("at")},15814:function(t,e,i){var a=i(41765),n=i(32350);a({target:"Array",proto:!0,forced:n!==[].lastIndexOf},{lastIndexOf:n})},8206:function(t,e,i){var a=i(41765),n=i(13113),r=i(22669),o=i(33616),s=i(53138),l=i(26906),d=n("".charAt);a({target:"String",proto:!0,forced:l((function(){return"\ud842"!=="𠮷".at(-2)}))},{at:function(t){var e=s(r(this)),i=e.length,a=o(t),n=a>=0?a:i+a;return n<0||n>=i?void 0:d(e,n)}})},59613:function(t,e,i){function a(t,e){return t instanceof Date?new t.constructor(e):new Date(e)}i.d(e,{w:function(){return a}})},9854:function(t,e,i){i.d(e,{r:function(){return n}});var a=i(63165);function n(t,e){return+(0,a.o)(t)==+(0,a.o)(e)}},5343:function(t,e,i){i.d(e,{c:function(){return o}});var a=i(59613);function n(t){return(0,a.w)(t,Date.now())}var r=i(9854);function o(t){return(0,r.r)(t,n(t))}},63165:function(t,e,i){i.d(e,{o:function(){return n}});var a=i(30429);function n(t){var e=(0,a.a)(t);return e.setHours(0,0,0,0),e}},30429:function(t,e,i){i.d(e,{a:function(){return n}});var a=i(91001);i(39790),i(7760);function n(t){var e=Object.prototype.toString.call(t);return t instanceof Date||"object"===(0,a.A)(t)&&"[object Date]"===e?new t.constructor(+t):"number"==typeof t||"[object Number]"===e||"string"==typeof t||"[object String]"===e?new Date(t):new Date(NaN)}}}]);
//# sourceMappingURL=3945.yjt3Ik0DJBI.js.map