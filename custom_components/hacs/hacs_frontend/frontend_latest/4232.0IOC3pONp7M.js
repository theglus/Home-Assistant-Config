export const id=4232;export const ids=[4232];export const modules={4569:(e,i,t)=>{var s=t(36312),a=(t(253),t(5186),t(2075),t(16891),t(4525),t(66360)),r=t(29818),d=t(65520),l=t(94100),o=t(50880),n=t(31134),c=t(11605),u=t(69408),h=t(75325),v=t(75548),k=t(87846);t(98969),t(58715),t(27783),t(83859);const y=e=>a.qy`<ha-list-item graphic="icon" class="${(0,d.H)({"add-new":e.area_id===_})}"> ${e.icon?a.qy`<ha-icon slot="graphic" .icon="${e.icon}"></ha-icon>`:a.qy`<ha-svg-icon slot="graphic" .path="${"M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z"}"></ha-svg-icon>`} ${e.name} </ha-list-item>`,_="___ADD_NEW___",f="___NO_ITEMS___",p="___ADD_NEW_SUGGESTION___";(0,s.A)([(0,r.EM)("ha-area-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"no-add"})],key:"noAdd",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"exclude-areas"})],key:"excludeAreas",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,r.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,r.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_suggestion",value:void 0},{kind:"field",key:"_init",value:()=>!1},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"field",key:"_getAreas",value(){return(0,l.A)(((e,i,t,s,a,r,d,l,o,c)=>{let u,v,k={};(s||a||r||d||l)&&(k=(0,h.g2)(t),u=i,v=t.filter((e=>e.area_id)),s&&(u=u.filter((e=>{const i=k[e.id];return!(!i||!i.length)&&k[e.id].some((e=>s.includes((0,n.m)(e.entity_id))))})),v=v.filter((e=>s.includes((0,n.m)(e.entity_id))))),a&&(u=u.filter((e=>{const i=k[e.id];return!i||!i.length||t.every((e=>!a.includes((0,n.m)(e.entity_id))))})),v=v.filter((e=>!a.includes((0,n.m)(e.entity_id))))),r&&(u=u.filter((e=>{const i=k[e.id];return!(!i||!i.length)&&k[e.id].some((e=>{const i=this.hass.states[e.entity_id];return!!i&&(i.attributes.device_class&&r.includes(i.attributes.device_class))}))})),v=v.filter((e=>{const i=this.hass.states[e.entity_id];return i.attributes.device_class&&r.includes(i.attributes.device_class)}))),d&&(u=u.filter((e=>d(e)))),l&&(u=u.filter((e=>{const i=k[e.id];return!(!i||!i.length)&&k[e.id].some((e=>{const i=this.hass.states[e.entity_id];return!!i&&l(i)}))})),v=v.filter((e=>{const i=this.hass.states[e.entity_id];return!!i&&l(i)}))));let y,p=e;return u&&(y=u.filter((e=>e.area_id)).map((e=>e.area_id))),v&&(y=(y??[]).concat(v.filter((e=>e.area_id)).map((e=>e.area_id)))),y&&(p=p.filter((e=>y.includes(e.area_id)))),c&&(p=p.filter((e=>!c.includes(e.area_id)))),p.length||(p=[{area_id:f,floor_id:null,name:this.hass.localize("ui.components.area-picker.no_areas"),picture:null,icon:null,aliases:[],labels:[]}]),o?p:[...p,{area_id:_,floor_id:null,name:this.hass.localize("ui.components.area-picker.add_new"),picture:null,icon:"mdi:plus",aliases:[],labels:[]}]}))}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getAreas(Object.values(this.hass.areas),Object.values(this.hass.devices),Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd,this.excludeAreas).map((e=>({...e,strings:[e.area_id,...e.aliases,e.name]})));this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return a.qy` <ha-combo-box .hass="${this.hass}" .helper="${this.helper}" item-value-path="area_id" item-id-path="area_id" item-label-path="name" .value="${this._value}" .disabled="${this.disabled}" .required="${this.required}" .label="${void 0===this.label&&this.hass?this.hass.localize("ui.components.area-picker.area"):this.label}" .placeholder="${this.placeholder?this.hass.areas[this.placeholder]?.name:void 0}" .renderer="${y}" @filter-changed="${this._filterChanged}" @opened-changed="${this._openedChanged}" @value-changed="${this._areaChanged}"> </ha-combo-box> `}},{kind:"method",key:"_filterChanged",value:function(e){const i=e.target,t=e.detail.value;if(!t)return void(this.comboBox.filteredItems=this.comboBox.items);const s=(0,c.H)(t,i.items?.filter((e=>![f,_].includes(e.label_id)))||[]);0===s.length?this.noAdd?(this._suggestion=t,this.comboBox.filteredItems=[{area_id:p,floor_id:null,name:this.hass.localize("ui.components.area-picker.add_new_sugestion",{name:this._suggestion}),icon:"mdi:plus",picture:null,labels:[],aliases:[]}]):this.comboBox.filteredItems=[{area_id:f,floor_id:null,name:this.hass.localize("ui.components.area-picker.no_match"),icon:null,picture:null,labels:[],aliases:[]}]:this.comboBox.filteredItems=s}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();let i=e.detail.value;if(i===f)return i="",void this.comboBox.setInputValue("");[p,_].includes(i)?(e.target.value=this._value,this.hass.loadFragmentTranslation("config"),(0,k.J)(this,{suggestedName:i===p?this._suggestion:"",createEntry:async e=>{try{const i=await(0,u.L3)(this.hass,e),t=[...Object.values(this.hass.areas),i];this.comboBox.filteredItems=this._getAreas(t,Object.values(this.hass.devices),Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd,this.excludeAreas),await this.updateComplete,await this.comboBox.updateComplete,this._setValue(i.area_id)}catch(e){(0,v.K$)(this,{title:this.hass.localize("ui.components.area-picker.failed_create_area"),text:e.message})}}}),this._suggestion=void 0,this.comboBox.setInputValue("")):i!==this._value&&this._setValue(i)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,o.r)(this,"value-changed",{value:e}),(0,o.r)(this,"change")}),0)}}]}}),a.WF)},44232:(e,i,t)=>{t.r(i),t.d(i,{HaAreaSelector:()=>k});var s=t(36312),a=(t(253),t(4525),t(66360)),r=t(29818),d=t(94100),l=t(38782),o=t(75325),n=t(50880),c=t(43527),u=t(37880),h=t(91148),v=(t(4569),t(2075),t(16891),t(31627));(0,s.A)([(0,r.EM)("ha-areas-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"no-add"})],key:"noAdd",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:"picked-area-label"})],key:"pickedAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:"pick-area-label"})],key:"pickAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.hass)return a.s6;const e=this._currentAreas;return a.qy` ${e.map((e=>a.qy` <div> <ha-area-picker .curValue="${e}" .noAdd="${this.noAdd}" .hass="${this.hass}" .value="${e}" .label="${this.pickedAreaLabel}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeDeviceClasses="${this.includeDeviceClasses}" .deviceFilter="${this.deviceFilter}" .entityFilter="${this.entityFilter}" .disabled="${this.disabled}" @value-changed="${this._areaChanged}"></ha-area-picker> </div> `))} <div> <ha-area-picker .noAdd="${this.noAdd}" .hass="${this.hass}" .label="${this.pickAreaLabel}" .helper="${this.helper}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeDeviceClasses="${this.includeDeviceClasses}" .deviceFilter="${this.deviceFilter}" .entityFilter="${this.entityFilter}" .disabled="${this.disabled}" .placeholder="${this.placeholder}" .required="${this.required&&!e.length}" @value-changed="${this._addArea}" .excludeAreas="${e}"></ha-area-picker> </div> `}},{kind:"get",key:"_currentAreas",value:function(){return this.value||[]}},{kind:"method",key:"_updateAreas",value:async function(e){this.value=e,(0,n.r)(this,"value-changed",{value:e})}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;if(t===i)return;const s=this._currentAreas;t&&!s.includes(t)?this._updateAreas(s.map((e=>e===i?t:e))):this._updateAreas(s.filter((e=>e!==i)))}},{kind:"method",key:"_addArea",value:function(e){e.stopPropagation();const i=e.detail.value;if(!i)return;e.currentTarget.value="";const t=this._currentAreas;t.includes(i)||this._updateAreas([...t,i])}},{kind:"field",static:!0,key:"styles",value:()=>a.AH`div{margin-top:8px}`}]}}),(0,v.E)(a.WF));let k=(0,s.A)([(0,r.EM)("ha-selector-area")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[(0,r.wk)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_configEntries",value:void 0},{kind:"field",key:"_deviceIntegrationLookup",value:()=>(0,d.A)(o.fk)},{kind:"method",key:"_hasIntegration",value:function(e){return e.area?.entity&&(0,l.e)(e.area.entity).some((e=>e.integration))||e.area?.device&&(0,l.e)(e.area.device).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&void 0!==this.value&&(this.selector.area?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,n.r)(this,"value-changed",{value:this.value})):!this.selector.area?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,n.r)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,c.c)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,u.VN)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){return this._hasIntegration(this.selector)&&!this._entitySources?a.s6:this.selector.area?.multiple?a.qy` <ha-areas-picker .hass="${this.hass}" .value="${this.value}" .helper="${this.helper}" .pickAreaLabel="${this.label}" no-add .deviceFilter="${this.selector.area?.device?this._filterDevices:void 0}" .entityFilter="${this.selector.area?.entity?this._filterEntities:void 0}" .disabled="${this.disabled}" .required="${this.required}"></ha-areas-picker> `:a.qy` <ha-area-picker .hass="${this.hass}" .value="${this.value}" .label="${this.label}" .helper="${this.helper}" no-add .deviceFilter="${this.selector.area?.device?this._filterDevices:void 0}" .entityFilter="${this.selector.area?.entity?this._filterEntities:void 0}" .disabled="${this.disabled}" .required="${this.required}"></ha-area-picker> `}},{kind:"field",key:"_filterEntities",value(){return e=>!this.selector.area?.entity||(0,l.e)(this.selector.area.entity).some((i=>(0,h.Ru)(i,e,this._entitySources)))}},{kind:"field",key:"_filterDevices",value(){return e=>{if(!this.selector.area?.device)return!0;const i=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,l.e)(this.selector.area.device).some((t=>(0,h.vX)(t,e,i)))}}}]}}),a.WF)},69408:(e,i,t)=>{t.d(i,{L3:()=>r,dj:()=>l,ft:()=>a.f,gs:()=>d});t(89655);var s=t(82739),a=t(20691);const r=(e,i)=>e.callWS({type:"config/area_registry/create",...i}),d=(e,i,t)=>e.callWS({type:"config/area_registry/update",area_id:i,...t}),l=(e,i)=>(t,a)=>{const r=i?i.indexOf(t):-1,d=i?i.indexOf(a):-1;if(-1===r&&-1===d){const i=e?.[t]?.name??t,r=e?.[a]?.name??a;return(0,s.x)(i,r)}return-1===r?1:-1===d?-1:r-d}},43527:(e,i,t)=>{t.d(i,{c:()=>r});const s=async(e,i,t,a,r,...d)=>{const l=r,o=l[e],n=o=>a&&a(r,o.result)!==o.cacheKey?(l[e]=void 0,s(e,i,t,a,r,...d)):o.result;if(o)return o instanceof Promise?o.then(n):n(o);const c=t(r,...d);return l[e]=c,c.then((t=>{l[e]={result:t,cacheKey:a?.(r,t)},setTimeout((()=>{l[e]=void 0}),i)}),(()=>{l[e]=void 0})),c},a=e=>e.callWS({type:"entity/source"}),r=e=>s("_entitySources",3e4,a,(e=>Object.keys(e.states).length),e)},20691:(e,i,t)=>{t.d(i,{f:()=>o});var s=t(84280),a=t(82739),r=t(46530);const d=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then((e=>e.sort(((e,i)=>(0,a.x)(e.name,i.name))))),l=(e,i)=>e.subscribeEvents((0,r.s)((()=>d(e).then((e=>i.setState(e,!0)))),500,!0),"area_registry_updated"),o=(e,i)=>(0,s.N)("_areaRegistry",d,l,e,i)},31627:(e,i,t)=>{t.d(i,{E:()=>l});var s=t(36312),a=t(14562),r=t(19867),d=t(29818);const l=e=>(0,s.A)(null,(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)((0,r.A)(t.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.A)((0,r.A)(t.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,a.A)((0,r.A)(t.prototype),"updated",this).call(this,e),e.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const i of e.keys())if(this.hassSubscribeRequiredHostProps.includes(i))return void this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some((e=>void 0===this[e]))&&(this.__unsubs=this.hassSubscribe())}}]}}),e)},87846:(e,i,t)=>{t.d(i,{J:()=>r});var s=t(50880);const a=()=>Promise.all([t.e(6342),t.e(6279),t.e(3832),t.e(4555),t.e(4421),t.e(1056)]).then(t.bind(t,1056)),r=(e,i)=>{(0,s.r)(e,"show-dialog",{dialogTag:"dialog-area-registry-detail",dialogImport:a,dialogParams:i})}},5186:(e,i,t)=>{var s=t(41765),a=t(73201),r=t(95689),d=t(56674),l=t(1370);s({target:"Iterator",proto:!0,real:!0},{every:function(e){d(this),r(e);var i=l(this),t=0;return!a(i,(function(i,s){if(!e(i,t++))return s()}),{IS_RECORD:!0,INTERRUPTED:!0}).stopped}})}};
//# sourceMappingURL=4232.0IOC3pONp7M.js.map