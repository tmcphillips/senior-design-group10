# senior-design-group10
Document sharing between team members, sponsors, faculty advisors, and DAB members for the Senior Design Software Project

## Setting up development environment

1. Insure Python 3.6 or greater is installed
2. Install pip3 (pip for windows)
3. Install dependencies with `pip3 install`: `django==2.1.3`, `djangorestframework`, `pillow`
4. Optional: If you would like to deploy the server and are running a UNIX OS (OS X, linux, etc), open your `.profile` or `.bash_profile`, create a new config `DJANGO_DEBUG=""` and run `source .profile` or `source .bash_profile`.

## Code Review

When merging, be sure to select the `Squash and Merge` option on Github.

#### Requester

Before pushing your feature branch to remote, be sure to use `pull --rebase` with master to avoid merge conflicts on the pull request and squash merge commits like `merged with <branch_name>`.

#### Reviewer

When someone requests you review their work, make sure you get a copy of that person's pull request and test their code locally. To get the pull request as a new branch, follow [these steps](https://help.github.com/articles/checking-out-pull-requests-locally/#modifying-an-inactive-pull-request-locally)

Summary:

Use `git fetch origin pull/<Merge Number>/head:<Name of new Branch>`, then checkout the newly created branch


## Setting up YesWorkflow dev Environment

YesWorkflow is a maven project. To set up the project for development follow these steps:

1. Ensure you have a Java SE 7 or above installed on your device. To see all versions on a mac device and their location, run `$ /usr/libexec/java_home -V`.
2. Set JAVA_HOME to any version that is 1.7 or greater. I.e. on mac `$ export JAVA_HOME="/usr/libexec/java_home -v 1.8"` for Java 8.
3. Ensure [Maven 3.2](https://maven.apache.org/install.html) or above is installed on your device.
4. Run `$ git clone https://github.com/aniehuser/yw-prototypes.git`.
5. Navigate to the newly cloned directory.
6. Open the `pom.xml` file in the project's root directory and edit the following portion to reflect the current java and maven version
```
<!-- Set Java compiler source and target versions -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.5</version>      <!-- This specifies maven version -->
    <configuration>
        <source>1.8</source>    <!-- These specify java version -->
        <target>1.8</target>
    </configuration>
</plugin>
```
7. Save edits made to the `pom.xml` file, and run `$ mvn clean install`. You can now build the project from an intellij or eclipse project!

## Using the YesWorkflow Save CLI command

Most recent version of [YesWorkflow CLI Java implementation](https://github.com/aniehuser/yw-prototypes)

### Building a jar file

You can build a new jar file from the above repository by following these steps:

1. Set up a development environment for yw-prototypes [Setting up YesWorkflow dev Environment](https://github.com/aniehuser/senior-design-group10#setting-up-yesworkflow-dev-environment)
2. Open up a command prompt and navigate to the directory you cloned yw-prototypes into.
3. Run `mvn package`
    1. If you run into issues with tests from YwClient failing, you likely are running an old version YesWorkflow WebComponents on `localhost:8000`. You can terminate this process and the tests will be ignored.
4. The new jar will be placed in the path `<path-to-yw-prototypes>/yw-prototypes/out/artifacts` folder.

You can now execute YesWorkflow CLI as normal. 

### YesWorkflow Save Command and Configurations

YesWorkflow CLI's Save command works by executing and aggregating all YesWorkflow commands and then sending important data up to your deployed YesWorkflow WebComponents instance. To use, one can type in the command prompt

```
java -jar yesworkflow.jar save my_scripty.py
```

You can set configurations manually in the command prompt
```
java -jar yesworkflow.jar save my_scripty.py -c save.serveraddress=http://localhost:8000/
```

For multiple manual configurations, use `-c` flag again
```
java -jar yesworkflow.jar save my_scripty.py -c save.serveraddress=http://localhost:8000/ -c graph.dotfile=out.txt
```

or you can set configurations in a text file named `yw.properties` that you must place in the same directory as your yesworkflow jar file.

```
## Example File Contents ##

save.serveraddress=http://localhost:8000/
save.username=my_username
```

Required configurations to use YesWorkflow Save
+ save.serveraddress *(Only if you are using a YesWorkflow WebComponents that is not hosted on your localhost port 8000)*
+ save.username

#### save.serveraddress

**REQUIRED - Usually**

Set `save.serveraddress` to the DNS/IP address/URL of the server you would like to save a workflow's run to. 
You can view what the server address to set the configuration on YesWorkflow WebComponents instance's Home Page. 
![Image of instance's DNS](demos/tutorials/dns.png)

**NOTE** :: YesWorkflow Save is currently a bit finicky, so, in this example, to save a workflow's run to `localhost:8000` as shown, you would need to include the `http://` before the dns, as well as a trailing `/`. It would look something like `save.serveraddress=http://localhost:8000/`

#### save.username

**REQUIRED**

For security purposes, you must also specify that you are a valid user on the server that you have specified in `save.serveradress`.

To upload a workflow's run, you as a user must first create a new account on the YesWorkflow WebComponents instance you would like to save to. Then, you must specify your username in using this configuration. If your user name is *"george_danger"*, you would have a configuration like `save.username=george_danger`.

#### save.workflow

To create a new, fresh workflow, make sure that no configuration is set for `save.workflow`.

To add a run to an existing workflow, specify the workflow's id. For a workflow with an id of 69
```
save.workflow=69 
```

#### save.title

This is an optional field to set or update the title of a workflow.
```
save.title=This is an example title for a workflow
```


#### save.description

This is an optional field to set or update the description of a workflow.
```
save.description=This is an example description for a workflow
```

#### save.tags

This is a comma delimited list of tags you want to set or update the tags of a workflow.
```
save.tags=fun,science,bill-nye
```

#### Some things to note

YesWorkflow save calls all subsequent commands (extract, model, graph, recon). When calling graph, by default, there will be a dump of a graphviz string to terminal output. To hide this output when calling YesWorkflow save, it's recommended that you use the following configuration
```
graph.dotfile=out.txt
```

This puts the graphviz string into a file so you can see 'save' related content.


## Papers For Review

* [Retrospective Provenance and YesWorkflow](https://github.com/yesworkflow-org/yw-tapp-15-recon/blob/master/yw-prov-recon-tapp15-submitted.pdf)
* [Displaying and Querying Scientific Workflow Provenance](https://www.researchgate.net/publication/220965045_Provenance_Browser_Displaying_and_Querying_Scientific_Workflow_Provenance_Graphs)
* [More about YesWorkflow](http://www.ijdc.net/article/view/10.1.298/401)
