/**
 * Created with PyCharm.
 * User: 4ikist
 * Date: 17.10.12
 * Time: 0:46
 * To change this template use File | Settings | File Templates.
 */
map = function () {
    this.value.forEach(function (x) {
        emit(x, {count:1});
    })
};
reduce = function (key, values) {
    var total = 0;
    for (var i=0;i<values.length;i++){
        total+=values[i].count;
    }
    return {count:total};

};
get_values_weights = function () {
    var res = db.clust.mapReduce(map,reduce,{out:'clust_values'});
    printjson(res)
};

get_values_weights();