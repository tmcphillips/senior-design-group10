# Using the YesWorkflow Save CLI command

YesWorkflow CLI's Save command works by executing and aggregating all YesWorkflow commands and then sending important data up to your deployed YesWorkflow WebComponents instance. To use, one can type in the command prompt

```
java -jar yesworkflow.jar save my_scripty.py
```

You can set configurations manually in the command prompt
```
java -jar yesworkflow.jar save my_scripty.py -c save.serveraddress=localhost:8000
```

For multiple manual configurations, use `-c` flag again
```
java -jar yesworkflow.jar save my_scripty.py -c save.serveraddress=localhost:8000 -c graph.dotfile=out.txt
```

or you can set configurations in a text file named `yw.properties` that you must place in the same directory as your yesworkflow jar file.

```
## Example File Contents ##

save.serveraddress=localhost:8000
save.username=my_username
```

Required configurations to use YesWorkflow Save
+ save.serveraddress *(Only if you are using a YesWorkflow WebComponents that is not hosted on your localhost port 8000)*

# Configurations

## save.serveraddress

**REQUIRED - Usually**

Set `save.serveraddress` to the DNS/IP/URL of the server you would like to save a workflow's run to. 
You can view what the server address to set the configuration on YesWorkflow WebComponents instance's Home Page. 
![Image of instance's DNS](demos/tutorials/dns.png)

## save.username

For security purposes, you must also specify that you are a valid user on the server that you have specified in `save.serveradress`.

To upload a workflow's run, you as a user must first create a new account on the YesWorkflow WebComponents instance you would like to save to. Then, you must specify your username in using this configuration. If your user name is *"bill_nye"*, you would have a configuration like `save.username=bill_nye`.

You don't have to specify a username, but it can save you some time!

## save.workflow

To create a new, fresh workflow, make sure that no configuration is set for `save.workflow`.

To add a run to an existing workflow, specify the workflow's id. For a workflow with an id of 69
```
save.workflow=69 
```

## save.title

This is an optional field to set or update the title of a workflow.
```
save.title=This is an example title for a workflow
```

## save.description

This is an optional field to set or update the description of a workflow.
```
save.description=This is an example description for a workflow
```

## save.tags

This is a comma delimited list of tags you want to set or update the tags of a workflow.
```
save.tags=fun,science,bill-nye
```

## Some things to note

YesWorkflow save calls all subsequent commands (extract, model, graph, recon), which can lead to some messy looking output by default.

We recommend adding the following configurations to your `yw.properties` file to keep things looking neat.
```
graph.dotfile=graphdot-out.txt
recon.factsfile=reconfacts-out.txt
```

This puts some of the default output into files instead of printing it out on your command line.
