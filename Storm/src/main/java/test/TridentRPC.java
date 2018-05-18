package test;

import org.apache.storm.trident.operation.BaseFunction;
import org.apache.storm.trident.operation.TridentCollector;
import org.apache.storm.trident.tuple.TridentTuple;
import org.apache.storm.tuple.Values;

public class TridentRPC {


    public class NLPfetch extends BaseFunction {
        public void execute(TridentTuple tuple, TridentCollector collector) {
            int a = tuple.getInteger(0);
            String text = tuple.getString(1);
            collector.emit(new Values(a + b));
        }
    }
}
