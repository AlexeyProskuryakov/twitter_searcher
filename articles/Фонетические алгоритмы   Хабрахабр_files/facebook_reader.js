$(function () {
  (function () {

    var ctor = function(){},
        slice = Array.prototype.slice,

        bind = function (func, context) {
          var bound, args;
          args = slice.call(arguments, 2);

          return bound = function() {
            if (!(this instanceof bound)) return func.apply(context, args.concat(slice.call(arguments)));
            ctor.prototype = func.prototype;
            var self = new ctor;
            var result = func.apply(self, args.concat(slice.call(arguments)));
            if (Object(result) === result) return result;
            return self;
          };
        },

        bindAll = function(obj) {
          var funcs = slice.call(arguments, 1);
          for(var i=0,l=funcs.length; i<l; i++) {
            var f = funcs[i];
            obj[f] = bind(obj[f], obj);
          }
          return obj;
        },

        template = function(templ, object) {
          return templ.
            replace(/\$\{([^}]+)\}/g, function (all, part) {
              return object[part];
            });
        },

        setCookie = function(name, value) {
          var date = new Date();
          date.setDate(date.getDate() + 30);

          if (value === null) {
            value = '0';
            date = new Date(0);
          }

          value = value || '1';

          document.cookie = [
              encodeURIComponent(name), '=', value,
              '; expires=' + date.toUTCString(),
              '; path=/',
              // '; domain=.habrahabr.ru',
          ].join('')
        },

        getCookie = function (name) {
          var decode = encodeURIComponent;
          var pairs = document.cookie.split('; ');

          for (var i = 0, pair; pair = pairs[i] && pairs[i].split('='); i++) {
              if (decode(pair[0]) === name) return decode(pair[1] || '');
          }
          return null;
        },

        deleteCookie = function (name) { 
          setCookie(name, null); 
        },

        plural = function(a, one, few, many) {
          if (a % 10 == 1 && a % 100 != 11) { 
              return one;

          } else if (a % 10 >= 2 && a % 10 <= 4 && ( a % 100 < 10 || a % 100 >= 20)) { 
              return few;

          } else { 
              return many; 
          }
        },

        getTime = function(timestamp) {
          var current_timestamp = Math.round((new Date()).getTime() / 1000),
            time_ago = current_timestamp - timestamp,
            days = Math.floor( time_ago/86400 ),
            hours = Math.floor( ( time_ago - days * 86400)/3600 ),
            min = Math.floor( ( time_ago - days * 86400 - hours * 3600 )/60 ),
            sec = time_ago - days * 86400 - hours * 3600 - min * 60,

            time_ago_text   =   (( days > 0 ) ?
                days + " " + plural( days, "день", "дня", "дней" ) :
                (( hours > 0 ) ?
                    hours + " " + plural( hours, "час", "часа", "часов" ) :
                    (( min > 0 ) ?
                        min + " " + plural( min, "минута", "минуты", "минут" ) :
                        (( sec > 0 ) ? sec + " " + plural( sec, "секунда", "секунды", "секунд" ) : "0" )
                    )
                )
            ) + " назад";
          return time_ago_text;
        }



    var FacebookReader = function (container, app_id) {
      this.container = container;
      this._app_id = app_id;

      if (this._app_id && 
        this.container.length && !this.container.data('_facebook_reader')) {

        this.container.data('_facebook_reader', this);

        if (typeof(FB) !== 'undefined') {
          this.init();
        } else {
          this.connect_facebook();
        };
      };
    };
    window['FacebookReader'] = FacebookReader;

    FacebookReader.prototype = {

      'TEMPLATES': {
        'guest': ' \
          <div class="connect"> \
            <div class="button"><div class="fb-login-button" data-show-faces="false" data-width="200" data-max-rows="1" data-scope="publish_actions"></div></div> \
            <div class="text">Делитесь прочитанными статьями с вашими друзьями в Facebook <a href="https://www.facebook.com/about/timeline/apps"><img class="help-tip tip_top" title="Что это?" src="/i/bg_cicle_help.png"></a></div> \
            <div class="loading_text">Загрузка...</div> \
          </div> \
        ',
        'connected': '\
          <div class="connected"> \
            ${user} \
            <div class="history">\
              <span class="history_toggle"><ins>Прочитанное</ins></span>\
	              <span class="history_enabled"> \
	            	| \
	              <label for="facebook_reader_history_enabled"> \
	              	История:  \
	                <input type="checkbox" name="facebook_reader_history_enabled" id="facebook_reader_history_enabled" /> \
	                <span class="checker"></span> \
	              </label> \
	            </span> \
              <div class="content"> \
                ${history} \
                <div class="all"> \
                  <a target="_blank" href="${all_history_link}" >Вся история</a> \
                </div> \
                <div class="notifications"> \
                  <label for="article_overlay_notify"> \
                    <input type="checkbox" id="article_overlay_notify" class="article_notify" /> \
                    Напоминать о <span class="excess">каждом </span>добавлении<span class="excess"> в историю</span> \
                  </label> \
                </div> \
              </div> \
            </div> \
          </div> \
        ',
        'user': ' \
          <div class="user"> \
            <a href="${link}" class="user" target="_blank"> \
              <img src="${picture}" class="avatar" /> \
            </a> \
            <span class="name"> \
              <a href="${link}" class="user" target="_blank">${first_name} ${last_name}</a> \
              <a href="https://www.facebook.com/about/timeline/apps"><img class="help-tip tip_top" title="Что это?" src="/i/bg_cicle_help.png"></a> \
            </span> \
            <span class="disable"><ins title="Отключить виджет">Отключить виджет</ins></span> \
          </div> \
        ',
        'history_item': '\
          <div class="item" data-id="${id}"> \
            <div class="time">${time}</div>\
            <div class="link">\
            	<a  href="${link}">${title}</a>\
            	<span class="delete" title="Удалить из истории"></span>\
            </div>\
          </div>\
        ',
        'confirmation_overlay': '\
          <p> \
            Сохранить в истории<span class="excess"> чтения</span>? \
            <ins class="confirmation_yes">Да</ins> \
            <ins class="confirmation_no">Нет</ins> \
          </p> \
        ',
        'article_overlay': '\
          <div class="added"> \
            Добавлено в историю чтения: \
            <ins class="article_overlay_cancel dotted">отменить</ins> \
          </div> \
          <div class="title"> \
            <a class="link" href="${link}">${title}</a> \
          </div> \
          <div class="notification"> \
            <label for="article_overlay_notify"> \
              <input type="checkbox" id="article_overlay_notify" class="article_notify" /> \
              Напоминать о <span class="excess">каждом </span>добавлении<span class="excess"> в историю</span> \
            </label> \
          </div> \
          <ins class="article_overlay_close" title="скрыть уведомление">×</ins> \
        '
      },

      'HISTORY_COOKIE': 'fbr_disabled',
      'NOTIFICATION_COOKIE': 'fbr_notifications_disabled',

      'connect_facebook': function () {
        var self = this;

        window.fbAsyncInit = function() {
          FB.init({
              'appId': self._app_id,
              'status': true, 
              'cookie': true,
              'xfbml': true,
              // 'oauth': true
          });

          self.init();
        };

        (function(d){
          var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
          js = d.createElement('script'); js.id = id; js.async = true;
          js.src = "//connect.facebook.net/ru_RU/all.js";
          d.getElementsByTagName('head')[0].appendChild(js);
        }(document));
      },

      'init': function () {
        bindAll(this, 'checkStatus', 'addArticle', 'check_width');

        this.events = {};
        for(var e in this._events) {
          if (this._events.hasOwnProperty(e)) {
            this.events[e] = bind(this._events[e], this);
          }
        };

        FB.Event.subscribe("auth.authResponseChange", this.checkStatus);
        FB.getLoginStatus(this.checkStatus);

        this._historyEnabled = !getCookie(this.HISTORY_COOKIE);
        this._notificationsEnabled = !getCookie(this.NOTIFICATION_COOKIE);

        var container = this.container;
        $(window).bind('resize', this.check_width);
      },

      'check_width' : function () {
        var container = this.container;

        container.toggleClass(
          'narrow',
          container[0].offsetWidth < 350
        );
      },

      'checkStatus': function (response) {
        if (response.status == 'connected') {
          this.container.find('.connect').addClass('loading');
          this.getUser();
        } else {
          this.render_guest();
        };
      },
      
      'cleanup_container': function () {
        this.unbind_user_events();
        
        // tipTip не умеет удалять себя, поэтому так
        //$("#facebook_reader .help-tip").remove();  
      },

      'render_guest': function () {
        this.cleanup_container();

        this.container.
          html(
            template(this.TEMPLATES['guest'], this)
          ).
          show();

        this.check_width();

        FB.XFBML.parse();
      },

      'render_connected': function (user, news) {
        this.cleanup_container();

        this.container.
          html(
              template(
                this.TEMPLATES['connected'],
                {
                  'user': template(this.TEMPLATES['user'], user),
                  'history': this.render_history(news),
                  'all_history_link': user.link + '/app_' + this._app_id
                }
              )
          ).
          show();
          
        // настройки тултипов
        //$("#facebook_reader .help-tip").tipTip({maxWidth: "300px", edgeOffset: 10});  

        this.check_width();

        this.bind_user_events();

        this.container.
          find('#facebook_reader_history_enabled').
          prop('checked', !getCookie(this.HISTORY_COOKIE));

        this.events.historyEnableClick();

        if (!this._article_inited) {
          this._article_inited = true;

          if (this.getArticleTitle()) {
            setTimeout(bind(function () {
              if (this._historyEnabled) {
                this.addArticle();
              } else {
                this.showAddConfirmationOverlay();
              }
            }, this), 10000);
          };
        }

        this.events.articleNotifyChanged();
      },

      'render_history': function (items) {
        var html=[];
        for(var i=0,l=items.length; i<l; i++) {
          var item = items[i];
          html.push(template(this.TEMPLATES['history_item'], {
              id: item.id,
              link: item.data.article.url,
              time: getTime(item.start_time),
              title: item.data.article.title
          }));
        };

        return html.join('');
      },

      'enableHistory': function () {
        this._historyEnabled = true;
        deleteCookie(this.HISTORY_COOKIE);
      },

      'disableHistory': function () {
        this._historyEnabled = false;
        setCookie(this.HISTORY_COOKIE);

        if (this._current_article_id ) {
          this.deleteArticle(this._current_article_id);
          this._current_article_id = null;
        }
      },

      'showAddConfirmationOverlay': function () {
        this.confirmation_overlay = $('<div/>', {
          'class': 'overlay confirmation_overlay',
          'html': template(this.TEMPLATES['confirmation_overlay'])
        }).
          hide().
          appendTo(this.container.find('.connected')).
          fadeIn(500);
      },

      'showArticleOverlay': function (article) {
        this.article_overlay = $('<div/>', {
          'class': 'overlay article_overlay',
          'html': template(this.TEMPLATES['article_overlay'], article)
        }).
          hide().
          appendTo(this.container.find('.connected'));

        this.events.articleNotifyChanged();

        this.events.historyHide();

        this.article_overlay.fadeIn(500);
      },

      'bind_user_events': function () {
        this.container.
          delegate('.disable', 'click', this.events.disableClick).
          delegate('#facebook_reader_history_enabled', 'click', this.events.historyEnableClick).
          delegate('.history_toggle', 'click', this.events.historyToggle).
          delegate('.history .content .delete', 'click', this.events.historyDelete).
          delegate('.confirmation_yes', 'click', this.events.confirmAdding).
          delegate('.confirmation_no', 'click', this.events.hideConfirmationOverlay).
          delegate('.article_overlay_close', 'click', this.events.hideArticleOverlay).
          delegate('.article_overlay_cancel', 'click', this.events.cancelArticleOverlay).
          delegate('.article_notify', 'click', this.events.articleNotifyChanged);
      },

      'unbind_user_events': function () {
        this.container.
          undelegate('.disable', 'click', this.events.disableClick).
          undelegate('#facebook_reader_history_enabled', 'click', this.events.historyEnableClick).
          undelegate('.history_toggle', 'click', this.events.historyToggle).
          undelegate('.history .content .delete', 'click', this.events.historyDelete).
          undelegate('.confirmation_yes', 'click', this.events.confirmAdding).
          undelegate('.confirmation_no', 'click', this.events.hideConfirmationOverlay).
          undelegate('.article_overlay_close', 'click', this.events.hideArticleOverlay).
          undelegate('.article_overlay_cancel', 'click', this.events.cancelArticleOverlay).
          undelegate('.article_notify', 'click', this.events.articleNotifyChanged);
      },

      '_events': {
        'userLoad': function (response) {
          this.render_connected(
            $.parseJSON(response[0].body),
            $.parseJSON(response[1].body).data || []
          );
        },

        'disableClick': function (e) {
          e && e.preventDefault && e.preventDefault();

          FB.api("me/permissions", "DELETE", function (response) {
            window.location.reload();
          });

          this._historyWasDisabled = true
        },

        'historyEnableClick': function () {
          var input = $('#facebook_reader_history_enabled'),
              label = input.parent(),
              enabled = input.prop('checked');

          enabled ?
            this.enableHistory() :
            this.disableHistory();

          label.toggleClass('checked', enabled);
        },

        'historyHide': function () {
          this.container.find('.history .content').slideUp(200);
        },

        'historyToggle': function () {
					this.container.find('.history_toggle').toggleClass('open');	
          this.container.find('.history .content').slideToggle(200);
        },

        'articleAdded': function (response) {
          if (response.id) {
            this._current_article_id = response.id.toString();;

            var article = {
              'id': response.id,
              'time': 'только что',
              'link': document.location.href,
              'title': this.getArticleTitle()
            };

            var new_item = $('<div/>', {

              'html': template(this.TEMPLATES['history_item'], article)
            });

            this.container.find('.history .content').prepend(new_item);

            if (this._notificationsEnabled) {
              this.showArticleOverlay(article);
            };

            if (this._historyWasDisabled) {
              this.deleteArticle(this._current_article_id);
            }
          }
        },

        'historyDelete': function(e) {
          var t = $(e.target),
              container = t.closest('div.item'),
              id = container.data('id');

          this.deleteArticle(id, container);
        },

        'confirmAdding': function () {
          this.addArticle();
          this.events.hideConfirmationOverlay();
        },

        'hideConfirmationOverlay': function () {
          var self = this;

          this.confirmation_overlay.fadeOut(200, function () {
            $(this).remove();
            self.confirmation_overlay = null;
          });
        },

        'hideArticleOverlay': function () {
          var self = this;
          this.article_overlay.fadeOut(200, function () {
            $(this).remove();
            self.article_overlay = null;
          });
        },

        'cancelArticleOverlay': function () {
          this.deleteArticle(this._current_article_id);
          this.events.hideArticleOverlay();
        },

        'articleNotifyChanged': function (e) {
          var checked;
          if (e) {
            var t = $(e.target);
            checked = t.prop('checked');
          } else {
            checked = this._notificationsEnabled;
          };

          $('.article_notify').prop('checked', checked);

          this._notificationsEnabled = checked;

          if (checked) {
            deleteCookie(this.NOTIFICATION_COOKIE);
          } else {
            setCookie(this.NOTIFICATION_COOKIE);
          };
        }

      },

      'getUser': function () {
        FB.api('me', "POST",
          {
            "limit": 5,
            "batch": [
              {
                "method": "GET",
                "relative_url": "me/?fields=first_name,last_name,link,username,picture"
              },
              {
                "method": "GET",
                "relative_url": "me/news.reads?date_format=U&limit=7"
              }
            ]
          },
          this.events.userLoad
        );
      },

      'deleteArticle': function (id, item) {
        var item = item && item.length ?
            item :
            this.container.find('.history .item[data-id="' + id + '"]');

          FB.api(id.toString(), 'delete', function (response) {});
          item && item.hide(100, function () {
            item.remove();
          });
      },

      'addArticle': function () {
        var type = $('meta[property="og:type"]').attr('content');
        if (type) {
          FB.api('/me/news.reads?' + type + '=' + document.location.href, 'post', this.events.articleAdded);
        };
      },

      'getArticleTitle': function () {
        return $('meta[property="og:title"]').attr('content')
      }

    };

  })();
});
