define("duokan/store/1/page/act_index.js",[],function(t){var e=t("module"),i=t("module/comment_square"),o=t("module/md_like"),n=t("widget/tab/tab.slide.js"),s=t("widget/cycler/cycler"),r=t("base"),a=t("tpl"),_=t("common"),h=t("request"),c=e.create({initialize:function(){this.supInitialize.apply(this,arguments),this.__initLikeList(),this.__initCycler(),this.__initRankTab(),this.__buildSquare(),this.__buildPublishers(),this.__buildReadGuide()},__initLikeList:function(){new o({el:this.$("#module-like")})},__buildSquare:function(){new i({el:$(".j-square")})},__initCycler:function(){var t={list:$("#slides").children(),nbox:$("#slides"),plist:$(".slides_tabs a"),pbox:$(".slides_tabs"),prev:this.$(".j-prev"),next:this.$(".j-next"),interval:4,speed:400};new s(t)},__initRankTab:function(){new n({list:this.$(".j-rank-tab .itm"),duration:200,target:this.$(".j-rank-tab .j-target"),selected:"crt",onchange:function(t){this.$(".j-rank .j-cnt").hide().eq(t.index).show()}.bind(this)})},__buildPublishers:function(){new n({list:this.$(".j-publish-tab .itm"),target:this.$(".j-publish-tab .j-target"),duration:300,onchange:function(t){this.$(".j-publish .j-cnt").hide().eq(t.index).show()}.bind(this)})},__buildReadGuide:function(){new d({el:this.$(".j-read-guide")})}}),d=r.create(),l=d.prototype;return l.initialize=function(){return this.supInitialize.apply(this,arguments),this.__data={login:_.isLogin(),list:[]},this.__data.login?(h.get_read_history().done(this.__render.bind(this)),void 0):(this.$el.html(a.getJst("jst-read-guide",{status:this.__data})),void 0)},l.__render=function(t){0==t.status.code&&(this.__data.list=t.data.books),this.$el.html(a.getJst("jst-read-guide",{status:this.__data}))},new c}),define("duokan/store/1/module/comment_square.js",[],function(t){var e=t("base"),i=t("request"),o=t("tpl"),n=(t("business"),t("common")),s=t("common/account/nick"),r=t("widget/cache/cache"),a=t("widget/cycler/cycler.slide.js"),_=null,h=e.create(),c=h.prototype;c.events={"click .j-like":"__onVote"},c.__onVote=function(t){if(!n.isLogin())return n.login(),void 0;var e=$(t.currentTarget);i.vote_comment(e.data("id"),function(t){if(e.addClass("icn-smile-selected").removeClass("j-like"),0==t.result){var i=e.next();i.html(+i.html()+1),e.parents("li").addClass("selected")}else 40007==t.result}.bind(this))},c.initialize=function(t){this.supInitialize(t),o.parse("#template-box"),this.__getComments(this.__doBuild.bind(this))},c.__getComments=function(t){var e={};e.count=36,i.get_hot_comments(e,function(e){t(e.items)})},c.__doBuild=function(t){this.__setCache(t),this.__cache.on("change",function(t){_=t.xlist}),this.__initCycler()},c.__setCache=function(t){this.__cache=new r,this.__cache.setCache("comments",t)},c.__initCycler=function(){var t={cache:this.__cache,interval:30,nbox:this.$(".j-cnt"),plist:this.$(".j-pager a"),selected:"crt",tpl:"booksquare-item",prev:this.$(".j-prev"),next:this.$(".j-next"),onviewload:this.__replaceNick.bind(this)};this.__cycler=new d(t)},c.__replaceNick=function(){new s({data:_})};var d=a.create();return _proCacheCycler=d.prototype,_suproCacheCycler=d._$supro,_proCacheCycler.__getData=function(t,e){return this.__list[t-1]?(_suproCacheCycler.__getData.apply(this,arguments),void 0):(this.__cache||(this.__cache=this.options.cache,this.__cache.on("change",function(t){e({xlist:t.xlist})})),this.__cache.get({key:"comments",offset:6*(t-1),limit:6}),void 0)},h}),define("duokan/store/1/module/md_like.js",[],function(t){"use strict";var e=t("base"),i=t("common/like/like");t("common");var o=t("business"),n=t("tpl"),s=e.create(),r=s.prototype;return r.events={"click .j-change":"__doBuild"},r.initialize=function(){this.supInitialize.apply(this,arguments),this.__doBuild()},r.__doBuild=function(){i.get(9).done(function(t){var e=n.getJst("jst-like-list",{xlist:o.formatBooks(t.list)});this.$(".j-list").html(e),this.$(".j-change").toggle(t.size>1)}.bind(this))},s}),define("duokan/store/1/common/like/like.js",[],function(t,e){"use strict";function i(t){var e=$$Storage.get("paidList"),i=[];return _.each(t,function(t){e.has(t.book_id)||i.push(t)}),i}function o(){var t=$.Deferred(),e=r.get("rock_item"),i=+new Date,o=h.getInfo().user_id;return!e||i>e.t||o!==e.user_id?(r.remove("rock_item"),e={t:0,user_id:o,list:[]},a.like_list().done(function(o){e.list=o.items;var n=1e3*(o.timeout||3600);e.t=i+n,t.resolve(e),r.set("rock_item",e)})):setTimeout(function(){t.resolve(e)},0),t.promise()}function n(t,e){var o=t+"-"+e.t,n=c[o];if(!n){c[o]=_.extend({index:0,group:[]},e),n=c[o];var s=i(e.list);s.length=Math.floor(s.length/t)*t,n.group=_.groupBy(s,function(e,i){return Math.floor(i/t)})}var r=n.index;return n.index=(r+1)%_.size(n.group)||0,{list:n.group[r]||[],size:_.size(n.group)}}function s(t,e){var i=$.Deferred();return!d||e?o().done(function(e){d=e,i.resolve(n(t,e))}):setTimeout(function(){i.resolve(n(t,d))},0),i.promise()}var r=t("gallery/store/1.3.5/store"),a=t("request"),h=t("common"),c={},d=null;e.requestLike=o,e.get=s});