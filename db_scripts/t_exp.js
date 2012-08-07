/**
 * Created by PyCharm.
 * User: Alesha
 * Date: 04.08.12
 * Time: 13:14
 * To change this template use File | Settings | File Templates.
 */
/**
 * some analytic data evaluation for messages loaded
 */
/**
 * creating m_users collection with users data retrieving from tweets and some process this tweets
 */
get_users_from_text = function(skip, limit, add_or_set) {
//    db.m_users.drop();
//    db.createCollection('m_users');
//    db.m_users.ensureIndex({'name':1}, {unique:true});
    print("retrieving users with messages skip "+skip+" limit "+limit);
    var result = null;
    if (skip == 0) {
        result = db.messages.aggregate(
            {$limit:limit},
            {$project:{_id:0,user:1}},
            {$group:{_id:'$user'}}
        );
    } else {
        result = db.messages.aggregate(
            {$skip:skip}, {$limit:limit},
            {$project:{_id:0,user:1}},
            {$group:{_id:'$user'}}
        );
    }

    if (!result['ok']) {
        printjson(result);
        return null;
    }
    print('result was get processing...');
    result.forEach(function(x) {
        printjson(x);
        if (add_or_set == '$add') {
            var saved_user = db.m_users.findOne({'name':x['_id']});
            db.m_users.update(
                {'name':x['_id']}
                , {'$set':
                {'words_per_user':x['words_per_user'] + saved_user['words_per_user'],
                    'messages':sum_of_messages(sum_of_user_messages(x['_id']), saved_user['messages'])
                }
                }
                , true);
        }
        else {
            db.m_users.update(
                {'name':x['_id']}
                , {'$set':
                {'words_per_user':x['words_per_user'],
                    'messages':sum_of_user_messages(x['_id'])
                }
                }
                , true);
        }
    });
};

/**
 * returning sum of all messages which user say, sum of words for this user, sum of unique words
 * @param user_name
 */
sum_of_user_messages = function(user_name) {
    var sum = 0;
    var sum_words = 0;
    var sum_words_unique = 0;

    db.messages.find({user:user_name}).forEach(function(x) {
        if (!x) {
            printjson(x);
        } else {
            sum++;
            if (x['message']) {
                sum_words += x['message'].length;
                sum_words_unique += get_words_unique(x['message']).length;
            }
        }
    });

    return {'sum':sum,'sum_words':sum_words,'sum_words_unique':sum_words_unique};
};

/**
 * retuning sum of messages
 * @param mess1
 * @param mess2
 */

sum_of_messages = function(mess1, mess2) {
    mess1['sum'] = mess1['sum'] + mess2['sum'];
    mess1['sum_words'] = mess1['sum_words'] + mess2['sum_words'];
    mess1['sum_words_unique'] = mess1['sum_words_unique'] + mess2['sum_words-unique'];
    return mess1;
};
/**
 * realizing add to set operation
 * @param array
 * @param element
 */
add_to_set = function(array, element) {
    if (array.indexOf(element) == -1) {
        array[array.length] = element;
    }
    return array;
};
/**
 * returning set of words
 * @param message
 */
get_words_unique = function(message) {
    s = [];
    for (i = 0; i < message.length; i++) {
        s = add_to_set(s, message[i]);
    }
    return s;
};
/**
 * deprecated
 * @param count
 * create clone collection for messages
 */
get_clone_little = function(count) {
    //getting little clone of messages
    //also uniques messages
    if (count > db.messages.count()) {
        print('count to clone is big than all count');
        return null;
    }
    db.messages_clone.drop();
    db.createCollection('messages_clone');
    db.messages_clone.ensureIndex({'message':1}, {'unique':true});
    for (i = 0; i < count; i++) {
        var message = db.messages.findOne();
        db.messages_clone.insert(message);
    }
};


/**
 * now it is retrieving users from messages with that schema:
 * 1) username
 * 2) his messages - all messages, all words, unique words. 
 */
var step = 10000;

for (var i =0 ; i <= db.messages.count() - step; i += step) {
    get_users_from_text(i, step, '$add')
}


