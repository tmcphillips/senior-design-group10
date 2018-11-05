SET sql_mode = STRICT_ALL_TABLES;

DROP TABLE IF EXISTS Workflow;
DROP TABLE IF EXISTS Versions;
DROP TABLE IF EXISTS Run;
DROP TABLE IF EXISTS Workflow_Data;
DROP TABLE IF EXISTS Users;


CREATE TABLE Workflow(
	workflow_id INT NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(workflow_id)
) ENGINE = InnoDB;
	
CREATE TABLE Versions(
	version_num INT NOT NULL, 
	workflow_id INT NOT NULL,
	date_modified TIMESTAMP NOT NULL,
	PRIMARY KEY(workflow_id, version_num),
	FOREIGN KEY (workflow_id) REFERENCES Workflow(workflow_id)
) ENGINE = InnoDB;

CREATE TABLE Run(
	workflow_id INT NOT NULL,
	version_num INT NOT NULL,
	run_num INT NOT NULL,
	graph_output LONGBLOB NOT NULL,
	recon_output LONGBLOB NOT NULL,
	PRIMARY KEY(workflow_id, version_num, run_num),
	FOREIGN KEY(workflow_id, version_num) REFERENCES Versions(version_num)
) ENGINE = InnoDB;

CREATE TABLE Workflow_Data(
	workflow_id INT NOT NULL,
	version_num INT NOT NULL,
	run_num INT NOT NULL,
	file_uri VARCHAR(255) NOT NULL,
	PRIMARY KEY(workflow_id),
	FOREIGN KEY (workflow_id) REFERENCES Workflow(workflow_id)
) ENGINE = InnoDB;

CREATE TABLE File_Run(
	file_checksum VARCHAR(255) NOT NULL,
	workflow_id INT NOT NULL,
	version_num INT NOT NULL,
	run_num INT NOT NULL,
	date_modified TIMESTAMP NOT NULL,
	file_uri VARCHAR(255) NOT NULL,
	[filename] VARCHAR(255) NOT NULL,
	PRIMARY KEY(file_checksum,workflow_id,version_num,run_num)

) ENGINE = InnoDB;

CREATE TABLE Users( 
	username VARCHAR(255) NOT NULL,
	pswd VARCHAR(255) NOT NULL,
	is_admin BOOL NOT NULL,
	email VARCHAR(255) NOT NULL,
	PRIMARY KEY (username)
) ENGINE = InnoDB;