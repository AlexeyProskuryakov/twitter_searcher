init = function() {
    db.createCollection('users');
    db.users.ensureIndex({'name':1}, {unique:true});
    db.createCollection('entities');
    db.createCollection('relations');
    db.createCollection('not_searched');
};

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
        {$group:{
            _id:"$entity",
            followers_count:{$sum:'$followers_count'},
            freq_all:{$sum:'$freq_all'},
            type:{$addToSet:'$type'},
            name:{$addToSet:'$name'}}
        })['result'].
        forEach(function(x) {
        db.entities.save(x);
    });
};

relations = function (followers_, _followers, friends_, _friends) {
    print('create relations on users');
    db.relations.drop();
    db.relations.ensureIndex({'from':1,'to':1}, {'unique':true});
    db.users.aggregate(
        {$project:{name:1,followers:1,followers_count:1}},
        {$match:
        {followers_count:{$gt:followers_,$lt:_followers},
        }},
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
            from:'$name'}})
        ['result'].forEach(
        function(x) {
            db.relations.save(x)
        });
};
create_not_searched = function() {
    print('create not searched');
    db.not_searched.drop();
    db.not_searched.ensureIndex({'name':1}, {'unique':true});
    db.users.find().forEach(function(x) {
        var name = x['name'];
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
//init();
//relations(0, 100, 0, 100);
//entities(0, 100);
create_not_searched();
