SET sql_mode = STRICT_ALL_TABLES;

DROP TABLE IF EXISTS Workflow;
DROP TABLE IF EXISTS Version;
DROP TABLE IF EXISTS Runs;
DROP TABLE IF EXISTS Workflow_Data;
DROP TABLE IF EXISTS Users;


CREATE TABLE Workflow(
	workflow_id INT NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(workflow_id)
) ENGINE = InnoDB;
	
CREATE TABLE Version(
	version_num INT NOT NULL, 
	workflow_id INT NOT NULL,
	PRIMARY KEY(workflow_id),
	FOREIGN KEY (workflow_id) REFERENCES Workflow(workflow_id)
) ENGINE = InnoDB;

CREATE TABLE Runs(
	version_num INT NOT NULL,
	run_num INT NOT NULL,
	graph_output LONGBLOB NOT NULL,
	recon_output VARCHAR(255) NOT NULL,
	PRIMARY KEY(version_num),
	FOREIGN KEY(version_num) REFERENCES Version(version_num)
) ENGINE = InnoDB;

CREATE TABLE Workflow_Data(
	workflow_id INT NOT NULL,
	version_num INT NOT NULL,
	run_num INT NOT NULL,
	file_uri VARCHAR(255) NOT NULL,
	PRIMARY KEY(workflow_id),
	FOREIGN KEY (workflow_id) REFERENCES Workflow(workflow_id)
) ENGINE = InnoDB;

CREATE TABLE Users( 
	username VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	is_admin BOOL NOT NULL,
	email VARCHAR(255) NOT NULL,
	PRIMARY KEY (username)
) ENGINE = InnoDB;
