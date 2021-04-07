# Doclab Crawler

## Setup and Installation

### Prerequisites
In order to run the crawler locally, you will need to have
**Docker Desktop** installed on your machine.
Link: https://www.docker.com/products/docker-desktop

### Building the containers
We use Docker Compose in order to spin up and orchestrate the
required containers to run the crawler locally. First we need
to build Python image used by the crawler tasks. Do this using the
following command:

```
docker-compose build
```

### Running the containers
To run the project, start up the containers using the following
command:

```
docker-compose up
```

This can be run as a daemon process by passing the `-d` argument.

This will create bridge network, spin up the DB container and the
task containers. The MySQL container will have a schema created automatically
on its first run so may take a few minutes before becoming active.


In order to destroy the containers, run the following command:

```
docker-compose down
```

This will destroy all containers used to run the project. The populated
DB will remain on your host machine in the projects `./docker/db/data`
directory.
