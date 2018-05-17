package test;


import edu.stanford.nlp.pipeline.StanfordCoreNLPClient;
import edu.stanford.nlp.pipeline.Annotation;

import org.apache.storm.Config;

import org.apache.storm.LocalCluster;
import org.apache.storm.LocalDRPC;
import org.apache.storm.StormSubmitter;

import org.apache.storm.drpc.LinearDRPCTopologyBuilder;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;


import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import java.util.*;

public class NLPServer {

    public static class NLPServerBolt extends BaseBasicBolt {

        public void execute(Tuple tuple, BasicOutputCollector collector) {

            Object id = tuple.getValue(0);
            String text = tuple.getString(1);

            Properties props = new Properties();
            props.setProperty("annotators", "ner, lemma");
            StanfordCoreNLPClient pipeline = new StanfordCoreNLPClient(props, "http://localhost", 9000, 2);


            Annotation document = new Annotation(text);

            pipeline.annotate(document);
            //System.out.println(document.toString());
            collector.emit(new Values(id, document.toShorterString()));
            collector.emit(new Values(id, document.toShorterString()));
        }

        public void declareOutputFields(OutputFieldsDeclarer declarer) {
            declarer.declare(new Fields("id", "annotated"));
        }
    }



    public static LinearDRPCTopologyBuilder construct() {
        LinearDRPCTopologyBuilder builder = new LinearDRPCTopologyBuilder("annotate");
        builder.addBolt(new NLPServerBolt(), 4);
        return builder;
    }

    public static void main(String[] args) throws Exception {
        LinearDRPCTopologyBuilder builder = construct();


        Config conf = new Config();

        if (args == null || args.length == 0) {
            conf.setMaxTaskParallelism(1);
            LocalDRPC drpc = new LocalDRPC();
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("reach-drpc", conf, builder.createLocalTopology(drpc));

            String[] to_annotate = new String[]{ "Hello Mr. Sandman.", "Kim would like a bigger ice-cream than Trump has.", "Kim Jong-Il is a vilain that lives in North Korea."};
            for (String sentence: to_annotate) {
                System.out.println("Annotation of " + sentence+ ": \n" + drpc.execute("annotate", sentence));
            }

            cluster.shutdown();
            drpc.shutdown();
        }
        else {
            conf.setNumWorkers(1);
            StormSubmitter.submitTopologyWithProgressBar(args[0], conf, builder.createRemoteTopology());
        }
    }
}
