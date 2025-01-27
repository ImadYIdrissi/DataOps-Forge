# Global CI/CD Suggestions for Improvements

## Ideas for Making the CI Better

### Isolating Service Dependencies with Specialized Virtual Environments

**Purpose**: As services grow increasingly specialized and utilize complex, distinct dependencies, managing these requirements globally (e.g., by concatenating and compiling all the `services/**/requirements.in` into `requirements.services.txt` before applying them to library-sensitive steps such as **security** checks) can lead to conflicts. This section outlines a potential improvement for isolating service dependencies using service-specific virtual environments.

**Potential Workflow**:

1. **Service-Specific Virtual Environments**:

   - Each service will have a dedicated virtual environment (venv) to manage its dependencies independently.
   - Dependencies for each service will be installed locally based on its `requirements.txt` file.

2. **Automating Dependency Management**:
   - Create and activate a venv for each service.
   - Install dependencies from the service's `requirements.txt`.
   - Run dependency-sensitive tasks, like security checks, within the specific venv.
   - **[Idea/Question]**: Potentially cache the venvs and downstream dependency-sensitive tasks using these caches?

**Drawbacks**:

- **Increased Disk Usage**: Multiple venvs require additional storage.
- **Maintenance Overhead**: Managing multiple environments can increase complexity.
- **Performance Impact**: Slightly slower CI/CD pipelines due to the setup of multiple venvs.

---

### Implementing Taskfile to Compile All the Repo's `requirements.in` and Running This in Each Branch's CI During Push

**Goals**:

- Ensure developers stabilize their Python requirements by pinning the relevant versions.
- Track and historize changes in Python library requirements on each branch, testing them in the CI before merging to master.
- Work with `requirements.*.txt` directly instead of performing `pip-compile` in the CI.

**Drawbacks**:

- **Dependency on Taskfile**: Need to install Taskfile in the CI images to integrate these steps easily if required.
- **Automation Gap**: If Taskfile scripts/recipes are not used in CI, how do we automate their application to the repo's merge requests and/or branch pushes, ensuring `requirements.*.txt` files are fresh and ready to be used in CI?
