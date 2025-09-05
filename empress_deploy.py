import os

def deploy_to_platforms(intent):
    deployed = []

    if "Etsy" in intent:
        # Placeholder: Etsy deployment logic
        os.system("echo 'EMPRESS: Deploying to Etsy storefront...'")
        deployed.append("Etsy")

    if "TikTok" in intent:
        # Placeholder: TikTok deployment logic
        os.system("echo 'EMPRESS: Publishing to TikTok...'")
        deployed.append("TikTok")

    if not deployed:
        return "No matching platforms found in intent."

    return f"Deployed to: {', '.join(deployed)}"
