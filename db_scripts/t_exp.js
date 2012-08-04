/**
 * Created by PyCharm.
 * User: Alesha
 * Date: 04.08.12
 * Time: 13:14
 * To change this template use File | Settings | File Templates.
 */
process_messages = function(start, count) {
    var count_message_null = 0;
    db.messages.find().skip(start).limit(count).forEach(function (x) {

        if (x['message'] == 'No Post Title') {
            db.messages.update({'_id':x['_id']}, {'$set':{'message':null}});
            printjson(x);
            count_message_null++;
        }
    });
    print('messages_with_null:'+count_message_null);
    db.message_stat.insert({'date':new Date(),'messages_with_null':count_message_null})
};

process_messages(0, 16892566);
