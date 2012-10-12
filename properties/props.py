# -*- coding: utf-8 -*-
import os
import datetime

__author__ = '4ikist'

####    ttr api properties
CONSUMER_KEY = 'VbDKb4QMLwe5YsdHESNFOg'
CONSUMER_SECRET = 'cEaSWdxHnQ6I3sGYaIBufjahyDsAP0SY5lx1YCI'

#at first start, delete it values and save new (it can see in logs by similar keys):
access_token = "612776846-ZC55TSeiCvufmggMVz9ZKpbQFXodTXuA9JSq9Vee"
access_token_secret = "kxm2cuq9xNaSUBKPxIlUNJI3wKJ57VHmT0h1w1PuLWE"

#for facebook
fb_app_id = '182482928555387'
fb_app_secret = 'd8188882ccf227f3b1c1b2f31b7f4429'
fb_email = 'alexey.proskuryakov@gmail.com'
fb_pass = 'sederfes_fb#'

#for vkontakte
vk_email = 'graviti2008@yandex.ru'
vk_password = u'russian_vkрф'
vk_uid = '17489305'
vk_app_id = '3168657'
vk_app_secret = '5dRPeUXgrUYfw0hoota2'

#####   db properties
#host = '178.49.120.77'
host = 'localhost'
port = 27017
db_name = 'ttr'

#for another instance of db. for experiments. Connect must be very very fast/
local_host = 'localhost'
local_port = 27027
local_db_name = 'ttr_local'

#####   application properties
time_format = '%Y.%m.%d_%H:%M'
ttr_time_format = '%Y-%m-%d %H:%M:%S'

####    scrapper properties
def_n = 0   #default neighbourhood
relation_types = ['mentions', 'friends', 'followers']


####    diff props
#if it true - diff machine will be get users for diff from diff_users_input collection
prepared_collection = True
#if it False - get users for parameters:
timedelta = datetime.timedelta(days=10) #get users with date_touch_ between now-timedelta and now
time_start = datetime.datetime(2012, 8, 18) #
time_stop = datetime.datetime(2012, 8, 25) # and between time_start and time_stop
#bach size for users to diff machine processing
diff_batch_size = 10
#timedelta for actual state of user:
#if user have date_touch_ less than this timedelta user data in data base is actual
min_timedelta = datetime.timedelta(days=1)


####dictionaries for pymorphy
dict_en_path = os.path.join(os.path.dirname(__file__), 'dicts/en/morphs.pickle')
dict_ru_path = os.path.join(os.path.dirname(__file__), 'dicts/ru/morphs.pickle')


####    state properties
is_debug = True
is_client = True

#### visualise server gephi props
v_host = 'http://localhost:8080/workspace0?operation=updateGraph'


def is_inited():
    if len(access_token)and len(access_token_secret):
        return True
    return False


t = {u'paging': {
    u'next': u'https://graph.facebook.com/100002078473947/home?access_token=AAACl954iVXsBAMmvAuHjI4xRySbYTBexFrGM5CmYdhdXuOyLp1hCZBGSwi517gQEI8GicVA7ZCy8y4m3bQckDpvpc5WB5WMAQbfQXVegZDZD&limit=25&until=1349788907'
    ,
    u'previous': u'https://graph.facebook.com/100002078473947/home?access_token=AAACl954iVXsBAMmvAuHjI4xRySbYTBexFrGM5CmYdhdXuOyLp1hCZBGSwi517gQEI8GicVA7ZCy8y4m3bQckDpvpc5WB5WMAQbfQXVegZDZD&limit=25&since=1350023888&__previous=1'
}
    ,
     u'data':


         [{u'from': {u'name': u'Anna Zhuchkova', u'id': u'100001263853040'}, u'comments': {u'count': 0},
                u'updated_time': u'2012-10-12T06:38:08+0000',
                u'application': {u'namespace': u'instapp', u'name': u'Instagram', u'id': u'124024574287414'},
                u'created_time': u'2012-10-12T06:38:08+0000', u'type': u'link',
                u'id': u'100001263853040_452969461421845'}, {
         u'picture': u'http://platform.ak.fbcdn.net/www/app_full_proxy.php?app=45439413586&v=1&size=z&cksum=73acb497fa190bf4e28d4d3ed227353a&src=http%3A%2F%2Ftrendclub.ru%2Fupload%2Fmedia%2Fimages%2Fnartes%2Fcomix_1349981037.png'
         , u'from': {u'category': u'Science', u'name': u'TrendClub', u'id': u'189098644458980'},
         u'name': u"i don't know what is it.",
         u'actions': [{u'link': u'http://www.facebook.com/189098644458980/posts/439754829393359', u'name': u'Comment'},
                 {u'link': u'http://www.facebook.com/189098644458980/posts/439754829393359', u'name': u'Like'}],
         u'id': u'189098644458980_439754829393359',
         u'application': {u'namespace': u'rssgraffiti', u'name': u'RSS Graffiti', u'id': u'45439413586'},
         u'link': u'http://trendclub.ru/blogs/comix/8418', u'comments': {u'count': 0},
         u'created_time': u'2012-10-11T20:13:34+0000', u'updated_time': u'2012-10-11T20:13:34+0000', u'type': u'link',
         u'properties': [{u'text': u'TrendClub.ru', u'href': u'http://trendclub.ru/', u'name': u'Source'}],
         u'status_type': u'app_created_story',
         u'icon': u'http://photos-d.ak.fbcdn.net/photos-ak-snc7/v43/70/45439413586/app_2_45439413586_6053.gif'}, {
         u'from': {u'name': u'\u0414\u0430\u043d\u044c\u043a\u0430 \u0410\u0445\u043c\u0435\u0440\u043e\u0432\u0430',
                   u'id': u'1314845840'},
         u'actions': [{u'link': u'http://www.facebook.com/1314845840/posts/4807284222728', u'name': u'Comment'},
                 {u'link': u'http://www.facebook.com/1314845840/posts/4807284222728', u'name': u'Like'}],
         u'updated_time': u'2012-10-11T17:28:57+0000',
         u'application': {u'namespace': u'fbandroid', u'name': u'Facebook for Android', u'id': u'350685531728'},
         u'likes': {u'count': 3, u'data': [
                 {u'name': u'\u0415\u043b\u0435\u043d\u0430 \u042f\u0432\u043e\u0440\u0441\u043a\u0430\u044f',
                  u'id': u'100001573274189'}, {u'name': u'Maria Akhmerova', u'id': u'100001080130728'},
                 {u'name': u'Elena Koshkarova', u'id': u'100001883673075'}]},
         u'created_time': u'2012-10-11T17:28:57+0000',
         u'message': u'\u041a\u0430\u043a \u043d\u0430\u0439\u0442\u0438 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430 \u0432 \u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438\n\n#237180(2012-10-09 22:35)\n\u0425\u0425\u0425: \u0410 \u0442\u044b \u0437\u043d\u0430\u0435\u0448\u044c \u0433\u0434\u0435 ZZZ \u0441\u0438\u0434\u0438\u0442?\nYYY: \u041d\u0435\u0430.\n\u0425\u0425\u0425: \u0411\u043b\u0438\u043d. \u0423\u0436\u0435 \u043d\u0435\u0434\u0435\u043b\u044e \u0438\u0449\u0443.\nYYY: \u0422\u043e\u043b\u044c\u043a\u043e \u0430\u0439\u043f\u0438\u0448\u043d\u0438\u043a \u043c\u043e\u0433\u0443 \u043d\u0430\u0439\u0442\u0438.\n\u0425\u0425\u0425: \u0421\u043b\u0443\u0448\u0430\u0439... \u0430 \u043e\u0442\u0440\u0443\u0431\u0438 \u0435\u043c\u0443 \u0438\u043d\u0435\u0442.\nYYY: \u041d\u0430\u0445\u0435\u0440\u0430?\n\u0425\u0425\u0425: \u041e\u043d \u0432\u0430\u043c \u043f\u043e\u0437\u0432\u043e\u043d\u0438\u0442, \u0438 \u0442\u044b \u0435\u0433\u043e \u043a\u043e \u043c\u043d\u0435 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0448\u044c... :)'
         , u'type': u'status', u'id': u'1314845840_4807284222728', u'status_type': u'mobile_status_update',
         u'comments': {u'count': 0}},
             {u'picture': u'http://photos-f.ak.fbcdn.net/hphotos-ak-ash4/485857_393980944008332_552613062_s.jpg',
              u'from': {u'name': u'\u0412\u0430\u0441\u0438\u043b\u0438\u0439 \u041f\u0438\u043d\u0442\u043e\u0432',
                        u'id': u'100001892908794'}, u'name': u'ResumUP Photos', u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100001892908794/posts/393980957341664', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100001892908794/posts/393980957341664', u'name': u'Like'}],
              u'updated_time': u'2012-10-11T15:33:07+0000',
              u'application': {u'namespace': u'resumup', u'name': u'ResumUP', u'id': u'229741933727379'},
              u'link': u'http://www.facebook.com/photo.php?fbid=393980944008332&set=a.393980940674999.90586.100001892908794&type=1&relevant_count=1'
             , u'object_id': u'393980944008332', u'created_time': u'2012-10-11T15:33:07+0000',
              u'message': u"I've just joined ResumUP - it shows how to achieve your career goals! ResumUP. Know what it takes. http://resumup.com/?m_fb&user_id=11081173"
             , u'type': u'photo', u'id': u'100001892908794_393980957341664', u'status_type': u'added_photos',
              u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yz/r/StEh3RhPvjk.gif'},
             {u'picture': u'http://photos-g.ak.fbcdn.net/hphotos-ak-snc6/261828_209016432565205_1272167166_s.jpg',
              u'story': u"Julia  Sannikova shared \u0421\u0435\u043a\u0440\u0435\u0442\u044b \u0443\u0441\u043f\u0435\u0445\u0430 \u0412\u0435\u043b\u0438\u043a\u0438\u0445's photo."
             , u'likes': {u'count': 2, u'data': [{u'name': u'Maria Smolskaya', u'id': u'1540249634'},
                 {u'name': u'Vyacheslav Kim', u'id': u'100000721558087'}]},
              u'from': {u'name': u'Julia  Sannikova', u'id': u'100002278454997'}, u'name': u'Wall Photos',
              u'application': {u'name': u'Links', u'id': u'2309869772'}, u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100002278454997/posts/234605010001532', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100002278454997/posts/234605010001532', u'name': u'Like'}],
              u'properties': [{
                  u'text': u'\u0421\u0435\u043a\u0440\u0435\u0442\u044b \u0443\u0441\u043f\u0435\u0445\u0430 \u0412\u0435\u043b\u0438\u043a\u0438\u0445'
                  , u'href': u'http://www.facebook.com/SecretiUspexa.V?ref=stream', u'name': u'By'}],
              u'caption': u'\u0425\u043e\u0442\u0438\u0442\u0435 \u043d\u0430\u0441 \u0447\u0438\u0442\u0430\u0442\u044c, \u0442\u043e\u0433\u0434\u0430 \u0437\u0430\u0439\u0434\u0438\u0442\u0435 \u043d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443 \u0438 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u043d\u0430 Like!!!\r\nhttp://www.facebook.com/pages/\u0421\u0435\u043a\u0440\u0435\u0442\u044b-\u0443\u0441\u043f\u0435\u0445\u0430-\u0412\u0435\u043b\u0438\u043a\u0438\u0445/142419012558281\r\n\r\n\u041f\u043e\u043d\u0440\u0430\u0432\u0438\u043b\u0441\u044f \u043f\u043e\u0441\u0442, \u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u043f\u043e\u0434\u0435\u043b\u0438\u0442\u0435\u0441\u044c \u0441 \u0434\u0440\u0443\u0437\u044c\u044f\u043c\u0438!!!'
             ,
              u'link': u'http://www.facebook.com/photo.php?fbid=209016432565205&set=a.142423039224545.30295.142419012558281&type=1'
             , u'object_id': u'209016432565205', u'shares': {u'count': 2}, u'story_tags': {u'24': [
                 {u'length': 22, u'offset': 24, u'type': u'page', u'id': u'142419012558281',
                  u'name': u'\u0421\u0435\u043a\u0440\u0435\u0442\u044b \u0443\u0441\u043f\u0435\u0445\u0430 \u0412\u0435\u043b\u0438\u043a\u0438\u0445'}]
             , u'0': [{u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100002278454997',
                       u'name': u'Julia  Sannikova'}]}, u'created_time': u'2012-10-11T15:22:36+0000',
              u'updated_time': u'2012-10-11T15:22:36+0000', u'type': u'photo', u'id': u'100002278454997_234605010001532'
             ,
              u'status_type': u'shared_story', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'},
             {u'picture': u'http://profile.ak.fbcdn.net/hprofile-ak-snc7/373481_290001094358147_36010510_q.jpg',
              u'story': u'Julia  Sannikova shared "\u041d\u0415" \u043f\u0441\u0438\u0445\u0443\u0439\'s status update.'
             ,
              u'from': {u'name': u'Julia  Sannikova', u'id': u'100002278454997'},
              u'name': u'"\u041d\u0415" \u043f\u0441\u0438\u0445\u0443\u0439',
              u'actions': [
                      {u'link': u'http://www.facebook.com/100002278454997/posts/420137598035285', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100002278454997/posts/420137598035285', u'name': u'Like'}],
              u'updated_time': u'2012-10-11T15:22:09+0000', u'application': {u'name': u'Links', u'id': u'2309869772'},
              u'link': u'http://www.facebook.com/NEpsikhui/posts/497318230293098', u'comments': {u'count': 0},
              u'story_tags': {u'24': [{u'length': 11, u'offset': 24, u'type': u'page', u'id': u'290001094358147',
                                       u'name': u'"\u041d\u0415" \u043f\u0441\u0438\u0445\u0443\u0439'}], u'0': [
                      {u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100002278454997',
                       u'name': u'Julia  Sannikova'}]}, u'created_time': u'2012-10-11T15:22:09+0000',
              u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif', u'type': u'link',
              u'id': u'100002278454997_420137598035285', u'status_type': u'shared_story',
              u'description': u'\u0414\u0430\u0432\u0430\u0439\u0442\u0435 \u0441\u0440\u0430\u0437\u0443 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u043c\u0441\u044f - \u044f \u0432\u0430\u043c \u043d\u0443\u0436\u043d\u0430 \u0434\u043b\u044f \u043f\u043e\u043b\u043d\u043e\u0433\u043e \u0441\u0447\u0430\u0441\u0442\u044c\u044f \u0438\u043b\u0438 \u0434\u043b\u044f \u0440\u043e\u0432\u043d\u043e\u0433\u043e \u0441\u0447\u0435\u0442\u0430?'}
         , {
             u'picture': u'http://platform.ak.fbcdn.net/www/app_full_proxy.php?app=2231777543&v=1&size=z&cksum=0e180bd78fff1274af175ccca2e29194&src=http%3A%2F%2Fnews.bbcimg.co.uk%2Fmedia%2Fimages%2F63338000%2Fjpg%2F_63338923_63338767.jpg'
             , u'from': {u'name': u'Jennifer Trelewicz', u'id': u'520831766'},
             u'name': u'Rebel sticker craze on the Tube',
             u'application': {u'namespace': u'twitter', u'name': u'Twitter', u'id': u'2231777543'},
             u'actions': [{u'link': u'http://www.facebook.com/520831766/posts/10151050533811767', u'name': u'Comment'},
                     {u'link': u'http://www.facebook.com/520831766/posts/10151050533811767', u'name': u'Like'}, {
                     u'link': u'https://twitter.com/trelevich?utm_source=fb&utm_medium=fb&utm_campaign=trelevich&utm_content=256337510907658242'
                     , u'name': u'@trelevich on Twitter'}], u'updated_time': u'2012-10-11T10:16:42+0000',
             u'caption': u'bbc.in', u'link': u'http://t.co/KOBoMsaL', u'comments': {u'count': 0},
             u'created_time': u'2012-10-11T10:16:42+0000',
             u'message': u"BBC News - Guerrilla sticker craze hits London's Tube http://t.co/KOBoMsaL",
             u'icon': u'http://photos-d.ak.fbcdn.net/photos-ak-snc7/v85006/23/2231777543/app_2_2231777543_2016407632.gif'
             ,
             u'type': u'link', u'id': u'520831766_10151050533811767', u'status_type': u'app_created_story',
             u'description': u'Some commuters are noticing an increase in subversive guerrilla stickers appearing on the London Underground network.'}
         , {u'picture': u'http://photos-g.ak.fbcdn.net/hphotos-ak-prn1/550678_248766845246607_344793268_s.jpg',
            u'story': u"Stepan Volkov shared ImproveIT's photo.",
            u'from': {u'name': u'Stepan Volkov', u'id': u'1507167662'},
            u'name': u'Wall Photos', u'application': {u'name': u'Links', u'id': u'2309869772'},
            u'comments': {u'count': 0},
            u'actions': [{u'link': u'http://www.facebook.com/1507167662/posts/430768836986549', u'name': u'Comment'},
                    {u'link': u'http://www.facebook.com/1507167662/posts/430768836986549', u'name': u'Like'}],
            u'properties': [
                    {u'text': u'ImproveIT', u'href': u'http://www.facebook.com/improveitgroup?ref=stream',
                     u'name': u'By'}],
            u'caption': u'\u0421\u0435\u043a\u0440\u0435\u0442\u043d\u044b\u0435 \u043a\u0430\u0434\u0440\u044b \u0438\u0437 \u043d\u0430\u0448\u0435\u0439 \u043c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u0445\u0440\u043e\u043d\u0438\u043a\u0438 - \u043a\u0430\u043a \u044d\u0442\u043e \u0431\u044b\u043b\u043e \u0438 \u0447\u0442\u043e \u043c\u044b \u0442\u0430\u043c \u0434\u0435\u043b\u0430\u043b\u0438 http://bit.ly/T7IYcI @[430140197015808:274:\u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0439 \u0410\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044c\u043d\u044b\u0439 \u0421\u0430\u043b\u043e\u043d]'
             ,
            u'link': u'http://www.facebook.com/photo.php?fbid=248766845246607&set=a.156554904467802.30211.147015708755055&type=1'
             , u'object_id': u'248766845246607', u'story_tags': {
                 u'0': [{u'length': 13, u'offset': 0, u'type': u'user', u'id': u'1507167662',
                         u'name': u'Stepan Volkov'}],
                 u'21': [{u'length': 9, u'offset': 21, u'type': u'page', u'id': u'147015708755055',
                          u'name': u'ImproveIT'}]},
            u'created_time': u'2012-10-11T08:51:50+0000', u'updated_time': u'2012-10-11T08:51:50+0000',
            u'type': u'photo',
            u'id': u'1507167662_430768836986549', u'status_type': u'shared_story',
            u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'}, {
             u'from': {u'name': u'\u0414\u0430\u043d\u044c\u043a\u0430 \u0410\u0445\u043c\u0435\u0440\u043e\u0432\u0430'
                 ,
                       u'id': u'1314845840'}, u'comments': {u'count': 0}, u'updated_time': u'2012-10-11T07:34:11+0000',
             u'application': {u'namespace': u'likes', u'name': u'Likes', u'id': u'193048140809145'},
             u'created_time': u'2012-10-11T07:34:11+0000', u'type': u'link', u'id': u'1314845840_4805179970123'},
             {u'picture': u'http://photos-e.ak.fbcdn.net/hphotos-ak-prn1/30970_344331678995921_1713390319_s.jpg',
              u'story': u"Dina Tushinskaya shared Photography's photo.",
              u'likes': {u'count': 1, u'data': [{u'name': u'Dina Tushinskaya', u'id': u'100001794014548'}]},
              u'from': {u'name': u'Dina Tushinskaya', u'id': u'100001794014548'}, u'name': u'Wall Photos',
              u'application': {u'name': u'Photos', u'id': u'2305272732'}, u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100001794014548/posts/373774172700452', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100001794014548/posts/373774172700452', u'name': u'Like'}],
              u'properties': [
                      {u'text': u'Photography', u'href': u'http://www.facebook.com/FFotograf?ref=stream',
                       u'name': u'By'}],
              u'caption': u'LOL',
              u'link': u'http://www.facebook.com/photo.php?fbid=344331678995921&set=a.170645353031222.37167.168524003243357&type=1'
             , u'object_id': u'344331678995921', u'story_tags': {
             u'24': [{u'length': 11, u'offset': 24, u'type': u'page', u'id': u'168524003243357',
                      u'name': u'Photography'}],
             u'0': [{u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100001794014548',
                     u'name': u'Dina Tushinskaya'}]}, u'created_time': u'2012-10-11T04:39:42+0000',
              u'updated_time': u'2012-10-11T04:39:42+0000', u'type': u'photo', u'id': u'100001794014548_373774172700452'
             ,
              u'status_type': u'shared_story', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'},
             {u'picture': u'http://profile.ak.fbcdn.net/hprofile-ak-ash4/369648_100001588370098_1762188037_q.jpg',
              u'story': u"\u041b\u0435\u043d\u0430 \u0428\u043a\u0430\u0440\u0443\u0431\u043e shared Gleb Tertychny's status update."
             , u'from': {u'name': u'\u041b\u0435\u043d\u0430 \u0428\u043a\u0430\u0440\u0443\u0431\u043e',
                         u'id': u'100000757994691'}, u'name': u'Gleb Tertychny', u'comments': {u'count': 1, u'data': [
                 {u'created_time': u'2012-10-11T05:09:17+0000',
                  u'message': u'Planet is fine, people are fucked. \u0410 \u0442\u0430\u043a \u0436\u0435 \u043f\u043b\u0430\u043d\u0435\u0442\u0435 \u043d\u0443\u0436\u043d\u044b \u0434\u0435\u043d\u044c\u0433\u0438 \u043d\u0430 \u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0435\u043d\u0438\u0435 \u0432\u043e\u043e\u0440\u0443\u0436\u0435\u043d\u043d\u043e\u0433\u043e \u0441\u043e\u043f\u0440\u043e\u0442\u0438\u0432\u043b\u0435\u043d\u0438\u044f \u043a\u0438\u0442\u0430\u044e \u0447\u0442\u043e\u0431\u044b \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0440\u0430\u0431\u043e\u0432\u043b\u0430\u0434\u0435\u043b\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u0442\u0440\u043e\u0439 \u0432 \u0442\u0438\u0431\u0435\u0442\u0435.'
                 , u'from': {u'name': u'Kirill Pisman', u'id': u'100001617260276'},
                  u'id': u'100000757994691_535604203120283_108645819'}]},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100000757994691/posts/535604203120283', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100000757994691/posts/535604203120283', u'name': u'Like'}],
              u'updated_time': u'2012-10-11T05:09:17+0000', u'application': {u'name': u'Status', u'id': u'25554907596'},
              u'link': u'http://www.facebook.com/gleb.tertichny/posts/424008527662089',
              u'likes': {u'count': 7, u'data': [
                      {u'name': u'Alexander Lyskovsky', u'id': u'100000448302204'},
                      {u'name': u'Dmitry Smirnov', u'id': u'1072778551'},
                      {u'name': u'Vadim  Krivenko', u'id': u'100002376077552'}
                  , {u'name': u'Eray Alperenkent', u'id': u'100002509218275'}]}, u'story_tags': {u'0': [
                 {u'length': 12, u'offset': 0, u'type': u'user', u'id': u'100000757994691',
                  u'name': u'\u041b\u0435\u043d\u0430 \u0428\u043a\u0430\u0440\u0443\u0431\u043e'}], u'20': [
                 {u'length': 14, u'offset': 20, u'type': u'user', u'id': u'100001588370098',
                  u'name': u'Gleb Tertychny'}]},
              u'created_time': u'2012-10-11T04:16:07+0000',
              u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif', u'type': u'link',
              u'id': u'100000757994691_535604203120283', u'status_type': u'shared_story',
              u'description': u'\u041f\u043b\u0430\u043d\u0435\u0442\u0435 \u043d\u0435 \u043d\u0443\u0436\u043d\u043e \u0431\u043e\u043b\u044c\u0448\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e "\u0443\u0441\u043f\u0435\u0448\u043d\u044b\u0445 \u043b\u044e\u0434\u0435\u0439". \u041f\u043b\u0430\u043d\u0435\u0442\u0430 \u043e\u0442\u0447\u0430\u044f\u043d\u043d\u043e \u043d\u0443\u0436\u0434\u0430\u0435\u0442\u0441\u044f \u0432 \u043c\u0438\u0440\u043e\u0442\u0432\u043e\u0440\u0446\u0430\u0445, \u0446\u0435\u043b\u0438\u0442\u0435\u043b\u044f\u0445, \u0440\u0435\u0441\u0442\u0430\u0432\u0440\u0430\u0442\u043e\u0440\u0430\u0445, \u0440\u0430\u0441\u0441\u043a\u0430\u0437\u0447\u0438\u043a\u0430\u0445 \u0438 \u043b\u044e\u0431\u044f\u0449\u0438\u0445 \u0432\u0441\u0435\u0445 \u0432\u0438\u0434\u043e\u0432. \u041e\u043d\u0430 \u043d\u0443\u0436\u0434\u0430\u0435\u0442\u0441\u044f \u0432 \u043b\u044e\u0434\u044f\u0445, \u0440\u044f\u0434\u043e\u043c \u0441 \u043a\u043e\u0442\u043e\u0440\u044b\u043c\u0438 \u0445\u043e\u0440\u043e\u0448\u043e \u0436\u0438\u0442\u044c. \u041f\u043b\u0430\u043d\u0435\u0442\u0430 \u043d\u0443\u0436\u0434\u0430\u0435\u0442\u0441\u044f \u0432 \u043b\u044e\u0434\u044f\u0445 \u0441 \u043c\u043e\u0440\u0430\u043b\u044c\u044e, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0433\u043e\u0442\u043e\u0432\u044b \u0432\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u0432 \u0431\u043e\u0440\u044c\u0431\u0443, \u0447\u0442\u043e\u0431\u044b \u0441\u0434\u0435\u043b\u0430\u0442\u044c \u043c\u0438\u0440 \u0436\u0438\u0432\u044b\u043c \u0438 \u0433\u0443\u043c\u0430\u043d\u043d\u044b\u043c. \u0410 \u044d\u0442\u0438 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430 \u0438\u043c\u0435\u044e\u0442 \u043c\u0430\u043b\u043e \u043e\u0431\u0449\u0435\u0433\u043e \u0441 "\u0443\u0441\u043f\u0435\u0445\u043e\u043c", \u043a\u0430\u043a \u043e\u043d \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u0442\u0441\u044f \u0432 \u043d\u0430\u0448\u0435\u043c \u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0435. \xa9\u0414\u0430\u043b\u0430\u0439 \u041b\u0430\u043c\u0430'}
         , {u'story': u'Dina Tushinskaya likes her own link.',
            u'from': {u'name': u'Dina Tushinskaya', u'id': u'100001794014548'}, u'comments': {u'count': 0},
            u'updated_time': u'2012-10-11T03:15:35+0000', u'story_tags': {u'0': [
                     {u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100001794014548',
                      u'name': u'Dina Tushinskaya'}]}, u'created_time': u'2012-10-11T03:15:35+0000', u'type': u'status',
            u'id': u'100001794014548_153330321478619'},
             {u'picture': u'http://photos-g.ak.fbcdn.net/hphotos-ak-ash3/522253_477119315661464_2100727422_s.jpg',
              u'story': u"Julia  Sannikova shared design-dautore.com's photo.",
              u'updated_time': u'2012-10-10T16:02:36+0000',
              u'from': {u'name': u'Julia  Sannikova', u'id': u'100002278454997'},
              u'name': u'ECOdesign - Recycle, Reuse, Sustainability in Design 2',
              u'likes': {u'count': 1, u'data': [{u'name': u'Vyacheslav Kim', u'id': u'100000721558087'}]},
              u'application': {u'name': u'Photos', u'id': u'2305272732'}, u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100002278454997/posts/123156157834906', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100002278454997/posts/123156157834906', u'name': u'Like'}],
              u'properties': [
                      {u'text': u'design-dautore.com', u'href': u'http://www.facebook.com/designdautore?ref=stream',
                       u'name': u'By'}], u'caption': u'MIMI Table Lamp by Kozo Lamp (o',
              u'link': u'http://www.facebook.com/photo.php?fbid=477119315661464&set=a.215542878485777.62494.112397672133632&type=1'
             , u'object_id': u'477119315661464', u'story_tags': {u'24': [
                 {u'length': 18, u'offset': 24, u'type': u'page', u'id': u'112397672133632',
                  u'name': u'design-dautore.com'}]
             , u'0': [{u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100002278454997',
                       u'name': u'Julia  Sannikova'}]}, u'created_time': u'2012-10-10T16:02:36+0000',
              u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif', u'type': u'photo',
              u'id': u'100002278454997_123156157834906', u'status_type': u'shared_story',
              u'description': u'SEE https://www.facebook.com/media/set/?set=a.119776014729131.8942.112397672133632'},
             {u'picture': u'http://photos-a.ak.fbcdn.net/hphotos-ak-ash4/249397_485745494778985_911076366_s.jpg',
              u'story': u"Julia  Sannikova shared \u0421\u043b\u043e\u0432\u0430, \u043d\u0435\u043f\u043e\u0434\u0432\u043b\u0430\u0441\u0442\u043d\u044b\u0435 \u0432\u0440\u0435\u043c\u0435\u043d\u0438's photo."
             , u'likes': {u'count': 1, u'data': [{u'name': u'Maria Smolskaya', u'id': u'1540249634'}]},
              u'from': {u'name': u'Julia  Sannikova', u'id': u'100002278454997'}, u'name': u'Wall Photos',
              u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100002278454997/posts/232206903573857', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100002278454997/posts/232206903573857', u'name': u'Like'}],
              u'properties': [{
                  u'text': u'\u0421\u043b\u043e\u0432\u0430, \u043d\u0435\u043f\u043e\u0434\u0432\u043b\u0430\u0441\u0442\u043d\u044b\u0435 \u0432\u0440\u0435\u043c\u0435\u043d\u0438'
                  , u'href': u'http://www.facebook.com/OneTezcan?ref=stream', u'name': u'By'}],
              u'application': {u'name': u'Photos', u'id': u'2305272732'},
              u'link': u'http://www.facebook.com/photo.php?fbid=485745494778985&set=a.170386849648186.34190.170377179649153&type=1'
             , u'object_id': u'485745494778985', u'story_tags': {u'24': [
                 {u'length': 28, u'offset': 24, u'type': u'page', u'id': u'170377179649153',
                  u'name': u'\u0421\u043b\u043e\u0432\u0430, \u043d\u0435\u043f\u043e\u0434\u0432\u043b\u0430\u0441\u0442\u043d\u044b\u0435 \u0432\u0440\u0435\u043c\u0435\u043d\u0438'}]
             , u'0': [{u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100002278454997',
                       u'name': u'Julia  Sannikova'}]}, u'created_time': u'2012-10-10T16:00:44+0000',
              u'updated_time': u'2012-10-10T16:00:44+0000', u'type': u'photo', u'id': u'100002278454997_232206903573857'
             ,
              u'status_type': u'shared_story', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'},
             {u'picture': u'http://photos-b.ak.fbcdn.net/hphotos-ak-ash4/430536_279441368841769_439762551_s.jpg',
              u'story': u"Julia  Sannikova shared Oksana Ksenya's photo.",
              u'from': {u'name': u'Julia  Sannikova', u'id': u'100002278454997'}, u'name': u'Wall Photos',
              u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100002278454997/posts/438274842895463', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100002278454997/posts/438274842895463', u'name': u'Like'}],
              u'properties': [{u'text': u'Oksana Ksenya', u'href': u'http://www.facebook.com/oksana.kavetskapertsovych',
                               u'name': u'By'}], u'application': {u'name': u'Links', u'id': u'2309869772'},
              u'link': u'http://www.facebook.com/photo.php?fbid=279441368841769&set=a.114638361988738.15260.100003277247294&type=1'
             , u'object_id': u'279441368841769', u'story_tags': {
             u'24': [{u'length': 13, u'offset': 24, u'type': u'user', u'id': u'100003277247294',
                      u'name': u'Oksana Ksenya'}],
             u'0': [{u'length': 16, u'offset': 0, u'type': u'user', u'id': u'100002278454997',
                     u'name': u'Julia  Sannikova'}]}, u'created_time': u'2012-10-10T16:00:14+0000',
              u'message': u'\u043a\u0430\u043a \u0432\u0441\u0442\u0440\u0435\u0442\u044f\u0442... \u043c\u043c\u043c...))'
             ,
              u'updated_time': u'2012-10-10T16:00:14+0000', u'type': u'photo', u'id': u'100002278454997_438274842895463'
             ,
              u'status_type': u'shared_story', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'},
             {u'picture': u'http://photos-g.ak.fbcdn.net/hphotos-ak-snc6/261841_395997023801828_1786213778_s.jpg',
              u'likes': {u'count': 3, u'data': [{u'name': u'Helen  Malakhina', u'id': u'100003143136070'},
                      {u'name': u'Evgeniy Petrenko', u'id': u'100002100867608'},
                      {u'name': u'Mikhail Vavilov', u'id': u'847675646'}]},
              u'from': {u'category': u'Internet/software', u'name': u'WebProfessionals.ru', u'id': u'101556639912536'},
              u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/101556639912536/posts/395997043801826', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/101556639912536/posts/395997043801826', u'name': u'Like'}],
              u'updated_time': u'2012-10-10T15:18:14+0000',
              u'link': u'http://www.facebook.com/photo.php?fbid=395997023801828&set=a.114641618604038.15296.101556639912536&type=1&relevant_count=1'
             , u'object_id': u'395997023801828', u'created_time': u'2012-10-10T15:18:14+0000',
              u'message': u'\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0438 \u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0438\u0445 Windows Phone-\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u043e\u0432.\r\n\r\n\u041e\u0442\u043b\u0438\u0447\u043d\u043e\u0435 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u0434\u043b\u044f \u0432\u0441\u0435\u0445, \u043a\u0442\u043e \u0445\u043e\u0447\u0435\u0442 \u043f\u043e\u043f\u0440\u043e\u0431\u043e\u0432\u0430\u0442\u044c \u0441\u0432\u043e\u0438 \u0441\u0438\u043b\u044b \u0432 Windows 8, \u043d\u043e \u043f\u043e \u043a\u0430\u043a\u043e\u0439\u2013\u0442\u043e \u043f\u0440\u0438\u0447\u0438\u043d\u0435 \u0435\u0449\u0435 \u043d\u0435 \u0440\u0435\u0448\u0438\u043b\u0441\u044f \u043d\u0430 \u044d\u0442\u043e. Microsoft \u043f\u0440\u0438\u0433\u043b\u0430\u0448\u0430\u0435\u0442 \u0432\u0441\u0435\u0445 \u0436\u0435\u043b\u0430\u044e\u0449\u0438\u0445 \u043f\u0440\u0438\u043d\u044f\u0442\u044c \u0443\u0447\u0430\u0441\u0442\u0438\u0435 \u0432 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0438, \u0432\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0435\u0439 \u0432 \u0441\u0435\u0431\u044f \u043e\u043f\u043b\u0430\u0442\u0443 \u0440\u0430\u0431\u043e\u0442\u044b \u0434\u0438\u0437\u0430\u0439\u043d\u0435\u0440\u0441\u043a\u043e\u0433\u043e \u0430\u0433\u0435\u043d\u0442\u0441\u0442\u0432\u0430, \u043a\u043e\u043d\u0441\u0443\u043b\u044c\u0442\u0430\u0446\u0438\u0438 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u0432 \u0438 \u043f\u043e\u043c\u043e\u0449\u044c \u0432 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f. \u0421\u043f\u0435\u0448\u0438\u0442\u0435 \u0443\u0447\u0430\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c!\r\nhttp://habrahabr.ru/company/microsoft/blog/154145/'
             , u'type': u'photo', u'id': u'101556639912536_395997043801826', u'status_type': u'added_photos',
              u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yz/r/StEh3RhPvjk.gif'}, {
             u'story': u'Denis Proskuryakov answered \u041b\u0443\u0447\u0448\u0438\u0439 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044c \u0434\u043b\u044f \u0436\u0435\u043d\u0449\u0438\u043d. \u0412\u0430\u0448\u0435 \u043c\u043d\u0435\u043d\u0438\u0435: with Mini Cooper.'
             , u'from': {u'name': u'Denis Proskuryakov', u'id': u'100001247606379'}, u'object_id': u'453122624740098',
             u'updated_time': u'2012-10-10T14:43:35+0000',
             u'application': {u'name': u'Questions', u'id': u'10150110253435258'}, u'comments': {u'count': 0},
             u'story_tags': {u'0': [{u'length': 18, u'offset': 0, u'type': u'user', u'id': u'100001247606379',
                                     u'name': u'Denis Proskuryakov'}], u'28': [
                     {u'length': 42, u'offset': 28, u'id': u'453122624740098',
                      u'name': u'\u041b\u0443\u0447\u0448\u0438\u0439 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044c \u0434\u043b\u044f \u0436\u0435\u043d\u0449\u0438\u043d. \u0412\u0430\u0448\u0435 \u043c\u043d\u0435\u043d\u0438\u0435:'}]
                 , u'76': [{u'length': 11, u'offset': 76, u'id': u'414752961912227', u'name': u'Mini Cooper'}]},
             u'created_time': u'2012-10-10T14:43:35+0000', u'type': u'question',
             u'id': u'100001247606379_447542508630665',
             u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yg/r/5PpICR5KcPe.png'}, {
             u'story': u'Denis Proskuryakov answered \u0420\u0430\u0441\u0445\u043e\u0434 \u0431\u0435\u043d\u0437\u0438\u043d\u0430 - \u044d\u0442\u043e \u0432\u0430\u0436\u043d\u044b\u0439 \u0434\u043b\u044f \u0432\u0430\u0441 \u0444\u0430\u043a\u0442\u043e\u0440 \u043f\u0440\u0438 \u0432\u044b\u0431\u043e\u0440\u0435 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044f? with \u041d\u0435\u0442, \u044f \u043d\u0430 \u043d\u0435\u0433\u043e \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u044f \u043d\u0435 \u043e\u0431\u0440\u0430\u0449\u0430\u044e.'
             , u'from': {u'name': u'Denis Proskuryakov', u'id': u'100001247606379'}, u'object_id': u'453113361407691',
             u'updated_time': u'2012-10-10T14:43:15+0000',
             u'application': {u'name': u'Questions', u'id': u'10150110253435258'}, u'comments': {u'count': 0},
             u'story_tags': {u'99': [{u'length': 34, u'offset': 99, u'id': u'362786650471076',
                                      u'name': u'\u041d\u0435\u0442, \u044f \u043d\u0430 \u043d\u0435\u0433\u043e \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u044f \u043d\u0435 \u043e\u0431\u0440\u0430\u0449\u0430\u044e'}]
                 , u'0': [{u'length': 18, u'offset': 0, u'type': u'user', u'id': u'100001247606379',
                           u'name': u'Denis Proskuryakov'}], u'28': [
                         {u'length': 65, u'offset': 28, u'id': u'453113361407691',
                          u'name': u'\u0420\u0430\u0441\u0445\u043e\u0434 \u0431\u0435\u043d\u0437\u0438\u043d\u0430 - \u044d\u0442\u043e \u0432\u0430\u0436\u043d\u044b\u0439 \u0434\u043b\u044f \u0432\u0430\u0441 \u0444\u0430\u043a\u0442\u043e\u0440 \u043f\u0440\u0438 \u0432\u044b\u0431\u043e\u0440\u0435 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044f?'}]}
             , u'created_time': u'2012-10-10T14:43:15+0000', u'type': u'question',
             u'id': u'100001247606379_447542418630674',
             u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yg/r/5PpICR5KcPe.png'}, {
             u'story': u'Denis Proskuryakov answered \u0418\u0437-\u0437\u0430 \u0447\u0435\u0433\u043e \u043d\u0435 \u0445\u0432\u0430\u0442\u0430\u0435\u0442 \u043f\u0430\u0440\u043a\u043e\u0432\u043e\u0447\u043d\u044b\u0445 \u043c\u0435\u0441\u0442? with \u0418\u0437-\u0437\u0430 \u0442\u043e\u0433\u043e, \u0447\u0442\u043e \u043c\u0435\u0441\u0442 \u0432 \u043f\u0440\u0438\u043d\u0446\u0438\u043f\u0435 \u043c\u0430\u043b\u043e.'
             , u'from': {u'name': u'Denis Proskuryakov', u'id': u'100001247606379'}, u'object_id': u'453140921404935',
             u'updated_time': u'2012-10-10T14:43:01+0000',
             u'application': {u'name': u'Questions', u'id': u'10150110253435258'}, u'comments': {u'count': 0},
             u'story_tags': {u'73': [{u'length': 36, u'offset': 73, u'id': u'532298816795811',
                                      u'name': u'\u0418\u0437-\u0437\u0430 \u0442\u043e\u0433\u043e, \u0447\u0442\u043e \u043c\u0435\u0441\u0442 \u0432 \u043f\u0440\u0438\u043d\u0446\u0438\u043f\u0435 \u043c\u0430\u043b\u043e'}]
                 , u'0': [{u'length': 18, u'offset': 0, u'type': u'user', u'id': u'100001247606379',
                           u'name': u'Denis Proskuryakov'}], u'28': [
                         {u'length': 39, u'offset': 28, u'id': u'453140921404935',
                          u'name': u'\u0418\u0437-\u0437\u0430 \u0447\u0435\u0433\u043e \u043d\u0435 \u0445\u0432\u0430\u0442\u0430\u0435\u0442 \u043f\u0430\u0440\u043a\u043e\u0432\u043e\u0447\u043d\u044b\u0445 \u043c\u0435\u0441\u0442?'}]}
             , u'created_time': u'2012-10-10T14:43:01+0000', u'type': u'question',
             u'id': u'100001247606379_447542338630682',
             u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yg/r/5PpICR5KcPe.png'},
             {u'picture': u'http://photos-h.ak.fbcdn.net/hphotos-ak-ash4/307910_4942210512506_976930309_s.jpg',
              u'story': u'Yekaterina Zhmud added a new photo.', u'likes': {u'count': 3, u'data': [
                 {u'name': u'Sam Faktorovich', u'id': u'1123346110'},
                 {u'name': u'Anastacia Seretkina', u'id': u'100000936776152'},
                 {u'name': u'Egor Aprelsky', u'id': u'100000073039015'}]},
              u'from': {u'name': u'Yekaterina Zhmud', u'id': u'1216003625'}, u'comments': {u'count': 1, u'data': [
                 {u'created_time': u'2012-10-10T13:27:29+0000',
                  u'message': u'\u043a\u0440\u0430\u0441\u0438\u0432\u043e!',
                  u'from': {u'name': u'Anastacia Seretkina', u'id': u'100000936776152'},
                  u'id': u'1216003625_4942213792588_3384815'}]},
              u'actions': [{u'link': u'http://www.facebook.com/1216003625/posts/4942213792588', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/1216003625/posts/4942213792588', u'name': u'Like'}],
              u'updated_time': u'2012-10-10T13:27:29+0000',
              u'link': u'http://www.facebook.com/photo.php?fbid=4942210512506&set=a.4942209992493.2200992.1216003625&type=1&relevant_count=1'
             , u'object_id': u'4942210512506', u'story_tags': {
             u'0': [{u'length': 16, u'offset': 0, u'type': u'user', u'id': u'1216003625',
                     u'name': u'Yekaterina Zhmud'}]},
              u'created_time': u'2012-10-10T11:18:25+0000', u'type': u'photo', u'id': u'1216003625_4942213792588',
              u'status_type': u'added_photos', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yz/r/StEh3RhPvjk.gif'},
             {u'picture': u'http://photos-a.ak.fbcdn.net/hphotos-ak-snc7/576323_465376216835501_678122576_s.jpg',
              u'story': u"Golneva  Olya shared \u041a\u0430\u0434\u0440\u043e\u0432\u043e\u0435 \u0410\u0433\u0435\u043d\u0442\u0441\u0442\u0432\u043e \u0410\u043b\u0435\u043a\u0441\u0435\u044f \u0421\u0443\u0445\u043e\u0440\u0443\u043a\u043e\u0432\u0430's photo."
             , u'from': {u'name': u'Golneva  Olya', u'id': u'100001892712878'}, u'name': u'Wall Photos',
              u'application': {u'name': u'Photos', u'id': u'2305272732'}, u'comments': {u'count': 0},
              u'actions': [
                      {u'link': u'http://www.facebook.com/100001892712878/posts/478780305489886', u'name': u'Comment'},
                      {u'link': u'http://www.facebook.com/100001892712878/posts/478780305489886', u'name': u'Like'}],
              u'properties': [{
                  u'text': u'\u041a\u0430\u0434\u0440\u043e\u0432\u043e\u0435 \u0410\u0433\u0435\u043d\u0442\u0441\u0442\u0432\u043e \u0410\u043b\u0435\u043a\u0441\u0435\u044f \u0421\u0443\u0445\u043e\u0440\u0443\u043a\u043e\u0432\u0430'
                  , u'href': u'http://www.facebook.com/kaasuhorukova?ref=stream', u'name': u'By'}],
              u'caption': u'\u0422\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f QA-\u0438\u043d\u0436\u0435\u043d\u0435\u0440 \u0441\u043e \u0437\u043d\u0430\u043d\u0438\u0435\u043c Java, \u0438\u043d\u0436\u0435\u043d\u0435\u0440 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u0438 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044f \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430\r\n\r\n\u041e\u0431\u044f\u0437\u0430\u043d\u043d\u043e\u0441\u0442\u0438: \u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0442\u0435\u0441\u0442\u043e\u0432 \u043d\u0430 Java + Selenium; \r\n\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0439 \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430; \r\n\u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u0438 \u0443\u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u0441\u0442\u0432\u043e\u0432\u0430\u043d\u0438\u0435 \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432 \u0438 \u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u044b \u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f; \r\n\u0410\u043d\u0430\u043b\u0438\u0437 \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u0439 \u0438 \u0434\u0438\u0437\u0430\u0439\u043d \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u0438.\r\n\r\n\u0422\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u044f: \u041d\u0435 \u043c\u0435\u043d\u0435\u0435 \u0433\u043e\u0434\u0430 \u0432 \u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u0438 \u0438\u043d\u0436\u0435\u043d\u0435\u0440\u0430 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u0438 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044f \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430;\r\n\u041e\u043f\u044b\u0442 \u0437\u0430\u043f\u0443\u0441\u043a\u0430 \u0438 \u0430\u043d\u0430\u043b\u0438\u0437\u0430 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0442\u0435\u0441\u0442\u043e\u0432\u044b\u0445 \u043f\u0440\u043e\u0446\u0435\u0434\u0443\u0440 \u0438 \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f;\r\n\u0411\u0430\u0437\u043e\u0432\u044b\u0439 \u043e\u043f\u044b\u0442 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0430 Java; \r\n\u041d\u0430\u0432\u044b\u043a\u0438 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u0438 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f Windows, Linux \u0438 SQL; \u0417\u043d\u0430\u043d\u0438\u0435 \u0441\u0435\u0442\u0435\u0432\u044b\u0445 \u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u043e\u0432, \u043f\u0440\u0438\u043d\u0446\u0438\u043f\u043e\u0432 \u0440\u0430\u0431\u043e\u0442\u044b \u0441\u0435\u0442\u0435\u0432\u044b\u0445 \u0441\u0435\u0440\u0432\u0438\u0441\u043e\u0432 (HTTP, SMTP, POP3, FTP, \u0438 \u0442.\u0434.) \u0438 \u043e\u043f\u044b\u0442 \u0438\u0445 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f; \r\n\u0423\u043c\u0435\u043d\u0438\u0435 \u0432\u044b\u0440\u0430\u0436\u0430\u0442\u044c \u0441\u0432\u043e\u0438 \u043c\u044b\u0441\u043b\u0438 \u0441 \u043f\u043e\u043c\u043e\u0449\u044c\u044e \u043f\u0438\u0441\u044c\u043c\u0435\u043d\u043d\u043e\u0433\u043e \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u043e\u0433\u043e; \u0411\u043e\u043b\u044c\u0448\u0438\u043c \u043f\u043b\u044e\u0441\u043e\u043c \u0431\u0443\u0434\u0435\u0442 \u043d\u0430\u043b\u0438\u0447\u0438\u0435 \u043e\u043f\u044b\u0442\u0430 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0442\u0435\u0441\u0442\u043e\u0432 \u043d\u0430 Selenium \u0438 \u0431\u0430\u0437\u043e\u0432\u044b\u0435 \u0437\u043d\u0430\u043d\u0438\u044f Python \u0438 Perl. \r\n\r\n\u0423\u0441\u043b\u043e\u0432\u0438\u044f \u0440\u0430\u0431\u043e\u0442\u044b: \r\n\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043c\u0435\u0434\u0438\u0446\u0438\u043d\u0441\u043a\u043e\u0435 \u0441\u0442\u0440\u0430\u0445\u043e\u0432\u0430\u043d\u0438\u0435 + \u0441\u0442\u043e\u043c\u0430\u0442\u043e\u043b\u043e\u0433\u0438\u044f; \xab\u0411\u0435\u043b\u0430\u044f\xbb \u0437\u0430\u0440\u0430\u0431\u043e\u0442\u043d\u0430\u044f \u043f\u043b\u0430\u0442\u0430;\r\n\u041a\u043e\u043c\u0444\u043e\u0440\u0442\u043d\u044b\u0435 \u0443\u0441\u043b\u043e\u0432\u0438\u044f \u0442\u0440\u0443\u0434\u0430, \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0435 \u043e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u0435 \u0438 \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438;\r\n\u0412\u043e\u0437\u043c\u043e\u0436\u043d\u043e\u0441\u0442\u044c \u0440\u0430\u0431\u043e\u0442\u044b \u0441 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430\u043c\u0438, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u044e\u0442\u0441\u044f \u043a\u0440\u0443\u043f\u043d\u0435\u0439\u0448\u0438\u043c\u0438 \u0432 \u043c\u0438\u0440\u0435 \u0441\u0435\u0440\u0432\u0438\u0441-\u043f\u0440\u043e\u0432\u0430\u0439\u0434\u0435\u0440\u0430\u043c\u0438 \u0438 \u0442\u0435\u043b\u0435\u043a\u043e\u043c\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u043c\u0438 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u044f\u043c\u0438. \r\n\r\n\u0417\u0430\u0440\u0430\u0431\u043e\u0442\u043d\u0430\u044f \u043f\u043b\u0430\u0442\u0430 60-75 \u0442\u044b\u0441. \u0440\u0443\u0431. \r\n\r\n\u0420\u0435\u0437\u044e\u043c\u0435 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u043d\u0430 email: nataly.kazakova@suhorukov.com'
             ,
              u'link': u'http://www.facebook.com/photo.php?fbid=465376216835501&set=a.366776633362127.88495.340250572681400&type=1'
             , u'object_id': u'465376216835501', u'story_tags': {
             u'0': [{u'length': 13, u'offset': 0, u'type': u'user', u'id': u'100001892712878',
                     u'name': u'Golneva  Olya'}],
             u'21': [{u'length': 37, u'offset': 21, u'type': u'page', u'id': u'340250572681400',
                      u'name': u'\u041a\u0430\u0434\u0440\u043e\u0432\u043e\u0435 \u0410\u0433\u0435\u043d\u0442\u0441\u0442\u0432\u043e \u0410\u043b\u0435\u043a\u0441\u0435\u044f \u0421\u0443\u0445\u043e\u0440\u0443\u043a\u043e\u0432\u0430'}]}
             , u'created_time': u'2012-10-10T09:41:49+0000', u'updated_time': u'2012-10-10T09:41:49+0000',
              u'type': u'photo',
              u'id': u'100001892712878_478780305489886', u'status_type': u'shared_story',
              u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'}, {
             u'picture': u'http://external.ak.fbcdn.net/safe_image.php?d=AQC9Deh-9L0n2PNb&w=90&h=90&url=http%3A%2F%2Ffile.podfm.ru%2F1%2F10%2F106%2F1063%2Fimages%2Fpod_333.jpg%3F2'
             , u'from': {u'category': u'News/media',
                         u'name': u'\u0420\u0443\u043d\u0435\u0442\u043e\u043b\u043e\u0433\u0438\u044f',
                         u'id': u'233266153309'},
             u'name': u'\u0428\u0430\u0445\u0430\u0440 \u0412\u0430\u0439\u0441\u0435\u0440, \u043e\u0441\u043d\u043e\u0432\u0430\u0442\u0435\u043b\u044c GetTaxi/ \u0410\u043d\u0430\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430 \xab\u0420\u0443\u043d\u0435\u0442\u043e\u043b\u043e\u0433\u0438\u044f\xbb...'
             , u'application': {u'name': u'HootSuite', u'id': u'183319479511'}, u'comments': {u'count': 3, u'data': [
                     {u'created_time': u'2012-10-11T02:23:20+0000',
                      u'message': u'\u0421\u0440\u0430\u0437\u0443 \u0432\u0438\u0434\u043d\u043e, \u0447\u0442\u043e \u0447\u0435\u043b\u043e\u0432\u0435\u043a \u0437\u043d\u0430\u0435\u0442 \u0442\u0430\u043a\u0441\u0438 \u0442\u043e\u043b\u044c\u043a\u043e \u0441\u043e \u0441\u0442\u043e\u0440\u043e\u043d\u044b \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440\u0430.'
                     , u'from': {
                     u'name': u'\u0410\u043d\u0442\u043e\u043d \u0412\u0440\u0443\u0431\u043b\u0435\u0432\u0441\u043a\u0438\u0439'
                     , u'id': u'100001276727361'}, u'id': u'233266153309_355650637856296_2133154'},
                     {u'created_time': u'2012-10-11T08:01:25+0000',
                      u'message': u'\u0410\u043d\u0442\u043e\u043d, \u0430 \u043f\u043e\u0447\u0435\u043c\u0443 \u0443 \u0432\u0430\u0441 \u0441\u043b\u043e\u0436\u0438\u043b\u043e\u0441\u044c \u0442\u0430\u043a\u043e\u0435 \u043c\u043d\u0435\u043d\u0438\u0435?'
                     , u'from': {u'category': u'News/media',
                                 u'name': u'\u0420\u0443\u043d\u0435\u0442\u043e\u043b\u043e\u0433\u0438\u044f',
                                 u'id': u'233266153309'}, u'id': u'233266153309_355650637856296_2133832'},
                     {u'created_time': u'2012-10-11T13:08:11+0000',
                      u'message': u'\u041f\u043e\u0442\u043e\u043c\u0443 \u0447\u0442\u043e \u0441\u0430\u043c \u0442\u0430\u043a\u0441\u043e\u0432\u0430\u043b \u043a\u043e\u0433\u0434\u0430 \u0442\u043e, \u0435\u0441\u0442\u044c \u0445\u043e\u0440\u043e\u0448\u0435\u0435 \u0432\u0438\u0434\u0438\u043d\u044c\u0435 \u0447\u0442\u043e \u0442\u0430\u043c \u0438\u0437\u043d\u0443\u0442\u0440\u0438. \u0410 \u0435\u0449\u0435 \u0437\u043d\u0430\u044e \u043a\u0430\u043a \u0432\u0438\u0434\u0438\u0442 \u0441\u0438\u0442\u0443\u0430\u0446\u0438\u044e \u0434\u0438\u0441\u043f\u0435\u0442\u0447\u0435\u0440\u0441\u043a\u0430\u044f \u0441\u043b\u0443\u0436\u0431\u0430 (\u0437\u0430\u043d\u0438\u043c\u0430\u043b\u0441\u044f \u0432\u043d\u0435\u0434\u0440\u0435\u043d\u0438\u0435\u043c \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u0438 \u0443 \u0445\u043e\u0440\u043e\u0448\u0435\u0433\u043e \u0437\u043d\u0430\u043a\u043e\u043c\u043e\u0433\u043e). \u0428\u0430\u0445\u0430\u0440 \u043c\u043e\u0436\u0435\u0442 \u0438 \u043d\u0435 \u0432\u0441\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e \u0432\u0438\u0434\u0438\u0442, \u043d\u043e, \u0431\u0435\u0437\u0443\u0441\u043b\u043e\u0432\u043d\u043e, \u0435\u0441\u0442\u044c \u0447\u0442\u043e \u043f\u043e\u0434\u0447\u0435\u0440\u043f\u043d\u0443\u0442\u044c \u0432 \u0435\u0433\u043e \u0441\u0443\u0436\u0434\u0435\u043d\u0438\u044f\u0445, \u043d\u0430\u0431\u043b\u044e\u0434\u0435\u043d\u0438\u044f\u0445.'
                     , u'from': {
                     u'name': u'\u0410\u043d\u0442\u043e\u043d \u0412\u0440\u0443\u0431\u043b\u0435\u0432\u0441\u043a\u0438\u0439'
                     , u'id': u'100001276727361'}, u'id': u'233266153309_355650637856296_2134468'}]},
             u'actions': [{u'link': u'http://www.facebook.com/233266153309/posts/355650637856296', u'name': u'Comment'},
                     {u'link': u'http://www.facebook.com/233266153309/posts/355650637856296', u'name': u'Like'}],
             u'updated_time': u'2012-10-11T13:08:11+0000', u'caption': u'ow.ly', u'link': u'http://ow.ly/em9cd',
             u'likes': {u'count': 1, u'data': [{u'name': u'Yuri Frolov', u'id': u'100002686011701'}]},
             u'created_time': u'2012-10-10T07:03:51+0000',
             u'message': u'\u0420\u0443\u043d\u0435\u0442\u043e\u043b\u043e\u0433\u0438\u044f(168): \u0428\u0430\u0445\u0430\u0440 \u0412\u0430\u0439\u0441\u0435\u0440, \u043e\u0441\u043d\u043e\u0432\u0430\u0442\u0435\u043b\u044c GetTaxi http://ow.ly/em9cd'
             , u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif', u'type': u'link',
             u'id': u'233266153309_355650637856296', u'status_type': u'shared_story',
             u'description': u'\u0428\u0430\u0445\u0430\u0440 \u0412\u0430\u0439\u0441\u0435\u0440 \u043e \u0442\u043e\u043c, \u043f\u043e\u0447\u0435\u043c\u0443 \u0441\u0442\u043e\u0438\u0442 \u0438\u0434\u0442\u0438 \u0432 \u043c\u043e\u0431\u0438\u043b\u044c\u043d\u0443\u044e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0443, \u0447\u0435\u043c \u043e\u0442\u043b\u0438\u0447\u0430\u044e\u0442\u0441\u044f \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0442\u0435\u043b\u0438 \u043e\u0442 \u043e\u0431\u044b\u0447\u043d\u044b\u0445 \u043b\u044e\u0434\u0435\u0439 \u0438 \u043f\u043e\u0447\u0435\u043c\u0443 \u043c\u0430\u0440\u043a\u0435\u0442\u0438\u043d\u0433 \u0434\u043b\u044f \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430...'}
         , {
             u'picture': u'http://external.ak.fbcdn.net/safe_image.php?d=AQC77S9nXG04MXCh&w=90&h=90&url=http%3A%2F%2Fwww.etoday.ru%2Fuploads%2F2012%2F09%2F27%2FJoelSossaButton.jpg'
             ,
             u'story': u'\u0414\u0430\u043d\u044c\u043a\u0430 \u0410\u0445\u043c\u0435\u0440\u043e\u0432\u0430 shared a link.'
             ,
             u'from': {u'name': u'\u0414\u0430\u043d\u044c\u043a\u0430 \u0410\u0445\u043c\u0435\u0440\u043e\u0432\u0430'
                 ,
                       u'id': u'1314845840'},
             u'name': u'\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444 Joel Sossa (\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u0436\u0443\u0440\u043d\u0430\u043b ETODAY)'
             , u'application': {u'name': u'Share_bookmarklet', u'id': u'5085647995'},
             u'actions': [{u'link': u'http://www.facebook.com/1314845840/posts/462012493849084', u'name': u'Comment'},
                     {u'link': u'http://www.facebook.com/1314845840/posts/462012493849084', u'name': u'Like'}],
             u'updated_time': u'2012-10-09T17:38:23+0000', u'caption': u'www.etoday.ru',
             u'link': u'http://www.etoday.ru/2012/09/fotograf-joel-sossa.php', u'comments': {u'count': 0},
             u'story_tags': {
                 u'0': [{u'length': 15, u'offset': 0, u'type': u'user', u'id': u'1314845840',
                         u'name': u'\u0414\u0430\u043d\u044c\u043a\u0430 \u0410\u0445\u043c\u0435\u0440\u043e\u0432\u0430'}]}
             , u'created_time': u'2012-10-09T17:38:23+0000',
             u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif', u'type': u'link',
             u'id': u'1314845840_462012493849084', u'status_type': u'shared_story',
             u'description': u'\u0414\u0436\u043e\u0435\u043b \u0421\u043e\u0441\u0441\u0430 (Joel Sossa) - 23-\u043b\u0435\u0442\u043d\u0438\u0439 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444 \u0438\u0437 \u041c\u0435\u043a\u0441\u0438\u043a\u0438, \u0447\u044c\u0438 \u0440\u0430\u0431\u043e\u0442\u044b \u043f\u043e\u043b\u043d\u044b \u0441\u043e\u043b\u043d\u0446\u0430, \u043c\u043e\u043b\u043e\u0434\u043e\u0441\u0442\u0438, \u0441\u0432\u043e\u0431\u043e\u0434\u044b \u0438 \u043b\u044e\u0431\u0432\u0438. \u0414\u0436\u043e\u0435\u043b \u0432\u0434\u043e\u0445\u043d\u043e\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043c\u0443\u0437\u044b\u043a\u043e\u0439 \u0442\u0430\u043a\u0438\u0445 \u0433\u0440\u0443\u043f\u043f \u043a\u0430\u043a Angus Stone, Devendra Banhart, The Head and'}
         , {u'from': {u'name': u'Marina Zakhozheva', u'id': u'100001041793806'},
            u'actions': [
                    {u'link': u'http://www.facebook.com/100001041793806/posts/469830046395051', u'name': u'Comment'},
                    {u'link': u'http://www.facebook.com/100001041793806/posts/469830046395051', u'name': u'Like'},
                    {u'link': u'http://vk.com/ejina_vrajina', u'name': u'Ezhina on vk.com'}],
            u'updated_time': u'2012-10-10T07:21:58+0000', u'application': {u'name': u'VK', u'id': u'128749580520227'},
            u'comments': {u'count': 2, u'data': [{u'created_time': u'2012-10-10T06:44:13+0000',
                                                  u'message': u'\u0412 \u041d\u043e\u0432\u043e\u0441\u0438\u0431?',
                                                  u'from': {
                                                      u'name': u'\u041c\u0430\u0440\u0438\u043d\u0430 \u041a\u043e\u043d\u0435\u0432\u0441\u043a\u0438\u0445'
                                                      , u'id': u'1781672238'},
                                                  u'id': u'100001041793806_469830046395051_99479405'},
                    {u'created_time': u'2012-10-10T07:21:58+0000',
                     u'message': u'\u0414\u0430, \u044f \u0442\u0435\u0431\u0435 \u0412\u041a \u043f\u0438\u0441\u0430\u043b\u0430 \u044d\u0442\u043e)'
                    , u'from': {u'name': u'Marina Zakhozheva', u'id': u'100001041793806'},
                     u'id': u'100001041793806_469830046395051_99479481'}]}, u'created_time': u'2012-10-09T13:47:45+0000'
             ,
            u'message': u'bileti vz9ti! 29.12 pribivayu!!', u'type': u'status',
            u'id': u'100001041793806_469830046395051',
            u'status_type': u'app_created_story',
            u'icon': u'http://photos-d.ak.fbcdn.net/photos-ak-snc7/v85006/107/128749580520227/app_2_128749580520227_7859.gif'}
         , {u'picture': u'http://photos-a.ak.fbcdn.net/hphotos-ak-ash3/562003_432700063454024_736771858_s.jpg',
            u'story': u"Denis Proskuryakov shared Radio Record's photo.",
            u'from': {u'name': u'Denis Proskuryakov', u'id': u'100001247606379'}, u'name': u'Wall Photos',
            u'application': {u'name': u'Photos', u'id': u'2305272732'}, u'comments': {u'count': 0},
            u'actions': [
                    {u'link': u'http://www.facebook.com/100001247606379/posts/354963991262450', u'name': u'Comment'},
                    {u'link': u'http://www.facebook.com/100001247606379/posts/354963991262450', u'name': u'Like'}],
            u'properties': [
                    {u'text': u'Radio Record', u'href': u'http://www.facebook.com/radiorecord?ref=stream',
                     u'name': u'By'}],
            u'caption': u'\u041f\u043e\u043d\u0435\u0434\u0435\u043b\u044c\u043d\u0438\u043a...\r\n\u0410 \u043a\u0430\u043a \u0432\u044b \u0441\u0435\u0431\u044f \u0447\u0443\u0432\u0441\u0442\u0432\u0443\u0435\u0442\u0435 \u0432 \u043f\u043e\u043d\u0435\u0434\u0435\u043b\u044c\u043d\u0438\u043a?'
             ,
            u'link': u'http://www.facebook.com/photo.php?fbid=432700063454024&set=a.178846568839376.45951.123133364410697&type=1'
             , u'object_id': u'432700063454024', u'story_tags': {u'0': [
                     {u'length': 18, u'offset': 0, u'type': u'user', u'id': u'100001247606379',
                      u'name': u'Denis Proskuryakov'}], u'26': [
                     {u'length': 12, u'offset': 26, u'type': u'page', u'id': u'123133364410697',
                      u'name': u'Radio Record'}]},
            u'created_time': u'2012-10-09T13:21:48+0000', u'updated_time': u'2012-10-09T13:21:48+0000',
            u'type': u'photo',
            u'id': u'100001247606379_354963991262450', u'status_type': u'shared_story',
            u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'}]
}