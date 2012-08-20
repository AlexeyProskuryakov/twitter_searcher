/***
 * some functions for initializing some data in data base.
 * functions:
 * init - initializing all db schema
 * entities -
 */
//initialization of all schema
init = function() {
    db.createCollection('users');
    db.users.ensureIndex({'name_':1}, {unique:true});
    db.createCollection('entities');
    db.createCollection('relations');
    db.createCollection('not_searched');
};
//initializing entities
//some statistic analyse of words with their followers and etc
entities = function(followers_, _followers) {
    print('create entities');
    db.entites.drop();
    db.users.aggregate(
        {$match:{tweets_stat:{$exists:true},followers_count:{$gt:followers_,$lt:_followers}}},
        {$project:{name:1,followers_count:1,tweets_stat:1}},
        {$unwind:'$tweets_stat'},
        {$project:{
            name:1,
            followers_count:1,
            entity:'$tweets_stat.entity',
            type:'$tweets_stat.type',
            freq_all:'$tweets_stat.freq_all',
            tweets_stat:1}},
        {$match:{entity:{$exists:true}}},
        //after all:
        {$group:{
            _id:"$entity",
            followers_count:{$sum:'$followers_count'}, //sum of followers counts in users,  which say this word
            freq_all:{$sum:'$freq_all'}, //sum of frequencies in users which say this word
            type:{$addToSet:'$type'}, //types... may be it will be hash tag and simple word? ha ha :)
            name:{$addToSet:'$name'}} //names of people which say this word
        })['result'].
        forEach(function(x) {
        db.entities.save(x);
    });
};
//creating relation schema of users
//todo may be add to relations some type ne?
relations = function (followers_, _followers, friends_, _friends) {
    print('create relations on users');
    db.relations.drop();
    db.relations.ensureIndex({'from':1,'to':1}, {'unique':true});
    db.users.aggregate(
        {$project:{name:1,followers:1,followers_count:1}},
        {$match:
        {followers_count:{$gt:followers_,$lt:_followers}}
        },
        {$unwind:"$followers"},
        {$project:{
            '_id':0,
            to:'$name',
            from:'$followers'}})
        ['result'].forEach(
        function(x) {
            db.relations.save(x)
        });

    db.users.aggregate(
        {$project:{name:1,friends:1,friends_count:1}},
        {$match:
        {
            friends_count:{$gt:friends_,$lt:_friends}
        }},
        {$unwind:"$friends"},
        {$project:{
            '_id':0,
            to:'$friends',
            from:'$name_'}})
        ['result'].forEach(
        function(x) {
            db.relations.save(x)
        });
};
//create collection for users which never have scrapper in guests
//todo think! about
create_not_searched = function() {
    print('create not searched');
    db.not_searched.drop();
    db.not_searched.ensureIndex({'name':1}, {'unique':true});
    db.users.find().forEach(function(x) {
        var name = x['name_'];
        var friends = x['friends'];
        for (var friend in friends) {
            if (!db.users.findOne({name:friends[friend]})) {
                print('find friend without our serialize ' + friends[friend]);
                db.not_searched.insert({'name':friend});
                print(friends);
            }
        }
    });
};

//initialise differences machine

init_diff_machine = function(first, date_start,date_stop) {
    print(date_start);
    print(date_stop);
    print('init differences');
    users = null;
    if (first) {
        users = db.users.find();
    } else {
        users = db.users.find({$and:[{date_touch_:{$gte:date_start}},{date_touch_:{$lte:date_stop}}]});
    }

    users.forEach(function(x){
        printjson(x);
        db.diffs_users_input.insert({'user_name':x['name_'],'date_touch_':x['date_touch_']});
    })
};

db.system.js.save({_id:'init_diff_machine',value:init_diff_machine});

init_diff_machine(false,new Date('Mon Aug 20 01:37:24 2012'),new Date('2012-08-20T01:37:24.386000'));
