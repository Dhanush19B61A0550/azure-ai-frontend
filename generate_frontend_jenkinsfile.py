import os
import openai
import subprocess

API_KEY = "2PmPHTJm6RDsnRJ21l3OFZBYDIQA7wc0ay04vuIxpKjYaooTAhEWJQQJ99BBACYeBjFXJ3w3AAABACOGbnuZ"
BASE_URL = "https://d-o-ai.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-4o"
API_VERSION = "2023-12-01-preview"

openai_client = openai.AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=BASE_URL,
    api_version=API_VERSION
)

repo_path = r"C:\Users\MTL1027\Downloads\azure-ai-frontend"
jenkinsfile_path = os.path.join(repo_path, "Jenkinsfile")

prompt = """Generate a Jenkinsfile with the following conditions:
- The response should contain only valid Jenkinsfile syntax.
- Do NOT include Markdown formatting like 'groovy' or 'sh' at the start or end.
- The response should start directly with 'pipeline {'.
- The pipeline should have four stages: Install, Build, Test, and Deploy.
- The Install stage should run 'npm install'.
- The Build stage should run 'npm run build'.
- The Test stage should run 'npm test --passWithNoTests || exit /b 0' to prevent failure if no tests exist.
- The Deploy stage should deploy the built frontend files to Azure App Service.
  - First, zip the 'build/' directory before deployment using:
    - 'powershell Compress-Archive -Path build\\* -DestinationPath build.zip -Force'.
  - Use 'build.zip' as the deployment source.
  - The Azure Resource Group and Web App Name should be retrieved from Jenkins credentials:
    - RESOURCE_GROUP = credentials('RESOURCE_GROUP_NAME')
    - WEB_APP_NAME = credentials('WEB_APP_NAMES')
  - In the Deploy stage, use the following Azure CLI command to deploy:
    - 'az webapp deployment source config-zip --resource-group %RESOURCE_GROUP_NAME% --name %WEB_APP_NAMES% --src build.zip'.
- Ensure proper environment variable usage in the Jenkinsfile for Azure CLI commands.
- Replace 'sh' with 'bat' for Windows compatibility.
"""


try:
    print("⏳ Generating Jenkinsfile using Azure OpenAI...")
    response = openai_client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )

    jenkinsfile_content = response.choices[0].message.content.strip()
    jenkinsfile_content = jenkinsfile_content.replace('sh ', 'bat ')

    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"❌ Repository path not found: {repo_path}")

    with open(jenkinsfile_path, "w") as file:
        file.write(jenkinsfile_content + "\n")

    print(f"✅ Jenkinsfile created at {jenkinsfile_path}")

    print("⏳ Adding and committing Jenkinsfile...")
    subprocess.run(["git", "-C", repo_path, "add", "Jenkinsfile"], check=True)

    status_output = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"], capture_output=True, text=True)

    if status_output.stdout.strip():
        subprocess.run(["git", "-C", repo_path, "commit", "-m", "Auto-generated Jenkinsfile"], check=True)
        subprocess.run(["git", "-C", repo_path, "push", "origin", "main"], check=True)
        print("🚀 Jenkinsfile successfully pushed to GitHub!")
    else:
        print("⚠️ No changes detected. Skipping commit and push.")

except Exception as e:
    print(f"❌ Error generating or pushing Jenkinsfile: {e}")