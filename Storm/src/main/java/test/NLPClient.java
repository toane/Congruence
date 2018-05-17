package test;

import edu.stanford.nlp.pipeline.StanfordCoreNLPClient;
import edu.stanford.nlp.pipeline.Annotation;

import org.apache.storm.Config;

import org.apache.storm.LocalCluster;
import org.apache.storm.LocalDRPC;
import org.apache.storm.StormSubmitter;

import org.apache.storm.drpc.LinearDRPCTopologyBuilder;

import org.apache.storm.shade.org.apache.commons.io.IOUtils;
import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;


import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.util.*;


public class NLPClient {

    public static class NLPClientBolt extends BaseBasicBolt {

        public void execute(Tuple tuple, BasicOutputCollector collector) {

            Object id = tuple.getValue(0);
            String text = tuple.getString(1);

            Properties props = new Properties();
            props.setProperty("annotators", "ner, lemma");
            try {
                URL url = new URL("http://localhost:9000/?properties=%7B%27annotators%27%3A+%27lemma%27%2C+%27outputFormat%27%3A+%27json%27%7D");
                //RL url = new URL("http://localhost:9000/?properties={\"annotators\": \"ner, lemma\", \"outputFormat\": \"json\"}");
                URLConnection con = url.openConnection();
                HttpURLConnection http = (HttpURLConnection) con;
                http.setRequestMethod("POST"); // PUT is another valid option
                http.setDoOutput(true);

                byte[] out = text.getBytes();

                http.setFixedLengthStreamingMode(out.length);
                http.setRequestProperty("Content-Type", "text/json; charset=UTF-8");
                http.connect();
                try (OutputStream os = http.getOutputStream()) {
                    os.write(out);
                }

                String answer = IOUtils.toString(http.getInputStream(), StandardCharsets.UTF_8);
                collector.emit(new Values(id, answer));
            } catch (java.io.IOException e) {
                collector.emit(new Values(id, "error: " + e.toString()));
            }
        }

        public void declareOutputFields(OutputFieldsDeclarer declarer) {
            declarer.declare(new Fields("id", "annotated"));
        }
    }



  public static LinearDRPCTopologyBuilder construct() {
    LinearDRPCTopologyBuilder builder = new LinearDRPCTopologyBuilder("annotate");
    builder.addBolt(new NLPClientBolt(), 4);
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
