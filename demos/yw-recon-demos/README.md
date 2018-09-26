# Basic Recon Demo
I outline some of the basics of how recon currently works as of September 26, 2018.

I would not try to execute this python script, it requires the following:
* Interpreted using python3
* matplotlib, pickle, and nltk.corpus downloaded on your local machine

Recon does not require an executable script, just proper file paths. 

All filepaths are relative to the working directory of your terminal. This includes:
* @URI tags in your scripts
* files in your `yw.properties` file
* files specified in the command prompt

## Step 1: Navigate to working directory
Clone or pull this repository and open your terminal. Set this directory as your working directory
`cd /senior-design-group10/demos/yw-recon-demos` 

YesWorkflow can have strange behavior when trying to specify file paths. The program will work as expected when executing commands from the working directory and all file paths are specified with respect to the current working directory. 

## Step 2: Execute recon
There are several ways to get output from YesWorkFlow's `recon` command.

### A) Output to terminal
Execute the following command
`java -jar yw recon yw_recon.py -c recon.factsfile`

This should generate the following output to your terminal
``` 

% FACT: resource(resource_id, resource_uri).
resource(1, 'proj3.pkl').
resource(2, 'inaugural.zip').

% FACT: data_resource(data_id, resource_id).
data_resource(3, 1).
data_resource(5, 2).
data_resource(7, 1).
data_resource(7, 1).

% FACT: uri_variable_value(resource_id, uri_variable_id, uri_variable_value).
```

Of course this can also be piped to a file by appending ` > recon_logs/terminal_recon_facts.txt` to the previous command.

### B) Specify output using terminal
Append `=recon_logs/recon_facts.txt` to the command in [Part A](https://github.com/aniehuser/senior-design-group10/demos/yw-recon-demos/README.md#a-output-to-terminal)

`java -jar yw recon yw_recon.py -c recon.factsfile=recon_logs/recon_facts.txt`

Again, this will put the same output into the `reconfact

Note: `recon_logs/recon_facts.txt` is not magically created. It must already exist. I have already added it to the working directory.

### C) Specify output using configuration file
Creating a `yw.properties` file is outlined in [yw-prototypes](https://github.com/yesworkflow-org/yw-prototypes#store-command-line-options-in-a-ywproperties-file)

Again, `yw.properties` is not created by magic, this must be done manually. 

Ensure that
* `yw.properties` is located in your working directory when executing a YesWorkflow command
* file paths referenced in `yw.properties` are relative to your working directory

I have set up an example `yw.properties` file in this demo. Simply run the recon command with a script to pipe output to the file `recon_logs/properties_recon_facts.txt`.
`java -jar yw recon yw_recon.py`

## Step 3: Uri Variables
You'll notice in [Part A](https://github.com/aniehuser/senior-design-group10/demos/yw-recon-demos/README.md#a-output-to-terminal) the `uri_variable_value` fact has no data. This is an additional feature of the @URI tag in YesWorkflow. You can specify multiply files of similar names using curly braces in the URI in your script. 

If you look in `yw_recon_variables.py`, you'll notice I changed the URI's for some of the annotations. Try running `java -jar yw recon yw_recon_variables.py -c recon.factsfile` and look at the output in `recon_logs/properties_recon_facts.txt` output now. You'll see the `uri_variable_value` facts have now been populated.

## Step 4: Logging
I still have some figuring out to do with logging. Check out the [recon unit test](https://github.com/yesworkflow-org/yw-prototypes/blob/master/examples/simulate_data_collection/simulate_data_collection.py) if you'd like to check out an example of @LOG being used.

