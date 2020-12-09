The purpose of this project was to write a map-reduce program to equijoin tables from a large dataset. This file describes the functions used in the equijoin.java file. 

My mapper function describes the key-value pair I used for this assignment. It starts by retrieving each line and splitting the contents so I can extract certain features. I extract the primary key of each row (the values 1-4) and use that as my key for the key-value pair. The value is simply the row of data. This information is sent to the reduce function. 

The reduce function first extracts the table primary keys (1-4) for comparison. A flag boolean value is used to do this. The function then compares the two values, and if they are different the text if deleted, if not the rows are joined together. This is done for each row in the dataset with a loop. Lastly, the function writes the lines side by side when appropriate as output. 

The driver function puts everything together. It connects to hadoop, sets up a new configuration, and calls the mapper and reducer classes. It sets up the input and output paths as well. 

For more information on this project, please refer to the "CSE 512 Assignment 3.pdf" file.
