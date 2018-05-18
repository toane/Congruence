package test;


import org.apache.storm.Config;

import org.apache.storm.LocalCluster;
import org.apache.storm.LocalDRPC;
import org.apache.storm.StormSubmitter;

import org.apache.storm.drpc.LinearDRPCTopologyBuilder;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;

import org.apache.storm.tuple.Fields;

import java.util.*;



class BoltTest extends ShellBolt implements IRichBolt {

    public BoltTest(){
        super("python", "/home/mathias/bigdata/projet/Congruence/Storm/src/main/python/pyjava/NLPBolt.py");
        Map env = new HashMap();
        env.put("PYTHONPATH", "/bin/");
        this.setEnv(env);
    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {

        declarer.declare(new Fields("id", "annotated"));
    }

    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}



public class PyBolt {



    public static LinearDRPCTopologyBuilder construct() {

        //BoltTest splitBolt = new BoltTest();
        //Map env = new HashMap();
        //env.put("PYTHONPATH", "/bin/");
        //BoltTest.setEnv(env);

        LinearDRPCTopologyBuilder builder = new LinearDRPCTopologyBuilder("annotate");
        builder.addBolt(new BoltTest(), 4);
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

            String[] to_annotate = new String[]{ "Hello Mr. Sandman.", "Kim would like a bigger ice-cream than Trump has."};
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
