## Updating GHCR ##
Updating the GHCR will allow the nlp-suite-runner to pull the latest version of the repository you're currently working on, allowing testing and execution of frontend and backend together.

## 1. Save Local Changes ##
Make sure you are **navigated to the correct directory** with the Dockerfile (in this case you must be in the nlp-suite-agent). The image will be created based on the current local version, so there is no need to push to GitHub during testing phases.

## 2. Create Local Docker Image ##
Create an image
```bash
docker build -t ghcr.io/nlp-suite/nlp-suite-agent:main .
```
This command uses the Dockefile instructions to create an image of your local repository. This image will be tagged as `ghcr.io/nlp-suite/nlp-suite-agent:main`. It will be stored in the local Docker registry on your machine.

## 3. Login to your account on the GHCR ##
A) Create a personal access token for your GitHub account. You can do this on GitHub by navigating to Settings>Developer Settings>Tokens(Classic)
Make sure your token has **full control of private repos** as well as **full control of projects**

B) Export this person access token to your system's environment variables. You can this by this command:
```bash
export GHCR_TOKEN={insert your token here}
```
C) Login to the GHCR
```bash
echo $GHCR_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```
Replacing USERNAME with your GitHub username
