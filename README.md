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



## Papers For Review

* [Retrospective Provenance and YesWorkflow](https://github.com/yesworkflow-org/yw-tapp-15-recon/blob/master/yw-prov-recon-tapp15-submitted.pdf)
* [Displaying and Querying Scientific Workflow Provenance](https://www.researchgate.net/publication/220965045_Provenance_Browser_Displaying_and_Querying_Scientific_Workflow_Provenance_Graphs)
* [More about YesWorkflow](http://www.ijdc.net/article/view/10.1.298/401)
