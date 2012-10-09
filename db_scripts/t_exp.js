/**
 * Created by PyCharm.
 * User: Alesha
 * Date: 04.08.12
 * Time: 13:14
 * To change this template use File | Settings | File Templates.
 */
/**
 * retrieving user names in messages collection creating set on this users and storing into users_not_laded
 * @param skip
 * @param limit
 */
get_users_from_text_messages = function(skip, limit) {
    print("retrieving users with messages");
    var result = null;
    if (skip == 0) {
        result = db.messages.aggregate(
            {$limit:limit},
            {$project:{_id:0,user:1}},
            {$group:{_id:'$user'}}
        );
    } else {
        result = db.messages.aggregate(
            {$skip:skip},
            {$limit:limit},
            {$project:{_id:0,user:1}},
            {$group:{_id:'$user'}}
        );
    }
    if (!result['ok']) {
        print('some error');
        printjson(result);
        return null;
    }

    print('result was get processing...');

    result['result'].forEach(function(x) {
        print(x['_id']);
        db.users_not_loaded.insert({'name':x['_id']});

    });
};


db.createCollection('users_not_loaded');
db.users_not_loaded.ensureIndex({'name':1}, {unique:true});

var step = 100000;

for (var i = 0; i <= db.messages.count() - step; i += step) {
    get_users_from_text_messages(i, step)
}
