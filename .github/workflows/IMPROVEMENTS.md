# Global CICD suggestions for improvements

## Ideas for making the CI Better

### Isolating service dependencies with specialized virtual environments

**Purpose** As services grow increasingly specialized and utilize complex, distinct dependencies, managing these requirements globally e.g., by concatenating & compiling all the `services/**/requirements.in` in `requirements.services.txt` before applying them to library-sensitive steps such as **security** checks can lead to conflicts. This section outlines a potential improvement for isolating service dependencies using service-specific virtual environments.

Potential Workflow :

1. Service-Specific Virtual Environments:
   - Each service will have a dedicated virtual environment (venv) to manage its dependencies independently.
   - Dependencies for each service will be installed locally based on its requirements.txt file.
2. Automating Dependency Management:
   - Create and activate a venv for each service
   - Install dependencies from the service's `requirements.txt`
   - Run dependency-sensitive tasks, like security cehcks within the specific venv.
   - [Idea/question] Potentially cache the venvs & downstream the dependency-sensitive tasks using these caches?

Drawbacks:

- Increased disk usage for the venvs.
- Maintenance overhead: Manage multiple environments can increase complexity
- Performance: slightly slower CI/CD pipelines due to the setup of multiple venvs.

### Implementing taskfile to compile all the repo's requirements.in and running this in each branchs' ci during push

Goals :

- Make sure a developer will stabilize their python requirements by pinning the relevant versions.
- Historize and track in each branch the changes in python library requirements, test them in the ci before merging to master.
- Work with requirements.\*.txt directly instead of performing `pip-compile` in the ci.

Drawbacks :

- Need to install taskfile in the ci images in order to easily integrate these steps if needed.
- If we don't want to use these scripts/recipes in the ci, how do you automate their application to the repo's merge requests and/or branch pushes so that the requirements.\*.txt are fresh and ready to be used in the ci directly.
