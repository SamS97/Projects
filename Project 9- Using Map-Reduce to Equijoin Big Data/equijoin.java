import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class equijoin {
    
    public static class Map extends Mapper<Object, Text, Text, Text>
    {
    	private Text keyValue = new Text();
        private Text row = new Text();
        
        public void map(Object key, Text value, Context c) throws IOException, InterruptedException
        {
            String line = value.toString();
            String[] val = line.split(","); 
            String keyjoin = val[1]; //primary key number
            
            row.set(line); //Setting the row as the value
            keyValue.set(keyjoin); //Setting primary key as the key
            c.write(keyValue,row); //Writing the key value pair for the reduce function
        } 
    }
    
    public static class Reduce extends Reducer<Text, Text, Text, Text>
    {  
        public void reduce(Text key, Iterable<Text> map_values, Context c) throws IOException, InterruptedException 
        {
        	List<String> write_object = new ArrayList<String>();
            List<String> table1 = new ArrayList<String>();
            List<String> table2 = new ArrayList<String>();
            
            String table1Name = "";
            boolean flag = true;
            String r = new String();
            Text res = new Text();

            for(Text each : map_values)
            {
            	//Retrieving values of line
                String value = each.toString();
                String[] valueSplit = value.split(",");
                
                if(flag == true) 
                {
                    table1Name = valueSplit[0];
                    flag = false;
                }
                if(table1Name == valueSplit[0] ) {
                    table1.add(value);
                }
                else 
                {
                    table2.add(value);
                }
                write_object.add(value);   
            }
            
	    Collections.reverse(write_object);
        Text new_text = new Text("");
        
        //Removing value from table since it does not match
	    if(table1.size() == 0 || table2.size() == 0)
	    {
	    	key.clear();
	    }
	    else
            {	//Writing the output
            	for (int i = 0; i < write_object.size(); i++) 
            	{
                	for (int j = i+1; j < write_object.size(); j++) 
                	{
                    		r = write_object.get(i) + ", " + write_object.get(j);
                    		res.set(r);
                    		c.write(new_text,res);              
                	}  
                
            	}  
            }
        }
    }

    public static void main(String[] args) throws Exception
    {
    	 //Setting up new configuration, calling map and reduce classes, and setting new input and output paths.
         Configuration conf = new Configuration();
         Job job = Job.getInstance(conf, "equijoin");
         job.setJarByClass(equijoin.class);
         job.setMapperClass(Map.class);
         job.setReducerClass(Reduce.class);
         job.setOutputKeyClass(Text.class);
         job.setOutputValueClass(Text.class);
         FileInputFormat.addInputPath(job, new Path(args[0]));
         FileOutputFormat.setOutputPath(job, new Path(args[1]));
         System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

}