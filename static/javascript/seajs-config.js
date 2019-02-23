/*map start*/
seajs.production = true;
if(seajs.production){
    seajs.config({
        map : [
	[
		"action/app.js",
		"action/app-ee52c139c021386f9b57d56a4199416a.js"
	],
	[
		"app.js",
		"app-8f6dbb757fccb8461855ec14caeb536a.js"
	],
	[
		"view/book-data.js",
		"view/book-data-9d8cc1e83a98f6bfc96f84c8e45b680b.js"
	],
	[
		"view/book-tabs.js",
		"view/book-tabs-ecbe50d199aeb58b38631286ed5fc1ca.js"
	],
	[
		"view/bookshelf.js",
		"view/bookshelf-10eb5229d7413ee010af6cc54c2b88ee.js"
	],
	[
		"view/commentlist.js",
		"view/commentlist-844f272ed666c5f7168f3c6393ec7bdb.js"
	],
	[
		"view/coupon.js",
		"view/coupon-e063567a8ebbd07375615fff1485fd12.js"
	],
	[
		"view/folding.js",
		"view/folding-5d072d4eda4068eb934394d071254f9d.js"
	],
	[
		"view/login.js",
		"view/login-86a7927098241431b8cb0e31552902f0.js"
	],
	[
		"view/mybook.js",
		"view/mybook-0ed950596b1c2704fe3048558b3b8dd4.js"
	],
	[
		"view/pay.js",
		"view/pay-8a301c07d5c6ba8c8b818d9091b16fae.js"
	],
	[
		"view/redeem.js",
		"view/redeem-1a9dccee9b908e80a3f0aafae88cfbba.js"
	],
	[
		"view/redeem_input.js",
		"view/redeem_input-0d16546ffe094a8a754222085c662f58.js"
	],
	[
		"view/redeem_input_didi.js",
		"view/redeem_input_didi-d9823b525fd4084f42cce92a712e835b.js"
	],
	[
		"view/replydetail.js",
		"view/replydetail-413aebf8d781e7a50da663c2a9914453.js"
	],
	[
		"view/search.js",
		"view/search-776b1fc76fd8d0bb789abd4e70059a5c.js"
	],
	[
		"view/view.js",
		"view/view-df0921c4d3d6826b37f3392dfbe47dcc.js"
	]
]
    });
}
/*map end*/
//////////////////////////////////////////////////////
////////////////// develop config  ///////////////////
//////////////////////////////////////////////////////

if(!location.search.match(/product/) 
    && location.host.indexOf('local') == 0 
    || /^\d.+$/.test(location.host)){
  seajs.production = !1;
  seajs.data.map = [];
  seajs.config({preload : ['seajs-debug', 'viperjs/log/1.0.0/log']});
}

//////////////////////////////////////////////////////
////////////////// develop config  ///////////////////
//////////////////////////////////////////////////////

seajs.config({
  base : '/m/static/js/sea-modules',
  alias: {
    '$': 'gallery/jquery/1.9.1/jquery',
    '$-debug': 'gallery/jquery/1.9.1/jquery-debug',
    '_': 'gallery/underscore/1.4.4/underscore',
    '_-debug': 'gallery/underscore/1.4.4/underscore-debug',
    "seajs-debug": "seajs/seajs-debug/1.1.1/seajs-debug",
    'handlebars': 'gallery/handlebars/1.0.2/handlebars',
    'sdk' : (seajs.production ? '' : '/m/static/js/') + 'app/sdk/sdk',
  },
  preload: [
    this.JSON ? '' : 'gallery/json/1.0.2/json',
    Function.prototype.bind ? '' : 'gallery/es5-safe/es5-safe',
    seajs.production ? '' : 'seajs/seajs-text/1.0.0/seajs-text-debug',
    seajs.production ? 'app/app' : ''
  ]
});
(function(prefix) {
  var util = {};
  util.map = Array.prototype.map ?
    function(arr, fn) {
      return arr.map(fn);
  } :
    function(arr, fn) {
      var ret = [];
      for (var i = 0; i < arr.length; i++) {
        ret.push(fn(arr[i], i, arr));
      }
      return ret;
  };

  var _use = seajs.use;

  seajs.use = function(ids, callback) {
    if (typeof ids === 'string') {
      ids = [ids];
    }

    ids = util.map(ids, function(id) {
      return (seajs.production ? '' : prefix) + id;
    });
    console.log(ids);

    return _use(ids, callback);
  }
})('/m/static/js/');