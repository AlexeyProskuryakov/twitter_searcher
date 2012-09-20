/**
 * Created by PyCharm.
 * User: 4ikist
 * Date: 20.09.12
 * Time: 20:20
 * To change this template use File | Settings | File Templates.
 */
print_rel = function (rels) {
    rels.forEach(function (rel) {
        var fid = rel.from;
        fid = db.mc_nodes.findOne({_id:fid});
        var tid = rel.to;
        tid = db.mc_nodes.findOne({_id:tid});
        var weight = rel.weight;
        print(
            fid.content +
                "[" + fid.weight + "]\t---\t" +
                weight +
                "\t--->\t" +
                tid.content + "[" + tid.weight + "]\n\t"+rel['content']+'\n');
    });
};

print_rel(db.mc_relations.find({model_id_:'left_test'}));