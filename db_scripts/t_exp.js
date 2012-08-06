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
        var text = x['message'];
        if (text == 'No Post Title') {
            db.messages.update({'_id':x['_id']}, {'$set':{'message':null}});
            count_message_null++;
        }else{
            var arr = text.split(' ');
            db.messages.update({'_id':x['_id']}, {'$set':{'message':arr}});
        }

    });
    print('messages_with_null:'+count_message_null);
    db.message_stat.insert({'date':new Date(),'messages_with_null':count_message_null});
    db.messages.ensureIndex({'message':1})
};

process_messages(0, 16892566);
